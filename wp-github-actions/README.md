# WordPress Plugin GitHub Actions

Sets up a comprehensive CI/CD pipeline for WordPress plugins using GitHub Actions. Covers the full spectrum from code quality checks on pull requests to automated deployment to WordPress.org -- so plugin authors can ship higher-quality code with less manual effort.

## What it covers

- **Code quality** -- WordPress Coding Standards (WPCS/PHPCS) checks with custom rulesets
- **PHP linting** -- syntax error detection across a PHP version matrix (7.4 through 8.3)
- **JS/CSS linting** -- for plugins with frontend assets
- **PHPUnit testing** -- WordPress test library integration with PHP and WP version matrices
- **Static analysis** -- PHPStan with WordPress extensions
- **Security** -- Composer dependency vulnerability scanning
- **PR previews** -- WordPress Playground previews on pull requests
- **Deployment** -- automated deploy to WordPress.org SVN on GitHub release, including `.distignore`
- **Supporting config** -- generates `phpcs.xml.dist`, `phpstan.neon`, and `.distignore` as needed

## Usage

Trigger this skill when you want CI/CD for a WordPress plugin repository. Example prompts:

- "Set up GitHub Actions for my WordPress plugin"
- "Add PHPCS and PHPUnit to CI"
- "I want to stop doing manual SVN deploys"
- "Add Playground previews to my plugin PRs"
- "Set up automated checks for this plugin repo"

The skill inspects your plugin first -- it checks for Composer usage, JS/CSS assets, existing tests, and WordPress.org presence -- then recommends and creates only the workflows that apply.

## Works with

This skill is standalone. It does not chain into other skills.

## Install

```
npx skills add jdevalk/skills --skill wp-github-actions
```
