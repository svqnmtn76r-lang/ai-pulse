# Product-Match-Rate Diagnosis (Phase 0)

Date: 2026-06-09 · Branch: `match-rate-uplift`

## How match-rate is measured

`scripts/match_report.py` calls the **real** matcher
(`src.processors.affiliate_matcher.match_products`) over every `*.md` in
`output/articles/`. For each article it:

1. parses `title` (frontmatter) + `body`,
2. **strips the machine-injected `<div class="affiliate-cta">` block** so the
   measurement reflects *editorial* content only (no circular self-match),
3. applies the matcher's qualifying rule, attaching **at most one** product
   (highest score).

**Match rule** (`score_product`), per product, over lowercased title+body:

- `brand_hits` = occurrences of the brand token(s) (`display_name` + `id`).
- `distinct_nonbrand` = number of *distinct* non-brand trigger keywords present.
- **Qualifies iff** `brand_hits >= 1` **AND** (`brand_hits >= 2` **OR**
  `distinct_nonbrand >= 2`).

The **brand floor** (`brand_hits >= 1`) means a product is only attached if the
article actually **names** it. This is a deliberate relevance guard (drops
competitor-mismatches, e.g. an Obsidian article never matches Notion).

`match-rate = (articles with >= 1 matched product) / (total articles)`.

## Measured baseline

```
matched/total = 15/238 = 6.3%
```

All 15 matches are the deliberately-generated commercial articles
(comparison / deep_dive). The matcher attaches the intended product on every one
with **zero off-topic matches**.

## Root-cause analysis of the 223 unmatched articles

Diagnostic (`/tmp/phase0_diag.py`, reproducible): for each unmatched article,
score every eligible product and count brand mentions.

> **Unmatched articles that name *any* catalog brand even once: 0 / 223.**

Raw cross-check (case-insensitive grep over all 238 files) — every brand name
appears in only 1–3 files, and those files are the already-matched commercial
articles:

| brand | files containing it |
|---|---|
| perplexity | 3 | elevenlabs | 1 | shopify | 2 | kinsta | 1 |
| notion | 2 | semrush | 2 | jasper | 2 | hubspot | 2 | liquid web | 1 |

The unmatched corpus is **upstream AI-lab news and dev-tool releases** with no
relevant affiliate product:

- Anthropic / Claude announcements (acquisitions, funding, model releases) →
  **excluded program** (no affiliate, per CLAUDE.md §2.3).
- OpenAI items → **excluded program**.
- `vercel/ai`, `langchain`, `anthropic-sdk-python`, `claude-code` GitHub
  releases → no affiliate program exists.
- Hacker News research posts (genome sequencing, LLM-agent papers, prompt
  politeness) → no product.

## Ranked root causes

1. **Content mix (dominant cause).** ~94% of articles are upstream AI-lab /
   open-source-tool news that legitimately maps to **no** catalog product
   (Anthropic/OpenAI are explicitly *excluded* — they have no affiliate
   program). The matcher cannot and should not attach a product to them.
2. **Forward cadence throttle.** `src/pipeline/run.py` writes *all* qualifying
   news articles per run but generates only **ONE** product article per run
   (`generate_product_article`). So forward rate ≈ `1 / (news_count + 1)` ≈
   5–9%, which is exactly the observed sitewide number.
3. **NOT a cause: matcher strictness / thin keywords.** There are **zero**
   near-misses — no unmatched article names a brand at all, so loosening the
   threshold or adding keywords recovers **no true matches**; it would only
   manufacture false positives. The brand floor is working as a relevance
   feature, not a bug.

## Linkable products (real tracked URL vs placeholder homepage)

From `data/affiliate_sources.yml` `affiliate_url`:

| product | URL | tracked? |
|---|---|---|
| **elevenlabs** | `try.elevenlabs.io/lls9tf5hbp3e` | ✅ tracked |
| **shopify** | `shopify.pxf.io/1GRvJ9` | ✅ tracked |
| **kinsta** | `kinsta.com/?kaid=OHVLIYLXQQNA` | ✅ tracked |
| perplexity | `perplexity.ai/pro` | ⚠️ homepage, untracked |
| hubspot | `hubspot.com` | ⚠️ homepage, untracked |
| notion | `notion.com` | ⚠️ homepage, untracked |
| semrush | `semrush.com` | ⚠️ homepage, untracked |
| jasper | `jasper.ai` | ⚠️ homepage, untracked |
| liquidweb | `liquidweb.com` | ⚠️ homepage, untracked |

Only **ElevenLabs, Shopify, Kinsta** carry a real tracked link today (matches
the task's "approved/tracked" set). The other six match relevantly but their
links are not yet revenue-attributable.

## Implication for the uplift

- The number does **not** move by loosening the matcher or back-filling the
  existing news corpus — there is nothing relevant to back-fill (Phase 3 would
  attach **0** products honestly).
- It moves by **increasing the share of genuinely product-relevant articles
  going forward**: stock the buyer-intent topic rotation (Phase 2) and raise the
  product-article cadence so each daily batch reaches ≥20% commercial share,
  prioritising the three tracked products. Every such article matches its named
  product by construction → on-topic, zero false positives, tracked link.
