"""Score and filter articles by importance."""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import anthropic
import yaml

from src.utils.state_store import SeenArticleStore

SCORING_CONFIG = Path("config/scoring.yml")


def load_scoring_config() -> dict:
    """Load scoring thresholds and rules."""
    if not SCORING_CONFIG.exists():
        # Default config if not present
        return {
            "adoption_threshold": 60,
            "rule_filters": {
                "min_title_length": 10,
                "duplicate_days": 30,
                "skip_formats": ["interview", "podcast", "招待"],
            },
        }
    with open(SCORING_CONFIG) as f:
        return yaml.safe_load(f)


def stage1_rule_filter(article: dict, seen_store: SeenArticleStore) -> Optional[str]:
    """
    Apply rule-based filters. Return skip_reason if should be rejected.
    Returns None if article passes Stage 1.
    """
    config = load_scoring_config()
    rules = config.get("rule_filters", {})

    # Check title length
    min_len = rules.get("min_title_length", 10)
    if len(article.get("title", "").strip()) < min_len:
        return "title_too_short"

    # Check for emoji-only title
    title = article.get("title", "")
    if title and not any(c.isalnum() or c.isspace() for c in title):
        return "non_ascii_title"

    # Check for low-signal formats (non-RSS sources only)
    if article.get("source") != "openai" and article.get("source") != "google_deepmind" and article.get("source") != "huggingface":
        skip_formats = rules.get("skip_formats", [])
        title_lower = title.lower()
        for fmt in skip_formats:
            if fmt.lower() in title_lower:
                return "low_signal_format"

    # Check for duplicates
    if seen_store.exists(article.get("id", "")):
        return "duplicate"

    return None


def validate_json_schema(result: dict) -> bool:
    """Validate that result matches expected schema."""
    valid_categories = [
        "model_release", "feature_update", "pricing_change", "sdk_release",
        "research_paper", "tool_launch", "industry_news", "tutorial", "opinion", "off_topic"
    ]
    valid_scores = [0, 20, 40, 60, 80, 100]

    if not isinstance(result, dict):
        return False
    if result.get("importance_score") not in valid_scores:
        return False
    if result.get("category") not in valid_categories:
        return False
    if not isinstance(result.get("products_mentioned", []), list):
        return False
    return True


def stage2_claude_scoring(article: dict, retry: bool = True) -> dict:
    """
    Use Claude Haiku to score article importance.
    Returns dict with importance_score, category, products_mentioned.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "").strip())

    title = article.get("title", "")
    summary = article.get("summary", "")
    source = article.get("source", "")

    # Truncate summary
    summary = summary[:1200]

    prompt = f"""Score this AI industry article for importance. Respond with ONLY this JSON (no markdown, no extra text, no trailing text):
{{
  "importance_score": 40,
  "category": "industry_news",
  "products_mentioned": [],
  "reason": "example"
}}

Now score this actual article:
Title: {title}
Source: {source}
Summary: {summary}

SCORE MUST BE: 0, 20, 40, 60, 80, or 100
CATEGORY MUST BE: model_release, feature_update, pricing_change, sdk_release, research_paper, tool_launch, industry_news, tutorial, opinion, or off_topic

Scoring:
- 100: Major model launch
- 80: Price changes, major features, SDK updates
- 60: New products, tutorials
- 40: Research, tech blogs
- 20: Generic news
- 0: Off-topic"""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text.strip()

        # Remove markdown code block if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json\n"):
                text = text[5:]
            text = text.strip()

        # Parse JSON response
        result = json.loads(text)

        # Validate schema
        if not validate_json_schema(result):
            if retry:
                # One retry attempt with explicit correction
                return stage2_claude_scoring(article, retry=False)
            else:
                # Fallback to safe values
                return {
                    "importance_score": 40,
                    "category": "other",
                    "products_mentioned": [],
                }

        # Log cost
        from src.analytics.cost_report import log_api_call
        log_api_call(
            module="importance_scorer",
            model="claude-haiku-4-5-20251001",
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

        return {
            "importance_score": int(result.get("importance_score", 40)),
            "category": result.get("category", "industry_news"),
            "products_mentioned": result.get("products_mentioned", []),
        }

    except json.JSONDecodeError as e:
        print(f"JSON parse error: text='{text}' error={e}")
        if retry:
            return stage2_claude_scoring(article, retry=False)
        return {
            "importance_score": 40,
            "category": "industry_news",
            "products_mentioned": [],
        }
    except Exception as e:
        print(f"Claude API error: {e}")
        return {
            "importance_score": 40,
            "category": "industry_news",
            "products_mentioned": [],
        }


def score_article(article: dict, seen_store: SeenArticleStore) -> dict:
    """
    Full scoring pipeline: Stage 1 (rules) -> Stage 2 (Claude).
    Returns enriched article dict with scoring metadata.
    """
    # Stage 1: Rule filter
    skip_reason = stage1_rule_filter(article, seen_store)
    if skip_reason:
        return {
            **article,
            "importance_score": 0,
            "category": "skipped",
            "products_mentioned": [],
            "skip_reason": skip_reason,
            "scoring_method": "rule_v1",
        }

    # Stage 2: Claude scoring
    claude_result = stage2_claude_scoring(article)

    return {
        **article,
        "importance_score": claude_result["importance_score"],
        "category": claude_result["category"],
        "products_mentioned": claude_result.get("products_mentioned", []),
        "skip_reason": None,
        "scoring_method": "claude_v1",
    }


def batch_score_articles(articles: list, seen_store: SeenArticleStore) -> list:
    """Score multiple articles."""
    config = load_scoring_config()
    threshold = config.get("adoption_threshold", 60)

    scored = []
    for article in articles:
        scored_article = score_article(article, seen_store)
        # Only adopt articles above threshold (unless explicitly marked for inclusion)
        if scored_article.get("skip_reason") is None and scored_article.get("importance_score", 0) >= threshold:
            scored.append(scored_article)

    return scored
