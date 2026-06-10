# Readability Check

Runs a readability audit on blog posts, documentation, READMEs, and other multi-paragraph prose. Calibrated for readers who read English as a second language -- the default audience, not a fallback. Reports a Flesch Reading Ease score alongside a per-category status across ten checks.

## What it checks

- **Overall structure and topic order** -- one recognizable ordering principle, related topics grouped, skimmable via headings and first sentences, a conclusion that closes the loop
- **Paragraph structure** -- core sentence first, one complete topic per paragraph, visual density
- **Opening paragraph** -- states the message, hooks the reader, sets expectations, held to the strictest readability bar
- **Sentence length** -- tiered thresholds (14-20 normal, 21-30 long, 30+ flag every instance)
- **Passive voice** -- flags passive constructions and stacked passives, keeps passive when the actor is irrelevant
- **Difficult words** -- flags words an L2 reader would not use in conversation when a simpler synonym exists
- **Filler and hedging** -- "really", "just", "very", "in order to", "due to the fact that", and similar
- **Transition words** -- connectors matched to the relation (enumerating, cause, contrast, concluding), flags sequences of 3+ paragraphs with none
- **Variation** -- repeated words/phrases within 200 words, repetitive paragraph openings
- **Heading hierarchy** -- proper nesting, headings that cover their sections, parallel structure among siblings, a TOC for long posts

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

For short strings (titles, descriptions, bios, taglines), use **metadata-check** instead. For whether a post earns a ranking — intent fit, keyphrase placement, E-E-A-T — chain into **content-seo** after the readability pass.

## Install

```sh
npx skills add jdevalk/skills --skill readability-check
```

## Sources

- Yoast -- [Readability analysis in Yoast SEO](https://yoast.com/features/readability-analysis/)
- Rudolf Flesch -- [Flesch Reading Ease formula](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests)
- Hemingway Editor -- sentence-length tiering
