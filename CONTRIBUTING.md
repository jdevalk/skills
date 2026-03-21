# Contributing

Thanks for contributing to this repository.

## Scope

Each top-level skill directory is intended to be a shippable unit. A complete skill may include:

- `SKILL.md`
- `references/`
- `evals/`
- `test-cases/`
- optional helper files such as `assets/` or `scripts/`

Keep changes focused. If you are editing a skill, update its supporting references and evals in the same pull request when needed.

## Local Checks

Run the repo validator before opening a pull request:

```bash
bash .github/scripts/validate-skills.sh
```

Recommended additional checks:

```bash
npx markdownlint-cli2 "**/*.md"
lychee --no-progress "./**/*.md"
```

If you do not have those tools installed locally, rely on GitHub Actions for final verification.

## Authoring Rules

- Keep frontmatter valid YAML with both opening and closing `---` delimiters.
- Match the `name:` field in each `SKILL.md` to the containing directory name.
- Keep referenced files relative to the skill directory and ensure they exist.
- Prefer concrete instructions over generic advice.
- Update eval fixtures when behavior or expected outputs change.

## Pull Requests

- Use a short title that describes the behavioral change.
- Explain what changed and why.
- Note any new references, templates, or release implications.
- Include validation results in the pull request description.

## Releases

Releases are built from this repository's workflow configuration and publish `.skill` archives for each top-level skill directory. Do not rename skill directories casually because release filenames and validation assume stable names.
