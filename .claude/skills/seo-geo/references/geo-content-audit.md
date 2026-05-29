# GEO Content Audit (File-Based)

Score a finished content file against the levers that drive AI citation, then apply
fixes directly to the file. This mode is fully self-contained: it reads a Markdown or
HTML artifact in the repo and needs no live site, Search Console, or analytics access.

The score is a **rubric-based readiness heuristic**, not a measured citation rate. The
weights are derived from the relative impact of the 9 Princeton GEO methods (see
SKILL.md Step 4), but the methods are visibility *boosts*, not values that sum to 100.
Treat the number as "how citation-ready is this draft," not "this draft will be cited
X% of the time." Never present it as an empirical prediction.

---

## How to run it

1. **Identify the target file and its content type.** Ask the user, or infer from the
   path and structure. Content type drives which criteria apply (see the matrix below).
2. **Score each applicable criterion** 0 to its max points. Mark criteria that don't
   apply to the content type as **N/A** and exclude their points from the denominator.
3. **Normalize:** `score = round(100 * earned_applicable / total_applicable)`. Excluding
   N/A criteria from the denominator is what keeps a narrative case study from being
   penalized for lacking an FAQ block it was never supposed to have.
4. **Quote the evidence** for each criterion (cite the line or block you scored on).
5. **Write the report** (format below) into the project folder alongside the artifact.
6. **Offer to apply the top fixes** and, if approved, edit the file and commit.

---

## The scorecard (100 points)

### Evidence & Authority — 48 pts

These are the highest-impact Princeton levers, so they carry the most weight.

| Criterion | Max | Full marks when... |
|-----------|----:|--------------------|
| Source citations | 15 | Claims trace to named, authoritative sources (orgs, studies, primary data), not vague "studies show." |
| Statistics with numbers + timeframes | 14 | Specific figures with units and a date/period ("cut triage time 42% in Q1 2026"), not adjectives. |
| Named-attribution quotes | 11 | Direct quotes attributed to a named person + title + org. |
| Authoritative tone | 8 | Confident, specific, expert voice. No hedging, no filler, no marketing puffery. |

### Structure & Extractability — 33 pts

| Criterion | Max | Full marks when... |
|-----------|----:|--------------------|
| Leads with the point | 8 | The key answer/outcome appears at the top, extractable without reading the whole piece. |
| Heading hierarchy | 5 | Clean H1 > H2 > H3; each heading describes what follows. |
| Tables for data | 6 | Comparison or results data is in a table, not buried in prose. |
| Lists | 4 | Steps, features, or points use bullets/numbered lists where appropriate. |
| Short paragraphs | 4 | Paragraphs are 2-3 sentences; no dense walls of text. |
| Self-contained blocks | 6 | Key sections make sense if an AI engine extracts them alone. |

### Schema & Machine-Readability — 11 pts

| Criterion | Max | Full marks when... |
|-----------|----:|--------------------|
| Appropriate schema | 8 | The right schema type for the content (see matrix) is present or specified. |
| Clean metadata | 3 | Title, meta description, and headings are present and descriptive. |

### Language Quality — 8 pts

| Criterion | Max | Full marks when... |
|-----------|----:|--------------------|
| Fluency & readability | 4 | Reads smoothly; varied sentence structure; no AI-tell patterns. |
| Domain terminology | 2 | Uses correct domain-specific terms a buyer/engine would expect. |
| Vocabulary diversity | 2 | No keyword stuffing (an active GEO penalty), no repetitive phrasing. |

---

## Content-type applicability matrix

Score only the criteria that apply to the content type. Reframe, don't penalize: a case
study "leads with the point" by leading with the **headline result**, not by being
answer-first like an FAQ.

| Criterion | Case study | Blog / guide | Comparison / alt page | Landing page |
|-----------|:----------:|:------------:|:---------------------:|:------------:|
| Source citations | ✓ | ✓ | ✓ | optional |
| Statistics + timeframes | ✓ (results metrics) | ✓ | ✓ | ✓ |
| Named-attribution quotes | ✓ (customer quote) | ✓ | optional | ✓ (testimonial) |
| Authoritative tone | ✓ | ✓ | ✓ | ✓ |
| Leads with the point | ✓ (headline result) | ✓ | ✓ | ✓ |
| Heading hierarchy | ✓ | ✓ | ✓ | ✓ |
| Tables for data | ✓ (before/after metrics) | optional | ✓ (feature matrix) | optional |
| Lists | ✓ | ✓ | ✓ | ✓ |
| Short paragraphs | ✓ | ✓ | ✓ | ✓ |
| Self-contained blocks | ✓ (key outcomes box) | ✓ | ✓ | optional |
| Appropriate schema | `CaseStudy` / `Article` | `Article` / `FAQPage` | `FAQPage` / `Product` | `WebPage` / `Product` |
| Clean metadata | ✓ | ✓ | ✓ | ✓ |
| Fluency & readability | ✓ | ✓ | ✓ | ✓ |
| Domain terminology | ✓ | ✓ | ✓ | ✓ |
| Vocabulary diversity | ✓ | ✓ | ✓ | ✓ |

**N/A** any criterion marked "optional" if the piece reasonably omits it; drop its points
from the denominator. `FAQPage` schema is N/A for a case study; score it on `CaseStudy`
or `Article` schema instead.

### Why case studies are a strong demo target

A well-written case study already scores high on the heaviest levers: a named customer
quote (+30%), results statistics (+37%), and authoritative tone (+25%). That gives an
honest optimization story rather than a teardown. The usual gains:

- Add a **results-stat block** at the top (the headline metric, sourced to the customer).
- Add a **self-contained "Key outcomes" section** that an engine can lift verbatim.
- Specify **`CaseStudy` / `Article` schema** instead of leaving structured data off.
- Move a buried before/after metric into a small **results table**.

That is the punchline: even a narrative format can be made more citable, without turning
it into a listicle.

---

## Score bands

| Band | Score | Meaning |
|------|:-----:|---------|
| Citation-ready | 90-100 | Strong on every applicable lever. Ship it. |
| Strong | 75-89 | Solid; a few targeted additions raise it. |
| Developing | 50-74 | Real gaps in evidence or structure. Worth a fix pass. |
| Weak | 0-49 | Missing the core citation levers. Rework before publishing. |

---

## Report format

Write this to the project folder as `geo-audit.md`, and a machine-readable
`geo-audit.json` alongside it.

```
## GEO Content Audit — [file name]

**Content type:** [case study / blog / comparison / landing page]
**GEO readiness score:** [N]/100 — [band]
*(Rubric-based heuristic, not a measured citation rate.)*

### Scorecard
| Criterion | Score | Evidence | Fix |
|-----------|:-----:|----------|-----|
| Source citations | 9/15 | "studies show faster triage" — no source named (line 24) | Cite the source or replace with an internal proof point from truth.md |
| ... | ... | ... | ... |
| FAQPage schema | N/A | Not applicable to case studies | — |

### Top fixes (by impact)
1. [Highest-impact gap] — [specific, file-level change]
2. ...
3. ...

### Apply?
"I can make these edits to [file] and commit. Want me to proceed?"
```

The `geo-audit.json` mirrors the scorecard:

```json
{
  "file": "marketing/case-studies/acme/case-study.md",
  "contentType": "case-study",
  "score": 71,
  "band": "developing",
  "criteria": [
    { "name": "source-citations", "max": 15, "earned": 9, "applicable": true,
      "evidence": "line 24", "fix": "Cite source or use truth.md proof point" },
    { "name": "faq-schema", "applicable": false }
  ]
}
```

---

## Applying fixes

When the user approves:

- Make the edits directly in the target file (add the stat block, outcomes section,
  citations, table, schema). Pull all factual claims from `/brain/` — never invent a
  statistic or source to raise the score.
- For schema, hand off to or follow `schema-markup` for the JSON-LD.
- For prose-quality fixes, run `tagore` on the rewritten passages.
- Re-score after editing and show the before/after (e.g., 71 → 88).
- Run Vale on the edited file, then commit.
