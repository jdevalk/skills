# Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Markdown Lint](https://github.com/jdevalk/skills/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/markdown-lint.yml)
[![Link Check](https://github.com/jdevalk/skills/actions/workflows/link-check.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/link-check.yml)
[![Validate Skills](https://github.com/jdevalk/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/validate-skills.yml)

This repository collects Claude Code skills that improve your GitHub presence, WordPress plugins, EmDash plugins, Astro sites, and the readability of your writing. You can audit and improve GitHub repos and profile pages, set up CI/CD pipelines for WordPress and EmDash plugins, rewrite WordPress.org readme files for better search rankings, audit Astro site SEO end-to-end, and run a readability pass on drafts. Each skill is a structured, score-based workflow that produces drop-in replacements.

## Installation

Pick the option that matches your setup.

### Claude Code (one-click)

Download the `.skill` file for the skill you want from the [latest release](https://github.com/jdevalk/skills/releases/latest) and open it — Claude installs it automatically.

### Any agent that supports the skills format (manual copy)

`.skill` files are plain zip archives. Two ways to install the skill folder:

1. **From a release.** Download the `.skill` from the [latest release](https://github.com/jdevalk/skills/releases/latest), unzip it, and move the resulting folder into your agent's skills directory (for Claude Code that's `~/.claude/skills/`).
2. **From the repo.** Clone the repo and copy or symlink the skill folder:

   ```sh
   git clone https://github.com/jdevalk/skills.git
   cp -r skills/astro-seo ~/.claude/skills/
   # or, to stay in sync with upstream:
   ln -s "$(pwd)/skills/astro-seo" ~/.claude/skills/astro-seo
   ```

Each skill is self-contained: the folder holds a `SKILL.md` plus any referenced assets. If your agent uses a different skills directory, substitute that path.

## Update checks

Every skill carries a `version:` field in its frontmatter. On invocation, each skill fetches [`versions.json`](https://raw.githubusercontent.com/jdevalk/skills/main/versions.json) at the repo root and compares its own version to the manifest. If it's behind, it tells you and links to the [latest release](https://github.com/jdevalk/skills/releases/latest) — the check is informational and never blocks execution. CI validates that every SKILL.md's `version:` matches the `versions.json` entry for its directory, so the manifest and the shipped skills can't drift.

## What's included

### 🔧 GitHub Repo Optimizer

Audits a GitHub repository against best practices and generates the files that make a repo look professional: README, CONTRIBUTING.md, SECURITY.md, issue/PR templates, and more. Scores six categories out of 60 and produces drop-in replacements for anything that's missing or weak.

**Trigger phrases:** *"improve my repo"*, *"set up issue templates"*, *"make my GitHub project look professional"*

<details>
<summary><strong>Sources</strong></summary>

- Joost de Valk — [How to create a healthy GitHub repository](https://joost.blog/healthy-github-repository/)
- GitHub Docs — [About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- GitHub Docs — [Setting guidelines for repository contributors](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)
- GitHub Docs — [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- GitHub Docs — [Configuring issue templates for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- GitHub Docs — [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- GitHub Docs — [Customizing your repository's social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)

</details>

### 👤 GitHub Profile Optimizer

Reviews a GitHub profile page — bio, pinned repos, profile README, stats widgets, contribution visibility — and generates an optimized profile README. Works for both personal and organization profiles.

**Trigger phrases:** *"make my GitHub look good"*, *"create a profile README"*, *"optimize my developer profile"*

<details>
<summary><strong>Sources</strong></summary>

- Joost de Valk — [Good-looking GitHub profile pages](https://joost.blog/good-looking-github-profile-pages/)
- GitHub Docs — [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- GitHub Docs — [About your profile](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/about-your-profile)
- GitHub Docs — [Customizing your organization's profile](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile)
- GitHub Docs — [Contributions on your profile](https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile)

</details>

### ⚙️ WordPress GitHub Actions

Sets up a complete GitHub Actions CI/CD pipeline for WordPress plugins. The skill analyzes your plugin's structure — Composer, JS/CSS assets, tests, WordPress.org listing — and picks the workflows you need. Coverage includes:

- Coding standards (WPCS/PHPCS)
- PHP and JS/CSS linting
- PHPUnit testing and PHPStan static analysis
- Composer security scanning
- WordPress Playground PR previews
- Automated deployment to WordPress.org

**Trigger phrases:** *"add CI to my WordPress plugin"*, *"set up GitHub Actions for my plugin"*, *"deploy my plugin to WordPress.org automatically"*

<details>
<summary><strong>Sources</strong></summary>

- Joost de Valk — [GitHub Actions to keep your WordPress plugin healthy](https://joost.blog/github-actions-wordpress/)
- [10up/wpcs-action](https://github.com/10up/wpcs-action) — WordPress Coding Standards GitHub Action
- [10up/action-wordpress-plugin-deploy](https://github.com/10up/action-wordpress-plugin-deploy) — Deploy to WordPress.org
- [WordPress/action-wp-playground-pr-preview](https://github.com/WordPress/action-wp-playground-pr-preview) — Playground PR previews
- WordPress Developer Blog — [How to add automated unit tests to your WordPress plugin](https://developer.wordpress.org/news/2025/12/how-to-add-automated-unit-tests-to-your-wordpress-plugin/)

</details>

### 🔷 EmDash GitHub Actions

Sets up GitHub Actions CI/CD workflows for EmDash plugins. The skill analyzes your plugin's structure — TypeScript source, React admin UI, tests, npm publishing — and picks the workflows you need. Coverage includes:

- TypeScript type-checking with `emdash` types
- ESLint linting
- Vitest testing
- npm security auditing
- Automated npm publishing on release

**Trigger phrases:** *"add CI to my EmDash plugin"*, *"set up GitHub Actions for my EmDash plugin"*, *"publish my EmDash plugin to npm automatically"*

<details>
<summary><strong>Sources</strong></summary>

- [EmDash CMS](https://github.com/emdash-cms/emdash) — Full-stack TypeScript CMS based on Astro
- GitHub Docs — [Publishing Node.js packages](https://docs.github.com/en/actions/use-cases-and-examples/publishing-packages/publishing-nodejs-packages)
- TypeScript Docs — [Compiler Options](https://www.typescriptlang.org/tsconfig/)

</details>

### 📝 WordPress Readme Optimizer

Reviews a WordPress.org plugin `readme.txt` with a structured audit, scores each section, and produces a fully rewritten version optimized for search visibility and install conversion.

**Trigger phrases:** *"optimize my readme"*, *"review my plugin listing"*, *"make my plugin page better"*

<details>
<summary><strong>Sources</strong></summary>

- Matt Cromwell — [How I Optimize Plugin README's for Better Search Results](https://mattcromwell.com/wordpress-plugin-readme-optimization/)
- Freemius — [Outrank Competitors' SEO on the WordPress.org Plugin Repository](https://freemius.com/blog/seo-on-new-plugin-repository/)
- Freemius — [A Guide to Optimizing Your Plugin's WordPress.org Page](https://freemius.com/blog/optimizing-plugin-wordpress-page/)
- WordPress Plugin Handbook — [How Your Plugin Assets Work](https://developer.wordpress.org/plugins/wordpress-org/plugin-assets/)
- SitePoint — [How To Create an Awesome WordPress Page for Your Plugin](https://www.sitepoint.com/create-awesome-wordpress-org-page-plugin/)

</details>

### 🚀 Astro SEO

Audits and improves SEO for Astro sites across nine categories: the `<Seo>` component and head metadata, linked JSON-LD graphs, content-collection Zod schemas, auto-generated Open Graph images, per-collection sitemaps with git-based lastmod, IndexNow submission, schema endpoints and schema maps for agent discovery, redirects and `FuzzyRedirect`, and performance defaults. The stack is opinionated and routes most fixes through [`@jdevalk/astro-seo-graph`](https://github.com/jdevalk/seo-graph).

**Trigger phrases:** *"audit my Astro SEO"*, *"set up SEO for my Astro site"*, *"add structured data to my Astro blog"*

<details>
<summary><strong>Sources</strong></summary>

- Joost de Valk — [Astro SEO: the definitive guide](https://joost.blog/astro-seo-complete-guide/)
- [`@jdevalk/astro-seo-graph`](https://github.com/jdevalk/seo-graph) — the `<Seo>` component, schema endpoints, IndexNow, FuzzyRedirect, build validation
- [`@astrojs/sitemap`](https://docs.astro.build/en/guides/integrations-guide/sitemap/) — per-collection sitemaps
- [IndexNow](https://www.indexnow.org/) — active indexing protocol
- [NLWeb](https://github.com/nlweb-ai/NLWeb) — agent discovery protocol

</details>

### 📖 Readability Check

Runs a readability audit on a blog post draft, calibrated for readers who read English as a second language. The skill checks nine categories:

- Paragraph structure and lead sentences
- Opening paragraph strength
- Tiered sentence length
- Passive voice
- Difficult words (judged by L2 conversational use, not syllable count)
- Filler and hedging
- Transitions
- Variation
- Heading hierarchy

Output combines a Flesch Reading Ease score (with target bands) and a per-category status. Each issue quotes the problem text with a concrete fix, and specific passages that work get called out too. In technical posts, the skill holds non-technical paragraphs — intros, context, conclusions — to a stricter L2 standard than the technical sections.

**Trigger phrases:** *"check readability"*, *"is this readable"*, *"readability pass"*

<details>
<summary><strong>Sources</strong></summary>

- Yoast — [Readability analysis in Yoast SEO](https://yoast.com/features/readability-analysis/)
- Rudolf Flesch — [Flesch Reading Ease formula](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests)
- Hemingway Editor — sentence-length tiering

</details>

## License

This project is licensed under the [MIT License](LICENSE).
