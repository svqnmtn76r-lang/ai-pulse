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


def test_load_feeds_returns_only_verified():
    feeds = load_feeds()
    # After 2026-05-22 verification: only 3 official RSS feeds exist
    assert len(feeds) == 3
    assert set(feeds.keys()) == {"openai", "google_deepmind", "huggingface"}


def test_parse_pub_date_handles_missing():
    class FakeEntry:
        pass
    assert parse_pub_date(FakeEntry()) is None
