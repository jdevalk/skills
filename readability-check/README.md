# Readability Check

Runs a readability audit on blog posts, documentation, READMEs, and other multi-paragraph prose. Calibrated for readers who read English as a second language -- the default audience, not a fallback. Reports a Flesch Reading Ease score alongside a per-category status across nine checks.

## What it checks

- **Paragraph structure** -- lead sentence quality, one idea per paragraph, visual density
- **Opening paragraph** -- does the first sentence state the point, can the intro stand alone as a summary
- **Sentence length** -- tiered thresholds (14-20 normal, 21-30 long, 30+ flag every instance)
- **Passive voice** -- flags passive constructions and stacked passives, keeps passive when the actor is irrelevant
- **Difficult words** -- flags words an L2 reader would not use in conversation when a simpler synonym exists
- **Filler and hedging** -- "really", "just", "very", "in order to", "due to the fact that", and similar
- **Transition words** -- flags sequences of 3+ paragraphs with no connectors
- **Variation** -- repeated words/phrases within 200 words, repetitive paragraph openings
- **Heading hierarchy** -- proper nesting, descriptive subheadings, parallel structure among siblings

## Usage

Trigger this skill when you want a readability pass on prose. Example prompts:

- "Check the readability of this post"
- "Is this readable for a non-native English speaker?"
- "Run a readability audit on my README"
- "Readability pass on this draft"

The skill outputs a Flesch score, per-category pass/warn/fail status, quoted issues with concrete fixes, and specific praise for what works well.

## Works with

This skill is commonly chained into by other skills:

- **github-profile** -- invokes readability-check on the generated profile README
- **github-repo** -- invokes it on README, CONTRIBUTING.md, and SECURITY.md prose
- **wp-readme-optimizer** -- invokes it on the long description section

For short strings (titles, descriptions, bios, taglines), use **metadata-check** instead.

## Install

```
npx skills add jdevalk/skills --skill readability-check
```
