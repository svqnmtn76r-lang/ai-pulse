"""End-to-end article generation pipeline."""

import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(".env")

from src.sources.rss_monitor import articles_from_rss
from src.sources.github_releases import articles_from_github
from src.sources.hackernews import stories_from_hackernews
from src.processors.importance_scorer import batch_score_articles
from src.processors.affiliate_matcher import enrich_article_with_products
from src.processors.claude_writer import write_article, create_slug
from src.utils.state_store import SeenArticleStore

OUTPUT_DIR = Path("output/articles")


def run_pipeline(verbose: bool = True) -> dict:
    """
    Full pipeline: fetch -> score -> match -> write articles.
    Returns summary of execution.
    """
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

    summary["total_fetched"] = len(articles)
    if verbose:
        print(f"  Total fetched: {summary['total_fetched']}")

    # Step 2: Score articles
    if verbose:
        print("\n[2/4] Scoring articles for importance...")

    scored = batch_score_articles(articles, seen_store)
    summary["after_scoring"] = len(scored)

    if verbose:
        print(f"  After filtering: {summary['after_scoring']} articles (60+ score)")

    # Step 3: Match to products and enrich
    if verbose:
        print("\n[3/4] Matching articles to affiliate products...")

    enriched = []
    for article in scored:
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
