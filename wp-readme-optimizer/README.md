# WordPress Plugin readme.txt Optimizer

Audits and rewrites WordPress.org plugin `readme.txt` files for higher visibility in the plugin directory, better conversion of visitors to installs, and a more trustworthy listing page. Scores eight sections, infers target keywords, and produces a drop-in replacement file.

## What it checks

- **Plugin name and tags** -- keyword presence, descriptiveness, tag relevance (up to 5)
- **Short description** -- benefit-led, under 150 characters, primary keyword included, no vague claims
- **Long description** -- hook paragraph, keyword placement, heading structure, social proof, calls to action
- **Installation** -- numbered steps, both manual and dashboard methods, post-activation guidance
- **FAQ** -- real user questions, keyword-rich answers, objection handling
- **Screenshots** -- captions present and keyword-aware (captions are indexed by WordPress.org search)
- **Changelog** -- up to date, user-facing value communicated, consistent format
- **Stable tag and headers** -- version match, PHP/WP version requirements, license declaration

## Usage

Trigger this skill when you want to improve a WordPress.org plugin listing. Example prompts:

- "Optimize my plugin's readme.txt"
- "Review this readme.txt"
- "Help me rank higher on WordPress.org"
- "Make my plugin page better"

Provide the readme.txt content by pasting it, attaching the file, or pointing the skill to the file in your repo.

## Works with

- **metadata-check** -- automatically invoked on the plugin name, short description, and FAQ answers
- **readability-check** -- automatically invoked on the long description prose

## Install

```
npx skills add jdevalk/skills --skill wp-readme-optimizer
```
