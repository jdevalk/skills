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
  local required_fields=("name" "description")

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

  for skill in */SKILL.md; do
    validate_skill_frontmatter "$skill"
    validate_skill_references "$skill"

    local skill_dir
    skill_dir="$(dirname "$skill")"

    if [[ -f "${skill_dir}/evals/evals.json" ]]; then
      validate_evals_json "${skill_dir}/evals/evals.json"
    fi

    info "Validated ${skill}"
  done

  exit "$status"
}

main "$@"
