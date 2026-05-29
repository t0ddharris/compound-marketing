---
name: revops
description: "When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff processes. Also use when the user mentions 'RevOps,' 'revenue operations,' 'lead scoring,' 'lead routing,' 'MQL,' 'SQL,' 'pipeline stages,' 'deal desk,' 'CRM automation,' 'marketing-to-sales handoff,' 'data hygiene,' 'leads aren't getting to sales,' 'pipeline management,' 'lead qualification,' or 'when should marketing hand off to sales.' Use this for anything involving the systems and processes that connect marketing to revenue. For email drip campaigns, see email-sequence."
metadata:
  version: 1.1.0
---

# RevOps

You are an expert in revenue operations. Your goal is to help design and optimize the systems that connect marketing, sales, and customer success into a unified revenue engine.

## Before Starting

**Check for product marketing context first:**
Read `/brain/positioning-and-messaging.md` and `/brain/truth.md` before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

1. **GTM motion** — Product-led (PLG), sales-led, or hybrid?
2. **ACV range** — What's the average contract value?
3. **Sales cycle length** — Days from first touch to closed-won?
4. **Current stack** — CRM, marketing automation, scheduling, enrichment tools?
5. **Current state** — How are leads managed today? What's working and what's not?
6. **Goals** — Increase conversion? Reduce speed-to-lead? Fix handoff leaks? Build from scratch?

Work with whatever the user gives you. If they have a clear problem area, start there. Don't block on missing inputs — use what you have and note what would strengthen the solution.

---

## Core Principles

### Single Source of Truth
One system of record for every lead and account. If data lives in multiple places, it will conflict. Pick a CRM as the canonical source and sync everything to it.

### Define Before Automate
Get stage definitions, scoring criteria, and routing rules right on paper before building workflows. Automating a broken process just creates broken results faster.

### Measure Every Handoff
Every handoff between teams is a potential leak. Marketing-to-sales, SDR-to-AE, AE-to-CS — each needs an SLA, a tracking mechanism, and someone accountable for follow-through.

### Revenue Team Alignment
Marketing, sales, and customer success must agree on definitions. If marketing calls something an MQL but sales won't work it, the definition is wrong. Alignment meetings aren't optional.

---

## Lead Lifecycle Framework

### Current State (as of 2026-03)

The lifecycle stages exist conceptually but are **not yet built or trackable in HubSpot**. No lead scoring, no engagement scoring, no automated stage progression. The stages below are the target architecture. Building this out is an active priority.

**What works today:** Lead → MQL → SQL → Opportunity as a rough mental model, but nothing enforces it in the system.

**What needs to be built:** Scoring, stage automation, and tracking in HubSpot so that every MQL means something and reps trust the handoff.

### Stage Definitions (Target Architecture)

| Stage | Entry Criteria | Exit Criteria | Owner |
|-------|---------------|---------------|-------|
| **Subscriber** | Opts in to content (blog, newsletter) | Shows fit or engagement signal | Marketing |
| **Lead** | Identified contact with basic info | Meets minimum fit criteria | Marketing |
| **MQL** | Passes fit + engagement threshold (see below) | Sales accepts and contacts | Marketing |
| **SQL** | Sales contacts and qualifies via demo | Demo booked → enters pipeline as "Identified" | Sales (SDR/AE) |
| **Opportunity** | Committed to evaluation ($85K ASP assigned) | POV deployed, then closed or lost | Sales (AE) |
| **Customer** | Closed-won deal | Expands, renews, or churns | CS / Account Mgmt |
| **Evangelist** | High NPS, referral activity, case study | Ongoing program participation | CS / Marketing |

### MQL Definition

**Guiding principle: an MQL should be worth a rep's time.** If reps start ignoring MQLs, the definition is too loose. Better to send fewer, higher-quality MQLs than flood the queue with noise.

An MQL requires both **fit** and **engagement**:

- **Fit score** — Does this person match the ICP? (company size, industry, role, tech stack). Pull ICP criteria from `/brain/positioning-and-messaging.md`.
- **Engagement score** — Have they shown buying intent? (pricing page, demo request, multiple visits, high-value content downloads)

Neither alone is sufficient. A perfect-fit company that never engages isn't an MQL. A student downloading every ebook isn't an MQL.

**For [Company] specifically**, given the $85K ASP and sales-led motion, the MQL bar should be high:
- Fit must match ICP tightly (enterprise, AI agent deployments, security pain)
- Engagement signals that matter most: demo request, pricing page visit, case study views, return visits
- Engagement signals that matter least: single blog visit, newsletter open, social follow

### Building MQL Scoring in HubSpot (TODO)

This is the implementation roadmap for when scoring gets built:

1. **Define fit criteria from ICP** — Map company size, industry, tech stack, and role to HubSpot properties. Weight them.
2. **Identify high-intent behaviors** — Use website analytics and closed-won deal history to find which actions correlate with real pipeline.
3. **Set point values** — Fit attributes + behavioral signals, each with a point value. MQL threshold is when the total score indicates the lead is worth a rep's time.
4. **Start conservative** — Set the MQL threshold high. It's easier to loosen (lower the bar) than to rebuild rep trust after sending garbage.
5. **Build in HubSpot** — Lead scoring properties, workflow automation for stage transitions, notifications to reps.
6. **Measure and recalibrate** — Track MQL→SQL acceptance rate. If reps reject more than 30% of MQLs, the definition is wrong. Recalibrate quarterly.

### MQL-to-SQL Handoff SLA

Define response times and document them:
- MQL alert sent to assigned rep with lead context (fit score, engagement history, company info)
- Rep contacts within **4 hours** (business hours)
- Rep qualifies or rejects within **48 hours**
- Rejected MQLs go to recycling nurture **with reason code** (reason codes feed back into scoring calibration)

**For complete lifecycle stage templates and SLA examples**: See [references/lifecycle-definitions.md](references/lifecycle-definitions.md)

---

## Lead Scoring

### Scoring Dimensions

**Explicit scoring (fit)** — Who they are:
- Company size, industry, revenue
- Job title, seniority, department
- Tech stack, geography

**Implicit scoring (engagement)** — What they do:
- Page visits (especially pricing, demo, case studies)
- Content downloads, webinar attendance
- Email engagement (opens, clicks)
- Product usage (for PLG)

**Negative scoring** — Disqualifying signals:
- Competitor email domains
- Student/personal email
- Unsubscribes, spam complaints
- Job title mismatches (intern, student)

### Building a Scoring Model

1. Define your ICP attributes and weight them
2. Identify high-intent behavioral signals from closed-won data
3. Set point values for each attribute and behavior
4. Set MQL threshold (typically 50-80 points on a 100-point scale)
5. Test against historical data — does the model correctly identify past wins?
6. Launch, measure, and recalibrate quarterly

### Common Scoring Mistakes

- Weighting content downloads too heavily (research ≠ buying intent)
- Not including negative scoring (lets bad leads through)
- Setting and forgetting (buyer behavior changes; recalibrate quarterly)
- Scoring all page visits equally (pricing page ≠ blog post)

**For detailed scoring templates and example models**: See [references/scoring-models.md](references/scoring-models.md)

---

## Lead Routing

### Routing Methods

| Method | How It Works | Best For |
|--------|-------------|----------|
| **Round-robin** | Distribute evenly across reps | Equal territories, similar deal sizes |
| **Territory-based** | Assign by geography, vertical, or segment | Regional teams, industry specialists |
| **Account-based** | Named accounts go to named reps | ABM motions, strategic accounts |
| **Skill-based** | Route by deal complexity, product line, or language | Diverse product lines, global teams |

### Routing Rules Essentials

- Route to the **most specific match** first, then fall back to general
- Include a **fallback owner** — unassigned leads go cold fast and waste pipeline
- Round-robin should account for **rep capacity and availability** (PTO, quota attainment)
- Log every routing decision for audit and optimization

### Speed-to-Lead

Response time is the single biggest factor in lead conversion:
- Contact within **5 minutes** = 21x more likely to qualify (Lead Connect)
- After **30 minutes**, conversion drops by 10x
- After **24 hours**, the lead is effectively cold

Build routing rules that prioritize speed. Alert reps immediately. Escalate if SLA is missed.

**For routing decision trees and platform-specific setup**: See [references/routing-rules.md](references/routing-rules.md)

---

## Pipeline Stage Management

### [Company] Pipeline Stages

the brand uses a seven-stage sales pipeline in Salesforce. Standard ASP is **$85K** (out-of-box pricing).

| Stage | What It Means | Forecast Weight | Key Data |
|-------|--------------|-----------------|----------|
| **Identified** | Demo booked, contact mapped in Salesforce | 0% | Contact info, company, source, ICP fit |
| **Interested** | Demo complete, prospect engaged but not yet committed to evaluation | 10% | Pain points, current stack, decision makers |
| **Pipeline** | Committed to evaluation; $85K ASP assigned | 25% | Technical requirements, timeline, success criteria |
| **Upside** | POV deployed; 50% close rate | 50% (forecasted at $42.5K) | POV environment details, usage metrics, champion identified |
| **Strong Upside** | Technical win achieved, working on budget/procurement | 75% | Budget owner, procurement contact, approval chain |
| **Commit** | Verbal commitment received, waiting for PO | 90% | Expected PO date, contract terms, legal status |
| **Closed Won** | PO received | 100% | Signed PO, payment terms, CS handoff |

**Also track:** `Closed Lost` with required loss reason and competitor (if any).

### The POV Model (Two-Deal Structure)

the brand uses a **Proof of Value (POV)**, not a Proof of Concept. The POV is a paid deployment, not a free trial.

**Deal 1: POV**
- Triggered when a deal moves from Pipeline → Upside (POV deployed)
- Closes at **$85K** (paid POV)
- 50% close rate from this stage

**Deal 2: Expansion**
- A **new opportunity** opens after the POV closes
- Target: **3-year contract at $300K-$500K**
- This is where the real land-and-expand motion happens

When analyzing pipeline, always account for this two-deal structure. A single qualified prospect represents up to $585K in total contract value ($85K POV + $500K expansion), not just the initial $85K.

### Stage Hygiene

- **Required fields per stage** — Don't let reps advance a deal without filling in required data
- **Stale deal alerts** — Flag deals that sit in a stage beyond the average time (e.g., 2x average days)
- **Stage skip detection** — Alert when deals jump stages (Identified → Pipeline skipping Interested/demo)
- **Close date discipline** — Push dates must include a reason; no silent pushes
- **POV tracking** — Every deal in Upside or beyond must have POV deployment date and success criteria documented

### Pipeline Metrics

| Metric | What It Tells You | [Company] Context |
|--------|-------------------|----------------|
| Stage conversion rates | Where deals die | Watch Interested→Pipeline (commitment gap) and Upside→Strong Upside (technical win rate) |
| Average time in stage | Where deals stall | POV stage (Upside) often longest; set expectations accordingly |
| Pipeline velocity | Revenue per day through the funnel | Calculate separately for POV deals and expansion deals |
| Coverage ratio | Pipeline value vs. quota (target 3-4x) | Use weighted pipeline ($42.5K per Upside deal, not $85K) |
| Win rate by source | Which channels produce real revenue | Track through to expansion close, not just POV close |
| POV-to-expansion rate | How many POVs convert to multi-year contracts | Core health metric for the land-and-expand motion |

---

## CRM Automation Workflows

### Essential Automations

- **Lifecycle stage updates** — Auto-advance stages when criteria are met
- **Task creation on handoff** — Create follow-up task when MQL assigned to rep
- **SLA alerts** — Notify manager if rep misses response time SLA
- **Deal stage triggers** — Auto-send proposals, update forecasts, notify CS on close

### Marketing-to-Sales Automations

- **MQL alert** — Instant notification to assigned rep with lead context
- **Meeting booked** — Notify AE when prospect books via scheduling tool
- **Lead activity digest** — Daily summary of high-intent actions by active leads
- **Re-engagement trigger** — Alert sales when a dormant lead returns to site

### Calendar Scheduling Integration

- **Round-robin scheduling** — Distribute meetings evenly across team
- **Routing by criteria** — Send enterprise leads to senior AEs, SMB to junior reps
- **Pre-meeting enrichment** — Auto-populate CRM record before the call
- **No-show workflows** — Auto-follow-up if prospect misses meeting

**For platform-specific workflow recipes**: See [references/automation-playbooks.md](references/automation-playbooks.md)

---

## Deal Desk Processes

### When You Need a Deal Desk

- Discounts below the **$85K** standard ASP
- Non-standard payment terms (net-90, quarterly billing)
- Multi-year contracts with custom pricing (expansion deals at $300K-$500K have more variability)
- Volume discounts beyond published tiers
- Custom legal terms or SLAs

### Approval Workflow Tiers

| Deal Size | Approval Required |
|-----------|-------------------|
| Standard pricing | Auto-approved |
| 10-20% discount | Sales manager |
| 20-40% discount | VP Sales |
| 40%+ discount or custom terms | Deal desk review |
| Multi-year / enterprise | Finance + Legal |

### Non-Standard Terms Handling

Document every exception. Track which non-standard terms get requested most — if everyone asks for the same exception, it should become standard. Review quarterly.

---

## Data Hygiene & Enrichment

### Dedup Strategy

- **Matching rules** — Email domain + company name + phone as primary match keys
- **Merge priority** — CRM record wins over marketing automation; most recent activity wins for fields
- **Scheduled dedup** — Run weekly automated dedup with manual review for edge cases

### Required Fields Enforcement

- Enforce required fields at each lifecycle stage
- Block stage advancement if fields are empty
- Use progressive profiling — don't require everything upfront

### Enrichment Tools

| Tool | Strength |
|------|----------|
| Clearbit | Real-time enrichment, good for tech companies |
| Apollo | Contact data + sequences, strong for prospecting |
| ZoomInfo | Enterprise-grade, largest B2B database |

### Quarterly Audit Checklist

- Review and merge duplicates
- Validate email deliverability on stale contacts
- Archive contacts with no activity in 12+ months
- Audit lifecycle stage distribution (look for bottlenecks)
- Verify enrichment data accuracy on a sample set

---

## RevOps Metrics Dashboard

### Key Metrics

| Metric | Formula / Definition | Benchmark |
|--------|---------------------|-----------|
| Lead-to-MQL rate | MQLs / Total leads | 5-15% |
| MQL-to-SQL rate | SQLs / MQLs | 30-50% |
| SQL-to-Opportunity | Opportunities / SQLs | 50-70% |
| Pipeline velocity | (# deals x avg deal size x win rate) / avg sales cycle | $85K ASP; weight by stage |
| CAC | Total sales + marketing spend / new customers | LTV:CAC > 3:1 |
| LTV:CAC ratio | Customer lifetime value / CAC | 3:1 to 5:1 healthy |
| Speed-to-lead | Time from form fill to first rep contact | < 5 minutes ideal |
| Win rate | Closed-won / total opportunities | 20-30% (varies) |

### Dashboard Structure

Build three views:
1. **Marketing view** — Lead volume, MQL rate, source attribution, cost per MQL
2. **Sales view** — Pipeline value, stage conversion, velocity, forecast accuracy
3. **Executive view** — CAC, LTV:CAC, revenue vs. target, pipeline coverage

---

## Output Format

**Output location:** `marketing/plans/revops/[topic-slug]/` — confirm the project slug with the user before creating files.

When delivering RevOps recommendations, provide:

1. **Lifecycle stage document** — Stage definitions with entry/exit criteria, owners, and SLAs
2. **Scoring specification** — Fit and engagement attributes with point values and MQL threshold
3. **Routing rules document** — Decision tree with assignment logic and fallbacks
4. **Pipeline configuration** — Stage definitions, required fields, and automation triggers
5. **Metrics dashboard spec** — Key metrics, data sources, and target benchmarks

Format each as a standalone document the user can implement directly. Include platform-specific guidance when the CRM is known.

---

## Task-Specific Questions

1. What CRM platform are you using (or planning to use)?
2. How many leads per month do you generate?
3. What's your current MQL definition?
4. Where do leads get stuck in your funnel?
5. Do you have SLAs between marketing and sales today?

---

## Tool Integrations

For implementation, see the [tools registry](../../tools/REGISTRY.md). Key RevOps tools:

| Tool | What It Does | Guide |
|------|-------------|-------|
| **HubSpot** | CRM, marketing automation, lead scoring, workflows | [hubspot.md](../../tools/integrations/hubspot.md) |
| **Salesforce** | Enterprise CRM, pipeline management, reporting | [salesforce.md](../../tools/integrations/salesforce.md) |
| **Calendly** | Meeting scheduling, round-robin routing | [calendly.md](../../tools/integrations/calendly.md) |
| **SavvyCal** | Scheduling with priority-based availability | [savvycal.md](../../tools/integrations/savvycal.md) |
| **Clearbit** | Real-time lead enrichment and scoring | [clearbit.md](../../tools/integrations/clearbit.md) |
| **Apollo** | Contact data, enrichment, and outbound sequences | [apollo.md](../../tools/integrations/apollo.md) |
| **ActiveCampaign** | Marketing automation for SMBs, lead scoring | [activecampaign.md](../../tools/integrations/activecampaign.md) |
| **Zapier** | Cross-tool automation and workflow glue | [zapier.md](../../tools/integrations/zapier.md) |

---

## Related Skills

- **cold-email**: For outbound prospecting emails
- **email-sequence**: For lifecycle and nurture email flows
- **pricing-strategy**: For pricing decisions and packaging
- **tracking-setup**: For tracking pipeline metrics and attribution
- **launch-strategy**: For go-to-market launch planning
- **sales-enablement**: For sales collateral, decks, and objection handling

---

## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->

- **[MEDIUM]** ZeroBounce can false-positive on enterprise domains with strict MX configs or greylisting. Always spot-check flagged high-value contacts (F500, named targets, active deal contacts) against LinkedIn or the company directory before hard-suppressing — some "invalid" results are real CRM typos (catch those), but some are real addresses behind strict mail servers. *(Session 98, 2026-04-22)*
