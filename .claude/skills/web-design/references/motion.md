# Motion

Movement is communication. It clarifies cause-and-effect, shows state change, and guides attention. Bad motion is worse than no motion.

## Defaults

- **Global transition: `all 0.3s`** is a sane default — but match whatever production value your site already uses. Consistency beats the "right" number.
- **Easing: `ease` or `ease-out`** for most UI. Never `ease-in` for things appearing (looks slow starting, fast ending — wrong way). Never bounce / elastic / spring for UI.
- **Hover → 150-300ms.** Entrance → 300-500ms. Exit → 200ms (exits should feel faster than entrances).

## What should move

- State changes: hover, focus, open, close, active. These NEED motion to feel connected to the user's action.
- Scroll-triggered reveals (sparingly). Fade + 12-16px slide up works. Don't animate every section.
- Modal / drawer entry and exit.
- Focus rings on keyboard nav (instant appearance, transition on position if the focus jumps).

## What should not move

- Decorative loops (pulsing glows, floating particles) unless they serve a purpose. Subtle is fine; constant motion in peripheral vision is exhausting.
- The content a user is trying to read.
- Headlines that "type themselves" on every scroll — once on initial load, fine.
- Anything essential to comprehension of the page. If the user has `prefers-reduced-motion`, they should still be able to understand the page.

## Reduced motion

Wrap every animation in a media query:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

For scroll-triggered reveals, have the "final" state be the default — then only animate if `prefers-reduced-motion: no-preference`. This guarantees reduced-motion users see the content without flashes of missing elements.

## Stagger

When multiple elements enter together (card grid reveal, list of bullets), stagger by 50-80ms. More than ~8 elements staggered gets tedious; just fade the whole group in.

## Common motion patterns

- **Card hover:** border color change (default → hover values from brand-guide), no scale, no translate, no shadow.
- **Button hover:** background color change only. No scale, no lift.
- **Hero gradient text:** if the brand has a text gradient, the gradient itself can animate (cycle) — match the existing hero's production pattern. Keep slow (5-10s cycle) and subtle.
- **Section reveal on scroll:** opacity 0 → 1, transform translateY(16px) → translateY(0), 500ms ease-out. One-shot, not on every scroll back.

## Don't

- Bounce / elastic / spring easing on UI. It reads as dated.
- Long durations (>600ms) on routine interactions. Makes the UI feel slow.
- Parallax for its own sake. Almost always hurts more than helps, hurts performance, ignores reduced-motion.
- Infinite rotating elements in the viewport (spinning logos, orbiting dots). Exhausting.
- Entrance animations on every page load for primary content. The user came to read, not watch.
