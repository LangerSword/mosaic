---
name: mosaic-invent
description: Invent new interactions with a typed taste rubric.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, interaction, invention, taste, state-machine]
    related_skills: [mosaic, mosaic-forge, mosaic-components]
---

# Mosaic Invent

Mosaic Invent composes interaction candidates from a typed grammar and scores them with a transparent rubric. It does not claim to create from pure nothing: it recombines a small set of primitives, rejects weak combinations, and makes the trade-offs visible. A candidate is a hypothesis until it is rendered, used and judged.

## When to Use

- The existing patterns are not enough and you need a new state transition.
- A brief asks for a feeling, not a known component.
- You need three bounded directions to prototype, not an infinite moodboard.
- You want to add an accepted interaction to the cabinet.

Do not use it to clone a reference, to bypass a licence, or to skip browser verification.

## Grammar

Every candidate combines:

- **Object**: card, field, rail, token, ring, stack, ledger, lens.
- **Input**: hold, swipe, drag, tap, hover, scroll, key.
- **Physics**: pour, spring, fold, orbit, settle, breathe, cascade.
- **Feedback**: check, ring, trail, label, tick, ripple, dissolve.
- **Metaphor**: paper, tide, loom, compass, archive, signal, weather, workshop.

The state machine is the product. A candidate must state what happens at `idle`, `contact`, `armed`, `resolved` and `reset`; a transition without a cause is decoration.

## Taste

`mosaic_invent` scores each candidate:

- **Coherence** 30%: does the input cause the physics and feedback?
- **Legibility** 25%: can the state be understood without motion or hover?
- **Novelty** 20%: is this a new transition, not a renamed known component?
- **Restraint** 15%: one object, one input, one feedback.
- **Fit** 10%: does it belong to the brief?

Hard gates: pointer and keyboard reach the same state; reduced motion keeps the result; irreversible actions have a cancel; hover is never the only path. A high score is not a pass; render it.

## Procedure

1. Write a brief of at least one sentence: audience, action, feeling, constraint. Completion: no generic "modern UI" wording.
2. Call `mosaic_invent(brief, constraints, count=3, seed)`. Completion: three candidates with distinct inputs.
3. Pick one candidate by its state machine, not its name. Completion: a one-line reason for the choice.
4. Call `mosaic_forge` with the candidate's `forge_kind`, the target stack and CSS or GSAP. Completion: files emitted.
5. Render the candidate. Test pointer, keyboard, reduced motion, cancel and error. Completion: screenshots or test output.
6. Keep the candidate in the cabinet only if it survives. Record what was rejected and why.

## Cabinet

The cabinet is the taste memory: accepted interactions, rejected interactions and the reason. Do not train on a single verdict. A useful cabinet has enough variety to distinguish "new" from "noise"; the first ten verdicts are calibration, not truth.

## Pitfalls

- A clever metaphor does not rescue a state that cannot be cancelled.
- Novelty is not random; a new transition must still be learnable in one use.
- A score is a rubric, not a user test. Vision and people can disagree with it.
- Do not add a second signature move to rescue a weak first one.
- Do not copy the reference's implementation; copy the question it answered, then answer it differently.

## Verification

- Three candidates have distinct inputs and state machines.
- The chosen candidate has a forge output and a browser test.
- Keyboard and reduced motion are observed, not asserted.
- The cabinet records both accepted and rejected candidates.
- No reference code or paid asset is shipped.
