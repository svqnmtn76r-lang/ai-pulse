// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // Deployed on Cloudflare Pages. `site` makes canonical + sitemap emit
  // absolute URLs (required for SEO / search-engine indexing).
  site: 'https://aitickerhq.com',
  // Canonical URLs use a trailing slash (directory build format). Make the
  // intent explicit so dev/preview and internal links stay consistent with the
  // emitted <link rel="canonical"> and sitemap URLs.
  trailingSlash: 'always',
  integrations: [sitemap()],
});
