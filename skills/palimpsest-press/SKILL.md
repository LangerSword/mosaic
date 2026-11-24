---
name: palimpsest-press
description: Design tactile press, hold and confirm controls.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, interaction, press, hold, confirm]
    related_skills: [palimpsest]
---

# Palimpsest Press

Press is a transaction. A control should show contact, commitment, and consequence. This skill covers press states, hold-to-confirm, destructive actions, and the release path.

## When to Use

- A destructive or expensive action needs a deliberate hold.
- A physical button needs a convincing press state.
- A form needs a send, delete, pay, or publish that cannot be a single accidental tap.
- You need a progress interaction that is honest and accessible.

## State Model

1. **Idle**: label, shortcut or hint, no fake urgency.
2. **Pointer down**: scale to .98, darken, start a visible progress fill.
3. **Holding**: progress advances only while the pointer is down; announce the action once, not every frame.
4. **Release early**: drain faster than fill, return to idle, do not fire.
5. **Complete**: change to a check or confirmed state, then lock or reset after a short delay.
6. **Keyboard**: Space/Enter starts the hold; keyup cancels; the same duration applies.

Use 800-1500ms for destructive actions. Longer is not safer; it is annoying. Show the duration as a number if the action is expensive.

## Build

```css
.hold {
  position: relative; overflow: hidden;
  min-height: 44px; border-radius: 999px;
  touch-action: manipulation;
}
.hold__fill {
  position: absolute; inset: 0 auto 0 0; width: 0;
  background: var(--accent); transform-origin: left;
  transition: width 120ms linear;
}
.hold.is-releasing .hold__fill { transition-duration: 60ms; }
```

Use `pointerdown` + `pointerup` + `pointercancel` and `setPointerCapture` so leaving the button does not leave a stuck progress bar. Use a timestamp for elapsed time, not a chain of timeouts. Keep the label visible over the fill. On completion, change the accessible name to the result.

## Accessibility

- Use a real `<button>`, `aria-describedby` for the instruction, and `aria-live="polite"` for completion.
- Do not make the user hold a key for a long time with no alternative; provide a cancel path.
- Respect `prefers-reduced-motion`: remove the fill animation, keep the hold duration and a static state change.
- Provide a keyboard equivalent and a visible focus ring. Never rely on `onContextMenu` or a long-press-only gesture.
- Give a clear error state if the action fails; do not pretend success.

## Pitfalls

- A progress bar that fills on page load is a lie.
- Starting a timeout on pointerdown and never clearing it on pointercancel causes a ghost action.
- `onClick` plus a separate hold timer fires twice; one state machine only.
- A destructive action that resets instantly gives no confirmation.
- A hold control that is the only way to complete a form blocks switch and keyboard users.

## Verification

- Press and release early: no action, fill drains, button returns to idle.
- Hold to completion: one action, visible confirmation, accessible announcement.
- Keyboard: Space/Enter works; Escape/pointercancel cancels.
- Reduced motion: no fill animation, action still works.
- At 390px, the control is at least 44px tall and the label does not clip.
