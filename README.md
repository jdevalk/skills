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

### 👤 GitHub Profile Optimizer
Audits a GitHub profile page — bio, pinned repos, profile README, stats widgets, contribution visibility — and generates an optimized profile README. Works for both personal and organization profiles.

**Trigger phrases:** *"make my GitHub look good"*, *"create a profile README"*, *"optimize my developer profile"*

### 📝 WordPress Readme Optimizer
Reviews a WordPress.org plugin `readme.txt` with a structured audit, scores each section, and produces a fully rewritten version optimized for search visibility and install conversion.

**Trigger phrases:** *"optimize my readme"*, *"review my plugin listing"*, *"make my plugin page better"*

## Installation

Download the `.skill` file for the skill you want and open it — Claude will install it automatically. Alternatively, copy the skill folder into your Claude skills directory.

## Creating your own skills

Each skill is a folder containing a `SKILL.md` file with YAML frontmatter (name and description) followed by detailed instructions in Markdown. The description controls when Claude triggers the skill, and the body teaches Claude *how* to execute it.

See the existing skills for the pattern, or use the built-in **skill-creator** skill to scaffold a new one.

## License

This project is licensed under the [MIT License](LICENSE).
