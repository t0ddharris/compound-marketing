# Anti-patterns

Things never to ship. Two categories: generic-AI look (any frontend), and brand-specific bans.

## Generic-AI patterns (ban everywhere)

- **Default Inter + purple gradient + centered hero.** Inter is our font, but the combo of Inter, a purple gradient, and a centered hero on dark is the ChatGPT-landing-page look. Vary structure: off-center headlines, asymmetric hero grids, non-centered alignment.
- **Cards inside cards.** A card container nested inside another card container. Breaks the 32px radius rhythm and reads as indecision. Use spacing or borders for sub-grouping.
- **Gray text on colored backgrounds.** Low-contrast, lazy hierarchy. Pick white or near-white, or use opacity on white.
- **Bounce / elastic / spring easing on UI transitions.** Dated. Use `ease-out` or linear.
- **`border-radius: 999px` on anything.** Pill buttons, pill tags, pill badges. the brand uses `5px` tags / `12px` buttons / `32px` cards. No pills, ever.
- **Centered everything.** Vary alignment. Left-align when it makes sense. Centered is a valid choice, not a default.
- **`backdrop-filter: blur()` used for aesthetics.** Tacky when overused, ignored by Chromium's PDF renderer (things vanish). Sticky headers get a `blur(2.35px)` per production — beyond that, justify every use.
- **Gradient backgrounds covering whole sections.** Gradient loses impact when it's everywhere. It's an accent, not a canvas.
- **Rotating / orbiting / pulsing decorative elements.** Pulling focus away from content is never worth it.
- **"Hero + three feature cards + testimonial row + CTA" without variation.** That's the generic layout. Add variety: long-form paragraphs, diagrams, code blocks, large quotes, full-width visuals.
- **Lorem ipsum or placeholder copy in mockups.** Use real copy from brain files. Placeholder copy hides real length problems.
- **Floating labels on form fields.** Looks clever, accessibility trap, labels often clip at small viewports. Use top-aligned labels.

## brand-specific bans (hard rules from memory + brand-guide)

- **No gradient accent lines / dividers / rules.** Hard rule. Gradient only on text via `background-clip: text`. No decorative gradient bars.
- **No three-color gradient on non-text surfaces.** Two-color `#50F6E8 → #8B55FF` only for backgrounds/borders/lines. Three-color including pink only on text.
- **No "kernel-level" language** in any copy — landing-page examples, demo content, placeholder strings. Use "non-human adversary." Applies to AI agent attack explanations.
- **No full-spectrum rainbow lines/shapes.** 3+ brand colors on a single line or shape reads as a rainbow. Never acceptable.
- **No pink as a core brand color.** Pink is tertiary, text-only (third stop in the text gradient), and used sparingly for warmth. No pink backgrounds, no pink buttons, no pink tag variants.
- **No tag variants outside the three in brand-guide.** `.od-tag` (solid cyan), `.od-tag--outline`, `.od-tag--outline--sm`. If you need a different emphasis, use a different element type — not a new tag variant.
- **No `backdrop-filter: blur()`** on any page or component that might be exported to PDF. Chromium print renderer ignores it and elements disappear.
- **No teal body text.** Teal is accent/interactive, not a reading color. Use white/off-white for body.
- **No purple primary buttons as the site default.** Teal is the default; purple is the approved alternate for email contexts or dense teal-heavy layouts. Don't flip the convention.
- **No accusatory language toward readers** in any marketing copy. Don't imply the reader has outages, failures, or bad engineering. This is a CLAUDE.md rule.
- **No prospect quotes or named company references** in public content without approval. The audience-language brain file is tone/vocab only.

## The "generic AI landing page" smell test

If the page has:
- Centered hero with gradient-text headline
- Three equal feature cards with icons
- A logo strip
- Testimonial with blurred avatar
- Big gradient CTA section
- Footer

...it's the generic AI layout. That's the starting skeleton, not a finished page. Vary something: non-centered hero, asymmetric feature section, inline diagrams, long-form explanation between cards, code blocks, product screenshots with real labels. Production production pages should feel deliberate and technical, not templated.
