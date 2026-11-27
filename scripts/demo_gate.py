#!/usr/bin/env python3
"""Print the real visual-gate result in a film-friendly, factual form."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mosaic_tools import h_visual  # noqa: E402


def main() -> int:
    target = sys.argv[1]
    result = json.loads(h_visual({"target": target}))
    print(f"TARGET  {Path(target).name}")
    print(f"STATUS  {result.get('status', 'error').upper()}")
    print(f"GATES   {result.get('gates_passed')} / {result.get('gates_total')}")
    print(f"SOFT    {result.get('soft_passed')} / {result.get('soft_total')}")
    if result.get("blockers"):
        for blocker in result["blockers"]:
            print(f"BLOCK   {blocker}")
    else:
        print("BLOCK   none")
    for view in result.get("viewports", []):
        if view.get("contrast_failures"):
            print(f"CONTRAST {view['name']}: {len(view['contrast_failures'])} failure(s)")
        if view.get("small24"):
            print(f"TARGETS  {view['name']}: {len(view['small24'])} under 24px")
    print(f"EVIDENCE {result.get('evidence_id', '-')}")
    return 0 if result.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())