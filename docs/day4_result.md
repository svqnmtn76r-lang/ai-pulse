# Day 4 Result — Raise product-match-rate to ≥20%

Branch: `day4-matchrate`
Owner: Hiro · Executed by Claude Code (autopilot)

> This file is updated progressively, one section per phase. Numbers come from
> `scripts/match_report.py` run over real article output — no hardcoding.

---

## Phase 0 — Recon & baseline

### Real schema (the actual files win over the appendices)

- **`data/affiliate_sources.yml`** — products live under `programs.<id>`, each with a
  `trigger_keywords:` list (plus `category`, `competes_with`, `confidence`, `tier`, `status`, …).
  - Product IDs: `perplexity, elevenlabs, hubspot, notion, semrush, shopify, jasper, kinsta, liquidweb`.
  - ⚠️ The key is **`liquidweb`**, not `liquid_web` as written in Appendix B. Adapted accordingly.
- **Matcher** — `src/processors/affiliate_matcher.py`
  - `match_products(article, min_score=15)` scores on **title + summary**, `score = hits*10 + title_hits*5`,
    returns **top 3** products ≥ `min_score`.
  - `enrich_article_with_products(article)` → adds `products_matched`.
  - Restricted to `TIER_1_PRODUCTS` (excludes `kinsta`, `liquidweb`).
  - Gaps vs Day 4 rules: returns up to 3 products (violates one-product cap); threshold is a
    score, not an explicit ">=2 keyword hits". Both are fixed in Phase 1.
- **Templates** — `templates/{breaking_news,comparison,explainer}.md`. Selected by
  `claude_writer.select_template_type(article)` from `category` + `importance_score` +
  `products_mentioned`. `comparison` only fires when `category == tool_launch` AND
  `len(products_mentioned) >= 2` — so it effectively never fires. No `deep_dive` template exists.
- **Pipeline entry point** — `src/pipeline/run.py` (`python3 -m src.pipeline.run`), the local
  equivalent of `.github/workflows/daily-pipeline.yml`. fetch → score (Claude Haiku) → match → write.
- **Blog** — Astro v6 (`blog/`), content schema `blog/src/content.config.ts` already has a
  `products: z.array(z.string()).optional()` field; `index.astro` already uses `article.id` (good).

### Conflicts / notes

- **`docs/day4_instructions.md` (337 lines) does not exist.** Only `day1`–`day3` instruction docs are
  present. Nothing to reconcile; proceeded with this autopilot file as the source of truth.
- `.gitignore` did **not** cover `*.bak` / `.env.bak` — added before the first commit.
- Frontmatter `products` field is currently non-empty on only 2/38 generated articles.

### Baseline number

`scripts/match_report.py` over `output/articles` (38 files), with the Day 4 quality rule
(≥2 keyword hits across title+body, 1 product/article), current (un-expanded) keywords:

```
matched/total = 2/38 = 5.3%
```

Low single digits, consistent with the mission's expected ~3.8% (1/26 at the time the mission
was written; the repo now has 38 articles). **Baseline = 5.3%.**

**GATE 0: PASS** — baseline printed, schema + matcher understood.

---
<!-- Phases 1–5 appended below as they complete. -->
