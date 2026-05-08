---
name: astro-github-actions
description: |
  Sets up GitHub Actions CI/CD workflows for Astro sites — `astro check` (TypeScript + content schema), ESLint, Prettier, build verification, Vitest testing, Lighthouse CI, link checking, npm audit, and automated deployment to GitHub Pages, Cloudflare Pages, Netlify, or Vercel. ALWAYS use this skill when a user wants to create, add, set up, or configure GitHub Actions, CI/CD, automated checks, or deployment workflows for an Astro site — even if they don't use the exact phrase "GitHub Actions". This includes any request to: add automated type-checking or linting to an Astro repo; set up `astro check` in CI; add Lighthouse or accessibility checks to PRs; configure Vitest in CI for an Astro project; auto-deploy an Astro site to GitHub Pages, Cloudflare Pages, Netlify, or Vercel from GitHub; add link checking or broken-link detection; add security scanning to an Astro pipeline; or generally "add CI", "add automated checks", "set up workflows", or "automate" anything related to an Astro site's GitHub repository. Also trigger when someone wants quality gates on PRs, wants to verify the build still passes, or is setting up a new Astro repo and wants best practices for automation. If the user is inside an Astro project repository and mentions anything about automated testing, code quality, deployment, or GitHub workflows, use this skill.
---

# Astro GitHub Actions

This skill helps you set up a comprehensive CI/CD pipeline for Astro sites using GitHub Actions. The goal is to help authors ship higher-quality sites with less manual effort: type errors caught before merge, broken links flagged, builds verified, and deploys automated.

## What this skill covers

There are several categories of workflows that a healthy Astro project should have. Not every site needs all of them — the right mix depends on whether the project has TypeScript, custom components, content collections, tests, and where it deploys. Your job is to figure out which ones are relevant and set them up.

The workflows fall into these categories:

1. **Type/content checking** — `astro check` (TypeScript + content collection schema validation)
2. **Code quality** — ESLint and Prettier
3. **Build verification** — `astro build` runs cleanly
4. **Testing** — Vitest for unit and component tests
5. **Quality gates** — Lighthouse CI (performance, a11y, SEO, best practices)
6. **Link checking** — broken-link detection on the built site
7. **Security** — npm audit for dependency vulnerabilities
8. **Deployment** — GitHub Pages, Cloudflare Pages, Netlify, or Vercel

Read `references/workflows.md` for the detailed configuration of each workflow, including ready-to-use YAML templates and configuration files.

## How to approach a request

### Step 1: Understand the project

Before writing any workflow files, figure out what you're working with:

- **Is it TypeScript?** Check for `tsconfig.json` and `.ts`/`.astro` files. Almost every Astro project should run `astro check`, but the value is highest when there's TypeScript in `.astro` frontmatter, content collection schemas, or `src/`.
- **Does it use content collections?** Check for `src/content/config.ts` or `src/content.config.ts`. If yes, `astro check` validates the schemas — extra valuable.
- **Does it have tests?** Check for `tests/`, `__tests__/`, `*.test.ts`, or `vitest.config.ts`. If yes, set up the Vitest workflow. If not, mention that adding tests would be valuable but don't force it.
- **What's the package manager?** Look for `pnpm-lock.yaml`, `yarn.lock`, or `package-lock.json`. Match the workflow's install command (`pnpm i --frozen-lockfile`, `yarn install --frozen-lockfile`, or `npm ci`).
- **Where does it deploy?** Look for a `wrangler.toml` (Cloudflare), `netlify.toml` (Netlify), `vercel.json` (Vercel), or just ask. Most hosts have their own GitHub app that auto-deploys without Actions — only set up a deploy workflow if the user actually wants Actions to handle it (typically GitHub Pages or self-hosted).
- **Does it have a build step?** Astro always does (`astro build`) — but verify the script in `package.json` is the standard `astro build` and not something custom.
- **Is it SSR or static?** Check `astro.config.*` for an `output: 'server'` or an adapter import. SSR projects deploy differently (Cloudflare/Netlify/Vercel adapters) and may not be deployable to GitHub Pages at all.

### Step 2: Recommend a set of workflows

Based on what you found, recommend which workflows to set up. A good default for most Astro sites:

- `astro check` (almost always — this is the most valuable check for Astro)
- Build verification (almost always — catches integration regressions `astro check` can miss)
- ESLint + Prettier (if config files exist or the user wants them)
- Lighthouse CI (great for content sites with public URLs)
- Link checker (great for content-heavy sites)
- npm audit (cheap, almost always worth it)

And conditionally:

- Vitest tests (if tests exist)
- Deploy workflow (only if the user wants Actions-driven deploys — most Astro hosts use their own GitHub app)

### Step 3: Create the workflow files

Create each workflow as a separate YAML file in `.github/workflows/`. Using separate files rather than one monolithic workflow gives clearer feedback in PRs (each check shows independently) and makes it easier to enable/disable individual checks.

Use the templates from `references/workflows.md` as starting points, but adapt them to the specific project. Common adaptations include adjusting the package manager, the Node version, the build artifact path, and the deploy target.

### Step 4: Create supporting config files

Depending on which workflows you set up, you may also need:

- `eslint.config.js` — ESLint flat config with `eslint-plugin-astro`
- `.prettierrc` and `.prettierignore` — Prettier config with `prettier-plugin-astro`
- `lighthouserc.json` — Lighthouse CI assertions
- `lychee.toml` — link checker config (if using lychee)
- `vitest.config.ts` — Vitest configuration

### Step 5: Set up secrets reminder

If you're adding a deploy workflow, remind the user which repository secrets are needed:

- **GitHub Pages** — none (uses `GITHUB_TOKEN`)
- **Cloudflare Pages** — `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`
- **Netlify** — `NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID`
- **Vercel** — `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`

Walk them through: Repository Settings > Secrets and variables > Actions > New repository secret.

For Cloudflare, Netlify, and Vercel: also remind them that those platforms ship their own GitHub apps that handle build + deploy + PR previews automatically. Actions-based deploys are usually only worth it when you need to gate the deploy on test results, run a build with secrets the platform doesn't have, or deploy from a path other than the repo root.

## Naming conventions

Use descriptive workflow file names that make it obvious what each one does:

- `astro-check.yml` — `astro check` (type + content schema)
- `lint.yml` — ESLint
- `format.yml` — Prettier check
- `build.yml` — Build verification
- `test.yml` — Vitest
- `lighthouse.yml` — Lighthouse CI
- `links.yml` — Broken link checker
- `security.yml` — npm audit
- `deploy.yml` — Deploy to host

## Important details

**Node.js version**: Astro requires Node 18.20.8+, 20.3.0+, or 22.0.0+. Use Node 22 as the default — it matches Astro's stable target and many adapters are tested against it. Use `actions/checkout@v5` and `actions/setup-node@v5`.

**Package manager detection**: Always match the lockfile. `pnpm-lock.yaml` → use `pnpm/action-setup@v4` and `pnpm install --frozen-lockfile`. `yarn.lock` → `yarn install --frozen-lockfile`. `package-lock.json` → `npm ci`. Don't use `npm install` in CI (non-deterministic, slower).

**Branch naming**: Most Astro repos use `main` as the default branch, but check the actual repo before writing triggers.

**Astro adapters and SSR**: If the project uses `@astrojs/cloudflare`, `@astrojs/netlify`, or `@astrojs/vercel`, the build output may not be a static `dist/` directory. The Cloudflare adapter outputs `dist/` plus a `_worker.js`; Vercel outputs `.vercel/output/`; Netlify outputs `.netlify/`. Adjust deploy artifact paths accordingly.

**`astro check` requires `@astrojs/check` and `typescript`**: Both must be installed. If they're not in `devDependencies`, the workflow will fail. Add them as part of `npm ci` only if they're already in `package.json` — otherwise the workflow should install them explicitly.

**Lighthouse CI on PRs**: Running Lighthouse on every PR catches performance regressions early. The `treosh/lighthouse-ci-action` is the standard. For a public preview URL (Cloudflare Pages, Netlify, Vercel), point Lighthouse at the deploy preview URL — that gives realistic numbers. For internal-only setups, build and serve locally inside the runner.

**Link checking on built output, not source**: Run the link checker on the built `dist/` directory (or against a deployed preview URL) — running it on Markdown source misses generated routes and sitemap links.

**Prefer the platform's GitHub app over Actions deploys**: Cloudflare Pages, Netlify, and Vercel all have first-party GitHub apps that handle PR previews, branch deploys, and rollbacks better than a hand-rolled Action. Recommend the GitHub app first; only suggest an Actions deploy when the user has a specific reason to do it that way.
