#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RAW="$ROOT/demo/raw"
EDIT="$ROOT/demo/edit"
OUTDIR="$HOME/Videos/mosaic"
FONT="$ROOT/site/fonts/Barlow-Medium.ttf"
MONO="$ROOT/site/fonts/IBMPlexMono-Regular.ttf"
mkdir -p "$EDIT" "$OUTDIR"

# The raw takes are 25 fps WebM. Normalize every cut to 30 fps, 1920x1080.
# The UI is zoomed 1.11x to match the Recordly-style camera, and slowed 1.25x
# so the real cursor and section changes can breathe.
ffmpeg -y -v error -i "$RAW/kinetic.webm" -ss 0.4 -t 8.0 \
  -vf "fps=30,scale=1920:1080,format=yuv420p,fade=t=in:st=0:d=0.22,fade=t=out:st=7.68:d=0.32" \
  -an -c:v libx264 -crf 18 -preset medium "$EDIT/01-kinetic.mp4"

ffmpeg -y -v error -i "$RAW/ui.webm" -ss 0.55 -t 34.4 \
  -vf "setpts=1.25*PTS,fps=30,crop=1728:972:96:54,scale=1920:1080,format=yuv420p,fade=t=in:st=0:d=0.32,fade=t=out:st=42.4:d=0.7" \
  -an -c:v libx264 -crf 18 -preset medium "$EDIT/02-ui.mp4"

ffmpeg -y -v error -i "$RAW/endcard.webm" -ss 0.35 -t 8.0 \
  -vf "fps=30,scale=1920:1080,format=yuv420p,fade=t=in:st=0:d=0.35" \
  -an -c:v libx264 -crf 18 -preset medium "$EDIT/03-end.mp4"

printf "file '%s'\nfile '%s'\nfile '%s'\n" \
  "$EDIT/01-kinetic.mp4" "$EDIT/02-ui.mp4" "$EDIT/03-end.mp4" > "$EDIT/concat.txt"

ffmpeg -y -v error -f concat -safe 0 -i "$EDIT/concat.txt" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -r 30 -an \
  "$EDIT/silent.mp4"

# Captions sit in the lower-left gutter, not over the component cards.
CAPTIONS="$EDIT/captions.txt"
cat > "$CAPTIONS" <<'EOF'
drawtext=fontfile=FONT:text='FORGE / ONE BRIEF, SIX STACKS':fontcolor=0xf3efe6:fontsize=22:box=1:boxcolor=0x15130f@0.74:boxborderw=10:x=78:y=1018:enable='between(t,8.0,18.0)',
drawtext=fontfile=FONT:text='FORGE LAB / REAL GENERATED STATES':fontcolor=0xf3efe6:fontsize=22:box=1:boxcolor=0x15130f@0.74:boxborderw=10:x=78:y=1018:enable='between(t,18.0,28.0)',
drawtext=fontfile=FONT:text='TASTE / SCORE BEFORE CODE':fontcolor=0xf3efe6:fontsize=22:box=1:boxcolor=0x15130f@0.74:boxborderw=10:x=78:y=1018:enable='between(t,28.0,39.0)',
drawtext=fontfile=FONT:text='COMPONENTS / 20 PUBLIC SPECIMENS':fontcolor=0xf3efe6:fontsize=22:box=1:boxcolor=0x15130f@0.74:boxborderw=10:x=78:y=1018:enable='between(t,39.0,51.0)'
EOF
# drawtext fontfile expects an escaped path on some builds; substitute the
# absolute font path after the template is written.
sed -i "s|fontfile=FONT|fontfile='$FONT'|g" "$CAPTIONS"
FILTERS=$(tr '\n' ' ' < "$CAPTIONS")

# Ambient in-repo bed: no samples, no voice. Duration-locked at 60s.
ffmpeg -y -v error -i "$RAW/bed.wav" \
  -af "atrim=0:60,afade=t=in:st=0:d=1.1,afade=t=out:st=57.6:d=2.4,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:a pcm_s16le "$EDIT/bed.wav"

ffmpeg -y -v error -i "$EDIT/silent.mp4" -i "$EDIT/bed.wav" \
  -vf "$FILTERS" \
  -map 0:v:0 -map 1:a:0 -t 60 \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  "$OUTDIR/mosaic-demo.mp4"

echo "wrote $OUTDIR/mosaic-demo.mp4"
