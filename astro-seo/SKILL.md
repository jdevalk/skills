---
name: astro-seo
description: >
  Audits and improves SEO for Astro sites. Use when the user asks to audit,
  set up, or improve SEO on an Astro site, or mentions head metadata,
  structured data, JSON-LD, sitemaps, IndexNow, Open Graph images, schema
  endpoints, NLWeb, hreflang, or search engine indexing in an Astro project.
  Produces drop-in code routed through `@jdevalk/astro-seo-graph` and chains
  into `metadata-check` for generated SEO strings.
---

# Astro SEO

Audits and improves the SEO setup of an Astro site against the full stack described in [Astro SEO: the definitive guide](https://joost.blog/astro-seo-complete-guide/). The skill covers nine areas — technical foundation, structured data, content, site structure, performance, sitemaps and indexing, agent discovery, redirects, and analytics — and produces drop-in code for anything missing or weak.

The opinionated spine of this skill is [`@jdevalk/astro-seo-graph`](https://github.com/jdevalk/seo-graph). Most of the fixes route through it. If the project doesn't use it yet, installing it is the first recommendation.

**Code recipes live in `AGENTS.md`** — read it when you need to implement a specific fix. This file has the workflow and audit checklist.

## Workflow

1. **Detect the project** — confirm this is an Astro site and understand its shape.
2. **Audit** — score nine categories and produce actionable findings.
3. **Improve** — generate or modify files to close the gaps. Recipes are in `AGENTS.md`.
4. **Metadata pass** — invoke `metadata-check` on every short string the skill generated (titles, descriptions, schema `description` fields, FAQ answers, frontmatter excerpts).
5. **Verify** — run the build, check validations pass, remind the user about non-file tasks (Search Console, Bing Webmaster Tools, IndexNow key verification).

---

## Phase 0: Detect the project

Confirm the basics before auditing:

- `astro.config.mjs` / `astro.config.ts` exists.
- `package.json` has `astro` as a dependency.
- **`site:` is set in `astro.config`** — canonicals, sitemaps, and OG image URLs all derive from this. If it's missing, empty, or `http://localhost`, flag it as a blocking issue before anything else. This is the single most common misconfiguration.
- Content collections in `src/content/` (or legacy `src/pages/` markdown).
- **Deployment target** — read `package.json`, `vercel.json`, `netlify.toml`, `wrangler.toml`, or `public/_headers` to determine the host. This drives redirect and header syntax in Phase 2.
- **Is `@jdevalk/astro-seo-graph` already installed?** If yes, record the version and which features are wired (grep for `<Seo`, `seoGraph(`, `createSchemaEndpoint`, `createSchemaMap`, `FuzzyRedirect`, `createIndexNowKeyRoute`, `createMarkdownEndpoint`, `createApiCatalog`, `gitLastmod`). **Check the installed version against the latest on npm** with `npm view @jdevalk/astro-seo-graph version`. If the project is behind, recommend an upgrade in Phase 2 before auditing feature gaps — the package ships new defaults and fixes regularly, and an outdated version is a plausible cause for any audit finding. Phase 2 branches on this.
- **Is the site multilingual?** Check for `i18n` in `astro.config` or multiple locale directories under `src/content/`. If yes, hreflang matters; if no, skip it.

Ask only what you can't detect. Don't ask the user what the site is about — read `astro.config.mjs` and the homepage content.

---

## Phase 1: Audit

Score each category out of 10. For each, give 2–4 specific findings that quote the actual code or config. Within each category, checks are tiered:

- **Must** — ship blockers. A failure here causes visible SEO regression.
- **Should** — standard practice. Skipping costs reach.
- **Nice** — forward-looking or situational. Useful but not baseline for every site.

Skip **Nice** checks for small personal blogs unless the user asks for the full treatment.

### 1. `<Seo>` component and head metadata (/10)

- **Must** — single component for all head metadata (not scattered across layouts).
- **Must** — `site:` in `astro.config` is set to the production origin.
- **Must** — canonical URLs derived from `site` config with tracking params stripped.
- **Must** — canonical omitted when `noindex` is true (per Google's recommendation).
- **Must** — fallback chain for missing SEO fields: `seo.title → title → siteName`; `seo.description → excerpt → first paragraph`. Pages with blank titles or descriptions are the most common symptom of a broken fallback.
- **Should** — `robots` meta includes `max-snippet:-1`, `max-image-preview:large`, `max-video-preview:-1`.
- **Should** — Twitter tags suppressed when they duplicate Open Graph (Twitter falls back automatically).
- **Should** — `hreflang` alternates present on multilingual sites. Skip if monolingual.
- **Nice** — uses `@jdevalk/astro-seo-graph`'s `<Seo>` component rather than hand-rolled. (Hand-rolled that covers everything above is fine; this skill nudges toward the package because it handles the fallback chain and robots rules by default.)

### 2. Structured data / JSON-LD graph (/10)

- Single flat `Article` object, or a linked `@graph` with multiple entities?
- Entities wired with `@id` references?
- `WebSite`, `Blog`/`WebPage`, `Person`/`Organization`, `BlogPosting`/`Article`, `BreadcrumbList`, `ImageObject` all present where relevant?
- Trust signals: `publishingPrinciples`, `copyrightHolder`, `copyrightYear`, `knowsAbout`, `SearchAction`?
- Validates in [Rich Results Test](https://search.google.com/test/rich-results) and [ClassySchema](https://classyschema.org/Visualisation)?

### 3. Content collections and SEO schema (/10)

- Content collections defined with Zod schemas?
- `seoSchema` from `@jdevalk/astro-seo-graph` enforcing title (5–120) and description (15–160) lengths?
- Required fields (`publishDate`, `title`, `excerpt`) enforced at build time?
- Markdown-stripped `articleBody` exposed in schema endpoints (up to 10K chars)?

### 4. Open Graph images (/10)

- Every page has an OG image, or many missing?
- 1200×675 (Google Discover minimum 1200px wide, 16:9 ratio)?
- Generated at build time via satori + sharp, or manual?
- JPEG (social platforms don't reliably support WebP/AVIF)?
- Route derives OG URL from the slug automatically?
- Every `<img>` in rendered HTML has an `alt` attribute (or `alt=""` / `role="presentation"` for decorative images)? `validateImageAlt` on `seoGraph()` catches this at build time in ≥ 1.1.0.

### 5. Sitemaps and indexing (/10)

- **Must** — `@astrojs/sitemap` installed, sitemap index reachable.
- **Must** — `robots.txt` references the sitemap index.
- **Must** — RSS feed exists (`@astrojs/rss`), advertised via `<link rel="alternate" type="application/rss+xml">`, contains full post content (not truncated excerpts).
- **Should** — split per-collection via `chunks` option (`sitemap-posts-0.xml`, etc.) — much easier to debug indexing in GSC.
- **Should** — `lastmod` populated from git commit timestamps, not frontmatter dates or CI file timestamps. `@jdevalk/astro-seo-graph` ≥ 1.4.0 exports `gitLastmod(filePath, { excludeCommits, depth })` for this — it returns the committer date of the most recent non-excluded commit that touched the file, or `null` if git is unavailable. Wire it into the sitemap `serialize` callback. If the codebase has a hand-rolled `execSync('git log ...')` helper, replace it with the package export — the export handles bulk-commit exclusion (imports, reformats) which a naïve `-1` lookup can't.
- **Should** — IndexNow integrated and submitting on each build, with key verification route at `/[key].txt`. ≥ 1.0.1 excludes `/404` from submissions by default. **Gate submission on the production host** (e.g. `process.env.CF_PAGES === '1' && CF_PAGES_BRANCH === 'main'`, `VERCEL_ENV === 'production'`, `CONTEXT === 'production'`). Unconditional submission pings the endpoint on every local `npm run build` and preview deploy with URLs the production host hasn't served yet, which gets the key marked invalid (403) and forces rotation.

### 6. Agent discovery (/10)

- **Should** — schema endpoints (`/schema/*.json`) exposing corpus-wide JSON-LD.
- **Should** — schema map (`/schemamap.xml`) listing all endpoints, with `Schemamap:` directive in `robots.txt`.
- **Should** — [`llms.txt`](https://llmstxt.org) at the site root listing pages (title + description) for LLM consumers. `@jdevalk/astro-seo-graph` ≥ 0.9.0 generates this via the `llmsTxt` integration option.
- **Should** — markdown-alternate URLs (`/blog/post.md` next to `/blog/post/`) serving clean markdown with YAML frontmatter for AI agents to consume without HTML parsing. `@jdevalk/astro-seo-graph` ≥ 1.2.0 ships `createMarkdownEndpoint` for the route and a `markdownAlternate: true` integration option that emits `<link rel="alternate" type="text/markdown">` on every page. ≥ 1.3.0 adds post-build verification: the integration walks the build output and strips any link whose `.md` target isn't on disk (with a `warn` per occurrence) — so a misconfigured endpoint surfaces as a build warning instead of a shipped 404. Pair with a Cloudflare Transform Rule (URL rewrite via `wildcard_replace`, no `Vary: Accept` header — CF strips custom Vary values) for content negotiation on `Accept: text/markdown` without needing SSR.
- **Should** — API catalog at `/.well-known/api-catalog` per [RFC 9727](https://www.rfc-editor.org/rfc/rfc9727). `@jdevalk/astro-seo-graph` ≥ 1.4.0 ships `createApiCatalog`, which auto-types schema endpoints to their `https://schema.org/<Type>` URLs and absolutizes paths against `siteUrl`. List the schema endpoints, schemamap, and any site-specific APIs (`/ask`, `/feed.xml`, etc.). The RFC is finalized so the format is stable; adoption is early but the cost is one route file.
- **Should** — Content Signals directive in `robots.txt` (e.g. `Content-Signal: ai-train=yes, search=yes, ai-input=yes`). Declares preferences for AI training, search grounding, and AI input use independently of crawl access. The spec is an [IETF draft](https://datatracker.ietf.org/doc/draft-romm-aipref-contentsignals/) and adoption is early, but it's one line in a file every site already has.
- **Should** — `Link` header on `/*` pointing to discovery files (sitemap, llms.txt, api-catalog, schemamap, and any MCP / A2A cards the site publishes). Agents reading response headers find them without parsing HTML. On Cloudflare Pages / Netlify this is `public/_headers`; on Vercel it's `vercel.json`.
- **Nice** — MCP server card at `/.well-known/mcp/server-card.json` ([SEP-1649](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2127)) and / or A2A agent card at `/.well-known/agent-card.json` ([A2A protocol](https://a2a-protocol.org/)). Only relevant when the site actually exposes an MCP server or A2A agent. Both are static JSON files declaring the endpoint, capabilities, and skills. Skip otherwise.
- **Nice** — `<link rel="nlweb">` pointing to a conversational endpoint. NLWeb is early; the tag is one line and worth having, but it's not a scoring blocker in 2026.

### 7. Performance (/10)

- Static output by default (no SSR on pages that don't need it)?
- Zero client-side JS unless an island requires it?
- Astro `<Image>` component used for all content images (responsive srcset, WebP, lazy, async)?
- Primary web font preloaded in woff2?
- `<ClientRouter />` with `defaultStrategy: 'viewport'` for prefetch?
- Hashed assets under `/_astro/` serve `Cache-Control: public, max-age=31536000, immutable`?
- `No-Vary-Search` response header stripping UTM parameters from cache key?

### 8. Redirects and error handling (/10)

- `public/_redirects` (or equivalent) maintained for every URL that ever existed and moved?
- 301 not 302 for permanent moves?
- `FuzzyRedirect` component from `@jdevalk/astro-seo-graph` wired into the 404 page?
- 404 page itself returns a 404 status, not 200?

### 9. Build-time validation and content quality (/10)

- **Must** — `seoGraph()` integration running on each build with `validateH1` and `validateUniqueMetadata` enabled. For JSON-LD validation, pass `warnOnDanglingReferences: true` to `assembleGraph()` in `seo-graph-core` — that's the assembly-time check, not an integration option.
- **Should** — `validateImageAlt`, `validateMetadataLength`, and `validateInternalLinks` enabled on `seoGraph()` (all default `true` in ≥ 1.1.0). They catch missing alt text, titles or descriptions outside SERP bounds (defaults: title 30–65, description 70–200), and internal links that 404 or hit a trailing-slash mismatch. Upgrade to ≥ 1.1.1 if the project is on 1.1.0 — that patch release fixes two validator bugs: `validateInternalLinks` now recognises `public/` assets as valid targets (no more false positives on `/images/*` or `/fonts/*`), and `validateMetadataLength` no longer truncates descriptions containing a raw apostrophe. Use `skip` only for SSR-only routes, wildcards, and `[slug]` params.
- **Should** — broken link checker in CI for _external_ links. A [lychee](https://github.com/lycheeverse/lychee-action) GitHub Action on every push to content files catches dead links before they go live; a weekly scheduled run catches link rot as external sites move or disappear. Broken outbound links are a bad UX and a negative trust signal. Internal links are covered by `validateInternalLinks` at build time; lychee handles everything else.
- **Should** — SEO strings (titles, descriptions, FAQ answers) audited for metadata quality — front-loading, concreteness, truncation fit, no title/description duplication. Phase 2.5 chains this in via `metadata-check`. Individual post prose can be audited separately via `readability-check`.

---

## Phase 2: Improve

Based on the audit, produce the concrete code. Always ask before overwriting. **Read `AGENTS.md` for detailed recipes.**

**Branch on the Phase 0 findings.** If `@jdevalk/astro-seo-graph` is already installed, skip the install step and focus on wiring the features the audit flagged as missing (IndexNow, FuzzyRedirect, schema endpoints, build validation). If the user has a hand-rolled setup that already satisfies the **Must** checks in category 1, don't rip it out — add only what's missing. Replacement is a last resort, not the default.

`AGENTS.md` sections: Install/upgrade, Integration config, BaseHead.astro, Content collection schema, Sitemap + git lastmod, OG image route, Schema endpoints, llms.txt, Markdown alternates, API catalog, Content Signals in robots.txt, MCP and A2A discovery cards, Link headers for agent discovery, RSS feed, Redirects + FuzzyRedirect, Performance headers, Broken link checker in CI.

---

## Phase 2.5: Metadata and readability pass

Invoke the `metadata-check` skill on every short string the skill generated or modified: page titles, meta descriptions, schema `description` fields, FAQ answers, and any blog post frontmatter `excerpt` values you wrote. It checks front-loading, concreteness, filler, active voice, title/description duplication, difficult words, SERP-truncation fit (title 30–65, description 70–200 — the same bounds `validateMetadataLength` enforces), and one-idea-per-field. Apply the fixes directly. Skip the pass entirely for technical strings (URLs, schema `@id` values, enum values).

If the project has a blog or docs content collection, mention to the user as a follow-up that the `readability-check` skill can audit individual posts for multi-paragraph prose quality — but don't audit the entire content corpus yourself.

---

## Phase 3: Verify

- Run `npm run build`. If `seoGraph()` is wired, this also runs H1 validation, duplicate-meta detection, and schema validation — surface any warnings.
- Spot-check the built HTML: one page's `<head>` should now be clean, canonical correct, JSON-LD graph present and linked.
- Run the homepage through [Rich Results Test](https://search.google.com/test/rich-results) and [ClassySchema](https://classyschema.org/Visualisation).
- Confirm `/sitemap-index.xml` exists and references per-collection sitemaps.
- If IndexNow is wired, confirm the key verification route returns the key at `/[key].txt`.
- Remind the user about tasks that can't be automated:
  - Register the site in [Google Search Console](https://search.google.com/search-console) and [Bing Webmaster Tools](https://www.bing.com/webmasters).
  - Submit the sitemap index in both.
  - Generate an IndexNow key and commit it to config.
  - Install [Plausible](https://plausible.io/) or equivalent privacy-friendly analytics.

---

## Output format

```markdown
## Astro SEO audit: [site name]

### Score
| Category                              | Score |
|---------------------------------------|------:|
| 1. `<Seo>` component and head         |  x/10 |
| 2. Structured data / JSON-LD graph    |  x/10 |
| 3. Content collections and schema     |  x/10 |
| 4. Open Graph images                  |  x/10 |
| 5. Sitemaps and indexing              |  x/10 |
| 6. Agent discovery                    |  x/10 |
| 7. Performance                        |  x/10 |
| 8. Redirects and error handling       |  x/10 |
| 9. Build-time validation and content  |  x/10 |
| **Total**                             | xx/90 |

### Findings
[Grouped by category. Quote actual code/config. Be specific.]

### Files generated or changed
[List with short description of each.]

### Next steps
[Non-file tasks: GSC, Bing Webmaster Tools, IndexNow key generation, analytics.]
```

---

## Key principles

- **Opinionated defaults over optionality.** The guide picks a stack; this skill applies it. Don't offer five alternatives when one works.
- **`@jdevalk/astro-seo-graph` is the spine.** Route the `<Seo>` component, schema endpoints, IndexNow, FuzzyRedirect, and build validation through it unless the user has a strong reason to hand-roll.
- **Topics, not keyphrases.** When reviewing content, focus on topical coverage and readability, not keyword density.
- **Static, CDN-served HTML is the baseline.** Don't add SSR to solve problems static builds already don't have.
- **Agent discovery matters now.** Schema endpoints, schema map, NLWeb tags — the crawler is no longer the only consumer.
