Output demo/raw/plugin/plugin.mp4
Set Shell bash
Set FontSize 20
Set FontFamily "JetBrains Mono"
Set Width 1920
Set Height 1080
Set Padding 30
Set MarginFill "#0b0d0c"
Set Theme { "background": "#0b0d0c", "foreground": "#f3efe6", "cursor": "#c64a2e", "selection": "#2548d8", "black": "#0b0d0c", "red": "#c64a2e", "green": "#8fbf9f", "yellow": "#e8b79e", "blue": "#7f9cf5", "magenta": "#c64a2e", "cyan": "#8fbf9f", "white": "#f3efe6", "brightBlack": "#655f55", "brightRed": "#e07a5f", "brightGreen": "#b7d8c0", "brightYellow": "#f0c9a8", "brightBlue": "#a5b4fc", "brightMagenta": "#e07a5f", "brightCyan": "#b7d8c0", "brightWhite": "#ffffff" }
Set TypingSpeed 20ms
Set CursorBlink false
Set BorderRadius 0
Set Margin 0

Hide
Type "cd ~/projects/mosaic && clear"
Enter
Show
Sleep 400ms

Type "./mosaic --help | head -12"
Enter
Sleep 1400ms

Type "./mosaic index | jq -r '.families[].name'"
Enter
Sleep 1800ms

Type "./mosaic design --brief 'A quiet portfolio for a type designer who needs clients to trust the process' --audience 'independent studio founders' --constraints 'accessible, no hover-only, mobile-first' --mode page --seed 7 > /tmp/mosaic.json"
Enter
Sleep 1200ms

Type "jq -r '.chosen.name, .chosen.scores.overall' /tmp/mosaic.json"
Enter
Sleep 900ms

Type "jq -r '.page.files[0].content' /tmp/mosaic.json > /tmp/mosaic.html"
Enter
Sleep 500ms

Type "./mosaic visual --target /tmp/mosaic.html | jq '{status, gates_passed, gates_total}'"
Enter
Sleep 4200ms

Type "./mosaic taste --path /tmp/mosaic.html | jq '{taste_index, confidence}'"
Enter
Sleep 1200ms

Type "./mosaic components | jq '.components | length'"
Enter
Sleep 900ms

Type "printf '\\n  MOSAIC / 13 TOOLS / 23 SKILLS\\n\\n'"
Enter
Sleep 2600ms