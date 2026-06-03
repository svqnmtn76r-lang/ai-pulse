#!/usr/bin/env python3
"""Idempotently inject the in-body affiliate block into already-matched articles.

New articles get the block at generation time (claude_writer.write_article_file).
This migration backfills pre-existing matched articles (frontmatter `products`
non-empty) that were written before the render fix and therefore have no block.

Idempotent: an article that already contains a `data-affiliate` block is skipped,
so this is safe to re-run. href + display name come from data/affiliate_sources.yml.

Usage: python scripts/inject_affiliate_blocks.py [articles_dir]   (default output/articles)
"""

import sys
from pathlib import Path

import yaml

from src.processors.claude_writer import build_affiliate_block

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "data" / "affiliate_sources.yml"
DEFAULT_DIR = REPO / "output" / "articles"
DISCLOSURE_PREFIX = "*Disclosure:"


def load_products() -> dict:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    out = {}
    for pid, p in data.get("programs", {}).items():
        out[pid] = {
            "product_id": pid,
            "name": p.get("display_name", pid),
            "affiliate_url": p.get("affiliate_url"),
        }
    return out


def split_frontmatter(text: str):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            front = yaml.safe_load(parts[1]) or {}
            return front, parts[2]
    return {}, text


def main():
    articles_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    products = load_products()

    injected, skipped_has_block, skipped_unmatched, missing_cfg = [], 0, 0, []

    for md in sorted(articles_dir.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        if "data-affiliate" in text:
            skipped_has_block += 1
            continue
        front, _body = split_frontmatter(text)
        product_list = front.get("products") or []
        if not product_list:
            skipped_unmatched += 1
            continue
        pid = product_list[0]
        prod = products.get(pid)
        block = build_affiliate_block(prod) if prod else ""
        if not block:
            missing_cfg.append((md.name, pid))
            continue

        # Insert the block right before the FTC disclosure line (matching the
        # writer's body + block + disclosure order); else append at the end.
        lines = text.splitlines(keepends=True)
        idx = next((i for i, ln in enumerate(lines) if ln.startswith(DISCLOSURE_PREFIX)), None)
        block_text = block.strip("\n") + "\n"
        if idx is not None:
            lines.insert(idx, block_text + "\n")
            new_text = "".join(lines)
        else:
            new_text = text.rstrip() + "\n\n" + block_text
        md.write_text(new_text, encoding="utf-8")
        injected.append((md.name, pid))

    print(f"injected={len(injected)} skipped(has_block)={skipped_has_block} "
          f"skipped(unmatched)={skipped_unmatched} missing_config={len(missing_cfg)}")
    for name, pid in injected:
        print(f"  [INJECT] {pid:11} {name}")
    for name, pid in missing_cfg:
        print(f"  [NO-URL] {pid:11} {name}")
    return injected


if __name__ == "__main__":
    main()
