# SEO Foundation — Phase 0 Audit (NO changes)

Date: 2026-06-11 · Branch: `seo-foundation` (off main `65fbb71`)
Evidence verified against source + the real built `dist/` output.

## Per-area state

| Area | State | Evidence |
|---|---|---|
| **Sitemap** | ✅ GOOD | `@astrojs/sitemap` integrated (`blog/astro.config.mjs:10`), `site` set (`:9`). Built `dist/sitemap-0.xml` has **284 `<loc>` entries** = home + about + reviews + all 281 article routes, absolute URLs. |
| **robots.txt** | ❌ MISSING | `blog/public/` contains only favicons; no `robots.txt` in source or `dist/`. No `Sitemap:` reference, no explicit allow. |
| **Canonical** | ⚠️ MOSTLY | Correct absolute canonical on article (`[...slug].astro:37,47`), index (`index.astro:15,25`), reviews (`reviews.astro:10,20`). **Missing on `about.astro`.** |
| **`<title>`** | ⚠️ WEAK | Present on all pages. Article: `{data.title} - AI-Pulse` (`[...slug].astro:45`) — raw title + suffix, no length management (long money-page titles + " - AI-Pulse" can exceed ~60 chars). |
| **Meta description** | ❌ BROKEN | Article description = **the title duplicated**: `<meta name="description" content={data.title}>` (`[...slug].astro:46`). No real summary on any of the 281 article pages. `about.astro` has **no** description. |
| **Structured data** | ❌ MISSING | No JSON-LD anywhere — no `Article`, `BreadcrumbList`, or `FAQPage`. (`grep ld+json` → none.) |
| **Open Graph / Twitter** | ❌ MISSING | No `og:*` or `twitter:*` tags on any page. |
| **Headings** | ⚠️ TWO H1 | Every article page renders **two `<h1>`**: site name `<h1>AI-Pulse</h1>` (`[...slug].astro:164`) + article `<h1>{data.title}</h1>` (`:172`). Same on index/about. Should be one h1 = the page's primary topic. |
| **Internal linking** | ⚠️ PARTIAL | Hubs link out: `index.astro` + `reviews.astro` link to `/articles/{article.id}`. But **article pages link to NOTHING** — no "related comparisons/reviews" block; money pages don't pass equity to each other and are weakly discoverable. |
| **noindex / blocked** | ✅ NONE | No `noindex` in source; no blocked routes; `<html lang="en">`, viewport, charset all present. |

## Gap list — ranked by SEO impact

1. **Meta descriptions are the title duplicated on all 281 articles** (`[...slug].astro:46`). Highest-impact on-page miss: kills SERP relevance + click-through for the money pages. → Phase 2 (derive a real ~150-160-char description from the article body; allow a frontmatter override).
2. **No structured data** (Article + BreadcrumbList) → ineligible for rich results / weaker entity understanding. → Phase 3 (JSON-LD from REAL title/date/description; FAQPage only where genuine Q&A).
3. **No internal linking between articles** → money pages are near-orphans; no topical link equity flow. → Phase 3 ("Related comparisons/reviews" block, 3-5 relevant links).
4. **Two `<h1>` per page** → dilutes the primary heading signal. → Phase 2 (demote site-name to a non-h1 brand/logo; keep article title as the sole h1).
5. **No Open Graph / Twitter cards** → poor social/preview CTR (indirect). → Phase 2.
6. **robots.txt missing** → no explicit crawl allow, no `Sitemap:` pointer for discovery. → Phase 1.
7. **`about.astro` missing canonical + description** → Phase 1/2.
8. **Title length unmanaged** (`{title} - AI-Pulse` can exceed ~60 chars) → Phase 2 (suffix only when it fits; rely on already buyer-intent money titles e.g. "Shopify vs Wix … in 2026").
9. **No `description` field in content schema** (`content.config.ts`) → can't author per-article descriptions; needs a body-excerpt fallback. → Phase 2.

## Already solid (no action)
Sitemap completeness + absolute URLs; canonical on article/index/reviews; `site` configured; no noindex/blocked routes; lang/viewport/charset; hub→article internal links.

## Out of scope (noted, not implemented)
Backlinks/off-site/paid; keyword-research tooling; custom-domain migration; Google Search Console submission.

---
**Phase 0 gate: audit + ranked gap list delivered. STOPPING for Hiro review before any change.**
