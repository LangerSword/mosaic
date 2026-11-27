---
name: mosaic-score
description: Pre-awards score for a built source.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, score, review, awards, usability, originality]
    related_skills: [mosaic, mosaic-design, mosaic-critique]
---

# Mosaic Score

A page can look polished and still be a template. This is the pre-awards gate: a transparent text score across design, usability, creativity, content and originality, with **blockers** that must be fixed before the visual review.

## When to Use

- Before showing a generated page to a user or submitting it.
- Before a browser screenshot pass, to catch structural misses cheaply.
- When a page looks good but may be prompt-leaky, generic or shallow.

## What It Scores

| Criterion | Evidence in source |
|---|---|
| **Design** | token discipline, type roles, artifact, type/radius noise, prompt leak |
| **Usability** | focus-visible, reduced motion, one h1, CTA, keyboard affordances |
| **Creativity** | authored artifact, custom element, tokens, studied reference, generic-copy penalty |
| **Content** | data-slot contract, proof/provenance, headline not prompt-leaky, no generic copy |
| **Originality** | reference confidence + artifact + custom element − generic surface |

The overall is weighted 34% design, 25% usability, 20% creativity, 12% content, 9% originality.

## Reading the Verdict

- `ship`: no blockers, overall ≥ 8.5
- `revise`: specific findings or a lower score
- `reject`: three or more blockers, or overall < 6

Blockers include prompt leakage, generic copy, no focus path, no reduced-motion path, no content-slot contract and no clear h1.

## What It Cannot Prove

It is a text scan. It cannot judge:

- composition, rhythm or type texture
- colour in the rendered theme
- motion feel or timing
- image quality
- cross-browser layout
- the actual awwwards jury

Always run a real browser pass at 1440x900 and 390x844, keyboard test the controls and inspect the screenshots. Say that the score is a pre-awards gate, not a verdict.

## Wiring

```text
mosaic_design(brief: "...", mode: "page")
mosaic_score(source: page_html, brief: "...")
mosaic_critique(source: page_html, brief: "...")
```

Use `mosaic_study` first when a reference is named. A high score with no reference evidence is not originality.

## Pitfalls

- Do not reward a page for having many tokens; reward roles that are actually used.
- Do not let a custom element count as a concept if it does nothing.
- Do not call the score "visual QA".
- Remove one thing before adding another; a high score does not excuse a crowded page.