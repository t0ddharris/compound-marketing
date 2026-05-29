#!/usr/bin/env bash
# Granola CLI wrapper — pulls meeting notes via Granola's REST API
# Usage: granola.sh <command> [options]
#
# Commands:
#   list       List recent meeting notes
#   get        Get a specific note by ID
#   pull       Fetch a note and save to /incoming/
#   recent     Show notes from the last N days (default: 7)
#
# Requires: GRANOLA_API_KEY environment variable (starts with grn_)
#           Generate at: Granola desktop app > Settings > API > Create new key

set -euo pipefail

BASE_URL="https://public-api.granola.ai/v1"

# --- Auth -------------------------------------------------------------------

if [[ -z "${GRANOLA_API_KEY:-}" ]]; then
  # Load from project .env
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
  if [[ -f "$PROJECT_ROOT/.env" ]]; then
    GRANOLA_API_KEY="$(grep '^GRANOLA_API_KEY=' "$PROJECT_ROOT/.env" | cut -d'=' -f2- | tr -d '[:space:]')"
  fi
  if [[ -z "${GRANOLA_API_KEY:-}" ]]; then
    echo "Error: GRANOLA_API_KEY not set in .env" >&2
    echo "Generate a key in the Granola desktop app: Settings > API > Create new key" >&2
    echo "Then add it to .env: GRANOLA_API_KEY=grn_your_key_here" >&2
    exit 1
  fi
fi

AUTH_HEADER="Authorization: Bearer $GRANOLA_API_KEY"

# --- Helpers -----------------------------------------------------------------

api_get() {
  local endpoint="$1"
  local response
  local http_code

  response=$(curl -s -w "\n%{http_code}" -H "$AUTH_HEADER" "${BASE_URL}${endpoint}")
  http_code=$(echo "$response" | tail -1)
  body=$(echo "$response" | sed '$d')

  if [[ "$http_code" == "429" ]]; then
    echo "Error: Rate limited. Wait a few seconds and try again." >&2
    exit 1
  elif [[ "$http_code" != "200" ]]; then
    echo "Error: API returned HTTP $http_code" >&2
    echo "$body" >&2
    exit 1
  fi

  echo "$body"
}

format_note_list() {
  # Takes JSON array of notes, outputs a readable table
  echo "$1" | python3 -c "
import json, sys
data = json.load(sys.stdin)
notes = data.get('notes', [])
if not notes:
    print('No notes found.')
    sys.exit(0)
print(f'Found {len(notes)} note(s):')
print()
print(f'{\"ID\":<20} {\"Date\":<12} {\"Title\":<50}')
print('-' * 82)
for n in notes:
    nid = n['id']
    date = n['created_at'][:10]
    title = n.get('title', '(untitled)')[:50]
    print(f'{nid:<20} {date:<12} {title:<50}')
if data.get('hasMore'):
    cursor = data.get('cursor', '')
    print()
    print(f'More notes available. Use --cursor {cursor} to paginate.')
"
}

format_note_detail() {
  # Takes a single note JSON, outputs readable markdown
  echo "$1" | python3 -c "
import json, sys
n = json.load(sys.stdin)
title = n.get('title', '(untitled)')
date = n.get('created_at', '')[:10]
owner = n.get('owner', {})
owner_str = f\"{owner.get('name', '')} <{owner.get('email', '')}>\".strip(' <>')

print(f'# {title}')
print(f'**Date:** {date}')
if owner_str:
    print(f'**Owner:** {owner_str}')

# Calendar event
cal = n.get('calendar_event')
if cal:
    start = cal.get('scheduled_start_time', '')[:16].replace('T', ' ')
    end = cal.get('scheduled_end_time', '')[:16].replace('T', ' ')
    if start:
        print(f'**Scheduled:** {start} to {end.split(\" \")[-1] if end else \"?\"}')

# Attendees
attendees = n.get('attendees', [])
if attendees:
    print()
    print('## Attendees')
    for a in attendees:
        name = a.get('name', '')
        email = a.get('email', '')
        if name and email:
            print(f'- {name} ({email})')
        elif name:
            print(f'- {name}')
        elif email:
            print(f'- {email}')

# Folders
folders = n.get('folder_membership', [])
if folders:
    folder_names = ', '.join(f.get('name', f.get('id', '?')) for f in folders)
    print(f'**Folders:** {folder_names}')

# Summary
summary = n.get('summary_markdown') or n.get('summary_text')
if summary:
    print()
    print('## Summary')
    print(summary)

# Transcript
transcript = n.get('transcript')
if transcript:
    print()
    print('## Transcript')
    for t in transcript:
        speaker = t.get('speaker', {}).get('source', 'unknown')
        label = 'You' if speaker == 'microphone' else 'Other'
        text = t.get('text', '')
        if text.strip():
            print(f'**{label}:** {text}')
"
}

# --- Commands ----------------------------------------------------------------

cmd_list() {
  local page_size=20
  local created_after=""
  local created_before=""
  local cursor=""
  local raw=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --size)       page_size="$2"; shift 2 ;;
      --after)      created_after="$2"; shift 2 ;;
      --before)     created_before="$2"; shift 2 ;;
      --cursor)     cursor="$2"; shift 2 ;;
      --json)       raw=true; shift ;;
      *)            echo "Unknown option: $1" >&2; exit 1 ;;
    esac
  done

  local params="?page_size=${page_size}"
  [[ -n "$created_after" ]]  && params="${params}&created_after=${created_after}"
  [[ -n "$created_before" ]] && params="${params}&created_before=${created_before}"
  [[ -n "$cursor" ]]         && params="${params}&cursor=${cursor}"

  local result
  result=$(api_get "/notes${params}")

  if $raw; then
    echo "$result" | python3 -m json.tool
  else
    format_note_list "$result"
  fi
}

cmd_get() {
  local note_id=""
  local include_transcript=false
  local raw=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --transcript) include_transcript=true; shift ;;
      --json)       raw=true; shift ;;
      *)
        if [[ -z "$note_id" ]]; then
          note_id="$1"; shift
        else
          echo "Unknown option: $1" >&2; exit 1
        fi
        ;;
    esac
  done

  if [[ -z "$note_id" ]]; then
    echo "Usage: granola.sh get <note_id> [--transcript] [--json]" >&2
    exit 1
  fi

  local params=""
  $include_transcript && params="?include=transcript"

  local result
  result=$(api_get "/notes/${note_id}${params}")

  if $raw; then
    echo "$result" | python3 -m json.tool
  else
    format_note_detail "$result"
  fi
}

cmd_pull() {
  local note_id=""
  local include_transcript=true
  local output_dir="incoming"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --no-transcript) include_transcript=false; shift ;;
      --dir)           output_dir="$2"; shift 2 ;;
      *)
        if [[ -z "$note_id" ]]; then
          note_id="$1"; shift
        else
          echo "Unknown option: $1" >&2; exit 1
        fi
        ;;
    esac
  done

  if [[ -z "$note_id" ]]; then
    echo "Usage: granola.sh pull <note_id> [--no-transcript] [--dir PATH]" >&2
    exit 1
  fi

  local params=""
  $include_transcript && params="?include=transcript"

  local result
  result=$(api_get "/notes/${note_id}${params}")

  # Generate filename from title and date
  local filename
  filename=$(echo "$result" | python3 -c "
import json, sys, re
n = json.load(sys.stdin)
title = n.get('title', 'untitled')
date = n.get('created_at', '')[:10]
# Sanitize title for filename
slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')[:60]
print(f'granola-{date}-{slug}.md')
")

  local filepath="${output_dir}/${filename}"
  format_note_detail "$result" > "$filepath"
  echo "Saved to: $filepath"
}

cmd_recent() {
  local days="${1:-7}"
  local after_date
  after_date=$(python3 -c "
from datetime import datetime, timedelta
d = datetime.now() - timedelta(days=$days)
print(d.strftime('%Y-%m-%d'))
")
  echo "Notes from the last $days days (since $after_date):"
  echo
  cmd_list --after "$after_date" --size 30
}

cmd_help() {
  cat <<'HELP'
Granola CLI — Pull meeting notes from Granola

COMMANDS:
  list                 List recent notes
    --size N             Page size (default: 20, max: 30)
    --after DATE         Notes created after DATE (YYYY-MM-DD)
    --before DATE        Notes created before DATE (YYYY-MM-DD)
    --cursor TOKEN       Pagination cursor
    --json               Raw JSON output

  get <note_id>        Get a specific note
    --transcript         Include full transcript
    --json               Raw JSON output

  pull <note_id>       Fetch note and save to /incoming/
    --no-transcript      Exclude transcript
    --dir PATH           Custom output directory

  recent [N]           List notes from last N days (default: 7)

  help                 Show this help

SETUP:
  1. Open Granola desktop > Settings > API > Create new key
  2. Save the key:
     echo 'grn_your_key_here' > ~/.granola-api-key

  Or set the environment variable:
     export GRANOLA_API_KEY=grn_your_key_here

EXAMPLES:
  granola.sh recent              # Last 7 days
  granola.sh recent 30           # Last 30 days
  granola.sh list --after 2026-04-01
  granola.sh get not_ABC123 --transcript
  granola.sh pull not_ABC123     # Save to /incoming/
HELP
}

# --- Main --------------------------------------------------------------------

command="${1:-help}"
shift || true

case "$command" in
  list)    cmd_list "$@" ;;
  get)     cmd_get "$@" ;;
  pull)    cmd_pull "$@" ;;
  recent)  cmd_recent "$@" ;;
  help)    cmd_help ;;
  *)       echo "Unknown command: $command. Run 'granola.sh help' for usage." >&2; exit 1 ;;
esac
