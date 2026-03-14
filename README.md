# Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Markdown Lint](https://github.com/jdevalk/skills/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/markdown-lint.yml)
[![Link Check](https://github.com/jdevalk/skills/actions/workflows/link-check.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/link-check.yml)
[![Validate Skills](https://github.com/jdevalk/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/jdevalk/skills/actions/workflows/validate-skills.yml)

A collection of skills for [Claude](https://claude.ai) that automate common developer workflows. Each skill teaches Claude a structured, repeatable process — so instead of giving vague advice, it runs a full audit and produces ready-to-use output.

## What's included

### 🔧 GitHub Repo Optimizer

Audits a GitHub repository against best practices and generates the files that make a repo look professional: README, CONTRIBUTING.md, SECURITY.md, issue/PR templates, and more. Scores six categories out of 60 and produces drop-in replacements for anything that's missing or weak.

**Trigger phrases:** *"improve my repo"*, *"set up issue templates"*, *"make my GitHub project look professional"*

**Sources:**

- Joost de Valk — [How to create a healthy GitHub repository](https://joost.blog/healthy-github-repository/)
- GitHub Docs — [About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- GitHub Docs — [Setting guidelines for repository contributors](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)
- GitHub Docs — [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- GitHub Docs — [Configuring issue templates for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- GitHub Docs — [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- GitHub Docs — [Customizing your repository's social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)

### 👤 GitHub Profile Optimizer

Audits a GitHub profile page — bio, pinned repos, profile README, stats widgets, contribution visibility — and generates an optimized profile README. Works for both personal and organization profiles.

**Trigger phrases:** *"make my GitHub look good"*, *"create a profile README"*, *"optimize my developer profile"*

**Sources:**

- Joost de Valk — [Good-looking GitHub profile pages](https://joost.blog/good-looking-github-profile-pages/)
- GitHub Docs — [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- GitHub Docs — [About your profile](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/about-your-profile)
- GitHub Docs — [Customizing your organization's profile](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile)
- GitHub Docs — [Contributions on your profile](https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile)

### ⚙️ WordPress GitHub Actions

Sets up a complete GitHub Actions CI/CD pipeline for WordPress plugins. Analyzes your plugin's structure (Composer, JS/CSS assets, tests, WordPress.org listing) and creates the right set of workflows: coding standards (WPCS/PHPCS), PHP and JS/CSS linting, PHPUnit testing, PHPStan static analysis, Composer security scanning, WordPress Playground PR previews, and automated deployment to WordPress.org.

**Trigger phrases:** *"add CI to my WordPress plugin"*, *"set up GitHub Actions for my plugin"*, *"deploy my plugin to WordPress.org automatically"*

**Sources:**

- Joost de Valk — [GitHub Actions to keep your WordPress plugin healthy](https://joost.blog/github-actions-wordpress/)
- [10up/wpcs-action](https://github.com/10up/wpcs-action) — WordPress Coding Standards GitHub Action
- [10up/action-wordpress-plugin-deploy](https://github.com/10up/action-wordpress-plugin-deploy) — Deploy to WordPress.org
- [WordPress/action-wp-playground-pr-preview](https://github.com/WordPress/action-wp-playground-pr-preview) — Playground PR previews
- WordPress Developer Blog — [How to add automated unit tests to your WordPress plugin](https://developer.wordpress.org/news/2025/12/how-to-add-automated-unit-tests-to-your-wordpress-plugin/)

### 📝 WordPress Readme Optimizer

Reviews a WordPress.org plugin `readme.txt` with a structured audit, scores each section, and produces a fully rewritten version optimized for search visibility and install conversion.

**Trigger phrases:** *"optimize my readme"*, *"review my plugin listing"*, *"make my plugin page better"*

**Sources:**

- Matt Cromwell — [How I Optimize Plugin README's for Better Search Results](https://mattcromwell.com/wordpress-plugin-readme-optimization/)
- Freemius — [Outrank Competitors' SEO on the WordPress.org Plugin Repository](https://freemius.com/blog/seo-on-new-plugin-repository/)
- Freemius — [A Guide to Optimizing Your Plugin's WordPress.org Page](https://freemius.com/blog/optimizing-plugin-wordpress-page/)
- WordPress Plugin Handbook — [How Your Plugin Assets Work](https://developer.wordpress.org/plugins/wordpress-org/plugin-assets/)
- SitePoint — [How To Create an Awesome WordPress Page for Your Plugin](https://www.sitepoint.com/create-awesome-wordpress-org-page-plugin/)

## Installation

Download the `.skill` file for the skill you want and open it, Claude will install it automatically. Alternatively, copy the skill folder into your Claude skills directory.

## Creating your own skills

Each skill is a folder containing a `SKILL.md` file with YAML frontmatter (name and description) followed by detailed instructions in Markdown. The description controls when Claude triggers the skill, and the body teaches Claude *how* to execute it.

See the existing skills for the pattern, or use the built-in **skill-creator** skill to scaffold a new one.

## License

This project is licensed under the [MIT License](LICENSE).
