---
name: mosaic-product-video
description: Use when producing a Mosaic product film, not a slide demo.
version: 0.4.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video, demo, product, mosaic, playwright, ffmpeg, vhs]
    related_skills: [mosaic, mosaic-visual, demo-video-production, webreel, interactive-tty-automation]
---

# Mosaic Product Video

A **live split-screen** product demo: the real generated page on the left, the
real gate/terminal on the right, one continuous take. No stage, no floating
card, no lower-third manifesto, no redline gimmick.

## The accepted cut

**Runtime:** 20s. **Viewport:** 1920×1080. **Source:** real page captures and a
real VHS terminal recording.

```text
0.0-2.0    terminal: copy fail.html -> candidate.html
2.0-9.0    page: failing candidate; terminal types the gate command
           gate returns FAIL / 14/16 and names contrast + 16px target
9.0-14.0   terminal: two real sed edits; page still failing
14.0-16.8  terminal: gate re-run begins
16.8-19.2  page: fixed candidate; terminal returns PASS / 16/16
19.2-20.0  black end line: URL only
```

No added type, no labels over the product, no motion graphics. The only motion
is the actual terminal typing and the real page state change.

## Build

### 1. Candidate pages

```bash
cd ~/projects/mosaic
python scripts/build_redline.py
```

This creates `demo/redline/fail.html` (real generated page with a 2.23:1 token
and 16px range target) and `fixed.html`. Verify with the real gate:

```bash
python scripts/demo_gate.py demo/redline/fail.html   # 14/16, exit 1
python scripts/demo_gate.py demo/redline/fixed.html  # 16/16, exit 0
```

### 2. Real page footage

```bash
/home/lakshaya/.venv/bin/python demo/record_redline.py
```

Writes `demo/raw/redline/fail.webm` and `fixed.webm` at 1920×1080. Same scroll
path. No browser chrome.

### 3. Real terminal footage (VHS)

```bash
vhs demo/redline.tape
```

`demo/redline.tape` types the real commands and captures their real output into
`demo/raw/redline/terminal.mp4`. The terminal output comes from
`scripts/demo_gate.py`, which calls the real `mosaic_visual` handler. It is not
retyped text.

### 4. Split-screen composition

`demo/live-gate-film.html`:

- 60% page pane / 40% terminal pane
- page pane `object-fit: contain` on cream; full page visible
- terminal pane cropped to the left 170% so commands are readable
- fixed page swaps in at 16.8s, matching the terminal PASS beat
- end line only: `langersword.github.io/mosaic`
- no stage, no floating card, no lower-third

Record:

```bash
/home/lakshaya/.venv/bin/python demo/record_live_gate.py
```

### 5. Mux

```bash
ffmpeg -y -ss 0.25 -i demo/raw/redline/live-gate.webm -t 20.0 \
  -i demo/raw/bed.wav -map 0:v:0 -map 1:a:0 -t 20 \
  -vf "fps=30,scale=1920:1080,format=yuv420p" \
  -af "atrim=0:20,volume=0.6,afade=t=in:st=0:d=0.5,afade=t=out:st=18.7:d=1.3,loudnorm=I=-18:TP=-2:LRA=11" \
  -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 160k -movflags +faststart \
  ~/Videos/mosaic/mosaic-live-gate.mp4
```

Low bed only. No banger, no TTS, no narration.

### 6. QA

- 20.0s, 1920×1080, 30fps, H.264, AAC.
- Decode whole file; zero errors.
- 3s: page fully visible, terminal readable, command in progress.
- 18s: fixed page and PASS/16/16 terminal visible together.
- Check that the terminal actually says FAIL then PASS; not a staged frame.
- Check that the page pane is not clipped by the split.

## Rules

- **Show the tool, not a poster.** The page and terminal must be live together.
- **Causal beat:** the page switches to fixed at the same beat the terminal
  returns PASS.
- **No overlays.** No arrows, redlines, captions or labels over the product.
- **No stage.** No gradient, no floating browser card, no mockup.
- **No fake terminal.** VHS drives the real shell; no retyped output.
- **No fake page.** The failing and fixed pages are real generated pages with
  controlled faults, and the gate is a real handler run.

## Pitfalls

- A `contain` page leaves cream letterboxing; keep the pane background cream.
- Terminal at 40% is unreadable if you scale the full 1920 frame down. Crop to
  the left 170% in the pane.
- If the page switches before the terminal PASS, causality breaks. Use 16.8s.
- VHS tape total duration must cover both gate runs; check `ffprobe` before
  composing.
- Do not use banger.wav for this cut; low `bed.wav` only.
- If the terminal is still typing at 3s, that is fine; do not cut away from a
  command mid-beat.

## Verification

- `~/Videos/mosaic/mosaic-live-gate.mp4`
- `demo/live-gate-film.html`
- `demo/record_live_gate.py`
- `demo/record_redline.py`, `demo/redline.tape`, `scripts/demo_gate.py`
- Report the real gate results: FAIL 14/16 → PASS 16/16.