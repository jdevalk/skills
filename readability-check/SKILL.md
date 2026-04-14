---
name: readability-check
version: "0.3"
description: >
  Runs a readability audit on a blog post draft, calibrated for readers who read
  English as a second language. Checks nine categories — paragraph structure,
  opening paragraph strength, tiered sentence length, passive voice, difficult
  words, filler and hedging, transitions, variation, and heading hierarchy —
  and reports a Flesch Reading Ease score with a per-category status. Use when
  the user asks to check readability, run a readability pass, or asks "is this
  readable", or proactively as a second pass after a substantial draft is
  complete. Also invoked by the github-repo, github-profile, and
  wp-readme-optimizer skills on their generated prose.
---

# Readability check

Run a readability audit on a blog post draft. Use when the user asks to check readability ("check readability", "readability pass", "is this readable"), or proactively after a substantial draft is complete — as a second pass after the blog-drafting skill's critical read, not during active drafting.

## Check for skill updates

Before running, fetch <https://raw.githubusercontent.com/jdevalk/skills/main/versions.json> and compare the `readability-check` entry to the `version:` in this file's frontmatter. If the manifest version is higher, tell the user this skill is out of date and point them to the [latest release](https://github.com/jdevalk/skills/releases/latest). Continue regardless — the check is informational, not a blocker.

## Audience calibration

Always assume the reader reads English as a second language. That's the default, not a fallback.

In technical posts, the technical sections can use domain terms the audience expects — but any non-technical paragraph (introduction, context, conclusion, transitions, examples, analogies) must be readable by a non-technical L2 reader. Setup and motivation paragraphs carry the post for readers who don't know the domain yet; they're where you lose people.

## What to check

Read the full post, then report on each criterion below. For every issue, quote the specific text, reference its location (section heading or "intro" / "conclusion"), explain the problem, and suggest a concrete fix.

### 1. Paragraph structure

- Every paragraph must lead with its most important sentence. The opening sentence should make sense standalone — this is the unit AI systems extract for answers.
- One idea per paragraph. Break paragraphs that do two things.
- Visual density matters more than a strict sentence count, but flag paragraphs over ~8 sentences or ~120 words.

### 2. Opening paragraph

The first paragraph carries disproportionate weight — it's what AI systems quote and what readers use to decide whether to keep reading. Check specifically:

- Does the first sentence state the point of the post, not just set up context?
- Can the first paragraph stand alone as a summary?
- Is there hedging ("in this post I'll try to...") that can be cut?

### 3. Sentence length

Use tiered thresholds:

- **14–20 words**: normal, no action needed.
- **21–30 words**: long. Flag if a paragraph has more than one.
- **30+ words**: very long. Flag every instance; suggest a split.

Long sentences are especially costly for L2 readers because they have to hold more grammar in working memory. When a long sentence is unavoidable (e.g. a necessary list), check that the sentences around it are short.

### 4. Passive voice

Flag passive constructions ("X was done by Y", "it is recommended that..."). For each:

- If the actor is clear and active voice reads naturally, rewrite.
- Keep passive when the actor is genuinely unknown, irrelevant, or when the object is the real topic of the sentence.
- Flag stacked passives (two in one paragraph) even if each is individually defensible.

### 5. Difficult words

Don't rely on syllable count — it mislabels common words as hard ("information") and simple words as easy ("queue"). Instead, flag a word if:

- A non-technical L2 reader probably wouldn't use it in conversation, **and**
- A more common synonym exists that fits the sentence.

Examples of words to flag when a simpler option works: *utilize* (use), *leverage* (use), *facilitate* (help), *commence* (start), *subsequently* (then), *ascertain* (find out), *endeavor* (try).

Exceptions:

- Domain terms the audience expects ("structured data", "hydration", "middleware") — don't flag in technical sections.
- In non-technical paragraphs of technical posts, apply the strict L2 rule even to mild jargon.

When a difficult word is genuinely necessary, check that the surrounding sentences are short and simple so the reader has processing room.

### 6. Filler and hedging

Flag words that add length without meaning: *really*, *just*, *very*, *actually*, *basically*, *simply*, *in order to* (→ to), *at this point in time* (→ now), *due to the fact that* (→ because). Also flag hedges that weaken claims without reason: *I think*, *sort of*, *kind of*, *it could be argued that*.

### 7. Transition words

- Paragraphs should connect with transitions: *because*, *therefore*, *however*, *for example*, *first*, *in other words*, *as a result*, *that said*.
- Flag sequences of 3+ paragraphs with no transitions.
- Don't over-correct: natural flow counts. Not every paragraph needs an explicit connector.

### 8. Variation

- Flag words or phrases repeated 3+ times within ~200 words (excluding articles, prepositions, domain terms).
- Flag 3+ consecutive paragraphs that open with the same sentence structure (e.g. all starting "You can...").
- Suggest synonyms or restructuring.

### 9. Subheadings and heading hierarchy

- In posts over 1000 words, no prose section should run longer than ~300 words without a subheading.
- Subheadings should be descriptive enough to understand standalone — a reader skimming the table of contents should grasp the post's shape.
- Check heading levels are properly nested (no h2 → h4 jumps).
- Sibling headings should be grammatically parallel (all noun phrases, or all questions, or all imperatives — pick one and stick to it within a section).

## Scoring

Report two things.

**Flesch Reading Ease** (computed: `206.835 − 1.015 × (words/sentences) − 84.6 × (syllables/words)`). Target bands:

- **70+** — plain English, comfortable for L2 readers. Aim here for non-technical posts and for non-technical paragraphs in technical posts.
- **60–70** — standard. Acceptable for technical posts overall, provided non-technical sections score higher.
- **50–60** — fairly difficult. Flag; suggest specific cuts.
- **Below 50** — hard. Needs rework.

Flesch is mechanical and misses paragraph-level issues, but it's an objective anchor. If possible, also report the score for the intro and conclusion separately — those should sit at the top of the target band.

**Per-category status** — for each of the 9 checks above, assign one of:

- ✓ **Pass** — no meaningful issues.
- ⚠ **Needs work** — a few fixable issues; listed below.
- ✗ **Problem** — systemic issue across the post.

## Output format

```markdown
## Readability audit: [post title]

### Score
- Flesch Reading Ease: [n] ([band])
- Intro: [n] · Conclusion: [n]
- Per-category: 1. ✓  2. ⚠  3. ✓  4. ✗  5. ⚠  6. ✓  7. ✓  8. ⚠  9. ✓

### Summary
[One paragraph: overall readability, the one or two biggest issues, and which audience the post currently serves vs. which it should serve.]

### Issues found
[Grouped by category. For each: location, quoted text, why it's a problem, concrete fix.]

### What's working
[Specific sentences, paragraphs, or transitions that read well — quote them. Vague praise ("the intro is fine") doesn't help the writer calibrate; specific praise ("the analogy in the 'Setup' section lands because it bridges to a non-technical reader") does.]
```
