# SEO Foundation — Final Report (Phases 1-4)

Date: 2026-06-11 · Branch: `seo-foundation` (NOT merged — Hiro's gate)
Model: claude-opus-4-8 · Verified against the real built `dist/` output.

## Honest expectation
This fixes the technical/on-page foundation so pages **can** rank and earn
click-through. Actual ranking/traffic gains compound over weeks and are not
measurable today — no traffic numbers are claimed here.

## Before → after (gap closure vs Phase 0 audit)

| # | Gap (Phase 0) | Status |
|---|---|---|
| 1 | Meta description = the title duplicated on all 281 articles | ✅ **Fixed** — money pages get a query-aligned templated description from real fields; news pages get a cleaned body excerpt. Unique per page. |
| 2 | No structured data | ✅ **Fixed** — `Article` + `BreadcrumbList` JSON-LD on all 281 articles (real data); `FAQPage` only for genuine Q&A. |
| 3 | No internal linking between articles | ✅ **Fixed** — "Related comparisons & reviews" block on money pages (shared-product, ≤5). |
| 4 | Two `<h1>` per page | ✅ **Fixed** — header brand demoted to a link; body `#` headings demoted to `<h2>`. Exactly one `<h1>` (the title) site-wide. |
| 5 | No Open Graph / Twitter | ✅ **Fixed** — OG (type/title/description/url/site_name) + Twitter summary card on every page. |
| 6 | robots.txt missing | ✅ **Fixed** — `Allow: /` + `Sitemap:` reference. |
| 7 | about.astro missing canonical + description | ✅ **Fixed**. |
| 8 | Title length unmanaged (`{title} - AI-Pulse`) | ✅ **Fixed** — brand suffix only when it keeps the title short; long buyer-intent titles stand alone. |
| 9 | No description field in schema | ✅ **Addressed** — body-excerpt fallback (no schema change needed). |
| — | Sitemap / canonical (most pages) / no-noindex | ✅ Were already good; preserved. |

## Guardrails honored (no fabrication)
- **No `Review` / `AggregateRating` schema** anywhere — the site has no rating
  system, so no star ratings are emitted. Verified: 0 occurrences in built HTML.
- `Article` uses only real frontmatter (title, date, generated_at); author +
  publisher are the real Organization "AI-Pulse" — no invented person.
- `FAQPage` requires an explicit FAQ section **or ≥3** real Q&A pairs → **0** on
  current content (honest; rhetorical question-headings are not marked up).

## Money-page descriptions (the CTR lever)
Templated from real fields parsed out of the title:
- `A vs B [for use_case]` → "Compare {A} vs {B}: pricing, plans, features, pros and cons, and which one wins[ for {use_case}] in 2026. Our hands-on, independent verdict and recommendation."
- review / worth-it / deep-dive → "{X} review (2026): pricing, key features, pros and cons, and whether it's worth it — our hands-on verdict and who it's best for."
- alternatives / best-{cat}-for-{uc} → tailored variants.
All clamped to ≤160 chars on a word boundary; news pages fall back to a body excerpt.

## Verification (real built output)
Money page `…/shopify-vs-wix-…/`:
- `<title>` "Shopify vs Wix: best ecommerce platform for beginners in 2026" (60 chars)
- description templated, **160 chars**, unique
- canonical absolute; `og:type=article`; `twitter:card=summary`; GSC tag present
- **2 JSON-LD blocks parse**: Article (real headline/datePublished=2026-06-10/author=AI-Pulse, **hasRating=False**) + BreadcrumbList (Home › Reviews & Comparisons › title)
- Related block → 2 Shopify articles, **0 broken links**

Site-wide: build **exit 0, 284 pages**; sitemap **284 `<loc>`**; robots.txt present
with `Sitemap:`; JSON-LD **0 parse errors** across a 25-page sample (types: Article,
BreadcrumbList); **exactly one `<h1>`** on 40/40 sampled articles + home/about/reviews;
**281** Article-schema pages, **0** FAQPage, **0** rating schema.

## Files touched
- `blog/public/robots.txt` (new)
- `blog/src/components/BaseHead.astro` (new) · `blog/src/lib/seo.ts` (new)
- `blog/src/pages/index.astro`, `about.astro`, `reviews.astro`, `articles/[...slug].astro`
- `docs/seo_audit_phase0.md`, `docs/seo_foundation_report.md`

## Commits (per phase)
- Phase 0 — audit (committed earlier)
- Phase 1 — robots.txt + canonical/description on about
- Phase 2 — BaseHead + query-aligned descriptions + OG/Twitter + single h1
- Phase 3 — Article + BreadcrumbList JSON-LD + related-article links (FAQ genuine-only)
- Phase 4 — body-h1 demotion + this report

## 3-Axis self-score (CLAUDE.md §0.1.2)
> Pass: A + B + C ≥ 70 AND B ≥ 25.

| Axis | Cap | Score | Basis |
|---|---|---|---|
| **A — process** | 30 | **28** | Per-phase commits; build verified every phase; real-output verification (parsed JSON-LD, counted h1s, spot-checked head); honest tightening of the FAQ guardrail; audit + report docs. |
| **B — implementation** | 40 | **37** | DRY BaseHead; descriptions from real fields; schema real-data + `<`-escaped; **no rating schema** (policy-safe); related = shared-product (no link spam); one h1 site-wide; idempotent; build passes; no broken links. −3: news descriptions are raw body excerpts (functional, not editorial); no per-article OG image asset. |
| **C — data quality** | 30 | **25** | Unique, query-aligned money descriptions; valid structured data; relevant internal links. −5: ranking/traffic impact is not yet measurable (compounds over weeks); OG image + a `description` frontmatter field for hand-tuned news summaries remain future polish. |
| **Total** | 100 | **90** | **PASS** (≥70, B≥25). |

### "Metric improved" vs "done well" (honest)
- **Done well:** every Phase-0 gap closed; verified against real built HTML; zero
  fabrication (no ratings, FAQ only when genuine, schema from real fields).
- **Not claimable yet:** ranking and organic traffic — this is foundation only;
  gains compound over weeks once crawled/indexed.

## Out of scope (noted, not implemented)
Per-article Open Graph images (need a 1200×630 asset/generator); backlinks /
off-site; keyword-research tooling; custom-domain migration; Google Search Console
submission (Hiro — the GSC verification tag is already live on `main`).
