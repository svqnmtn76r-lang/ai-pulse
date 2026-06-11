# Phase 0 — Topic-Pool Consumption & Drain (inspection)

Date: 2026-06-11 · Branch: `topic-autoreplenish`

## How `data/product_topics.yml` is consumed

`src/pipeline/run.py`:

- **`generate_product_articles(news_count)`** (lines ~115-150) is the cadence.
  It loads the pool, then iterates topics **top-down**, skipping any whose slug
  is already published, and generates **up to `product_cadence_count(news_count)`**
  commercial articles. Each picked topic → `_generate_one_topic` → seeds the
  product as the match, routes to comparison/deep_dive, names the product, injects
  the product's `affiliate_url` block + FTC disclosure.
- **`existing_article_slugs()`** (lines 33-41) — published-slug set, built from
  `output/articles/*.md` with the `YYYY-MM-DD-` prefix stripped (a topic counts
  as done regardless of generation date).
- **`product_cadence_count(news_count)`** (lines 44-66) — commercial share logic:
  `k = ceil(target*news/(1-target))`, `target = PRODUCT_TARGET_RATIO` (default
  **0.25**), clamped to `[PRODUCT_MIN_PER_RUN=1, PRODUCT_MAX_PER_RUN=6]`. So the
  daily drain is **1-6 topics/run** (≈4-6 on typical 12-22-news days).

## "Rotation exhausted" detection

`generate_product_articles` lines 148-149: if **no** article was written this run
(every fresh topic consumed), it prints
`"  rotation exhausted — add topics to data/product_topics.yml"` and returns `[]`.
No error, no repeat — but **that day produces zero commercial articles**, which
silently kills the forward match-rate gain.

## Current pool size + drain rate

- Pool total: **18** topics; **6** already published; **12 fresh (usable)**.
- Drain: up to 6/run, ≈4-6/day typical → **~2-3 days of buffer remaining.**

## Dedup status

- **Published-slug dedup EXISTS** in the cadence (`slug in existing_article_slugs()`
  skip). So duplicates are never *generated*. But:
- The **pool is never replenished** and is **not** itself deduped/topped-up — it
  just drains to empty. There is no top-up step.

## Notification path

- The repo's `daily-pipeline.yml` has **no** GitHub-Issue / email step. `GH_TOKEN`
  IS available in the "Run pipeline" step's env. The workflow's "Commit new
  articles" step `git add output/articles/ blog/src/content/articles/ data/` —
  so **writing `data/product_topics.yml` (and a new `data/topic_map.yml`) is
  auto-committed**, which is the natural persistence path for a top-up.
- Phase 3 will surface low-supply via a **GitHub Actions `::warning::` annotation**
  + stdout (the idiomatic, non-spammy notification on this CI); can be upgraded to
  issue-creation later.

## Top-up insertion point

At the **start of `run_pipeline`** (after `init_db()`, before fetching), so the
pool is refreshed *before* the Step-5 cadence (`run.py:~307-311`,
`generate_product_articles(news_count=news_written)`) selects topics. Cadence
behaviour and the 25% commercial-share cap are left unchanged — only the supply
is kept fed.
