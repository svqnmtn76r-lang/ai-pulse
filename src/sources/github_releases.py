import os
import json
import hashlib
import requests
from datetime import datetime, timedelta, timezone
import structlog

log = structlog.get_logger()

WATCHED_REPOS = [
    "openai/openai-python",
    "anthropics/anthropic-sdk-python",
    "anthropics/claude-code",
    "langchain-ai/langchain",
    "vercel/ai",
]


def fetch_recent_releases(hours_back: int = 48):
    token = os.environ.get("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    new_releases = []

    for repo in WATCHED_REPOS:
        url = f"https://api.github.com/repos/{repo}/releases?per_page=5"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            for release in r.json():
                pub = datetime.strptime(
                    release["published_at"], "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=timezone.utc)
                if pub < cutoff:
                    continue
                new_releases.append({
                    "repo": repo,
                    "tag": release["tag_name"],
                    "title": release.get("name") or release["tag_name"],
                    "body": (release.get("body") or "")[:1000],
                    "url": release["html_url"],
                    "published": pub.isoformat(),
                })
        except Exception as e:
            log.error("repo_fetch_failed", repo=repo, error=str(e))

    return new_releases


def articles_from_github(hours_back: int = 48):
    """Fetch GitHub releases and convert to standard article format (Day 2 pipeline interface)."""
    releases = fetch_recent_releases(hours_back=hours_back)
    articles = []

    for release in releases:
        article_id = hashlib.md5(release["url"].encode()).hexdigest()
        articles.append({
            "id": article_id,
            "source": f"github:{release['repo']}",
            "title": f"{release['repo']} {release['title']}",
            "url": release["url"],
            "summary": release["body"],
            "published": release["published"],
        })

    return articles


if __name__ == "__main__":
    releases = fetch_recent_releases(hours_back=48)
    print(json.dumps(releases, indent=2, ensure_ascii=False))
