# Anti-patterns

Things never to ship. Two categories: generic-AI look (any frontend), and brand-specific bans.

## Generic-AI patterns (ban everywhere)

- **Default Inter + purple gradient + centered hero.** The combo of Inter (or any default sans), a purple gradient, and a centered hero on dark is the ChatGPT-landing-page look — even if some of those ingredients are in your brand. Vary structure: off-center headlines, asymmetric hero grids, non-centered alignment.
- **Cards inside cards.** A card container nested inside another card container. Breaks the radius rhythm and reads as indecision. Use spacing or borders for sub-grouping.
- **Gray text on colored backgrounds.** Low-contrast, lazy hierarchy. Pick white or near-white, or use opacity on white.
- **Bounce / elastic / spring easing on UI transitions.** Dated. Use `ease-out` or linear.
- **`border-radius: 999px` on anything** the brand guide doesn't define as a pill. Use the brand's tag/button/card radii.
- **Centered everything.** Vary alignment. Left-align when it makes sense. Centered is a valid choice, not a default.
- **`backdrop-filter: blur()` used for aesthetics.** Tacky when overused, ignored by Chromium's PDF renderer (things vanish). Justify every use.
- **Gradient backgrounds covering whole sections.** Gradient loses impact when it's everywhere. It's an accent, not a canvas.
- **Rotating / orbiting / pulsing decorative elements.** Pulling focus away from content is never worth it.
- **"Hero + three feature cards + testimonial row + CTA" without variation.** That's the generic layout. Add variety: long-form paragraphs, diagrams, code blocks, large quotes, full-width visuals.
- **Lorem ipsum or placeholder copy in mockups.** Use real copy from brain files. Placeholder copy hides real length problems.
- **Floating labels on form fields.** Looks clever, accessibility trap, labels often clip at small viewports. Use top-aligned labels.

## Brand-specific bans

Universal bans that apply regardless of brand:

- **No full-spectrum rainbow lines/shapes.** 3+ brand colors on a single line or shape reads as a rainbow. Never acceptable.
- **No tag/button/card variants outside those defined in brand-guide.** If you need a different emphasis, use a different element type — not a new variant.
- **No `backdrop-filter: blur()`** on any page or component that might be exported to PDF. Chromium print renderer ignores it and elements disappear.
- **No accent-colored body text.** Accent colors are for emphasis and interactive elements, not reading text.
- **No accusatory language toward readers** in any marketing copy. Don't imply the reader has outages, failures, or bad engineering. This is a CLAUDE.md rule.
- **No prospect quotes or named company references** in public content without approval. The audience-language brain file is tone/vocab only.

**Add your brand's own hard rules below as they accumulate** (via `/reflect` or design feedback). Good examples of the kind of rule that belongs here: which gradient variants are allowed on which surfaces, which colors are tertiary/text-only, which button color is the site default, banned words or framings in demo copy.

- [FILL IN — brand-specific bans discovered as you work]

## The "generic AI landing page" smell test

If the page has:
- Centered hero with gradient-text headline
- Three equal feature cards with icons
- A logo strip
- Testimonial with blurred avatar
- Big gradient CTA section
- Footer

...it's the generic AI layout. That's the starting skeleton, not a finished page. Vary something: non-centered hero, asymmetric feature section, inline diagrams, long-form explanation between cards, code blocks, product screenshots with real labels. Production pages should feel deliberate and specific to the product, not templated.
