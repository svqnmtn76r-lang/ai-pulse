"""Fetch AI-related stories from Hacker News."""

import hashlib
import requests
from datetime import datetime
from typing import Optional

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

# HN rate limit: gentle (no official limit, but be respectful)
REQUEST_TIMEOUT = 5  # seconds
MAX_STORIES_TO_FETCH = 50  # Process top 50 stories


def is_ai_related(title: str, text: Optional[str] = None) -> bool:
    """Check if story is AI-related based on strict keywords.

    Uses only title (HN summaries are often unavailable).
    Requires specific AI tool/technique mentions, not generic "ai" or "machine learning".
    """
    title_lower = title.lower()

    # Match at least one strict keyword from title only
    for keyword in RELEVANT_KEYWORDS_STRICT:
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
