---
name: mosaic-study
description: Turn reference observations into transferable principles.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, reference, study, originality, adaptation]
    related_skills: [mosaic, mosaic-design]
---

# Mosaic Study

A reference is evidence, not a palette to paste. Use this before adapting a site, component or art direction.

## When to Use

- The user names a reference, sends screenshots or asks for a design "like X".
- You need to explain what you are borrowing and what you refuse to copy.
- A page needs an original move derived from a reference's relationship, not its surface.

## The Rule

**A URL alone is not a study.** If only a name or URL exists, call `mosaic_study` and return its capture checklist. Do not invent layout, type, motion or colours from memory.

## What to Record

- layout: how the page is organised (split, index, table, sequence, canvas)
- type: display/body/utility roles and body measure
- colour: field, ink, muted, line, accent and deep — by role
- material: paper, steel, glass, ink, halftone or none
- motion: trigger, change, duration, reduced-motion path
- content: the objects and the relationship between them
- what works: one sentence, observable
- avoid: what must not be copied (brand assets, exact layout, copy, proprietary code)

## Output

`mosaic_study` returns:

- `status`: `studied` or `needs_observations`
- `confidence`: high / medium / low
- `principles`: observed facts plus transfer candidates
- `transferable`: the small set you may adapt
- `not_transferable`: same-layout, assets, copy and brand marks
- `originality_contract`: one principle per reference, a changed artifact, a named new move

## Adaptation

Borrow **one relational principle**, then change:

1. the artifact (index → specimen, cards → table, header → margin)
2. the content relationship (browse → compare, read → annotate)
3. the motion (reveal → settle, orbit → pause)
4. the visual language (palette, type pairing, material)

Then write the new move in one sentence. If the sentence could describe the reference unchanged, you are copying.

## Verification

- Every principle is traceable to supplied observations; none are invented.
- A URL-only reference reports `needs_observations`.
- The output names what is not transferable.
- `mosaic_design` can use the resulting map without remote access.