# Astro GitHub Actions — Workflow Templates

This file contains ready-to-use YAML templates for each workflow type. Adapt paths, Node versions, package manager, and deploy targets to the specific project.

All examples assume `npm` with `package-lock.json`. For `pnpm` or `yarn`, swap the install step (see "Package manager swaps" at the bottom).

## Table of Contents

1. [Astro Check](#1-astro-check)
2. [ESLint](#2-eslint)
3. [Prettier](#3-prettier)
4. [Build Verification](#4-build-verification)
5. [Vitest Testing](#5-vitest-testing)
6. [Lighthouse CI](#6-lighthouse-ci)
7. [Link Checker](#7-link-checker)
8. [npm Security Audit](#8-npm-security-audit)
9. [Deploy](#9-deploy)
10. [Supporting Config Files](#10-supporting-config-files)
11. [Package manager swaps](#11-package-manager-swaps)

---

## 1. Astro Check

The single most valuable check for an Astro project. Runs `astro check`, which type-checks `.astro` frontmatter, validates content collection schemas, and reports unused imports.

**File: `.github/workflows/astro-check.yml`**

```yaml
name: Astro Check

on:
  push:
    branches: [main]
  pull_request:

jobs:
  check:
    name: astro check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npx astro check
```

### Notes

- Requires `@astrojs/check` and `typescript` in `devDependencies`. If they're missing, run `npm install -D @astrojs/check typescript` once locally and commit the result before adding this workflow.
- For a non-TypeScript Astro project (rare), `astro check` still validates `.astro` frontmatter and content collection schemas, so it's still worth running.
- Add `--minimumSeverity error` if you want to ignore warnings.

---

## 2. ESLint

TypeScript- and Astro-aware linting using the `eslint-plugin-astro` plugin.

**File: `.github/workflows/lint.yml`**

```yaml
name: Lint

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    name: ESLint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npx eslint .
```

Requires an `eslint.config.js` file (see Supporting Config Files section).

### Notes

- Use the modern flat config format (`eslint.config.js`). The legacy `.eslintrc` format is deprecated.
- `eslint-plugin-astro` understands `.astro` files; without it, ESLint will skip them or error on the syntax.
- Install `emdash`/peer deps as needed if `typescript-eslint` type-aware rules need to resolve imports.

---

## 3. Prettier

Format checking on PRs. Doesn't auto-fix in CI — fails the check, leaving the author to run `npm run format` locally.

**File: `.github/workflows/format.yml`**

```yaml
name: Format

on:
  push:
    branches: [main]
  pull_request:

jobs:
  format:
    name: Prettier
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npx prettier --check .
```

Requires `prettier-plugin-astro` and a `.prettierrc` (see Supporting Config Files section).

---

## 4. Build Verification

Runs `astro build` to make sure the site still builds. Catches integration issues that `astro check` doesn't (broken imports at runtime, plugin config errors, content collection runtime failures).

**File: `.github/workflows/build.yml`**

```yaml
name: Build

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    name: astro build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run build
      - name: Upload build artifact
        if: github.event_name == 'pull_request'
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 7
```

### Notes

- The `upload-artifact` step lets reviewers download the built site to inspect output. Optional — drop it if you don't need it.
- For SSR builds with `@astrojs/cloudflare`, the artifact path is still `dist/`. For `@astrojs/vercel`, it's `.vercel/output/`. Adjust accordingly.

---

## 5. Vitest Testing

Vitest is the natural test runner for Astro since both use Vite under the hood. Astro provides a Vitest integration via `getViteConfig` (see `astro/config`).

**File: `.github/workflows/test.yml`**

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    name: Vitest
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npx vitest run
```

### With coverage

```yaml
      - run: npx vitest run --coverage
      - name: Upload coverage
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/
```

### Notes

- Vitest auto-discovers `**/*.{test,spec}.{js,ts,jsx,tsx}`.
- For component tests of `.astro` components, you'll need an Astro container or `@astro-build/test-utils`. Plain `vitest run` is fine for testing utilities, content schemas, and TypeScript modules.

---

## 6. Lighthouse CI

Runs Lighthouse against the built site (or a preview URL) and asserts on performance, accessibility, SEO, and best-practices scores. Catches regressions early.

**File: `.github/workflows/lighthouse.yml`**

### Option A: Build and serve locally inside the runner

```yaml
name: Lighthouse

on:
  pull_request:

jobs:
  lighthouse:
    name: Lighthouse CI
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run build
      - name: Run Lighthouse
        uses: treosh/lighthouse-ci-action@v12
        with:
          configPath: ./lighthouserc.json
          uploadArtifacts: true
          temporaryPublicStorage: true
```

### Option B: Run against a deployed preview URL

If you have Cloudflare Pages / Netlify / Vercel preview deploys, point Lighthouse at the preview URL — much more realistic numbers than `localhost`:

```yaml
      - name: Run Lighthouse against preview
        uses: treosh/lighthouse-ci-action@v12
        with:
          urls: |
            ${{ github.event.deployment_status.target_url }}
            ${{ github.event.deployment_status.target_url }}/about
          uploadArtifacts: true
          temporaryPublicStorage: true
```

For Option B, trigger the workflow on `deployment_status` and gate on `success`:

```yaml
on:
  deployment_status:

jobs:
  lighthouse:
    if: github.event.deployment_status.state == 'success'
    runs-on: ubuntu-latest
```

Requires a `lighthouserc.json` (see Supporting Config Files).

---

## 7. Link Checker

Catches broken links in the built site — internal links, external links, anchors, sitemap entries.

**File: `.github/workflows/links.yml`**

### Option A: lychee (recommended — fast, Rust-based)

```yaml
name: Links

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday at 6 AM

jobs:
  links:
    name: Check links
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run build
      - name: lychee
        uses: lycheeverse/lychee-action@v2
        with:
          args: --no-progress --verbose --base ./dist './dist/**/*.html'
          fail: true
```

### Option B: linkinator (Node-based)

```yaml
      - run: npm run build
      - name: linkinator
        run: npx linkinator dist --recurse --silent
```

### Notes

- The weekly `schedule` catches links that *become* dead even when no code changes. Skip it for sites that link mostly internally.
- Use a `lychee.toml` to skip false positives (LinkedIn, Twitter, paywalled domains often reject bots).

---

## 8. npm Security Audit

Scans dependencies for known vulnerabilities. Cheap to run, catches real issues.

**File: `.github/workflows/security.yml`**

```yaml
name: Security

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday at 6 AM

jobs:
  audit:
    name: npm Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
      - run: npm audit --audit-level=high
```

### Notes

- `--audit-level=high` ignores low and moderate severity issues. Adjust to `--audit-level=moderate` or `--audit-level=critical` based on your tolerance.
- The weekly `schedule` catches newly disclosed CVEs without code changes.

---

## 9. Deploy

Most Astro hosts ship a first-party GitHub app that handles build + deploy + PR previews automatically — recommend that route first. Use these workflows only when the user wants Actions-driven deploys (typically GitHub Pages, or when you need to gate deploy on test results).

### Option A: GitHub Pages

GitHub Pages doesn't have its own auto-deploy app, so this is the standard path.

**File: `.github/workflows/deploy.yml`**

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist/

  deploy:
    name: Deploy
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

In `astro.config.mjs`, set `site` and `base` correctly for GitHub Pages — without them, asset URLs break:

```js
export default defineConfig({
  site: 'https://username.github.io',
  base: '/repo-name', // omit if using a custom domain or username.github.io
});
```

### Option B: Cloudflare Pages (Wrangler)

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    permissions:
      contents: read
      deployments: write
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run build
      - name: Publish
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy dist --project-name=PROJECT_NAME
```

Replace `PROJECT_NAME` with the Cloudflare Pages project name. For SSR sites using `@astrojs/cloudflare`, the build artifact already includes the `_worker.js` file alongside `dist/`.

### Option C: Netlify

```yaml
name: Deploy to Netlify

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run build
      - name: Deploy
        uses: nwtgck/actions-netlify@v3
        with:
          publish-dir: dist
          production-branch: main
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "Deploy from GitHub Actions"
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

### Option D: Vercel

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    env:
      VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
      VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
      - run: npm install -g vercel@latest
      - run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}
      - run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}
      - run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

### Required secrets per host

| Host | Secrets |
| --- | --- |
| GitHub Pages | (none — uses `GITHUB_TOKEN`) |
| Cloudflare Pages | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` |
| Netlify | `NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID` |
| Vercel | `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` |

---

## 10. Supporting Config Files

### eslint.config.js

Modern flat config with Astro and TypeScript support:

```js
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import astro from 'eslint-plugin-astro';

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...astro.configs.recommended,
  {
    files: ['**/*.{js,ts,astro}'],
    rules: {
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',
    },
  },
  {
    ignores: ['dist/', '.astro/', 'node_modules/'],
  },
];
```

Install: `npm install -D eslint @eslint/js typescript-eslint eslint-plugin-astro`

### .prettierrc

```json
{
  "plugins": ["prettier-plugin-astro"],
  "overrides": [
    {
      "files": "*.astro",
      "options": { "parser": "astro" }
    }
  ]
}
```

Install: `npm install -D prettier prettier-plugin-astro`

### .prettierignore

```text
dist/
.astro/
node_modules/
package-lock.json
pnpm-lock.yaml
yarn.lock
```

### lighthouserc.json

Lighthouse CI assertions. Adjust thresholds to your project's reality.

```json
{
  "ci": {
    "collect": {
      "staticDistDir": "./dist",
      "url": ["http://localhost/index.html"]
    },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["error", { "minScore": 0.95 }],
        "categories:seo": ["error", { "minScore": 0.95 }],
        "uses-http2": "off",
        "csp-xss": "off"
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

### lychee.toml

Link checker config. Skip noisy false-positives:

```toml
# Cache results between runs
cache = true
max_cache_age = "2d"

# Concurrency
max_concurrency = 8

# Timeouts
timeout = 20

# Skip URLs that reject bots or require auth
exclude = [
  "^https?://(www\\.)?linkedin\\.com",
  "^https?://(www\\.)?twitter\\.com",
  "^https?://(www\\.)?x\\.com",
  "^https?://localhost",
]

# Treat anchors as informational, not errors
include_fragments = true
```

### vitest.config.ts

For a project with Astro integration:

```ts
import { getViteConfig } from 'astro/config';
import { defineConfig } from 'vitest/config';

export default getViteConfig(
  defineConfig({
    test: {
      globals: true,
      environment: 'node',
    },
  })
);
```

For a plain Vitest setup (no Astro container needed):

```ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
  },
});
```

---

## 11. Package manager swaps

The templates above use `npm`. For other package managers, swap the install steps.

### pnpm

```yaml
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: pnpm
      - run: pnpm install --frozen-lockfile
```

### Yarn (classic or berry)

```yaml
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          cache: yarn
      - run: yarn install --frozen-lockfile
```

### Bun

```yaml
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
```

Match the runner script to the package manager too: `npm run build` → `pnpm build` / `yarn build` / `bun run build`. The `npx` calls become `pnpm exec`, `yarn`, or `bunx` respectively.
