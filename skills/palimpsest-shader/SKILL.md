---
name: palimpsest-shader
description: Build atmospheric shaders with static fallbacks.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, shader, webgl, atmosphere, performance]
    related_skills: [palimpsest]
---

# Palimpsest Shader

A shader is atmosphere, not a screensaver. This skill covers noise fields, dot globes, heat maps, and subtle distortion. The rule: the page must still be readable when the shader is absent, paused, or reduced.

## When to Use

- A hero needs a living material that cannot be made with CSS alone.
- A data surface benefits from a field, grain, or flow.
- A brand needs one memorable ambient moment.

Do not use a shader for text, navigation, or a control that must be crisp. Do not make WebGL the only way to see the content.

## Build

- Start with a static poster or CSS gradient. It is the loading state and the fallback.
- Render at a capped device pixel ratio (1.5-2) and a low internal resolution; upscale with CSS.
- Pause when the canvas is offscreen, the tab is hidden, or the user prefers reduced motion.
- Use a fixed time step or a clamped delta; do not let a tab return and jump.
- Keep the fragment shader small: one noise function, one palette, one motion.
- Provide a `prefers-reduced-motion` path with a still frame.
- Test on integrated graphics and a 390px viewport.

## Visual Grammar

- Pick one field: grain, dots, contour, heat, or flow.
- Pick one motion: drift, breathe, sweep, or respond to the pointer.
- Keep contrast low behind text; add a solid scrim rather than fighting the shader.
- Use color from the page system, not a rainbow palette.
- Avoid chromatic aberration, bloom, and displacement all at once.

## Accessibility

- Canvas is decorative: `aria-hidden="true"` unless it carries data.
- If it carries data, provide a table or text summary.
- Reduced motion must stop or freeze the animation.
- Do not flash; keep transitions below three per second.
- Keep text outside the canvas or on a stable scrim.

## Performance

- Budget: one canvas, one draw call, no per-frame allocations.
- Use `requestAnimationFrame`; stop on `visibilitychange`.
- Cap DPR and resolution; use `ResizeObserver` with debounce.
- If the frame budget is missed, drop resolution before dropping content.
- No third-party runtime for a single effect.

## Pitfalls

- A shader that fills the viewport and leaves no readable text is a poster, not a page.
- Animating at full DPR on a 4K display cooks laptops.
- A canvas with no fallback is a blank rectangle when WebGL fails.
- Pointer-reactive shaders can fight scrolling; gate them to fine pointers.

## Verification

- Disable WebGL: static fallback is visible and the page still reads.
- Reduced motion: one still frame; no continuous animation.
- Offscreen/hidden tab: animation stops.
- 390px and integrated GPU: no scroll jank; text contrast passes.
