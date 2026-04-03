# Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Markdown Lint](https://github.com/jdevalk/skills/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/markdown-lint.yml)
[![Link Check](https://github.com/jdevalk/skills/actions/workflows/link-check.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/link-check.yml)
[![Validate Skills](https://github.com/jdevalk/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/validate-skills.yml)

Skills that optimize your GitHub presence, WordPress plugins, and EmDash plugins. Audit and improve your GitHub repos and profile pages, set up CI/CD pipelines for WordPress and EmDash plugins, and rewrite WordPress.org readme files for better search rankings and conversions — all through structured, score-based workflows that produce drop-in replacements.

## Installation

Download the `.skill` file for the skill you want from the [latest release](https://github.com/jdevalk/skills/releases/latest) and open it — Claude will install it automatically. Alternatively, copy the skill folder into your Claude skills directory.

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

Audits a GitHub profile page — bio, pinned repos, profile README, stats widgets, contribution visibility — and generates an optimized profile README. Works for both personal and organization profiles.

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

Sets up a complete GitHub Actions CI/CD pipeline for WordPress plugins. Analyzes your plugin's structure (Composer, JS/CSS assets, tests, WordPress.org listing) and creates the right set of workflows: coding standards (WPCS/PHPCS), PHP and JS/CSS linting, PHPUnit testing, PHPStan static analysis, Composer security scanning, WordPress Playground PR previews, and automated deployment to WordPress.org.

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

Sets up GitHub Actions CI/CD workflows for EmDash plugins. Analyzes your plugin's structure (TypeScript source, React admin UI, tests, npm publishing) and creates the right set of workflows: TypeScript type-checking with `emdash` types, ESLint linting, Vitest testing, npm security auditing, and automated npm publishing on release.

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

## License

This project is licensed under the [MIT License](LICENSE).
