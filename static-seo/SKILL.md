---
name: static-seo
description: >
  Audits and improves SEO for static HTML sites. Use when the user asks to
  audit, set up, or improve SEO on a static site (Hugo, Jekyll, 11ty,
  Gatsby, Next.js static export, hand-rolled HTML, or `wp-static-clone`
  output), or mentions head metadata, structured data, JSON-LD, sitemaps,
  IndexNow, Open Graph images, schema endpoints, NLWeb, hreflang, or
  search engine indexing for a static site. For Astro projects, use
  `astro-seo` instead — its recipes produce less hand-rolled boilerplate
  by routing through `@jdevalk/astro-seo-graph`.
---

# Static SEO

Audits and improves the SEO setup of a static HTML site against nine categories — head metadata, structured data, content quality, Open Graph images, sitemaps and indexing, agent discovery, performance, redirects, and CI validation. Recipes are platform-neutral: raw `<meta>` tags, raw JSON-LD, hand-rolled `sitemap.xml`, generic CI tooling. Audit framework parallels [`astro-seo`](../astro-seo/) but without the `@jdevalk/astro-seo-graph` spine.

**Code recipes live in `AGENTS.md`** — read it when you need to implement a specific fix. This file has the workflow and audit checklist.

## Workflow

1. **Detect the project** — confirm this is a static site, identify the build tool, find where to apply changes.
2. **Audit** — score nine categories and produce actionable findings.
3. **Improve** — generate or modify files to close the gaps. Recipes are in `AGENTS.md`.
4. **Metadata pass** — invoke `metadata-check` on every short string the skill generated (titles, descriptions, schema `description` fields, FAQ answers).
5. **Verify** — run any build, validate the output, remind the user about non-file tasks (Search Console, Bing Webmaster Tools, IndexNow key submission).

---

## Phase 0: Detect the project

Confirm the basics before auditing:

- **It is actually a static site.** Look for built HTML — `index.html` at the repo root, or under `_site/` (Jekyll), `public/` (Hugo / 11ty / Gatsby), `dist/` (Vite / Astro static), `out/` (Next.js with `output: export`). If everything is server-rendered (Express, PHP, dynamic routes), this is the wrong skill — point at `astro-seo` for Astro, `wp-readme-optimizer` for WP plugin pages, or recommend a generic SEO audit instead.
- **Source build tool.** Drives where to apply head metadata changes:
  - `_config.yml` / `_layouts/` → Jekyll
  - `config.toml` / `config.yaml` / `themes/` → Hugo
  - `.eleventy.js` / `_includes/` → 11ty
  - `gatsby-config.js` / `src/components/SEO.*` → Gatsby
  - `next.config.js` with `output: 'export'` and `pages/_document.tsx` → Next.js static export
  - `astro.config.mjs` → Astro (in which case **use `astro-seo` instead**)
  - No build config, just HTML files → hand-rolled or scraped (e.g. `wp-static-clone` output). Edit the HTML directly or use a post-process script.
- **Canonical site URL.** Search the repo for the production origin — typically in `_config.yml`, `config.toml`, `astro.config`, or hardcoded into a layout. **If it's missing, empty, or `localhost`, flag as a blocking issue before anything else.** Canonicals, sitemaps, OG image URLs, and JSON-LD `@id` values all derive from this.
- **Deployment target.** Read `vercel.json`, `netlify.toml`, `wrangler.toml`, or `public/_headers` to determine the host. Drives redirect and header syntax in Phase 2.
- **Is the site multilingual?** Check for locale subdirectories (`/en/`, `/nl/`, `/de/`) or build-tool i18n config. If yes, hreflang matters; if no, skip it.
- **What's already in `<head>`?** Open one built HTML file and inventory: title, description, canonical, robots, Open Graph, Twitter cards, JSON-LD, hreflang. The audit in Phase 1 is faster if you can reference what's there.

Ask only what you can't detect.

---

## Phase 1: Audit

Score each category out of 10. For each, give 2–4 specific findings that quote the actual HTML, config, or template. Within each category, checks are tiered:

- **Must** — ship blockers. A failure causes visible SEO regression.
- **Should** — standard practice. Skipping costs reach.
- **Nice** — forward-looking or situational. Useful but not baseline for every site.

Skip **Nice** checks for small personal sites unless the user asks for the full treatment.

### 1. Head metadata (/10)

- **Must** — every page has a `<title>` and `<meta name="description">`.
- **Must** — `<link rel="canonical">` set, with tracking parameters stripped, derived from the production origin.
- **Must** — canonical omitted when the page is `noindex` (per Google's recommendation).
- **Must** — `<title>` length 30–65 characters, `<meta name="description">` length 70–200 characters (the SERP-truncation bounds; same as `metadata-check` defaults).
- **Should** — `<meta name="robots">` includes `max-snippet:-1`, `max-image-preview:large`, `max-video-preview:-1`.
- **Should** — Open Graph (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`, `og:site_name`) on every page.
- **Should** — Twitter Card tags (`twitter:card`) suppressed when they duplicate Open Graph (Twitter falls back automatically).
- **Should** — `hreflang` alternates on multilingual sites. Skip if monolingual.
- **Should** — single `<meta name="robots">` and single `og:image` per page (legacy tooling sometimes emits duplicates).

### 2. Structured data / JSON-LD (/10)

- **Must** — at least one `<script type="application/ld+json">` block on every important page.
- **Should** — linked `@graph` rather than a flat `Article` object — entities wired with `@id` references so a `BlogPosting` can point at its `Person` author and `WebPage` parent.
- **Should** — `WebSite`, `Blog` / `WebPage`, `Person` / `Organization`, `BlogPosting` / `Article`, `BreadcrumbList`, `ImageObject` all present where relevant.
- **Should** — trust signals: `publishingPrinciples`, `copyrightHolder`, `copyrightYear`, `knowsAbout`, `SearchAction`.
- **Must** — validates in [Rich Results Test](https://search.google.com/test/rich-results) and [ClassySchema](https://classyschema.org/Visualisation).

### 3. Content quality (/10)

- **Must** — every page has a unique `<title>` and `<meta name="description">` (no duplicate metadata across the site).
- **Must** — exactly one `<h1>` per page.
- **Should** — `<title>` and `<meta name="description">` audited via `metadata-check` (Phase 2.5) for front-loading, concreteness, and SERP fit.
- **Should** — body prose audited via `readability-check` for individual long-form posts (don't bulk-audit).
- **Should** — every `<img>` has an `alt` attribute (or `alt=""` / `role="presentation"` for decorative).
- **Should** — internal links use root-relative paths (`/foo/`) not absolute (`https://...`) — survives domain changes and previews.

### 4. Open Graph images (/10)

- **Must** — every page has an OG image.
- **Must** — 1200×675 (Google Discover minimum 1200px wide, 16:9 ratio).
- **Should** — JPEG (social platforms don't reliably support WebP / AVIF for OG).
- **Should** — generated at build time (satori-cli, sharp, ImageMagick, Vercel OG, Bannerbear) rather than uploaded manually per page — prevents drift.
- **Should** — URL derived deterministically from the slug (e.g. `/og/<slug>.jpg`) so adding a page automatically gets an image.
- **Should** — every `<img>` in body content has an `alt` attribute (or `alt=""` / `role="presentation"`). Validated in CI via `html-proofer` or similar.

### 5. Sitemaps and indexing (/10)

- **Must** — `/sitemap.xml` (or `/sitemap_index.xml` for split sitemaps) reachable, valid XML, every URL returns 200.
- **Must** — `robots.txt` present at the site root and references the sitemap.
- **Must** — RSS feed exists, advertised via `<link rel="alternate" type="application/rss+xml">`, contains full post content (not truncated excerpts).
- **Should** — split per-section if the site has multiple content types (`sitemap-posts.xml`, `sitemap-pages.xml`) — easier to debug indexing in GSC.
- **Should** — `<lastmod>` populated from git commit timestamps (most accurate), build timestamps (acceptable), or frontmatter dates (last resort). Filesystem `mtime` from CI checkout is wrong — it's the checkout date, not the content date.
- **Should** — IndexNow integrated. Verification key as a static `/<key>.txt` route at the site root, plus a build-or-deploy hook that POSTs new URLs to `https://api.indexnow.org/IndexNow`. **Gate the submission on the production host** (e.g. `CF_PAGES_BRANCH=main`, `VERCEL_ENV=production`, `CONTEXT=production`) — unconditional submission pings the endpoint from local builds with URLs the production host hasn't served yet, which gets the key marked invalid (403) and forces rotation.

### 6. Agent discovery (/10)

- **Should** — schema endpoints (`/schema/<type>.json`) exposing corpus-wide JSON-LD per content type. Static JSON files committed to the repo or regenerated by the build.
- **Should** — schema map (`/schemamap.xml`) listing every schema endpoint, with `Schemamap:` directive in `robots.txt`.
- **Should** — [`llms.txt`](https://llmstxt.org) at the site root listing pages (title + description) for LLM consumers. Static text file; one line per page.
- **Should** — markdown-alternate URLs (`/blog/post.md` next to `/blog/post/`) serving clean markdown with YAML frontmatter so AI agents can consume content without HTML parsing. Either commit `.md` siblings, or use a Cloudflare Transform Rule + `Vary: Accept` for content negotiation (CF Pages strips custom Vary headers, so use the Transform Rule's URL rewrite alone — recipe in `AGENTS.md`).
- **Should** — API catalog at `/.well-known/api-catalog` per [RFC 9727](https://www.rfc-editor.org/rfc/rfc9727), as `application/linkset+json` ([RFC 9264](https://www.rfc-editor.org/rfc/rfc9264)). Lists schema endpoints, schemamap, RSS feed, and any site-specific APIs. Static JSON file.
- **Should** — Content Signals directive in `robots.txt` (`Content-Signal: ai-train=yes, search=yes, ai-input=yes` or your preferred policy). One line, IETF draft, low cost.
- **Should** — `Link` header on `/*` pointing to discovery files (sitemap, llms.txt, api-catalog, schemamap). Agents reading response headers find them without parsing HTML. Host-specific (`_headers` on Cloudflare Pages / Netlify, `vercel.json` on Vercel, server config elsewhere).
- **Nice** — MCP server card at `/.well-known/mcp/server-card.json` and / or A2A agent card at `/.well-known/agent-card.json`. Only relevant when the site exposes an MCP server or A2A agent.
- **Nice** — `<link rel="nlweb">` pointing to a conversational endpoint. NLWeb adoption is early; the tag is one line and worth having, but not a scoring blocker in 2026.

### 7. Performance (/10)

- **Must** — hashed assets serve `Cache-Control: public, max-age=31536000, immutable` (or equivalent) so they only download once.
- **Should** — primary web font preloaded as `woff2` via `<link rel="preload" as="font" crossorigin>`.
- **Should** — `No-Vary-Search` response header strips UTM parameters from cache key (so `/?utm_source=x` and `/` share a cache entry).
- **Should** — no render-blocking JavaScript on first paint (defer or async non-critical scripts).
- **Should** — images use modern formats (WebP / AVIF for in-page content; JPEG only for OG cards) and `loading="lazy"` below the fold.
- **Should** — all Lighthouse / PageSpeed Core Web Vitals in the green: LCP < 2.5s, INP < 200ms, CLS < 0.1.

### 8. Redirects and error handling (/10)

- **Must** — `_redirects` / `vercel.json` / server config maintained for every URL that ever existed and moved.
- **Must** — `301` not `302` for permanent moves.
- **Must** — `404.html` (or equivalent) returns a 404 status, not 200. Verify with `curl -I` against a deliberately wrong URL.
- **Should** — fuzzy-match suggestion on the 404 page ("did you mean…?") for typos in URLs. Static implementation: pre-build a JSON index of valid slugs, fuzzy-match client-side.

### 9. CI validation (/10)

- **Must** — broken-link checker in CI. [linkinator](https://github.com/JustinBeckwith/linkinator) or [lychee](https://github.com/lycheeverse/lychee-action) on every push that touches content. Internal and external links both — internal catches build regressions, external catches link rot. Schedule a weekly run for external-only checks.
- **Should** — HTML validation via [html-proofer](https://github.com/gjtorikian/html-proofer) or [W3C Validator](https://validator.w3.org/) — catches malformed markup that breaks crawlers.
- **Should** — [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) on every push, with score thresholds (e.g. SEO ≥ 95, Performance ≥ 80).
- **Should** — JSON-LD validation in CI via the [Schema.org JSON-LD validator](https://validator.schema.org/) (no official CLI; pipe through a Node script that POSTs to the API).
- **Should** — title and description length validation in CI: a small script that walks built HTML, extracts `<title>` and `<meta name="description">`, flags anything outside SERP-truncation bounds (title 30–65, description 70–200).

---

## Phase 2: Improve

Based on the audit, produce concrete code. Always ask before overwriting. **Read `AGENTS.md` for detailed recipes.**

**Branch on the Phase 0 findings.** If the site is a known build tool (Hugo, Jekyll, 11ty, Gatsby, Next.js), apply changes at the source level (templates, config, frontmatter). For hand-rolled or scraped HTML, post-process the built output. The recipes in `AGENTS.md` are output-shape recipes — show the HTML you want to land at — and a per-tool note on where to plumb them through.

`AGENTS.md` sections: Head metadata (the canonical block), JSON-LD graph, OG image generation (build-script options), `sitemap.xml` and `robots.txt`, IndexNow, llms.txt, Markdown alternates, API catalog, Content Signals, Link headers, Performance headers, Redirects by host, CI workflows.

---

## Phase 2.5: Metadata and readability pass

Invoke the `metadata-check` skill on every short string the skill generated or modified: page titles, meta descriptions, schema `description` fields, FAQ answers, and any frontmatter `excerpt` values you wrote. It checks front-loading, concreteness, filler, active voice, title / description duplication, difficult words, SERP-truncation fit (title 30–65, description 70–200), and one-idea-per-field. Apply fixes directly. Skip the pass for technical strings (URLs, schema `@id` values, enum values).

If the project has a blog or docs section, mention as a follow-up that the `readability-check` skill can audit individual posts for multi-paragraph prose quality — but don't audit the entire content corpus yourself.

---

## Phase 3: Verify

- Build the site (or rebuild if mid-iteration). Surface any build warnings.
- Spot-check the built HTML: one page's `<head>` should be clean, canonical correct, JSON-LD graph present and linked.
- Run the homepage through [Rich Results Test](https://search.google.com/test/rich-results) and [ClassySchema](https://classyschema.org/Visualisation).
- Confirm `/sitemap.xml` exists, returns 200, and references the right URLs.
- Confirm `/robots.txt` references the sitemap and includes Content Signals.
- If IndexNow is wired, confirm the key verification route returns the key at `/<key>.txt`.
- Run the local broken-link check (`linkinator http://localhost:8080 --recurse`).
- Remind the user about tasks that can't be automated:
  - Register the site in [Google Search Console](https://search.google.com/search-console) and [Bing Webmaster Tools](https://www.bing.com/webmasters).
  - Submit the sitemap in both.
  - Generate an IndexNow key and commit the `.txt` verification file.
  - Install [Plausible](https://plausible.io/) or equivalent privacy-friendly analytics.

---

## Output format

```markdown
## Static SEO audit: [site name]

### Score
| Category                              | Score |
| ------------------------------------- | ----: |
| 1. Head metadata                      |  x/10 |
| 2. Structured data / JSON-LD          |  x/10 |
| 3. Content quality                    |  x/10 |
| 4. Open Graph images                  |  x/10 |
| 5. Sitemaps and indexing              |  x/10 |
| 6. Agent discovery                    |  x/10 |
| 7. Performance                        |  x/10 |
| 8. Redirects and error handling       |  x/10 |
| 9. CI validation                      |  x/10 |
| **Total**                             | xx/90 |

### Findings
[Grouped by category. Quote actual HTML / config. Be specific.]

### Files generated or changed
[List with short description of each.]

### Next steps
[Non-file tasks: GSC, Bing Webmaster Tools, IndexNow key, analytics.]
```

---

## Key principles

- **Audit the output, fix at the source.** The skill checks the built HTML, but recommends changes at whatever layer produces it (Hugo template, Jekyll layout, 11ty include, post-process script). Don't recommend a fix that won't survive the next build.
- **Static = host-portable.** Every recipe should work on any static host. Where syntax differs (`_redirects` vs `vercel.json`), give both forms.
- **Topics, not keyphrases.** When reviewing content, focus on topical coverage and readability, not keyword density.
- **Agent discovery matters now.** Schema endpoints, schema map, llms.txt, API catalog, markdown alternates, MCP / A2A cards — the crawler is no longer the only consumer.
- **Defer to `astro-seo` for Astro.** That skill produces less hand-rolled boilerplate via `@jdevalk/astro-seo-graph`. `static-seo` is for everything else.
