# Content SEO

Audits a blog post draft or page copy for whether it earns a ranking -- not how it reads. Covers the content-level layer between writing quality and technical SEO: search intent, keyphrase placement, E-E-A-T, helpfulness, freshness, and internal linking. Reports a per-category status, an overall verdict, and quoted issues with concrete fixes.

## What it checks

- **Search intent fit** -- content type matches the query's intent (informational, commercial, transactional, navigational), CTAs match the intent, the answer appears early
- **Focus keyphrase placement** -- in the title, first paragraph, headings, and core sentences, using the searcher's words; varied naturally, never forced
- **E-E-A-T signals** -- first-hand experience visible in the text, author expertise stated and sourced, trust elements present, YMYL claims held to the strictest standard
- **Helpfulness and originality** -- adds something the current top results don't, answers the question completely, names and solves the reader's problem
- **Freshness** -- flags content that will age or already has, recommends a review cadence for time-sensitive topics
- **Internal linking and site fit** -- links to and from related posts and the cornerstone article, descriptive anchors, no keyphrase cannibalization

The verdict is three-way: ready, fixable, or wrong content for the query -- because an intent mismatch can't be edited away.

## Usage

Trigger this skill when you want a content-level SEO pass on a draft. Example prompts:

- "Will this post rank?"
- "SEO check this post"
- "Run a content SEO audit on this draft"
- "Optimize this post for search"

Give it the focus keyphrase and the intended audience if you can; if you don't, it derives the apparent keyphrase from the title and headings and flags the assumption.

## Works with

This skill is the third pass in the writing-quality chain:

- **readability-check** -- run first, for how the prose reads
- **metadata-check** -- for the page title and meta description
- **astro-seo** / **static-seo** -- for site-wide technical SEO (sitemaps, structured data, canonicals)

## Install

```sh
npx skills add jdevalk/skills --skill content-seo
```

## Sources

- Google -- [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- Google -- [Search Quality Rater Guidelines (E-E-A-T)](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t)
- Yoast -- [SEO copywriting](https://yoast.com/complete-guide-seo-copywriting/)
