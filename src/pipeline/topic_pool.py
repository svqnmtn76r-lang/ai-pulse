"""Self-replenishing buyer-intent topic pool.

The daily cadence (src/pipeline/run.py) drains data/product_topics.yml by ~4-6
topics/day; when it empties, the run produces NO commercial article and the
forward match-rate gain silently dies. This module keeps the pool fed:

- a curated competitor/category map (data/topic_map.yml, tracked products only),
- a deterministic generator that emits buyer-intent topics from a few patterns,
- `replenish_topic_pool()` — a top-up that, when the FRESH (unpublished) pool is
  low, appends enough NEW, deduped topics to reach a target buffer, and warns
  (GitHub Actions annotation) when sensible combinations run low.

Everything dedups against BOTH already-published article slugs AND the current
pool, so it never produces a duplicate article. Commercial topics only ever name
products that have a real tracked affiliate_url (the map lists tracked products
only), so generated articles always carry a real tracked link — never a fake one.
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

from src.processors.claude_writer import create_slug
from src.processors.affiliate_matcher import load_affiliate_catalog

REPO = Path(__file__).resolve().parent.parent.parent
PRODUCT_TOPICS = REPO / "data" / "product_topics.yml"
TOPIC_MAP = REPO / "data" / "topic_map.yml"
OUTPUT_DIR = REPO / "output" / "articles"

# Tunables (env-overridable so Hiro can dial without code changes).
def _low_threshold() -> int:
    return int(os.environ.get("TOPIC_LOW_THRESHOLD", "10"))

def _target_buffer() -> int:
    return int(os.environ.get("TOPIC_TARGET_BUFFER", "40"))

# Below this many still-generatable candidates after a top-up, warn Hiro to extend
# the curated map (≈ one day's worth left in reserve).
def _warn_reserve() -> int:
    return int(os.environ.get("TOPIC_WARN_RESERVE", "6"))


# --------------------------------------------------------------------------- #
# Slug helpers (mirror run.py.existing_article_slugs so dedup is identical)
# --------------------------------------------------------------------------- #
def published_slugs() -> set:
    """Article slugs already on disk, with the YYYY-MM-DD- date prefix stripped."""
    slugs = set()
    if OUTPUT_DIR.exists():
        for f in OUTPUT_DIR.glob("*.md"):
            m = re.match(r"\d{4}-\d{2}-\d{2}-(.+)$", f.stem)
            if m:
                slugs.add(m.group(1))
    return slugs


def load_pool() -> list:
    if not PRODUCT_TOPICS.exists():
        return []
    return yaml.safe_load(PRODUCT_TOPICS.read_text(encoding="utf-8")) or []


def pool_slugs(pool: list) -> set:
    return {create_slug((t.get("title") or "").strip())
            for t in pool if (t.get("title") or "").strip()}


# --------------------------------------------------------------------------- #
# SEMANTIC dedup — two titles describe the SAME article if they share a topic
# key, even when the wording (and therefore the slug) differs. This is what stops
# "X vs Y: which is better" from duplicating an existing "X vs Y: best ... for ...".
# --------------------------------------------------------------------------- #
def _name_to_pid(catalog: dict) -> dict:
    """lowercased product display_name / id -> product_id (longest names first)."""
    m = {}
    for pid, data in catalog.items():
        m[pid.lower()] = pid
        dn = str(data.get("display_name", "")).strip().lower()
        if dn:
            m[dn] = pid
    return m


def _find_product(text_lower: str, name2pid: dict):
    """Longest product display-name/id appearing in the text -> pid, else None."""
    best = None
    for name, pid in name2pid.items():
        if name and name in text_lower and (best is None or len(name) > best[0]):
            best = (len(name), pid)
    return best[1] if best else None


def semantic_key(title: str, name2pid: dict):
    """Canonical topic key shared by any two titles about the same thing.

    - "A vs B ..."            -> ('vs', frozenset({pidA_or_slug, slug(B)}))  order-free
    - "... alternatives ..."  -> ('alt', pid)
    - "is X worth it ..."     -> ('worth', pid)
    - "X review / deep dive"  -> ('profile', pid)   (one profile per product)
    - "best <cat> for <uc>"   -> ('best', slug(cat), slug(uc))
    - else                    -> ('slug', slug(title))   (exact fallback)
    """
    t = (title or "").lower()
    m = re.search(r"\bvs\b", t)
    if m:
        left, right = t[: m.start()], t[m.end():]
        right = re.split(r"[:\-–—]| which | best | in 20", right, 1)[0]
        lp = _find_product(left, name2pid) or create_slug(left)
        rp = _find_product(right, name2pid) or create_slug(right)
        return ("vs", frozenset({lp, rp}))
    pid = _find_product(t, name2pid)
    if "alternative" in t:
        return ("alt", pid or create_slug(t))
    if "worth it" in t:
        return ("worth", pid or create_slug(t))
    if "review" in t or "deep dive" in t or "hands-on" in t or "second brain" in t:
        return ("profile", pid or create_slug(t))
    if t.startswith("best ") and " for " in t:
        cat, uc = t[5:].split(" for ", 1)
        uc = re.split(r"\bin 20", uc, 1)[0]
        return ("best", create_slug(cat), create_slug(uc))
    return ("slug", create_slug(title))


def taken_keys(pool: list, published_titles: list, name2pid: dict) -> set:
    keys = set()
    for t in pool:
        title = (t.get("title") or "").strip()
        if title:
            keys.add(semantic_key(title, name2pid))
    for title in published_titles:
        if title:
            keys.add(semantic_key(title, name2pid))
    return keys


def published_titles() -> list:
    """Titles from every published article's frontmatter (for semantic dedup)."""
    titles = []
    if OUTPUT_DIR.exists():
        for f in OUTPUT_DIR.glob("*.md"):
            txt = f.read_text(encoding="utf-8")
            if txt.startswith("---"):
                parts = txt.split("---", 2)
                if len(parts) >= 3:
                    try:
                        fm = yaml.safe_load(parts[1]) or {}
                        if fm.get("title"):
                            titles.append(str(fm["title"]))
                    except yaml.YAMLError:
                        pass
    return titles


def fresh_pool_count(pool: list = None, published: set = None) -> int:
    """Topics in the pool whose article is NOT yet published (the usable buffer)."""
    pool = load_pool() if pool is None else pool
    published = published_slugs() if published is None else published
    return sum(1 for t in pool
               if (t.get("title") or "").strip()
               and create_slug(t["title"].strip()) not in published)


# --------------------------------------------------------------------------- #
# Generator
# --------------------------------------------------------------------------- #
def load_topic_map() -> dict:
    if not TOPIC_MAP.exists():
        return {}
    data = yaml.safe_load(TOPIC_MAP.read_text(encoding="utf-8")) or {}
    return data.get("products", {}) or {}


def _display_name(pid: str, catalog: dict) -> str:
    return str(catalog.get(pid, {}).get("display_name", pid)) or pid


def iter_candidate_topics(topic_map: dict = None, catalog: dict = None) -> list:
    """Ordered, deduped-by-self list of candidate topics from the curated map.

    Patterns (buyer-intent), interleaved ACROSS products within each tier so no
    single product dominates the front of the queue:
      1. {Product} vs {Competitor}        -> comparison
      2. {Product} review                 -> deep_dive
      3. Is {Product} worth it            -> deep_dive
      4. {Product} alternatives           -> comparison
      5. Best {category} for {use_case}   -> comparison
    Only products present in topic_map are emitted (curated = tracked-only), so a
    real tracked affiliate_url is guaranteed. A product without a tracked
    affiliate_url in the catalog is skipped defensively.
    """
    topic_map = load_topic_map() if topic_map is None else topic_map
    catalog = load_affiliate_catalog().get("programs", {}) if catalog is None else catalog

    # Keep only products that actually have an affiliate_url (defensive: the map
    # should already be tracked-only).
    products = [pid for pid in topic_map
                if (catalog.get(pid, {}).get("affiliate_url") or "").strip()]

    def name(pid):
        return _display_name(pid, catalog)

    out = []
    seen = set()

    def add(ttype, pid, title):
        s = create_slug(title)
        if s in seen:
            return
        seen.add(s)
        out.append({"type": ttype, "product": pid, "title": title})

    # Tier 1: vs competitor — round-robin across products by competitor index.
    maxc = max((len(topic_map[p].get("competitors", [])) for p in products), default=0)
    for i in range(maxc):
        for pid in products:
            comps = topic_map[pid].get("competitors", [])
            if i < len(comps):
                add("comparison", pid, f"{name(pid)} vs {comps[i]}: which is better in 2026")
    # Tier 2: review
    for pid in products:
        add("deep_dive", pid, f"{name(pid)} review 2026: features, pricing and verdict")
    # Tier 3: is it worth it
    for pid in products:
        add("deep_dive", pid, f"Is {name(pid)} worth it in 2026? An honest review")
    # Tier 4: alternatives
    for pid in products:
        cat = topic_map[pid].get("category", "tool")
        add("comparison", pid, f"{name(pid)} alternatives in 2026: top {cat} options")
    # Tier 5: best {category} for {use_case} — round-robin across products.
    maxu = max((len(topic_map[p].get("use_cases", [])) for p in products), default=0)
    for i in range(maxu):
        for pid in products:
            ucs = topic_map[pid].get("use_cases", [])
            cat = topic_map[pid].get("category", "tool")
            if i < len(ucs):
                add("comparison", pid, f"Best {cat} for {ucs[i]} in 2026")
    return out


def generate_new_topics(limit: int, pool: list = None,
                        topic_map: dict = None, catalog: dict = None):
    """Up to `limit` NEW topics that duplicate neither a published article nor a
    pool entry — by SLUG and by SEMANTIC key (so re-worded duplicates like
    "X vs Y: which is better" vs an existing "X vs Y: best ..." are caught).

    Returns (new_topics, remaining_candidates): remaining_candidates is how many
    additional unused, non-duplicate candidates still exist (low-supply signal).
    Never emits a duplicate or a nonsensical topic.
    """
    pool = load_pool() if pool is None else pool
    catalog = load_affiliate_catalog().get("programs", {}) if catalog is None else catalog
    name2pid = _name_to_pid(catalog)

    slug_taken = set(published_slugs()) | pool_slugs(pool)
    key_taken = taken_keys(pool, published_titles(), name2pid)

    chosen, chosen_keys, chosen_slugs = [], set(), set()
    remaining = 0
    for t in iter_candidate_topics(topic_map, catalog):
        s = create_slug(t["title"])
        k = semantic_key(t["title"], name2pid)
        if s in slug_taken or k in key_taken or s in chosen_slugs or k in chosen_keys:
            continue
        # a genuinely new, non-duplicate candidate
        if len(chosen) < max(0, limit):
            chosen.append(t)
            chosen_keys.add(k)
            chosen_slugs.add(s)
        else:
            remaining += 1
    return chosen, remaining
