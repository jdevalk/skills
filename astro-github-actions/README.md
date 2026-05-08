# Astro GitHub Actions

Sets up a comprehensive CI/CD pipeline for Astro sites using GitHub Actions. Covers the full spectrum from type-checking and link verification on pull requests to automated deployment to GitHub Pages, Cloudflare Pages, Netlify, or Vercel -- so site authors can ship higher-quality work with less manual effort.

## What it covers

- **Type/content checking** -- `astro check` validates TypeScript and content collection schemas
- **Code quality** -- ESLint with `eslint-plugin-astro`, Prettier with `prettier-plugin-astro`
- **Build verification** -- `astro build` runs cleanly on every PR, catching integration regressions
- **Testing** -- Vitest for unit and component tests, with optional Astro integration
- **Lighthouse CI** -- performance, accessibility, SEO, and best-practices regression checks
- **Link checking** -- broken-link detection with lychee or linkinator on the built site
- **Security** -- npm audit for dependency vulnerabilities, with a weekly schedule
- **Deployment** -- Actions-driven deploy to GitHub Pages, Cloudflare Pages, Netlify, or Vercel
- **Supporting config** -- generates `eslint.config.js`, `.prettierrc`, `lighthouserc.json`, `lychee.toml`, and `vitest.config.ts` as needed

## Usage

Trigger this skill when you want CI/CD for an Astro site repository. Example prompts:

- "Set up GitHub Actions for my Astro site"
- "Add `astro check` and Lighthouse to CI"
- "I want broken-link checking on every PR"
- "Deploy this Astro site to GitHub Pages from Actions"
- "Set up automated checks for this Astro repo"

The skill inspects your project first -- it detects the package manager, content collections, tests, adapters, and existing config -- then recommends and creates only the workflows that apply.

## Works with

This skill is standalone. It does not chain into other skills, but pairs well with `astro-seo` for SEO setup on the same project.

## Install

```sh
npx skills add jdevalk/skills --skill astro-github-actions
```

## Sources

- [Astro Docs -- Deploy your site](https://docs.astro.build/en/guides/deploy/)
- [`astro check` documentation](https://docs.astro.build/en/reference/cli-reference/#astro-check)
- [treosh/lighthouse-ci-action](https://github.com/treosh/lighthouse-ci-action) -- Lighthouse CI in GitHub Actions
- [lycheeverse/lychee-action](https://github.com/lycheeverse/lychee-action) -- Fast link checker
- [cloudflare/wrangler-action](https://github.com/cloudflare/wrangler-action) -- Cloudflare deploys
- [actions/deploy-pages](https://github.com/actions/deploy-pages) -- GitHub Pages deploys
