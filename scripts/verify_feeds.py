#!/usr/bin/env python3
"""Verify candidate affiliate-blog RSS feeds before adding them to the pipeline.

Only feeds that print [OK] (HTTP 200, >0 entries, not bozo) should be wired into
data/rss_feeds.yml. Run:  python scripts/verify_feeds.py
"""

import requests
import feedparser

CANDIDATES = {
    "hubspot":    "https://blog.hubspot.com/marketing/rss.xml",   # /rss.xml pattern — likely OK
    "semrush":    "https://www.semrush.com/blog/feed/",           # WP /feed/ — verify
    "shopify":    "https://www.shopify.com/blog/feed.atom",       # verify; also try /blog.atom
    "notion":     "https://www.notion.com/blog/rss.xml",          # uncertain
    "perplexity": "https://www.perplexity.ai/hub/rss.xml",        # likely no public RSS
    "elevenlabs": "https://elevenlabs.io/blog/rss.xml",           # likely no public RSS
}

# Alternates to try once if the primary FAILs (Appendix A note).
ALTERNATES = {
    "shopify":    ["https://www.shopify.com/blog.atom", "https://www.shopify.com/blog/feed"],
    "semrush":    ["https://www.semrush.com/blog/feed", "https://www.semrush.com/blog/rss"],
    "notion":     ["https://www.notion.so/blog/rss.xml"],
    "elevenlabs": ["https://elevenlabs.io/blog/feed", "https://elevenlabs.io/blog/rss"],
}


def check(name, url):
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "ai-pulse-feedcheck/1.0"})
        parsed = feedparser.parse(r.content)
        n = len(parsed.entries)
        ok = r.status_code == 200 and n > 0 and not parsed.bozo
        print(f"[{'OK' if ok else 'FAIL'}] {name:12} {r.status_code} entries={n}  {url}")
        return ok
    except Exception as e:
        print(f"[ERR ] {name:12} {type(e).__name__}: {e}  {url}")
        return False


def main():
    passed = {}
    for name, url in CANDIDATES.items():
        if check(name, url):
            passed[name] = url
            continue
        # try alternates once
        for alt in ALTERNATES.get(name, []):
            if check(f"{name}*", alt):
                passed[name] = alt
                break
    print("-" * 60)
    print("PASSED:", ", ".join(f"{k} -> {v}" for k, v in passed.items()) or "(none)")
    return passed


if __name__ == "__main__":
    main()
