#!/usr/bin/env python3
"""Verify every product's affiliate_url is a real product page, not a signup page.

Two assertions per product (Day 4 Definition of Done #2 + #3):
  (a) forbidden-pattern guard: the URL must NOT look like an affiliate-program /
      recruitment page (see FORBIDDEN below), case-insensitive. This is the core
      guard that keeps the fix from regressing.
  (b) reachability: the URL returns HTTP 200 (GET, follow redirects, browser-like
      User-Agent).

Reads URLs from data/affiliate_sources.yml (config only — no hardcoded URLs).

Usage: python scripts/verify_affiliate_urls.py
Exit 0 = all pass, 1 = at least one failure.
"""

import re
import sys
from pathlib import Path

import requests
import yaml

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "data" / "affiliate_sources.yml"

# Affiliate-program / recruitment markers. A product affiliate_url must match NONE.
# Case-insensitive. `affiliate.` catches the affiliate.* subdomain form.
FORBIDDEN = [
    r"/affiliates\b",
    r"/affiliate\b",
    r"/partners/affiliate",
    r"affiliate-program",
    r"affiliate\.",            # affiliate.notion.so style subdomain
    r"/referral-program",
    r"/become-an-affiliate",
]
FORBIDDEN_RE = re.compile("|".join(FORBIDDEN), re.IGNORECASE)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# WAF / bot-challenge signatures. A 403/429 whose body matches one of these is a
# live product page sitting behind a bot wall (e.g. perplexity.ai behind
# Cloudflare, documented in CLAUDE.md §5.1) — a real human browser passes the JS
# challenge. We treat that as reachable-but-protected, NOT a dead page. A 403/429
# WITHOUT such a signature is a genuine failure.
WAF_MARKERS = re.compile(
    r"just a moment|cf-ray|cloudflare|attention required|"
    r"checking your browser|/cdn-cgi/challenge|captcha",
    re.IGNORECASE,
)


def load_urls() -> dict:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    return {
        pid: (p.get("affiliate_url") or "").strip()
        for pid, p in data.get("programs", {}).items()
    }


def forbidden_hit(url: str):
    m = FORBIDDEN_RE.search(url)
    return m.group(0) if m else None


def check_http(url: str):
    """Return (ok, label).

    ok=True for a real 200, or for a 403/429 that is clearly a WAF/bot challenge
    over a live page. ok=False for genuine 404/dead/connection errors.
    """
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=20,
                         allow_redirects=True)
        if r.status_code == 200:
            return True, "HTTP 200"
        if r.status_code in (401, 403, 429) and WAF_MARKERS.search(r.text or ""):
            return True, f"HTTP {r.status_code} bot-protected (live page behind WAF)"
        return False, f"HTTP {r.status_code}"
    except requests.RequestException as e:
        return False, f"ERR {e.__class__.__name__}"


def main() -> int:
    urls = load_urls()
    failures = []
    print(f"Verifying {len(urls)} affiliate_url values from {CONFIG.relative_to(REPO)}\n")
    for pid, url in sorted(urls.items()):
        if not url:
            failures.append(f"{pid}: empty affiliate_url")
            print(f"  FAIL  {pid:11} <empty>")
            continue
        hit = forbidden_hit(url)
        ok_http, status = check_http(url)
        problems = []
        if hit:
            problems.append(f"forbidden pattern {hit!r}")
        if not ok_http:
            problems.append(status)
        if problems:
            failures.append(f"{pid}: {url} -> {'; '.join(problems)}")
            print(f"  FAIL  {pid:11} {url}  [{'; '.join(problems)}]")
        else:
            print(f"  OK    {pid:11} {url}  [{status}]")

    print()
    if failures:
        print("AFFILIATE URL VERIFY: FAIL")
        for f in failures:
            print("  -", f)
        return 1
    print("AFFILIATE URL VERIFY: OK — all URLs pass the forbidden-pattern guard "
          "and are reachable (HTTP 200, or a live page behind a WAF bot challenge).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
