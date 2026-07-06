# Claude Instructions for Compound Marketing

## Human Authority

The repository owner is the final authority on product facts, positioning, and messaging. When in doubt, ask the user.

## Synthesize, Don't Parrot

When the user provides direction, raw thoughts, or rough language, **never echo it back as-is.** Use the full context available (brain files, positioning framework, ICP, competitive landscape) to synthesize their intent into something stronger. You are a thinking partner: judge the input, challenge when warranted, and produce a better version than the raw input. Parroting back what you're told is a failure, even if the output looks polished.

## Writing Style

- When editing marketing/event copy, never use accusatory language toward the audience (e.g., don't imply they have breaches or failures).
- Always run Vale linting after writing or editing any Markdown or HTML content. Do not consider a content task complete until Vale passes.

## Verification Discipline

1. **Verify verifiable claims before acting on them.** When the user states a system-state fact you can check directly with an MCP tool or CLI (HubSpot deals/properties, GA4, LinkedIn, Google Workspace, etc.), verify *before* updating memory, writing reference files, or making downstream recommendations. This is not distrust, it is the same principle as "read the file before editing it." A ~30-second check prevents compounding errors into docs and memory.

2. **Don't diagnose dataset shape from the head of a sort.** When evaluating whether data looks right, wrong, or suspicious, pull a distribution (counts grouped by the relevant dimension like stage, source, date bucket) or explicitly caveat that you are looking at a sample. A burst of similar records at the top of a sort-by-createdate query is not evidence of a bulk import or spam. The shape of the head of a list is almost never the shape of the full dataset.

## Anti-Hallucination Rules & Content Sourcing

1. **Never invent product facts.** All factual claims must originate from `/brain/truth.md`.

2. **Check the brain first.** Before making any claim about the product, company, features, pricing, or customers, verify it exists in `/brain/`.
   - Positioning and messaging: `/brain/positioning-and-messaging.md`
   - ICP details: `/brain/positioning-and-messaging.md` (ICP section)
   - Competitive positioning: `/brain/positioning-and-messaging.md` (Competitive POV section)
   - Voice and tone: `/brain/voice-and-tone.md` if it exists. Match the user's sentence rhythm, vocabulary register, conviction level, and personality markers. If the file is missing or empty, write in a clean professional voice and suggest running `/tone-mapping`.
   - Voice calibration samples: `/brain/voice-samples.md` if it exists. Reuse the signature moves and argument structures it documents; its quoted examples are the target register for all drafts.

3. **Use placeholders for missing information.** If a fact is not in the brain, use `[FILL IN]` or `[VERIFY]` instead of guessing.

4. **Ask when uncertain.** If you need information that isn't available, ask the user rather than fabricating.

5. **Respect ownership.** Only the Product Marketer agent may modify files in `/brain/`. All other agents read only.

6. **Source Citation Rule.** When writing drafts, if a paragraph depends on a factual claim, explicitly reference the source file.
   > Example: Our product detects threats in under 200ms *(source: truth.md)* across cloud-native infrastructure *(source: positioning-and-messaging.md)*.

## File Structure

- `/brain/` — Source of truth. Product Marketer owns this.
- `/.claude/agents/` — Subagent role definitions and instructions.
- `/.claude/skills/` — Claude Code skills: marketing skills and project workflow skills (e.g., case studies).
- `/incoming/` — **Drop zone for raw inputs.** Files placed here for Claude to intake (notes, CSVs, briefs, rough drafts). Read from here, never write to here. Files here are for evaluation and context only; do not treat old marketing collateral as a source of verified claims for new content. All claims must trace to `/brain/`.
- `/marketing/` — **All Claude output goes here.** Blog drafts, social posts, analysis, reports, plans, templates, etc.
- `/marketing/plans/` — Backlog of improvements, new skills, tooling ideas, and projects.
- `/marketing/inspiration/` — Design references, competitor examples, and visual inspiration. Screenshots go in `visual/` subdirectory. Keep reference images co-located with their companion docs.

## Workflow Output Convention

When a workflow skill runs (any multi-step pipeline), all output goes into a single project folder under `marketing/`. The structure:

```
marketing/[category]/[project-slug]/[piece-name].md
```

**Categories** by workflow:

| Workflow | Category folder |
|----------|----------------|
| `/wf-blog-distribute` | `marketing/blog/[post-slug]/` |
| `/wf-landing-page` | `marketing/pages/[page-slug]/` |
| `/wf-campaign-launch` | `marketing/campaigns/[campaign-slug]/` |
| `/wf-competitive-positioning` | `marketing/competitive/[competitor-or-theme-slug]/` |
| `/wf-case-study-pipeline` | `marketing/case-studies/[customer-slug]/` |
| `/wf-repurpose` | `marketing/repurposed/[source-slug]/` |
| `/wf-seo-sprint` | `marketing/seo-sprints/[topic-slug]/` |
| `/wf-ad-campaign` | `marketing/ads/[campaign-slug]/` |

**Rules:**
- Every file produced by a workflow stage goes into the project folder, not scattered across `marketing/`
- Use kebab-case for all folder and file names; use descriptive names per deliverable (e.g., `blog-post.md`, `social-linkedin-1.md`, `email-announcement.md`)
- The project slug comes from the topic, campaign name, or customer name
- Ask the user to confirm the project slug before creating files if it's ambiguous
- Single-skill runs (not workflows) still use their natural location: `marketing/blog/`, `marketing/social/`, etc.

## When Creating Visual Assets or Design

- **Always read `/brain/brand-guide/brand-guide.md` first.** This is the source of truth for colors, typography, gradients, spacing, button styles, card patterns, and all visual design decisions.
- Logo files are in `/brain/brand-guide/` (PNG format).
- Use the `brand-design` skill for **static creative assets** (ads, carousels, social graphics, banners, slide graphics, whitepaper PDFs).
- Use the `web-design` skill for **live interactive web UI** (Next.js landing pages, HubSpot landing pages, component craft, interaction states, responsive, motion, accessibility, and polish/audit of shipped pages).
- `hubspot-email`, `hubspot-landing-page`, and `hubspot-cta` all reference `web-design` where relevant; loading them first is correct for those mediums.

## Mandatory Skill & Agent Routing

**This is non-negotiable. STOP before generating any output.**
Before responding to any task, you MUST:
1. Check the routing tables below
2. Identify the best matching skill and/or agent
3. Load and use that skill/agent BEFORE producing any work

Do not skip this step. Do not freestyle. Do not generate content without the relevant skill loaded. If you produce work without routing through the correct skill, it is a failure, even if the output looks good.

### Workflow Routing Table (multi-step)

**Check this table first.** If the user's intent spans multiple skills or channels, route to the workflow skill. It orchestrates the full pipeline with gates between stages.

| Task | Workflow Skill |
|------|---------------|
| Write a blog post AND distribute it (social, email) | `wf-blog-distribute` |
| Build a landing page end-to-end (copy → build → CRO → SEO → tracking) | `wf-landing-page` |
| Plan and execute a multi-channel campaign | `wf-campaign-launch` |
| Research competitors and build comparison pages | `wf-competitive-positioning` |
| Create a case study from meeting notes and distribute it | `wf-case-study-pipeline` |
| Take existing content and push it across channels | `wf-repurpose` |
| Run an SEO audit and write a batch of optimized posts | `wf-seo-sprint` |
| Launch paid ads from strategy through testing | `wf-ad-campaign` |

### Skill Routing Table (single task)

| Task | Skill to Use |
|------|-------------|
| Write new marketing copy (landing pages, feature pages, product pages) | `copywriting` |
| Edit, review, or improve existing copy (including pitch decks, slide copy, presentations) | `copy-editing` |
| Write LinkedIn posts, Twitter/X threads, social media content | `social-content` |
| Write a blog post (full workflow) | `blog` |
| Write datasheets, whitepapers, long-form content | Use `content-writer` agent |
| Write or draft case studies | `case-studies` |
| Plan content strategy, topics, content calendar | `content-strategy` |
| Write email sequences, drip campaigns, nurture flows | `email-sequence` |
| Create competitor comparison or alternative pages | `competitor-alternatives` |
| Plan a product launch or feature announcement | `launch-strategy` |
| Generate marketing ideas or growth tactics | `marketing-ideas` |
| Apply psychology, mental models, or behavioral science to marketing | `marketing-psychology` |
| Set up or audit analytics tracking (GA4, GTM, events, consent mode) | `tracking-setup` |
| Create or optimize paid ad campaigns | `paid-ads` |
| Generate, iterate, or scale ad creative (headlines, descriptions, variations) | `ad-creative` |
| Optimize a page for conversions (CRO) | `page-cro` |
| Optimize forms (lead capture, contact, demo request) | `form-cro` |
| Plan, design, or run A/B tests and experiments | `ab-test-setup` |
| Page titles, meta descriptions, slugs, on-page SEO metadata | `seo-geo` |
| Audit SEO issues on the site | `seo-geo` |
| Optimize content for AI search engines (GEO) | `seo-geo` |
| Keyword research, content gap analysis | `seo-geo` |
| Add or fix schema markup / structured data | `schema-markup` |
| Plan or restructure site hierarchy, navigation, URL structure, internal linking | `site-architecture` |
| Revenue operations, lead scoring, lead routing, marketing-to-sales handoff | `revops` |
| Create or update product marketing context | `product-marketing` |
| Positioning, messaging, value props, ICP, personas, differentiation, competitive battlecards, sales narratives | `product-marketing` |
| Generate images (illustrations, graphics, visuals via AI) | `image-gen` |
| Design creative assets (ads, carousels, social graphics, banners, visual content) | `brand-design` |
| Create YouTube thumbnails, video thumbnail art | `youtube-thumbnail` |
| Export HTML pages to print-quality vector PDFs | `html-to-pdf` |
| Pull meeting notes from Granola | `granola` |
| Reflect on session, extract skill learnings, self-improving skills | `reflect` |
| Browse websites, take screenshots, fill forms, scrape data, test web apps | `agent-browser` |
| Build HTML email templates for HubSpot | `hubspot-email` |
| Build HubSpot landing page templates (Design Manager) | `hubspot-landing-page` |
| CTA buttons, tracking strategy, custom CTA modules | `hubspot-cta` |
| Build, audit, critique, or polish live web UI | `web-design` |
| Analyse content patterns, reverse-engineer winning posts | `lookalike-content` |
| Marketing performance metrics (email, pages, social, video) | `analytics` |
| Strip AI patterns, score prose quality, enforce human voice | `tagore` |
| Build voice and tone profile from writing samples | `tone-mapping` |
| Extract design system (colors, fonts, spacing) from a website | `design-extract` |
| Check brain file completeness, see what's missing | `brain-health` |
| Sync skills between Claude Code and Codex runtimes | `sync-skills` |

### Agent Routing Table

| Task | Agent to Use |
|------|-------------|
| Datasheets, whitepapers, long-form content (for blog posts, use the `blog` skill) | `content-writer` |
| Positioning, messaging, brain updates | `product-marketer` |
| SEO strategy, keyword research, technical SEO, GEO optimization | `seo-specialist` |
| Social media content, scheduling, platform strategy | `social-media-manager` |
| Campaign planning, multi-channel coordination | `campaign-manager` |
| PPC, paid media, ad campaign management | `ppc-specialist` |

### Routing Rules

1. **Always check this table first.** Match the user's request to the best skill or agent before starting work.
2. **Skills and agents can be combined.** For example, use the `content-writer` agent with the `copy-editing` skill for reviewing a blog draft.
3. **When in doubt, ask.** If the request doesn't clearly map, ask the user which approach they prefer.
4. **Never skip the skill.** If a matching skill exists, load it. The skills contain frameworks, checklists, and quality standards that must be applied.
5. **`web-design` beats `frontend-design` (Anthropic plugin) for branded work.** The Anthropic `frontend-design` skill produces generic AI aesthetics. Always prefer the project's `web-design` skill for brand-consistent work.

### Proactive Analytics Usage

The `analytics` skill should be used **proactively**. Don't wait for the user to explicitly ask for "analytics." Load the skill and run the appropriate script when the user's question would benefit from real data:

| User asks something like... | Script to run |
|----------------------------|---------------|
| "How are our emails doing?" / "What's our open rate?" | `hubspot-emails.ts` |
| "How are our landing pages converting?" / "Which pages get the most traffic?" | `hubspot-pages.ts` |
| "How did that campaign do?" / "Which campaign drove the most leads?" | `hubspot-campaigns.ts` |
| "How are our LinkedIn posts doing?" / "What's our engagement?" | `linkedin.ts` |
| "How's our Twitter/X?" / "What tweets performed best?" | `x-analytics.ts` |
| "How's our YouTube channel?" / "Which videos got the most views?" | `youtube.ts` |
| "What should we do differently?" / "Where should we focus?" / "What's working?" | Run all configured platforms |
| Planning new content for a specific channel | Run that channel's script for baselines |

**Rule:** If the user asks a performance, results, or "how is X doing" question and analytics scripts can answer it, run the script FIRST, then answer with real data. Do not guess at metrics or use generic industry benchmarks when we have our own data available.

## CLI Tools

**GitHub CLI (`gh`):** Use `gh` for all GitHub operations: PRs, issues, API calls, repo queries. No MCP plugin needed.

**Google Workspace CLI (`gws`):** Configured for Google Workspace. Use it to read, create, and edit Google Sheets, Docs, Slides, and Drive files. See `.env.example` for setup details and command reference. Extract file IDs from Google URLs (the segment after `/d/` in the URL).

## Em Dash Discipline

Em dashes are overused in AI-generated text. Limit yourself to **1 per paragraph max, 3 per document max.** When you reach for an em dash, use one of these instead:

- **Comma** for light pauses or appositives
- **Colon** to introduce an explanation or list
- **Parentheses** for true asides
- **Period + new sentence** when the aside is substantial
- **Semicolon** to join related independent clauses

If a draft exceeds 3 em dashes, revise before presenting it. This applies to ALL output: content, chat responses, plans, everything.

## AI Slop Patterns: NEVER Use

These patterns are dead giveaways for AI-generated content. No agent, no skill, no draft should ever use them:

- **"X wasn't Y. It was Z."**
- **"That's not just X. That's Y."**
- **"Here's the thing:" / "Here's why that matters:"**
- **"Let that sink in." / "Read that again." / "Full stop." / "And that changes everything."**
- **Repetitive single-word punctuation lists** (e.g., "Point one. Permanent. Point two. Permanent."). Write real sentences with varying structure.
- **Dangling stat fragments** (e.g., "100+ rounds of improvement. 30% better."). Weave stats into real sentences.
- **Movie-trailer bridges** (e.g., "I've been thinking about that ever since."). Connect ideas directly.

If you catch yourself writing any of these, rewrite in a natural, human voice. This applies to ALL content.
