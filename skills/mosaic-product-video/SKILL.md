---
name: mosaic-product-video
description: Use when producing a Mosaic product film, not a slide demo.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video, demo, product, mosaic, playwright, ffmpeg]
    related_skills: [mosaic, mosaic-visual, demo-video-production, webreel]
---

# Mosaic Product Video

A 26-second product film built from **real Mosaic captures** on a designed
stage. The reference is Maaz's FlickAI cut: one visual world, floating UI,
hard cuts, kinetic type, sound — but with one coherent proof loop instead of a
feature smorgasbord.

## When to use

- Mosaic needs a launch/README/post demo.
- The existing 60-second scroll-and-slide film feels like a website tour.
- You need a short social clip that proves the gate, the director and the forge.

Do not make a fake UI, a retyped terminal, or a narrated TTS cut.

## The film

**Runtime:** 26s. **Viewport:** 1920×1080. **Source:** a real site capture.

```text
0.0-2.5  LOOKS FINE. / UNTIL YOU OPEN IT.
2.5-6.2  THE GATE CATCHES IT. / 16 hard gates + 3 soft
6.2-10.2 ONE BRIEF. / SEVEN STRUCTURES.
10.2-14.2 REAL INTERACTIONS. / magnetic link, lens, swipe
14.2-18.2 TWELVE LIVE PIECES.
18.2-21.8 EVIDENCE, NOT VIBES. / 16/16 + evidence id
21.8-26.0 REFERENCE IN. ORIGINAL OUT. / URL
```

One problem, one system, one proof loop. No logo intro longer than a beat.

## Pipeline

### 1. Capture the real product

```bash
# local showcase on :4322
cd ~/projects/mosaic
/home/lakshaya/.venv/bin/python demo/record_product_reel.py
```

This writes `demo/raw/product/ui.webm`. It uses Playwright `recordVideo`,
injects a styled cursor, and visits: hero → visual gate → director → forge lab
(magnetic/lens) → component ledger → install. Do not replace this with stills;
the film's centre panel is real product footage.

### 2. Compose the stage

`demo/product-film.html` is 1920×1080:

- navy → clay gradient stage, grid and grain
- real UI footage inside one floating window on the right
- type on the left, never over the UI
- one active headline per beat, hard state changes
- evidence metric panel, URL and lockup

Start the film with `window.__startFilm()`. Do not capture the HTML until
`window.__filmReady` is true and the video has `readyState >= 2`.

### 3. Record the film

```bash
/home/lakshaya/.venv/bin/python demo/record_product_film.py
```

Writes `demo/raw/product/film.webm` (~28s including pre-roll).

### 4. Sound and mux

Use the in-repo synth bed. Maaz's lesson is sound design, not voiceover.

```bash
python ~/.hermes/skills/creative/demo-video-production/scripts/make_banger.py \
  demo/raw/product/banger.wav 28

ffmpeg -y -ss 0.35 -i demo/raw/product/film.webm -t 26.0 \
  -i demo/raw/product/banger.wav \
  -map 0:v:0 -map 1:a:0 -t 26 \
  -vf "fps=30,scale=1920:1080,format=yuv420p,fade=t=in:st=0:d=0.25,fade=t=out:st=24.9:d=1.1" \
  -af "atrim=0:26,afade=t=in:st=0:d=0.35,afade=t=out:st=24.0:d=2.0,loudnorm=I=-15:TP=-1.5:LRA=10" \
  -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -movflags +faststart \
  ~/Videos/mosaic/mosaic-product-film.mp4
```

### 5. QA before calling it done

- `ffprobe` exact duration, H.264, 1920×1080, 30fps, audio present.
- `ffmpeg -v error -i OUT -f null -` and require zero decode errors.
- Contact sheet at 2s intervals and inspect: no blank frames, no overlay over
  the UI, no clipped headline, product proof visible.
- Check first 3s and last 3s: opening state and clean end card.
- Confirm the UI footage is current Mosaic, not an old capture.

## Direction rules

- **No full-screen slide.** UI is an object on a stage.
- **No overlay over the UI.** Copy lives in the left gutter.
- **One idea per beat.** 2–4s.
- **Hard cuts, not soft crossfades.**
- **No voice/TTS.** Sound-on bed and hit points.
- **No fake UI or invented metrics.** The gate numbers come from Mosaic.
- **No feature list.** One proof loop.

## Pitfalls

- `page.video` starts before the stage paints; trim pre-roll (`-ss 0.35`), then
  verify the first frame.
- A `<video>` inside a file:// film must reach `readyState >= 2` before record.
- Don't put the copy block over the right-hand window; that was the first cut's
  failure. Keep copy under 26% width and the window at 40%+ left.
- If the UI text is too small, capture the product at 1440×900 inside a
  1920×1080 film; do not shrink a 1920 capture into a 53% window and expect
  legibility.
- Re-record after changing `.frame` geometry. The old raw take does not match.
- Keep the output out of the repo if it exceeds GitHub's media limits; publish
  through a release.

## Verification

- File: `~/Videos/mosaic/mosaic-product-film.mp4`
- Storyboard: `demo/product-film.html`
- Capture: `demo/record_product_reel.py`
- Record: `demo/record_product_film.py`
- Report duration, fps, codec, audio, contact sheet path and any remaining
  subjective critique.