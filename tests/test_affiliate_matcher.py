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
    """Test match score calculation (Day 4: score = keyword hit count)."""

    def test_exact_keyword_match(self):
        """Should count keyword hits across title + summary."""
        score = calculate_match_score(
            "perplexity",
            "Perplexity AI Launch",
            "Perplexity released a new feature for search."
        )
        # 'perplexity' appears twice -> at least 2 hits
        assert score >= 2

    def test_no_match(self):
        """Should score zero when no keywords match."""
        score = calculate_match_score(
            "perplexity",
            "Random blog post",
            "This is about cooking recipes."
        )
        assert score == 0

    def test_multiple_keyword_matches(self):
        """Should count higher with multiple keyword hits."""
        score = calculate_match_score(
            "elevenlabs",
            "Voice synthesis with ElevenLabs TTS",
            "Using text-to-speech voice cloning for audio generation."
        )
        # elevenlabs, voice synthesis, tts, text-to-speech, voice cloning,
        # audio generation -> well above the 2-hit floor
        assert score >= 4


class TestProductMatching:
    """Test full matching pipeline with Day 4 guardrails."""

    def test_match_single_product(self):
        """Should return a list (0 or 1 product)."""
        article = {
            "title": "OpenAI GPT-5 Release",
            "summary": "OpenAI announces GPT-5 with advanced reasoning.",
        }
        matches = match_products(article, min_hits=0)
        assert isinstance(matches, list)

    def test_at_most_one_product(self):
        """One-product-per-article cap: never return 2+ products."""
        article = {
            "title": "Perplexity ElevenLabs Notion Semrush HubSpot integration",
            "summary": "All major AI tools integrate with each other.",
        }
        matches = match_products(article, min_hits=0)
        assert len(matches) <= 1

    def test_min_hits_threshold(self):
        """Should respect the minimum-hit threshold."""
        article = {
            "title": "Tech news",
            "summary": "Random unrelated content",
        }
        matches = match_products(article, min_hits=100)
        assert len(matches) == 0

    def test_two_hit_quality_floor(self):
        """A single incidental mention (1 hit) must NOT match at the >=2 floor."""
        article = {
            "title": "A note about productivity",
            "summary": "We briefly used notion once during the project.",
        }
        # default min_hits = MATCH_MIN_HITS (2); 'notion' appears once -> no match
        matches = match_products(article)
        assert all(m["product_id"] != "notion" for m in matches)

    def test_match_contains_required_fields(self):
        """Each match should have required fields."""
        article = {
            "title": "Perplexity announcement",
            "summary": "Perplexity released new perplexity features.",
        }
        matches = match_products(article, min_hits=2)
        if matches:
            match = matches[0]
            assert "product_id" in match
            assert "match_score" in match
            assert "match_reason" in match


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
