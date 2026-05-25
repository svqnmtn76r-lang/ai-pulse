"""Match articles to affiliate products."""

from pathlib import Path
import yaml
from typing import Optional

AFFILIATE_CATALOG = Path("data/affiliate_sources.yml")

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

# Tier 1 products (only these are eligible for Day 2)
TIER_1_PRODUCTS = {
    "perplexity", "elevenlabs", "hubspot", "notion", "semrush", "shopify", "jasper"
}


def load_affiliate_catalog() -> dict:
    """Load affiliate_sources.yml."""
    with open(AFFILIATE_CATALOG) as f:
        return yaml.safe_load(f)


def get_product_keywords(product_id: str) -> list:
    """Get trigger keywords for a product."""
    catalog = load_affiliate_catalog()
    product = catalog.get("programs", {}).get(product_id, {})

    # Check if product has keywords defined
    if "trigger_keywords" in product:
        return product["trigger_keywords"]

    # Fall back to defaults
    return DEFAULT_KEYWORDS.get(product_id, [])


def calculate_match_score(
    product_id: str,
    article_title: str,
    article_summary: str,
) -> int:
    """Calculate match score (0-100) based on keyword presence."""
    keywords = get_product_keywords(product_id)

    if not keywords:
        return 0

    # Combine title and summary for searching
    text = (article_title + " " + article_summary).lower()

    # Count keyword matches
    match_count = 0
    for keyword in keywords:
        if keyword.lower() in text:
            match_count += 1

    # Score = hit count * 10, capped at 100
    # Bonus for title matches (more relevant)
    title_matches = sum(1 for kw in keywords if kw.lower() in article_title.lower())
    score = (match_count * 10) + (title_matches * 5)

    return min(score, 100)


def match_products(article: dict, min_score: int = 15) -> list:
    """
    Match article to affiliate products.
    Returns list of matched products (max 3, score >= min_score), sorted by score.

    min_score=15: title(10pt) + summary(5pt) = minimum viable match
    """
    title = article.get("title", "")
    summary = article.get("summary", "")

    matches = []

    for product_id in TIER_1_PRODUCTS:
        score = calculate_match_score(product_id, title, summary)

        if score >= min_score:
            catalog = load_affiliate_catalog()
            product = catalog.get("programs", {}).get(product_id, {})

            # Determine affiliate URL (if available)
            affiliate_url = None
            if product.get("status") == "ready_to_apply":
                # Will be added in later stages
                affiliate_url = f"https://aipulse.pages.dev/affiliates/{product_id}"

            keyword_matches = []
            keywords = get_product_keywords(product_id)
            text = (title + " " + summary).lower()
            for kw in keywords:
                if kw.lower() in text:
                    keyword_matches.append(kw)

            matches.append({
                "product_id": product_id,
                "name": product.get("display_name", product_id),
                "affiliate_url": affiliate_url,
                "match_score": score,
                "match_reason": f"keywords: {', '.join(keyword_matches[:3])}",
            })

    # Sort by score descending, return top 3
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches[:3]


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
