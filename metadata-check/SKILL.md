---
name: metadata-check
version: "0.1"
description: >
  Reviews short high-value strings — page titles, meta descriptions,
  schema description fields, FAQ answers, GitHub repo taglines, profile
  bios, social-card copy, and other metadata where Flesch and
  paragraph-level readability checks don't apply. Checks front-loading,
  concreteness, filler, active voice, title/description duplication,
  difficult words, SERP-truncation fit, and one-idea-per-field. Use when
  the user asks to review metadata, a tagline, a bio, or SEO strings, or
  proactively after generating any short string with audience-facing
  impact. Chained into by astro-seo, wp-readme-optimizer, github-repo,
  and github-profile for their metadata outputs. For multi-paragraph
  prose, use the `readability-check` skill instead.
---

# Metadata check

Reviews short, high-value strings where every character counts — titles, meta descriptions, schema descriptions, FAQ answers, taglines, bios, and social-card copy. Flesch scoring and the nine-category readability rubric don't fit a 5–30 word string; this skill applies the checks that do.

Use this skill for anything in the metadata-string shape. For multi-paragraph prose (blog posts, READMEs, CONTRIBUTING files), use `readability-check` instead.

## What to check

For each string, check these points. Every check is either ✓ (pass), ⚠ (needs work), or ✗ (problem).

- **Front-load the distinguishing word.** The most specific, searchable term sits near the start. "Astro SEO: the definitive guide" beats "The definitive guide to Astro SEO" — the reader's eye hits the topic first.
- **Concrete over abstract.** Names, numbers, specific claims. "Reduce LCP by 40%" beats "Improve performance significantly."
- **Filler and hedging — aggressive.** Every word costs shelf space. Cut *really*, *just*, *very*, *actually*, *basically*, *simply*, *a bit*, *kind of*, *I think*. In metadata these aren't style ticks, they're wasted SERP characters.
- **Active voice unless the object is the subject.** "Audit your GitHub profile" beats "Your GitHub profile can be audited."
- **No title/description duplication.** A meta description that restates the title burns ~60 of 200 characters for nothing. The description should promise what's *inside* the page, not re-announce what it *is*.
- **Difficult words.** Prefer the common synonym unless the domain term is what the user searches for. Between *utilize* and *use*, use *use*. Domain terms the target audience expects are fine (*hydration*, *middleware*, *structured data*).
- **SERP and platform truncation.** Know the limit for the surface:
  - Google SERP: titles clipped around 55–65 characters, descriptions around 155–160.
  - GitHub repo description: ~350 chars, but only the first ~100 show in search results and on profile cards.
  - Twitter/X bio: 160 chars.
  - Open Graph description: usually shown at ~200 chars.
  Anything past the cut should be disposable, not a key promise.
- **One idea per field.** Titles and descriptions that try to promise two things land fuzzy. Pick the sharpest one.

## What to skip

Don't run this skill on:

- URLs, schema `@id` values, filenames, enum values, or any technical identifier.
- Multi-paragraph prose — route that to `readability-check`.
- Strings the user did not write and cannot change (imported content, upstream defaults).

## Output format

Per string, return:

```markdown
### [Field name] — [length] chars

> [The string itself]

- Front-loading: [✓/⚠/✗] [one-line reason if not ✓]
- Concreteness: [✓/⚠/✗] [reason]
- Filler: [✓/⚠/✗] [reason]
- Active voice: [✓/⚠/✗] [reason]
- Duplication: [✓/⚠/✗] [reason]
- Word choice: [✓/⚠/✗] [reason]
- Truncation fit: [✓/⚠/✗] [reason] — platform: [SERP/GitHub/Twitter/OG]
- One idea: [✓/⚠/✗] [reason]

**Rewrite:** [only if any check failed — a concrete replacement string, not a suggestion]
```

Keep the audit tight — metadata feedback should be actionable in seconds, and you're almost always running it across a batch of strings at once. If a string is already clean, don't pad the output; just mark all ✓ and move on.
