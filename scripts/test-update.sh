#!/usr/bin/env bash
#
# End-to-end check for the /update script: build an instance from a copy of
# this repo, edit it, change the starter kit, update, and check the result.
#
# Runnable locally:  ./scripts/test-update.sh
# Runs in CI:        see .github/workflows/leakage-check.yml

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=test@example.com GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=test@example.com
fail() { echo "FAIL: $1" >&2; exit 1; }

# Upstream holds the starter kit; "kit" is the user's clone of it.
mkdir "$T/upstream"
(cd "$ROOT" && git ls-files -z | xargs -0 tar cf -) | tar xf - -C "$T/upstream"
git -C "$T/upstream" init -q -b main && git -C "$T/upstream" add -A && git -C "$T/upstream" commit -qm v1
git clone -q "$T/upstream" "$T/kit"
"$T/kit/scripts/create-instance.sh" Acme "$T/acme" claude > /dev/null
grep -q '^starter_kit_version: [0-9a-f]\{40\}$' "$T/acme/.compound-marketing.yml" || fail "version not recorded"

# The user's edits.
cd "$T/acme"
perl -pi -e 's/^- Read files as-is.*/- Read files as-is, USER EDIT./' .claude/skills/brain-health/SKILL.md
printf '\n- user learning\n' >> .claude/skills/copy-editing/SKILL.md
perl -pi -e 's/^- \*\*Company name:\*\* \[FILL IN\]/- **Company name:** Acme/' brain/truth.md
git commit -qam "user edits"

# Starter kit changes: same line as the user (conflict), elsewhere in an edited
# file (merge), an untouched file (update), new skill, new brain file, and a
# brain template change that must not reach the instance.
cd "$T/upstream"
perl -pi -e 's/^- Read files as-is.*/- Read files as-is, KIT EDIT./' .claude/skills/brain-health/SKILL.md
perl -0pi -e 's/\A(---\n.*?\n---\n)/$1\nKIT INTRO\n/s' .claude/skills/copy-editing/SKILL.md
echo "KIT TAIL" >> .claude/skills/tagore/SKILL.md
mkdir .claude/skills/kit-new && printf -- '---\nname: kit-new\n---\n' > .claude/skills/kit-new/SKILL.md
echo "# New" > templates/brain/kit-new.md
echo "KIT TRUTH" >> templates/brain/truth.md
git add -A && git commit -qm v2

cd "$T/acme"
U=.claude/skills/update/update.sh
PLAN="$($U plan)"
for want in "CONFLICT .claude/skills/brain-health/SKILL.md" "MERGED .claude/skills/copy-editing/SKILL.md" \
            "UPDATED .claude/skills/tagore/SKILL.md" "NEW .claude/skills/kit-new/SKILL.md" "NEW brain/kit-new.md"; do
  echo "$PLAN" | grep -qx "$want" || fail "plan missing: $want"
done
echo "$PLAN" | grep -q "brain/truth.md" && fail "plan touches brain/truth.md"
git diff --quiet || fail "plan modified files"

$U apply > /dev/null
grep -q "USER EDIT" .claude/skills/brain-health/SKILL.md || fail "conflicted file was overwritten"
grep -q "KIT EDIT" .update-conflicts/.claude/skills/brain-health/SKILL.md || fail "conflict copy missing"
grep -q "user learning" .claude/skills/copy-editing/SKILL.md && grep -q "KIT INTRO" .claude/skills/copy-editing/SKILL.md || fail "merge lost a side"
grep -q "KIT TAIL" .claude/skills/tagore/SKILL.md || fail "update not applied"
[ .claude/skills/tagore/SKILL.md -ef .agents/skills/tagore/SKILL.md ] || fail "mirror not hardlinked"
[ -f .agents/skills/kit-new/SKILL.md ] || fail "new skill not mirrored"
grep -q "KIT TRUTH" brain/truth.md && fail "brain content modified"
grep -q "Company name:\*\* Acme" brain/truth.md || fail "brain content lost"
[ -f brain/kit-new.md ] || fail "new brain file not added"
grep -q "^starter_kit_version: $(git -C "$T/kit" rev-parse HEAD)$" .compound-marketing.yml || fail "version not advanced"
[ -d .claude/skills/setup ] && fail "setup skill added to instance"

echo "update: all checks passed"
