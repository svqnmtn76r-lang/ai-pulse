#!/usr/bin/env python3
"""Compute affiliate product-match-rate over generated articles.

Measurement definition (Day 4 DoD):
- A product matches an article only if its trigger_keywords hit >= 2 times
  across the article's title + body (case-insensitive). A single incidental
  mention does NOT count.
- At most ONE product is attached per article (the highest-scoring qualifying
  product). This protects data quality (C-axis) and honours the one-product cap.

match-rate = (articles with >= 1 matched product) / (total articles)

This script is self-contained: it reads trigger_keywords straight from
data/affiliate_sources.yml and parses the article markdown files directly, so
it can be run before or after any matcher change to compare apples to apples.

Usage:
    python scripts/match_report.py [articles_dir]

Default articles_dir = output/articles
"""

import sys
import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
AFFILIATE_CATALOG = REPO_ROOT / "data" / "affiliate_sources.yml"
DEFAULT_ARTICLES_DIR = REPO_ROOT / "output" / "articles"

MIN_HITS = 2  # quality threshold: keywords must hit >= 2 times across title+body


def load_program_keywords() -> dict:
    """Return {product_id: [keywords]} for every program with trigger_keywords."""
    with open(AFFILIATE_CATALOG) as f:
        catalog = yaml.safe_load(f)

    programs = catalog.get("programs", {})
    result = {}
    for product_id, data in programs.items():
        kws = data.get("trigger_keywords")
        if kws:
            # normalise to lowercased, de-duplicated list
            seen = set()
            clean = []
            for kw in kws:
                k = str(kw).lower().strip()
                if k and k not in seen:
                    seen.add(k)
                    clean.append(k)
            result[product_id] = clean
    return result


def parse_article(path: Path) -> tuple[str, str]:
    """Return (title, body) for a markdown article with YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    title = ""
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            front_raw, body = parts[1], parts[2]
            try:
                front = yaml.safe_load(front_raw) or {}
                title = str(front.get("title", ""))
            except yaml.YAMLError:
                title = ""
    return title, body


def count_hits(keywords: list, haystack: str) -> int:
    """Total occurrences of all keywords in haystack (already lowercased)."""
    total = 0
    for kw in keywords:
        # count non-overlapping occurrences of the keyword substring
        total += haystack.count(kw)
    return total


def best_product(title: str, body: str, program_keywords: dict):
    """Return (product_id, score) of the single best-matching product, or None.

    A product qualifies only if its keyword hits across title+body >= MIN_HITS.
    Among qualifying products, the highest hit count wins (one product per
    article). Title hits are used as a deterministic tie-breaker.
    """
    haystack = (title + " " + body).lower()
    title_l = title.lower()

    candidates = []
    for product_id, keywords in program_keywords.items():
        hits = count_hits(keywords, haystack)
        if hits >= MIN_HITS:
            title_hits = count_hits(keywords, title_l)
            candidates.append((hits, title_hits, product_id))

    if not candidates:
        return None

    # sort by (hits, title_hits, product_id) descending for determinism
    candidates.sort(key=lambda c: (c[0], c[1], c[2]), reverse=True)
    hits, _title_hits, product_id = candidates[0]
    return product_id, hits


def main():
    articles_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ARTICLES_DIR
    program_keywords = load_program_keywords()

    md_files = sorted(articles_dir.glob("*.md"))
    total = len(md_files)
    matched = 0
    matches_detail = []

    for path in md_files:
        title, body = parse_article(path)
        result = best_product(title, body, program_keywords)
        if result:
            matched += 1
            product_id, hits = result
            matches_detail.append((path.name, product_id, hits))

    rate = (matched / total * 100) if total else 0.0

    print("=" * 64)
    print(f"Articles dir : {articles_dir}")
    print(f"Threshold    : >= {MIN_HITS} keyword hits across title+body")
    print(f"Cap          : 1 product per article (highest-scoring)")
    print("-" * 64)
    for name, product_id, hits in matches_detail:
        print(f"  [MATCH] {product_id:11} hits={hits:<3} {name}")
    print("-" * 64)
    print(f"matched/total = {matched}/{total} = {rate:.1f}%")
    print("=" * 64)

    return rate


if __name__ == "__main__":
    main()
