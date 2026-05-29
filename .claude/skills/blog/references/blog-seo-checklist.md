# Blog SEO & GEO Checklist

Use this checklist during Step 4 (Quality Enforcement) of the blog workflow. Every item should be verified before the draft moves to Gate 2.

For the full SEO/GEO skill, see `/.claude/skills/seo-geo/SKILL.md`.

---

## On-Page SEO

### Title Tag
- [ ] 50-60 characters (visible in SERP without truncation)
- [ ] Primary keyword near the beginning
- [ ] Compelling and click-worthy (not just keyword-stuffed)
- [ ] Unique — not duplicating another page's title
- [ ] Brand name at end: `[Title] | [Company]`

### Meta Description
- [ ] 150-160 characters
- [ ] Includes primary keyword naturally
- [ ] Clear value proposition — why should someone click?
- [ ] Contains a call to action or outcome hint
- [ ] Unique per post

### URL Slug
- [ ] Short and descriptive (3-5 words ideal)
- [ ] Includes primary keyword
- [ ] Lowercase, hyphen-separated
- [ ] No dates (they age content)
- [ ] No stop words (a, the, is, of) unless needed for clarity

### Heading Structure
- [ ] One H1 per post — includes primary keyword
- [ ] H2s for major sections — include secondary/related keywords where natural
- [ ] H3s for subsections where needed
- [ ] No skipped heading levels (H1 > H2 > H3, never H1 > H3)
- [ ] Headings every 200-300 words for scannability

### Keyword Placement
- [ ] Primary keyword in title, H1, first 100 words, and at least one H2
- [ ] Related keywords distributed naturally throughout body
- [ ] No keyword stuffing (hurts both SEO and GEO)
- [ ] Keywords read naturally — if it sounds forced, rewrite

### Internal Links
- [ ] 3-5 internal links to related company content
- [ ] Descriptive anchor text (not "click here" or "learn more")
- [ ] Links are contextually relevant, not forced
- [ ] Check that linked pages exist and are current

### Images
- [ ] Descriptive file names (not `IMG_1234.png`) — generated images use `[slug]-hero.png` and `[slug]-inline.png`
- [ ] Alt text on every image — describes image, includes keyword when natural
- [ ] Compressed file sizes (WebP preferred)
- [ ] At least one image in the post (hero, inline, diagram, or screenshot)
- [ ] Hero image or documented placeholder in frontmatter `og_image` field (see Step 5.5)

---

## GEO (Generative Engine Optimization)

These optimizations increase the chance that AI search engines (ChatGPT, Perplexity, Gemini, Copilot, Claude) cite or surface the post.

### Content Structure
- [ ] **Answer-first format** — the direct answer or key insight appears early, not buried at the end
- [ ] **Self-contained sections** — each H2 section makes sense if extracted alone by an AI engine
- [ ] **Short paragraphs** — 2-3 sentences max. Dense blocks get skipped by AI parsers
- [ ] **Bullet points and numbered lists** — AI engines parse structured content more reliably than prose
- [ ] **Tables for comparison data** — easier for AI to extract and cite than prose comparisons

### Citation Fuel
- [ ] **Statistics with sources** — specific numbers with attribution (boosts AI visibility by ~37%)
- [ ] **Expert quotes with names** — attributed quotes from real people (boosts AI visibility by ~30%)
- [ ] **Authoritative tone** — confident, expert language without hedging (boosts AI visibility by ~25%)
- [ ] **Technical terms** — include domain-specific terminology where appropriate (+18%)

### Evidence Patterns
Use these patterns to structure claims for maximum AI extractability:

**Statistic Block:** `[Claim]. According to [Source], [specific number + timeframe]. [Why it matters].`

**Expert Quote Block:** `"[Quote]," says [Name], [Title] at [Org]. [Context sentence].`

**Self-Contained Answer Block:** `**[Topic]**: [Complete answer in 2-3 sentences with specific details].`

---

## E-E-A-T (Experience, Expertise, Authority, Trust)

### Experience
- [ ] First-hand insight or original perspective included (not just summarizing others)
- [ ] Real examples, scenarios, or case references (not hypothetical)
- [ ] Draws from brand-specific experience where relevant (customer stories, engineering decisions)

### Expertise
- [ ] Author expertise signaled (byline, credentials, or "written by" note)
- [ ] Accurate, detailed technical information
- [ ] All claims properly sourced (from `brain/truth.md` for the company facts, external sources for industry claims)

### Authoritativeness
- [ ] Content adds something new to the conversation (not just rehashing existing content)
- [ ] References authoritative external sources where appropriate
- [ ] Connects to the company's domain authority (AI threat detection, AI agent security, cybersecurity)

### Trustworthiness
- [ ] No invented facts, metrics, or customer names
- [ ] Unverified claims marked `[VERIFY]`
- [ ] Sources cited inline using the standard format: `*(source: truth.md)*`
- [ ] Forward-looking features tagged `[FORWARD-LOOKING]`

---

## Social Sharing Metadata

### Open Graph Tags
- [ ] `og:title` — compelling title (can differ from SEO title)
- [ ] `og:description` — 1-2 sentence summary optimized for social feeds
- [ ] `og:image` — generated image path (e.g., `marketing/blog/images/[slug]-hero.png`) or `[OG IMAGE: description]` placeholder (1200x630px ideal)
- [ ] `og:url` — canonical URL of the post
- [ ] `og:type` — `article`

### Twitter Card Tags
- [ ] `twitter:card` — `summary_large_image`
- [ ] `twitter:title` — same as og:title or customized for Twitter
- [ ] `twitter:description` — same as og:description or customized
- [ ] `twitter:image` — same as og:image

### Output Format

Include this metadata block at the top of the output package:

```yaml
# SEO & Social Metadata
title_tag: "[50-60 chars with primary keyword]"
meta_description: "[150-160 chars with keyword and CTA]"
slug: "[short-descriptive-slug]"
primary_keyword: "[keyword]"
secondary_keywords: ["keyword2", "keyword3"]
og_title: "[Social-optimized title]"
og_description: "[1-2 sentence social summary]"
og_image: "[Generated image path or placeholder description]"
```
