---
name: mosaic-design
description: Direct a brief into a novel, buildable design system.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, direction, composition, system, page, originality]
    related_skills: [mosaic, mosaic-study, mosaic-critique, mosaic-forge, frontend-design]
---

# Mosaic Design

The designer's job is not to pick a template. Read the brief, decide what the page is made of, then make one original structure hold the content.

## Workflow

1. **Read the brief** — subject, audience, primary action, real inventory, proof, constraints.
2. **Study the references** — call `mosaic_study` first; use observations, never a URL alone.
3. **Generate three structures** — use `mosaic_design` with `mode: "direction"`.
4. **Choose with a rubric** — fit, coherence, specificity, novelty, usability, restraint, reference distance.
5. **Commit the system** — tokens, type roles, measure, grid, motion and one signature interaction.
6. **Emit only when the content contract is clear** — use `mode: "page"` for a static starter, then replace every `data-slot`.
7. **Critique** — run `mosaic_critique`; then render at 1440x900 and 390x844.

## The Three Concepts

`mosaic_design` deliberately offers three different **artifacts**, not three palettes:

- **index** — scan a row, see the specimen
- **bench** — pick up a tool, change the example
- **field guide** — read an annotated specimen
- **programme** — cue a sequence
- **signal room** — tune one measured signal
- **specimen table** — pick up and compare objects
- **reading room** — a measured reading column

Each concept names its adjacent field, reference anchor, translation, do-not-copy list, new move and risk. The selected concept includes `scores` and an `overall`.

## System Contract

The output defines:

- colour roles, not a palette dump
- contrast measurements for ink, muted and signal
- display, body and utility roles
- a 12-column grid, a max width and a measured reading column
- one feedback duration, one scene duration and a reduced-motion path
- a content contract: brand, headline, thesis, action, inventory, proof and constraints
- a build order and acceptance checks

No invented metrics, logos or testimonials. No copied assets or reference code.

## Page Mode

`mode: "page"` emits a complete static `index.html`:

- no external fonts or images
- one real interaction (specimen selection or type controls)
- `data-slot` markers for replaceable content
- visible focus, reduced motion and a measured column
- a domain-specific artifact: type specimen, trace, source rail, object collection, reading extract, programme, table or index

The page is a **starter**, not a finished content site. A real typeface name, inventory and proof must replace the sample labels.

## Anti-Slop Rules

- Do not repeat the brief as the headline.
- Do not make three identical feature cards.
- Do not use purple gradients, glass everywhere or generic Inter as the identity.
- One accent, one display voice, one material.
- Show the artifact; do not describe it in three paragraphs.
- If the concept has no relationship to the primary action, reject it.

## Verification

- Three distinct concepts and one selected with transparent scores.
- Reference observations produce principles; a bare URL produces a checklist.
- Page output has no unresolved template tokens and contains `data-slot`.
- `mosaic_critique` passes the starter.
- Render 1440x900 and 390x844; test the signature interaction by keyboard and pointer.