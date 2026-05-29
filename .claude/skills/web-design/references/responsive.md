# Responsive

Mobile is not a smaller desktop. Design the content reflow before you design the big screen.

## Breakpoints (production)

[your-site-repo] uses a mobile-detection hook (`useMobile`) rather than strict breakpoints for JS logic. For CSS:

- **Mobile:** `max-width: 767px`
- **Tablet:** `768px – 1023px`
- **Desktop:** `min-width: 1024px`
- **Max content width:** `1080px` centered

Don't invent new breakpoints for a single element. If something needs a one-off breakpoint, the design is usually wrong.

## Section padding

| | Desktop | Mobile |
|---|---------|--------|
| Top/Bottom | 64px | 32px |
| Left/Right | 32px | 16px |

Never let content touch the edge on mobile. `16px` minimum side padding.

## Type scaling

Pull from brand-guide type scale — desktop and mobile sizes are explicit in the table. A few highlights:

- Extra Large Title: 68px desktop / **40px mobile** (big drop)
- Large Title: 56px / 32px
- Standard Title: 48px / 32px
- Body text: 18px / 16px
- Letter-spacing also changes: titles `-1.72px` desktop → `-0.8px` mobile

**Don't use desktop sizes on mobile.** 68px reads fine on a 27" monitor; on a 390px viewport it's two words per line.

## Layout reflow patterns

- **Multi-column → single column.** Two/three-column grids collapse to one on mobile. Don't try two columns at narrow widths — text becomes unreadable.
- **Side-by-side image + text → stacked.** Image above text on mobile unless the image is decorative (then below).
- **Horizontal card row → vertical stack.** Not carousel on mobile unless there are 5+ cards; carousels hide content and hurt SEO.
- **Desktop nav → hamburger.** Keep the hamburger in a consistent position (top-right).

## Touch targets

- Minimum 44×44px for any tappable element (Apple + WCAG guidance).
- Don't stack two small links vertically with tight spacing — at least 8px gap between tap targets.
- Don't rely on hover for mobile. Anything that only appears on hover doesn't exist on touch devices.

## Images

- Use `next/image` for Next.js pages. Always provide `sizes` for responsive loading.
- Hero images: think about the mobile crop. A wide desktop hero often becomes a mess cropped to square. Provide an art-directed mobile version when it matters.
- Never ship a 4MB PNG. WebP or AVIF, compressed.

## Forms on mobile

- One field per row. Never side-by-side fields on mobile except short pairs like first/last name — and even then, stacked is safer.
- Inputs at least 16px font-size. Anything smaller triggers iOS zoom-on-focus.
- Use correct `inputmode` and `autocomplete` attributes (email, tel, given-name, family-name, organization, postal-code, etc.).

## Avoid

- **Viewport width units (`vw`) for type.** Looks clever, scales badly at extremes. Use the discrete mobile/desktop sizes from brand-guide.
- **`100vh` for full-screen heroes.** Mobile browser chrome makes this jump on scroll. Use `100svh` or a fixed value.
- **Fixed headers taller than 64px on mobile.** Eats screen real estate.
- **Horizontal scroll.** Ever. If a page scrolls horizontally on mobile, something is overflowing its container.
