"""Fetch AI-related stories from Hacker News."""

import hashlib
import requests
from datetime import datetime
from typing import Optional
from pathlib import Path
import yaml

HN_API_BASE = "https://hacker-news.firebaseio.com/v0"
HN_ITEM_URL = f"{HN_API_BASE}/item/{{id}}.json"
HN_TOP_STORIES_URL = f"{HN_API_BASE}/topstories.json"

# Strict AI-related keywords for filtering
# Only specific tools and techniques, not generic "AI" or "machine learning"
RELEVANT_KEYWORDS_STRICT = [
    "openai", "anthropic", "claude", "gpt", "gemini", "llama",
    "mistral", "perplexity", "elevenlabs", "notion", "huggingface",
    "ai model", "llm", "model release", "api pricing", "agentic",
    "fine-tuning", "rag", "embedding", "transformer", "diffusion"
]

# Cache for affiliate keywords (loaded once per process)
_AFFILIATE_KEYWORDS_CACHE = None


def load_affiliate_keywords() -> set:
    """Load trigger_keywords from affiliate_sources.yml (Day 2.7).

    Returns a set of keywords. Cached after first load to avoid file I/O.
    """
    global _AFFILIATE_KEYWORDS_CACHE

    if _AFFILIATE_KEYWORDS_CACHE is not None:
        return _AFFILIATE_KEYWORDS_CACHE

    keywords = set()
    try:
        config_path = Path("data/affiliate_sources.yml")
        with open(config_path) as f:
            data = yaml.safe_load(f)

        for program_name, program_info in data.get("programs", {}).items():
            for keyword in program_info.get("trigger_keywords", []):
                # Normalize: lowercase
                keywords.add(keyword.lower())

        _AFFILIATE_KEYWORDS_CACHE = keywords
    except Exception as e:
        print(f"Warning: Failed to load affiliate keywords: {e}")
        _AFFILIATE_KEYWORDS_CACHE = set()

    return _AFFILIATE_KEYWORDS_CACHE

# HN rate limit: gentle (no official limit, but be respectful)
REQUEST_TIMEOUT = 5  # seconds
MAX_STORIES_TO_FETCH = 50  # Process top 50 stories


def is_ai_related(title: str, text: Optional[str] = None) -> bool:
    """Check if story is AI-related based on strict keywords + affiliate trigger keywords.

    Uses only title (HN summaries are often unavailable).
    Requires specific AI tool/technique mentions, not generic "ai" or "machine learning".

    Day 2.7: Also includes affiliate product trigger keywords from affiliate_sources.yml.
    """
    title_lower = title.lower()

    # Match at least one strict keyword from title only
    for keyword in RELEVANT_KEYWORDS_STRICT:
        if keyword in title_lower:
            return True

    # Day 2.7: Also check affiliate keywords
    affiliate_keywords = load_affiliate_keywords()
    for keyword in affiliate_keywords:
        if keyword in title_lower:
            return True

    return False


def fetch_story(story_id: int) -> Optional[dict]:
    """Fetch individual story details."""
    try:
        response = requests.get(
            HN_ITEM_URL.format(id=story_id),
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching HN story {story_id}: {e}")
        return None


def stories_from_hackernews() -> list:
    """
    Fetch AI-related stories from Hacker News.
    Returns list of article dicts matching RSS format.
    """
    articles = []

    try:
        # Get top story IDs
        response = requests.get(HN_TOP_STORIES_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        story_ids = response.json()[:MAX_STORIES_TO_FETCH]

    except Exception as e:
        print(f"Error fetching HN top stories: {e}")
        return articles

    # Fetch and filter stories
    for story_id in story_ids:
        story = fetch_story(story_id)
        if not story:
            continue

        # Skip if no URL (Ask HN, etc.)
        if "url" not in story:
            continue

        title = story.get("title", "")
        url = story.get("url", "")

        # Check if AI-related
        if not is_ai_related(title):
            continue

        # Skip dead/flagged stories
        if story.get("dead") or story.get("deleted"):
            continue

        # Convert to standard article format
        published_timestamp = story.get("time", 0)
        published = datetime.utcfromtimestamp(published_timestamp).isoformat() + "Z"

        # Summary: use title as summary for HN posts
        summary = f"Story on Hacker News with {story.get('descendants', 0)} comments."

        # Generate consistent ID
        article_id = hashlib.md5(
            f"hackernews:{story_id}:{url}".encode()
        ).hexdigest()

        articles.append({
            "id": article_id,
            "source": "hackernews",
            "title": title,
            "url": url,
            "summary": summary,
            "published": published,
            "hn_id": story_id,
            "hn_score": story.get("score", 0),
            "hn_comments": story.get("descendants", 0),
        })

    return articles


if __name__ == "__main__":
    # Test
    stories = stories_from_hackernews()
    print(f"Found {len(stories)} AI-related stories on HN")
    for story in stories[:3]:
        print(f"  - {story['title']}")
