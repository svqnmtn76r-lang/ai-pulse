"""Anthropic news scraper.

Anthropic doesn't provide an official RSS feed, so we scrape https://www.anthropic.com/news.
Day 2.7: Extract title, url, published date, and summary from news listings.
"""

import hashlib
import re
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import structlog

log = structlog.get_logger()

BASE_URL = "https://www.anthropic.com"
NEWS_URL = f"{BASE_URL}/news"
USER_AGENT = "ai-pulse/0.2 (+https://aipulse.pages.dev)"


def scrape_anthropic() -> List[dict]:
    """Scrape latest Anthropic news articles.

    Returns list of articles in format compatible with RSS pipeline.
    Articles are limited to most recent 10 items.
    """
    articles = []

    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(NEWS_URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all article links (/news/* pattern)
        article_links = []
        for link in soup.find_all('a', href=re.compile(r'^/news/')):
            href = link.get('href', '')
            if href.startswith('/news/'):
                article_links.append(href)

        # Deduplicate and limit to 10
        article_links = list(dict.fromkeys(article_links))[:10]

        if not article_links:
            log.warning("anthropic_no_articles_found")
            return []

        # Scrape each article
        for article_href in article_links:
            article_url = f"{BASE_URL}{article_href}"

            try:
                article_response = requests.get(
                    article_url,
                    headers=headers,
                    timeout=10
                )
                article_response.raise_for_status()
                article_soup = BeautifulSoup(article_response.text, 'html.parser')

                # Extract title
                title_tag = article_soup.find('h1')
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)

                # Extract summary from og:description or first paragraph
                summary = ""
                og_desc = article_soup.find('meta', {'property': 'og:description'})
                if og_desc:
                    summary = og_desc.get('content', '')

                # Fallback: use article text
                if not summary:
                    article_tag = article_soup.find('article')
                    if article_tag:
                        # Get first 100 words
                        text = article_tag.get_text()
                        summary = ' '.join(text.split()[:50])

                # Extract published date - look for date patterns
                published = extract_publication_date(article_soup, article_url)

                # Create article entry
                article_id = hashlib.md5(article_url.encode()).hexdigest()
                article = {
                    "id": article_id,
                    "source": "anthropic",
                    "title": title,
                    "url": article_url,
                    "summary": summary[:500] if summary else "",
                    "published": published.isoformat() if published else None,
                }
                articles.append(article)

            except Exception as e:
                log.warning("anthropic_article_scrape_failed", url=article_url, error=str(e))
                continue

        log.info("anthropic_scrape_complete", article_count=len(articles))
        return articles

    except Exception as e:
        log.error("anthropic_scrape_failed", error=str(e))
        return []


def extract_publication_date(soup: BeautifulSoup, url: str) -> Optional[datetime]:
    """Extract publication date from article page.

    Tries multiple patterns: time tag, meta tags, or date text patterns.
    Falls back to today if not found.
    """

    # Try <time datetime="">
    time_tag = soup.find('time')
    if time_tag and time_tag.get('datetime'):
        try:
            dt_str = time_tag.get('datetime')
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            pass

    # Try og:published_time
    og_published = soup.find('meta', {'property': 'og:published_time'})
    if og_published:
        try:
            dt_str = og_published.get('content', '')
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            pass

    # Try to find date text (e.g. "May 22, 2026")
    text = soup.get_text()
    date_match = re.search(
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})',
        text
    )
    if date_match:
        try:
            month_str, day_str, year_str = date_match.groups()
            # Parse simple date format
            dt_str = f"{month_str} {day_str}, {year_str}"
            published = datetime.strptime(dt_str, "%B %d, %Y")
            return published.replace(tzinfo=timezone.utc)
        except (ValueError, AttributeError):
            pass

    # Fallback: return today UTC
    return datetime.now(timezone.utc)


if __name__ == "__main__":
    import json
    articles = scrape_anthropic()
    print(json.dumps(articles, indent=2, ensure_ascii=False))
