---
name: mosaic-ascii
description: Build monospace fields without terminal cosplay.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, ascii, monospace, field, terminal, atmosphere]
    related_skills: [mosaic, mosaic-shader, mosaic-type]
---

# Mosaic ASCII

ASCII is a material, not a skin. It should carry atmosphere or data, remain readable at its actual character size, and still work when the pointer is gone or motion is reduced.

## When to Use

- A product lives near terminals, agents, local inference or night work.
- A hero or footer needs a living field without another WebGL scene.
- A data state can be expressed as a character ramp rather than a chart.

Do not use ASCII as a texture behind body copy. Do not simulate a terminal that does nothing. Do not make the field the only route to information.

## Rules

- **One ramp per field.** Example: ` .:-=+*#%@` or ` ·░▒▓█`. Pick one and keep the mapping stable.
- **Monospace only.** Measure the character cell; the grid is the art direction.
- **Density means value.** Map a real value (height, velocity, activity, presence) to the ramp. A random character field is decoration.
- **One motion cause.** Pointer proximity, scroll position or an explicit control. Never three competing animations.
- **Readability floor.** Character fields are atmosphere; labels and actions sit in normal type above them.
- **Static fallback.** Reduced motion and no-canvas environments get a finished static frame, not a blank box.
- **Pause offscreen.** Use IntersectionObserver and `document.hidden`.
- **Throttle.** Update at 20–30fps, not every animation frame; one text node update per tick is enough.

## Minimal Build

```html
<div class="ascii-field">
  <pre data-ascii aria-label="Ambient field"></pre>
  <button type="button" data-ascii-mode>Shift</button>
</div>
```

```css
.ascii-field { position: relative; overflow: clip; background: var(--deep); color: var(--paper); }
.ascii-field pre { margin: 0; font: 12px/1.05 var(--mono); letter-spacing: .06em; white-space: pre; }
.ascii-field button { position: absolute; right: 10px; bottom: 10px; }
@media (prefers-reduced-motion: reduce) { .ascii-field pre { transition: none; } }
```

```js
const ramp = ' .:-=+*#%@';
const draw = (cols, rows, phase) => Array.from({ length: rows }, (_, y) =>
  Array.from({ length: cols }, (_, x) => {
    const v = Math.sin(x * .23 + phase) * .5 + Math.cos(y * .41 - phase) * .5 + .5;
    return ramp[Math.max(0, Math.min(ramp.length - 1, Math.floor(v * ramp.length)))];
  }).join('')
).join('\n');
```

Use one `requestAnimationFrame` loop, one timer and one visible state. Stop on hidden.

## Accessibility

- The field is `aria-hidden` when it is purely atmospheric; a nearby text label carries the meaning.
- If it encodes a value, expose the value in normal text and `aria-live` when it changes.
- The control is a real button; keyboard and pointer are equivalent.
- Reduced motion freezes the field at a finished frame.

## Verification

- Character ramp remains legible at 390px; no horizontal scroll.
- Resize does not leak the old grid or cause a layout jump.
- Reduced motion shows a finished static frame.
- The field pauses when offscreen or hidden.
- Pointer, keyboard and no-JS states remain understandable.
- No fake terminal copy or invented telemetry.