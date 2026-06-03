---
name: github-profile
description: >
  Audits and optimizes GitHub profile pages — profile README, metadata fields, pinned repositories,
  stats widgets, and contribution visibility. Use this skill whenever the user asks to improve,
  create, review, or optimize their GitHub profile, or mentions "profile README", "GitHub bio",
  "pinned repos", "GitHub stats", "contribution graph", or "GitHub presence". Also trigger when
  someone says things like "make my GitHub look good", "I want a better GitHub profile",
  "help me stand out on GitHub", "set up my GitHub page", or "optimize my developer profile".
  Works for both personal profiles and organization profile pages.
---

# GitHub Profile Optimizer

This skill audits a GitHub profile and generates an optimized profile README along with recommendations for metadata, pinned repositories, and stats widgets. A strong GitHub profile is a developer's storefront — it shapes perception before anyone reads a line of code.

**Code recipes live in `AGENTS.md`** — read it when you need to implement a specific fix. This file has the workflow and audit checklist.

## Workflow

1. **Gather profile context** — Understand who this person/org is and what they want to showcase
2. **Audit the current profile** — Score every element of the profile's public presence
3. **Generate the profile README** — Write a polished, scannable README.md
4. **Recommend metadata and configuration** — Advise on bio, pinned repos, settings, and widgets
5. **Verify** — Confirm rendering, badge URLs, and summarize next steps

---

## Phase 0: Gather Context

### Determine profile type

Ask the user (if not obvious): is this a **personal profile** or an **organization profile**? The mechanics differ significantly:

| Feature | Personal profile | Organization profile |
| --- | --- | --- |
| README location | `username/username/README.md` | `.github/profile/README.md` |
| Visibility options | Public only | Public + member-only (via `.github-private` repo) |
| Pinned repos | Up to 6 | Up to 6 public + 6 member-only |
| Contribution graph | Yes | No |
| Achievements | Yes | No |

### Collect information

Gather before writing: **username**, current role/company, primary technologies, what they want to showcase, tone (professional/casual/creative/minimal), and target audience (recruiters/collaborators/investors/OSS community).

If `gh` is available (`gh auth status`), pull automatically:

- `gh api user` — name, bio, company, location, blog, twitter
- `gh api users/{username}/repos?sort=stars&per_page=10` — top repos for pin recommendations
- `gh repo view {username}/{username} --json name 2>/dev/null` — check if magic repo exists

---

## Phase 1: Audit

If the user has an existing profile, audit it. If they're starting fresh, skip to Phase 2. Score four categories (each x/10, total x/40):

### Profile README (x/10)

- **Exists?** No `username/username` repo with README.md is the biggest miss.
- **Structure** — Ideal flow: greeting/identity → current work → tech stack (badges) → GitHub stats → featured projects → social links → personal touch.
- **Length** — 400-800 words. Under 200 feels thin; over 2,000 clutters.
- **Scannability** — Gist in 10 seconds? Use `<details>` for collapsible sections.
- **Freshness** — Dynamic content still updating? GitHub stops cron Actions after 60 days of repo inactivity.

### Profile Metadata (x/10)

Every empty field is a missed opportunity:

- **Photo** — clear headshot, consistent across platforms?
- **Bio** — filled in (160 char limit), states role + primary tech + distinguishing trait?
- **Company** — linked with `@` prefix? **Location, Website** — filled in?
- **Social accounts** — Twitter/X, LinkedIn linked? Cross-linking builds trust.
- **Pronouns** — signals inclusivity. **Status** — shows current work or availability?

### Pinned Repositories (x/10)

Up to 6 repos (including contributed-to repos):

- All 6 slots used? Descriptions filled in? Variety across technologies?
- Prioritize repos with stars (social proof) that align with career/business goals.
- Each pinned repo should have a polished README (github-repo skill applies here).

### Contribution Activity (x/10)

- **Graph** — reasonably active? Completely empty raises questions.
- **Private contributions** — "Include private contributions" enabled in settings?
- **Achievements** — Starstruck, Pull Shark, Arctic Code Vault Contributor add credibility.

---

## Phase 2: Generate the Profile README

Based on the audit (or from scratch), produce the profile README. **Read `AGENTS.md` for detailed recipes.**

The profile README should be scannable, personal, and purposeful — every section should serve the person's goals. Adapt tone and structure to the audience.

`AGENTS.md` sections: Personal profile README template, Stats widgets, Badges for tech stack and social links, Dynamic auto-updating content, Organization profile README, Profile generators.

---

## Phase 2.5: Metadata and readability pass

1. **`metadata-check` skill** — run on the GitHub bio (160 chars) and any pinned repo descriptions you rewrote. Front-loading, concreteness, active voice, truncation fit (GitHub shows ~100 chars in profile cards).
2. **`readability-check` skill** — run on the profile README body. Profile READMEs are skimmed; one passive or long sentence stands out.

Apply fixes directly. Focus on: (1) bio / opening README line (disproportionate weight); (2) first sentence of each section (skimming entry point); (3) passive voice (flat in first-person content).

---

## Phase 3: Recommendations

### Metadata to update

Be specific: "Set your bio to: [text, under 160 chars]", "Add these topics to your top repos: [list]", "Set your status to: [suggestion]".

### Pinned repository strategy

Recommend which 6 repos to pin and why — variety across technologies, star count (social proof), README quality, alignment with goals. If pinned repos have weak READMEs, suggest improving those first (github-repo skill).

---

## Phase 4: Verify

- Confirm the README renders correctly (check markdown syntax, badge URLs, image links)
- Check that all shields.io badge URLs are valid (correct logo names, hex colors)
- Verify stats widget URLs use the correct username
- If generating locally, remind the user to create the magic repo (`username/username`) if it doesn't exist, and push the README there
- Summarize next steps: what to commit/push, what to change in GitHub settings manually

---

## Output format

Score table (4 categories, each x/10, total x/40) → Findings grouped by category → Files generated or changed → Next steps (settings changes, repos to pin, manual GitHub config).

---

## Key principles

- **Scannable over comprehensive.** A profile is skimmed in 10 seconds. Cut anything that doesn't earn its space.
- **Personality over template.** Adapt tone, structure, and content to the person's goals and audience. A creative developer and a startup founder need different profiles.
- **Every field filled.** Empty metadata fields, missing pinned repos, and blank descriptions are missed opportunities.
- **Dynamic where it adds value.** A stats image (via `lowlighter/metrics`) and an optional auto-updating blog feed keep a profile fresh — one of each is usually plenty. Avoid third-party-hosted widgets that 502 unpredictably; see `AGENTS.md`.
- **Cross-link everything.** GitHub, LinkedIn, Twitter/X, personal site — each profile should point to the others.
