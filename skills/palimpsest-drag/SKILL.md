---
name: mosaic-drag
description: Design direct-manipulation drag and reorder surfaces.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, interaction, drag, reorder, pointer]
    related_skills: [mosaic]
---

# Mosaic Drag

Drag is direct manipulation. The object should feel picked up, the drop target should be obvious, and the result should be recoverable. This skill covers card sorting, kanban movement, sliders, and canvas panning.

## When to Use

- Reordering items where position carries meaning.
- Moving an object between visible containers.
- A canvas or timeline needs panning or scrubbing.
- A knob, slider, or crop handle needs pointer control.

Do not use drag for primary navigation, a one-item choice, or anything that has no keyboard alternative.

## Anatomy

- **Pickup**: 2-4px lift, slight scale, shadow, cursor `grabbing`.
- **Ghost**: the original slot stays visible; the moving copy follows the pointer with a small offset.
- **Drop target**: a soft outline or a gap opens; use one cue, not five.
- **Settle**: 120-220ms ease-out into the slot; no bounce after a precise drop.
- **Cancel**: Escape returns the object to its origin; announce the result.

## Build

Use Pointer Events, not mouse events. Call `setPointerCapture` on the handle so the drag survives leaving the element. Compute deltas from the start rect, not from the page scroll. Use a transform for the ghost, not `left/top`. Keep the scroll container still unless the user reaches an edge; then autoscroll at a bounded speed.

For sortable lists, use a library if the list is large, but keep the keyboard path first-class. For a simple two-axis knob, use a hidden `<input type="range">` as the source of truth.

## Accessibility

- Provide keyboard move controls: focus an item, then use arrow keys or explicit Move up/down buttons.
- Announce pickup, move, drop, and cancel through a live region.
- Do not require a precision drag; provide a click-to-place alternative.
- Keep the drag handle at least 44px on touch.
- Respect reduced motion: remove the lift and settle animation, keep the position change.

## Pitfalls

- A drag that only works with a mouse is a broken feature.
- Starting a drag on the whole row blocks text selection and scrolling; use a handle.
- A drop zone that only appears after hover is invisible on touch.
- Animating layout properties causes jank; use transforms and a placeholder.
- Dropping outside the container must cancel, not silently delete.

## Verification

- Drag with pointer, cancel with Escape, drop in a new slot; state matches the visible result.
- Keyboard: move the item without dragging; focus and live announcement work.
- Touch: handle is large, page can still scroll, drag does not fight the scroll.
- Reduced motion: no lift animation; final order is correct.
- Test at 390px and with a long list.
