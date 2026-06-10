"""Tests for the self-replenishing topic pool (src/pipeline/topic_pool.py)."""

import pytest

from src.pipeline import topic_pool as tp
from src.processors.claude_writer import create_slug
from src.processors.affiliate_matcher import load_affiliate_catalog


CATALOG = load_affiliate_catalog().get("programs", {})
N2P = tp._name_to_pid(CATALOG)


class TestSemanticKey:
    def test_vs_is_order_independent(self):
        a = tp.semantic_key("Shopify vs Wix: which is better in 2026", N2P)
        b = tp.semantic_key("Wix vs Shopify: a 2026 comparison", N2P)
        assert a == b == ("vs", frozenset({"shopify", "wix"}))

    def test_vs_reworded_collides(self):
        """Different wording, same comparison -> same key (the core dedup)."""
        a = tp.semantic_key("ElevenLabs vs Murf: best AI voice generator for creators", N2P)
        b = tp.semantic_key("ElevenLabs vs Murf: which is better in 2026", N2P)
        assert a == b

    def test_multiword_competitor(self):
        k = tp.semantic_key("Kinsta vs WP Engine: managed WordPress hosting compared", N2P)
        assert k == ("vs", frozenset({"kinsta", "wp-engine"}))

    def test_profile_one_per_product(self):
        a = tp.semantic_key("ElevenLabs review 2026: AI voice and text-to-speech tested", N2P)
        b = tp.semantic_key("ElevenLabs review 2026: features, pricing and verdict", N2P)
        assert a == b == ("profile", "elevenlabs")

    def test_distinct_products_dont_collide(self):
        a = tp.semantic_key("Shopify vs Wix: which is better", N2P)
        b = tp.semantic_key("Kinsta vs WP Engine: which is better", N2P)
        assert a != b


class TestGenerator:
    def test_only_known_tracked_products(self):
        tmap = tp.load_topic_map()
        new, _ = tp.generate_new_topics(limit=200)
        for t in new:
            assert t["product"] in tmap, t
            # the product must have a real affiliate_url (tracked-only)
            assert (CATALOG.get(t["product"], {}).get("affiliate_url") or "").strip()

    def test_valid_shape(self):
        new, _ = tp.generate_new_topics(limit=200)
        for t in new:
            assert t["type"] in ("comparison", "deep_dive")
            assert t["title"].strip()

    def test_no_duplicate_vs_published_or_pool(self):
        pool = tp.load_pool()
        slug_taken = set(tp.published_slugs()) | tp.pool_slugs(pool)
        key_taken = tp.taken_keys(pool, tp.published_titles(), N2P)
        new, _ = tp.generate_new_topics(limit=200)
        for t in new:
            assert create_slug(t["title"]) not in slug_taken
            assert tp.semantic_key(t["title"], N2P) not in key_taken

    def test_internally_unique(self):
        new, _ = tp.generate_new_topics(limit=200)
        slugs = [create_slug(t["title"]) for t in new]
        keys = [tp.semantic_key(t["title"], N2P) for t in new]
        assert len(slugs) == len(set(slugs))
        assert len(keys) == len(set(keys))

    def test_limit_respected(self):
        new, remaining = tp.generate_new_topics(limit=5)
        assert len(new) == 5
        assert remaining >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
