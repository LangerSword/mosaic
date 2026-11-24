---
name: palimpsest
description: Turn design references into original web systems.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, web, reference, system, frontend]
    related_skills: [palimpsest-cards, palimpsest-press, palimpsest-drag, palimpsest-hover, palimpsest-select, palimpsest-shader, palimpsest-type, palimpsest-scroll, palimpsest-loading]
---

# Palimpsest

Palimpsest is a design-reference method. Inspect a surface, name what makes it work, then build an original system from the principles. It does not clone a reference, copy proprietary code or assets, or stop at a moodboard. The output is a direction, a small token set, a composition, one or two signature moves, and a verification pass.

## When to Use

- The user gives a reference URL or image and asks for something in that spirit without copying it.
- A page needs a coherent visual language, not another component.
- A design feels generic and needs a specific point of view.
- You are turning a catalog of specimens into a brief for one product.

Do not use for pixel-perfect recreation, licensed asset extraction, paywall bypass, or a one-line CSS fix.

## Prerequisites

- A reference URL or image and permission to study it.
- `browser_navigate`, `browser_exec` or CDP, and `vision_analyze` for first-screen evidence.
- `rea` passive inspection when the claim depends on a shipped or running surface. Record the evidence id; static inspection is not execution.
- The target stack and real content. If the user did not specify them, choose a sensible default and state it.

## Reference Protocol

1. Capture the page at 1440 and 390 widths: first screen, one scroll state, and one interaction state. Completion: three images with URLs and viewport sizes.
2. Read the live DOM and computed styles, not your impression. Record display/body faces, sizes, line-heights, tracking, colors, hairlines, radii, shadows, gaps, and transition durations.
3. Use REA passive inspection for runtime evidence when needed. Keep observed, inferred, and unknown separate.
4. Write a reference map with four columns: observed, why it works, keep as principle, do not copy.
5. Name one specimen idea, the page's reason to exist. "Modern SaaS" is not an idea.
6. Stop when you can explain the page in three sentences without adjectives.

## Choose the System

- Pick one base field: paper, ink, night, or tinted ground. Pick one accent and one hairline family.
- Scope color per specimen. A quiet shell can hold loud content; do not force every section into one global palette.
- Pick one display voice, one body face, and at most one utility face. A third face is for code or numbers only.
- Pick two signature moves total: one structural and one behavioral. More than two reads as noise.
- Pick one material: paper, glass, metal, or pixel. Do not stack materials without a reason.
- Write a not-doing list before writing code.

## Token Recipe

Start small and derive everything else:

```css
--paper: #faf8f2; --ink: #17181a; --muted: #6b6a66; --line: #e7e3d8;
--accent: #ce4631; --accent-deep: #0c2342;
--display: clamp(2.6rem, 6vw, 6rem);
--body: 1rem/1.55;
--radius: 2px; /* editorial; 18px soft; 999px for one pill family */
--ease-out: cubic-bezier(.22, 1, .36, 1);
--ease-spring: cubic-bezier(.2, 1.35, .4, 1);
```

Use `clamp()` for display type. Keep body measure at 45-75ch. Use tabular numerals for data. Use 1px hairlines. Use shadows only for objects that should feel physical.

## Compose

- Hero: one loud line, one quiet paragraph, one primary action, one proof object.
- Alternate dense instruments with quiet breathing room. Do not repeat the same card grid five times.
- Put labels and index numbers on a common baseline; use few words.
- Asymmetry with a reason: one large object, one narrow rail, one full-bleed moment.
- The first screen must read without motion or JavaScript.
- Use real content. No lorem, fake logos, or invented metrics.

## Motion

- Motion must explain state or physics. Decoration is not a rationale.
- One signature interaction. Use 120-240ms for feedback and 400-700ms for scene changes.
- Use a spring for objects that have weight; use an ease-out for surfaces.
- Provide a reduced-motion path for every animation. Never make content depend on hover or scroll.
- Test keyboard only and `prefers-reduced-motion: reduce`.

## Build

- Semantic HTML first. Use CSS variables and layout primitives; do not add a component library for one page.
- Use SVG, canvas, or WebGL only when the effect earns its weight.
- Load fonts with `font-display: swap` and a local fallback; reserve space to avoid layout shift.
- Give images explicit dimensions and `object-fit`; lazy-load below the fold.
- No network keys, tracking, copied assets, or hidden data collection.

## Audit

- Screenshot 1440, 1024, and 390 widths; inspect first screen, scroll, and focus states.
- Contrast: 4.5:1 for body, 3:1 for large text and UI boundaries.
- Keyboard: visible focus, logical tab order, no traps.
- Reduced motion: transforms and animations stop; content remains.
- Performance: no layout shift; pause shaders offscreen; no unbounded blur.
- Originality: remove any direct copy. The reference map is a check, not a template.

## With the Palimpsest plugin

If `palimpsest_recipe` is available, use it as a starting direction, then apply this method. Ask for a mood and a brief, take the two signature moves and token table, and replace anything that does not belong to the actual product. `palimpsest_audit` is a quick text screen before browser review; it is not a substitute for keyboard, contrast or performance tests. The skills work without the plugin.

## Verification

- Three-sentence rationale: what it is, why the signature moves, what was refused.
- Token table and one screenshot at each width.
- Accessibility and reduced-motion results.
- No unresolved "looks generic" note.

## See Also

`palimpsest-cards`, `palimpsest-press`, `palimpsest-drag`, `palimpsest-hover`, `palimpsest-select`, `palimpsest-shader`, `palimpsest-type`, `palimpsest-scroll`, `palimpsest-loading`. The reference notes are in `references/construct-teardown.md`.
