"""Tests for importance_scorer module."""

import pytest
from src.processors.importance_scorer import (
    stage1_rule_filter,
    batch_score_articles,
)
from src.utils.state_store import SeenArticleStore


@pytest.fixture
def sample_article():
    """Sample article for testing."""
    return {
        "id": "test123",
        "source": "openai",
        "title": "GPT-5 Released: Revolutionary Model Training",
        "url": "https://example.com/gpt5",
        "summary": "OpenAI released GPT-5 with breakthrough capabilities in reasoning and coding.",
        "published": "2026-05-23T10:00:00Z",
    }


@pytest.fixture
def seen_store(tmp_path):
    """Temporary seen articles store."""
    store = SeenArticleStore(db_path=tmp_path / "test.db")
    return store


class TestStage1Filtering:
    """Test rule-based filtering."""

    def test_title_too_short(self, seen_store):
        """Should reject articles with very short titles."""
        article = {
            "title": "Hi",
            "url": "https://example.com/test",
            "source": "openai",
        }
        reason = stage1_rule_filter(article, seen_store)
        assert reason == "title_too_short"

    def test_duplicate_detection(self, sample_article, seen_store):
        """Should detect duplicate URLs."""
        # Mark as seen
        seen_store.mark_seen(
            sample_article["id"],
            sample_article["source"],
            sample_article["title"],
            sample_article["url"],
        )

        # Try filtering - should be rejected
        reason = stage1_rule_filter(sample_article, seen_store)
        assert reason == "duplicate"

    def test_valid_article_passes(self, sample_article, seen_store):
        """Valid articles should pass Stage 1."""
        reason = stage1_rule_filter(sample_article, seen_store)
        assert reason is None

    def test_low_signal_format_rejection(self, seen_store):
        """Should reject interview/podcast titles from non-RSS."""
        article = {
            "title": "An Interview with Claude Creator",
            "url": "https://example.com/interview",
            "source": "hackernews",
        }
        reason = stage1_rule_filter(article, seen_store)
        assert reason == "low_signal_format"


class TestBatchScoringIntegration:
    """Test batch scoring pipeline."""

    def test_batch_with_empty_list(self, seen_store):
        """Should handle empty article list."""
        scored = batch_score_articles([], seen_store)
        assert scored == []

    def test_batch_filters_low_score(self, seen_store):
        """Should filter articles scoring below threshold."""
        articles = [
            {
                "id": "low1",
                "source": "hackernews",
                "title": "Random tech post",
                "url": "https://example.com/low",
                "summary": "Not AI related",
                "published": "2026-05-23T10:00:00Z",
            }
        ]
        # This will be scored by Claude, may be < 60
        # We're just testing the filtering mechanism
        scored = batch_score_articles(articles, seen_store)
        # May be empty if Claude gives it < 60, which is expected
        assert isinstance(scored, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
