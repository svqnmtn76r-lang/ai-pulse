#!/usr/bin/env python3
"""Phase 0 diagnostic: why are articles unmatched?

For every article the REAL matcher does NOT attach a product to, score every
eligible product and report any with brand_hits >= 1 (a true brand mention that
failed to qualify -- a "near-miss"). If there are no near-misses, the gap is a
content-mix problem, not a matcher-strictness problem.

Usage: PYTHONPATH=. python scripts/diagnose_unmatched.py [articles_dir]
Default articles_dir = output/articles
"""

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from src.processors.affiliate_matcher import (  # noqa: E402
    load_affiliate_catalog, eligible_products, get_product_keywords,
    score_product, match_products,
)

_CTA = re.compile(r'<div class="affiliate-cta".*?</div>', re.DOTALL)


def parse(path: Path):
    t = path.read_text(encoding="utf-8")
    title, body = "", t
    if t.startswith("---"):
        parts = t.split("---", 2)
        if len(parts) >= 3:
            front_raw, body = parts[1], parts[2]
            try:
                title = str((yaml.safe_load(front_raw) or {}).get("title", ""))
            except yaml.YAMLError:
                pass
    return title, _CTA.sub("", body)


def main():
    articles_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "output" / "articles"
    programs = load_affiliate_catalog().get("programs", {})
    prods = eligible_products()

    files = sorted(articles_dir.glob("*.md"))
    matched, unmatched = [], []
    for f in files:
        title, body = parse(f)
        (matched if match_products({"title": title, "body": body}) else unmatched).append(f)

    print(f"TOTAL={len(files)} MATCHED={len(matched)} UNMATCHED={len(unmatched)}")

    near = {}
    brand_named_any = 0
    for f in unmatched:
        title, body = parse(f)
        text = (title + " " + body).lower()
        hit = False
        for pid in prods:
            q, score, bh, dnb = score_product(text, pid, get_product_keywords(pid), programs.get(pid, {}))
            if bh >= 1:
                hit = True
                near.setdefault(pid, []).append((f.name, bh, dnb))
        if hit:
            brand_named_any += 1

    print(f"\nUnmatched articles naming >=1 catalog brand (near-misses): {brand_named_any}")
    if not near:
        print("  -> ZERO near-misses. The gap is CONTENT MIX, not matcher strictness.")
        print("     Loosening the matcher would only add false positives.")
        return
    for pid in sorted(near):
        rows = sorted(near[pid], key=lambda r: (-r[1], -r[2]))
        print(f"\n  {pid} ({len(rows)} near-miss articles):")
        for name, bh, dnb in rows[:12]:
            print(f"     brand_hits={bh} distinct_nonbrand={dnb}  {name}")


if __name__ == "__main__":
    main()
