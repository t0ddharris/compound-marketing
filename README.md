<p align="center">
  <img src="github-social.png" alt="Compound Marketing">
</p>

# Compound Marketing

**Each unit of marketing work should make the next one easier.**

Compound Marketing is built primarily for B2B marketers and GTM teams — more reach without sacrificing quality. It does three things:

- **Automates** repetitive production work through skills and workflows.
- **Speeds up** the work you already do.
- **Extends** into specialties you'd otherwise outsource or skip.

What makes it compound: skills capture how you work, workflows chain those skills into full pipelines, and a "brain" holds your company's positioning, personas, and brand. Every correction you make and every session you close feeds back into the system — so the hundredth blog post starts from everything the first ninety-nine taught it. The approach borrows from [compound engineering](https://github.com/EveryInc/compound-engineering-plugin), applied to marketing.

Everything is moldable. Work with your agent to customize the workflows and skills to your own processes and styles. Trim what you don't need, modify what you want, add what you're missing!

Works with **Claude Code** and **OpenAI Codex**.

## Getting Started

You need [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or [OpenAI Codex](https://openai.com/codex). Both are AI agents that run in your terminal (the Terminal app on a Mac). Everything else is optional: [Vale](https://vale.sh/) checks drafts for banned words and AI tells, the [GitHub CLI](https://cli.github.com/) (`gh`) helps if you put your work on GitHub, the [Codex CLI](https://github.com/openai/codex) signed in with a ChatGPT account makes images (no API key needed), and [QMD](https://github.com/tobi/qmd) searches a notes folder if you connect one.

This project is a starter kit. You download it once, and its setup command builds a separate folder just for your company, with its own copy of the skills and a set of blank "brain" files that hold your company's facts, positioning, and brand. You do all your marketing work in that new folder.

### 1. Download the starter kit and run setup

Open Terminal and run the commands below. They use a folder called `Development` in your home folder, but any folder works. To use `Documents` instead, change the first line to `cd ~/Documents`. If you pick a folder that doesn't exist yet, create it first (for example, `mkdir ~/Development`).

One caution: avoid folders that a sync service like iCloud, OneDrive, or Dropbox backs up, because syncing can damage the change history git keeps. Work laptops often sync `Documents` and `Desktop` this way. On a Mac, iCloud does it when "Desktop & Documents Folders" is turned on under System Settings › your name › iCloud. If you're not sure, `~/Development` is a safe choice.

```bash
cd ~/Development
git clone https://github.com/t0ddharris/compound-marketing.git
cd compound-marketing
claude          # or: codex
```

`git clone` downloads this project into a new `compound-marketing` folder. The last line starts your agent. When it's ready, type `/setup`.

Setup asks for your company name and creates your company's folder next to the starter kit. It shows you the location first, so you can pick a different one:

```
~/Development/compound-marketing/          # the starter kit you downloaded
~/Development/your-company-marketing/      # your company's folder, where you'll work
```

Both are ordinary, permanent folders on your computer; nothing goes to a temporary location. Your company's folder is also a git repository, which means it keeps a history of every change so you can see what changed and undo mistakes. It stays on your computer unless you choose to put it on GitHub. Keep the starter kit folder where it is. It's how your company's folder gets new skills and fixes later (see step 6).

### 2. Answer the setup questions

Setup is a conversation. It will:

- Ask about your product, target customer, and category
- Read your website (optional) to pull in messaging and features
- Draft a starter positioning statement and buyer personas
- Pick up your brand colors and fonts from your site (optional)
- Connect a folder of notes you already keep (optional, see step 4)
- Connect other tools: image generation, HubSpot, LinkedIn, Granola, and more

You don't need perfect answers. Anything you skip stays as a `[FILL IN]` placeholder that you can complete later.

Comfortable in the terminal and want to skip the conversation? `./scripts/create-instance.sh` creates the same company folder, but leaves every brain file blank.

### 3. Bring your own docs (optional)

Have messaging frameworks, product overviews, brand guidelines, or competitive research? When setup asks, copy them into the `incoming` folder inside your company's folder. Drag them in with Finder, or from Terminal:

```bash
cp ~/Documents/our-messaging.pdf ~/Development/your-company-marketing/incoming/
```

Setup reads PDFs, Markdown, plain text, and images, then shows you what it wants to add to your brain files and asks before writing anything. That saves a lot of typing.

The brain keeps growing after setup. Run `/brain-ingest` whenever you find something useful. It reads files in `incoming` or pulls straight from the tools your agent is connected to, like email, Google Drive, SharePoint, or meeting notes. For each brain file it shows the changes it suggests and where each fact came from, flags anything that disagrees with what's already there, and writes only what you approve.

### 4. Connect your notes (optional)

If you keep meeting notes, people profiles, and clippings in a notes app like Obsidian, setup can let the agent read that folder. Your notes stay where they are, and the agent never changes them. It checks them for context on customers, people, and past meetings. Before a fact from your notes goes into anything you publish, the agent suggests adding it to a brain file and asks you first.

Setup also offers to install [QMD](https://github.com/tobi/qmd), a search tool that lets the agent find the right note without opening every file. You can install it yourself with `npm install -g @tobilu/qmd` (needs Node.js). Without it, the agent still searches, just more slowly.

Under the hood: Claude Code gets read access through `.claude/settings.local.json`, which stays on your machine and out of git because the path only works there. The folder is also listed under `knowledge_sources` in `.compound-marketing.yml`, which is where Codex finds it.

### 5. Start working

From now on, start your agent in your company's folder:

```bash
cd ~/Development/your-company-marketing
claude          # or: codex
```

Then ask for what you need in plain language, or use a slash command:

```
/blog              Write a blog post
/social-content    Draft LinkedIn or X posts
/wf-landing-page   Build a landing page, end to end
```

### 6. Get updates

When the starter kit gets new skills or fixes, run `/update` in your company's folder. It downloads the latest starter kit and shows you what would change before touching anything. Skills you never edited get the new version. Skills you edited, including lessons your agent saved with `/reflect`, keep your changes, with the new material merged in around them. If you and the update changed the same lines, the agent shows you both versions and you choose. Your brain files are never changed, though new ones get added.

The agent saves your work before updating, so if you don't like the result, you can undo the whole update with one command it gives you.

## How It Works

Compound Marketing has three layers, each fixing a way AI marketing usually goes wrong:

- **Brain** (`brain/`) — One source of truth for your company. Every factual claim traces back to a brain file. If a fact isn't there, the system writes `[FILL IN]` instead of inventing one. `/brain-ingest` fills it from your email, drives, and documents, with your approval and a source on every fact.
- **Skills** (`.claude/skills/`) — Step-by-step workflows for specific tasks, each with its own references, templates, and approval gates.
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
| **Content** | `blog`, `long-form`, `copywriting`, `copy-editing`, `content-strategy`, `case-studies`, `lookalike-content`, `tagore` |
| **SEO & Site** | `seo-geo`, `schema-markup`, `site-architecture` |
| **CRO** | `page-cro`, `form-cro`, `ab-test-setup` |
| **Paid** | `paid-ads`, `ad-creative` |
| **Social** | `social-content` |
| **Email & HubSpot** | `email-sequence`, `hubspot-email`, `hubspot-cta`, `hubspot-landing-page` |
| **Design & Brand** | `brand-design`, `web-design`, `image-gen`, `youtube-thumbnail`, `html-to-pdf`, `excalidraw`, `impeccable` |
| **Strategy & PMM** | `product-marketing`, `marketing-psychology`, `marketing-ideas`, `launch-strategy`, `competitor-alternatives`, `revops` |
| **Analytics** | `analytics`, `tracking-setup` |
| **Onboarding & Brand setup** | `setup`, `tone-mapping`, `design-extract`, `brain-health`, `brain-ingest` |
| **System & tools** | `start`, `brief`, `reflect`, `sync-skills`, `update`, `granola`, `agent-browser`, `devils-advocate` |

## What's Inside

```
.claude/skills/    # 57 skills (blog, SEO, CRO, HubSpot, ads, etc.)
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

**Claude Code:** load it for a session with
```bash
claude --plugin-dir ./path-to-compound-marketing
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
