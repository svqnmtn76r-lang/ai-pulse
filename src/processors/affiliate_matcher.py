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
    """Raw keyword-occurrence count across title + summary/body.

    Kept for reference/tests. The qualifying decision now lives in
    `score_product` (brand>=2 OR >=2 distinct non-brand keywords).
    """
    keywords = get_product_keywords(product_id)
    if not keywords:
        return 0

    text = (article_title + " " + article_summary).lower()
    return count_keyword_hits(keywords, text)


def brand_tokens_for(product_id: str, product: dict) -> list:
    """Brand token(s) for a product: lowercased display_name + id.

    For liquidweb both spellings ('liquid web', 'liquidweb') are brand tokens.
    """
    tokens = set()
    dn = str(product.get("display_name", "")).strip().lower()
    if dn:
        tokens.add(dn)
    if product_id:
        tokens.add(product_id.lower())
    if product_id == "liquidweb":
        tokens.update({"liquid web", "liquidweb"})
    return [t for t in tokens if t]


def score_product(text_lower: str, product_id: str, keywords: list, product: dict):
    """Tightened match rule (Day 4 matcher tightening).

    A product qualifies iff:
        brand_hits >= 2  OR  distinct_nonbrand_keywords >= 2
    across the (already-lowercased) text, where:
      - brand_hits = occurrences of the brand token(s);
      - distinct_nonbrand_keywords = count of DISTINCT non-brand trigger keywords
        present (repeated occurrences of one keyword count as ONE).

    This is strictly a tightening of the old "total occurrences >= 2" rule: a lone
    repeated generic keyword (e.g. workspace x4) no longer qualifies.

    Returns (qualifies, score, brand_hits, distinct_nonbrand). The score (for the
    one-product cap) prefers brand-driven matches, then keyword diversity.
    """
    brands = brand_tokens_for(product_id, product)
    brand_hits = sum(text_lower.count(b) for b in brands)
    nonbrand = {kw.lower() for kw in keywords} - set(brands)
    distinct_nonbrand = sum(1 for kw in nonbrand if kw in text_lower)
    qualifies = (brand_hits >= 2) or (distinct_nonbrand >= 2)
    score = brand_hits * 10 + distinct_nonbrand
    return qualifies, score, brand_hits, distinct_nonbrand


def match_products(article: dict) -> list:
    """
    Match article to affiliate products.

    Guardrails (Day 4):
    - a product qualifies only under `score_product`'s rule
      (brand_hits >= 2 OR >= 2 distinct non-brand keywords) across title+body;
    - at most ONE product is returned (the single highest-scoring one).

    Returns a list of 0 or 1 product dicts (list kept for caller compatibility).
    """
    title = article.get("title", "")
    # Use summary if present; fall back to body (so the same logic works whether
    # matching happens pre-generation on the summary or post-hoc on the body).
    summary = article.get("summary", "") or article.get("body", "")
    text_lower = (title + " " + summary).lower()

    catalog = load_affiliate_catalog()
    programs = catalog.get("programs", {})

    candidates = []
    for product_id in eligible_products():
        product = programs.get(product_id, {})
        keywords = get_product_keywords(product_id)
        qualifies, score, brand_hits, distinct_nb = score_product(
            text_lower, product_id, keywords, product
        )
        if qualifies:
            candidates.append((score, brand_hits, distinct_nb, product_id))

    if not candidates:
        return []

    # Highest score wins; brand_hits then distinct then id break ties deterministically.
    candidates.sort(key=lambda c: (c[0], c[1], c[2], c[3]), reverse=True)
    score, _brand_hits, _distinct_nb, product_id = candidates[0]

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
