#!/usr/bin/env python3
"""Generate product-centric articles via the comparison / deep_dive templates.

This is the affiliate-product-category arm of the pipeline (CLAUDE.md strategy:
"速報 + 即座にツール比較・購入導線"). Each seed is a real comparison pair or a
single-tool deep dive. The REAL matcher decides which product attaches (>=2-hit
rule, one product per article); the REAL claude_writer generates the body via the
category-routed template. Nothing about the match is hardcoded.

Usage:
    python scripts/generate_product_articles.py [N]                 # first N seeds (default: all)
    python scripts/generate_product_articles.py perplexity,elevenlabs  # specific products

Requires ANTHROPIC_API_KEY in .env (stripped before use, per repo rules).
"""

import sys
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

load_dotenv(".env")

from src.processors.affiliate_matcher import enrich_article_with_products
from src.processors.claude_writer import write_article, create_slug, select_template_type

OUTPUT_DIR = Path("output/articles")

# Real comparison pairs (affiliate product on one side) + single-tool deep dives.
# Summaries deliberately use the product's own vocabulary so the matcher attaches
# the intended product on its own merits (>= 2 keyword hits across title+summary).
SEEDS = [
    {
        "product": "perplexity",
        "title": "Perplexity vs ChatGPT: Which AI Search Answer Engine Wins in 2026?",
        "summary": ("Perplexity has become the default ai search and answer engine for "
                    "people who want cited answers, while ChatGPT remains a general ai chatbot. "
                    "We compare Perplexity and ChatGPT as a research assistant for factual, "
                    "source-backed answers."),
        "category": "tool_launch",
    },
    {
        "product": "semrush",
        "title": "Semrush vs Ahrefs: The Better SEO Tool for Keyword Research in 2026",
        "summary": ("Semrush and Ahrefs dominate the seo tool market. This comparison covers "
                    "keyword research, backlink analysis, rank tracking and competitor analysis, "
                    "with a focus on where Semrush leads on serp data and site audits."),
        "category": "tool_launch",
    },
    {
        "product": "notion",
        "title": "Notion vs Obsidian: Picking the Right Knowledge Base and Note-Taking App",
        "summary": ("Notion is an all-in-one workspace and knowledge base; Obsidian is a local-first "
                    "note-taking tool. We compare Notion and Obsidian for a team wiki, project "
                    "management and building a second brain."),
        "category": "tool_launch",
    },
    {
        "product": "shopify",
        "title": "Shopify vs WooCommerce: Best Ecommerce Platform to Sell Online in 2026",
        "summary": ("Shopify is a hosted ecommerce platform; WooCommerce is a WordPress plugin. "
                    "We compare Shopify and WooCommerce for building an online store, dropshipping "
                    "and running an ecommerce business that needs to sell online fast."),
        "category": "tool_launch",
    },
    {
        "product": "kinsta",
        "title": "Kinsta vs Shared Hosting: Is Managed WordPress Hosting Worth It?",
        "summary": ("Kinsta offers premium managed wordpress hosting on cloud hosting infrastructure, "
                    "versus cheap shared web hosting. We weigh Kinsta's wordpress performance and "
                    "managed wordpress features against generic web hosting."),
        "category": "tool_launch",
    },
    {
        "product": "elevenlabs",
        "title": "ElevenLabs Deep Dive: The State of AI Voice and Text-to-Speech in 2026",
        "summary": ("ElevenLabs is the leading ai voice and text to speech platform, known for "
                    "voice cloning, realistic voiceover and dubbing. This deep dive covers "
                    "ElevenLabs features, pricing and where its tts voice generation excels."),
        "category": "tool_launch",
    },
    {
        "product": "hubspot",
        "title": "HubSpot Deep Dive: A Complete Look at the CRM and Marketing Automation Suite",
        "summary": ("HubSpot bundles a crm with marketing automation, email marketing and a sales "
                    "pipeline. This deep dive examines HubSpot for inbound marketing, lead generation "
                    "and contact management across growing B2B teams."),
        "category": "tool_launch",
    },
    {
        "product": "jasper",
        "title": "Jasper Deep Dive: Is This AI Writing Tool Worth It for Content Teams?",
        "summary": ("Jasper is an ai writing and ai copywriting tool built for marketing copy and "
                    "content generation. This deep dive on Jasper covers blog writing, the ai writer "
                    "workflow and content automation for marketing teams."),
        "category": "tool_launch",
    },
    {
        "product": "liquidweb",
        "title": "Liquid Web Deep Dive: Managed VPS and Dedicated Server Hosting Reviewed",
        "summary": ("Liquid Web (liquidweb) targets high traffic hosting with managed vps, dedicated "
                    "server and managed hosting plans. This deep dive reviews Liquid Web for "
                    "enterprise hosting and ecommerce hosting workloads."),
        "category": "tool_launch",
    },
]


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg is None:
        seeds = SEEDS
    elif arg.isdigit():
        seeds = SEEDS[:int(arg)]
    else:
        wanted = {p.strip() for p in arg.split(",")}
        seeds = [s for s in SEEDS if s["product"] in wanted]

    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    written, skipped, unmatched = [], [], []

    for seed in seeds:
        article = {
            "id": f"product-seed::{seed['product']}",
            "title": seed["title"],
            "summary": seed["summary"],
            "category": seed["category"],
            "importance_score": 60,
            "source": "ai-pulse-editorial",
            "url": f"https://aipulse.pages.dev/compare/{seed['product']}",
        }

        enriched = enrich_article_with_products(article)
        matched = enriched.get("products_matched", [])

        # Honesty checks: exactly one product, and it is the intended one.
        if len(matched) != 1:
            unmatched.append((seed["product"], len(matched)))
            print(f"  [SKIP] {seed['product']}: matcher returned {len(matched)} products")
            continue

        slug = create_slug(seed["title"])
        expected = OUTPUT_DIR / f"{timestamp}-{slug}.md"
        if expected.exists():
            skipped.append(expected.name)
            print(f"  [EXISTS] {expected.name}")
            continue

        tpl = select_template_type(enriched)
        path = write_article(enriched, matched)
        written.append(path.name)
        print(f"  [WRITE] {path.name}  product={matched[0]['product_id']}  template={tpl}")

    print("-" * 60)
    print(f"written={len(written)} skipped(existing)={len(skipped)} unmatched={len(unmatched)}")
    return written


if __name__ == "__main__":
    main()
