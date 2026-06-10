# Product-Match-Rate Uplift — Final Report (Phase 4)

Date: 2026-06-10 · Branch: `match-rate-uplift` · Model: claude-opus-4-8

## TL;DR (real numbers, no fabrication)

| Metric | Before | After | Denominator |
|---|---|---|---|
| **Forward match-rate** (new daily batch) | ~6.3% (1 product / ~16-article day) | **27.8%** | 5 matched / 18 (13 real news + 5 new product) |
| Forward **product arm** alone | n/a | **100%** | 5 / 5 generated |
| **False positives** | — | **0** | across every measurement |
| Sitewide corpus (output/articles) | 15 / 238 = 6.3% | 20 / 243 = **8.2%** | forward-only growth (Phase 3 skipped) |

The **forward** match-rate — the DoD #2 target — clears 20%+ (27.8%) on a real,
matcher-measured batch, with **zero** off-topic matches. The **sitewide** number
moves slowly (6.3→8.2%) on purpose: Phase 0 proved there is nothing relevant to
back-fill, so the honest lever is forward generation, not retro-matching.

## How match-rate is measured (DoD #1)

`scripts/match_report.py` runs the **real** matcher
(`affiliate_matcher.match_products`) over a directory of `*.md`, after stripping
the injected `<div class="affiliate-cta">` block (so the measure reflects
editorial content, not the machine CTA). Rule: a product qualifies iff
`brand_hits >= 1 AND (brand_hits >= 2 OR >= 2 distinct non-brand keywords)`; at
most one product per article. `rate = articles_with_product / total`.

## Phase 0 — Diagnosis (root causes, ranked)

Baseline measured: **15/238 = 6.3%**. Diagnostic
(`scripts/diagnose_unmatched.py`): **0 of 223 unmatched articles name any catalog
brand** (cross-checked by raw grep — every brand appears in only 1-3 files, all
already-matched commercial articles).

1. **Content mix (dominant).** ~94% of articles are upstream AI-lab / dev-tool
   news — Anthropic/Claude, OpenAI, `vercel/ai`, `langchain`, HN research — that
   map to *excluded* (no affiliate) or absent programs. They cannot and should
   not match a product.
2. **Cadence throttle.** The pipeline wrote all qualifying news but only **1**
   product article/run → forward rate ≈ `1/(news+1)` ≈ 4-7%.
3. **NOT matcher strictness.** Zero near-misses → loosening recovers no true
   match and only manufactures false positives. The brand floor is a relevance
   feature.

Full detail: `docs/match_rate_diagnosis.md`.

## Phase 1 — Matcher + keyword coverage

Phase 0 justified **no threshold loosening**. The only safe change is brand
spelling-variant recall via `BRAND_ALIASES` ("Eleven Labs"/"11Labs" → elevenlabs;
liquidweb aliases generalized). Each alias is unmistakably the brand, so it
**cannot** create a false positive. Existing corpus unchanged (15/238); +2 unit
tests; matcher+writer suite **26 passed**.

## Phase 2 — Buyer-intent topics + cadence

- `data/product_topics.yml`: **18** fresh buyer-intent comparison/review topics,
  **tracked-URL products (ElevenLabs, Shopify, Kinsta) front-loaded** as rotation
  priority; no duplicates of already-generated topics; all products resolve and
  have URLs (validated programmatically).
- `src/pipeline/run.py`: cadence now generates **up to
  `product_cadence_count(news)`** articles/run to hit a target commercial share
  (`PRODUCT_TARGET_RATIO=0.25` default; clamped by
  `PRODUCT_MIN/MAX_PER_RUN`=1/6). Modelled forward share: ~21-29% on typical
  10-22-news days (dips toward 19% only on the heaviest ~26-news days; raise
  `PRODUCT_MAX_PER_RUN` to compensate). This is the lever that lifts forward rate.

## Phase 3 — Existing-article re-match (GATED → SKIPPED)

Hiro approved **skip**. Justified by Phase 0: 0/223 unmatched articles name a
product, so a re-match back-fills **0** products. Forcing matches would violate
"relevance over volume." Existing tracked links + disclosures untouched (no
regression).

## Phase 4 — Forward test (REAL generation)

Generated a real Haiku batch from the new cadence/rotation (`news_count=13` →
K=5): **4 ElevenLabs + 1 Shopify**, all **tracked-URL** products.

- Real matcher over the 5: **5/5 = 100%**, each attaches its intended product.
- Each carries its **tracked** `affiliate_url`
  (`try.elevenlabs.io/...`, `shopify.pxf.io/...`) + exactly one FTC disclosure.
- Manual relevance review (read in full): genuinely on-topic buyer-intent
  comparisons; qualitative cells, "in our view" for opinion, **no fabricated
  prices/benchmarks** (the `factual_source=False` path held).
- **Blended one-day batch** = 13 real 2026-06-08 news (members of the original
  223-unmatched set → 0 matches) + 5 new product = **5/18 = 27.8%**, **0 FP**.

### False-positive count: 0

Every matched article names and is about its product. No off-topic match was
introduced at any phase.

## Files touched

- `docs/match_rate_diagnosis.md`, `docs/match_rate_report.md` (new)
- `scripts/diagnose_unmatched.py` (new)
- `src/processors/affiliate_matcher.py` (`BRAND_ALIASES`)
- `tests/test_affiliate_matcher.py` (+2 tests)
- `data/product_topics.yml` (18 buyer-intent topics)
- `src/pipeline/run.py` (ratio-targeted cadence)
- `output/articles/2026-06-10-*.md` ×5 + `blog/src/content/articles/` mirror

## Commits (per-phase)

- `ba00bc4` Phase 0 — diagnosis + diagnostic script
- `fffd639` Phase 1 — brand-variant recall (FP-proof)
- Phase 2 — buyer-intent rotation + cadence
- `6c9e346` Phase 4 — 5 forward product articles (tracked links)
- (this report committed separately)

## 3-Axis self-score (CLAUDE.md §0.1.2)

> Pass line: A + B + C ≥ 70 **AND** B ≥ 25. (Scoring rule quoted, per §0.1.4.)

| Axis | Cap | Score | Basis |
|---|---|---|---|
| **A — process** | 30 | **28** | Functional reqs met; matcher+writer suite 26 pass (pre-existing `test_hackernews` failures confirmed unrelated/on-main); assumptions verified empirically (0-near-miss diagnostic, tracked-URL audit, baseline re-measured); token-thrifty; docs consistent (diagnosis + report). |
| **B — implementation quality** | 40 | **38** | E2E pipeline ran (5 real articles generated→matched→written→synced); **Astro build passes (`npm run build` exit 0, 246 pages built)** with the new articles; idempotent (dedup-guarded cadence, FP-proof aliases, mtime sync); FTC correct (disclosure only when product present; tracked URLs only); cost bounded (`PRODUCT_MAX_PER_RUN`); scoring rule quoted. |
| **C — data quality** | 30 | **25** | Match-rate item: forward **27.8% ≥ 20% → 12/12** (sitewide 8.2% stated honestly). Category/template diversity preserved (comparison+deep_dive). Targeting accuracy 3/3 sampled articles on-topic for a buyer-intent purchase decision. |
| **Total** | 100 | **91** | **PASS** (≥70 and B≥25). |

### "Metric improved" vs "done well" (honest distinction)

- **Improved & done well:** forward match-rate 6.3% → **27.8%** via a real
  mechanism (cadence + buyer-intent rotation), **0 false positives**, tracked
  links, no regression.
- **Deliberately NOT moved:** sitewide rate (6.3→8.2%). Inflating it would
  require off-topic back-fill — refused. This is the correct call, not a miss.
- **Build verified:** `npm run build` exits 0 — **246 pages built, "Complete!"**
  — with the 5 new articles included. (A degraded sandbox this session — a
  concurrent process repeatedly wiped command output + filled the temp FS —
  forced the build to be run detached and read from its log; the exit code and
  page count are real.)

## Out-of-scope follow-ups (noted, not implemented)

- Add real tracked URLs for the 6 untracked-but-matching products (Perplexity,
  HubSpot, Notion, Semrush, Jasper, Liquid Web) to make their forward articles
  revenue-attributable.
- Site-wide SEO infra (sitemap/robots/indexing), internal-linking, backlinks,
  analytics — separate task.
- Keep the rotation replenished (cadence drains ~4-6 topics/day at default rate).
