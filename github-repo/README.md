# GitHub Repository Optimizer

Audits a GitHub repository against best practices and generates or improves the files that make a repo look professional, welcoming, and well-maintained. Works with live repos via `gh` CLI, local git directories, or files you provide directly.

## What it checks

- **README quality** -- structure, badge row, one-liner description, quick start, code examples, visual demo
- **Repository metadata** -- name, description, topics/tags, website URL, social preview image
- **Community health files** -- CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md, LICENSE, SUPPORT.md, CHANGELOG.md
- **Issue and PR templates** -- YAML-based issue forms, PR template with checklists, CODEOWNERS
- **CI/CD and automation** -- GitHub Actions workflows, Dependabot, code quality actions, stale issue management
- **Releases and branch hygiene** -- tagged releases, semantic versioning, stale branch cleanup, `.gitattributes`

## Usage

Trigger this skill when you want to improve a GitHub repository's public-facing quality. Example prompts:

- "Audit this repo"
- "Make my repo look professional"
- "Add contributing guidelines and issue templates"
- "Prepare this repo for open source"
- "Set up community health files"

The skill also handles organization-level setup -- creating a `.github` repo with default health files that apply across all org repos.

## Works with

- **metadata-check** -- automatically invoked on the repo description and README tagline
- **readability-check** -- automatically invoked on generated prose (README, CONTRIBUTING.md, SECURITY.md)

## Install

```
npx skills add jdevalk/skills --skill github-repo
```
