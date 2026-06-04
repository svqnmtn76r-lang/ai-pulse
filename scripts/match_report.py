#!/usr/bin/env python3
"""Compute affiliate product-match-rate over generated articles.

Measurement definition (Day 4 DoD):
- A product matches an article under the matcher's tightened rule:
  brand_hits >= 2 OR >= 2 distinct non-brand keywords, across title + body.
- At most ONE product is attached per article (the highest-scoring qualifying
  product). This protects data quality (C-axis) and honours the one-product cap.

match-rate = (articles with >= 1 matched product) / (total articles)

This report calls the REAL matcher (`src.processors.affiliate_matcher.match_products`)
so it always reflects the live matching rule. Run with the repo root importable,
e.g. `PYTHONPATH=. python scripts/match_report.py [articles_dir]`.

Default articles_dir = output/articles
"""

import re
import sys
from pathlib import Path

import yaml

# The machine-injected affiliate CTA block names the product; strip it before
# matching so the measurement reflects EDITORIAL content (no circular self-match).
_CTA_BLOCK = re.compile(r'<div class="affiliate-cta".*?</div>', re.DOTALL)

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
AFFILIATE_CATALOG = REPO_ROOT / "data" / "affiliate_sources.yml"
DEFAULT_ARTICLES_DIR = REPO_ROOT / "output" / "articles"

from src.processors.affiliate_matcher import match_products  # noqa: E402


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
    body = _CTA_BLOCK.sub("", body)
    return title, body


def best_product(title: str, body: str):
    """Return (product_id, score) via the REAL matcher, or None.

    Delegates to `match_products` so the report always reflects the live rule
    (brand_hits >= 2 OR >= 2 distinct non-brand keywords; one product per article).
    """
    matches = match_products({"title": title, "body": body})
    if not matches:
        return None
    m = matches[0]
    return m["product_id"], m["match_score"]


def main():
    articles_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ARTICLES_DIR

    md_files = sorted(articles_dir.glob("*.md"))
    total = len(md_files)
    matched = 0
    matches_detail = []

    for path in md_files:
        title, body = parse_article(path)
        result = best_product(title, body)
        if result:
            matched += 1
            product_id, score = result
            matches_detail.append((path.name, product_id, score))

    rate = (matched / total * 100) if total else 0.0

    print("=" * 64)
    print(f"Articles dir : {articles_dir}")
    print(f"Rule         : brand_hits>=2 OR >=2 distinct non-brand keywords (matcher)")
    print(f"Cap          : 1 product per article (highest-scoring)")
    print("-" * 64)
    for name, product_id, score in matches_detail:
        print(f"  [MATCH] {product_id:11} score={score:<4} {name}")
    print("-" * 64)
    print(f"matched/total = {matched}/{total} = {rate:.1f}%")
    print("=" * 64)

    return rate


if __name__ == "__main__":
    main()
