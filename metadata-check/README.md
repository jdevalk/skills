# Metadata Check

Reviews short, high-value strings where every character counts -- page titles, meta descriptions, schema description fields, FAQ answers, GitHub repo taglines, profile bios, and social-card copy. These strings are too short for Flesch scoring or paragraph-level readability analysis, so this skill applies the checks that actually matter at that scale.

## What it checks

- **Front-loading** -- the most specific, searchable term sits near the start of the string
- **Concreteness** -- names, numbers, and specific claims over vague language
- **Filler and hedging** -- flags wasted characters like "really", "just", "very", "basically"
- **Active voice** -- unless the object is genuinely the subject
- **Title/description duplication** -- descriptions that restate the title waste SERP space
- **Word choice** -- prefers common synonyms unless the domain term is what users search for
- **Truncation fit** -- checks against platform limits (SERP title ~60 chars, description ~160, GitHub ~100, Twitter bio 160)
- **One idea per field** -- titles and descriptions that try to promise two things land fuzzy

## Usage

Trigger this skill when you want to review short copy. Example prompts:

- "Check these meta descriptions"
- "Review my page titles for SEO"
- "Is this tagline good?"
- "Audit my GitHub bio"

The skill outputs a per-string report with pass/warn/fail on each check and a concrete rewrite for any string that fails.

## Works with

This skill is commonly chained into by other skills:

- **astro-seo** -- invokes metadata-check on generated SEO strings
- **wp-readme-optimizer** -- invokes it on plugin names, short descriptions, and FAQ answers
- **github-repo** -- invokes it on repo descriptions and README taglines
- **github-profile** -- invokes it on bios and pinned repo descriptions

For multi-paragraph prose, use **readability-check** instead.

## Install

```
npx skills add jdevalk/skills --skill metadata-check
```
