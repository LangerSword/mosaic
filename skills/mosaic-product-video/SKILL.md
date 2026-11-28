---
name: mosaic-product-video
description: Use when producing a demo for the Mosaic plugin itself.
version: 0.6.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video, demo, plugin, mosaic, vhs, ffmpeg, terminal]
    related_skills: [mosaic, mosaic-visual, demo-video-production, interactive-tty-automation]
---

# Mosaic Plugin Video

A **terminal demo of the plugin**, not a tour of the showcase site. The viewer
sees the actual `mosaic` CLI commands and the actual JSON output: help surface,
reference families, a directed page, the visual gate, a taste profile and the
component count.

**Runtime:** 31s. **Viewport:** 1920×1080. **Source:** VHS terminal recording.

## Sequence

```text
00-03  ./mosaic --help
       index / stacks / recipe / study / design / critique / score / taste
       visual / audit / components / forge / invent
03-06  ./mosaic index
       thirteen reference families
06-12  ./mosaic design --mode page --seed 7
       chosen: The Field Guide / overall 9.0
12-16  extract .page.files[0].content to /tmp/mosaic.html
16-22  ./mosaic visual --target /tmp/mosaic.html
       status: pass / 16 gates passed / 16 total
22-25  ./mosaic taste --path /tmp/mosaic.html
       taste_index 7.9 / confidence low
25-28  ./mosaic components
       20 public component records
28-31  MOSAIC / 13 TOOLS / 23 SKILLS
```

## Build

### 1. Real CLI

`./mosaic` is a thin wrapper around `mosaic_cli.py`:

```bash
cd ~/projects/mosaic
./mosaic --help
```

The demo must use this CLI, not the site UI.

### 2. VHS tape

`demo/plugin.tape` holds the exact commands. Every command and every line of
output is real. Do not paste fabricated JSON.

```bash
vhs demo/plugin.tape
```

Writes `demo/raw/plugin/plugin.mp4` at 1920×1080, 25fps.

### 3. Mux

```bash
python ~/.hermes/skills/creative/demo-video-production/scripts/make_music.py \
  demo/raw/plugin/bed.wav 32

ffmpeg -y -i demo/raw/plugin/plugin.mp4 -i demo/raw/plugin/bed.wav \
  -map 0:v:0 -map 1:a:0 -t 31 \
  -vf "fps=30,scale=1920:1080,format=yuv420p,fade=t=in:st=0:d=0.3,fade=t=out:st=29.5:d=1.5" \
  -af "atrim=0:31,volume=0.5,afade=t=in:st=0:d=0.5,afade=t=out:st=29:d=2,loudnorm=I=-18:TP=-2:LRA=12" \
  -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 160k -movflags +faststart \
  ~/Videos/mosaic/mosaic-plugin-demo.mp4
```

No TTS. Low bed only.

### 4. QA

- 31.0s, 1920×1080, 30fps, H.264, AAC.
- Decode zero errors.
- 4s: `mosaic --help` and families visible.
- 18s: design command and `The Field Guide / 9.0` visible.
- 25s: `visual` returns `16 / 16`.
- 30s: `20` components and `13 TOOLS / 23 SKILLS`.
- Every command fits the terminal width; break long commands rather than
  letting the right edge clip the `jq` filter.

## Rules

- **Plugin, not showcase.** No generated-site tour, no before/after page film.
- **Real command → real output.** VHS drives the shell; no retyped JSON.
- **Show the differentiation:** design direction, measured visual gates, taste
  confidence, public component count.
- **Keep the terminal plain.** No fake window chrome, no stage, no lower-third.
- **One take.** The viewer sees the actual workflow, including the gate run.

## Pitfalls

- `mosaic` is not on PATH; call the repo wrapper `./mosaic` or the Python CLI.
- VHS cannot parse escaped double quotes inside `Type`; use single-quoted shell
  arguments.
- Long commands wrap; shorten the `jq` projection instead of shrinking the font.
- The VHS file is 25fps; convert to 30fps during mux.
- Do not use the site's generated page as the demo subject; this video is about
  the plugin surface and its outputs.

## Verification

- `~/Videos/mosaic/mosaic-plugin-demo.mp4`
- `demo/plugin.tape`
- `demo/raw/plugin/plugin.mp4`
- `mosaic` wrapper + `mosaic_cli.py`
- Report: 13 tools / 23 skills, 16/16 visual gates, 20 components, 31s.