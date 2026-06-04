# Product Discovery + Cadence — result

Branch: `product-discovery-cadence` (off `main`). Three problems fixed in one cycle:
commercial articles were invisible on the site, SEO/canonical/sitemap were absent, and product
content was a decaying one-time batch. **Stopped before merge + push** (human gates).

"Commercial article" = frontmatter `products` non-empty (it carries an in-body affiliate block +
FTC disclosure). Count went from **10 → 11** this cycle (the cadence dry-run added one).

---

## Phase 1 — Discovery (homepage section + /reviews + nav)

- `blog/src/pages/index.astro`: new **"Reviews & Comparisons"** section, newest-first, top 6 +
  a `See all N →` link to `/reviews`. Reuses the existing `<article>` card markup + design tokens;
  adds a small `.product-badge` (from `data.products`) and `.section-title` styled like the about
  page's `h2`. The "Latest" news feed is unchanged below it.
- `blog/src/pages/reviews.astro` (new): lists **all** commercial articles; same card style + nav.
- Nav (`Home · Reviews · About`) added to home + /reviews.
- **Filter:** strictly `Array.isArray(products) && products.length > 0`. odysseus/karpathy
  (`products: []`) and all news articles are excluded. Verified: `/reviews` lists exactly the
  commercial set (10 at build time, 11 after Phase 3); 0 odysseus/karpathy references.

## Phase 2 — SEO + doc fix

- `astro.config.mjs`: `site: 'https://ai-pulse-b35.pages.dev'` + `@astrojs/sitemap` integration.
  Build emits `sitemap-index.xml` + `sitemap-0.xml` with **all absolute URLs** (166 pages incl.
  `/`, `/about`, `/reviews`, and every `/articles/…`).
- Absolute `<link rel="canonical">` added to article pages (there were none), home, and /reviews
  via `new URL(Astro.url.pathname, Astro.site)`. Verified on an article page:
  `https://ai-pulse-b35.pages.dev/articles/2026-06-03-elevenlabs-deep-dive-…/`.
- `CLAUDE.md`: corrected stale deploy domain `aipulse.pages.dev` → `ai-pulse-b35.pages.dev`.
- Dep: `@astrojs/sitemap@^3.7.3` added to `blog/package.json` + `package-lock.json`.

## Phase 3 — Cadence (daily product-article generation)

- `data/product_topics.yml` (new): **12 fresh** comparison/deep_dive topics (Appendix B), none
  overlapping the 10 already generated. Each names an affiliate product so the **brand≥1** matcher
  attaches it.
- `src/pipeline/run.py`: new **`[cadence]`** step (after news generation) → `generate_product_article()`:
  - **Dedup:** picks the first topic whose output file does not already exist, comparing
    `create_slug(title)` against existing filenames with the `YYYY-MM-DD-` prefix stripped (so a
    topic counts as done regardless of which day it ran). Default rate **1 per run** (tunable).
  - **Rotation exhausted:** logs `rotation exhausted — add topics to data/product_topics.yml` and
    returns None — no error, no repeat.
  - **Same path as everything else:** seeds the product from config → routes to the
    comparison/deep_dive template → product-page `affiliate_url` from `affiliate_sources.yml` → one
    in-body block → FTC disclosure. The pipeline's reconciler step then re-validates the match on the
    real body (brand≥1).
- `src/processors/claude_writer.py`: `generate_article_content(..., factual_source=False)` for
  product topics — the prompt **forbids invented prices/benchmarks/dates/feature claims** and uses
  qualitative comparison cells (honors CLAUDE.md "no fabricated claims"). News path unchanged
  (`factual_source=True`).
- `blog/src/content.config.ts`: `source_url` now accepts a valid URL **OR** empty string (original
  editorial like comparisons has no external source) **OR** absent. (The writer emits `source_url:
  ''` for sourceless articles; the old `z.string().url()` rejected it and broke the build.)

### Dry-run proof (one real Haiku call)
`generate_product_article()` produced `2026-06-04-perplexity-vs-google-ai-overviews-which-answers-be.md`:
- (a) **names** the product — `brand_hits(perplexity) = 14`;
- (b) **matches** via the real matcher → `['perplexity']` (brand≥1);
- (c) renders **one** `data-affiliate` block, href `https://www.perplexity.ai/pro` (product page, not
  `/affiliates`), + "contains affiliate links" FTC disclosure;
- (d) after sync+rebuild it appears in the **homepage Reviews section** and on **/reviews** (now 11).
- No fabricated prices/benchmarks; comparison table cells are qualitative ("Free tier available;
  paid plans for extended use", "Explicit inline citations", …).
- **Dedup:** the next run would pick `notion — Notion vs Coda` (not a repeat). **Exhausted** path
  logs the reminder and generates nothing.

## Phase 4 — Whole-site verification

- `npm run build`: green, 166 pages, sitemap emitted.
- `scripts/verify_render.py`: **OK** — 11 matched articles each render exactly one product-page
  block + FTC; **forbidden-pattern guard** and **bidirectional false-disclosure guard** pass;
  non-matched render zero blocks.
- `tests/test_affiliate_matcher.py`: 13/13. Full suite: **40 passed**, only the **3 pre-existing**
  `test_hackernews.py` failures remain (untouched this cycle).

---

## Commits on `product-discovery-cadence` (one per phase)
- `feat(discovery): surface commercial articles (homepage section + /reviews + nav)`
- `fix(seo): set astro site + absolute canonical/sitemap; correct deploy domain in CLAUDE.md`
- `feat(cadence): daily product-article generation from rotating topics (dedup-guarded)`
- `test(discovery): whole-site verification green`

## Status
- Branch clean; no secrets staged (only `.env.example`); `api_calls.db` still untracked; no new
  **Python** deps (`requirements.txt` unchanged; cadence uses existing PyYAML). One npm dep
  (`@astrojs/sitemap`) recorded in `blog/package.json` + lockfile.
- Match-rate note: this cycle is about **discovery + growth**, not the rate. Commercial count 10→11;
  the cadence grows it ~1/run going forward (until the 12-topic rotation is exhausted, then Hiro
  extends the list). Denominator also grows daily from bot news, so the % is not the headline metric.

## Open HUMAN gates (NOT done)
1. **Merge + push** of `product-discovery-cadence` (commands below).
2. Dub/Perplexity signup; swapping config `affiliate_url`s for real **tracked** referral links.
3. Tuning the cadence rate + extending `data/product_topics.yml`.

### Ready-to-run commands (for Hiro — NOT run by the agent)
```
git checkout main && git merge --no-ff product-discovery-cadence
git push origin main
```
With `api_calls.db` untracked the recurring binary conflict is gone. If `origin/main` has new bot
commits, integrate them with a plain **merge** (no rebase/force); if any **non-trivial** conflict
appears, **STOP** rather than hand-merge.

### Reviewer quick-path
- `cd blog && npm run build` — 166 pages + sitemap.
- open `blog/dist/index.html` (Reviews section) and `blog/dist/reviews/index.html` (all commercial).
- `grep -o 'rel="canonical" href="https://ai-pulse-b35[^"]*"' blog/dist/articles/*/index.html | head`.
- `PYTHONPATH=. python scripts/verify_render.py` — 11 matched, both guards green.
- `PYTHONPATH=. python -c "from src.pipeline.run import generate_product_article as g; print(g())"` —
  generates the next rotation topic (one Haiku call).
