---
name: content-seo
description: >
  Audits a blog post draft or page copy for content-level SEO: search
  intent fit, focus keyphrase placement, E-E-A-T signals (experience,
  expertise, authoritativeness, trustworthiness), helpfulness and
  originality, content freshness, and internal linking. Use when the
  user asks "will this rank", "SEO check this post", "content SEO
  audit", or "optimize this post for search" — or proactively after a
  readability pass on a post that's meant to rank. For how the prose
  reads, use the `readability-check` skill; for titles and meta
  descriptions, use `metadata-check`; for site-wide technical SEO
  (sitemaps, structured data, canonicals), use `astro-seo` or
  `static-seo`.
---

# Content SEO audit

Audit a post or page draft for whether it earns a ranking — not how it reads. This skill covers the content-level questions: does the post match a real search intent, does it use the words searchers use, does it demonstrate experience and trustworthiness, and does it give the searcher a reason to stay.

This is the third pass in the writing-quality chain. Run `readability-check` first (how the prose reads), `metadata-check` on the title and meta description, and this skill on the question of whether the content deserves the click. Technical SEO — sitemaps, structured data, canonicals, performance — belongs to `astro-seo` or `static-seo`.

## Before you audit

You need two facts. If the user hasn't supplied them, derive them and state your assumption — a wrong assumption flagged is better than a silent one:

- **The focus keyphrase**: the exact query this post should rank for, in the words a searcher would type. If the user can't name one, derive the apparent keyphrase from the title and headings — and report that as the first finding, because a post written without a target query usually serves none.
- **The audience and their problem**: who lands on this page and what they were trying to fix when they searched.

The reader decides what quality is, not the writer. Every check below reduces to one question: does this content serve the person who typed the query better than what's already ranking?

## What to check

Read the full post, then report on each criterion below. For every issue, quote the specific text, reference its location, explain the problem, and suggest a concrete fix.

### 1. Search intent fit

Searchers arrive with one of four intents, and the content type must match:

- **Informational** ("how does X work") — wants a guide or explainer, not a product pitch.
- **Commercial investigation** ("best X for Y", "X vs Z") — wants comparison and honest trade-offs.
- **Transactional** ("buy X", "X pricing") — wants a product or category page with a clear path to purchase.
- **Navigational** ("X login", brand names) — wants a specific page; don't intercept it with a blog post.

Checks:

- Name the keyphrase's dominant intent and verify the content type matches. A sales page targeting an informational query loses the visitor before the second paragraph — they wanted an answer, got a pitch.
- Calls-to-action must match the intent. Informational page → soft CTA (related reading, newsletter); transactional page → direct path to the product. Flag a hard sell on an informational post.
- The answer to the searcher's question should appear early, not after 800 words of preamble. A searcher who has to scroll for the answer goes back to the results — and that return is the negative signal that costs rankings.

### 2. Focus keyphrase placement

The keyphrase confirms to the searcher — and to the search engine — that this page answers their query. It should appear naturally in the places both of them weight most:

- The page title and the first paragraph. A searcher should recognize their query within seconds of landing.
- At least one or two headings, where it fits without contortion.
- Several core sentences (the first sentence of a paragraph). In a well-structured post that stays on topic, this happens by itself — if you have to force it, the post has drifted off topic, and that's the real finding.
- Use the searcher's words, not internal jargon. If the audience searches "site speed" and the post says "performance optimization" throughout, the post is invisible to its own audience.

And the inverse checks:

- **Never force it.** If the keyphrase makes a sentence read wrong, the sentence wins. Search engines recognize synonyms and word forms; readers don't forgive stilted prose.
- **Vary it.** Mechanical repetition of the exact phrase reads as stuffing to readers and engines alike. Synonyms and related phrases cover more queries and read better.

### 3. E-E-A-T signals

Search quality raters assess experience, expertise, authoritativeness, and trustworthiness. These aren't abstract virtues — each one is visible (or absent) in the text:

- **Experience**: does the post show first-hand involvement — things only someone who actually did this would know? Real numbers, screenshots of real results, what went wrong, what surprised the author. A post assembled from other posts has none of this, and it shows.
- **Expertise**: is the author identified, with a reason to trust them on this topic? Are claims sourced — linked to reliable references rather than asserted?
- **Authoritativeness**: does the post cite or connect to recognized sources in the field? This is the weakest lever for most sites — if it doesn't apply, say so and weight the other three; don't fake it.
- **Trustworthiness**: is it clear who is responsible for this content and how to reach them? Are claims accurate and current? For YMYL topics — health, money, safety, legal — hold every claim to the strictest standard; an unsourced medical or financial claim is a ✗, not a ⚠.

### 4. Helpfulness and originality

The people-first test: would this post exist if search engines didn't?

- Does the post add something the current top results don't — first-hand data, a sharper angle, a worked example, an honest limitation? A competent rehash of what already ranks gives the searcher no reason to prefer it and gives the engine no reason to rank it.
- Is the answer complete? The searcher should not need to return to the results to finish the job. Flag questions the post raises but doesn't answer, and steps it mentions but doesn't explain.
- Is the reader's problem named explicitly and solved by the end? A post that's *about* a topic but doesn't *resolve* anything serves the writer, not the reader.

### 5. Freshness

- Flag content that will age: version numbers, prices, screenshots of UIs, "last year" / "recently" phrasing, references to current events. Either make them evergreen or date them explicitly so staleness is visible.
- Flag content that has already aged: outdated facts, deprecated tools, superseded advice.
- For time-sensitive topics, recommend a review cadence. A post that's right today and wrong in six months needs a calendar entry, not just a publish button.

### 6. Internal linking and site fit

A post doesn't rank in isolation — it ranks as part of a site:

- The post should link to related content on the same site, especially the cornerstone article for its topic, with descriptive anchor text ("our guide to keyword research", never "click here").
- Related posts should link back. A new post with no inbound internal links is an orphan — flag it and name the existing posts that should link to it, if the user has given you access to the site or its content inventory.
- Check for cannibalization: does an existing post on the same site already target this keyphrase? Two posts competing for one query split their strength; recommend merging, differentiating, or re-targeting one of them.

## Scoring

**Per-category status** — for each of the 6 checks above, assign one of:

- ✓ **Pass** — no meaningful issues.
- ⚠ **Needs work** — a few fixable issues; listed below.
- ✗ **Problem** — systemic issue across the post.

**Overall verdict** — one of three:

- **Ready** — publishes as-is; minor issues only.
- **Fixable** — right content for the query, but the listed issues hold it back.
- **Wrong content for the query** — the intent mismatch or originality gap can't be edited away; the post needs a different angle or a different target keyphrase. Say this plainly when it's true — polishing a post that targets the wrong query wastes the writer's time.

## Output format

```markdown
## Content SEO audit: [post title]

### Target
- Focus keyphrase: [phrase] ([stated by user / derived — assumption])
- Intent: [informational / commercial / transactional / navigational]
- Verdict: [Ready / Fixable / Wrong content for the query]
- Per-category: 1. ✓  2. ⚠  3. ✓  4. ✗  5. ✓  6. ⚠

### Summary
[One paragraph: what query this post serves, how well it serves it, and the one or two changes that would move it most.]

### Issues found
[Grouped by category. For each: location, quoted text, why it's a problem, concrete fix.]

### What's working
[Specific elements that earn the ranking — a genuinely first-hand example, a complete answer placed early, a well-linked cornerstone reference. Quote them so the writer can calibrate.]
```
