// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // Deployed on Cloudflare Pages. `site` makes canonical + sitemap emit
  // absolute URLs (required for SEO / search-engine indexing).
  site: 'https://ai-pulse-b35.pages.dev',
  integrations: [sitemap()],
});
