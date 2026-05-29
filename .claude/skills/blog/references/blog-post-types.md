# Blog Post Types

Use this reference during Step 2 (Outline) of the blog workflow. Match the topic to the right post type, then follow the outline template.

---

## Quick Reference

| Type | When to Use | Typical Length |
|------|-------------|----------------|
| Thought Leadership | Challenging conventional wisdom, introducing a new frame | 1200-2000 words |
| How-To / Tutorial | Teaching a specific process or implementation | 1500-2500 words |
| Comparison | Helping readers choose between approaches or tools | 1200-2000 words |
| News / Announcement | Product releases, company milestones, event recaps | 600-1000 words |
| Listicle | Curating options, tips, or examples around a theme | 1000-1800 words |

---

## 1. Thought Leadership

### When to Use
- You have a non-obvious insight or contrarian take on a problem the audience faces
- You want to reframe how the audience thinks about an issue
- The goal is brand authority and trust, not immediate conversion

### Outline Template

```
# [Title: State the contrarian claim or new frame]

## The Conventional Wisdom
- What most people believe about [topic]
- Why that belief made sense historically
- Where this thinking comes from

## Why That Frame Is Breaking Down
- What has changed in the environment
- Evidence that the old approach is failing
- Real consequences teams are experiencing

## A Better Way to Think About This
- Introduce the new frame
- Explain why it fits the current reality
- Connect to first principles

## Evidence
- Data points, customer examples, or industry trends
- Specific before/after scenarios
- Expert perspectives (with attribution)

## What This Means for [Audience]
- Practical implications
- What to do differently starting now
- How to evaluate whether this applies to your situation

## [CTA]
```

### Opening Pattern
Lead with the contrarian claim directly. Do not warm up. State what everyone assumes, then reveal why it's wrong.

### Key Structural Rules
- The "better frame" must be supported by evidence, not just asserted
- Include at least one real-world example or data point
- The conclusion should give the reader something actionable
- Source all factual claims from `brain/truth.md`

---

## 2. How-To / Tutorial

### When to Use
- Teaching readers how to accomplish a specific task
- Demonstrating a process, implementation, or configuration
- The reader has a clear goal and needs step-by-step guidance

### Outline Template

```
# How to [Achieve Specific Outcome]

## [Opening: State the outcome and who this is for]
- What the reader will accomplish by the end
- Prerequisites or assumptions
- Estimated time/effort

## Prerequisites
- What you need before starting
- Required tools, access, or knowledge
- Environment assumptions

## Step 1: [First Action]
- What to do
- Why this step matters
- Expected result after completing it

## Step 2: [Second Action]
- [Same structure]

## Step N: [Final Action]
- [Same structure]

## Common Mistakes
- Mistake 1: [What goes wrong] > [How to fix it]
- Mistake 2: [What goes wrong] > [How to fix it]

## Summary
- What you accomplished
- Key configuration or output to verify
- Next steps or related guides

## [CTA]
```

### Opening Pattern
Lead with the outcome — what the reader will have built, configured, or accomplished by the end. Do not start with background context.

### Key Structural Rules
- Number every step and keep them in strict order
- Each step should be independently testable — the reader can verify success before moving on
- Include code snippets, commands, or configuration examples where relevant
- The "Common Mistakes" section is required — it adds real-world value
- Keep steps focused: one action per step, not multi-step paragraphs

---

## 3. Comparison

### When to Use
- Readers are choosing between approaches, tools, or methods
- You want to position the product against alternatives or compare ecosystem options
- The reader is in evaluation mode, not learning mode

### Outline Template

```
# [Option A] vs. [Option B]: [Decision Context]

## [Opening: Frame the decision the reader is facing]
- Who needs to make this decision
- What's at stake (consequences of choosing wrong)

## What to Evaluate
- Criteria 1: [Name] — why it matters
- Criteria 2: [Name] — why it matters
- Criteria 3: [Name] — why it matters

## [Option A]: How It Works
- Overview
- Strengths for specific use cases
- Limitations

## [Option B]: How It Works
- Overview
- Strengths for specific use cases
- Limitations

## Comparison Table

| Criteria | Option A | Option B |
|----------|----------|----------|
| [Criterion 1] | [Assessment] | [Assessment] |
| [Criterion 2] | [Assessment] | [Assessment] |
| [Criterion 3] | [Assessment] | [Assessment] |

## When to Choose [Option A]
- Scenarios where this is the better fit

## When to Choose [Option B]
- Scenarios where this is the better fit

## [CTA]
```

### Opening Pattern
Lead with the decision context — the reader is trying to choose, and you're going to help them. Do not start with definitions.

### Key Structural Rules
- Be fair to both options. Readers lose trust if comparisons feel like thinly disguised sales pitches
- Use a comparison table — readers expect it and it's scannable
- End with "When to Choose" sections, not a single winner declaration
- All product claims must be sourced from `brain/truth.md`
- If comparing the product to a competitor, check `brain/positioning-and-messaging.md` (Competitive POV) for approved framing

---

## 4. News / Announcement

### When to Use
- Product launches, feature releases, version updates
- Company milestones (funding, partnerships, hires)
- Event recaps or conference takeaways

### Outline Template

```
# [News Headline: State what happened]

## [News Lead: The essential facts in 2-3 sentences]
- What happened
- When it happened
- Why it matters to the reader

## Why This Matters
- Impact on the reader's work
- Problem this solves or opportunity it creates
- Context within the broader industry or product direction

## Details
- How it works (for product news)
- Key features or specifics
- Availability, timeline, or access information

## What's Next
- Roadmap context (if appropriate and approved)
- How to get started or learn more
- Related resources

## [CTA]
```

### Opening Pattern
Lead with the news — what happened, stated plainly. The first sentence should contain the essential fact. Do not build suspense.

### Key Structural Rules
- Keep it short (600-1000 words). News posts that drag lose readers
- The "Why This Matters" section must connect to the reader, not just celebrate the company
- All product claims from `brain/truth.md`
- Forward-looking statements need `[FORWARD-LOOKING]` tags per `brain/positioning-and-messaging.md`
- Link to docs, demos, or detailed resources for readers who want depth

---

## 5. Listicle

### When to Use
- Curating a set of related items (tools, tips, practices, examples)
- The reader wants options or quick-reference information
- The topic naturally breaks into discrete, parallel items

### Outline Template

```
# [Number] [Things] for [Audience/Outcome]

## [Opening: Why this list matters]
- What problem this list helps solve
- How items were selected (criteria)
- How to use this list

## 1. [Item Name]
- What it is (1-2 sentences)
- Why it belongs on the list
- When/how to use it
- [Link or reference if applicable]

## 2. [Item Name]
- [Same parallel structure]

## N. [Last Item]
- [Same parallel structure]

## Key Takeaway
- The single most important insight from this list
- How to decide which items matter most for the reader's situation

## [CTA]
```

### Opening Pattern
Lead with why this list exists — the problem it solves or the decision it helps with. Do not start with "Here are N things..."

### Key Structural Rules
- Every item must follow the same structure (parallel construction is mandatory)
- Items should be ordered by importance, impact, or logical sequence — not randomly
- Keep items roughly equal in length — one item getting 3x the space signals bias
- The "Key Takeaway" section is required — it prevents the reader from leaving without a clear action
- Odd numbers (5, 7, 9) tend to perform better than even numbers in headlines, but prioritize accuracy over clickbait
