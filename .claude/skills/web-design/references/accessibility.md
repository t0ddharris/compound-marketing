# Accessibility

Minimums. These are non-negotiable; the skill should never ship code that fails these.

## Semantic HTML first

- One `<h1>` per page, and it's the page topic. Don't skip heading levels.
- `<button>` for actions, `<a>` for navigation. Never a styled `<div>` with a click handler.
- Lists are `<ul>` / `<ol>`, not `<div>` with bullets.
- Forms use `<label for="id">` paired to inputs. No bare inputs.
- Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`, `<section>` with `aria-labelledby`.

## Contrast

WCAG AA minimum: 4.5:1 for body text, 3:1 for large text (18px+ bold or 24px+ regular).

Build a contrast matrix for your brand palette the first time you work with it, and record it in `brain/brand-guide/brand-guide.md`: check every text color against every surface it appears on, and note which pairings pass AA for body text, which only pass for large text, and which are decoration-only. Common failure: mid-saturation purples and mid-greys on dark canvases sit near ~4:1 and fail body-text AA while looking fine to the eye.

When in doubt, run the swatch through a contrast checker. Never ship accent-colored body text — accents are for emphasis and interactive elements.

## Focus rings

Every interactive element needs `:focus-visible`. See interaction.md. Never `outline: none` without a replacement.

## ARIA (only when semantic HTML isn't enough)

- **First rule of ARIA: don't use ARIA.** Native HTML elements have the correct roles built in. Only reach for ARIA when you have no alternative.
- `aria-label` for icon-only buttons (`<button aria-label="Close">✕</button>`).
- `aria-live="polite"` for form errors and success messages appearing dynamically.
- `aria-current="page"` for the active nav item.
- `aria-expanded` / `aria-controls` for accordion and dropdown triggers.
- Modal: `role="dialog"` + `aria-modal="true"` + `aria-labelledby` pointing to the modal title.

## Images

- Every `<img>` has `alt`. Decorative images: `alt=""` (not missing, empty).
- Meaningful images: alt describes what the image conveys, not what it looks like. "Diagram showing the product detecting an AI agent attack on an API endpoint" > "Diagram".
- SVG icons that are decorative: `aria-hidden="true"`. Functional SVG icons: `role="img"` + `<title>`.

## Keyboard

- Tab order matches visual order.
- Skip link at the top of every page: `<a href="#main">Skip to main content</a>`.
- Every interactive element reachable by Tab.
- Escape closes modals, menus, dropdowns.

## Reduced motion

See motion.md. Wrap animations in `@media (prefers-reduced-motion: reduce)`.

## Forms

- Labels always visible.
- Required fields marked with both `*` and `aria-required="true"`.
- Errors associated with fields via `aria-describedby`.
- Error messages live in `aria-live="polite"` region.

## Quick audit checklist (for the audit workflow)

1. Tab through the page with keyboard. Every interactive element reachable? Visible focus ring?
2. Screen-reader spot check: does the page's structure make sense read top to bottom?
3. Zoom to 200%. Does it still work? Any text cut off?
4. All images have alt? Decorative ones empty, meaningful ones descriptive?
5. Color contrast passes on all text?
6. Animations respect `prefers-reduced-motion`?
7. Form: labels visible, errors announced, submit works via keyboard?
