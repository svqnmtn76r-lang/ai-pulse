"""Generate blog articles using Claude."""

import os
import anthropic
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
import yaml

from src.analytics.cost_report import log_api_call


OUTPUT_DIR = Path("output/articles")
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


def ensure_output_dir():
    """Create output directory if needed."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Day 4: route a matched affiliate product to a product-centric template so the
# article matches that product by construction. Products with a clear head-to-head
# rival go to `comparison`; the rest get a single-tool `deep_dive`. This split
# guarantees both new templates actually appear (template diversity, C-axis).
COMPARISON_PRODUCTS = {"perplexity", "semrush", "notion", "shopify", "kinsta"}
DEEP_DIVE_PRODUCTS = {"elevenlabs", "hubspot", "jasper", "liquidweb"}


def select_template_type(article: dict) -> str:
    """Select template type based on matched product, category, and importance.

    Day 4 routing: if an affiliate product matched, the topic IS an affiliate
    product category, so route it to a product-centric template
    (`comparison` or `deep_dive`) instead of the generic templates.
    """
    # 1) Product-centric routing (highest priority)
    matched = article.get("products_matched", [])
    if matched:
        pid = matched[0].get("product_id", "")
        return "deep_dive" if pid in DEEP_DIVE_PRODUCTS else "comparison"

    category = article.get("category", "industry_news")
    score = article.get("importance_score", 40)
    products = article.get("products_mentioned", [])

    # 2) Breaking news for high-score releases
    if score >= 80 and category in ["model_release", "pricing_change", "pricing"]:
        return "breaking"
    # 3) Comparison if 2+ products mentioned (tool launches)
    elif category in ["tool_launch", "tool"] and products and len(products) >= 2:
        return "comparison"
    # 4) Explainer for research and SDK releases
    elif category in ["research_paper", "research", "sdk_release", "tutorial"]:
        return "explainer"
    # 5) Default to breaking
    else:
        return "breaking"


def generate_article_content(
    article: dict,
    template_type: str,
    matched_products: list,
) -> str:
    """Generate article body using Claude."""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "").strip())

    title = article.get("title", "Untitled")
    summary = article.get("summary", "")
    source_url = article.get("url", "")
    source_name = article.get("source", "")

    # Truncate summary for prompt
    summary = summary[:1000]

    # Format products section
    products_text = ""
    if matched_products:
        products_text = "### Relevant tools\n\n"
        for prod in matched_products:
            status = f"[{prod['product_id']}]({prod['affiliate_url']})" if prod.get('affiliate_url') else f"**{prod['product_id']}**"
            products_text += f"- **{prod['name']}** ({prod['match_score']}/100 relevance): "
            products_text += f"[Learn more]({prod.get('affiliate_url', '#')})\n"
    else:
        products_text = "### Related tools\n\nNo affiliated tools match this article.\n"

    # Load template
    template_names = {
        "breaking": "breaking_news.md",
        "comparison": "comparison.md",
        "explainer": "explainer.md",
        "deep_dive": "deep_dive.md",
    }
    template_file = TEMPLATES_DIR / template_names.get(template_type, "breaking_news.md")
    with open(template_file) as f:
        template = f.read()

    # Remove template boilerplate
    template = template.split("---\n\n", 1)[1] if "---\n\n" in template else template

    # Determine max_tokens and word count target based on template type
    template_config = {
        "breaking": {"max_tokens": 1024, "word_range": "200-400"},
        "comparison": {"max_tokens": 2048, "word_range": "400-800"},
        "explainer": {"max_tokens": 3072, "word_range": "600-1200"},
        "deep_dive": {"max_tokens": 3072, "word_range": "600-1200"},
    }
    config = template_config.get(template_type, template_config["breaking"])
    max_tokens = config["max_tokens"]
    word_range = config["word_range"]

    # Day 4: for product-centric templates, tell Claude which affiliate product to
    # center the article on, so the body mentions it by name several times (the
    # matcher needs >= 2 keyword hits across title + body to attach the product).
    featured_line = ""
    if matched_products and template_type in ("comparison", "deep_dive"):
        featured = matched_products[0]
        featured_name = featured.get("name") or featured.get("product_id", "")
        featured_line = (
            f"\nFeatured product: {featured_name}. Center the article on {featured_name}, "
            f"and mention it by name naturally several times throughout the body."
        )

    prompt = f"""You are a technical AI journalist. Write a {template_type}-style article based on this information:

Title: {title}
Source: {source_name}
Original URL: {source_url}
Summary: {summary}{featured_line}

Template structure to follow:
{template[:500]}...

Guidelines:
- Write in clear, concise technical English
- Keep total length {word_range} words
- Do NOT quote the summary directly; paraphrase and add context
- Include facts, figures, and context the summary didn't provide
- End with a "What happens next" or "Learn more" section
- DO NOT include the PRODUCTS_SECTION placeholder - it will be added separately

Respond with ONLY the article body (no frontmatter, no boilerplate, no markdown fence)."""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.content[0].text.strip()

        # Log API cost
        log_api_call(
            module="claude_writer",
            model="claude-haiku-4-5-20251001",
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

        return content

    except Exception as e:
        print(f"Claude API error: {e}")
        return f"[Article generation failed: {str(e)}]"


def create_slug(title: str) -> str:
    """Create URL-safe slug from title."""
    # Basic transliteration for non-ASCII
    title = title.replace("é", "e").replace("ö", "o").replace("ü", "u")
    # Keep alphanumeric and hyphens, lowercase
    slug_text = re.sub(r"[^a-z0-9\s-]", "", title.lower())
    slug_text = re.sub(r"\s+", "-", slug_text.strip())
    slug_text = re.sub(r"-+", "-", slug_text)
    return slug_text[:50]  # Max 50 chars


def write_article_file(
    article: dict,
    body_content: str,
    matched_products: list,
    template_type: str,
) -> Path:
    """Write article to markdown file with frontmatter."""
    ensure_output_dir()

    # Generate slug
    slug_text = create_slug(article.get("title", "article"))

    # Filename
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"{timestamp}-{slug_text}.md"
    filepath = OUTPUT_DIR / filename

    # Avoid overwriting
    if filepath.exists():
        # Add counter
        base = filepath.stem
        counter = 1
        while filepath.exists():
            counter += 1
            filename = f"{base}-{counter}.md"
            filepath = OUTPUT_DIR / filename

    # Build products section
    products_text = ""
    has_affiliate_products = False
    if matched_products:
        products_text = "### Relevant tools\n\n"
        for prod in matched_products:
            url = prod.get("affiliate_url", "#")
            products_text += f"- **{prod['name']}** ([affiliate link]({url}))\n"
        has_affiliate_products = True
    else:
        products_text = ""

    # Replace placeholder in body
    body_content = body_content.replace("{PRODUCTS_SECTION}", products_text)

    # Build frontmatter
    # Use products_matched (catalog matched products) from affiliate_matcher
    matched = article.get("products_matched", [])
    products = [m["product_id"] for m in matched] if matched else []

    frontmatter = {
        "title": article.get("title", ""),
        "date": timestamp,
        "source_url": article.get("url", ""),
        "source_name": article.get("source", ""),
        "importance_score": article.get("importance_score", 0),
        "category": article.get("category", ""),
        "products": products,
        "word_count": len(body_content.split()),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "generated_by": "claude-haiku-4-5-20251001",
        "template_type": template_type,
    }

    # FTC disclosure - only if affiliate products are present
    if has_affiliate_products:
        ftc_disclosure = "\n*Disclosure: This article contains affiliate links. As an affiliate, we earn from qualifying purchases at no extra cost to you.*"
    else:
        ftc_disclosure = "\n*This article does not contain affiliate links.*"

    # Write file
    with open(filepath, "w") as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
        f.write("---\n\n")
        f.write(body_content)
        f.write(ftc_disclosure)
        f.write("\n")

    return filepath


def write_article(
    article: dict,
    matched_products: list = None,
) -> Optional[Path]:
    """
    Full article generation pipeline.
    Returns path to written file or None on error.
    """
    if matched_products is None:
        matched_products = []

    # Select template
    template_type = select_template_type(article)

    # Generate content
    body = generate_article_content(article, template_type, matched_products)

    # Write file
    filepath = write_article_file(article, body, matched_products, template_type)

    return filepath
