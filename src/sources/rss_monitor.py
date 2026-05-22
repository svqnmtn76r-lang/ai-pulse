import feedparser
import hashlib
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
import yaml
import structlog

from src.utils.state_store import SeenArticleStore

log = structlog.get_logger()


def load_feeds(config_path: Path = Path("data/rss_feeds.yml")) -> dict:
    """Load verified_official_rss feeds from data/rss_feeds.yml.

    no_official_rss feeds are not included (require scrapers in Phase 2).
    """
    with open(config_path) as f:
        data = yaml.safe_load(f)

    feeds = {}
    verified = data.get("verified_official_rss", {})
    for name, info in verified.items():
        if isinstance(info, dict) and "url" in info:
            feeds[name] = info["url"]
    return feeds


def parse_pub_date(entry) -> Optional[datetime]:
    """安全に published_parsed をdatetimeに変換"""
    for key in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, key, None)
        if parsed:
            try:
                return datetime(*parsed[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                continue
    return None


def poll_all_sources(window_hours: int = 24):
    """全RSSをポーリングして新規記事のみ返す"""
    store = SeenArticleStore()
    feeds = load_feeds()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    new_articles = []

    for source_name, url in feeds.items():
        log.info("polling", source=source_name, url=url)
        try:
            feed = feedparser.parse(url, request_headers={"User-Agent": "ai-pulse/0.1"})
            if feed.bozo and not feed.entries:
                log.warning("feed_parse_failed", source=source_name, error=str(feed.bozo_exception))
                continue

            for entry in feed.entries[:15]:
                article_id = hashlib.md5(entry.link.encode()).hexdigest()
                if store.exists(article_id):
                    continue

                pub = parse_pub_date(entry)
                if pub and pub < cutoff:
                    continue

                article = {
                    "id": article_id,
                    "source": source_name,
                    "title": entry.title,
                    "url": entry.link,
                    "summary": getattr(entry, "summary", "")[:500],
                    "published": pub.isoformat() if pub else None,
                }
                new_articles.append(article)
                store.mark_seen(article_id, source_name, entry.title, entry.link)
        except Exception as e:
            log.error("source_failed", source=source_name, error=str(e))

        time.sleep(0.5)  # マナー

    return new_articles


if __name__ == "__main__":
    articles = poll_all_sources(window_hours=24)
    print(json.dumps(articles, indent=2, ensure_ascii=False))
    log.info("poll_complete", new_count=len(articles))
