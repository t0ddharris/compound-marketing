# HTML Template Guide — Lookalike Content Ideas

This document describes how to generate the HTML versions for both the winning content profile and the content ideas output.

## Requirements (Both Files)

- **Single file** — all CSS inline in a `<style>` block
- **One Google Font** — load via CDN. Use `DM Sans`, `Plus Jakarta Sans`, `Outfit`, or `Sora`. Do NOT use Inter, Roboto, or Arial.
- **No JavaScript required** — static document
- **Print-friendly** — include `@media print` rules

---

## Winning Content Profile HTML

### Design Direction

This is an insight document — think of it as a research report that a strategist would reference before creating content. Clean, scannable, data-forward.

### Layout

- Max-width: `780px`, centered
- The "Winning Formula" (Section 10) should be visually prominent at the top — a highlighted box with the one-sentence summary and the testable checklist
- Each section as a distinct block with clear headings
- Evidence quotes from the data should be styled as subtle blockquotes
- The "What Doesn't Work" section should have a distinct visual treatment — maybe a muted red/warning accent

### Colour Palette

- Background: `#FAFAFA`
- Card background: `#FFFFFF`
- Text: `#1A1A2E`
- Muted text: `#64748B`
- Accent for key findings: `#2563EB`
- Evidence/quotes: `#F1F5F9` background with left border `#CBD5E1`
- Warning (what doesn't work): `#FEF2F2` background with left border `#FECACA`
- Winning formula box: `#F0FDF4` background with border `#BBF7D0`

---

## Lookalike Content Ideas HTML

### Design Direction

This is a menu of options — the user needs to scan 10 ideas quickly and decide which ones to pursue. Think of it like a content calendar planning tool. Each idea should feel actionable, not theoretical.

### Layout

- Max-width: `780px`, centered
- The winning formula at the top as a compact reminder box
- Each content idea as a card
- Summary table at the bottom for quick reference

### Idea Cards

Each card should show:
- **Number** — large, left side
- **Title** — bold, prominent
- **Topic** — one sentence below the title, muted
- **Pattern match badges** — small coloured pills showing which winning patterns this idea follows (e.g., "Story format", "Implementation topic", "Validation emotion")
- **Angle** — the suggested take, regular text
- **Hook** — the draft opening line in a highlighted box (light background)
- **Format + Emotion** — as a compact line below
- **Trending signal** — muted text with a small "trending" icon or indicator

### Badge Colours for Pattern Matches

- Topic match: `#2563EB` (blue)
- Format match: `#7C3AED` (purple)
- Hook match: `#D97706` (amber)
- Emotion match: `#059669` (green)
- Specificity match: `#64748B` (grey)

### Summary Table

At the bottom, a compact table listing all 10 ideas with columns:
- #
- Title
- Key pattern
- Format
- Trending signal

### Colour Palette

- Background: `#FFFFFF`
- Card background: `#FFFFFF` with border `#E2E8F0` and subtle shadow
- Text: `#1A1A2E`
- Muted text: `#64748B`
- Hook highlight box: `#FFFBEB` background with border `#FDE68A`
- Card hover (if desired): subtle shadow increase

## Print Styles

```css
@media print {
  body { font-size: 11pt; }
  .card { break-inside: avoid; box-shadow: none; border: 1px solid #ccc; }
  .badge { border: 1px solid #999; }
}
```

## Filenames

- Profile: `winning-content-profile-[platform].html` in `./profiles/`
- Ideas: `lookalike-ideas-YYYY-MM-DD-[platform].html` in `./content/content-ideas/`
