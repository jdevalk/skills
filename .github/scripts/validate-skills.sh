#!/usr/bin/env bash

set -euo pipefail

status=0

error() {
  local file="$1"
  local message="$2"
  echo "::error file=${file}::${message}"
  status=1
}

info() {
  local message="$1"
  echo "${message}"
}

extract_frontmatter() {
  local skill="$1"
  local closing_line

  if [[ "$(head -n 1 "$skill")" != "---" ]]; then
    error "$skill" "Missing YAML frontmatter opening delimiter"
    return 1
  fi

  closing_line="$(awk 'NR > 1 && /^---$/ { print NR; exit }' "$skill")"
  if [[ -z "$closing_line" ]]; then
    error "$skill" "Missing YAML frontmatter closing delimiter"
    return 1
  fi

  sed -n "2,$((closing_line - 1))p" "$skill"
}

validate_skill_frontmatter() {
  local skill="$1"
  local dir
  local frontmatter
  local required_fields=("name" "description" "version")

  dir="$(dirname "$skill")"
  frontmatter="$(extract_frontmatter "$skill")" || return

  for field in "${required_fields[@]}"; do
    if ! grep -q "^${field}:" <<<"$frontmatter"; then
      error "$skill" "Missing required '${field}' field in frontmatter"
    fi
  done

  local declared_name
  declared_name="$(sed -n 's/^name:[[:space:]]*//p' <<<"$frontmatter" | head -n 1)"
  if [[ -n "$declared_name" && "$declared_name" != "$(basename "$dir")" ]]; then
    error "$skill" "Frontmatter name '${declared_name}' must match directory name '$(basename "$dir")'"
  fi
}

validate_versions_manifest() {
  local manifest="versions.json"

  if [[ ! -f "$manifest" ]]; then
    error "$manifest" "Missing versions.json at repository root"
    return
  fi

  if ! python3 - "$manifest" <<'PY'
import json
import sys
from pathlib import Path

manifest_path = Path(sys.argv[1])

try:
    manifest = json.loads(manifest_path.read_text())
except json.JSONDecodeError as exc:
    print(f"::error file={manifest_path}::Invalid JSON: {exc}")
    sys.exit(1)

if not isinstance(manifest, dict):
    print(f"::error file={manifest_path}::versions.json must be a JSON object")
    sys.exit(1)

skill_dirs = sorted(p.parent.name for p in Path(".").glob("*/SKILL.md"))
errors = []

for skill in skill_dirs:
    skill_md = Path(skill) / "SKILL.md"
    frontmatter_version = None
    in_frontmatter = False
    for line in skill_md.read_text().splitlines():
        if line.strip() == "---":
            if in_frontmatter:
                break
            in_frontmatter = True
            continue
        if in_frontmatter and line.startswith("version:"):
            frontmatter_version = line.split(":", 1)[1].strip().strip('"').strip("'")
            break

    manifest_version = manifest.get(skill)
    if manifest_version is None:
        errors.append(f"::error file={manifest_path}::Skill '{skill}' missing from versions.json")
    elif frontmatter_version and manifest_version != frontmatter_version:
        errors.append(
            f"::error file={skill_md}::Frontmatter version '{frontmatter_version}' does not match versions.json entry '{manifest_version}'"
        )

for extra in sorted(set(manifest) - set(skill_dirs)):
    errors.append(f"::error file={manifest_path}::versions.json references unknown skill '{extra}'")

if errors:
    print("\n".join(errors))
    sys.exit(1)
PY
  then
    status=1
  fi
}

validate_skill_references() {
  local skill="$1"
  local dir

  dir="$(dirname "$skill")"

  while IFS= read -r ref; do
    [[ -n "$ref" ]] || continue
    if [[ ! -e "${dir}/${ref}" ]]; then
      error "$skill" "Referenced file '${ref}' does not exist relative to ${dir}"
    fi
  done < <(grep -oE '(references|evals|test-cases|assets|scripts)/[^` )"]+' "$skill" | sort -u || true)
}

validate_evals_json() {
  local evals_file="$1"
  local skill_dir

  skill_dir="$(basename "$(dirname "$(dirname "$evals_file")")")"

  if ! python3 - "$evals_file" "$skill_dir" <<'PY'
import json
import sys
from pathlib import Path

evals_path = Path(sys.argv[1])
skill_dir = sys.argv[2]

try:
    data = json.loads(evals_path.read_text())
except json.JSONDecodeError as exc:
    print(f"::error file={evals_path}::Invalid JSON: {exc}")
    sys.exit(1)

skill_name = data.get("skill_name")
if skill_name != skill_dir:
    print(
        f"::error file={evals_path}::skill_name must match directory name '{skill_dir}', found '{skill_name}'"
    )
    sys.exit(1)

evals = data.get("evals")
if not isinstance(evals, list) or not evals:
    print(f"::error file={evals_path}::evals must be a non-empty array")
    sys.exit(1)
PY
  then
    status=1
  fi
}

main() {
  shopt -s nullglob
  local skill

  validate_versions_manifest

  for skill in */SKILL.md; do
    local before=$status
    validate_skill_frontmatter "$skill"
    validate_skill_references "$skill"

    local skill_dir
    skill_dir="$(dirname "$skill")"

    if [[ -f "${skill_dir}/evals/evals.json" ]]; then
      validate_evals_json "${skill_dir}/evals/evals.json"
    fi

    if [[ $status -eq $before ]]; then
      info "Validated ${skill}"
    fi
  done

  exit "$status"
}

main "$@"
