"""Web scrapers for sources without official RSS feeds.

Day 2.7: Anthropic news scraper.
"""

import structlog

log = structlog.get_logger()


def articles_from_scrapers() -> list:
    """Fetch articles from all available scrapers.

    Returns articles in the same format as RSS pipeline:
      {
        "id": str,
        "source": str,
        "title": str,
        "url": str,
        "summary": str,
        "published": str (ISO format),
      }
    """
    from .anthropic_news import scrape_anthropic

    articles = []

    try:
        articles.extend(scrape_anthropic())
    except Exception as e:
        log.warning("anthropic_scrape_failed", error=str(e))

    return articles


if __name__ == "__main__":
    import json
    articles = articles_from_scrapers()
    print(json.dumps(articles, indent=2, ensure_ascii=False))
