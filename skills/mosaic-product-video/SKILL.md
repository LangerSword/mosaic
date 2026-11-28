---
name: mosaic-product-video
description: Use when directing a kinetic 3D demo for the Mosaic plugin.
version: 0.7.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video, demo, plugin, mosaic, kinetic, 3d, klieg, gsap, ffmpeg]
    related_skills: [kinetic-product-demo, mosaic, mosaic-visual, demo-video-production]
---

# Mosaic Kinetic 3D Plugin Video

A 30-second **kinetic product demo** for the Mosaic plugin, not a tour of the
showcase site. Direction follows `kinetic-product-demo`: problem → pain →
product → proof → mechanism → distribution → lockup. The composition is 3D
CSS planes with a moving camera, rendered **frame by frame through Klieg's
motion renderer**. No Blender, no DCC, no screen recording.

## Beat sheet

`demo/kinetic-3d/beat-sheet.md` is the source of truth.

```text
00.0-03.4  A BRIEF IS NOT A PAGE.          title plane at z=660
03.4-06.6  ONE BRIEF. THREE DIRECTIONS.    brief plane, real brief copy
06.6-11.2  three directed concepts         cards fan in 3D (9.0 / 8.9 / 8.8)
11.2-14.4  PICK ONE. / The Field Guide      chosen card at z=300
14.4-18.2  ./mosaic design --mode page      mechanism plane
18.2-22.2  16/16 hard gates                 proof plane, huge number
22.2-25.0  taste 7.9 / 20 components        two profile cards
25.0-30.0  MOSAIC / 13 tools / 23 skills    lockup and URL
```

Real values only:

- chosen The Field Guide 9.0
- concepts The Field Guide 9.0, The Bench 8.9, The Working Index 8.8
- visual status pass, gates_passed 16, gates_total 16
- taste_index 7.9, confidence low
- components 20, tools 13, skills 23

## Build

The scene is raw HTML + GSAP, which Klieg explicitly supports. It exposes
`window.__tl`; Klieg pauses and seeks the timeline per frame, so the render is
deterministic and has no screencast frame drops.

```bash
cd ~/projects/hermes-klieg
/home/lakshaya/.venv/bin/python scripts/motion_render.py \
  /home/lakshaya/projects/mosaic/demo/kinetic-3d/index.html \
  ~/Videos/mosaic/mosaic-plugin-kinetic-3d.mp4 \
  --fps 30 --duration 30 --width 1920 --height 1080 \
  --format mp4 --music /home/lakshaya/projects/mosaic/demo/raw/plugin/bed.wav
```

Klieg handles the frame loop, MP4 encode and the low music bed. Do not invoke
Blender for this cut.

## QA

- 30.0s, 1920×1080, 30fps, H.264, AAC.
- Decode whole file; zero errors.
- 1s: MOSAIC title, no blank frame.
- 9s: three cards readable; visible perspective, floor grid, selected card.
- 17s: `./mosaic design --mode page` legible.
- 21s: 16/16 dominates the frame.
- 26s: lockup with 13 tools / 23 skills / 16-16 gates.
- Preview stills before the full render; inspect 1, 9, 13, 17, 21, 26.

## Rules

- **Klieg is the renderer, not the subject.** No Blender render, no DCC.
- **3D must be visible.** Camera depth, card fan, floor plane, perspective.
- **Kinetic type carries the argument.** One idea per beat; no card wall.
- **Plugin artifacts are the proof.** Real command, real scores, real counts.
- **No site tour.** The page is never shown as the subject.
- **No fake numbers.** Read them from the generated JSON and gate output.

## Pitfalls

- CSS `rotateY` alone reads flat. Set final rotation and z in the GSAP
  `fromTo`; do not rely on a CSS transform that GSAP overwrites.
- Keep the floor grid low-contrast; it supports depth but can become noise.
- Klieg's renderer needs Playwright and Chromium in the interpreter running it.
- Do not use `recordVideo`; Klieg's deterministic seek is the point.
- A 30s 30fps Klieg render is 900 screenshots; budget a few minutes.

## Verification

- `~/Videos/mosaic/mosaic-plugin-kinetic-3d.mp4`
- `demo/kinetic-3d/index.html`
- `demo/kinetic-3d/beat-sheet.md`
- `~/projects/hermes-klieg/scripts/motion_render.py`
- Report: 30s, 30fps, 16/16, 13 tools, 23 skills, 20 components.