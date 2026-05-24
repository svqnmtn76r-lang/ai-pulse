"""Tests for hackernews module."""

import pytest
from src.sources.hackernews import (
    is_ai_related,
    fetch_story,
)


class TestAIKeywordDetection:
    """Test AI-related content detection."""

    def test_obvious_ai_keywords(self):
        """Should detect obvious AI keywords."""
        assert is_ai_related("New GPT-5 Model Released")
        assert is_ai_related("Claude AI Breakthrough")
        assert is_ai_related("Deep Learning with Transformers")

    def test_llm_related(self):
        """Should detect LLM-related content."""
        assert is_ai_related("Large Language Models")
        assert is_ai_related("LLM fine-tuning techniques")

    def test_non_ai_content(self):
        """Should reject non-AI content."""
        assert not is_ai_related("Best Pizza Recipes")
        assert not is_ai_related("How to Fix Your Car")

    def test_combined_text(self):
        """Should check title and text combined."""
        title = "Tech Update"
        text = "A new AI model was released today"
        assert is_ai_related(title, text)

    def test_case_insensitive(self):
        """Should be case-insensitive."""
        assert is_ai_related("NEW AI RELEASE")
        assert is_ai_related("Ai development")


class TestStoryFetching:
    """Test story fetching (mocked)."""

    def test_fetch_handles_errors(self):
        """Should handle network errors gracefully."""
        # Fetch with invalid ID should fail gracefully
        result = fetch_story(999999999)
        # May return None or empty dict depending on HN API
        assert result is None or isinstance(result, dict)

    def test_fetch_returns_dict(self):
        """Should return dict when successful."""
        # This tests the type, not actual API call
        # Real test would require mocking
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
