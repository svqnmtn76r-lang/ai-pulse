// SEO helpers: query-aligned meta descriptions + title management.
// Money pages (comparison/review = frontmatter `products` non-empty) get a
// templated, query-aligned description built from REAL fields parsed out of the
// title (the two compared products, the use_case). News pages fall back to a
// cleaned body excerpt. Everything is derived from real data — no fabrication.

export interface ArticleData {
  title?: string;
  products?: string[];
  category?: string;
  template_type?: string;
  date?: string;
}

export function isMoneyPage(data: ArticleData): boolean {
  return Array.isArray(data.products) && data.products.length > 0;
}

/** Date-stripped slug, so date-variants of the same article collapse to one key. */
export function baseSlug(slug: string): string {
  return slug.replace(/^\d{4}-\d{2}-\d{2}-/, '');
}

/** Collapse whitespace and clamp to `max` chars on a word boundary. */
export function clamp(input: string, max = 160): string {
  const s = (input || '').replace(/\s+/g, ' ').trim();
  if (s.length <= max) return s;
  const cut = s.slice(0, max - 1);
  const sp = cut.lastIndexOf(' ');
  return (sp > 80 ? cut.slice(0, sp) : cut).trim() + '…';
}

/** Templated, query-aligned description for a money page, or null if the title
 *  doesn't match a known buyer-intent shape. */
export function moneyDescription(rawTitle: string): string | null {
  const t = (rawTitle || '').trim();

  // "A vs B: <tail>"  (optionally with a "for <use_case>")
  let m = t.match(/^(.+?)\s+vs\.?\s+(.+?)\s*[:\-–]\s*(.*)$/i);
  if (m) {
    const A = m[1].trim();
    const B = m[2].trim();
    const tail = m[3].trim();
    const f = tail.match(/\bfor\s+(.+?)(?:\s+in\s+20\d{2}.*)?$/i);
    const uc = f ? f[1].replace(/\s+in\s+20\d{2}.*/i, '').trim() : '';
    const ucPart = uc ? ` for ${uc}` : '';
    return clamp(`Compare ${A} vs ${B}: pricing, plans, features, pros and cons, and which one wins${ucPart} in 2026. Our hands-on, independent verdict and recommendation.`);
  }

  // "A vs B"  (no colon)
  m = t.match(/^(.+?)\s+vs\.?\s+(.+)$/i);
  if (m && !/[:\-–]/.test(t)) {
    const A = m[1].trim();
    const B = m[2].replace(/\s+in\s+20\d{2}.*/i, '').trim();
    return clamp(`Compare ${A} vs ${B}: pricing, plans, features, pros and cons, and which one wins in 2026. Our hands-on, independent verdict and recommendation.`);
  }

  // "X review" / "Is X worth it" / "X deep dive"
  const kw = t.match(/\b(review|worth it|deep dive)\b/i);
  if (kw && kw.index !== undefined) {
    let A = t.slice(0, kw.index).split(/[:\-–]/)[0].replace(/\s+in\s+20\d{2}.*/i, '').replace(/^is\s+/i, '').trim();
    if (A) {
      return clamp(`${A} review (2026): pricing, key features, pros and cons, and whether it's worth it — our hands-on verdict and who it's best for.`);
    }
  }

  // "X alternatives"
  m = t.match(/^(.+?)\s+alternatives\b/i);
  if (m) {
    const A = m[1].trim();
    return clamp(`The best ${A} alternatives in 2026, compared on pricing, features and value — with our top picks and an honest recommendation.`);
  }

  // "Best <category> for <use_case>"
  m = t.match(/^best\s+(.+?)\s+for\s+(.+?)(?:\s+in\s+20\d{2})?$/i);
  if (m) {
    const cat = m[1].trim();
    const uc = m[2].trim();
    return clamp(`The best ${cat} for ${uc} in 2026, compared on pricing, features and value. Our top pick and an honest, hands-on recommendation.`);
  }

  return null;
}

/** Clean a markdown body down to a plain-text excerpt (news fallback). */
export function excerpt(markdown: string, max = 158): string {
  const s = (markdown || '')
    .replace(/<div class="affiliate-cta"[\s\S]*?<\/div>/gi, ' ')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/^\s{0,3}#{1,6}\s+/gm, ' ')
    .replace(/[*_`~>|]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  return clamp(s, max);
}

/** Final description for an article: money template, else news excerpt, else title. */
export function articleDescription(data: ArticleData, markdown: string): string {
  if (isMoneyPage(data)) {
    const d = moneyDescription(String(data.title || ''));
    if (d) return d;
  }
  return excerpt(markdown) || clamp(String(data.title || ''), 160);
}

/** Extract GENUINE Q&A pairs from the body: markdown headings that are questions
 *  (end with "?") followed by real answer text. Used to emit FAQPage schema ONLY
 *  when the article actually contains visible Q&A (Google policy). Returns [] when
 *  there is no real Q&A — callers should require >= 2 pairs before emitting. */
export function extractFaq(markdown: string): { q: string; a: string }[] {
  const md = markdown || '';
  const lines = md.split('\n');
  const out: { q: string; a: string }[] = [];
  for (let i = 0; i < lines.length; i++) {
    const h = lines[i].match(/^#{2,4}\s+(.*\?)\s*$/);
    if (!h) continue;
    const q = h[1].replace(/[*_`]+/g, '').trim();
    const ans: string[] = [];
    for (let j = i + 1; j < lines.length; j++) {
      if (/^#{1,6}\s+/.test(lines[j])) break;
      ans.push(lines[j]);
    }
    const a = ans.join(' ')
      .replace(/<div class="affiliate-cta"[\s\S]*?<\/div>/gi, ' ')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
      .replace(/[*_`~>|#]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    if (a.length >= 40) out.push({ q, a: clamp(a, 320) });
  }
  // Only treat as a GENUINE FAQ when the article has an explicit FAQ section, or
  // a real Q&A list (>= 3 Q&A pairs). One or two rhetorical question-headings in a
  // comparison are NOT an FAQ — don't mark those up.
  const hasFaqHeading = /^#{1,6}\s+.*\b(faq|frequently asked questions)\b/im.test(md);
  if (!hasFaqHeading && out.length < 3) return [];
  return out;
}

/** Page <title>: append the brand only when it keeps the title reasonably short
 *  (the buyer-intent article titles are already long + descriptive). */
export function pageTitle(rawTitle: string): string {
  const t = String(rawTitle || '').trim();
  return t.length <= 50 ? `${t} | AI Ticker HQ` : t;
}
