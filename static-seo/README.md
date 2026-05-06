# static-seo

Audits and improves the SEO setup of a static HTML site across nine categories, then produces drop-in code for anything missing or weak. Works for any source that produces static HTML — Hugo, Jekyll, 11ty, Gatsby, Next.js static export, Astro static output, hand-rolled HTML, or `wp-static-clone` output. Recipes are platform-neutral: raw `<meta>` tags, raw JSON-LD, hand-rolled `sitemap.xml`, generic CI tooling.

## What it checks

- **Head metadata** -- `<title>` and `<meta name="description">` length bounds, canonical URLs, robots directives, Open Graph + Twitter cards, hreflang
- **Structured data** -- linked JSON-LD `@graph` with `WebSite`, `Article`, `BreadcrumbList`, trust signals; valid against the Rich Results Test and Schema.org
- **Content quality** -- title and description hygiene, frontmatter consistency, body text readability
- **Open Graph images** -- 1200x675 JPEG, deterministic per-page URLs, alt text on every `<img>`
- **Sitemaps and indexing** -- `sitemap.xml` reachable, referenced from `robots.txt`, RSS feed with full content, IndexNow integration
- **Agent discovery** -- schema endpoints, schema map, `llms.txt`, markdown alternates, API catalog (RFC 9727), Content Signals, MCP / A2A discovery cards
- **Performance** -- cache headers on hashed assets, font preload, no render-blocking JS, image optimisation
- **Redirects** -- `_redirects` / `vercel.json` / nginx maintained, 301 not 302, custom 404 returns 404 status
- **CI validation** -- broken-link checking, HTML validation, Lighthouse CI, schema validation

## Usage

Trigger this skill when you want to audit, set up, or improve SEO on a static site. Example prompts:

- "Audit the SEO on my static site"
- "Set up structured data for my Hugo site"
- "Add IndexNow and a sitemap to my Jekyll project"
- "Improve my static site's head metadata"

The skill detects the source build tool (Hugo / Jekyll / 11ty / Gatsby / Next.js / Astro / hand-rolled) and tailors recommendations to the right place to apply changes.

## Works with

- **astro-seo** -- if the site is an Astro project, that skill produces less hand-rolled boilerplate by routing through `@jdevalk/astro-seo-graph`. `static-seo` is the right choice for everything else.
- **wp-static-clone** -- produces the kind of static HTML this skill audits. Chain them: clone with `wp-static-clone`, audit with `static-seo`.
- **metadata-check** -- automatically invoked on all generated SEO strings (titles, descriptions, schema fields).
- **readability-check** -- recommended as a follow-up for auditing blog post prose.

## Install

```sh
npx skills add jdevalk/skills --skill static-seo
```
