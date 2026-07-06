---
name: web-design
description: Live interactive web craft for the company — Next.js landing pages, HubSpot landing pages, and any production web UI. Use when building, reviewing, or polishing web components and pages that will ship to a browser. Covers interaction, responsive, motion, accessibility, composition, state, and brand-specific anti-patterns. Trigger on "build a page," "web design," "polish this page," "audit this page," "this hero feels off," "responsive issue," "hover state," "loading state," or any critique of shipped web UI. Beats Anthropic's `frontend-design` plugin for any on-brand work. NOT the primary skill for: static creative assets (use `brand-design`), HubSpot email templates (use `hubspot-email` — it references accessibility.md and anti-patterns.md from this skill), or HubSpot template mechanics (use `hubspot-landing-page` — pairs with this skill for the craft layer).
---

# web-design — web craft

## Read brand-guide FIRST

**Before doing anything in this skill, read `./brain/brand-guide/brand-guide.md`.**

That file is authoritative for colors, typography, gradients, buttons, tags, cards, spacing, shadows, and dark-theme rules. This skill does **not** redefine any of those. If you find yourself about to write a hex code, type scale, or button variant into a page, stop — reference brand-guide instead.

Production source of truth for component patterns: `[your-site-repo-path]/src/`.

## Scope

**In scope:**
- Next.js landing pages in `[your-site-repo-path]`
- Net-new HubSpot landing page HTML/CSS (coordinate with `hubspot-landing-page` for template mechanics)
- React/styled-components component work for on-brand web UI
- Critiquing and polishing shipped web pages ([your-site], go.[your-site])
- Interaction, motion, responsive, accessibility for production web

**Out of scope — use the right skill instead:**
- Static creative assets (LinkedIn ads, carousels, banners, slide graphics) → `brand-design`
- HubSpot email HTML → `hubspot-email`
- HubSpot template variables, Design Manager, HubL syntax → `hubspot-landing-page`
- CTA button modules in HubSpot → `hubspot-cta`
- AI-generated illustrations and imagery → `image-gen`
- Copy on a page → `copywriting` / `copy-editing`

## Reference files

Load the reference file for the problem you are solving. Do not load all of them.

- [interaction.md](references/interaction.md) — hover, focus, active, keyboard, forms
- [responsive.md](references/responsive.md) — breakpoints, fluid type, mobile rules
- [motion.md](references/motion.md) — transitions, easing, reduced-motion
- [accessibility.md](references/accessibility.md) — a11y minimums, ARIA, focus rings, contrast
- [component-composition.md](references/component-composition.md) — [your-site-repo] patterns, card nesting rules
- [state-patterns.md](references/state-patterns.md) — loading, empty, error, success
- [anti-patterns.md](references/anti-patterns.md) — generic-AI patterns to avoid + brand-specific bans

## Workflows (run the one that matches the ask)

When the user asks for review, polish, or critique, pick the workflow that matches. Don't announce the workflow — just do it.

### Audit (technical quality)
Used when asked to "audit," "check," or "review" a page for correctness.
1. Load `accessibility.md`, `responsive.md`, `interaction.md`.
2. Open the live page with `agent-browser` and snapshot it. **Mandatory** for any shipped page — don't audit from source alone, class names drift.
3. Check in this order: semantic HTML, heading hierarchy, focus rings, keyboard nav, contrast, responsive breakpoints, form behavior, hover/active states, reduced-motion.
4. Report findings grouped by severity. Don't fix without approval unless the user said "fix."

### Critique (design judgment)
Used when asked "what's wrong with this" or "does this feel right."
1. Load `anti-patterns.md` and `component-composition.md`.
2. Compare the page against brand-guide and landing-page patterns.
3. Call out specific issues: hierarchy, spacing rhythm, alignment, interaction clarity, visual weight. Reference concrete brand-guide values when relevant (e.g., "tag should be the brand-guide's small outlined variant at its specified padding").
4. Rank issues — lead with the one that would most improve the page.

### Polish (pre-ship pass)
Used before a page ships or when asked to "polish" / "tighten" / "finalize."
1. Load `anti-patterns.md`, `motion.md`, `interaction.md`.
2. Scan for: stray gradient lines, tag variant drift, inconsistent border-radius, missing hover/focus states, off-spec spacing, 999px pill shapes, backdrop-filter in PDF-exportable designs.
3. Apply the brand-guide spacing scale (2/4/8/12/16/24/32/48/64/80/128). Spacing that isn't on the scale needs a reason.
4. Verify transitions use `all 0.3s` (or the production value in use).

### Typeset (typography pass)
Used when asked to fix fonts, hierarchy, or "the text feels wrong."
1. Reference brand-guide type scale directly. Never invent sizes.
2. Check every heading level against the brand-guide's size, weight, and letter-spacing values. Titles, buttons, and body each have defined weights — verify, don't assume.
3. Apply any brand-guide casing rules (e.g., uppercase mini titles). Gradient/accent headline treatments only where the brand guide allows, and text-effect gradients **only** via `background-clip: text`.
4. Mobile sizes are smaller — don't use desktop scale on mobile.

### Layout (spacing / rhythm pass)
Used when asked to fix spacing, alignment, or "rhythm feels off."
1. Check max content width and centering against the brand-guide layout values.
2. Check section padding (desktop and mobile) against the brand-guide values.
3. All gaps come from the brand-guide spacing scale. If a gap isn't on the scale, it's probably wrong — round to the nearest scale value or document a reason.
4. Vertical rhythm between sections should be consistent. A short section followed by a very tall section with the same padding often reads as broken — adjust the smaller section up.
5. Border-radius values come from brand-guide (cards, buttons, tags each have one). No `999px` pills unless the brand guide defines them.

## Design verification is mandatory

**Every design change to a shipped page must be verified with `agent-browser` before declaring it done.** Class names in source != class names in the live DOM (dynamically-loaded CSS, form renderers, and CMS wrappers all rewrite markup at runtime). Snapshot the live page, confirm the change rendered, confirm nothing else regressed.

## Non-negotiables (fast lookup)

Universal rules, plus wherever the brand guide defines a value, that value wins. If you see any of these in a page, fix them:

- **No invented brand values.** Colors, gradients, type sizes, radii, spacing, and borders come from brand-guide. If you're about to type a hex or px value that isn't in brand-guide, stop.
- **Gradients only where the brand guide allows them.** Text-effect gradients only via `background-clip: text`. Never apply a text-only gradient to lines, borders, or backgrounds.
- **No pill shapes (`border-radius: 999px`)** unless the brand guide defines them. Use the brand's tag/button/card radii.
- **No tag or button variants outside those defined in brand-guide.** If you need different emphasis, use a different element type — not a new variant.
- **No `backdrop-filter: blur()`** in any design that could be exported to PDF (Chromium print renderer ignores it).
- **No cards inside cards.** If content needs sub-grouping, use spacing, borders, or background tint — not nested card containers.
- **No generic-AI default look.** Default font + purple gradient + centered dark hero is the ChatGPT-landing-page aesthetic — vary structure even when the ingredients overlap with your brand.
- **No accent-colored body text.** Accent colors are for emphasis and interactive elements, not reading text.
- Record instance-specific bans (banned phrases, banned patterns, header specs) in `references/anti-patterns.md` and brand-guide as they accumulate — this list stays universal.

## Interaction Patterns

### Peek-reveal

An image (or any element) that hides mostly behind a card, peeks out with a subtle bounce to tease interaction, then slides fully into view on hover. On mobile (no hover), show the element statically.

**Key implementation detail:** CSS animations override transitions on the same property. If the bounce and hover both animate `transform` on the same element, the first hover jumps instead of transitioning. Fix: use a tiny JS snippet that adds a class on first mouseenter to kill the animation, letting the CSS transition take over cleanly. This keeps the bounce on the actual container (the whole frame moves, not just content inside it).

```css
.peek-container {
  transform: translateY(14px);          /* mostly hidden behind the card below */
  transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin-bottom: -100px;               /* overlap with card */
  overflow: hidden;
  border-radius: 20px 20px 0 0;
  animation: peekBounce 3s ease-in-out 1.5s infinite;
}
.peek-container.peek-hovered {
  animation: none;                      /* JS adds this on first hover */
}
@keyframes peekBounce {
  0%, 100% { transform: translateY(14px); }
  50% { transform: translateY(6px); }
}
.parent:hover .peek-container {
  transform: translateY(-86px);         /* fully revealed */
}
.card { position: relative; z-index: 1; }

/* Mobile: static, no tricks */
@media (max-width: 960px) {
  .peek-container { transform: none; margin-bottom: 16px; animation: none; }
  .parent:hover .peek-container { transform: none; }
}
```

```js
// Kill bounce animation on first hover so CSS transition takes over
document.addEventListener('DOMContentLoaded', function() {
  var parent = document.querySelector('.parent');
  var peek = document.querySelector('.peek-container');
  if (parent && peek) {
    parent.addEventListener('mouseenter', function() {
      peek.classList.add('peek-hovered');
    }, { once: true });
  }
});
```

Tune the `translateY` values per image height and desired peek amount. The `1.5s` animation delay prevents the bounce from firing during page load animations.

## When building something new

1. Read brand-guide.
2. Find the closest existing component in `[your-site-repo-path]/src/components/`. Copy its patterns — don't invent parallel ones.
3. Load the relevant reference file(s) for the problem.
4. Build.
5. Run the polish workflow on your own output before presenting it.
6. Verify in browser with `agent-browser` if it's shipping.

## Output Location

Built pages go wherever the framework dictates (e.g., `src/` for Next.js). Supporting docs (specs, audit notes) go to `marketing/pages/[page-slug]/` — confirm the project slug with the user before creating files.

---

## Learnings

<!-- Updated by /reflect in your instance. Promote stable patterns to the main skill body. Ships empty. -->
