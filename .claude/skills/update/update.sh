#!/usr/bin/env bash
#
# Bring a Compound Marketing instance up to date with its starter kit.
#
# Usage (run from the instance root):
#   .claude/skills/update/update.sh plan  [starter-kit-dir]   # pull the kit, show what would change
#   .claude/skills/update/update.sh apply [starter-kit-dir]   # make the changes
#
# Three-way merge per file: base = the kit version this instance was last
# built or updated from, theirs = the kit now, ours = the instance file.
# Files you never touched take the new version. Files you changed get the
# kit's changes merged in. Overlapping edits are written to
# .update-conflicts/ and the original is left alone. Brain content files
# are never modified; new brain files are added.
#
# Output lines: NEW, UPDATED, MERGED, CONFLICT, REMOVED, KEPT, SKIPPED.

# Wrapped in main so bash parses the whole script before running it: an
# update can overwrite this file mid-run.
main() {
  set -euo pipefail
  MODE="${1:-plan}"
  case "$MODE" in plan|apply) ;; *) echo "Usage: $0 plan|apply [starter-kit-dir]" >&2; return 2 ;; esac

  INST="$(pwd)"
  CONFIG="$INST/.compound-marketing.yml"
  [ -f "$CONFIG" ] || { echo "ERROR: run this from your company folder (no .compound-marketing.yml here)." >&2; return 1; }

  yml() { { grep "^$1:" "$CONFIG" || true; } | head -1 | sed "s/^$1:[[:space:]]*//; s/^\"//; s/\"\$//"; }

  KIT="${2:-$(yml starter_kit)}"
  KIT="${KIT:-$(dirname "$INST")/compound-marketing}"
  [ -d "$KIT/.git" ] || { echo "ERROR: starter kit not found at $KIT. Pass its path as the second argument." >&2; return 1; }
  KIT="$(cd "$KIT" && pwd)"

  RUNTIME="$(yml primary_runtime)"; RUNTIME="${RUNTIME:-claude}"
  COMPANY="$(yml company)"
  if [ "$RUNTIME" = "codex" ]; then PRIMARY=".agents/skills"; SECONDARY=".claude/skills"; INSTR="AGENTS.md"; OTHER="CLAUDE.md"
  else PRIMARY=".claude/skills"; SECONDARY=".agents/skills"; INSTR="CLAUDE.md"; OTHER="AGENTS.md"; fi

  if [ "$MODE" = "apply" ] && [ -n "$(git -C "$INST" status --porcelain)" ]; then
    echo "ERROR: your company folder has uncommitted changes. Commit them first so the update can be undone." >&2
    return 1
  fi

  # Get the latest kit. Plan pulls too, so apply uses exactly what plan showed.
  if [ "$MODE" = "plan" ]; then
    git -C "$KIT" pull --ff-only -q || { echo "ERROR: couldn't pull the starter kit at $KIT (local changes?)." >&2; return 1; }
  fi
  HEAD_REV="$(git -C "$KIT" rev-parse HEAD)"

  BASE="$(yml starter_kit_version)"
  if [ -z "$BASE" ] || ! git -C "$KIT" cat-file -e "$BASE^{commit}" 2>/dev/null; then
    # Instances made before versions were recorded: use the kit commit that
    # was current when the instance's first commit was made.
    FIRST="$(git -C "$INST" log --reverse --format=%cI | head -1)"
    BASE="$(git -C "$KIT" rev-list -1 --before="$FIRST" HEAD 2>/dev/null || true)"
    echo "BASE guessed from instance creation date ($FIRST): ${BASE:-none}"
  fi
  echo "FROM ${BASE:-unknown} TO $HEAD_REV"

  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

  # Kit path -> "instance-path mode". Modes: merge, add (add if missing, never modify).
  map() {
    case "$1" in
      .claude/skills/setup/*) ;;
      .claude/skills/*) echo "$PRIMARY/${1#.claude/skills/} merge" ;;
      .claude/settings.json) echo ".claude/settings.json merge" ;;
      templates/CLAUDE.md) echo "$INSTR merge" ;;
      templates/brain/INDEX.md|templates/brain/README.md) echo "brain/${1#templates/brain/} merge" ;;
      templates/brain/*) echo "brain/${1#templates/brain/} add" ;;
      templates/styles/*) echo "styles/${1#templates/styles/} merge" ;;
      templates/README.md|templates/PRODUCT.md|templates/INDEX.md|templates/.vale.ini|templates/.env.example|templates/.gitignore)
        echo "${1#templates/} merge" ;;
    esac
  }

  # Write a kit file at a revision, transformed the way create-instance.sh does.
  render() { # rev kitpath out -> 0 if the file exists at rev
    git -C "$KIT" cat-file -e "$1:$2" 2>/dev/null || return 1
    case "$2" in
      templates/README.md) git -C "$KIT" show "$1:$2" | sed "s/\[COMPANY\]/$COMPANY/g" > "$3" ;;
      templates/CLAUDE.md)
        if [ "$RUNTIME" = "codex" ]; then
          git -C "$KIT" show "$1:$2" | sed '1s/Claude Instructions/Codex Instructions/' | sed 's|/\.claude/skills/|/.agents/skills/|g' > "$3"
        else git -C "$KIT" show "$1:$2" > "$3"; fi ;;
      *) git -C "$KIT" show "$1:$2" > "$3" ;;
    esac
  }

  text() { [ ! -s "$1" ] || grep -Iq . "$1"; }

  { [ -n "$BASE" ] && git -C "$KIT" ls-tree -r --name-only "$BASE"; git -C "$KIT" ls-tree -r --name-only HEAD; } | sort -u |
  while IFS= read -r kp; do
    m="$(map "$kp")"; [ -n "$m" ] || continue
    ip="${m% *}"; mode="${m##* }"; dst="$INST/$ip"
    b="$TMP/base"; t="$TMP/theirs"; rm -f "$b" "$t"
    hb=0; ht=0; ho=0
    [ -n "$BASE" ] && render "$BASE" "$kp" "$b" && hb=1
    render HEAD "$kp" "$t" && ht=1
    [ -f "$dst" ] && ho=1

    if [ "$mode" = "add" ]; then
      if [ $ht = 1 ] && [ $ho = 0 ] && [ $hb = 0 ]; then
        echo "NEW $ip"; [ "$MODE" = "apply" ] && { mkdir -p "$(dirname "$dst")"; cp "$t" "$dst"; }
      fi
      continue
    fi

    if [ $ht = 0 ]; then                                  # removed from the kit
      [ $ho = 1 ] && [ $hb = 1 ] || continue
      if cmp -s "$dst" "$b"; then echo "REMOVED $ip"; [ "$MODE" = "apply" ] && rm "$dst"
      else echo "KEPT $ip (removed from the starter kit, but you changed it)"; fi
    elif [ $ho = 0 ]; then
      if [ $hb = 1 ]; then echo "SKIPPED $ip (you deleted it)"
      else echo "NEW $ip"; [ "$MODE" = "apply" ] && { mkdir -p "$(dirname "$dst")"; cp "$t" "$dst"; }; fi
    elif cmp -s "$dst" "$t"; then
      :                                                    # already current
    elif [ $hb = 1 ] && cmp -s "$dst" "$b"; then
      echo "UPDATED $ip"; [ "$MODE" = "apply" ] && cat "$t" > "$dst"
    elif [ $hb = 1 ] && cmp -s "$t" "$b"; then
      :                                                    # only you changed it
    elif [ $hb = 1 ] && text "$dst" && text "$b" && text "$t" && git merge-file -p "$dst" "$b" "$t" > "$TMP/merged" 2>/dev/null; then
      echo "MERGED $ip"; [ "$MODE" = "apply" ] && cat "$TMP/merged" > "$dst"
    else
      echo "CONFLICT $ip"
      if [ "$MODE" = "apply" ]; then
        c="$INST/.update-conflicts/$ip"; mkdir -p "$(dirname "$c")"
        if [ $hb = 1 ]; then git merge-file -p -L yours -L base -L starter-kit "$dst" "$b" "$t" > "$c" 2>/dev/null || true
        else cp "$t" "$c"; fi
      fi
    fi
    :
  done

  [ "$MODE" = "apply" ] || return 0

  # Secondary instruction file and skills mirror, rebuilt from the primary
  # the same way create-instance.sh builds them.
  if [ "$RUNTIME" = "codex" ]; then
    sed '1s/Codex Instructions/Claude Instructions/' "$INST/$INSTR" | sed 's|/\.agents/skills/|/.claude/skills/|g' > "$INST/$OTHER"
  else
    sed '1s/Claude Instructions/Codex Instructions/' "$INST/$INSTR" | sed 's|/\.claude/skills/|/.agents/skills/|g' > "$INST/$OTHER"
  fi
  rm -rf "$INST/$SECONDARY"; mkdir -p "$INST/$SECONDARY"
  (cd "$INST/$PRIMARY" && find . -type f -not -path './sync-skills/*') | while IFS= read -r f; do
    mkdir -p "$(dirname "$INST/$SECONDARY/$f")"; ln "$INST/$PRIMARY/$f" "$INST/$SECONDARY/$f"
  done

  # Record the new base.
  if grep -q '^starter_kit_version:' "$CONFIG"; then
    sed -i.bak "s|^starter_kit_version:.*|starter_kit_version: $HEAD_REV|" "$CONFIG" && rm -f "$CONFIG.bak"
  else
    printf '\n# Starter kit this folder was built from; /update reads these.\nstarter_kit: "%s"\nstarter_kit_version: %s\n' "$KIT" "$HEAD_REV" >> "$CONFIG"
  fi
  if ! grep -q '^starter_kit:' "$CONFIG"; then printf 'starter_kit: "%s"\n' "$KIT" >> "$CONFIG"; fi
  echo "DONE"
}
main "$@"; exit $?
