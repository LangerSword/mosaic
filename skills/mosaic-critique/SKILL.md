---
name: mosaic-critique
description: Critique a built source for design specificity and honesty.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, critique, review, generic, accessibility, content]
    related_skills: [mosaic, mosaic-design, accessibility]
---

# Mosaic Critique

A design critique is not praise and it is not a screenshot. It is a list of specific claims a builder can act on, plus the limits of what the source can prove.

## When to Use

- A page has been generated or implemented and needs a design review.
- The user asks whether a design looks generic, AI-made or unfinished.
- A concept direction is about to be handed to a builder.

## What It Checks

`mosaic_critique` reads local text and checks:

- generic product copy (`seamless`, `unlock`, `empower`, `supercharge`, ...)
- a headline that repeats the brief (`portfolio for ... who needs ...`)
- more than one h1
- missing `focus-visible`
- missing a `data-slot` content contract
- missing `prefers-reduced-motion`
- too many radius values
- too many font families
- the existing Mosaic audit patterns (transition-all, generic gradients, glass, spinners, lack of reduced motion)

It returns a score, verdict (`pass`, `revise`, `reject`), findings, strengths and next actions.

## What It Cannot Prove

No text scan proves:

- visual accuracy
- contrast in the rendered theme
- keyboard behaviour
- motion quality
- image or asset fidelity
- cross-browser layout

Say so. Then render the page at 1440x900 and 390x844, test focus and the signature interaction, and inspect the actual screenshots.

## Review Order

1. Does the headline address a visitor, not repeat the brief?
2. Is there one artifact or a card pile?
3. Is the primary action visible and real?
4. Is there evidence, not invented metrics?
5. Is the palette doing roles rather than decorating?
6. Is the content contract marked (`data-slot`)?
7. Does keyboard/focus/reduced motion work?
8. Does the rendered thing match the concept?

## Pitfalls

- A clean text scan is not a good design.
- A high novelty score does not excuse an unusable page.
- A reference cannot be verified from a URL alone.
- Do not praise a page because it is minimal; empty is not the same as restrained.
- Do not add another panel to fix a weak composition; remove or reorganise.

## Output

Return a verdict, not a vibe:

- `pass`: source has a content contract, focus, reduced motion and no generic copy.
- `revise`: specific findings exist but the concept still stands.
- `reject`: prompt leakage, no primary action, no content contract or a generic template with no artifact.

Every finding needs a fix. Every claim about the rendered result needs a browser observation.