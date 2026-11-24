# Mosaic demo film

60-second cut: kinetic intro, real Mosaic site footage, and an end card.

## Source

- `kinetic.html` — 8-second kinetic intro at 1920x1080.
- `endcard.html` — 8-second proof and lockup.
- `record_ui.py` — records the live site at 1920x1080 with a visible cursor. `record_ui_long.py` is the paced variant used for the final cut.
- `record_film.py` — records the two HTML pieces with Playwright.
- `make_video.sh` — normalizes the three takes, adds captions and the in-repo ambient bed, and muxes the final file.
- `scripts/make_music.py` from the `demo-video-production` skill generates `raw/bed.wav`; no samples, no voice.

## Build

```bash
python3 demo/record_film.py
python3 demo/record_ui_long.py
python3 demo/make_video.sh
```

The final file is `~/Videos/mosaic/mosaic-demo.mp4`. Raw recordings stay out of git.

## Notes

The UI portion is captured from the running site through Playwright, not Recordly. The cut is Recordly-style: continuous UI, visible cursor, a 1.11x camera crop and slow 1.25x pacing. The site URL is in the end card. No paid Construct code or assets are used.
