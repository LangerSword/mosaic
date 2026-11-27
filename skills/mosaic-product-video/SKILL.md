---
name: mosaic-product-video
description: Use when producing a Mosaic product film, not a slide demo.
version: 0.2.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video, demo, product, mosaic, playwright, ffmpeg]
    related_skills: [mosaic, mosaic-visual, demo-video-production, webreel]
---

# Mosaic Product Video

A short product film where the **page is the stage**. No gradient backdrop, no
floating browser card, no cute mockup. The film is a live audit:

> a candidate page looks finished -> the visual gate finds two real failures ->
> the page is fixed -> 16/16 -> evidence, not vibes.

The Mosaic site and langersword.in are demos of what Mosaic can create. The
film must show that creation and verification, not advertise the demo page.

## The cut

**Runtime:** 18s. **Viewport:** 1920×1080. **Source:** two real captures of a
generated candidate page: `fail.webm` and `fixed.webm`.

```text
0.0-2.0  A PAGE CAN LOOK FINISHED.       real candidate page
2.0-4.0  CONTRAST 2.23 / 4.5             redline + callout
4.0-7.0  TARGET 16 / 24  /  14/16        redline + callout
7.0-9.0  THE SAME PAGE. FIXED.           hard cut to fixed capture
9.0-12.0 16/16                            green scan + pass
12.0-16.6 EVIDENCE, NOT VIBES.            lower-third narrative
16.6-18.0 end card                        black, lockup, URL
```

No gradient stage. No floating UI card. One black lower-third bar. One thin
scanline. Three callouts. One hard cut from failure to fixed.

## Pipeline

### 1. Build the candidate pair

```bash
cd ~/projects/mosaic
python scripts/build_redline.py
```

`demo/redline/fixed.html` is the real generated page. `demo/redline/fail.html`
is the same page with a failing signal token and a 16px range control. This is
a candidate fixture, not a fake product screenshot. Run the actual gate:

```text
mosaic_visual(target="demo/redline/fail.html")  -> 14/16 hard
mosaic_visual(target="demo/redline/fixed.html") -> 16/16 hard
```

### 2. Capture real footage

```bash
/home/lakshaya/.venv/bin/python demo/record_redline.py
```

Writes `demo/raw/redline/fail.webm` and `fixed.webm` at 1920×1080. Each clip
scrolls the real page to the failing signature and controls. No browser chrome.

### 3. Compose and record

`demo/redline-film.html`:

- full-bleed page footage
- redline scan and three anchored callouts
- black lower-third bar (`A PAGE CAN LOOK FINISHED.` → `THE GATE SAYS NO.` →
  `THE SAME PAGE. FIXED.` → `EVIDENCE, NOT VIBES.`)
- hard cut at 7s; green scan and 16/16 after
- end card on black

```bash
/home/lakshaya/.venv/bin/python demo/record_redline_film.py
```

### 4. Sound and mux

```bash
python ~/.hermes/skills/creative/demo-video-production/scripts/make_banger.py \
  demo/raw/redline/banger.wav 20

ffmpeg -y -ss 0.35 -i demo/raw/redline/redline-film.webm -t 18.0 \
  -i demo/raw/redline/banger.wav \
  -map 0:v:0 -map 1:a:0 -t 18 \
  -vf "fps=30,scale=1920:1080,format=yuv420p,fade=t=in:st=0:d=0.2,fade=t=out:st=17.2:d=0.8" \
  -af "atrim=0:18,afade=t=in:st=0:d=0.3,afade=t=out:st=16.2:d=1.8,loudnorm=I=-15:TP=-1.5:LRA=10" \
  -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -movflags +faststart \
  ~/Videos/mosaic/mosaic-redline.mp4
```

No TTS. Sound-on, in-repo synth.

### 5. QA

- `ffprobe`: 18.0s, 1920×1080, 30fps, H.264, AAC.
- Decode whole file: `ffmpeg -v error -i OUT -f null -`; require zero errors.
- 5s frame: failure obvious (pale accent, redline, 14/16), page readable.
- 9s frame: fixed state clearly different, green 16/16, no clipping.
- Contact sheet: no black/missing frames; end card readable.

## Rules

- **No gradient stage, no floating card.** That is the old, rejected grammar.
- **The page is the stage.** Full-bleed real footage.
- **One concrete failure, one concrete fix.** Show the number.
- **Redlines must sit in margins**, not cover the proof.
- **Hard cut, not crossfade**, at the fix.
- **No feature list.** One proof loop.
- **No fake UI.** The candidate pages are real generated pages with controlled
  faults; the gate result is real.

## Pitfalls

- A pale failing token (`#d89a84`) is a real 2.23:1 failure and is visible;
  a 4.35 token is too subtle on screen.
- The `fail` and `fixed` captures must have identical scroll paths or the cut
  reads as a different page.
- Don't put the lower-third over the failing controls; it covers the proof.
- The redline scan is 1px; add a faint glow, not a thick bar.
- Re-record both source clips after changing the candidate pages.
- Keep the film under 20s; this concept gets weaker when repeated.

## Verification

- `~/Videos/mosaic/mosaic-redline.mp4`
- `demo/redline-film.html`
- `demo/record_redline.py` / `demo/record_redline_film.py`
- `scripts/build_redline.py`
- Report the exact gate results: 14/16 fail, 16/16 fixed.