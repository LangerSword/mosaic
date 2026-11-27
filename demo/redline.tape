Output demo/raw/redline/terminal.mp4

Set FontSize 20
Set Width 1920
Set Height 1080
Set Padding 28
Set MarginFill "#0b0d0c"
Set Theme { "background": "#0b0d0c", "foreground": "#f3efe6", "cursor": "#c64a2e", "selection": "#2548d8" }
Set CursorBlink false
Set TypingSpeed 28ms

Type "cp demo/redline/fail.html demo/redline/candidate.html"
Enter
Sleep 900ms

Type "python scripts/demo_gate.py demo/redline/candidate.html"
Enter
Sleep 3s

Type "sed -i 's/#d89a84/#be402d/' demo/redline/candidate.html"
Enter
Sleep 500ms
Type "sed -i 's/height:16px/height:44px/' demo/redline/candidate.html"
Enter
Sleep 1s

Type "python scripts/demo_gate.py demo/redline/candidate.html"
Enter
Sleep 8s