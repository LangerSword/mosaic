---
name: palimpsest-components
description: Specify component states before styling them.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, components, states, interaction, spec]
    related_skills: [palimpsest]
---

# Palimpsest Components

A component is a state machine with a surface, not a rectangle with a hover colour. This skill covers the public component grammar behind the Construct study: flow canvases, cards, live rails, publishing bars, wordmarks, cursors, story pills, hold controls, segmented pickers and thinking states.

## When to Use

- You are about to build a component from a reference.
- A component works in one state but falls apart in hover, press, focus, loading or error.
- You need to choose between a card, a control, an instrument or a surface.
- You want to add a component family to Palimpsest.

Do not use for a full-page composition; use `palimpsest` first.

## Object, Control, Instrument, Surface

- **Object**: a card, ticket, portrait or deck. Its job is identity and weight.
- **Control**: a button, hold, segmented picker or drag handle. Its job is a state change.
- **Instrument**: a rail, ruler, counter, workflow or live list. Its job is to make a system legible.
- **Surface**: a canvas, glass panel or field. Its job is atmosphere and containment.

Pick one primary type. A card with three controls inside is a page, not a component.

## State Matrix

Write this before styling:

| State | What changes | What the user sees |
|---|---|---|
| Rest | type, material, primary affordance | the component at a glance |
| Hover | lift, sheen, preview | it is reachable |
| Focus-visible | ring, label, same information as hover | keyboard parity |
| Pressed | scale, fill, progress, label | contact and commitment |
| Loading | named step, skeleton, slow state | honest work |
| Success | check, settled state, announcement | the action completed |
| Error | specific message, retry | what to do next |
| Disabled | reduced contrast plus reason | why it is unavailable |
| Cancelled | returned state, no ghost action | nothing fired |

If a state cannot be seen in a still frame, it probably is not designed yet.

## Public Component Notes

These are public observations, not code to copy. The full records live in `references/public-component-notes.md`; the `palimpsest_components` tool returns them filtered.

| Component | Family | Public state idea |
|---|---|---|
| Flow canvas | select | A token travels a dotted graph; nodes light and tick; a node opens an inspector |
| Face card | hover | Halftone portrait; tilt, sheen, local dot swell; copy becomes a tick |
| Live card | press | Pulsing LIVE tag, count tick, lift; Join live → Joining… → You're in |
| Glass title card | hover | Frosted word over a photo; lean and light sweep |
| Card arc | drag | Bank cards on a ring; ghost ends; spring to the next card |
| Script over | press | A pen writes a hand word over a condensed word; next word on press |
| Channel rail | drag | Middle channel goes live; lift, count, caption, auto step |
| Publish bar | press | Autosave spins; Publish fills, ticks and flips DRAFT to LIVE |
| Beat wordmark | press | Letters pump to a beat; press drops them with a squash |
| Join group | press | Pill becomes Joined; your disc slides into the stack; count rolls |
| Live cursors | hover | Named cursors glide, pause and colour a node; click pings |
| Story pills | press | Unread badge pops; pill hops to front; tap springs it away |
| Hold to confirm | press | 1200ms fill, faster release, check at completion |
| Segmented control | select | One track, one sliding indicator, content changes in place |
| Thinking shimmer | loading | Named steps, elapsed time, quiet shimmer, no fake percentage |
| Quanta | type | One claim, one live instrument, one proof block |

## Procedure

1. Name the object, control, instrument or surface in one sentence. Completion: no more than one primary type.
2. Write the state matrix above. Completion: every state has a visible change and an accessible name.
3. Pick one signature motion. Completion: it explains a state change, not decoration.
4. Build rest and focus first, then press, then loading/error. Completion: each state works without hover.
5. Test 390px, keyboard, reduced motion and a slow network. Completion: no state is lost.
6. Add observed-but-original notes to the Palimpsest corpus only if they teach a reusable move.

## Pitfalls

- A component that only exists on hover is not a component.
- Copying the reference's timing as a law; use it as a starting point and test the product.
- Animating a card's width or height instead of transform.
- A success state that only changes colour; add a word, a check or a live announcement.
- A drag rail with no arrow keys; a live rail that auto-advances under focus.
- A hold control with a timer that survives pointercancel.

## Verification

- The state matrix is complete; each state has a test.
- Keyboard and pointer reach the same information.
- Reduced motion keeps every state change, removes the decoration.
- The component is readable at rest in a screenshot.
- No paid reference code, font or asset is shipped.
