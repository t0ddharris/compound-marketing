# Compound Marketing Generator

This is the source repo for Compound Marketing, a distributable system that creates fully configured marketing environments for AI coding agents.

## What This Repo Is

A generator, not a marketing instance. Users clone this repo, run `/setup`, and it scaffolds a new standalone repo for their company with all skills, agents, brain templates, and config. Supports both Claude Code and OpenAI Codex as runtimes.

## Repo Structure

```
.claude/skills/       # Marketing skills (copied to generated repos)
.claude/agents/       # Specialist agents (copied to generated repos)
templates/            # Everything that gets copied into a new instance:
  CLAUDE.md           #   Instance instructions, routing tables, guardrails
  brain/              #   Brain file templates with [FILL IN] placeholders
  styles/             #   Vale linting rules
  PRODUCT.md          #   impeccable skill config
  INDEX.md            #   Master index for the instance
  .vale.ini           #   Vale config
  .env.example        #   API key template
scripts/              # Generator scripts
  create-instance.sh  #   Scaffolds a new repo (called by /setup)
README.md             # Public-facing docs
```

## Dual-Runtime Support

Generated instances support both Claude Code (`.claude/`) and OpenAI Codex (`.agents/`). During `/setup`, users pick a primary runtime. The generator:

- Scaffolds skills into both `.claude/skills/` and `.agents/skills/` (hardlinked)
- Generates both `CLAUDE.md` and `AGENTS.md` (identical except title and path references)
- Writes `.compound-marketing.yml` recording the primary runtime
- Includes a `sync-skills` skill that keeps the secondary in sync after edits

Skills use `SKILL.md` as the entry point, which both runtimes understand. The `sync-skills` skill reads `.compound-marketing.yml` to determine direction (primary → secondary).

## Key Rule

Do not modify files in `templates/` to be company-specific. They must remain generic with `[FILL IN]` placeholders. The `/setup` skill fills them in after copying to the generated repo.

## Working in This Repo

When working here, you are maintaining the generator itself: skills, agents, templates, scripts, and docs. You are not doing marketing work. The routing tables and brain file rules in `templates/CLAUDE.md` apply to generated instances, not here.
