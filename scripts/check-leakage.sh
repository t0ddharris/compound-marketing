#!/usr/bin/env bash
#
# check-leakage.sh — Generator hygiene guard for Compound Marketing.
#
# This repo is a *generator*: it scaffolds marketing environments for arbitrary
# companies. It must stay company-agnostic. Instance-specific values (a specific
# company's brand colors, a person's name, a former employer, session provenance)
# belong in a generated instance's brain files, never in the skills, templates,
# scripts, or docs that ship to everyone.
#
# This script scans .claude/, templates/, scripts/, and README.md for banned
# content and fails (exit 1) with a readable, one-line-per-violation report.
# It also verifies the structural invariant that every skill directory has a
# SKILL.md whose frontmatter `name:` matches its directory name.
#
# Runnable locally:  ./scripts/check-leakage.sh
# Runs in CI:        see .github/workflows/leakage-check.yml
#
# Extending it:
#   - Add a banned string to BANNED_FIXED (matched literally, case-insensitive).
#   - Add a banned regex to BANNED_REGEX (matched with grep -E, case-insensitive).
#   - Add a legitimate exception to ALLOWLIST as "FILE|PATTERN|CONTEXT":
#       FILE     path relative to repo root (exact match on the reported path)
#       PATTERN  the banned pattern this exception covers, or "*" for any pattern
#       CONTEXT  substring that must appear on the matched line (empty = whole file)
#
# Dependency-free: uses grep/awk/sed only (no ripgrep). GNU grep on CI, ugrep or
# BSD grep locally — only portable flags are used.

# Resolve repo root from this script's location so it works from any cwd.
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$ROOT" || exit 2

# Directories/files to scan.
TARGETS=".claude templates scripts README.md"

# This script itself necessarily contains every banned string as data, so it is
# excluded from the scan by basename.
SELF_BASENAME="check-leakage.sh"

# --- Banned patterns -------------------------------------------------------

# Fixed strings (matched literally, case-insensitive).
BANNED_FIXED="
odigos
odiglet
celect
kieran
walmart
tonik
todd
harris
50F6E8
8B55FF
FF7CA9
6A2AFF
0F0F0F
444AD9
0D9488
A39BA0
CBCACB
od-tag
--od-
Banner9
logo_text_white
YwZzzI2srMQ9nLwIixJD16
humanizer
AI threat detection
non-human adversary
"

# Regexes (matched with grep -E, case-insensitive).
# Session provenance like "(Session 3, 2026-01-01)". Anchored on a digit so the
# reflect skill's literal template example "(Session N, YYYY-MM-DD)" does NOT match.
BANNED_REGEX="
\(Session [0-9]
"

# --- Allowlist -------------------------------------------------------------
# Known-legitimate exceptions. Format: FILE|PATTERN|CONTEXT (see header).
ALLOWLIST="
README.md|harris|t0ddharris/compound-marketing
README.md|todd|t0ddharris/compound-marketing
.claude/skills/tagore/SKILL.md|humanizer|
.claude/skills/youtube-thumbnail/SKILL.md|*|Friday Labs
"

# --- Implementation --------------------------------------------------------

VIOL_FILE=$(mktemp)
trap 'rm -f "$VIOL_FILE"' EXIT

# is_allowed FILE PATTERN CONTENT -> return 0 if this match is allowlisted.
# Uses a here-string (not a pipe) so `return` acts on the function, not a subshell.
is_allowed() {
  _file=$1
  _pat=$2
  _content=$3
  while IFS='|' read -r a_file a_pat a_ctx; do
    [ -n "$a_file" ] || continue
    [ "$a_file" = "$_file" ] || continue
    if [ "$a_pat" != "*" ] && [ "$a_pat" != "$_pat" ]; then
      continue
    fi
    if [ -z "$a_ctx" ]; then
      return 0
    fi
    case "$_content" in
      *"$a_ctx"*) return 0 ;;
    esac
  done <<< "$ALLOWLIST"
  return 1
}

# scan_pattern GREP_MODE PATTERN
#   GREP_MODE is "F" (fixed) or "E" (regex).
scan_pattern() {
  _mode=$1
  _pat=$2
  if [ "$_mode" = "F" ]; then
    _flags="-rHnIiF"
  else
    _flags="-rHnIiE"
  fi
  # -e protects patterns beginning with '-'. --exclude skips this script.
  grep $_flags --exclude="$SELF_BASENAME" -e "$_pat" $TARGETS 2>/dev/null \
  | while IFS= read -r match; do
      _f=${match%%:*}
      _rest=${match#*:}
      _ln=${_rest%%:*}
      _content=${_rest#*:}
      if is_allowed "$_f" "$_pat" "$_content"; then
        continue
      fi
      printf "%s:%s: matched '%s'\n" "$_f" "$_ln" "$_pat" >> "$VIOL_FILE"
    done
}

# Content scan.
printf '%s\n' "$BANNED_FIXED" | while IFS= read -r pat; do
  [ -n "$pat" ] || continue
  scan_pattern F "$pat"
done

printf '%s\n' "$BANNED_REGEX" | while IFS= read -r pat; do
  [ -n "$pat" ] || continue
  scan_pattern E "$pat"
done

# Structural check: every directory under .claude/skills/ must have a SKILL.md
# whose frontmatter `name:` matches the directory name.
if [ -d ".claude/skills" ]; then
  for dir in .claude/skills/*/; do
    [ -d "$dir" ] || continue
    skill="${dir}SKILL.md"
    expected=$(basename "$dir")
    if [ ! -f "$skill" ]; then
      printf "%s: missing SKILL.md (expected name: %s)\n" "$dir" "$expected" >> "$VIOL_FILE"
      continue
    fi
    actual=$(awk '
      /^---[[:space:]]*$/ { f++; next }
      f==1 && /^name:/ {
        sub(/^name:[[:space:]]*/, "")
        gsub(/["'"'"']/, "")
        sub(/[[:space:]]+$/, "")
        print
        exit
      }' "$skill")
    if [ -z "$actual" ]; then
      printf "%s: frontmatter has no 'name:' field (expected: %s)\n" "$skill" "$expected" >> "$VIOL_FILE"
    elif [ "$actual" != "$expected" ]; then
      printf "%s: frontmatter name '%s' does not match directory '%s'\n" "$skill" "$actual" "$expected" >> "$VIOL_FILE"
    fi
  done
fi

# --- Report ----------------------------------------------------------------

count=$(wc -l < "$VIOL_FILE" | tr -d '[:space:]')
[ -n "$count" ] || count=0
if [ "$count" -gt 0 ]; then
  cat "$VIOL_FILE"
  echo
  echo "FAIL: $count leakage/hygiene violation(s) found."
  echo "See scripts/check-leakage.sh for the banned-patterns list and allowlist."
  exit 1
fi

echo "clean: no company-specific content or structural issues found."
exit 0
