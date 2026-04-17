# EmDash Plugin GitHub Actions

Sets up a comprehensive CI/CD pipeline for EmDash plugins using GitHub Actions. EmDash is a full-stack TypeScript CMS based on Astro, so the skill focuses on TypeScript-native tooling: type-checking, ESLint, Vitest, npm audit, and automated npm publishing.

## What it covers

- **Type checking** -- TypeScript strict mode with `emdash` peer dependency and `--skipLibCheck`
- **Code quality** -- ESLint with TypeScript support via flat config
- **Testing** -- Vitest or similar TypeScript-native test runner
- **Security** -- npm audit for dependency vulnerabilities
- **Deployment** -- automated npm publish on GitHub release/tag
- **Supporting config** -- generates `tsconfig.json`, `eslint.config.js`, and `vitest.config.ts` as needed

## Usage

Trigger this skill when you want CI/CD for an EmDash plugin repository. Example prompts:

- "Set up GitHub Actions for my EmDash plugin"
- "Add CI to this plugin repo"
- "I want automated type-checking and linting on PRs"
- "Set up npm publishing for this EmDash plugin"

The skill inspects your plugin first -- it checks for React admin UI, existing tests, peer dependencies, and npm publishing config -- then recommends and creates only the workflows that apply.

## Works with

This skill is standalone. It does not chain into other skills.

## Install

```
npx skills add jdevalk/skills --skill emdash-github-actions
```
