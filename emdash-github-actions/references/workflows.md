# EmDash Plugin GitHub Actions — Workflow Templates

This file contains ready-to-use YAML templates for each workflow type. Adapt dependencies, file paths, and configuration to the specific plugin.

## Table of Contents

1. [TypeScript Type-Checking](#1-typescript-type-checking)
2. [ESLint](#2-eslint)
3. [Vitest Testing](#3-vitest-testing)
4. [npm Security Audit](#4-npm-security-audit)
5. [npm Publish](#5-npm-publish)
6. [Supporting Config Files](#6-supporting-config-files)

---

## 1. TypeScript Type-Checking

The most valuable CI check for an EmDash plugin. Runs `tsc --strict` against the plugin's source with the actual `emdash` types installed.

**File: `.github/workflows/ci.yml`**

### Basic plugin (no React admin UI)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  typecheck:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
      - run: npm install emdash typescript
      - run: >
          npx tsc --noEmit
          --strict
          --moduleResolution bundler
          --module esnext
          --target esnext
          --skipLibCheck
          $(find src -name '*.ts')
```

### Plugin with React admin UI (.tsx files)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  typecheck:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
      - run: npm install emdash typescript @types/react
      - run: >
          npx tsc --noEmit
          --strict
          --moduleResolution bundler
          --module esnext
          --target esnext
          --jsx react-jsx
          --skipLibCheck
          $(find src -name '*.ts' -o -name '*.tsx')
```

### Notes on type-checking

- **Always install `emdash`** — it ships `.d.mts` type declarations that `tsc` needs. Without it, every import fails.
- **Add `@types/react`** only if the plugin has `.tsx` files. Check for an `admin.tsx` or similar.
- **Use `--skipLibCheck`** to avoid false positives from emdash's transitive dependencies.
- **Use `--moduleResolution bundler`** because EmDash plugins are consumed by Astro's Vite-based bundler, not Node's module resolver.
- **Use `find` instead of shell globs** — `src/**/*.tsx` fails in CI if no `.tsx` files exist at the glob depth.
- If the plugin has a `tsconfig.json`, you can simplify the command to just `npx tsc --noEmit`.

### Plugin with tsconfig.json

If the plugin has its own `tsconfig.json`, the workflow simplifies to:

```yaml
      - run: npm install emdash typescript @types/react
      - run: npx tsc --noEmit
```

---

## 2. ESLint

TypeScript-aware linting. Uses the modern flat config format.

**File: `.github/workflows/lint.yml`**

```yaml
name: Lint

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    name: ESLint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
      - run: npm install eslint @eslint/js typescript-eslint typescript emdash
      - run: npx eslint src/
```

Requires an `eslint.config.js` file (see Supporting Config Files section).

### Notes on ESLint

- Use `typescript-eslint` for TypeScript-aware rules. It catches issues that `tsc` alone won't flag (unused variables in certain patterns, naming conventions, etc.).
- The flat config format (`eslint.config.js`) is the modern standard — avoid the legacy `.eslintrc` format.
- Install `emdash` so that `typescript-eslint`'s type-aware rules can resolve imports.

---

## 3. Vitest Testing

Vitest is the natural choice for EmDash plugins since it uses the same Vite-based toolchain as Astro/EmDash.

**File: `.github/workflows/test.yml`**

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Vitest
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
      - run: npm ci
      - run: npx vitest run
```

### With coverage reporting

```yaml
      - run: npx vitest run --coverage
      - name: Upload coverage
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/
```

### Notes on testing

- Use `npm ci` (not `npm install`) when the plugin has a `package-lock.json` — it's faster and deterministic.
- If the plugin doesn't have a `package-lock.json`, use `npm install` instead.
- Vitest automatically finds test files matching `**/*.{test,spec}.{ts,tsx}`.
- For plugins that need EmDash's runtime (e.g., testing hooks), you may need to mock the EmDash context. Check if `emdash` provides test utilities.

---

## 4. npm Security Audit

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

### Notes on security scanning

- `--audit-level=high` ignores low and moderate severity issues, reducing noise. Adjust to `--audit-level=moderate` or `--audit-level=critical` based on your tolerance.
- The `schedule` trigger runs weekly to catch newly disclosed CVEs even when no code changes.
- If the plugin has no `dependencies` (only `peerDependencies`), this workflow won't find much — but it's still worth having for when dependencies are added later.

---

## 5. npm Publish

Automatically publishes the plugin to npm when a GitHub release is created.

**File: `.github/workflows/publish.yml`**

### Basic publish on release

```yaml
name: Publish to npm

on:
  release:
    types: [published]

jobs:
  publish:
    name: Publish
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          registry-url: https://registry.npmjs.org
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Scoped package publish

For scoped packages like `@org/emdash-plugin-foo`, add `--access public` (scoped packages default to private):

```yaml
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Publish with build step

If the plugin needs a build step before publishing (e.g., compiling TypeScript to JavaScript):

```yaml
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 22
          registry-url: https://registry.npmjs.org
      - run: npm ci
      - run: npm run build
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Required secrets

Set this in the repository's Settings > Secrets and variables > Actions:

- **`NPM_TOKEN`** — npm access token with publish permissions. Create one at npmjs.com > Access Tokens > Generate New Token > Granular Access Token.

### Notes on npm publish

- **`--provenance`** links the published package to its GitHub source, showing a "Published via GitHub Actions" badge on npmjs.com. Requires the `id-token: write` permission.
- **Version management**: The version in `package.json` must match the release tag. Either update `package.json` before creating the release, or use a tool like `npm version` to bump and tag in one step.
- **Dry run**: Test with `npm publish --dry-run` locally before setting up the workflow.

---

## 6. Supporting Config Files

### tsconfig.json

A TypeScript configuration file for the plugin. Having this in the repo simplifies the CI command and ensures consistent settings between local development and CI.

```json
{
  "compilerOptions": {
    "strict": true,
    "noEmit": true,
    "moduleResolution": "bundler",
    "module": "esnext",
    "target": "esnext",
    "jsx": "react-jsx",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "resolveJsonModule": true
  },
  "include": ["src"]
}
```

Remove the `"jsx": "react-jsx"` line if the plugin has no `.tsx` files.

### eslint.config.js

Modern flat config with TypeScript support:

```js
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["src/**/*.{ts,tsx}"],
    rules: {
      "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
      "@typescript-eslint/no-explicit-any": "warn",
    },
  },
  {
    ignores: ["node_modules/", "dist/"],
  }
);
```

### vitest.config.ts

Vitest configuration for EmDash plugins:

```ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
  },
});
```

### .npmignore

Controls which files are excluded from the npm package. Only needed if you don't use the `files` field in `package.json`:

```text
.claude/
.github/
.git/
tests/
__tests__/
*.test.ts
*.spec.ts
vitest.config.ts
tsconfig.json
eslint.config.js
.eslintrc*
.gitattributes
CONTRIBUTING.md
SECURITY.md
CHANGELOG.md
```

The preferred approach is to use the `"files"` field in `package.json` instead (allowlist rather than denylist):

```json
{
  "files": ["src/"]
}
```
