# Opening Hooks

Use this reference during Step 2 (Outline) of the blog workflow. Select a hook type that matches the post type and audience, then adapt the formula.

A strong opening does two things: (1) signals relevance to the reader and (2) creates enough tension or curiosity that they keep reading.

---

## 1. Pain-Point Hooks

**Formula:** State a specific frustration the reader recognizes from their own experience.

**When to use:** How-to posts, thought leadership, product-related content. Works best when you can describe the pain vividly enough that the reader thinks "that's exactly my situation."

**Examples:**
- "Your SIEM says everything is clean. Your API logs show 4,000 enumeration requests from a single source in the last hour. Your EDR didn't flag any of them."
- "Every incident review ends the same way: 'The traffic looked like normal API usage.' Except normal users don't systematically probe every endpoint in sequence."
- "You spent a year building detection rules for credential stuffing. The AI agent that hit your auth API last Tuesday didn't match a single one."

**Pattern:** [Describe the specific pain] + [Make the consequence visible]

---

## 2. Surprising Stat Hooks

**Formula:** Lead with a specific number or data point that challenges assumptions.

**When to use:** Thought leadership, listicles, comparison posts. The stat must be sourced and verifiable. If you don't have a real stat, use a different hook type.

**Examples:**
- "AI agents can probe thousands of API endpoints in minutes. A human pentester takes days to cover the same surface. Your detection rules were calibrated for the human."
- "Fewer than 15% of enterprise security teams have any detection capability specifically designed for autonomous AI agent attacks. The other 85% are relying on tools built for human adversaries."

**Pattern:** [Specific number with source] + [Why that number matters to the reader]

**Rule:** Every stat must be sourced from `brain/truth.md` or an external source cited inline. Mark unverified stats `[VERIFY]`.

---

## 3. Contrarian Hooks

**Formula:** State what most people believe, then reveal why that belief is wrong or incomplete.

**When to use:** Thought leadership posts. This is the default hook for pieces that challenge conventional wisdom.

**Examples:**
- "Most security teams assume their EDR will catch AI-agent attacks. It won't. EDR was trained on human attacker behavior, and AI agents don't behave like humans."
- "Adding more SIEM correlation rules to catch AI agents sounds logical. But if every rule is pattern-matching against known attack signatures, you're always one step behind an adversary that generates novel attack paths on the fly."

**Pattern:** [State the conventional wisdom] + [Reveal the flaw or blind spot]

**Rule:** The contrarian claim must be defensible. Don't be provocative for its own sake.

---

## 4. Scenario Hooks

**Formula:** Drop the reader into a specific, recognizable situation.

**When to use:** How-to posts, case study-adjacent content, news posts (for context). Works well when the scenario is specific enough to feel real but broad enough that many readers recognize it.

**Examples:**
- "It's 2 AM. PagerDuty fires. Your API gateway is returning 429s, but the traffic pattern doesn't match any known bot signature. Hundreds of unique endpoints probed in a systematic sweep. By the time your SOC analyst opens the dashboard, the agent has already moved to credential testing."
- "Your security team just deployed a new public API. Within 72 hours, an autonomous agent has mapped every endpoint, tested every parameter, and found the one misconfigured permission boundary your pen test missed."

**Pattern:** [Set the scene with specific details] + [Reveal the problem or gap]

---

## 5. Question Hooks

**Formula:** Ask a question the reader already has, or one that exposes a gap in their thinking.

**When to use:** Comparison posts, listicles, thought leadership. The question must be something the reader genuinely cares about — not a rhetorical setup for a sales pitch.

**Examples:**
- "What does your SOC do when an attacker doesn't match any known signature, doesn't trigger rate limits, and uses legitimate API credentials?"
- "If your security tools can't distinguish an AI agent systematically probing your API from a developer testing integrations, what are you actually detecting?"
- "How many of your production APIs are protected against an adversary that adapts its approach based on your responses?"

**Pattern:** [Question that exposes a specific gap or decision] + [Implied stakes]

**Rule:** Don't answer the question immediately in the next sentence. Let it sit for a beat, then build context.

---

## 6. Outcome Hooks

**Formula:** Lead with the end result — what the reader will achieve or understand.

**When to use:** How-to posts, tutorials. This is the default hook for instructional content.

**Examples:**
- "By the end of this guide, your SOC will have a detection pipeline purpose-built for AI agent attacks, integrated with the SIEM and EDR stack you already run."
- "This post walks through how one security team went from zero AI-agent detection capability to blocking automated reconnaissance in production, deployed in under a day."

**Pattern:** [Specific outcome the reader wants] + [Specificity that makes it credible]

---

## Anti-Patterns: Openings to Avoid

These openings signal AI-generated or lazy writing. Never use them.

| Banned Opening | Why It Fails |
|----------------|-------------|
| "In today's fast-paced world..." | Generic filler. Says nothing specific. |
| "In today's digital age..." | Same. Readers have seen this thousands of times. |
| "In the ever-evolving landscape of..." | Throat-clearing. Delays the point. |
| "According to the dictionary, [term] means..." | Dictionary definitions are never a compelling hook. |
| "[Company name] is excited to announce..." | Starting with the company instead of the reader (exception: news posts, where the news lead format is expected). |
| "Imagine a world where..." | Overworn hypothetical. |
| "Have you ever wondered...?" | Weak question that doesn't create tension. |
| "Let me tell you about..." | Breaks fourth wall without earning it. |
| "It's no secret that..." | If it's no secret, it's not worth leading with. |

### What to Do Instead

1. **Start with the reader's world** — their pain, their situation, their decision
2. **Be specific** — name the technology, the scenario, the consequence
3. **Create tension** — something is wrong, something is at stake, something is surprising
4. **Get to the point** — the hook should be in the first 1-2 sentences, not after a paragraph of context
