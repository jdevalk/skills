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

```sh
npx skills add jdevalk/skills --skill github-repo
```

## Sources

- Joost de Valk -- [How to create a healthy GitHub repository](https://joost.blog/healthy-github-repository/)
- GitHub Docs -- [About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- GitHub Docs -- [Setting guidelines for repository contributors](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)
- GitHub Docs -- [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- GitHub Docs -- [Configuring issue templates for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- GitHub Docs -- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- GitHub Docs -- [Customizing your repository's social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
