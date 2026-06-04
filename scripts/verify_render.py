#!/usr/bin/env python3
"""Verify in-body affiliate link rendering in the BUILT site (dist/).

Deterministic stand-in for 目視. For every article it asserts the Day 4 Definition
of Done render rules, using:
  - the product config (data/affiliate_sources.yml) for expected affiliate URLs, and
  - the matcher result the pipeline already wrote to each article's frontmatter
    (`products:`) for which product (if any) the article should carry.

Rules:
  matched article  -> exactly ONE block [data-affiliate], its <a href> equals the
                      product config affiliate_url, non-empty anchor text, FTC present.
  non-matched      -> ZERO [data-affiliate] blocks.

Also writes docs/day4_link_digest.md (matched article -> href / anchor / FTC).

Usage: python scripts/verify_render.py        # assumes a fresh blog/dist
Exit 0 = OK, 1 = FAIL.
"""

import re
import sys
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "data" / "affiliate_sources.yml"
CONTENT_DIR = REPO / "blog" / "src" / "content" / "articles"
DIST_DIR = REPO / "blog" / "dist" / "articles"
DIGEST = REPO / "docs" / "day4_link_digest.md"

FTC_MARKERS = ("affiliate", "commission", "disclosure")

# A rendered affiliate href must point at a product page, never at an
# affiliate-program / recruitment page. Same guard as
# scripts/verify_affiliate_urls.py (Day 4 DoD #2), enforced here on the BUILT
# HTML so the fix can't regress through the render path. Case-insensitive.
FORBIDDEN_RE = re.compile(
    r"/affiliates\b|/affiliate\b|/partners/affiliate|affiliate-program|"
    r"affiliate\.|/referral-program|/become-an-affiliate",
    re.IGNORECASE,
)


def load_product_urls() -> dict:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    return {
        pid: (p.get("affiliate_url") or "").strip()
        for pid, p in data.get("programs", {}).items()
    }


def load_match_result() -> dict:
    """article_id -> product_id (matched) or None (from frontmatter `products`)."""
    matches = {}
    for md in sorted(CONTENT_DIR.glob("*.md")):
        article_id = md.stem
        front = {}
        text = md.read_text(encoding="utf-8")
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                front = yaml.safe_load(parts[1]) or {}
        products = front.get("products") or []
        matches[article_id] = products[0] if products else None
    return matches


def dist_path(article_id: str) -> Path:
    return DIST_DIR / article_id / "index.html"


def main():
    product_urls = load_product_urls()
    matches = load_match_result()

    errors = []
    digest_rows = []

    for article_id, product_id in matches.items():
        path = dist_path(article_id)
        if not path.exists():
            errors.append(f"{article_id}: built HTML not found at {path}")
            continue
        html = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")
        blocks = soup.select("[data-affiliate]")

        if product_id is None:
            if blocks:
                errors.append(f"{article_id}: affiliate block leaked into a NON-matched article "
                              f"({len(blocks)} found)")
            continue

        # matched article
        if len(blocks) != 1:
            errors.append(f"{article_id}: expected exactly 1 affiliate block, found {len(blocks)}")
            continue
        a = blocks[0].find("a", href=True)
        expected = product_urls.get(product_id, "")
        href = a["href"].strip() if a else None
        anchor = a.get_text(strip=True) if a else ""
        ftc = any(m in html.lower() for m in FTC_MARKERS)

        if not expected:
            errors.append(f"{article_id}: no affiliate_url in config for '{product_id}'")
        if href != expected:
            errors.append(f"{article_id}: href != config url ({href!r} vs {expected!r})")
        if href and FORBIDDEN_RE.search(href):
            errors.append(f"{article_id}: rendered href points at an affiliate-signup "
                          f"page, not a product page ({href!r})")
        if not anchor:
            errors.append(f"{article_id}: affiliate link has no anchor text")
        if not ftc:
            errors.append(f"{article_id}: FTC disclosure missing")
        # data-affiliate must name the matched product (single-product correctness)
        if blocks[0].get("data-affiliate") != product_id:
            errors.append(f"{article_id}: data-affiliate={blocks[0].get('data-affiliate')!r} "
                          f"!= matched product {product_id!r}")

        digest_rows.append((article_id, product_id, href or "", anchor or "", "Y" if ftc else "N"))

    # Write the human-review digest
    matched_n = len(digest_rows)
    lines = [
        "# Day 4 — In-body affiliate link digest",
        "",
        "Rendered from `blog/dist/` by `scripts/verify_render.py`. One row per matched article.",
        "`href` is read from the **built HTML**; expected value is the product's `affiliate_url`",
        "in `data/affiliate_sources.yml`.",
        "",
        f"Matched articles: **{matched_n}**",
        "",
        "| Article | Product | Rendered href | Anchor text | FTC |",
        "|---|---|---|---|---|",
    ]
    for article_id, product_id, href, anchor, ftc in sorted(digest_rows):
        lines.append(f"| {article_id} | {product_id} | {href} | {anchor} | {ftc} |")
    lines.append("")
    DIGEST.write_text("\n".join(lines), encoding="utf-8")

    if errors:
        print("RENDER VERIFY: FAIL")
        for e in errors:
            print("  -", e)
        print(f"\nDigest written to {DIGEST.relative_to(REPO)} ({matched_n} matched articles)")
        return 1

    print("RENDER VERIFY: OK — all matched articles render one correct in-body affiliate link;"
          " no leakage into non-matched articles.")
    print(f"Matched articles: {matched_n}. Digest -> {DIGEST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
