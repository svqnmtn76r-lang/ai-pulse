import pytest
import tempfile
from pathlib import Path
from src.utils.state_store import SeenArticleStore


def test_mark_and_exists():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        store = SeenArticleStore(db_path)

        assert not store.exists("abc123")
        store.mark_seen("abc123", "test_source", "Test Title", "https://example.com")
        assert store.exists("abc123")


def test_mark_seen_is_idempotent():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        store = SeenArticleStore(db_path)

        store.mark_seen("abc123", "s1", "T", "https://x.com")
        store.mark_seen("abc123", "s1", "T", "https://x.com")  # 2回呼んでも問題ないこと
        assert store.exists("abc123")
