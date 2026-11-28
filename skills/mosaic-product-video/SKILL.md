---
name: mosaic-product-video
description: Use when producing a Mosaic product film, not a slide demo.
version: 0.5.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video, demo, product, mosaic, playwright, ffmpeg, gsap, motion-index]
    related_skills: [mosaic, mosaic-visual, demo-video-production, webreel, kinetic-product-demo]
---

# Mosaic Product Video

A **before/after reveal** of the same generated page: `14/16` failing state on
the left, `16/16` fixed state on the right, separated by a sweep divider. Real
page footage; the gate scores are real. No split-screen terminal, no gradient
stage, no lower-third manifesto.

The direction comes from **Motion Index / “Before and after”** (Shaan Johari,
animation styles for Claude). Credit the reference; the assets are original.

## The cut

**Runtime:** 20s. **Viewport:** 1920×1080. **Source:** `demo/raw/redline/fail.webm`
and `fixed.webm` at the same scroll position.

```text
0.0-2.2   failing page; BEFORE / 14/16 appears
2.2-6.8   divider sweeps from right to left; fixed page enters
6.8-10.2  AFTER / 16/16, full fixed page
10.2-14.2 divider returns to 50/50; both scores held
14.2-17.2 fixed page full; AFTER held
17.2-20.0 black end card / URL
```

The viewer sees the exact same page, the exact same crop and the exact same
coordinates in both states. The only thing that changes is the token and the
target height.

## Build

### 1. Candidate pair

```bash
cd ~/projects/mosaic
python scripts/build_redline.py
```

`fail.html` is a real generated page with a 2.23:1 token and 16px range target.
`fixed.html` is the same page fixed. Verify:

```bash
python scripts/demo_gate.py demo/redline/fail.html   # 14/16
python scripts/demo_gate.py demo/redline/fixed.html  # 16/16
```

### 2. Page footage

```bash
/home/lakshaya/.venv/bin/python demo/record_redline.py
```

Same scroll path for both. No browser chrome. Use the real capture, not stills.

### 3. Motion composition

`demo/before-after-film.html` + local GSAP (`demo/vendor/gsap.min.js`):

- fail layer full-bleed
- fixed layer clips in from the right
- 2px divider with a circular drag handle
- `BEFORE / 14/16` and `AFTER / 16/16` labels
- large score blocks outside the main reading area
- hard cuts only at the end

```bash
/home/lakshaya/.venv/bin/python demo/record_before_after.py
```

### 4. Audio and mux

```bash
python ~/.hermes/skills/creative/demo-video-production/scripts/make_banger.py \
  demo/raw/redline/before-after.wav 22

ffmpeg -y -ss 0.25 -i demo/raw/redline/before-after.webm -t 20.0 \
  -i demo/raw/redline/before-after.wav -map 0:v:0 -map 1:a:0 -t 20 \
  -vf "fps=30,scale=1920:1080,format=yuv420p,fade=t=in:st=0:d=0.2,fade=t=out:st=19.0:d=1.0" \
  -af "atrim=0:20,afade=t=in:st=0:d=0.3,afade=t=out:st=18.2:d=1.8,loudnorm=I=-15:TP=-1.5:LRA=10" \
  -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -movflags +faststart \
  ~/Videos/mosaic/mosaic-before-after.mp4
```

No TTS.

### 5. QA

- 20.0s, 1920×1080, 30fps, H.264, AAC.
- Decode whole file; zero errors.
- 1s: failing page and BEFORE/14/16 visible.
- 7s: divider clear, fixed page visible, no overlapping score over the headline.
- 15s: fixed state and AFTER/16/16 clear.
- Check page crop: same composition in both states.

## Rules

- **Same page, same crop, two verdicts.**
- **Divider is the event.** Sweep it; do not just fade.
- **Scores are real:** 14/16 and 16/16 from the visual gate.
- **No terminal in this cut.** The page is the proof.
- **No overlap over the headline.** Put score blocks in the lower corners or a
  black band, not across the main type.
- **No placeholder copy in the visible crop.** Use a generated page whose
  visible slots are replaced or crop above them.

## Pitfalls

- The score blocks can cover the evidence headline if placed over the page.
  Move them to a black lower band or corners.
- The fixed clip must be the same scroll position as the fail clip; re-record
  both if the candidate changes.
- GSAP `clip-path` needs the fixed layer above the fail layer.
- VHS/Playwright pre-roll must be trimmed; verify first frame.
- Do not call this a “product film” if the page still shows `replace` slots.

## Verification

- `~/Videos/mosaic/mosaic-before-after.mp4`
- `demo/before-after-film.html`
- `demo/record_before_after.py`
- `scripts/build_redline.py`, `scripts/demo_gate.py`
- Report: 14/16 failing state, 16/16 fixed state, 20s, 30fps.