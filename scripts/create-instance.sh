#!/usr/bin/env bash
#
# Create a new standalone Marketing OS instance.
#
# Usage:
#   ./scripts/create-instance.sh "Company Name" [target-dir] [runtime]   (non-interactive, called by /setup)
#   ./scripts/create-instance.sh                                          (interactive)
#
# runtime: claude (default), codex, or both

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATES="$REPO_ROOT/templates"
PARENT_DIR="$(dirname "$REPO_ROOT")"

# --- Get company name (from arg or prompt) ---
if [ $# -ge 1 ]; then
  COMPANY="$1"
else
  echo ""
  echo "  Marketing OS Setup"
  echo "  ─────────────────────────"
  echo ""
  read -p "  Company name: " COMPANY
  if [ -z "$COMPANY" ]; then
    echo "  Company name is required."
    exit 1
  fi
fi

COMPANY_SLUG="$(echo "$COMPANY" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')"
DEFAULT_DIR="$PARENT_DIR/${COMPANY_SLUG}-marketing"

# --- Get target dir (from arg or prompt or default) ---
if [ $# -ge 2 ]; then
  TARGET="$2"
elif [ $# -ge 1 ]; then
  TARGET="$DEFAULT_DIR"
else
  echo ""
  read -p "  Where should I create it? [$DEFAULT_DIR] " TARGET
  TARGET="${TARGET:-$DEFAULT_DIR}"
fi

# --- Get runtime preference (from arg or prompt or default) ---
if [ $# -ge 3 ]; then
  RUNTIME="$3"
elif [ $# -ge 1 ]; then
  RUNTIME="claude"
else
  echo ""
  echo "  Which AI runtime is your primary?"
  echo "    1) claude  (Claude Code — default)"
  echo "    2) codex   (OpenAI Codex)"
  echo "    3) both    (scaffold both, pick primary later)"
  read -p "  Choice [1]: " runtime_choice
  case "$runtime_choice" in
    2|codex)  RUNTIME="codex" ;;
    3|both)   RUNTIME="both" ;;
    *)        RUNTIME="claude" ;;
  esac
fi

# Normalize
case "$RUNTIME" in
  claude|codex|both) ;;
  *) RUNTIME="claude" ;;
esac

if [ -d "$TARGET" ]; then
  echo "  Directory already exists: $TARGET"
  if [ $# -ge 1 ]; then
    echo "  Overwriting (called non-interactively)."
    rm -rf "$TARGET"
  else
    read -p "  Overwrite? (y/N) " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || exit 1
    rm -rf "$TARGET"
  fi
fi

echo "  Creating $COMPANY marketing OS at $TARGET..."
echo "  Primary runtime: $RUNTIME"

# --- Determine primary/secondary directories ---
if [ "$RUNTIME" = "codex" ]; then
  PRIMARY_SKILLS_DIR=".agents/skills"
  SECONDARY_SKILLS_DIR=".claude/skills"
else
  PRIMARY_SKILLS_DIR=".claude/skills"
  SECONDARY_SKILLS_DIR=".agents/skills"
fi

# --- Directory structure ---
mkdir -p "$TARGET"/{brain/brand-guide,marketing/plans,incoming}
mkdir -p "$TARGET"/styles/{Brand,config/vocabularies/Brand}
mkdir -p "$TARGET/.claude" "$TARGET/.agents"

# --- Skills into primary runtime directory ---
cp -R "$REPO_ROOT/.claude/skills" "$TARGET/$PRIMARY_SKILLS_DIR"
rm -rf "$TARGET/$PRIMARY_SKILLS_DIR/setup"

# --- Agents into both runtime directories (hardlinked) ---
cp -R "$REPO_ROOT/.claude/agents" "$TARGET/.claude/agents"
mkdir -p "$TARGET/.agents/agents"
for f in "$TARGET/.claude/agents/"*; do
  [ -f "$f" ] && ln "$f" "$TARGET/.agents/agents/$(basename "$f")"
done

# --- Mirror skills to secondary runtime via hardlinks ---
mkdir -p "$TARGET/$SECONDARY_SKILLS_DIR"
cd "$TARGET/$PRIMARY_SKILLS_DIR"
find . -type f -not -path './sync-skills/*' | while read -r f; do
  dst_file="$TARGET/$SECONDARY_SKILLS_DIR/$f"
  mkdir -p "$(dirname "$dst_file")"
  ln "$TARGET/$PRIMARY_SKILLS_DIR/$f" "$dst_file"
done
cd "$REPO_ROOT"

# --- Settings ---
if [ "$RUNTIME" = "codex" ] || [ "$RUNTIME" = "both" ]; then
  cp "$REPO_ROOT/.claude/settings.json" "$TARGET/.claude/settings.json" 2>/dev/null || true
else
  cp "$REPO_ROOT/.claude/settings.json" "$TARGET/.claude/settings.json"
fi

# --- Brain templates ---
cp "$TEMPLATES"/brain/*.md "$TARGET/brain/"
cp -R "$TEMPLATES/brain/brand-guide" "$TARGET/brain/"

# --- Primary instruction file ---
if [ "$RUNTIME" = "codex" ]; then
  # Generate AGENTS.md as primary from CLAUDE.md template
  sed '1s/Claude Instructions/Codex Instructions/' "$TEMPLATES/CLAUDE.md" \
    | sed 's|/\.claude/skills/|/.agents/skills/|g' \
    | sed 's|/\.claude/agents/|/.agents/agents/|g' \
    > "$TARGET/AGENTS.md"
  # Generate CLAUDE.md as secondary (copy of primary with title swapped back)
  sed '1s/Codex Instructions/Claude Instructions/' "$TARGET/AGENTS.md" \
    | sed 's|/\.agents/skills/|/.claude/skills/|g' \
    | sed 's|/\.agents/agents/|/.claude/agents/|g' \
    > "$TARGET/CLAUDE.md"
else
  # Claude primary — copy template directly
  cp "$TEMPLATES/CLAUDE.md" "$TARGET/CLAUDE.md"
  # Generate AGENTS.md as secondary
  sed '1s/Claude Instructions/Codex Instructions/' "$TARGET/CLAUDE.md" \
    | sed 's|/\.claude/skills/|/.agents/skills/|g' \
    | sed 's|/\.claude/agents/|/.agents/agents/|g' \
    > "$TARGET/AGENTS.md"
fi

# --- Other root config files ---
sed "s/\[COMPANY\]/$COMPANY/g" "$TEMPLATES/README.md" > "$TARGET/README.md"
cp "$TEMPLATES/PRODUCT.md" "$TARGET/PRODUCT.md"
cp "$TEMPLATES/INDEX.md" "$TARGET/INDEX.md"
cp "$TEMPLATES/.vale.ini" "$TARGET/.vale.ini"
cp "$TEMPLATES/.env.example" "$TARGET/.env.example" 2>/dev/null || true
cp "$REPO_ROOT/.gitignore" "$TARGET/.gitignore" 2>/dev/null || true

# --- Runtime config ---
# "both" defaults to claude as primary for sync direction
CONFIG_PRIMARY="$RUNTIME"
if [ "$CONFIG_PRIMARY" = "both" ]; then
  CONFIG_PRIMARY="claude"
fi
cat > "$TARGET/.marketing-os.yml" <<EOF
# Marketing OS runtime configuration
# Generated by create-instance.sh

primary_runtime: $CONFIG_PRIMARY
company: "$COMPANY"
EOF

# --- Vale styles ---
cp "$TEMPLATES"/styles/Brand/*.yml "$TARGET/styles/Brand/"
cp "$TEMPLATES"/styles/config/vocabularies/Brand/* "$TARGET/styles/config/vocabularies/Brand/"

# --- Placeholders ---
touch "$TARGET/marketing/.gitkeep" "$TARGET/marketing/plans/.gitkeep" "$TARGET/incoming/.gitkeep"

# --- Init git ---
cd "$TARGET"
git init -q
git add -A
git commit -q -m "Initial setup: $COMPANY marketing OS"

# --- Output the path for the calling skill to use ---
echo "CREATED:$TARGET"
