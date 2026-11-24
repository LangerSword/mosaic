#!/usr/bin/env python3
"""Copy the bundled Palimpsest skills into the active Hermes skills tree."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "skills"
DEST = Path.home() / ".hermes" / "skills" / "web-design"


def main() -> int:
    if not SOURCE.is_dir():
        print(f"missing skills directory: {SOURCE}")
        return 1
    DEST.mkdir(parents=True, exist_ok=True)
    count = 0
    for skill in sorted(SOURCE.iterdir()):
        if not skill.is_dir() or not (skill / "SKILL.md").is_file():
            continue
        target = DEST / skill.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(skill, target)
        count += 1
    print(f"installed {count} Palimpsest skills into {DEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
