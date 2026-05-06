# Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Markdown Lint](https://github.com/jdevalk/skills/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/markdown-lint.yml)
[![Link Check](https://github.com/jdevalk/skills/actions/workflows/link-check.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/link-check.yml)
[![Validate Skills](https://github.com/jdevalk/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/validate-skills.yml)

This repository collects agent skills that audit and improve your GitHub presence, WordPress and EmDash plugin CI/CD, WordPress.org plugin pages, Astro and static-site SEO, and the readability of your writing. There's also a tool to scrape a live WordPress site into a static HTML clone deployable on any static host. Each skill is a structured, score-based workflow that produces drop-in replacements.

## Installation

Install a single skill or all of them via the [skills CLI](https://skills.sh):

```sh
# One skill
npx skills add jdevalk/skills --skill astro-seo

# All skills in this repo
npx skills add jdevalk/skills
```

The CLI supports Claude Code, Cursor, Cline, GitHub Copilot, and 20+ other agents. Use `--agent` to pick which ones.

## Updating

```sh
# Update all installed skills
npx skills update

# Update a single skill
npx skills update astro-seo
```

**Optional: auto-check on session start.** Add a `SessionStart` hook to your Claude Code `settings.json` so stale skills are flagged before you hit them:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "npx skills update -g -y 2>/dev/null"
      }
    ]
  }
}
```

This runs outside the context window on every session start, `/clear`, and compaction — zero token cost.

## What's included

Each skill links to its own README with the full audit checklist, recipes, and sources.

### GitHub

- 🔧 **[github-repo](github-repo/)** — Audits a repo and generates the files that make it look professional: README, CONTRIBUTING, SECURITY, issue/PR templates, CODEOWNERS. Scores six categories. *Triggers:* "improve my repo", "set up issue templates", "make my GitHub project look professional".
- 👤 **[github-profile](github-profile/)** — Reviews your profile (bio, pinned repos, profile README, stats, contributions) and generates an optimised profile README. Personal and organisation profiles. *Triggers:* "make my GitHub look good", "create a profile README", "optimize my developer profile".

### CI/CD pipelines

- ⚙️ **[wp-github-actions](wp-github-actions/)** — Sets up a complete GitHub Actions pipeline for WordPress plugins: WPCS/PHPCS, PHP/JS/CSS linting, PHPUnit, PHPStan, Composer security, Playground PR previews, automated deployment to WordPress.org. *Triggers:* "add CI to my WordPress plugin", "deploy my plugin to WordPress.org automatically".
- 🔷 **[emdash-github-actions](emdash-github-actions/)** — Sets up GitHub Actions for EmDash plugins: TypeScript type-checking, ESLint, Vitest, npm security auditing, automated npm publishing on release. *Triggers:* "add CI to my EmDash plugin", "publish my EmDash plugin to npm automatically".

### WordPress

- 📝 **[wp-readme-optimizer](wp-readme-optimizer/)** — Reviews a WordPress.org plugin `readme.txt`, scores each section, and produces a fully rewritten version optimised for search visibility and install conversion. *Triggers:* "optimize my readme", "review my plugin listing", "make my plugin page better".
- 🧊 **[wp-static-clone](wp-static-clone/)** — Clones a live WordPress site into a static HTML site deployable on any static host (Cloudflare Pages, Netlify, Vercel, S3+CloudFront, plain Apache/nginx). Handles Cloudflare bot protection, mid-scrape link rewriting, comment-form runtime, Yoast attribution, and Gravatar privacy. *Triggers:* "scrape this WordPress site", "freeze [domain] as static HTML", "move this WP site to [host] with no build step".

### SEO

- 🚀 **[astro-seo](astro-seo/)** — Audits and improves SEO for Astro sites across nine categories: head metadata, JSON-LD graph, content collections, OG image generation, sitemaps + IndexNow, agent discovery, performance, redirects, build validation. Recipes route through [`@jdevalk/astro-seo-graph`](https://github.com/jdevalk/seo-graph). *Triggers:* "audit my Astro SEO", "set up SEO for my Astro site", "add structured data to my Astro blog".
- 🌐 **[static-seo](static-seo/)** — Same audit framework as `astro-seo`, but for any static HTML site (Hugo, Jekyll, 11ty, Gatsby, Next.js static export, hand-rolled, or `wp-static-clone` output). Platform-neutral recipes — raw `<meta>`, raw JSON-LD, hand-rolled `sitemap.xml`, generic CI tooling. *Triggers:* "audit the SEO on my static site", "set up structured data for my Hugo site", "add IndexNow and a sitemap to my Jekyll project".

### Writing quality

- 📖 **[readability-check](readability-check/)** — Readability audit calibrated for L2 English readers. Nine categories, Flesch Reading Ease score, quoted issues with concrete fixes. *Triggers:* "check readability", "is this readable", "readability pass".
- 🏷 **[metadata-check](metadata-check/)** — Reviews short high-value strings — page titles, meta descriptions, schema descriptions, FAQ answers, repo taglines, profile bios, social-card copy. Eight checks (front-loading, concreteness, filler removal, active voice, dedup, difficult words, truncation fit, one idea per field). Chained into by `astro-seo`, `static-seo`, `wp-readme-optimizer`, `github-repo`, and `github-profile`. *Triggers:* "check my metadata", "review my tagline", "is this bio any good".

## License

This project is licensed under the [MIT License](LICENSE).
