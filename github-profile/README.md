# GitHub Profile Optimizer

Audits a GitHub profile's public presence and generates an optimized profile README, along with recommendations for metadata fields, pinned repositories, and stats widgets. Works for both personal profiles and organization profile pages.

## What it checks

- **Profile README** -- structure, length, scannability, dynamic content freshness
- **Profile metadata** -- photo, bio (160 chars), company, location, website, social links, pronouns, status
- **Pinned repositories** -- all 6 slots used, descriptions filled, variety, star count, alignment with goals
- **Contribution activity** -- contribution graph, private contributions visibility, achievement badges
- **Stats widgets** -- github-readme-stats, streak stats, trophies, with theme recommendations
- **Tech stack badges** -- shields.io badges with Simple Icons for languages and tools
- **Social links** -- badge-style links to LinkedIn, Twitter/X, blog, email

## Usage

Trigger this skill when you want to improve your GitHub profile. Example prompts:

- "Audit my GitHub profile"
- "Create a profile README for my GitHub"
- "Make my GitHub look good"
- "Help me stand out on GitHub"
- "Set up our organization's GitHub profile page"

The skill pulls context automatically via `gh` CLI when available, so it can inspect your current repos, bio, and profile state.

## Works with

- **metadata-check** -- automatically invoked on your GitHub bio and pinned repo descriptions
- **readability-check** -- automatically invoked on the generated profile README prose
- **github-repo** -- recommended for polishing pinned repo READMEs individually

## Install

```
npx skills add jdevalk/skills --skill github-profile
```
