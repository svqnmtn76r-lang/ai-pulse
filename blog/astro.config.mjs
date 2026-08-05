// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import fs from 'node:fs';
import path from 'node:path';

// Build the set of thin-stub article URLs so the sitemap can exclude exactly the
// pages the article layout marks <meta robots="noindex">. Shipping a noindex URL
// inside the sitemap sends Google contradictory signals and wastes crawl budget.
// NOTE: astro:content is not available inside astro.config, so frontmatter is read
// directly here. The rule must stay in sync with isStubPage() in src/lib/seo.ts.
const STUB_CATEGORIES = new Set(['sdk_release', 'feature_update']);
const COMMERCIAL_CATEGORIES = new Set(['comparison', 'tool_launch', 'deep_dive']);
const ARTICLES_DIR = new URL('./src/content/articles/', import.meta.url).pathname;

function frontmatterOf(raw) {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return { category: '', title: '', hasProducts: false };
  const fm = m[1];
  const category = (fm.match(/^category:\s*(.+)$/m)?.[1] || '').trim().replace(/^['"]|['"]$/g, '').toLowerCase();
  const title = (fm.match(/^title:\s*(.+)$/m)?.[1] || '').trim().replace(/^['"]|['"]$/g, '');
  // `products:` is a YAML list; a non-empty list has at least one "- item" line after it.
  const productsBlock = fm.match(/^products:\s*\n((?:\s*-\s*.+\n?)*)/m)?.[1] || '';
  const hasProducts = /-\s*\S/.test(productsBlock);
  return { category, title, hasProducts };
}

const stubUrls = new Set();
try {
  for (const file of fs.readdirSync(ARTICLES_DIR)) {
    if (!file.endsWith('.md')) continue;
    const { category, title, hasProducts } = frontmatterOf(
      fs.readFileSync(path.join(ARTICLES_DIR, file), 'utf8')
    );
    const isMoney = hasProducts && COMMERCIAL_CATEGORIES.has(category);
    const isStub = !isMoney && (STUB_CATEGORIES.has(category) || /\S+@\d[\d.]/.test(title));
    if (isStub) {
      stubUrls.add(`https://aitickerhq.com/articles/${file.replace(/\.md$/, '')}/`);
    }
  }
} catch (err) {
  console.warn('[sitemap] could not scan articles for stub exclusion:', err?.message);
}
console.log(`[sitemap] excluding ${stubUrls.size} noindex stub page(s) from sitemap`);

// https://astro.build/config
export default defineConfig({
  // Deployed on Cloudflare Pages. `site` makes canonical + sitemap emit
  // absolute URLs (required for SEO / search-engine indexing).
  site: 'https://aitickerhq.com',
  // Canonical URLs use a trailing slash (directory build format). Make the
  // intent explicit so dev/preview and internal links stay consistent with the
  // emitted <link rel="canonical"> and sitemap URLs.
  trailingSlash: 'always',
  integrations: [
    sitemap({
      filter: (page) => !stubUrls.has(page),
    }),
  ],
});
