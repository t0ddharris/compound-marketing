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
3. Call out specific issues: hierarchy, spacing rhythm, alignment, interaction clarity, visual weight. Reference concrete brand-guide values when relevant (e.g., "tag should be `.od-tag--outline--sm` at 2px 8px per brand-guide").
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
2. Check: heading level → correct size, weight 600 for titles, weight 500 for buttons, 400 for body. Letter-spacing negative on titles (`-1.72px` desktop / `-0.8px` mobile), positive on body (`0.4px` / `0.3px`).
3. Mini titles must be `uppercase`. Gradient headlines use three-color gradient **only** via `background-clip: text`.
4. Mobile sizes are smaller — don't use desktop scale on mobile.

### Layout (spacing / rhythm pass)
Used when asked to fix spacing, alignment, or "rhythm feels off."
1. Check max-width: `1080px` centered.
2. Section padding: desktop `64px 32px`, mobile `32px 16px`.
3. All gaps come from the scale. If a gap is `20px`, it's probably wrong — round to `16px` or `24px` with a reason.
4. Vertical rhythm between sections should be consistent. A short section followed by a very tall section with the same padding often reads as broken — adjust the smaller section up.
5. Card border-radius is always `32px`. Buttons `12px`. Tags `5px`. No `999px`.

## Design verification is mandatory

**Every design change to a shipped page must be verified with `agent-browser` before declaring it done.** This is a hard rule (see memory: HubSpot form renderer incident). Class names in source != class names in the live DOM. Snapshot the live page, confirm the change rendered, confirm nothing else regressed.

## Non-negotiables (fast lookup)

Pulled forward from brand-guide + project memory. If you see any of these in a page, fix them:

- **No gradient accent lines / dividers / rules.** Gradient only on text via `background-clip: text`. (Hard rule from memory.)
- **No three-color gradient on non-text surfaces.** Two-color `#50F6E8 → #8B55FF` for UI decorations; three-color for text effects only.
- **No pill shapes (`border-radius: 999px`).** Tags are `8px`, buttons `12px`, cards `32px`.
- **No tag variants outside the three in brand-guide** (`.od-tag`, `.od-tag--outline`, `.od-tag--outline--sm`). No pink/purple tags.
- **No `backdrop-filter: blur()`** in any design that could be exported to PDF (Chromium print renderer ignores it).
- **No "kernel-level" language** in any copy examples in this skill or pages it produces. Use "non-human adversary." (Memory feedback.)
- **No cards inside cards.** If content needs sub-grouping, use spacing, borders, or background tint — not nested card containers.
- **No Inter + purple gradient + centered-hero default.** That's the generic-AI look even if Inter is our font.
- **No invented border colors.** Borders are one of two values from brand-guide: soft `1px solid rgba(69, 69, 69, 0.5)` for section dividers / inline separators, or opaque `1px solid #454545` for card containers. Nothing else.
- **No opaque sticky headers and no legacy blur values.** The site header is always translucent (`rgba(15, 15, 15, 0.4)`) with `backdrop-filter: blur(12px)` — see brand-guide "Site Header" for the full spec. Use the pattern from `go.[your-site]/request-a-demo-thanks`.

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

Tune the `translateY` values per image height and desired peek amount. The `1.5s` animation delay prevents the bounce from firing during page load animations. First shipped on the CNCF happy hour landing page (2026-04-16).

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

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->

- **[HIGH]** Before building CSS/Canvas approximations of production visuals, check if the actual assets can be pulled from the live site. Pre-rendered Spline scenes at `[your-site]/assets/renders/` are SVGs with embedded PNGs; extract layers with base64 decode when needed for compositing. *(Session 85, 2026-04-16)*
- **[HIGH]** For dark-mode assets (particle renders, Spline scenes) on light backgrounds, use `filter: invert(1) hue-rotate(180deg)` directly on the image. Don't wrap in dark containers/bands/panels. *(Session 87, 2026-04-17)*
