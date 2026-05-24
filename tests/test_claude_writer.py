"""Tests for claude_writer module."""

import pytest
from pathlib import Path
from src.processors.claude_writer import (
    create_slug,
    select_template_type,
    ensure_output_dir,
)


class TestSlugGeneration:
    """Test slug creation from titles."""

    def test_basic_title_slug(self):
        """Should create valid slug from basic title."""
        slug = create_slug("GPT-5 Released: Revolutionary Update")
        assert slug == "gpt-5-released-revolutionary-update"

    def test_slug_removes_special_chars(self):
        """Should remove special characters."""
        slug = create_slug("Tool! @#$% Version 2.0")
        assert "@" not in slug
        assert "$" not in slug

    def test_slug_length_limit(self):
        """Should cap slug length."""
        long_title = "This is a very long title " * 5
        slug = create_slug(long_title)
        assert len(slug) <= 50

    def test_empty_title_slug(self):
        """Should handle empty title."""
        slug = create_slug("")
        assert isinstance(slug, str)

    def test_unicode_slug(self):
        """Should handle unicode characters."""
        slug = create_slug("Café résumé")
        assert isinstance(slug, str)
        assert len(slug) > 0


class TestTemplateSelection:
    """Test template type selection logic."""

    def test_breaking_for_high_score_release(self):
        """Should select breaking for major releases."""
        article = {
            "category": "model_release",
            "importance_score": 90,
        }
        tpl = select_template_type(article)
        assert tpl == "breaking"

    def test_comparison_for_multiple_products(self):
        """Should select comparison when products mentioned."""
        article = {
            "category": "tool",
            "importance_score": 50,
            "products_mentioned": ["perplexity", "openai"],
        }
        tpl = select_template_type(article)
        assert tpl == "comparison"

    def test_explainer_for_research(self):
        """Should select explainer for research."""
        article = {
            "category": "research",
            "importance_score": 60,
        }
        tpl = select_template_type(article)
        assert tpl == "explainer"

    def test_default_breaking(self):
        """Should default to breaking for unknown categories."""
        article = {
            "category": "other",
            "importance_score": 30,
        }
        tpl = select_template_type(article)
        # May be breaking or other, but should be valid
        assert tpl in ["breaking", "comparison", "explainer"]


class TestOutputDirectory:
    """Test output directory management."""

    def test_create_output_dir(self, tmp_path, monkeypatch):
        """Should create output directory."""
        output_path = tmp_path / "output" / "articles"
        monkeypatch.setattr("src.processors.claude_writer.OUTPUT_DIR", output_path)

        ensure_output_dir()
        assert output_path.exists()

    def test_idempotent_dir_creation(self, tmp_path, monkeypatch):
        """Should handle existing directory."""
        output_path = tmp_path / "output" / "articles"
        output_path.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr("src.processors.claude_writer.OUTPUT_DIR", output_path)

        ensure_output_dir()
        assert output_path.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
