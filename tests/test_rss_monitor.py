import pytest
from src.sources.rss_monitor import load_feeds, parse_pub_date


def test_load_feeds_returns_dict():
    feeds = load_feeds()
    assert isinstance(feeds, dict)
    assert len(feeds) > 0
    # すべての値がURLであること
    for name, url in feeds.items():
        assert url.startswith("http")


def test_load_feeds_includes_openai():
    feeds = load_feeds()
    assert "openai" in feeds


def test_load_feeds_includes_verified_and_affiliate():
    feeds = load_feeds()
    # The 3 verified official RSS feeds are always present.
    assert {"openai", "google_deepmind", "huggingface"}.issubset(feeds.keys())
    # Day 4: validated affiliate-blog feeds are ingested too (lift match-rate).
    assert {"hubspot_blog", "semrush_blog"}.issubset(feeds.keys())
    # Red / no-RSS sources are never loaded.
    assert "anthropic" not in feeds
    assert "perplexity" not in feeds


def test_parse_pub_date_handles_missing():
    class FakeEntry:
        pass
    assert parse_pub_date(FakeEntry()) is None
