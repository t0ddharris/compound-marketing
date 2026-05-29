# Positioning & Messaging Framework

This is the canonical structural framework for product marketing work. It was reverse-engineered from the positioning-and-messaging architecture and codified as the default thinking model for all product marketing tasks.

Use this framework when building positioning and messaging from scratch or auditing existing work for structural completeness.

---

## Framework Architecture

The framework operates in three layers. Each layer builds on the one above it. You cannot produce strong Layer 2 without solid Layer 1.

```
Layer 1: Strategic Positioning (Decision Layer)     ← Internal only
    ↓ derives
Layer 2: Core Messaging (Applied Layer)             ← External-safe
    ↓ governs
Layer 3: Guardrails & Usage                         ← Rules for deployment
```

---

## Layer 1: Strategic Positioning (Decision Layer)

This is the internal strategic foundation. It captures market truths and strategic framing. Language here may later be adapted into external messaging, but inclusion here does NOT imply external readiness.

### 1.1 Market Problem / Category Framing

Define the systemic problem that creates demand.

**Structure:**
- What do organizations believe? (the false confidence)
- Why is that belief wrong? (the reality)
- What traditional approaches miss (the gap)
- What happens as a result (the consequence)

**Key question:** What false belief do buyers hold that makes your product necessary?

### 1.2 Buyer Mindset

Map the buyer's mental model.

| Component | What to Define |
|-----------|---------------|
| Current State | What is true today about their situation? |
| Desires | What do they want to be true? |
| Objections | What concerns prevent them from acting? |
| Failed Alternatives | What have they tried that didn't work? |

### 1.3 Problem Discovery Flow

Map how the problem surfaces in the organization.

| Component | What to Define |
|-----------|---------------|
| Trigger | What event makes the problem visible? |
| Constraint | What limits their current approach? |
| Cost | What is the cost of not solving this? |
| Failed Alternatives | Why haven't existing solutions worked? |

**Key insight:** The trigger determines the urgency. Map triggers to buying urgency.

### 1.4 False Confidence Narrative

The core narrative tension. What do buyers wrongly believe is true?

**Structure:**
- What leadership assumes
- What reality actually looks like
- Where the gap is worst
- How the risk compounds over time

### 1.5 Business Risk & Impact

Map problem to business consequences across five dimensions:

| Risk Area | Impact |
|-----------|--------|
| Revenue | Direct financial impact |
| Customer Trust | Reputation and relationship damage |
| Engineering Productivity | Team velocity and morale costs |
| Cloud & Tooling Cost | Infrastructure and tooling overhead |
| Executive Risk | Leadership exposure and accountability |

### 1.6 Technical Risk & Impact

Map technical gaps to business outcomes.

| Technical Risk | Business Impact |
|----------------|----------------|
| [Gap in coverage/capability] | [Consequence for the business] |

### 1.7 Competitive POV

**Market Category:**
- Category name
- How we define it (not how analysts define it — how we frame it to buyers)

**Competitive Positioning:**
For each competitor class (direct, traditional, indirect):

| Component | What to Define |
|-----------|---------------|
| Their weakness | Where they fall short |
| Our advantage | What we do that they can't |
| Positioning line | One sentence that captures the competitive frame |

**Competitive Landmines:**
What competitors say about us and how to respond.

**How We Win / How We Lose / Our Advantages:**
Honest internal assessment of competitive dynamics.

### 1.8 Differentiation Themes

These are capabilities that make you UNIQUE (not just better) in the market.

For each theme:

| Component | What to Define |
|-----------|---------------|
| What makes it unique | The specific capability and why no one else has it |
| Validation | Customer quote, third-party proof, or technical evidence |
| Customer value | What this means for the buyer in concrete terms |

**Test:** If a competitor could credibly claim the same thing, it's not a differentiation theme.

### 1.9 ICP: Who Cares and Why

**Company Characteristics:**
- Industry
- Company size (revenue range)
- Tech stack requirements
- Growth stage

**Triggers:** Events that cause them to look for a solution.

**Disqualifiers:** Who is NOT a fit. (Critical — saves everyone time.)

**Secondary ICP:** If applicable.

### 1.10 Buyer Personas

For each persona:

| Component | What to Define |
|-----------|---------------|
| Title | Specific role titles |
| Top Problems | 3-4 problems ranked by urgency |
| What They Need | Concrete requirements (not vague desires) |
| Decision Role | EB, Champion, Technical Evaluator, User Buyer, Blocker |

---

## Layer 2: Core Messaging (Applied Layer)

External-safe messaging derived intentionally from Layer 1. Every message here must trace back to a strategic decision above.

### 2.1 Situation / Complication / Resolution (SCR)

The narrative arc that frames all messaging.

- **Situation:** What the audience accepts as true
- **Complication:** The unexpected wrinkle that creates urgency
- **Resolution:** How your product resolves the tension

### 2.2 Messaging Pillars

4-6 themed capability clusters. Each pillar:

| Component | What It Contains |
|-----------|-----------------|
| Headline | One sentence that captures the pillar |
| Supporting Proof Points | 3-5 specific, verifiable claims |
| Use When | Audience and context guidance |
| Customer Quote | If available |

### 2.3 Positioning Statement

**Formula:**
For **[target audience]**
Who **[situation/problem]**
[Product] is a **[market category]**
That **[key benefit]**
Unlike **[alternatives]**
[Product] **[key differentiator]**

### 2.4 Who We Are / What We Do / How We Do It

Three levels of explanation:
- **Who We Are:** Identity + core value in 1-2 sentences
- **What We Do:** Capability + outcome in 2-3 sentences
- **How We Do It:** Technical approach + mechanism in 2-3 sentences

### 2.5 Elevator Pitches

- **25 words:** Core identity and value
- **50 words:** + key capability and proof
- **75 words:** + problem framing and competitive context

### 2.6 Description Blocks

- **Short (1 sentence):** Core value proposition
- **Medium (2-3 sentences):** + how and key proof
- **Long (paragraph):** + problem context, customer names, full positioning

### 2.7 Value Propositions

- **Core:** The single most important value statement
- **Variants (A/B):** Alternative angles for testing

### 2.8 Messaging Architecture

All external messaging follows this structure:

```
Headline → Subhead → Pillar → Proof → CTA
```

### 2.9 Outcomes & Benefits (Value Drivers)

Categorize by stakeholder level:
- **Operational Outcomes:** Day-to-day improvements
- **Strategic Outcomes:** Long-term business advantages
- **Team Outcomes:** Role-specific improvements

### 2.10 Audience-Specific Variants

Adapt messaging for:
- Technical Practitioners
- Engineering Leaders
- Executives

### 2.11 Words We Use / Words We Avoid

Controlled vocabulary that enforces differentiation and prevents generic language.

---

## Layer 3: Guardrails & Usage

- Layer 2 messaging is canonical for all external assets
- Tactical assets (pages, emails, ads) must derive from Layer 2
- Claims without proof get marked `[VERIFY]`
- Section 1 language requires adaptation before external use

---

## Completeness Checklist

When building or auditing a positioning-and-messaging document, verify:

### Layer 1
- [ ] Market problem defined with false confidence narrative
- [ ] Buyer mindset mapped (current state, desires, objections, failed alternatives)
- [ ] Problem discovery flow complete (trigger, constraint, cost, failed alternatives)
- [ ] Business and technical risk mapped to impact
- [ ] Competitive POV with specific competitor positioning
- [ ] Differentiation themes with validation and customer value
- [ ] ICP defined with triggers and disqualifiers
- [ ] Buyer personas with problems, needs, and decision roles

### Layer 2
- [ ] SCR narrative arc defined
- [ ] 4-6 messaging pillars with proof points
- [ ] Positioning statement (Dunford format)
- [ ] Who/What/How blocks written
- [ ] Elevator pitches at 25/50/75 words
- [ ] Description blocks at short/medium/long
- [ ] Value propositions with variants
- [ ] Outcomes categorized by stakeholder level
- [ ] Audience-specific variants for each persona
- [ ] Controlled vocabulary defined
