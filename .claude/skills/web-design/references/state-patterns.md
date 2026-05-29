# State Patterns

Loading, empty, error, success. Every component that fetches, submits, or changes over time needs all four. Missing state = broken UX.

## Loading

- **Never use a bare spinner for initial page content.** Use a skeleton (layout placeholder) that matches the real content shape. Spinners are fine for buttons and short actions.
- Buttons: on submit, disable + replace label with "Submitting…" or spinner glyph. Keep width stable (don't let the button collapse).
- Skeletons use `background: ${grey_darker}` with subtle shimmer or static. Match the real content's dimensions.
- Never block the whole page for a slow fetch. Fetch in parallel where possible, show what you have.

## Empty

- Empty ≠ error. "You don't have any X yet" needs a friendly message, a visual, and a next-step CTA.
- Never show a bare empty div or "No results." Say what's missing and what to do about it.
- Example: search with no results → "No matches for 'foo'. Try fewer words, or browse [popular topics]."

## Error

- Always explain what failed and what the user can do.
- Never: "Something went wrong." Instead: "We couldn't load the page. Check your connection and try again."
- Inline errors (form field) stay near the field. Global errors (network, 500) get a top-level alert or error boundary.
- Provide a recovery action: retry button, go home, contact support. Never a dead-end.
- Log the underlying error for developers. Never show raw stack traces or API error JSON to users.
- Errors get `aria-live="polite"` so screen readers announce them.

## Success

- After successful submission, the UI must visibly change. Options:
  - Redirect to a thank-you page (forms, sign-ups)
  - Show inline success message + clear the form (lightweight submits)
  - Replace the component with a completed-state view (inline edit, save actions)
- Success messages are specific: "Demo requested — we'll email you within 1 business day" beats "Success!".
- Silence after submit is a broken form. The user does not know if it worked.

## Disabled / locked

- Disabled elements must be visually clear (opacity 0.5, cursor not-allowed).
- Include `aria-disabled="true"` or the native `disabled` attribute so screen readers announce it.
- Don't disable without explanation — tooltip or helper text saying why.

## In between

- **Optimistic UI:** update the UI before the server confirms, roll back on error. Good for fast actions (likes, toggles).
- **Debounced loading:** delay showing the spinner for 100-200ms to avoid flicker on fast responses.
- **Stale + loading:** keep old content visible while refreshing in the background, with a subtle indicator.

## Page-level

Every page needs to handle:
- **Loading** (before data arrives) → skeleton or cached placeholder
- **Empty** (data arrived, nothing to show) → empty state
- **Error** (fetch failed) → error state with retry
- **Happy path** (data, rendered) → the design

Missing any one of these = the page silently fails in that scenario. Default to designing all four.
