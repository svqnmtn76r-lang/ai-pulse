"""Match articles to affiliate products.

Day 4 guardrails:
- A product matches only if its trigger_keywords hit >= MATCH_MIN_HITS (2) times
  across the article text (title + summary/body). A single incidental mention
  does NOT count -- this protects data quality (CLAUDE.md C-axis).
- AT MOST ONE product is attached per article (the single highest-scoring one).
"""

from pathlib import Path
import yaml
from typing import Optional

AFFILIATE_CATALOG = Path("data/affiliate_sources.yml")

# Quality threshold: keywords must hit at least this many times across the
# article text for the product to count as a match. Do NOT lower below 2.
MATCH_MIN_HITS = 2

# Default keywords per product (used if not in affiliate_sources.yml)
DEFAULT_KEYWORDS = {
    "perplexity": ["perplexity", "search", "pplx", "reasoning"],
    "elevenlabs": ["voice", "text-to-speech", "tts", "elevenlabs", "speech synthesis"],
    "hubspot": ["hubspot", "crm", "marketing automation", "sales"],
    "notion": ["notion", "database", "wiki", "workspace", "notes"],
    "semrush": ["semrush", "seo", "marketing", "analytics", "keyword"],
    "shopify": ["shopify", "ecommerce", "store", "merchant", "commerce"],
    "jasper": ["jasper", "copywriting", "content generation", "ai writing"],
    "kinsta": ["kinsta", "hosting", "wordpress", "web hosting"],
}

# Tier 1 products (kept for reference / backward compat)
TIER_1_PRODUCTS = {
    "perplexity", "elevenlabs", "hubspot", "notion", "semrush", "shopify", "jasper"
}


def load_affiliate_catalog() -> dict:
    """Load affiliate_sources.yml."""
    with open(AFFILIATE_CATALOG) as f:
        return yaml.safe_load(f)


def eligible_products() -> list:
    """Every program that has trigger_keywords is a match candidate.

    Day 4: kinsta/liquidweb (tier 2) are now eligible too, since their keywords
    were expanded and WP-hosting topics route to product-centric templates.
    """
    catalog = load_affiliate_catalog()
    programs = catalog.get("programs", {})
    return [pid for pid, data in programs.items() if data.get("trigger_keywords")]


def get_product_keywords(product_id: str) -> list:
    """Get trigger keywords for a product."""
    catalog = load_affiliate_catalog()
    product = catalog.get("programs", {}).get(product_id, {})

    # Check if product has keywords defined
    if "trigger_keywords" in product:
        return product["trigger_keywords"]

    # Fall back to defaults
    return DEFAULT_KEYWORDS.get(product_id, [])


def count_keyword_hits(keywords: list, text_lower: str) -> int:
    """Total number of keyword occurrences in already-lowercased text."""
    return sum(text_lower.count(kw.lower()) for kw in keywords)


def calculate_match_score(
    product_id: str,
    article_title: str,
    article_summary: str,
) -> int:
    """Match score = number of keyword hits across title + summary/body.

    A hit is one occurrence of a trigger keyword. Score is the raw hit count;
    callers compare it against MATCH_MIN_HITS (>= 2 to qualify).
    """
    keywords = get_product_keywords(product_id)
    if not keywords:
        return 0

    text = (article_title + " " + article_summary).lower()
    return count_keyword_hits(keywords, text)


def match_products(article: dict, min_hits: int = MATCH_MIN_HITS) -> list:
    """
    Match article to affiliate products.

    Guardrails (Day 4):
    - a product qualifies only with >= min_hits (default 2) keyword hits across
      title + summary/body;
    - at most ONE product is returned (the single highest-scoring one).

    Returns a list of 0 or 1 product dicts (list kept for caller compatibility).
    """
    title = article.get("title", "")
    # Use summary if present; fall back to body (so the same logic works whether
    # matching happens pre-generation on the summary or post-hoc on the body).
    summary = article.get("summary", "") or article.get("body", "")
    title_lower = title.lower()

    catalog = load_affiliate_catalog()
    programs = catalog.get("programs", {})

    candidates = []
    for product_id in eligible_products():
        score = calculate_match_score(product_id, title, summary)
        if score >= min_hits:
            keywords = get_product_keywords(product_id)
            title_hits = count_keyword_hits(keywords, title_lower)
            candidates.append((score, title_hits, product_id))

    if not candidates:
        return []

    # Highest hit count wins; title hits then id break ties deterministically.
    candidates.sort(key=lambda c: (c[0], c[1], c[2]), reverse=True)
    score, _title_hits, product_id = candidates[0]

    product = programs.get(product_id, {})
    # Affiliate URL comes from the product config (never hardcoded / placeholder /
    # homepage). Hiro replaces these with real tracked links after signup.
    affiliate_url = product.get("affiliate_url")

    keywords = get_product_keywords(product_id)
    text = (title + " " + summary).lower()
    keyword_matches = [kw for kw in keywords if kw.lower() in text]

    return [{
        "product_id": product_id,
        "name": product.get("display_name", product_id),
        "affiliate_url": affiliate_url,
        "match_score": score,
        "match_reason": f"keywords: {', '.join(keyword_matches[:3])}",
    }]


def enrich_article_with_products(article: dict) -> dict:
    """Add matched products to article dict.

    重要: products_mentioned は scorer の出力（記事内言及製品名）を保持。
    本関数は products_matched (catalog マッチ結果) のみを追加し、
    products_mentioned には触れない。
    """
    matches = match_products(article)

    return {
        **article,
        "products_matched": matches,
    }
