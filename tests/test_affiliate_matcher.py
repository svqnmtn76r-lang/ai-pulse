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
    """Test full matching pipeline with the tightened rule + brand floor:
    brand_hits >= 1 AND (brand_hits >= 2 OR >= 2 distinct non-brand keywords).
    The brand floor means a product must be NAMED at least once to match."""

    def test_match_single_product(self):
        """Should return a list (0 or 1 product)."""
        article = {
            "title": "OpenAI GPT-5 Release",
            "summary": "OpenAI announces GPT-5 with advanced reasoning.",
        }
        matches = match_products(article)
        assert isinstance(matches, list)

    def test_at_most_one_product(self):
        """One-product-per-article cap: never return 2+ products."""
        article = {
            "title": "Perplexity ElevenLabs Notion Semrush HubSpot integration",
            "summary": "All major AI tools integrate with each other.",
        }
        matches = match_products(article)
        assert len(matches) <= 1

    def test_brand_repeated_matches(self):
        """Brand token repeated >= 2 times qualifies (perplexity x22 case)."""
        article = {
            "title": "Perplexity vs ChatGPT",
            "summary": "perplexity " * 22,
        }
        matches = match_products(article)
        assert matches and matches[0]["product_id"] == "perplexity"

    def test_single_generic_keyword_repeated_does_not_match(self):
        """A lone generic keyword repeated N times must NOT match (workspace x4)."""
        article = {
            "title": "Show HN: an open-source workspace",
            "summary": "workspace workspace workspace workspace for teams",
        }
        # 'notion' brand appears 0 times; only ONE distinct non-brand keyword
        # ('workspace') -> fails brand>=2 and distinct>=2.
        matches = match_products(article)
        assert all(m["product_id"] != "notion" for m in matches)

    def test_generic_keywords_without_brand_does_not_match(self):
        """Brand floor: >= 2 distinct generic keywords but brand_hits == 0 must
        NOT match -- the product is never named (the karpathy/Obsidian case:
        knowledge base + wiki + workspace, but no "Notion")."""
        article = {
            "title": "Karpathy LLM wiki pattern integrated into Obsidian",
            "summary": "A self-hosted knowledge base and personal wiki workspace "
                       "for note-taking, built on Obsidian.",
        }
        # 'notion' brand appears 0 times; several distinct non-brand keywords hit,
        # so the OLD rule would have matched. The brand floor drops it.
        matches = match_products(article)
        assert all(m["product_id"] != "notion" for m in matches)

    def test_brand_named_plus_distinct_keyword_matches(self):
        """Brand named once + >= 2 distinct non-brand keywords qualifies (brand
        floor satisfied, second clause via keyword diversity)."""
        article = {
            "title": "Notion vs Obsidian for your team",
            "summary": "Notion is a knowledge base and wiki workspace for "
                       "note-taking and project docs.",
        }
        matches = match_products(article)
        assert matches and matches[0]["product_id"] == "notion"

    def test_single_incidental_brand_mention_does_not_match(self):
        """One brand mention + no second distinct keyword must NOT match."""
        article = {
            "title": "A note about productivity",
            "summary": "We briefly used notion once during the project.",
        }
        matches = match_products(article)
        assert all(m["product_id"] != "notion" for m in matches)

    def test_match_contains_required_fields(self):
        """Each match should have required fields."""
        article = {
            "title": "Perplexity announcement",
            "summary": "Perplexity released new perplexity features.",
        }
        matches = match_products(article)
        if matches:
            match = matches[0]
            assert "product_id" in match
            assert "match_score" in match
            assert "match_reason" in match


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
