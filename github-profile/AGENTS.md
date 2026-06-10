# GitHub Profile — Implementation recipes

Detailed code recipes for Phase 2 (Generate the Profile README). Read this file when you need to implement a specific fix flagged by the audit. The parent `SKILL.md` has the workflow and audit checklist.

## Personal profile README template

Create the `username/username` repo's `README.md`. The structure below is a starting point — adapt it to the person's tone and goals. A creative developer might want something playful. A startup founder might want something that signals credibility. A junior developer might emphasize learning and growth. Don't be afraid to deviate — personality matters more than structure.

```markdown
# Hi, I'm [Name] [optional wave emoji]

[One-liner about what you do and what drives you. This is the hook.]

## What I'm working on

[2-3 sentences about current projects, company, or focus areas.]

## Tech stack

[Badges using shields.io, e.g.:]
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)

## GitHub stats

[Stats cards — see widget section below]

## Featured projects

[Brief descriptions of 2-3 key projects with links, if they want to highlight beyond pins]

## Connect with me

[Badge-style links to email, Twitter/X, LinkedIn, blog]
```

## Stats widgets

Default recommendation: **lowlighter/metrics**. It runs as a GitHub Action in the user's magic repo, renders an SVG, and commits it back. The README then serves a static file straight from GitHub — nothing to rate-limit, nothing to 502.

The third-party-hosted alternatives (github-readme-stats, streak-stats, trophies) all run on shared Vercel infrastructure that regularly hits the GitHub API rate limit. They go down for hours at a time, leaving broken images on the profile. Only suggest them if the user specifically asks, and warn about the reliability problem.

### lowlighter/metrics (recommended)

Add `.github/workflows/metrics.yml` to the magic repo:

```yaml
name: Metrics

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
  push:
    branches: [main]
    paths: [.github/workflows/metrics.yml]

permissions:
  contents: write

jobs:
  github-metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: lowlighter/metrics@latest
        with:
          token: ${{ secrets.METRICS_TOKEN }}
          user: {username}
          template: classic
          base: header, activity, community, repositories, metadata
          plugin_languages: yes
          plugin_languages_details: bytes-size, percentage
          plugin_languages_limit: 6
          plugin_isocalendar: yes
          plugin_isocalendar_duration: half-year
```

Reference the generated SVG in the README:

```markdown
![Metrics](./github-metrics.svg)
```

User-side setup:

1. Create a PAT at <https://github.com/settings/tokens/new> with `public_repo` and `read:user` scopes
2. Add it as a repo secret named `METRICS_TOKEN` (`gh secret set METRICS_TOKEN --repo {username}/{username}`)
3. Push the workflow — the first run commits `github-metrics.svg` back to the repo

Useful additional plugins beyond the defaults: `plugin_followup` (issues/PRs ratio), `plugin_topics` (repo topics word cloud), `plugin_lines` (lines of code), `plugin_traffic` (repo views — needs `repo` scope, not just `public_repo`). Full list: <https://github.com/lowlighter/metrics/blob/master/source/plugins/README.md>

### Third-party-hosted alternatives (use with caution)

These services 502 frequently. Only suggest if the user asks for them directly.

- **github-readme-stats** (anuraghazra) — `https://github-readme-stats.vercel.app/api?username={username}` and `/api/top-langs/?username={username}`. 30+ themes. Can be self-hosted on Vercel with a personal token to avoid the shared rate limit.
- **github-readme-streak-stats** (DenverCoder1) — `https://streak-stats.demolab.com/?user={username}`. Same shared-infra reliability problem.
- **github-profile-trophy** (ryo-ma) — `https://github-profile-trophy.vercel.app/?username={username}&no-frame=true&row=1`. Same shared-infra reliability problem.

## Badges for tech stack and social links

Use **shields.io** combined with **Simple Icons** (3,000+ brand logos):

```text
https://img.shields.io/badge/-{Label}-{Color}?style={style}&logo={logo}&logoColor=white
```

Styles: `flat`, `flat-square`, `plastic`, `for-the-badge`, `social`

For social links, wrap badges in links:

```markdown
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/{handle})
[![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=flat-square&logo=twitter&logoColor=white)](https://twitter.com/{handle})
```

## Dynamic auto-updating content

Optional — requires GitHub Actions. If the person blogs or creates content, suggest these:

- **blog-post-workflow** (gautamkrishnar) — Auto-pulls latest posts from RSS feeds into the README. Uses HTML comment placeholders. Needs a scheduled GitHub Action (daily cron).
- **waka-readme-stats** — Coding time metrics from WakaTime.

Remind them: GitHub stops cron triggers after 60 days of repo inactivity. The blog-post-workflow includes a keepalive feature; others may not.

## Organization profile README

Create `.github/profile/README.md` in the org's `.github` repo.

Organization profile READMEs should be more structured and less personal:

- What the organization does
- Key products or projects (with links to repos)
- How to get involved (contributing, jobs, community)
- Contact and social links

Optionally, create a `.github-private/profile/README.md` for member-only content:

- Internal resources and onboarding links
- Private repo directory
- Team information

Remind the user to **verify their organization's domain** (Settings → Verified & approved domains) for the verified badge.

## Profile generators

If the user wants a faster path, mention these tools:

- **GPRM** (gprm.itsvg.in) — No-code generator with 300+ tech icons
- **rahuldkjain's generator** — Popular fill-in-the-blanks tool
- **readme.so** — Drag-and-drop editor for both profile and project READMEs

Recommendation: start with a generator, then customize to add personality and remove boilerplate.
