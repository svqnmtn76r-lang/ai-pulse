"""End-to-end article generation pipeline."""

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


def generate_product_article(verbose: bool = True) -> Optional[Path]:
    """Cadence: generate ONE commercial article from the rotating topic list.

    Dedup-guarded: picks the first topic whose output file does not already exist
    (any date); if every topic is already generated, logs a reminder and returns
    None (no error, no repeat). Reuses the normal path: the topic's product is
    seeded as the match, so the article routes to the comparison/deep_dive
    template, is centered on (and names) the product, gets the product-page
    affiliate_url from config, one in-body block, and the FTC disclosure. The
    pipeline's reconciler step then re-validates the match on the real body
    (brand>=1).
    """
    if not PRODUCT_TOPICS.exists():
        if verbose:
            print(f"  (no {PRODUCT_TOPICS} — skipping cadence)")
        return None

    topics = yaml.safe_load(PRODUCT_TOPICS.read_text(encoding="utf-8")) or []
    programs = load_affiliate_catalog().get("programs", {})
    existing = existing_article_slugs()

    topic = next(
        (t for t in topics
         if (t.get("title") or "").strip()
         and create_slug(t["title"].strip()) not in existing),
        None,
    )
    if topic is None:
        print("  rotation exhausted — add topics to data/product_topics.yml")
        return None

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
    summary["after_scoring"] = len(adopted)

    if verbose:
        print(f"  Total scored: {len(scored)}, Adopted (score >= {SCORE_THRESHOLD}): {summary['after_scoring']}")

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

    # Step 5: Cadence — generate ONE product (commercial) article per run from
    # the rotating topic list, so monetizable coverage grows over time.
    if verbose:
        print("\n[cadence] Generating one product article from the rotation...")
    try:
        product_path = generate_product_article(verbose=verbose)
        if product_path:
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
