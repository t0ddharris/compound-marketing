<p align="center">
  <img src="github-social.png" alt="Compound Marketing">
</p>

# Compound Marketing

**Each unit of marketing work should make the next one easier.**

Compound Marketing is built primarily for B2B marketers and GTM teams — more reach without sacrificing quality. It does three things:

- **Automates** repetitive production work through skills and workflows.
- **Speeds up** the work you already do.
- **Extends** into specialties you'd otherwise outsource or skip.

What makes it compound: skills capture how you do the work, workflows chain those skills into full pipelines, and a "brain" holds your company's positioning, personas, and brand. Every correction you make and every session you close feeds back into the system — so the hundredth blog post starts from everything the first ninety-nine taught it. The approach borrows from [compound engineering](https://github.com/EveryInc/compound-engineering-plugin), applied to marketing.

Everything is moldable. You do not need to use the specialist sub-agents. Feel free to work with your main agent to customize the workflows and skills to your own processes and styles. Trim what you don't need, modify what you want, add what you're missing!

Works with **Claude Code** and **OpenAI Codex**.

## Getting Started

**Prerequisites:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or [OpenAI Codex](https://openai.com/codex). Optional: [Vale](https://vale.sh/) for content linting, [GitHub CLI](https://cli.github.com/) (`gh`) for PR workflows.

### 1. Clone and scaffold

```bash
git clone https://github.com/t0ddharris/compound-marketing.git compound-marketing
cd compound-marketing
./scripts/create-instance.sh
```

This asks for your company name and creates a standalone repo (e.g., `../your-company-marketing/`) with all skills, agents, and brain templates.

### 2. Run setup

```bash
cd ../your-company-marketing
claude          # or: codex
/setup
```

`/setup` is a guided walkthrough. It will:

- Ask about your product, target customer, and category
- Scrape your website (optional) to pull in messaging and features automatically
- Build a starter positioning statement and buyer personas
- Extract your brand colors and fonts from your site (optional)
- Set up integrations (HubSpot, LinkedIn, Google AI Studio, etc.)

You don't need perfect answers. Anything you skip stays as a `[FILL IN]` placeholder that you can complete later.

### 3. Bring your own docs (optional)

Already have messaging frameworks, product overviews, brand guidelines, or competitive research? Drop them in the `incoming/` folder before or during setup:

```bash
cp ~/Documents/our-messaging.pdf incoming/
cp ~/Documents/brand-guide.pdf incoming/
```

`/setup` will ask if you have reference files in `incoming/` and use the content to pre-fill your brain files (with your approval before writing anything). Supports PDFs, Markdown, plain text, and images. This can save significant manual entry.

### 4. Start working

Once setup finishes, you're ready to go. Ask for what you need in plain language, or use a slash command:

```
/blog              Write a blog post
/social-content    Draft LinkedIn or X posts
/wf-landing-page   Build a landing page, end to end
```

## How It Works

Compound Marketing has four layers, each fixing a way AI marketing usually goes wrong:

- **Brain** (`brain/`) — One source of truth for your company. Every factual claim traces back to a brain file. If a fact isn't there, the system writes `[FILL IN]` instead of inventing one.
- **Skills** (`.claude/skills/`) — Step-by-step workflows for specific tasks, each with its own references, templates, and approval gates.
- **Agents** (`.claude/agents/`) — Specialist roles with defined tools and brain access. One agent (product-marketer) owns brain writes; the rest read only.
- **`CLAUDE.md`** — Routing and governance. Maps each request to the right skill, enforces the writing rules, and blocks AI slop.

Vale linting runs automatically after every edit in `marketing/`, catching banned words, weak language, and AI tells before you read the draft.

## Workflows

Each workflow is one command that chains several skills, with an approval gate between stages. Skip any stage you don't need.

| Command | What it does | Skills it chains |
|---------|-------------|-----------------|
| `/wf-blog-distribute` | Write a blog post and push it across channels | `blog` → `tagore` → `seo-geo` → `social-content` → `email-sequence` |
| `/wf-landing-page` | Ship a conversion-ready page from copy to tracking | `copywriting` → `web-design` → `page-cro` → `seo-geo` → `schema-markup` → `tracking-setup` |
| `/wf-campaign-launch` | Coordinate a multi-channel campaign | `launch-strategy` → `copywriting` → `email-sequence` → `social-content` → `ad-creative` → `tracking-setup` |
| `/wf-competitive-positioning` | Research competitors and build pages that rank | `product-marketing` → `competitor-alternatives` → `copywriting` → `seo-geo` |
| `/wf-case-study-pipeline` | Turn a customer conversation into a distributed case study | `granola` → `case-studies` → `tagore` → `social-content` → `email-sequence` |
| `/wf-repurpose` | Fan one piece of content out to every channel | source → `social-content` + `email-sequence` + `ad-creative` |
| `/wf-seo-sprint` | Audit, plan, and write a batch of SEO content | `seo-geo` → `content-strategy` → `blog` (xN) → `schema-markup` |
| `/wf-ad-campaign` | Launch paid ads from strategy through testing | `paid-ads` → `ad-creative` → `tracking-setup` → `ab-test-setup` |

## Skills

| Category | Skills |
|----------|--------|
| **Content** | `blog`, `copywriting`, `copy-editing`, `content-strategy`, `case-studies`, `lookalike-content`, `tagore` |
| **SEO & Site** | `seo-geo`, `schema-markup`, `site-architecture` |
| **CRO** | `page-cro`, `form-cro`, `ab-test-setup` |
| **Paid** | `paid-ads`, `ad-creative` |
| **Social** | `social-content` |
| **Email & HubSpot** | `email-sequence`, `hubspot-email`, `hubspot-cta`, `hubspot-landing-page` |
| **Design & Brand** | `brand-design`, `web-design`, `image-gen`, `youtube-thumbnail`, `html-to-pdf`, `excalidraw`, `impeccable` |
| **Strategy & PMM** | `product-marketing`, `marketing-psychology`, `marketing-ideas`, `launch-strategy`, `competitor-alternatives`, `revops` |
| **Analytics** | `analytics`, `tracking-setup` |
| **Onboarding & Brand setup** | `setup`, `tone-mapping`, `design-extract`, `brain-health` |
| **System & tools** | `start`, `brief`, `reflect`, `sync-skills`, `granola`, `agent-browser`, `devils-advocate` |

## Agents

| Agent | Role |
|-------|------|
| `content-writer` | Blogs, datasheets, whitepapers, case studies |
| `product-marketer` | Positioning, messaging, brain ownership |
| `seo-specialist` | SEO and AI-search (GEO) optimization |
| `social-media-manager` | Social content and platform strategy |
| `campaign-manager` | Multi-channel campaign coordination |
| `ppc-specialist` | Paid advertising campaigns |

## What's Inside

```
.claude/skills/    # 54 marketing skills (blog, SEO, CRO, HubSpot, ads, etc.)
.claude/agents/    # 6 specialist agents
templates/         # Everything copied into a new instance:
  CLAUDE.md        #   Routing tables, writing rules, anti-hallucination guardrails
  brain/           #   Source-of-truth templates (positioning, personas, competitive)
  brain/brand-guide/  # Visual brand system (colors, typography, components)
  styles/          #   Vale linting rules (AI-slop detection, banned words)
  .env.example     #   API key template
scripts/           # Generator scripts
```

## Install as a Plugin

Prefer to add the skills to an existing project instead of scaffolding a new repo?

**Claude Code:**
```bash
claude plugin install --plugin-dir ./path-to-compound-marketing
```

**Codex:** Clone into your Codex plugin path. The `.codex-plugin/plugin.json` manifest registers it automatically.

## Contributing

This repo is a generator: everything here ships to arbitrary companies, so it must stay company-agnostic. Instance-specific values (brand colors, personal names, positioning) belong in a generated instance's brain files, never in the skills, templates, or docs. CI enforces this by running `scripts/check-leakage.sh` on every pull request, failing if it finds banned content or a malformed skill directory. Run it yourself before opening a PR:

```bash
./scripts/check-leakage.sh
```

Legitimate exceptions live in an allowlist inside that script, so genuine edge cases can be permitted without weakening the check.

## License

MIT
