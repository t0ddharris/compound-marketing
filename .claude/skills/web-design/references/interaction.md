# Interaction

Hover, focus, active, keyboard, forms. Everything the user touches.

## Base rules

- **Every interactive element needs four visible states:** default, hover, focus-visible, active. No exceptions. Disabled is a fifth when applicable.
- **Global transition is `all 0.3s`** (production value). Don't ship custom durations without reason.
- **Cursor: pointer** on every clickable non-button element (cards, links styled as cards, etc.). Buttons get it by default.
- **pointer-events: auto** on buttons — matches the production button component.

## Buttons

See brand-guide for variants. Interaction rules on top of that:

- Hover changes background (not border, not text) for primary/secondary. Use the hover values from brand-guide — typically the same hue shifted one step (darker on light accents, lighter on dark ones). Never invent a hover color.
- Tertiary/ghost hover uses a low-opacity tint of a brand color (~5% opacity; active ~8%).
- Transparent variant uses `text-decoration: underline` on hover — no background change.
- Disabled: `opacity: 0.5; cursor: not-allowed;`.
- Never change the button's size or border-radius on hover. Movement belongs in motion.md.

## Cards (clickable)

- Hover = border color shifts one step brighter/darker (use the brand-guide's default and hover border values). That's the whole hover treatment — don't add shadow, scale, or translate unless there's a reason.
- The whole card is the click target. Don't put a small "Read more" button inside a clickable card — double target, ambiguous.
- If the card has a CTA button visually, still make the whole card clickable; the button is visual affordance.

## Focus rings

- **Never `outline: none` without a replacement.** Keyboard users need a visible focus state.
- Default focus ring: `outline: 2px solid var(--accent); outline-offset: 2px;` (use the brand accent). On accent-colored surfaces, invert: use the canvas color for the ring.
- `:focus-visible` only — not `:focus`. Mouse clicks should not trigger the ring.
- Cards, buttons, links, form inputs all need focus rings.

## Keyboard nav

- Tab order must follow visual order. If the DOM is out of order, fix the DOM — don't use `tabindex` to patch it.
- Skip links for any page with substantial nav.
- Modal open → trap focus inside, return focus to trigger on close. Escape closes.
- Dropdowns: arrow keys navigate, Enter selects, Escape closes.

## Forms

- Labels are always visible. Placeholders are not labels — they disappear on focus.
- Label above input (not floating, not inline-left). Production pattern is top-aligned.
- Required fields marked with `*` **and** `aria-required="true"`.
- Error states: red border + error message below the field, not a tooltip. Error message has `aria-live="polite"`.
- Submit button disabled state only when the form is actually unsubmittable — don't gate on "all fields filled," gate on "all fields valid."
- After successful submission, the page should visibly change (redirect, success state, cleared form). Silence is a broken form.

## HubSpot form renderer note

Production HubSpot forms use the **new renderer** with `hsfc-*` prefixed classes, not legacy `.hs-form` / `.hs-input`. Key classes: `.hsfc-FormWrapper`, `.hsfc-Step`, `.hsfc-Step__Content`, `.hsfc-Row`. Internal padding via `--hsf-background__padding` CSS variable. Form CSS loads dynamically at runtime AFTER `<head>` styles — place overrides in a `<style>` block AFTER `{{ standard_footer_includes }}` to win the cascade. See `hubspot-landing-page` skill for full fix.

## Links in body copy

- Underlined (subtle) or teal. Pick one per page and stick with it.
- Hover: if underlined, add weight or color; if teal, darken slightly or underline.
- External links in new tab **only** when the user would lose context otherwise. Don't blanket `target="_blank"`.

## Modals

- Dark overlay at ~70% opacity over dark page is fine.
- Close button top-right, minimum 44×44 touch target.
- Click outside closes (unless it's destructive — then require explicit close).
- Escape closes. Focus trapped. Return focus to trigger on close.
