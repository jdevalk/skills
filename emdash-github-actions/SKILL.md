---
name: emdash-github-actions
description: |
  Sets up GitHub Actions CI/CD workflows for EmDash plugins — TypeScript type-checking, ESLint linting, Vitest testing, npm publishing, and automated releases. ALWAYS use this skill when a user wants to create, add, set up, or configure GitHub Actions, CI/CD, automated checks, or deployment workflows for an EmDash plugin — even if they don't use the exact phrase "GitHub Actions". This includes any request to: add automated type-checking or linting to an EmDash plugin repo; set up testing in CI for a plugin; auto-publish a plugin to npm from GitHub; add security scanning or dependency auditing to a plugin pipeline; or generally "add CI", "add automated checks", "set up workflows", or "automate" anything related to an EmDash plugin's GitHub repository. Also trigger when someone wants quality gates on PRs or is setting up a new EmDash plugin repo and wants best practices for automation. If the user is inside an EmDash plugin repository and mentions anything about automated testing, code quality, deployment, or GitHub workflows, use this skill.
---

# EmDash Plugin GitHub Actions

This skill helps you set up a comprehensive CI/CD pipeline for EmDash plugins using GitHub Actions. EmDash is a full-stack TypeScript CMS based on Astro, so its plugin ecosystem is entirely TypeScript-based.

## What this skill covers

There are several categories of workflows that a healthy EmDash plugin should have. Not every plugin needs all of them — the right mix depends on the plugin's complexity, whether it has a React admin UI, whether it has tests, etc. Your job is to figure out which ones are relevant and set them up.

The workflows fall into these categories:

1. **Type checking** — TypeScript strict mode with emdash peer dependency
2. **Code quality** — ESLint with TypeScript support
3. **Testing** — Vitest or similar TypeScript-native test runner
4. **Security** — npm audit for dependency vulnerabilities
5. **Deployment** — Automated npm publish on tag/release

Read `references/workflows.md` for the detailed configuration of each workflow, including ready-to-use YAML templates and configuration files.

## How to approach a request

### Step 1: Understand the plugin

Before writing any workflow files, figure out what you're working with:

- **What does the plugin do?** Check the `package.json` description and `src/index.ts` exports. EmDash plugins typically hook into `page:metadata`, `page:fragment`, content hooks, or provide admin UI.
- **Does it have a React admin UI?** Check for `.tsx` files or `admin.tsx`. If yes, the type-check needs `@types/react` and `--jsx react-jsx`.
- **Does it have tests?** Check for a `tests/` or `__tests__/` directory, or a `vitest.config.ts`. If yes, set up the test workflow. If not, mention that adding tests would be valuable but don't force it.
- **What are its peer dependencies?** Check `package.json` for `peerDependencies`. EmDash plugins always depend on `emdash` and may depend on `react`, `astro`, etc.
- **Does it use additional npm dependencies?** Check for `dependencies` in `package.json`. If yes, the CI needs an `npm install` step.
- **Is it published to npm?** Check if the package name is scoped (e.g., `@org/emdash-plugin-foo`) and whether it has a `publishConfig`. If yes, the deploy workflow is relevant.

### Step 2: Recommend a set of workflows

Based on what you found, recommend which workflows to set up. A good default for most plugins:

- TypeScript type-check (almost always — this is the most valuable check)
- ESLint (if the plugin has more than a handful of files)
- npm audit (cheap security check, almost always worth it)

And conditionally:

- Vitest tests (if tests exist)
- npm publish (if the plugin is published to npm)

### Step 3: Create the workflow files

Create each workflow as a separate YAML file in `.github/workflows/`. Using separate files rather than one monolithic workflow gives clearer feedback in PRs (each check shows independently) and makes it easier to enable/disable individual checks.

Use the templates from `references/workflows.md` as starting points, but adapt them to the specific plugin. Common adaptations include:

- Adding `@types/react` if the plugin has `.tsx` files
- Adding additional peer dependencies that provide types
- Adjusting file paths for the type-check and lint commands
- Configuring the npm publish scope and access level

### Step 4: Create supporting config files

Depending on which workflows you set up, you may also need:

- `tsconfig.json` — TypeScript configuration (if not already present)
- `eslint.config.js` — ESLint flat config with TypeScript support
- `vitest.config.ts` — Vitest configuration

### Step 5: Set up secrets reminder

If you're adding the npm publish workflow, remind the user that they need to configure a repository secret in GitHub:

- `NPM_TOKEN` — Their npm access token with publish permissions

Walk them through: Repository Settings > Secrets and variables > Actions > New repository secret.

For scoped packages (`@org/package-name`), the token must have access to the organization.

## Naming conventions

Use descriptive workflow file names that make it obvious what each one does:

- `ci.yml` — TypeScript type-checking (the primary CI check)
- `lint.yml` — ESLint
- `test.yml` — Vitest/test runner
- `security.yml` — npm audit
- `publish.yml` — npm publish on release

## Important details

**Node.js version**: Use Node.js 22 as the default. EmDash is built on modern TypeScript and Astro, so there's no need to support older Node versions. Use `actions/checkout@v5` and `actions/setup-node@v5` (v5 runs on Node.js 24 runners, avoiding the Node.js 20 deprecation).

**Peer dependency installation**: EmDash plugins declare `emdash` as a peer dependency. For type-checking in CI, you must explicitly install `emdash` (and `@types/react` if the plugin has `.tsx` files) since peer dependencies aren't auto-installed in a standalone plugin repo.

**The `--skipLibCheck` flag**: Use `--skipLibCheck` when running `tsc` in CI. EmDash and its transitive dependencies may have internal type issues that aren't relevant to the plugin author. `--skipLibCheck` skips checking `.d.ts` files while still fully checking the plugin's own source code.

**The `find` command for file discovery**: Don't use shell globs like `src/**/*.ts` in CI commands — they fail when no files match at a given depth. Use `$(find src -name '*.ts' -o -name '*.tsx')` instead.

**Branch naming**: Most EmDash plugin repos use `main` as the default branch. Always check the actual repo and use the correct branch name in workflow triggers.
