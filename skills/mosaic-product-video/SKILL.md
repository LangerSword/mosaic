---
name: mosaic-product-video
description: Use when producing a Mosaic product film, not a slide demo.
version: 0.3.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video, demo, product, mosaic, playwright, ffmpeg, pty]
    related_skills: [mosaic, mosaic-visual, demo-video-production, webreel, interactive-tty-automation]
---

# Mosaic Product Video

A short film where the **product does the work on screen**. No gradient stage,
floating card, redesign poster, lower-third manifesto or fake UI.

## Status: Redline was rejected

The 18-second Redline cut was pulled from the release. It was a design-critique
poster with a redline gimmick: no real interaction, no cause-and-effect, and the
lower-third carried the story. Do not make another one.

The next film must show a real Mosaic task from the actual tools:

> brief → generated page → real visual gate → fix → pass.

The Mosaic site and langersword.in are demos of what Mosaic can create. Use them
as artifacts, not as the product.

## The correct 20s cut

**Runtime:** 20s. **Viewport:** 1920×1080. **Source:** real terminal/PTY and real
browser capture. No staging.

```text
0.0-2.0   terminal: a real command starts from a brief
2.0-5.0   generated page opens; the viewer sees the actual output
5.0-8.0   real cursor changes type / selects a specimen
8.0-12.0  terminal: mosaic_visual runs; 14/16, failing rule named
12.0-15.0 the token is changed; same page reloads
15.0-17.5 terminal: 16/16, evidence id
17.5-20.0 end card with URL and one command
```

If the screen is split, the split must be earned: terminal on the left, actual
site on the right, both live. No title card after a static screenshot.

## Capture-first pipeline

### 1. Record the real terminal

Use a real PTY, not retyped text. Record the exact command sequence and timings
with `scripts`/`asciinema`-style cast data; replay actual bytes. If a cast is
not possible, use VHS against the real shell. Do not render a fake terminal.

### 2. Record the real page

Use Playwright at 1920×1080 against the generated page. Capture the actual
cursor, scroll to the failing element, change the control, reload fixed page.
No browser chrome. No injected fake state.

### 3. Compose

Use a **side-by-side or full-screen cut**, whichever shows the cause and effect
better. The product must be readable; crop/zoom into the exact failing control
when it changes. No stage, no floating card, no giant headline not present in
the product.

### 4. Sound

Use real terminal clicks and browser interactions plus the in-repo synth bed.
No TTS. If the product is genuinely quiet, do not add a banger just to hide it.

### 5. QA

- The command in the film must be a command that actually ran.
- The gate result in the film must come from a real `mosaic_visual` run.
- The before and after must show the same page and the same location.
- `ffprobe`: 20.0s, 1920×1080, 30fps, H.264, AAC.
- Decode whole file; zero errors.
- First 2s has product, not a logo; last 2s has a clean end card.
- Contact sheet: no dead frames, no text over the failing control.

## Rules

- **Show a task, not a taste claim.** A viewer should be able to describe what
  changed between the first and last frame.
- **No lower-third as narrator.** Use small labels only when the product itself
  cannot carry the state.
- **No mockup browser frame.** Use the real page.
- **No redline gimmick.** If a rule fails, show the actual gate output and the
  actual fix.
- **No “evidence, not vibes” poster.** Show evidence.
- **No gradient/floating-card stage.** That grammar is rejected.

## What remains unbuilt

The capture-first 20s film is **not yet built**. The Redline assets remain only
as a rejected experiment; do not ship them as the product film. The plugin and
release can ship without a film; a bad film is worse than none.

## Verification

When built, report:
- exact command that ran
- exact gate result before/after
- path to the real captures
- duration/fps/codec/audio
- contact sheet path
- what a viewer can actually verify by watching