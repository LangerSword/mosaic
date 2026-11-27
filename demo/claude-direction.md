# Mosaic 20s film: direction

## Concept

**One page, one line, re-measured.** The camera never leaves the real generated page. The film holds on a single line of body copy that fails contrast, cuts to the real gate's output, then cuts back to the same line after the token changes. The viewer's eye does the work: the same pixels, two verdicts.

No composition is added to the product. The only typography is the gate's own terminal output and one end line.

## Assets

Real, existing:
- `demo/raw/redline/fail.webm`: generated page, failing state
- `demo/raw/redline/fixed.webm`: same page, token changed
- `demo/raw/bed.wav`: synth bed (use this; drop `banger.wav`)
- `site/visual/desktop-1440.png`, `site/visual/mobile-390.png`: reference stills only, not footage

Must be recorded before cutting (none found in repo):
- Real PTY capture of `mosaic_visual` run, before (14/16, contrast 2.23:1 vs 4.5) and after (16/16). Use `asciinema`/`scripts` or VHS against the real shell. No retyped text.
- Playwright 1920×1080 capture at the same framing and location for both states, re-run from a real `mosaic_visual` pass. Verify the fail/fixed webms match this run before using them.
- 390px capture of the range control at 16px target → fixed height.

## Beat sheet (20.0s, 1920×1080, 30fps)

| Time | Shot | Content |
|---|---|---|
| 0.00–1.50 | Black, then hard cut | Real terminal: the brief command runs (recorded PTY). No logo. |
| 1.50–4.00 | Hard cut to page | `fail.webm`, locked framing on the body-copy line. Camera pushes 1.00→1.08 over 2.5s. |
| 4.00–6.00 | Hard cut to terminal | Real `mosaic_visual` output: `contrast 2.23:1 < 4.5 FAIL`, `14/16`. Hold. |
| 6.00–9.00 | Hard cut to page | Same `fail.webm` frame, same framing. Hold 0.5s, then 0.5s push to 1.08. Nothing added. |
| 9.00–11.00 | Hard cut to terminal | Token edit command runs (real PTY). Diff line visible. |
| 11.00–13.00 | Hard cut to page | `fixed.webm`: same framing, same line, now legible. Push 1.00→1.08 to match. |
| 13.00–15.50 | Hard cut to terminal | Real re-run output: `16/16`, evidence id. |
| 15.50–17.50 | Hard cut to 390px capture | Range control at new target height. Static hold 1.5s. |
| 17.50–20.00 | Black | One line, Plex Mono, 1 size: `langersword.github.io/mosaic`. Nothing else. |

Pacing rule: every cut lands on a terminal line or a page change. No cut without a visible state change.

## Camera, type, motion

- **Camera:** locked-off or a single slow push (max 8% scale over the shot). No pans, no handheld, no whip.
- **Cuts:** hard cuts only. Max 6-frame dissolve on terminal↔page changes. No wipes, no fades to colour.
- **Type:** the terminal's own type and the page's own type. One end line in IBM Plex Mono, regular, no caps treatment. No Anton, no Playfair, no headline in the film.
- **Motion:** only what the product does. No animated overlays, no tweened numbers, no glow, no grain.
- **Colour:** no grade beyond the captures' own. No gradient, no vignette, no backdrop.
- **Sound:** `bed.wav` at low level, ducked 3dB under terminal keystrokes. Real keystrokes and clicks from the captures. No TTS, no banger.

## Delete

- `demo/gate-film.html` and `demo/redline-film.html`: the veil, panel, rule, grain, numbered overlays, lower-third type, and "EVIDENCE, NOT VIBES" end card. Delete the files.
- `demo/raw/redline/redline-film.webm`, `demo/raw/redline/banger.wav`: rejected cut and banger. Delete from release.
- `demo/redline/fail.html` and `demo/redline/fixed.html`: check first. If they contain annotations, delete. The page itself is kept, not the wrapper.
- `demo/raw/endcard.webm`, `demo/raw/kinetic.webm`, `demo/edit/*`: prior cuts. Remove from release.
- Any tag, note, scanner line, or `.low` bar in the rendering pipeline.

## Done when

- `ffprobe`: 20.0s, 1920×1080, 30fps, H.264, AAC.
- Every terminal line in the film appears in the raw recording of a real run.
- A viewer watching only the film can say what changed between 1.50s and 11.00s: the line went from 2.23:1 to passing, and the gate went from 14/16 to 16/16.
