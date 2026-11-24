---
name: mosaic-hover
description: Build hover reveals, cursors and pointer states.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, interaction, hover, cursor, reveal]
    related_skills: [mosaic]
---

# Mosaic Hover

Hover is a preview, not a requirement. This skill covers image reveals, cursor-follow effects, magnetic buttons, and hover cards. The test is whether the page still works when hover does not exist.

## When to Use

- A gallery needs a preview on hover.
- A dense index needs one quiet reveal.
- A cursor can carry a small piece of information.
- A card or row needs a hover lift.

Do not hide primary navigation, prices, or actions behind hover. Do not use hover on touch as a requirement.

## Patterns

- **Image reveal**: a small preview follows the pointer, clamped to the viewport; hide it on touch.
- **Row reveal**: a thumbnail slides in from the edge; keep the row text stable.
- **Magnetic button**: translate 2-6px toward the pointer; return with a spring; disable for reduced motion.
- **Cursor label**: a small tag follows the cursor; use it for "View", "Drag", or "Play", not for essential text.
- **Hover lift**: 4-8px translate and a slightly stronger shadow; one object at a time.

## Build

```css
@media (hover: hover) and (pointer: fine) {
  .row:hover .preview { opacity: 1; transform: translateY(0); }
}
.preview { opacity: 0; transform: translateY(6px); transition: opacity 160ms var(--ease-out), transform 160ms var(--ease-out); }
```

Keep hover styles inside a hover-capable media query. Use `pointerenter`/`pointerleave`, not `mouseover`, when the preview follows the pointer. Clamp the preview with `Math.min/max` and account for its width. Use one preview node, not one per row, for large lists.

## Accessibility

- Provide focus-visible parity: keyboard focus reveals the same preview or a static version.
- Never make the preview the only place a title or price exists.
- On touch, show the preview as a static thumbnail or omit it.
- Reduced motion: remove the follow, lift, and spring; keep content visible on focus.
- Respect `prefers-reduced-motion` and avoid cursor effects on low-power devices.

## Pitfalls

- A preview that follows the pointer outside the viewport creates scrollbars; clamp it.
- Hover-only actions are invisible to keyboard users; add focus and a visible button.
- Per-row preview DOM for 200 rows is a memory leak; reuse one node.
- `transition: all` on a hover card animates layout; list properties explicitly.
- A cursor effect that covers the text it describes is worse than no effect.

## Verification

- Hover a row: preview appears, stays inside the viewport, and the row text does not shift.
- Tab to the row: focus reveals the same information.
- Touch emulation: no hover-only dead end.
- Reduced motion: no follow or lift; content remains.
- Check 390px and a 200-row list.
