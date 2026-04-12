---
name: astro-seo
description: >
  Audits and improves SEO for Astro sites. Use when the user asks to audit,
  set up, or improve SEO on an Astro site, or mentions head metadata,
  structured data, JSON-LD, sitemaps, IndexNow, Open Graph images, schema
  endpoints, NLWeb, hreflang, or search engine indexing in an Astro project.
  Produces drop-in code routed through `@jdevalk/astro-seo-graph` and chains
  into `readability-check` for generated prose.
---

# Astro SEO

Audits and improves the SEO setup of an Astro site against the full stack described in [Astro SEO: the definitive guide](https://joost.blog/astro-seo-complete-guide/). The skill covers nine areas — technical foundation, structured data, content, site structure, performance, sitemaps and indexing, agent discovery, redirects, and analytics — and produces drop-in code for anything missing or weak.

The opinionated spine of this skill is [`@jdevalk/astro-seo-graph`](https://github.com/jdevalk/seo-graph). Most of the fixes route through it. If the project doesn't use it yet, installing it is the first recommendation.

## Workflow

1. **Detect the project** — confirm this is an Astro site and understand its shape.
2. **Audit** — score nine categories and produce actionable findings.
3. **Improve** — generate or modify files to close the gaps.
4. **Readability pass** — invoke `readability-check` on any prose the skill generated (titles, descriptions, schema `description` fields, FAQ entries).
5. **Verify** — run the build, check validations pass, remind the user about non-file tasks (Search Console, Bing Webmaster Tools, IndexNow key verification).

---

## Phase 0: Detect the project

Confirm the basics before auditing:

- `astro.config.mjs` / `astro.config.ts` exists.
- `package.json` has `astro` as a dependency.
- **`site:` is set in `astro.config`** — canonicals, sitemaps, and OG image URLs all derive from this. If it's missing, empty, or `http://localhost`, flag it as a blocking issue before anything else. This is the single most common misconfiguration.
- Content collections in `src/content/` (or legacy `src/pages/` markdown).
- **Deployment target** — read `package.json`, `vercel.json`, `netlify.toml`, `wrangler.toml`, or `public/_headers` to determine the host. This drives redirect and header syntax in Phase 2.
- **Is `@jdevalk/astro-seo-graph` already installed?** If yes, record the version and which features are wired (grep for `<Seo`, `seoGraph(`, `createSchemaEndpoint`, `FuzzyRedirect`, `createIndexNowKeyRoute`). **Check the installed version against the latest on npm** with `npm view @jdevalk/astro-seo-graph version`. If the project is behind, recommend an upgrade in Phase 2 before auditing feature gaps — the package ships new defaults and fixes regularly, and an outdated version is a plausible cause for any audit finding. Phase 2 branches on this.
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

### 5. Sitemaps and indexing (/10)

- **Must** — `@astrojs/sitemap` installed, sitemap index reachable.
- **Must** — `robots.txt` references the sitemap index.
- **Must** — RSS feed exists (`@astrojs/rss`), advertised via `<link rel="alternate" type="application/rss+xml">`, contains full post content (not truncated excerpts).
- **Should** — split per-collection via `chunks` option (`sitemap-posts-0.xml`, etc.) — much easier to debug indexing in GSC.
- **Should** — `lastmod` populated from git commit timestamps, not frontmatter dates or CI file timestamps.
- **Should** — IndexNow integrated and submitting on each build, with key verification route at `/[key].txt`.

### 6. Agent discovery (/10)

- **Should** — schema endpoints (`/schema/*.json`) exposing corpus-wide JSON-LD.
- **Should** — schema map (`/schemamap.xml`) listing all endpoints, with `Schemamap:` directive in `robots.txt`.
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

- **Must** — `seoGraph()` integration running on each build with H1 validation, duplicate title/description detection, and JSON-LD schema validation enabled.
- **Should** — broken link checker in CI. A [lychee](https://github.com/lycheeverse/lychee-action) GitHub Action on every push to content files catches dead links before they go live; a weekly scheduled run catches link rot as external sites move or disappear. Broken outbound links are a bad UX and a negative trust signal.
- **Should** — content audited for readability (lead sentences, sentences under 20 words, transitions). Phase 2.5 chains this in via `readability-check`.

---

## Phase 2: Improve

Based on the audit, produce the concrete code. Always ask before overwriting.

**Branch on the Phase 0 findings.** If `@jdevalk/astro-seo-graph` is already installed, skip the install step and focus on wiring the features the audit flagged as missing (IndexNow, FuzzyRedirect, schema endpoints, build validation). If the user has a hand-rolled setup that already satisfies the **Must** checks in category 1, don't rip it out — add only what's missing. Replacement is a last resort, not the default.

### Install or upgrade `@jdevalk/astro-seo-graph`

If not installed:

```sh
npm install @jdevalk/astro-seo-graph
```

If installed but behind the latest npm version (checked in Phase 0):

```sh
npm install @jdevalk/astro-seo-graph@latest
```

Read the package's [changelog](https://github.com/jdevalk/seo-graph/blob/main/packages/astro-seo-graph/CHANGELOG.md) between the installed and latest version before upgrading — new defaults may need explicit opt-out if the project relied on old behavior.

Wire the integration:

```js
// astro.config.mjs
import seoGraph from '@jdevalk/astro-seo-graph/integration';

export default defineConfig({
    site: 'https://example.com',
    integrations: [
        seoGraph({
            validateH1: true,
            validateDuplicateMeta: true,
            validateSchema: true,
            indexNow: {
                key: 'REPLACE_WITH_GENERATED_KEY',
                host: 'example.com',
                siteUrl: 'https://example.com',
            },
        }),
    ],
});
```

### `BaseHead.astro`

Replace whatever head metadata the project has with a single `<Seo>` call. The component handles title, description, canonical, Open Graph, Twitter, JSON-LD graph, and extra links in one place.

### Content collection schema

```ts
// src/content/config.ts
import { defineCollection, z } from 'astro:content';
import { seoSchema } from '@jdevalk/astro-seo-graph';

export const collections = {
    blog: defineCollection({
        schema: ({ image }) => z.object({
            title: z.string(),
            excerpt: z.string(),
            publishDate: z.coerce.date(),
            seo: seoSchema(image).optional(),
        }),
    }),
};
```

### Per-collection sitemap + git lastmod

```js
import sitemap from '@astrojs/sitemap';
import { execSync } from 'node:child_process';

function gitLastmod(filePath) {
    try {
        const log = execSync(`git log -1 --format="%cI" -- "${filePath}"`, { encoding: 'utf-8' }).trim();
        return log ? new Date(log) : null;
    } catch { return null; }
}

sitemap({
    entryLimit: 1000,
    chunks: {
        posts: (item) => isBlogPost(new URL(item.url).pathname) ? item : undefined,
    },
    serialize: (item) => {
        // attach gitLastmod for the source file that produced this URL
        return item;
    },
});
```

### OG image route

Stand up `/og/[...slug].jpg` using satori + sharp. If the project already has one, check it outputs 1200×675 JPEG.

### Schema endpoints and schema map

Each endpoint collects every entry in a content collection, builds the JSON-LD graph per entry, and serves the combined result as `application/ld+json`. Don't hand-write the mapper — the full implementation with entity builders (`buildWebPage`, `buildArticle`, etc.) and their expected arguments is documented in the [`astro-seo-graph` schema endpoints docs](https://github.com/jdevalk/seo-graph/tree/main/packages/astro-seo-graph#schema-endpoints). Copy from there. Then add `/schemamap.xml` listing every endpoint, and a `Schemamap:` directive in `robots.txt`.

### RSS feed

If no feed exists, add `@astrojs/rss`:

```sh
npm install @astrojs/rss
```

Create `src/pages/feed.xml.ts` that pulls the blog collection and renders full post bodies (not excerpts) — truncated feeds frustrate readers and give AI agents less to work with. Advertise the feed in the `<Seo>` component's `extraLinks` with `rel="alternate"` and `type="application/rss+xml"`.

### Redirects and FuzzyRedirect

Seeding `_redirects` from scratch is the unpleasant part. Practical approach:

- If migrating from WordPress or another CMS, export the old URL list from the source (WP-CLI `wp post list`, database dump, or the old sitemap via Wayback Machine).
- Diff old URLs against the current sitemap; every URL in the old set not in the new set needs a redirect entry.
- Commit the table once, maintain it going forward whenever you change a slug.

Syntax depends on the host:
- **Cloudflare Pages / Netlify:** `public/_redirects` — `/old-path /new-path 301` per line.
- **Vercel:** `vercel.json` with a `redirects` array.
- **Other hosts:** server config (nginx, Apache, etc.).

Then add `<FuzzyRedirect>` to the 404 page. Confirm the 404 page returns a 404 status, not 200 — platform-specific behavior, check the deployed response.

### Performance headers

Syntax depends on the host. Pick the one matching Phase 0's detected deployment target.

**Cloudflare Pages / Netlify** — `public/_headers`:

```text
/_astro/*
  Cache-Control: public, max-age=31536000, immutable

/*
  No-Vary-Search: key-order, params=("utm_source" "utm_medium" "utm_campaign" "utm_content" "utm_term")
```

**Vercel** — `vercel.json`:

```json
{
    "headers": [
        {
            "source": "/_astro/(.*)",
            "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
        },
        {
            "source": "/(.*)",
            "headers": [{ "key": "No-Vary-Search", "value": "key-order, params=(\"utm_source\" \"utm_medium\" \"utm_campaign\" \"utm_content\" \"utm_term\")" }]
        }
    ]
}
```

**Other hosts** — configure equivalents in server config; syntax varies.

### Broken link checker in CI

Add a [lychee](https://github.com/lycheeverse/lychee-action) workflow at `.github/workflows/link-check.yml`:

```yaml
name: Link Check
on:
  push:
    paths:
      - 'src/content/**'
      - 'src/pages/**'
      - '*.md'
  schedule:
    - cron: '0 9 * * 1'  # Weekly, Mondays 09:00 UTC — catches link rot
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lycheeverse/lychee-action@v2
        with:
          args: --no-progress './**/*.md' './**/*.astro' './**/*.mdx'
          fail: true
```

Push-triggered runs block broken links from shipping. The weekly run catches external link rot.

---

## Phase 2.5: Readability pass

Invoke the `readability-check` skill on every piece of prose the skill generated or modified: page titles, meta descriptions, schema `description` fields, FAQ entries, and any blog post frontmatter `excerpt` values you wrote.

SEO titles and descriptions are short but consequential — a long passive opening sentence in a meta description wastes the 160 characters Google shows in results. Apply the ⚠ and ✗ fixes directly. Skip the pass for technical strings (URLs, schema `@id` values, enum values).

If the project has a blog or docs content collection, note that the same `readability-check` skill can audit individual posts — mention this to the user as a follow-up, but don't audit the entire content corpus yourself.

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
