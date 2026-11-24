# Construct Design: public teardown

Observed 2026-11-24 from the public catalog and the free specimen pages. Source: `https://www.tobiadonadon.com/projects/construct/design?kind=component`. REA passive capture: `ev_ef4dfd62abbdcca076183eda6b9aafd68f126d39e5a09d2b024039301e6c778c`. Browser captures: catalog at 1440, plus Hold to confirm, Segmented control, Thinking shimmer and Quanta. No login or paywall was bypassed, and no code or assets are copied here. This is a study note for original work.

## What the public page is

Construct Design is a library of hand-made web specimens: 269 designs in the public counter, split into 176 components, 54 websites and 39 apps. The catalog filters by interaction family: Press, Drag, Hover, Select, Shader, Type, Scroll and Loading. The page says 107 designs can be tried without an account; four are code-free. A specimen opens with Preview, Code and Prompt tabs, a line count and, for some, live parameters.

This is not one design system. It is a gallery of independent specimens under a quiet shell. That distinction is the most useful thing to take from it.

## The shell

The catalog is a neutral gallery, not a brand template:

- Body: Satoshi, 16px / 24px, regular, near-black on a light field.
- Display: Host Grotesk available as a variable face; the hero measured 51.48px / 50.45px, weight 500, tracking -2.06px. Tight, large, editorial.
- Accents: Instrument Serif italic and Caveat hand are available for specimens; they are not used for the shell body.
- Muted copy: 18px / 27px, around `#3d3d3a`.
- Section title: 22px / 33px, weight 600, tracking -0.44px.
- Core tokens observed: `--paper: #faf8f2`, `--ink: #17181a`, `--muted: #6b6a66`, `--line: #e7e3d8`, `--primary: #0a0a0a`, `--accent-clay: #ce4631`, `--accent-deep: #0c2342`, `--accent-sky: #38bdf8`, `--hairline: #0b1f3a1f`.
- The catalog uses pill tabs with inventory counts, thin rules, a poster grid, a huge headline, one quiet paragraph, a black primary action and a ghost secondary action. There is very little chrome around the work.
- Per-specimen scopes were visible in the CSS: `--m-*` (cream, ink, clay, green, blue, gold), `--wd-*` and `--ga-*` palettes. The shell is neutral so a specimen can own its temperature.

The hero uses a colour accent on one phrase. Treat that as a one-off gesture, not a house rule: the library is deliberately plural.

## Four specimens

### Hold to confirm

A destructive control with a 1200ms hold. Colour pours in from the left while the pointer is down; releasing early drains it back about twice as fast. At completion it becomes a check and holds itself. The page describes it as a button for things you cannot undo. This is a state machine, not a progress decoration.

### Segmented control

Day / Week / Month / Year. One active option, a sliding indicator, a quiet track. The control changes the content below it without moving the page furniture. The comparison stays visible.

### Thinking shimmer

An agent-progress specimen. It shows named steps (Reading your files, Planning the change, Writing code, Checking it, Done), elapsed time and a shimmer. It does not invent a percentage. The steps carry the state; the shimmer is atmosphere.

### Quanta

A product-page specimen for an API. One large claim (frontier reasoning at autocomplete speed), one live instrument (tokens per second), one proof block, then a compact benchmark/result area. The data is treated as an instrument panel, not a row of generic feature cards.

## Reference map

| Observed | Why it works | Keep as principle | Do not copy |
|---|---|---|---|
| Warm paper, ink and hairlines under a loud specimen | The shell recedes; the work carries the colour | Neutral shell, scoped specimen tokens | The exact palette or poster artwork |
| One huge display line with a quiet lead | Clear entry point; no competing messages | One loud line, one quiet paragraph | The exact headline or gradient phrase |
| Pills with inventory counts | Compact filtering; counts build trust | Counts as metadata, not decoration | The exact pill shadow or radius |
| Hold, drag, segmented controls | Direct manipulation makes state legible | Physical state model with cancel/release | The 1200ms value as a universal law |
| Steps in an agent loading state | Honest work beats a spinner | Named steps, truthful progress, slow state | The exact shimmer |
| Per-specimen palettes | The library stays plural | Scope tokens to the object, not the whole page | Any one specimen's full look |
| Type as image in posters | A specimen needs a point of view | One display voice plus one utility voice | The exact faces or lettering |

## Principles to carry forward

1. **A specimen is one idea.** Name the interaction or object; do not bundle five features into a hero.
2. **The shell is quiet; the object is loud.** Spend colour, type and motion on one thing.
3. **State is physical.** Press, hold, drag and select should show contact, commitment and release.
4. **Type carries hierarchy.** Display, body and utility are different jobs; use contrast, not five weights of one face.
5. **Data is an instrument.** Use ticks, counters, rails and labels; avoid generic dashboards.
6. **Motion has a cause.** Every transition answers a state change; remove decoration that does not.
7. **Texture is optional, not a default.** Paper, glass, noise and foil are materials; pick one.
8. **Make the document work without the show.** Keyboard, reduced motion, no-JS and slow-network paths are part of the design.

## Anti-patterns the study argues against

- A page of identical rounded cards with the same shadow and radius.
- A purple-blue gradient as the only identity.
- Glass blur on every surface, especially behind text.
- A spinner with no named work and a fake percentage.
- Hover-only actions on touch devices.
- Six accent colours and no hierarchy.
- A hero that says nothing a human would say.
