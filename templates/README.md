# [COMPANY] Marketing OS

Your company's marketing operations system, powered by AI coding agents. This repo is the single source of truth for your marketing: brand knowledge, skills, workflows, and all generated content.

Works with **Claude Code** and **OpenAI Codex**.

## Getting Started

Open this repo in your AI coding agent and start working:

```bash
cd [this-repo]
claude          # or: codex
```

That's it. The routing table in CLAUDE.md (or AGENTS.md) automatically matches your requests to the right skill. Ask for what you need in plain language.

## Quick Reference

### Common Tasks

| What you want to do | Command |
|---------------------|---------|
| Write a blog post | `/blog` |
| Write landing page copy | `/copywriting` |
| Edit or improve existing copy | `/copy-editing` |
| Create social media posts | `/social-content` |
| Write an email sequence | `/email-sequence` |
| Generate marketing ideas | `/marketing-ideas` |
| Write a case study | `/case-studies` |
| SEO audit or optimization | `/seo-geo` |
| Create ad copy variations | `/ad-creative` |
| Check marketing performance | `/analytics` |

### Workflows (Multi-Step Pipelines)

These orchestrate multiple skills in sequence with approval gates between each stage. Use them when your task spans multiple channels or steps.

| Command | What it does |
|---------|-------------|
| `/wf-blog-distribute` | Write a blog post, clean it up, optimize for SEO, then create social posts and email content |
| `/wf-landing-page` | Build a page end-to-end: copy, design, CRO audit, SEO, structured data, tracking |
| `/wf-campaign-launch` | Plan and execute a multi-channel campaign: strategy, copy, email, social, ads, tracking |
| `/wf-competitive-positioning` | Research competitors, define positioning, build comparison pages, optimize for search |
| `/wf-case-study-pipeline` | Pull meeting notes, draft the case study, distribute across social and email |
| `/wf-repurpose` | Take any existing content and fan it out to social, email, and ads |
| `/wf-seo-sprint` | Audit your SEO, plan a topic cluster, write a batch of optimized posts |
| `/wf-ad-campaign` | Launch paid ads: strategy, creative variations, tracking, test plan |

Every workflow gates on your approval before moving to the next stage. Skip any stage you don't need.

## How It Works

### Brain Files — Your Source of Truth

The `/brain/` directory is the knowledge base that drives everything. All generated content pulls facts, messaging, and positioning from here. If something isn't in the brain, the system uses `[FILL IN]` placeholders instead of making things up.

Key brain files:
- `brain/truth.md` — Verified product facts (the ground truth)
- `brain/positioning-and-messaging.md` — Positioning, messaging, ICP, competitive POV
- `brain/personas.md` — Buyer personas
- `brain/competitive.md` — Competitive landscape
- `brain/brand-guide/brand-guide.md` — Visual brand system

As you learn more about your market, customers, and product, update these files. The better your brain files, the better every skill performs.

### Skills — What Gets the Work Done

Skills are step-by-step frameworks for specific marketing tasks. Each one has intake questions, references, quality checks, and approval gates. The routing table in CLAUDE.md automatically loads the right skill based on what you ask for.

### Agents — Specialist Roles

Six specialist agents handle tasks that benefit from a focused persona:

| Agent | Role |
|-------|------|
| `content-writer` | Blogs, datasheets, whitepapers, case studies |
| `product-marketer` | Positioning, messaging, brain file ownership |
| `seo-specialist` | SEO/GEO strategy and optimization |
| `social-media-manager` | Social content and platform strategy |
| `campaign-manager` | Multi-channel campaign coordination |
| `ppc-specialist` | Paid advertising campaigns |

### Routing — Automatic Skill Selection

You don't need to memorize commands. The system matches your request to the right skill or workflow automatically. Ask in plain language and it routes correctly. Slash commands are shortcuts, not requirements.

## File Structure

```
brain/                  Source of truth (positioning, personas, competitive, brand)
marketing/              All generated content (blog drafts, social posts, reports)
marketing/plans/        Backlog and project plans
incoming/               Drop zone for raw inputs (notes, CSVs, briefs)
.claude/skills/         Marketing skills (Claude Code)
.claude/agents/         Specialist agents (Claude Code)
.agents/skills/         Marketing skills (Codex) — mirrored from .claude/
.agents/agents/         Specialist agents (Codex) — mirrored from .claude/
CLAUDE.md               Routing tables and rules (Claude Code)
AGENTS.md               Routing tables and rules (Codex)
.marketing-os.yml       Runtime configuration
```

## Keeping Skills in Sync

If you edit a skill and use both Claude Code and Codex, run `/sync-skills` to keep the secondary runtime's copy up to date. The `.marketing-os.yml` file records which runtime is primary and governs sync direction.

## Session Workflow

Start each session with `/start` to load context. End with `/brief` to checkpoint your work and push a session summary.

## Tips

- **Fill in brain files over time.** You don't need everything on day one, but it's ideal if you do. Each conversation teaches the system more about your company.
- **Drop files in `/incoming/`.** Raw notes, competitor PDFs, customer transcripts — drop them here and reference them in your requests.
- **Use `/reflect` after a session** to capture what worked and improve skills for next time.
- **Run `/tagore` on any prose** to catch AI writing patterns before publishing.
- **Check `/analytics`** before planning new content — use your real performance data, not guesses.
