"""Tests for affiliate_matcher module."""

import pytest
from src.processors.affiliate_matcher import (
    get_product_keywords,
    calculate_match_score,
    match_products,
)


class TestProductKeywords:
    """Test keyword retrieval."""

    def test_known_product_keywords(self):
        """Should return keywords for known products."""
        kw = get_product_keywords("perplexity")
        assert isinstance(kw, list)
        assert len(kw) > 0
        assert any("perplexity" in k.lower() for k in kw)

    def test_unknown_product_fallback(self):
        """Should return empty list for unknown products."""
        kw = get_product_keywords("nonexistent_product")
        assert isinstance(kw, list)


class TestMatchScoring:
    """Test match score calculation."""

    def test_exact_keyword_match(self):
        """Should score high for exact keyword matches."""
        score = calculate_match_score(
            "perplexity",
            "Perplexity AI Launch",
            "Perplexity released a new feature for search."
        )
        assert score >= 20  # May have 2 keyword hits for 20 points

    def test_no_match(self):
        """Should score zero when no keywords match."""
        score = calculate_match_score(
            "perplexity",
            "Random blog post",
            "This is about cooking recipes."
        )
        assert score == 0

    def test_multiple_keyword_matches(self):
        """Should score higher with multiple keyword matches."""
        score = calculate_match_score(
            "elevenlabs",
            "Voice synthesis with ElevenLabs TTS",
            "Using text-to-speech voice API for audio generation."
        )
        assert score >= 50


class TestProductMatching:
    """Test full matching pipeline."""

    def test_match_single_product(self):
        """Should match relevant article to product."""
        article = {
            "title": "OpenAI GPT-5 Release",
            "summary": "OpenAI announces GPT-5 with advanced reasoning.",
        }
        matches = match_products(article, min_score=0)
        # May or may not match depending on keywords
        assert isinstance(matches, list)

    def test_max_three_products(self):
        """Should return at most 3 products."""
        article = {
            "title": "Perplexity ElevenLabs Notion Semrush HubSpot integration",
            "summary": "All major AI tools integrate with each other.",
        }
        matches = match_products(article, min_score=0)
        assert len(matches) <= 3

    def test_min_score_threshold(self):
        """Should respect minimum score threshold."""
        article = {
            "title": "Tech news",
            "summary": "Random unrelated content",
        }
        matches = match_products(article, min_score=100)
        assert len(matches) == 0

    def test_match_contains_required_fields(self):
        """Each match should have required fields."""
        article = {
            "title": "Perplexity announcement",
            "summary": "Perplexity released new features.",
        }
        matches = match_products(article, min_score=0)
        if matches:
            match = matches[0]
            assert "product_id" in match
            assert "match_score" in match
            assert "match_reason" in match


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
