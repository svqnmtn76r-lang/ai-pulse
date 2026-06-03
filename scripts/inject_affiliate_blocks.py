#!/usr/bin/env python3
"""Reconcile in-body affiliate blocks with the CURRENT matcher result.

Idempotent reconciler (safe to re-run):
  - MATCHED article   -> ensure exactly one affiliate block for the matched
                         product, frontmatter `products: [pid]`, and the
                         "contains affiliate links" FTC disclosure.
  - UNMATCHED article -> remove any affiliate block, clear `products: []`, and
                         set the "does not contain affiliate links" disclosure.

The match is decided on EDITORIAL content: the machine-injected affiliate block
is stripped before calling the real matcher, so a block can never circularly
keep its own article matched.

New articles still get their block at generation time
(claude_writer.write_article_file); this script backfills/repairs existing files.

Usage: python scripts/inject_affiliate_blocks.py [articles_dir]   (default output/articles)
"""

import re
import sys
from pathlib import Path

import yaml

from src.processors.affiliate_matcher import match_products
from src.processors.claude_writer import build_affiliate_block

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "data" / "affiliate_sources.yml"
DEFAULT_DIR = REPO / "output" / "articles"

DISCLOSURE_PREFIX = "*Disclosure:"
DISCLOSURE_CONTAINS = ("*Disclosure: This article contains affiliate links. "
                       "As an affiliate, we earn from qualifying purchases at no extra cost to you.*")
DISCLOSURE_NONE = "*This article does not contain affiliate links.*"

CTA_BLOCK = re.compile(r'<div class="affiliate-cta".*?</div>\n?', re.DOTALL)


def load_products() -> dict:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    return {
        pid: {"product_id": pid, "name": p.get("display_name", pid),
              "affiliate_url": p.get("affiliate_url")}
        for pid, p in data.get("programs", {}).items()
    }


def split_frontmatter(text: str):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]) or {}, parts[2]
    return {}, text


def set_frontmatter_products(text: str, products: list) -> str:
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text
    fm = parts[1]
    repl = ("products:\n" + "".join(f"- {p}\n" for p in products)) if products else "products: []\n"
    new_fm, n = re.subn(r"(?m)^products:(?:[^\n]*)\n(?:- .*\n)*", repl, fm)
    if n == 0:
        new_fm = fm.rstrip("\n") + "\n" + repl
    return "---" + new_fm + "---" + parts[2]


def set_disclosure(text: str, matched: bool) -> str:
    if matched:
        return text.replace(DISCLOSURE_NONE, DISCLOSURE_CONTAINS) if DISCLOSURE_NONE in text else text
    return text.replace(DISCLOSURE_CONTAINS, DISCLOSURE_NONE) if DISCLOSURE_CONTAINS in text else text


def insert_block_before_disclosure(text: str, block: str) -> str:
    block_text = block.strip("\n") + "\n"
    lines = text.splitlines(keepends=True)
    idx = next((i for i, ln in enumerate(lines)
                if ln.startswith(DISCLOSURE_PREFIX) or ln.startswith("*This article does not")), None)
    if idx is not None:
        lines.insert(idx, block_text + "\n")
        return "".join(lines)
    return text.rstrip() + "\n\n" + block_text


def main():
    articles_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    products = load_products()

    added, stripped, repaired, missing_cfg = [], [], [], []
    ok_matched = ok_clean = 0

    for md in sorted(articles_dir.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        front, body = split_frontmatter(text)
        title = str(front.get("title", ""))
        editorial_body = CTA_BLOCK.sub("", body)

        matched = match_products({"title": title, "body": editorial_body})
        matched_pid = matched[0]["product_id"] if matched else None
        front_products = front.get("products") or []
        block_pids = re.findall(r'data-affiliate="([^"]+)"', text)

        if matched_pid:
            if block_pids == [matched_pid] and front_products == [matched_pid]:
                ok_matched += 1
                continue
            prod = products.get(matched_pid)
            block = build_affiliate_block(prod) if prod else ""
            if not block:
                missing_cfg.append((md.name, matched_pid))
                continue
            new = CTA_BLOCK.sub("", text)
            new = set_frontmatter_products(new, [matched_pid])
            new = set_disclosure(new, matched=True)
            new = insert_block_before_disclosure(new, block)
            md.write_text(new, encoding="utf-8")
            (added if not block_pids else repaired).append((md.name, matched_pid))
        else:
            if not block_pids and not front_products:
                ok_clean += 1
                continue
            new = CTA_BLOCK.sub("", text)
            new = set_frontmatter_products(new, [])
            new = set_disclosure(new, matched=False)
            md.write_text(new, encoding="utf-8")
            dropped = front_products[0] if front_products else (block_pids[0] if block_pids else "?")
            stripped.append((md.name, dropped))

    print(f"added={len(added)} stripped={len(stripped)} repaired={len(repaired)} "
          f"ok_matched={ok_matched} ok_clean={ok_clean} missing_config={len(missing_cfg)}")
    for tag, rows in (("ADD", added), ("STRIP", stripped), ("REPAIR", repaired), ("NO-URL", missing_cfg)):
        for name, pid in rows:
            print(f"  [{tag}] {pid:11} {name}")
    return added, stripped


if __name__ == "__main__":
    main()
