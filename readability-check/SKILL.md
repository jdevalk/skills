---
name: readability-check
description: >
  Runs a readability audit on a blog post draft or other multi-paragraph
  prose, calibrated for readers who read English as a second language.
  Checks ten categories — overall structure and topic order, paragraph
  structure, opening paragraph strength, tiered sentence length, passive
  voice, difficult words, filler and hedging, transitions, variation,
  and heading hierarchy — and reports a Flesch Reading Ease score with
  a per-category status.
  Use when the user asks to check readability, run a readability pass,
  or asks "is this readable", or proactively as a second pass after a
  substantial draft is complete. Also invoked by the github-repo,
  github-profile, and wp-readme-optimizer skills on their generated
  prose. For short strings (titles, meta descriptions, taglines, bios),
  use the `metadata-check` skill instead — Flesch and paragraph-level
  checks don't apply to them.
---

# Readability check

Run a readability audit on a blog post draft or other multi-paragraph prose. Use when the user asks to check readability ("check readability", "readability pass", "is this readable"), or proactively after a substantial draft is complete — as a second pass after the blog-drafting skill's critical read, not during active drafting.

For short strings — page titles, meta descriptions, schema `description` fields, FAQ answers, profile bios, repo taglines — use the `metadata-check` skill. Flesch scoring and the ten-category rubric below don't fit a 5–30 word string and will mislead.

For whether a post earns a ranking — search intent fit, keyphrase placement, E-E-A-T, internal linking — chain into the `content-seo` skill after this audit. Readability is a prerequisite for ranking, not a substitute.

## Audience calibration

Always assume the reader reads English as a second language. That's the default, not a fallback.

In technical posts, the technical sections can use domain terms the audience expects — but any non-technical paragraph (introduction, context, conclusion, transitions, examples, analogies) must be readable by a non-technical L2 reader. Setup and motivation paragraphs carry the post for readers who don't know the domain yet; they're where you lose people.

Conversational beats formal. Posts that address the reader directly ("you", "your") and occasionally ask them a question hold L2 readers far better than impersonal prose. Flag long stretches of detached, third-person register in non-technical sections.

## How readers actually read

Readers scan before they commit. They look at the headings, the first paragraph, and the first sentence of each paragraph, and decide from those alone whether to read on. Search engines and AI systems weight the same elements when working out what a text is about. That's why the audit leans hard on those three places: a post whose headings and first sentences carry the argument works for scanners, full readers, and machines at once.

## What to check

Read the full post, then report on each criterion below. For every issue, quote the specific text, reference its location (section heading or "intro" / "conclusion"), explain the problem, and suggest a concrete fix.

### 1. Overall structure and topic order

The post should read as if it was planned before it was written — topics grouped, ordered, and finished one at a time.

- The post should follow one recognizable ordering principle: **thematic** (aspect by aspect), **chronological** (old to new), **didactic** (easy to hard — best for explaining complicated subjects), **problem–solution** (state the problem, then the options), or **inverted pyramid** (most important first, details and background after — best for news and announcements).
- Related topics must sit together. Flag topic ping-pong: a subject discussed, dropped, and picked up again two sections later.
- The skim test: reading only the headings and the first sentence of each paragraph should yield the post's full argument. If a skimmer would miss a key point, it's buried mid-paragraph — surface it.
- The conclusion should restate the core message, using concluding signal words (*so*, *in short*, *the takeaway is*). If the intro opened with a story, question, or statistic, the conclusion should circle back to it — that closes the loop and makes the post feel complete.

### 2. Paragraph structure

A paragraph is a thematic unit, not a visual one. Whitespace placed for looks, with no shift in topic, breaks the reader's map of the text.

- Every paragraph must lead with its most important sentence — the core sentence. The opening sentence should make sense standalone: it's what scanners read and the unit AI systems extract for answers.
- The rest of the paragraph elaborates on that core sentence: supporting sentences that explain, evidence, or add nuance, optionally ending with a concluding or transitional sentence. Longer paragraphs benefit from a final summarizing sentence.
- One idea per paragraph. Break paragraphs that do two things.
- Each paragraph should be complete: say everything about its topic in one place. Flag the inverse of ping-pong — a paragraph break where the next paragraph just continues the same point (the break is aesthetic, not structural).
- Visual density matters more than a strict sentence count, but flag paragraphs over ~8 sentences or ~120 words. An overlong paragraph almost always hides two topics — split it by topic, not at an arbitrary midpoint.
- Mixing lengths is good: a run of identical-length paragraphs reads as monotone. Don't flag a short punchy paragraph between longer ones.

### 3. Opening paragraph

The first paragraph carries disproportionate weight — it's what AI systems quote and what readers use to decide whether to keep reading. There's no room for a print-style teaser that warms up to the point; web readers give you seconds. A good intro does three jobs: states the message, hooks the reader, and sets expectations. Check specifically:

- Does the first sentence state the point of the post, not just set up context?
- Can the first paragraph stand alone as a summary?
- Is there a hook — a question, a surprising fact, a statistic, a short anecdote — that gives the reader a reason to continue? A correct-but-flat opening loses people just as surely as a vague one.
- Does the intro name the problem the reader came with? Readers who recognize their problem in the first lines keep reading to find the solution.
- Does it set expectations — can the reader tell what they'll learn or get by the end?
- Does the post's main topic term appear naturally in the first paragraph? A reader (or search engine) should never have to guess the subject.
- Is there hedging ("in this post I'll try to...") that can be cut?
- Length: at most two short paragraphs (~10–12 sentences total). Longer intros delay the payoff.

Hold the intro to the strictest readability bar in the post: short sentences, active voice, no difficult words. It should be the easiest section to read, not the hardest.

### 4. Sentence length

Use tiered thresholds:

- **14–20 words**: normal, no action needed.
- **21–30 words**: long. Flag if a paragraph has more than one.
- **30+ words**: very long. Flag every instance; suggest a split.

Long sentences are especially costly for L2 readers because they have to hold more grammar in working memory. When a long sentence is unavoidable (e.g. a necessary list), check that the sentences around it are short.

### 5. Passive voice

Flag passive constructions ("X was done by Y", "it is recommended that..."). For each:

- If the actor is clear and active voice reads naturally, rewrite.
- Keep passive when the actor is genuinely unknown, irrelevant, or when the object is the real topic of the sentence.
- Flag stacked passives (two in one paragraph) even if each is individually defensible.

### 6. Difficult words

Don't rely on syllable count — it mislabels common words as hard ("information") and simple words as easy ("queue"). Instead, flag a word if:

- A non-technical L2 reader probably wouldn't use it in conversation, **and**
- A more common synonym exists that fits the sentence.

Examples of words to flag when a simpler option works: *utilize* (use), *leverage* (use), *facilitate* (help), *commence* (start), *subsequently* (then), *ascertain* (find out), *endeavor* (try).

Exceptions:

- Domain terms the audience expects ("structured data", "hydration", "middleware") — don't flag in technical sections.
- In non-technical paragraphs of technical posts, apply the strict L2 rule even to mild jargon.

When a difficult word is genuinely necessary, check that the surrounding sentences are short and simple so the reader has processing room.

### 7. Filler and hedging

Flag words that add length without meaning: *really*, *just*, *very*, *actually*, *basically*, *simply*, *in order to* (→ to), *at this point in time* (→ now), *due to the fact that* (→ because). Also flag hedges that weaken claims without reason: *I think*, *sort of*, *kind of*, *it could be argued that*.

### 8. Transition words

Transitions are the cement between sentences and paragraphs — they tell the reader what relation to expect before they read it. Match the connector to the relation:

- **Enumerating**: *first*, *also*, *in addition*, *another*, *finally*
- **Cause and effect**: *because*, *so*, *since*, *therefore*
- **Comparing or contrasting**: *however*, *rather*, *yet*, *while*, *on the other hand*
- **Concluding**: *as a result*, *hence*, *in short*, *the takeaway is*
- **Emphasizing**: *especially*, *most of all*, *above all*
- **Illustrating**: *for example*, *in other words*, *that said*

Checks:

- Flag sequences of 3+ paragraphs with no transitions.
- Lists, step sequences, and the conclusion need them most — an unsignposted enumeration forces the reader to infer the structure, and a conclusion without concluding words doesn't read as one.
- Don't over-correct: natural flow counts. Not every paragraph needs an explicit connector.

### 9. Variation

- Flag words or phrases repeated 3+ times within ~200 words (excluding articles, prepositions, domain terms).
- Flag 3+ consecutive paragraphs that open with the same sentence structure (e.g. all starting "You can...").
- Suggest synonyms or restructuring.

### 10. Subheadings and heading hierarchy

Writers almost always use too few subheadings, not too many. When in doubt, the fix is to add one.

- In posts over 1000 words, no prose section should run longer than ~300 words without a subheading. Put a heading above every long paragraph or group of thematically similar paragraphs.
- Each heading must accurately cover the content beneath it — a catchy heading that doesn't describe its section misleads scanners and machines alike.
- Subheadings should be descriptive enough to understand standalone — a reader skimming the table of contents should grasp the post's shape.
- Check heading levels are properly nested (no h2 → h4 jumps).
- Sibling headings should be grammatically parallel (all noun phrases, or all questions, or all imperatives — pick one and stick to it within a section).
- For posts over ~1500 words, suggest a table of contents. Landing on a wall of text with no map makes readers hesitant; a TOC gives them a sense of control and a way to jump to what they need.

## Scoring

Report two things.

**Flesch Reading Ease** (computed: `206.835 − 1.015 × (words/sentences) − 84.6 × (syllables/words)`). Target bands:

- **70+** — plain English, comfortable for L2 readers. Aim here for non-technical posts and for non-technical paragraphs in technical posts.
- **60–70** — standard. Acceptable for technical posts overall, provided non-technical sections score higher.
- **50–60** — fairly difficult. Flag; suggest specific cuts.
- **Below 50** — hard. Needs rework.

Flesch is mechanical and misses paragraph-level issues, but it's an objective anchor. If possible, also report the score for the intro and conclusion separately — those should sit at the top of the target band.

**Per-category status** — for each of the 10 checks above, assign one of:

- ✓ **Pass** — no meaningful issues.
- ⚠ **Needs work** — a few fixable issues; listed below.
- ✗ **Problem** — systemic issue across the post.

## Output format

```markdown
## Readability audit: [post title]

### Score
- Flesch Reading Ease: [n] ([band])
- Intro: [n] · Conclusion: [n]
- Per-category: 1. ✓  2. ⚠  3. ✓  4. ✗  5. ⚠  6. ✓  7. ✓  8. ⚠  9. ✓  10. ✓

### Summary
[One paragraph: overall readability, the one or two biggest issues, and which audience the post currently serves vs. which it should serve.]

### Issues found
[Grouped by category. For each: location, quoted text, why it's a problem, concrete fix.]

### What's working
[Specific sentences, paragraphs, or transitions that read well — quote them. Vague praise ("the intro is fine") doesn't help the writer calibrate; specific praise ("the analogy in the 'Setup' section lands because it bridges to a non-technical reader") does.]
```
