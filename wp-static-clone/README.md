# wp-static-clone

Turn a live WordPress site into a static HTML clone deployable on any static host (Cloudflare Pages, Netlify, Vercel, S3+CloudFront, plain Apache/nginx). Driven by the site's XML sitemap. Handles the WordPress-specific gotchas that a naïve `wget` run misses — Cloudflare bot protection, mid-scrape link rewriting, proxied analytics, R2-offloaded uploads, comment-form runtime, Yoast attribution, Gravatar privacy.

## What it does

- **Discovers URLs** from the Yoast `sitemap_index.xml` (or plain `sitemap.xml`), including child sitemaps.
- **Scrapes in one shot** with a real-browser UA so Cloudflare doesn't 403, and `--convert-links` rewrites cross-page links correctly.
- **Pulls long-tail assets** referenced only in `og:image`, JSON-LD, `apple-touch-icon`, and `modulepreload` — the things `wget -p` doesn't follow.
- **Rewrites paths to root-relative** with a Python script that derives page slugs from the sitemap (not from a directory walk that would mis-classify `category/`, `feed/`, `author/`, etc.).
- **Strips WP runtime markup** that breaks once the backend is gone: comment forms, reply-link anchors (block + classic theme variants), `comment-reply.min.js`, REST API discovery, RSD, oEmbed, RSS alternates, archive `next` links.
- **Replaces the Plausible WP plugin** with the standard tracker, since the plugin proxies through `/wp-json/...` which doesn't exist statically.
- **Self-hosts every Gravatar** under `avatars/` — privacy fix and self-contained archive in one pass; size variants kept separate, extension detected from response bytes.
- **Brands the output** with an HTML banner and updates the Yoast XSL attribution.
- **Deploys** with host-specific recipes for Cloudflare Pages, Netlify, Vercel, nginx, and Apache.

## Usage

Trigger this skill when you want to scrape a WordPress site and deploy it as static HTML. Example prompts:

- "Scrape this WordPress site for Cloudflare Pages"
- "Freeze [domain] as static HTML"
- "Pull all the pages from this sitemap and turn them into static files"
- "Move this WP site to [host] with no build step"

The broad shape (sitemap → wget → root-relative paths → static host) generalises to any CMS that emits a standard XML sitemap. The runtime cleanup is WordPress-specific.

## Works with

- **static-seo** -- the natural follow-up. After cloning, run `static-seo` to audit head metadata, structured data, sitemaps, and indexing on the produced static HTML.

## Install

```sh
npx skills add jdevalk/skills --skill wp-static-clone
```
