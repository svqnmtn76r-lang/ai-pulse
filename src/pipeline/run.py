"""End-to-end article generation pipeline."""

import math
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(".env")

from src.sources.rss_monitor import articles_from_rss
from src.sources.github_releases import articles_from_github
from src.sources.hackernews import stories_from_hackernews
from src.sources.scrapers import articles_from_scrapers
from src.processors.importance_scorer import batch_score_articles
from src.processors.affiliate_matcher import enrich_article_with_products, load_affiliate_catalog
from src.processors.claude_writer import (
    write_article, create_slug, generate_article_content, write_article_file,
)
from src.utils.state_store import SeenArticleStore
from src.analytics.cost_report import init_db
from src.pipeline.topic_pool import replenish_topic_pool

OUTPUT_DIR = Path("output/articles")
PRODUCT_TOPICS = Path("data/product_topics.yml")


def existing_article_slugs() -> set:
    """Slugs already generated, with the 'YYYY-MM-DD-' date prefix stripped, so a
    topic counts as done regardless of which day it was generated on."""
    slugs = set()
    for f in OUTPUT_DIR.glob("*.md"):
        m = re.match(r"\d{4}-\d{2}-\d{2}-(.+)$", f.stem)
        if m:
            slugs.add(m.group(1))
    return slugs


def product_cadence_count(news_count: int) -> int:
    """How many product articles to generate this run.

    Forward match-rate is driven by the commercial:news ratio. With only ONE
    product article per run (the old behaviour) against ~10-26 news articles,
    forward rate was capped at ~4-7%. This targets a commercial *share* instead.

    K is the smallest count making product/(news+product) >= PRODUCT_TARGET_RATIO
    (default 0.25 -> ~20-25% on typical days), clamped to
    [PRODUCT_MIN_PER_RUN (default 1), PRODUCT_MAX_PER_RUN (default 6)] to bound
    API cost and avoid draining the rotation. All three are env-tunable so Hiro
    can dial the rate without code changes.
    """
    target = float(os.environ.get("PRODUCT_TARGET_RATIO", "0.25"))
    target = min(max(target, 0.0), 0.9)
    min_per = int(os.environ.get("PRODUCT_MIN_PER_RUN", "1"))
    max_per = int(os.environ.get("PRODUCT_MAX_PER_RUN", "6"))
    if target <= 0:
        k = min_per
    else:
        # solve k/(news+k) >= target  ->  k >= target*news/(1-target)
        k = math.ceil(target * news_count / (1 - target))
    return max(min_per, min(k, max_per))


def _generate_one_topic(topic: dict, programs: dict, verbose: bool) -> Optional[Path]:
    """Generate a single product article from a topic dict. Returns path or None.

    Reuses the normal path: the topic's product is seeded as the match, so the
    article routes to the comparison/deep_dive template, is centered on (and
    names) the product, gets the product-page affiliate_url from config, one
    in-body block, and the FTC disclosure. The pipeline's reconciler step then
    re-validates the match on the real body (brand>=1).
    """
    product_id = (topic.get("product") or "").strip()
    template_type = (topic.get("type") or "comparison").strip()
    prod = programs.get(product_id, {})
    affiliate_url = (prod.get("affiliate_url") or "").strip()
    if not affiliate_url:
        print(f"  product '{product_id}' has no affiliate_url in config — skipping topic")
        return None

    # Seed the matched product (id/name/url straight from config — never hardcoded).
    matched = [{
        "product_id": product_id,
        "name": prod.get("display_name", product_id),
        "affiliate_url": affiliate_url,
        "match_score": 100,
        "match_reason": "product-topic cadence",
    }]
    article = {
        "title": topic["title"].strip(),
        "summary": "",
        "url": "",
        "source": "product_topic",
        "category": template_type,
        "importance_score": 70,
        "products_matched": matched,
    }

    if verbose:
        print(f"  generating [{template_type}] {product_id}: {article['title']}")

    body = generate_article_content(article, template_type, matched, factual_source=False)
    if body.startswith("[Article generation failed"):
        print(f"  product-article generation failed: {body}")
        return None

    return write_article_file(article, body, matched, template_type)


def generate_product_articles(news_count: int = 0, verbose: bool = True) -> list:
    """Cadence: generate UP TO `product_cadence_count(news_count)` commercial
    articles from the rotating topic list, top-down, skipping any whose output
    already exists (any date). If the rotation runs dry first, logs a reminder
    and stops (no error, no repeat).
    """
    if not PRODUCT_TOPICS.exists():
        if verbose:
            print(f"  (no {PRODUCT_TOPICS} — skipping cadence)")
        return []

    topics = yaml.safe_load(PRODUCT_TOPICS.read_text(encoding="utf-8")) or []
    programs = load_affiliate_catalog().get("programs", {})
    want = product_cadence_count(news_count)
    if verbose:
        print(f"  target {want} product article(s) (news={news_count})")

    written = []
    done_slugs = existing_article_slugs()  # refreshed via the set as we write
    for topic in topics:
        if len(written) >= want:
            break
        title = (topic.get("title") or "").strip()
        if not title:
            continue
        slug = create_slug(title)
        if slug in done_slugs:
            continue
        path = _generate_one_topic(topic, programs, verbose)
        if path:
            written.append(path)
            done_slugs.add(slug)

    if not written:
        print("  rotation exhausted — add topics to data/product_topics.yml")
    return written


def run_pipeline(verbose: bool = True) -> dict:
    """
    Full pipeline: fetch -> score -> match -> write articles.
    Returns summary of execution.
    """
    # Initialize API cost tracking DB
    init_db()

    if verbose:
        print("=" * 60)
        print(f"Starting pipeline at {datetime.utcnow().isoformat()}")
        print("=" * 60)

    summary = {
        "total_fetched": 0,
        "after_scoring": 0,
        "articles_written": 0,
        "errors": 0,
        "files_created": [],
    }

    # Step 0: keep the commercial topic pool fed BEFORE the cadence selects topics,
    # so the run never hits "rotation exhausted". Idempotent + never blocks the run.
    if verbose:
        print("\n[0/4] Replenishing commercial topic pool...")
    summary["topic_pool"] = replenish_topic_pool(verbose=verbose)

    seen_store = SeenArticleStore()

    # Step 1: Fetch articles from all sources
    if verbose:
        print("\n[1/4] Fetching articles from sources...")

    articles = []
    try:
        rss_articles = articles_from_rss()
        if verbose:
            print(f"  RSS: {len(rss_articles)} articles")
        articles.extend(rss_articles)
    except Exception as e:
        print(f"  RSS error: {e}")
        summary["errors"] += 1

    try:
        gh_articles = articles_from_github()
        if verbose:
            print(f"  GitHub: {len(gh_articles)} articles")
        articles.extend(gh_articles)
    except Exception as e:
        print(f"  GitHub error: {e}")
        summary["errors"] += 1

    try:
        hn_articles = stories_from_hackernews()
        if verbose:
            print(f"  Hacker News: {len(hn_articles)} articles")
        articles.extend(hn_articles)
    except Exception as e:
        print(f"  Hacker News error: {e}")
        summary["errors"] += 1

    try:
        scraped_articles = articles_from_scrapers()
        if verbose:
            print(f"  Scrapers: {len(scraped_articles)} articles")
        articles.extend(scraped_articles)
    except Exception as e:
        print(f"  Scrapers error: {e}")
        summary["errors"] += 1

    summary["total_fetched"] = len(articles)
    if verbose:
        print(f"  Total fetched: {summary['total_fetched']}")

    # Step 2: Score articles
    if verbose:
        print("\n[2/4] Scoring articles for importance...")

    scored = batch_score_articles(articles, seen_store)

    # Apply score threshold filter (minimum 40 to exclude off-topic and low quality)
    SCORE_THRESHOLD = 40
    adopted = [a for a in scored if a.get("importance_score", 0) >= SCORE_THRESHOLD]

    # Category gate: package-bump / minor-feature items are thin, no-demand stubs.
    # They are already covered by the auto-populating /claude-code-changelog/ hub,
    # so generating a standalone page per release only dilutes site quality and
    # burns crawl budget. Skip them here (override with STUB_CATEGORIES="" if ever needed).
    STUB_CATEGORIES = {
        c.strip()
        for c in os.environ.get("STUB_CATEGORIES", "sdk_release,feature_update").split(",")
        if c.strip()
    }
    before_gate = len(adopted)
    adopted = [a for a in adopted if a.get("category", "") not in STUB_CATEGORIES]
    stub_skipped = before_gate - len(adopted)
    summary["stub_skipped"] = stub_skipped
    summary["after_scoring"] = len(adopted)

    if verbose:
        print(f"  Total scored: {len(scored)}, Adopted (score >= {SCORE_THRESHOLD}): {before_gate}")
        print(f"  Stub categories skipped ({', '.join(sorted(STUB_CATEGORIES))}): {stub_skipped} -> remaining {summary['after_scoring']}")

    # Step 3: Match to products and enrich
    if verbose:
        print("\n[3/4] Matching articles to affiliate products...")

    enriched = []
    for article in adopted:
        enriched_article = enrich_article_with_products(article)
        enriched.append(enriched_article)

    if verbose:
        print(f"  Enriched: {len(enriched)} articles")

    # Step 4: Generate and write articles
    if verbose:
        print("\n[4/4] Generating and writing articles...")

    skipped_count = 0
    for article in enriched:
        try:
            # Check for duplicates before generating
            article_id = article.get("id", "")

            # Check if already seen (URL-based)
            if article_id and seen_store.exists(article_id):
                if verbose:
                    print(f"  ⊘ Skipping (already seen): {article.get('title')[:40]}...")
                skipped_count += 1
                continue

            # Check if output file already exists (filename-based)
            slug = create_slug(article.get("title", "article"))
            from datetime import datetime as dt_util
            timestamp = dt_util.utcnow().strftime("%Y-%m-%d")
            expected_path = OUTPUT_DIR / f"{timestamp}-{slug}.md"

            if expected_path.exists():
                if verbose:
                    print(f"  ⊘ Skipping (file exists): {expected_path.name}")
                skipped_count += 1
                continue

            # Get matched products
            matched = article.get("products_matched", [])

            # Write article
            filepath = write_article(article, matched)

            if filepath:
                summary["articles_written"] += 1
                summary["files_created"].append(str(filepath))

                if verbose:
                    print(f"  ✓ {filepath.name}")

                # Mark as seen after successful generation
                seen_store.mark_seen(
                    article_id,
                    article.get("source", ""),
                    article.get("title", ""),
                    article.get("url", "")
                )

        except Exception as e:
            print(f"  Error writing article for '{article.get('title')}': {e}")
            summary["errors"] += 1

    if verbose and skipped_count > 0:
        print(f"  Skipped (duplicates): {skipped_count}")

    # Step 5: Cadence — generate enough product (commercial) articles from the
    # rotating topic list to reach the target commercial share (default ~25%),
    # so forward match-rate clears the 20% goal and monetizable coverage grows.
    news_written = summary["articles_written"]
    if verbose:
        print("\n[cadence] Generating product articles from the rotation...")
    try:
        product_paths = generate_product_articles(news_count=news_written, verbose=verbose)
        for product_path in product_paths:
            summary["articles_written"] += 1
            summary["files_created"].append(str(product_path))
            if verbose:
                print(f"  ✓ {product_path.name}")
    except Exception as e:
        print(f"  Product-article cadence error: {e}")
        summary["errors"] += 1

    # Note: SeenArticleStore auto-saves on mark_seen()

    # Final summary
    if verbose:
        print("\n" + "=" * 60)
        print(f"Pipeline complete: {summary['articles_written']} articles written")
        print(f"Errors: {summary['errors']}")
        print("=" * 60)

    return summary


if __name__ == "__main__":
    try:
        result = run_pipeline(verbose=True)
        sys.exit(0 if result["errors"] == 0 else 1)
    except Exception as e:
        print(f"Pipeline error: {e}")
        sys.exit(1)
