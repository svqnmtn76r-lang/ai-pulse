# Self-Replenishing Buyer-Intent Topic Pool — Final Report

Date: 2026-06-11 · Branch: `topic-autoreplenish` (NOT merged — Hiro's gate)
Model: claude-opus-4-8

## Goal

Keep the daily pipeline from ever hitting "rotation exhausted" for commercial
articles — by making the buyer-intent topic supply self-replenishing, relevant,
deduped against published articles, and capped to the existing ~25% commercial
share. Protects the forward match-rate gain (6.3%→27.8%) just shipped.

## Mechanism (Phase 0)

`run.py` cadence (`generate_product_articles`) consumes `data/product_topics.yml`
top-down, skipping published slugs, up to `product_cadence_count(news)` (1-6/run,
~4-6/day). When every fresh topic is consumed it logs "rotation exhausted" and
produces **zero** commercial articles that day. The pool was at **12 fresh / 18**
(~2-3 days left) with no top-up. Insertion point: **start of `run_pipeline`**,
before the cadence.

## What was built

1. **`data/topic_map.yml`** — curated competitor/category map, **tracked products
   only** (ElevenLabs, Shopify, Kinsta), 12 real competitors + 8 use-cases each.
   → **69 distinct candidate topics.** (Hiro verifies/extends; commercial topics
   are tracked-only so they always carry a real tracked link, never a fake block.)
2. **`src/pipeline/topic_pool.py`** — generator over buyer-intent patterns
   (`X vs Y`, `X review`, `is X worth it`, `X alternatives`,
   `best <category> for <use_case>`), interleaved across products. **Dedup is by
   slug AND by semantic key**, so a re-worded duplicate ("X vs Y: which is better"
   vs an existing "X vs Y: best …") is caught. `replenish_topic_pool()` tops the
   pool up to a target buffer when the fresh pool drops below a low threshold;
   `plan_replenishment()` is a pure, testable core.
3. **`run.py` Step 0** — calls `replenish_topic_pool()` before the cadence.
   Idempotent; wrapped so a top-up failure never blocks the run.
4. **Graceful degradation + alert** — when the map's combinations run low it adds
   what it can (never nonsense/duplicates) and emits a GitHub Actions
   `::warning::` annotation telling Hiro to extend the map. Never raises.

## Real numbers (measured)

### Top-up (Phase 2, run against the real pool)
`fresh 12 → 40 (+28 unique tracked-product topics), reserve 7.` Pool now 46
entries / 40 fresh. Gate verified: pool ≥ target, **0** internal dup slugs/keys,
**0** collisions vs published.

### Simulation (`scripts/simulate_topic_pool.py`, in-memory, no publish)

| scenario | days | K/day | produced | **dup slugs** | auto-generated | warns | pool emptied? | result |
|---|---|---|---|---|---|---|---|---|
| realistic | 10 | 5 | 50 | **0** | 28 | 1 (day 8) | no | **PASS** |
| stress | 14 | 6 | 68 | **0** | 28 | 5 | yes (day 13) | boundary |

- **10 days @ K=5 (realistic): PASS** — pool never empties, **zero** duplicate
  slugs. One low-supply warning fires on day 8 (the moment the map's reserve hits
  zero), ~4-5 days before any real shortfall.
- **14 days @ K=6 (stress):** the 3-product map (~69 combos + 12 legacy) is
  finite, so it drains by ~day 12-13. Crucially it **degrades gracefully** —
  produces *fewer* articles (2, then 0), **never a duplicate, never a crash**, and
  warns from day 7 onward. That is the designed "extend the map" trigger, not a
  failure mode.

### Projected buffer
At realistic K=5/day the current map sustains **~13-14 commercial-days**
(40 fresh + 28 reserve + legacy), and the warning gives **~4-5 days** of lead
time. Each added competitor ≈ +1 topic (+~0.2 day); each added tracked product
with ~12 competitors ≈ +20 topics (+~4 days).

## Dedup correctness

Zero duplicate slugs were produced across **all** simulated runs, and zero
fresh-pool entries collide with a published slug. Semantic dedup additionally
prevents re-worded duplicates (order-free `vs` pairs; one profile per product) —
covered by 15 unit tests, all passing.

## Hard rules honored

- Relevance/quality > volume: all topics from a curated map of real competitors;
  generator emits nothing nonsensical; exhaustion → fewer, not garbage.
- Dedup mandatory: slug + semantic, vs published + pool. 0 dups in every sim.
- Commercial topics → tracked products only (ElevenLabs/Shopify/Kinsta); no fake
  affiliate block for untracked products.
- Idempotent (no-op when healthy); branch only; no `.env`/backups; no new deps.

## Build

`npm run build` → exit 0, **284 pages**, "Complete!" (new data files + module
introduce no build breakage).

## Files touched

- `data/topic_map.yml` (new) · `src/pipeline/topic_pool.py` (new)
- `src/pipeline/run.py` (Step 0 wiring) · `data/product_topics.yml` (topped to 40 fresh)
- `tests/test_topic_pool.py` (new, 15 tests) · `scripts/simulate_topic_pool.py` (new)
- `docs/topic_autoreplenish_phase0.md`, `docs/topic_autoreplenish_report.md` (new)

## Commits (per phase)

- Phase 0 — inspection doc
- Phase 1 — curated map + generator + tests
- Phase 2 — auto top-up wired into run_pipeline (pool 12→40 fresh)
- Phase 3 — graceful low-supply + alert (tests)
- Phase 4 — extended map (69 combos) + simulation + this report

## 3-Axis self-score (CLAUDE.md §0.1.2)

> Pass: A + B + C ≥ 70 AND B ≥ 25.

| Axis | Cap | Score | Basis |
|---|---|---|---|
| **A — process** | 30 | **28** | Per-phase commits; 41 tests pass (15 new); assumptions verified (real consumption code read, sim on real state); docs (Phase 0 + report); token-thrift. |
| **B — implementation** | 40 | **37** | Top-up wired before cadence, idempotent, never-blocks (try/except); pure `plan_replenishment` for testability; **0 duplicate slugs** across all sims; tracked-only commercial topics (no fake blocks); commercial-share cap untouched; build passes. −3: ultimate buffer is bounded by a 3-product map (mitigated by early warning, but not infinite). |
| **C — data quality** | 30 | **26** | 69 curated, on-topic, real-competitor candidates; semantic dedup prevents re-worded dupes; graceful degradation; alert path (CI annotation). −4: Hiro still owns competitor-accuracy verification + map extension (the designed human step). |
| **Total** | 100 | **91** | **PASS** (≥70, B≥25). |

## "Metric improved" vs "done well" (honest)

- **Done well:** silent exhaustion is eliminated — the pool auto-refills, dedups
  perfectly (0 dups in every sim), degrades gracefully, and warns ~4-5 days
  early. The 10-day realistic gate **passes**.
- **Honest limitation:** with only 3 tracked products the topic space is finite
  (~69 combos), so indefinite operation depends on acting on the warning
  (extend `topic_map.yml`, or add a tracked product once it has a real affiliate
  link). The system guarantees *no silent death*, not infinite supply from a
  fixed map.

## Out of scope (noted)

New affiliate program applications (would add tracked products → more topics);
matcher/keyword changes; broader SEO infra.
