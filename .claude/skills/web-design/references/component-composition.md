# Component Composition

How production pages are built. Pull patterns from `[your-site-repo-path]/src/`, don't invent parallels.

## Canonical source

- **Theme:** `src/styles/theme.ts` — colors, typography, spacing tokens
- **Styled layout primitives:** `src/styles/styled.ts`
- **Buttons:** `src/components/button/` (+ named variants `contact-us-button`, `quickstart-button`, `watch-demo-button`, etc.)
- **Cards:** `src/components/card/`
- **Tags:** `src/components/tags/`
- **Text layers:** `src/components/text-layers/` — titles, body, labels
- **Modal:** `src/components/modal/`
- **Inputs:** `src/components/input/`, `src/components/text-area/`
- **Containers:** `src/containers/` — full page sections

**Process:** before building something new, grep the components and containers directories. If there's a close match, extend or compose it. Don't fork.

## Styling approach

[your-site-repo] uses `styled-components` with a theme provider. Pattern:

```tsx
import styled, { css } from 'styled-components';

const Wrapper = styled.div<{ $variant: 'a' | 'b' }>`
  background: ${({ theme }) => theme.colors.black};
  padding: ${({ $variant }) => ($variant === 'a' ? '64px 32px' : '32px 16px')};
  ${({ $variant }) => $variant === 'a' && css`border: 1px solid ${({ theme }) => theme.colors.grey_darker};`}
`;
```

Transient props (`$variant`) prevent prop leaking to DOM. Use them for all styled-component-only props.

## Theme tokens

Never hardcode hex values in components. Pull from the theme:

```tsx
background: ${({ theme }) => theme.colors.accent};
color: ${({ theme }) => theme.colors.text};
border: 1px solid ${({ theme }) => theme.colors.border};
```

If a color you need isn't in the theme, add it to `theme.ts` with a semantic name — don't inline.

## Responsive via `useMobile()`

The production pattern is a `useMobile()` hook + `$isMobile` prop, not strict CSS media queries for component-level changes. Example from `button/index.tsx`:

```tsx
const { isMobile } = useMobile();
// ...
padding: ${({ $padding, $isMobile }) => $padding || ($isMobile ? '8px 18px' : '8px 24px')};
```

Use this pattern for any component that needs different behavior, not just different sizing. For pure CSS layout shifts (grid → column), use media queries.

## Card nesting rule

**No cards inside cards.** If a card needs internal grouping:
- Use spacing (`gap: 16px`) to separate groups
- Use a thin border between groups (`border-top: 1px solid ${grey_darker}`)
- Use a subtle background tint (`background: rgba(255,255,255,0.02)`)

Never nest a `.card` container inside another `.card` container. It reads as indecision and breaks the card radius rhythm.

## Section pattern

Every full-page section follows the same skeleton:

```tsx
<Section>
  <SectionInner>
    <Eyebrow>OPTIONAL OUTLINED TAG</Eyebrow>
    <SectionTitle>The headline</SectionTitle>
    <SectionDescription>Supporting copy.</SectionDescription>
    <SectionContent>{/* cards, grid, image, etc. */}</SectionContent>
    <SectionCta><Button /></SectionCta>
  </SectionInner>
</Section>
```

- `Section` handles full-bleed background + top/bottom padding
- `SectionInner` caps at the brand's max content width and applies side padding
- Every level of the tree uses the gap/spacing scale, no one-off values

## When to create a new component

Create a new component when:
- The same JSX pattern appears 3+ times
- A pattern has non-trivial logic (form validation, state machine, modal behavior)
- A design element has strong semantic meaning ("Quickstart button," "Watch demo button")

Do NOT create a new component for:
- A one-off layout tweak — inline it
- A color variant of an existing component — add a prop
- A slightly different size — add a prop

## Imports

- `@/components/*` for shared UI
- `@/styles` for theme + helpers (`hexOpacity`, etc.)
- `@/contexts` for React contexts (`useMobile`, etc.)
- `@/hooks` for hooks
- `@/functions` for pure utilities
- `next/image` for images, `next/navigation` for routing

Match the existing path alias conventions — don't use relative imports.

## HubSpot landing pages

Net-new HubSpot landing pages don't have React components, but the same spacing/type/color tokens apply. Use CSS custom properties at the top of the template to mirror the theme:

```css
:root {
  /* Fill values from brain/brand-guide/brand-guide.md */
  --canvas: /* primary background */;
  --text: /* primary text */;
  --accent: /* primary accent */;
  --accent-2: /* secondary accent, if any */;
  --gradient: /* decorative gradient, if the brand has one */;
  --gradient-text: /* text-effect gradient, if the brand has one */;
  --radius-tag: /* tag radius */;
  --radius-btn: /* button radius */;
  --radius-card: /* card radius */;
}
```

Then reference those variables in every rule. Makes brand-drift catchable with a single grep.
