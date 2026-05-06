# Static SEO — Implementation recipes

Detailed code recipes for Phase 2 (Improve). Read this when you need to implement a specific fix flagged by the audit. Parent `SKILL.md` has the workflow and audit checklist.

## Where to apply changes (per build tool)

The recipes below show **the HTML that should land in the build output**. Apply at whichever layer your stack provides:

| Build tool | Where head metadata lives |
| --- | --- |
| Jekyll | `_includes/head.html` (or `_layouts/default.html`) |
| Hugo | `themes/<theme>/layouts/partials/head.html` (or `layouts/_default/baseof.html`) |
| 11ty | `_includes/layouts/base.njk` (or whatever the base layout is) |
| Gatsby | `src/components/SEO.js` (or `Helmet` in each page) |
| Next.js (static export) | `pages/_document.tsx` for global, `<Head>` in each page for per-page |
| Astro | use `astro-seo` skill instead — `<Seo>` component handles all of this |
| Hand-rolled / scraped | edit `<head>` directly, or post-process via a Python / Node script |

For dynamic values (title, description, canonical), wire up the build tool's templating syntax — Liquid (`{{ page.title }}`) for Jekyll, Go templates (`{{ .Title }}`) for Hugo, Nunjucks / EJS / JSX as appropriate.

## Head metadata

Canonical block to land on every page. Inline placeholders are filled per-page; the rest is global.

```html
<!-- Title and description -->
<title>{{ title }} — {{ siteName }}</title>
<meta name="description" content="{{ description }}">

<!-- Canonical and robots -->
<link rel="canonical" href="{{ canonicalUrl }}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">

<!-- Open Graph -->
<meta property="og:type" content="{{ ogType }}"><!-- "website" or "article" -->
<meta property="og:title" content="{{ title }}">
<meta property="og:description" content="{{ description }}">
<meta property="og:url" content="{{ canonicalUrl }}">
<meta property="og:image" content="{{ ogImageUrl }}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="675">
<meta property="og:site_name" content="{{ siteName }}">
<meta property="og:locale" content="{{ locale }}"><!-- e.g. en_US -->

<!-- Twitter Card (suppress duplicates of og:* — Twitter falls back automatically) -->
<meta name="twitter:card" content="summary_large_image">

<!-- Hreflang (multilingual sites only) -->
<link rel="alternate" hreflang="en" href="{{ siteOrigin }}/en/foo/">
<link rel="alternate" hreflang="nl" href="{{ siteOrigin }}/nl/foo/">
<link rel="alternate" hreflang="x-default" href="{{ siteOrigin }}/en/foo/">

<!-- Noindex pages: omit canonical entirely (Google's recommendation) -->
<!-- <meta name="robots" content="noindex"> -->

<!-- Article-specific OG (only for article pages) -->
<meta property="article:author" content="{{ siteOrigin }}/about/">
<meta property="article:published_time" content="{{ publishDateISO }}">
<meta property="article:modified_time" content="{{ modifiedDateISO }}">
```

Fallback chain to apply when generating titles and descriptions: `seo.title → page.title → siteName`; `seo.description → page.excerpt → first paragraph of body`. Pages with blank titles or descriptions are the most common symptom of a broken fallback.

## Structured data / JSON-LD graph

A linked `@graph` is much more useful than a flat `Article`. Every entity gets an `@id` (a URL fragment), and other entities reference it. Crawlers reconstruct the relationships automatically.

```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebSite",
            "@id": "https://example.com/#website",
            "url": "https://example.com/",
            "name": "Example",
            "publisher": { "@id": "https://example.com/#organization" },
            "potentialAction": {
                "@type": "SearchAction",
                "target": "https://example.com/?s={search_term_string}",
                "query-input": "required name=search_term_string"
            }
        },
        {
            "@type": "Organization",
            "@id": "https://example.com/#organization",
            "name": "Example",
            "url": "https://example.com/",
            "logo": {
                "@type": "ImageObject",
                "url": "https://example.com/logo.png",
                "width": 600,
                "height": 60
            }
        },
        {
            "@type": "BlogPosting",
            "@id": "https://example.com/blog/post/#article",
            "headline": "{{ title }}",
            "description": "{{ description }}",
            "image": { "@id": "https://example.com/blog/post/#primaryimage" },
            "author": { "@id": "https://example.com/about/#person" },
            "publisher": { "@id": "https://example.com/#organization" },
            "datePublished": "{{ publishDateISO }}",
            "dateModified": "{{ modifiedDateISO }}",
            "mainEntityOfPage": { "@id": "https://example.com/blog/post/#webpage" },
            "articleBody": "{{ articleBodyTextStripped }}"
        },
        {
            "@type": "ImageObject",
            "@id": "https://example.com/blog/post/#primaryimage",
            "url": "https://example.com/og/blog-post.jpg",
            "width": 1200,
            "height": 675
        },
        {
            "@type": "WebPage",
            "@id": "https://example.com/blog/post/#webpage",
            "url": "https://example.com/blog/post/",
            "name": "{{ title }}",
            "isPartOf": { "@id": "https://example.com/#website" },
            "primaryImageOfPage": { "@id": "https://example.com/blog/post/#primaryimage" },
            "breadcrumb": { "@id": "https://example.com/blog/post/#breadcrumb" }
        },
        {
            "@type": "BreadcrumbList",
            "@id": "https://example.com/blog/post/#breadcrumb",
            "itemListElement": [
                { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
                { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog/" },
                { "@type": "ListItem", "position": 3, "name": "{{ title }}" }
            ]
        }
    ]
}
</script>
```

Validate with [Rich Results Test](https://search.google.com/test/rich-results) and [ClassySchema](https://classyschema.org/Visualisation). The latter visualises `@id` references — handy for spotting dangling pointers.

## Open Graph image generation

Goal: every page has a 1200×675 JPEG OG image with a deterministic URL derived from the slug, generated at build time. No manual upload step. Three common approaches:

### Option A — `satori-cli` (best for text cards)

```sh
npm install -g @vercel/satori-cli
# In a build script, for each page:
satori-cli render \
    --width 1200 --height 675 \
    --font Inter:700 \
    --template '<div style="display:flex;...">{{ title }}</div>' \
    --out dist/og/{{ slug }}.svg
sharp dist/og/{{ slug }}.svg --jpeg --output dist/og/{{ slug }}.jpg
```

Satori renders JSX / HTML to SVG; convert with `sharp` to JPEG. Stick to flexbox, basic typography, absolute positioning — satori doesn't support every CSS feature.

### Option B — `sharp` composite (best for photo cards)

```js
// build-og.js
import sharp from 'sharp';

await sharp('hero.jpg')
    .resize(1200, 675, { fit: 'cover' })
    .composite([{
        input: Buffer.from(`
            <svg width="1200" height="675">
                <rect x="0" y="450" width="1200" height="225" fill="rgba(0,0,0,0.6)"/>
                <text x="60" y="600" font-family="Inter" font-size="72" fill="white">${title}</text>
            </svg>`),
        top: 0, left: 0,
    }])
    .jpeg({ quality: 90 })
    .toFile(`dist/og/${slug}.jpg`);
```

Faster than satori for photo-heavy cards and avoids the CSS limits.

### Option C — ImageMagick

```sh
magick -size 1200x675 xc:'#0e2e5c' \
    -font Inter-Bold -pointsize 72 -fill white -gravity center \
    -annotate 0 "${title}" \
    dist/og/${slug}.jpg
```

Bare-bones, works in any CI, no Node dependency. Limited typography control.

### Wire-up

For each page, set `og:image` to the deterministic URL: `https://example.com/og/{{ slug }}.jpg`. If the site is multilingual, include the locale: `/og/<locale>/<slug>.jpg`.

If the project already has an OG route, verify: output is 1200×675 JPEG (not WebP / AVIF / PNG — social platforms don't all support those), the URL is deterministic from the slug, and generation runs at build time (not on request).

## `sitemap.xml` and `robots.txt`

### sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://example.com/</loc>
        <lastmod>2026-05-06</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://example.com/blog/post/</loc>
        <lastmod>2026-04-12</lastmod>
    </url>
    <!-- ... -->
</urlset>
```

For lastmod, prefer git commit timestamps over filesystem `mtime` (CI checkouts have wrong mtimes). Most build tools ship a sitemap plugin: `jekyll-sitemap`, `hugo` built-in `sitemap.xml`, `@11ty/eleventy-plugin-rss`, `gatsby-plugin-sitemap`, `next-sitemap`. For hand-rolled / scraped sites, write a small build script.

### robots.txt

```text
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
Schemamap: https://example.com/schemamap.xml

Content-Signal: ai-train=yes, search=yes, ai-input=yes
```

Common Content-Signal policies:

- "Public corpus, anything goes": `ai-train=yes, search=yes, ai-input=yes`
- "Indexable but not for training": `ai-train=no, search=yes, ai-input=yes`
- "Search only, no AI": `ai-train=no, search=yes, ai-input=no`

## IndexNow

Two pieces:

1. **Key verification.** Generate a UUID-like key. Commit a static file at `<key>.txt` whose contents are exactly `<key>` (one line, no whitespace).
2. **Submission.** Post URLs to `https://api.indexnow.org/IndexNow` on each production deploy:

```sh
# Run only on production deploys — gate on host env vars.
# Vercel: VERCEL_ENV=production
# Cloudflare Pages: CF_PAGES_BRANCH=main
# Netlify: CONTEXT=production
test "$VERCEL_ENV" = "production" || exit 0

KEY="${INDEXNOW_KEY:?set INDEXNOW_KEY}"
HOST="example.com"
URLS=$(grep -oE '<loc>[^<]+</loc>' public/sitemap.xml | sed -E 's|</?loc>||g')
JSON=$(jq -c --arg host "$HOST" --arg key "$KEY" --argjson urls "$(echo "$URLS" | jq -R . | jq -s .)" \
    '{host: $host, key: $key, keyLocation: "https://\($host)/\($key).txt", urlList: $urls}' <<<'{}')
curl -fsSL -H "Content-Type: application/json" -X POST \
    https://api.indexnow.org/IndexNow -d "$JSON"
```

**Don't submit from local builds** — it pings the endpoint with URLs the production host hasn't served yet, gets the key marked invalid (403), and forces rotation.

## llms.txt

Static text file at the site root. Format ([spec](https://llmstxt.org)):

```text
# Example

> One-line description of the site.

Optional paragraphs giving more context.

## Blog posts

- [Post one](https://example.com/blog/post-one/): One-line description from the frontmatter excerpt.
- [Post two](https://example.com/blog/post-two/): One-line description from the frontmatter excerpt.

## Pages

- [About](https://example.com/about/): Who runs this site.
```

Generate from your content collection in a build step. Most build tools have a way to walk all pages and emit a custom file; for hand-rolled sites, write a Python script that reads frontmatter and emits the format.

## Markdown alternates

Serve `/blog/post.md` next to `/blog/post/index.html` so AI agents can consume content without HTML parsing.

### Static option (commit the `.md` files)

For each markdown source, also emit a clean `.md` to the build output with YAML frontmatter:

```yaml
---
title: Post title
canonical: https://example.com/blog/post/
pubDate: 2026-04-12
description: Excerpt.
---

# Post title

Body markdown without HTML wrappers.
```

Add `<link rel="alternate" type="text/markdown" href="/blog/post.md">` to the page's `<head>`. **Verify the file exists before adding the link** — broken alternates 404 when agents fetch them.

### Cloudflare content negotiation (no separate file)

If the site is on Cloudflare Pages, a Transform Rule rewrites `Accept: text/markdown` requests to the `.md` path. Free plan-compatible (`wildcard_replace` instead of paid-only `regex_replace`):

```text
When incoming requests match:
    http.request.headers["accept"][0] contains "text/markdown"
    and ends_with(http.request.uri.path, "/")
    and not starts_with(http.request.uri.path, "/_")

Then rewrite URI path (dynamic):
    wildcard_replace(http.request.uri.path, "*/", "${1}.md")
```

**Don't add a `Vary: Accept` response-header rule** — Cloudflare strips custom Vary values at the edge. The URL rewrite already separates cache entries per content type.

## API catalog (RFC 9727)

Static JSON file at `/.well-known/api-catalog`. `Content-Type: application/linkset+json`.

```json
{
    "linkset": [
        {
            "anchor": "https://example.com/schema/post.json",
            "service-doc": [{ "href": "https://example.com/schema/" }],
            "type": [{ "href": "https://schema.org/BlogPosting" }]
        },
        {
            "anchor": "https://example.com/schemamap.xml",
            "service-doc": [{ "href": "https://example.com/schema/" }]
        },
        {
            "anchor": "https://example.com/feed.xml",
            "type": [{ "href": "https://www.w3.org/2005/Atom" }]
        }
    ]
}
```

Set the `Content-Type` via `_headers` (CF Pages / Netlify) or `vercel.json`:

```text
/.well-known/api-catalog
    Content-Type: application/linkset+json
    Cache-Control: max-age=300
```

## `Link` headers for agent discovery

A single `Link` header on `/*` consolidates the discovery surface — sitemap, llms.txt, api-catalog, schemamap, RSS — so agents reading response headers don't have to load HTML.

**Cloudflare Pages / Netlify** — `public/_headers`:

```text
/*
    Link: </sitemap.xml>; rel="sitemap", </llms.txt>; rel="alternate"; type="text/plain", </.well-known/api-catalog>; rel="api-catalog", </schemamap.xml>; rel="schemamap", </feed.xml>; rel="alternate"; type="application/atom+xml"
```

**Vercel** — `vercel.json`:

```json
{
    "headers": [
        {
            "source": "/(.*)",
            "headers": [{
                "key": "Link",
                "value": "</sitemap.xml>; rel=\"sitemap\", </llms.txt>; rel=\"alternate\"; type=\"text/plain\", </.well-known/api-catalog>; rel=\"api-catalog\", </schemamap.xml>; rel=\"schemamap\""
            }]
        }
    ]
}
```

Only list resources the site actually serves — a `Link` entry pointing at a 404 is worse than no entry.

## Performance headers

### Cloudflare Pages / Netlify (`_headers`)

```text
/_astro/*
    Cache-Control: public, max-age=31536000, immutable

/assets/*
    Cache-Control: public, max-age=31536000, immutable

/*
    No-Vary-Search: key-order, params=("utm_source" "utm_medium" "utm_campaign" "utm_content" "utm_term")
```

### Vercel (`vercel.json`)

```json
{
    "headers": [
        {
            "source": "/_astro/(.*)",
            "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
        },
        {
            "source": "/assets/(.*)",
            "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
        }
    ]
}
```

### nginx

```nginx
location ~* \.(css|js|woff2|jpg|jpeg|png|webp|svg|avif)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Redirects

Maintain a redirect for every URL that ever existed and moved. Diff old URLs against the current sitemap; every URL in the old set not in the new set needs a redirect entry.

### Cloudflare Pages / Netlify (`_redirects`)

```text
/old-path/   /new-path/   301
/category/*  /blog/       301
```

### Vercel (`vercel.json`)

```json
{
    "redirects": [
        { "source": "/old-path/", "destination": "/new-path/", "permanent": true }
    ]
}
```

### nginx

```nginx
location = /old-path/ {
    return 301 /new-path/;
}
```

Confirm the 404 page returns a 404 status, not 200 — platform-specific behaviour, check the deployed response with `curl -I https://example.com/definitely-not-a-real-page`.

## CI workflows

### Broken-link checking ([linkinator](https://github.com/JustinBeckwith/linkinator))

```yaml
# .github/workflows/link-check.yml
name: Link Check
on:
    push:
        paths: ['src/**', 'content/**', '*.md']
    schedule:
        - cron: '0 9 * * 1'  # Weekly external-link recheck
    workflow_dispatch:
jobs:
    check:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - uses: actions/setup-node@v4
              with: { node-version: '20' }
            - run: npm install -g linkinator
            - run: linkinator https://example.com --recurse --skip "^https://(twitter|x)\\.com"
```

### HTML validation ([html-proofer](https://github.com/gjtorikian/html-proofer))

```yaml
- run: gem install html-proofer
- run: htmlproofer ./public --check-html --check-img-http --check-favicon
```

### Lighthouse CI

```yaml
- uses: treosh/lighthouse-ci-action@v11
  with:
      urls: |
          https://example.com/
          https://example.com/blog/post/
      uploadArtifacts: true
      configPath: ./.lighthouserc.json
```

`.lighthouserc.json`:

```json
{
    "ci": {
        "assert": {
            "assertions": {
                "categories:seo": ["error", { "minScore": 0.95 }],
                "categories:performance": ["warn", { "minScore": 0.8 }]
            }
        }
    }
}
```

### Title and description length validation

```py
# scripts/validate-metadata.py
import pathlib, re, sys
ERR = 0
TITLE_RE = re.compile(r'<title>([^<]+)</title>')
DESC_RE  = re.compile(r'<meta name="description" content="([^"]*)"', re.IGNORECASE)
for path in pathlib.Path('public').rglob('*.html'):
    html = path.read_text(encoding='utf-8')
    title = (TITLE_RE.search(html) or [None, ''])[1]
    desc  = (DESC_RE.search(html)  or [None, ''])[1]
    if not (30 <= len(title) <= 65):
        print(f'{path}: title length {len(title)} (want 30–65): {title!r}'); ERR += 1
    if not (70 <= len(desc) <= 200):
        print(f'{path}: description length {len(desc)} (want 70–200)'); ERR += 1
sys.exit(1 if ERR else 0)
```

Wire as a CI step. Same SERP-truncation bounds `metadata-check` enforces.
