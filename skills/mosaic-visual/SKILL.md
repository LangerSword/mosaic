---
name: mosaic-visual
description: Use when a page needs a measured visual check, not a screenshot opinion.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, web, visual, qa, accessibility, evidence]
    related_skills: [mosaic, mosaic-score, mosaic-critique]
---

# Mosaic Visual

A deterministic browser gate for a built page. It returns a pass or fail from
measurements, not from a model describing a screenshot.

## When to use

- A page is about to be called finished, shipped or "visually guaranteed".
- A text score says `ship` but nobody has rendered the page.
- A mobile layout looks fine in source and suspicious in a real viewport.
- You need a compact evidence pack: two screenshots, hard-gate results and
  exact blocker strings.

Do not use it to judge taste, originality or whether a composition is
Awwwards-worthy. Those need a human or a vision critique pitched as opinion.

## Run it

Tool:

```json
{"target": "http://127.0.0.1:4322/"}
```

```json
{"target": "/absolute/path/to/index.html"}
```

```json
{"source": "<!doctype html>…"}
```

CLI:

```bash
mosaic visual --target http://127.0.0.1:4322/
mosaic visual --target ./dist/index.html
```

For a first run on a machine without a browser, the tool returns
`status: "needs_browser"` and does not pretend to have a guarantee. The
handler looks for Playwright in `MOSAIC_BROWSER_PYTHON`, then
`~/.venv/bin/python`, then the current interpreter.

## What it measures

One Chromium launch, two viewports: `1440x900` and `390x844`.

Hard gates, per viewport:

- console or page errors
- horizontal overflow and visible out-of-viewport elements
- visible `h1` in the first screen
- real text-box overlap (descendants ignored; clipped decorations ignored)
- WCAG text contrast against the effective solid background
- focusable controls and a visible focus indicator while tabbing
- reduced-motion: no moving elements without a reduced-motion rule
- screenshot is not blank
- mobile controls are at least 24px

Soft gates:

- controls at least 44px on mobile
- screenshot has at least six colours and real tonal spread

The output includes `gates_passed`, `gates_total`, `blockers`, per-viewport
metrics, and two screenshot paths. `visual_guarantee` is true only when every
hard gate passes. It is a bounded guarantee: layout, contrast, interaction
affordance and a real render. It is not a guarantee of beauty.

## Efficient usage

- Use one call on the **candidate page**, not one per section.
- Use `mosaic_score` first for text-level items; use `mosaic_visual` once the
  page exists.
- Do not attach screenshots to the chat. Read the returned paths, or open the
  two files locally. The tool returns paths, not base64.
- A pass with a focused h1, no blockers and no console errors is the stopping
  condition. Do not rerun for a third viewport unless a breakpoint changed.
- If it fails, fix the named blocker and rerun once. Do not argue with the
  report.

## Reading a failure

- `contrast` rows give `text`, `ratio` and `expected`. Fix the token or the
  background; a small accent on paper is the usual offender.
- `overflow_elements` means a rendered box exceeds the viewport and is not
  clipped by an ancestor. Decorative elements inside `overflow:hidden` are
  ignored on purpose.
- `overlaps` is direct visible text boxes intersecting. Parent/child pairs are
  excluded.
- `focus` needs an actual `:focus-visible` outline or shadow. Source-level
  `outline:none` does not pass.
- `reduced-motion` fails only when moving elements exist and no stylesheet rule
  handles `prefers-reduced-motion: reduce`.
- A `needs_browser` result is an environment blocker, not a page failure.

## Verification

- Run on the real built page, not a hand-written fixture.
- Keep the two screenshot paths as evidence.
- Re-run after fixes and report `gates_passed/gates_total` plus blockers.
- Pair with `mosaic_score` (text) and `mosaic_critique` (copy/contract). The
  visual gate does not replace either.