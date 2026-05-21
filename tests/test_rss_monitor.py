import pytest
from src.sources.rss_monitor import load_feeds, parse_pub_date


def test_load_feeds_returns_dict():
    feeds = load_feeds()
    assert isinstance(feeds, dict)
    assert len(feeds) > 0
    # すべての値がURLであること
    for name, url in feeds.items():
        assert url.startswith("http")


def test_load_feeds_includes_anthropic():
    feeds = load_feeds()
    assert "anthropic" in feeds


def test_parse_pub_date_handles_missing():
    class FakeEntry:
        pass
    assert parse_pub_date(FakeEntry()) is None
