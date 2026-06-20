# Astro SEO

Audits and improves the SEO setup of an Astro site across nine categories, then produces drop-in code for anything missing or weak. The skill is opinionated: it routes most fixes through [`@jdevalk/astro-seo-graph`](https://github.com/jdevalk/seo-graph) and follows the methodology from [Astro SEO: the definitive guide](https://joost.blog/astro-seo-complete-guide/).

## What it checks

- **Head metadata** -- `<Seo>` component, canonical URLs, fallback chains, robots directives, hreflang
- **Structured data** -- linked JSON-LD `@graph` with `WebSite`, `Article`, `BreadcrumbList`, trust signals
- **Content collections** -- Zod schemas, SEO field validation, `articleBody` in schema endpoints
- **Open Graph images** -- 1200x675 JPEG generation via satori + sharp, alt text validation
- **Sitemaps and indexing** -- sitemap index, RSS feed, IndexNow integration, git-based `lastmod`
- **Agent discovery** -- schema endpoints, schema map, `llms.txt`, markdown alternates, NLWeb, ARD catalog, OKF bundle
- **Performance** -- static output, zero client JS, image optimization, font preloading, caching headers
- **Redirects** -- `_redirects` file, `FuzzyRedirect` on the 404 page, correct status codes
- **Build-time validation** -- H1 checks, unique metadata, internal link validation, broken link CI

## Usage

Trigger this skill when you want to audit, set up, or improve SEO on an Astro site. Example prompts:

- "Audit the SEO on my Astro site"
- "Set up structured data for my blog"
- "Add IndexNow and a sitemap to my Astro project"
- "Improve my site's head metadata"

The skill detects your project shape automatically -- you do not need to describe your setup.

## Works with

- **metadata-check** -- automatically invoked on all generated SEO strings (titles, descriptions, schema fields)
- **readability-check** -- recommended as a follow-up for auditing blog post prose
- **static-seo** -- if the site is *not* an Astro project (Hugo, Jekyll, 11ty, Gatsby, Next.js static export, hand-rolled HTML, or `wp-static-clone` output), use that skill instead. Same audit framework, platform-neutral recipes, no `@jdevalk/astro-seo-graph` dependency.

## Install

```sh
npx skills add jdevalk/skills --skill astro-seo
```

## Sources

- Joost de Valk -- [Astro SEO: the definitive guide](https://joost.blog/astro-seo-complete-guide/)
- [`@jdevalk/astro-seo-graph`](https://github.com/jdevalk/seo-graph) -- the `<Seo>` component, schema endpoints, IndexNow, FuzzyRedirect, build validation
- [`@astrojs/sitemap`](https://docs.astro.build/en/guides/integrations-guide/sitemap/) -- per-collection sitemaps
- [IndexNow](https://www.indexnow.org/) -- active indexing protocol
- [NLWeb](https://github.com/nlweb-ai/NLWeb) -- agent discovery protocol
