#!/usr/bin/env python3
"""Build the checked-in visual-gate sample: one rendered generated page."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mosaic_tools import h_design  # noqa: E402
from mosaic_visual import visual_source  # noqa: E402

BRIEF = "A quiet portfolio for a type designer who needs clients to trust the process"
OUT = ROOT / "site" / "visual"


def main() -> int:
    design = json.loads(h_design({"brief": BRIEF, "mode": "page"}))
    source = design["page"]["files"][0]["content"]
    report = visual_source(source, name="visual-sample.html")
    if not report.get("ok"):
        print(json.dumps(report, indent=2))
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    shots = {}
    for key, path in report.get("screenshots", {}).items():
        suffix = "desktop-1440" if key == "desktop" else "mobile-390"
        target = OUT / f"{suffix}.png"
        shutil.copyfile(path, target)
        shots[key] = f"visual/{suffix}.png"
    data = {
        "target": "generated / A quiet portfolio for a type designer",
        "status": report.get("status"),
        "visual_guarantee": report.get("visual_guarantee"),
        "strict_visual_guarantee": report.get("strict_visual_guarantee"),
        "soft_passed": report.get("soft_passed"),
        "soft_total": report.get("soft_total"),
        "warnings": report.get("warnings", []),
        "evidence_id": report.get("evidence_id"),
        "gates_passed": report.get("gates_passed"),
        "gates_total": report.get("gates_total"),
        "blockers": report.get("blockers", []),
        "screenshots": shots,
        "viewports": [
            {
                "name": v["name"],
                "width": v["width"],
                "height": v["height"],
                "contrast": len(v["contrast_failures"]),
                "overlaps": len(v["overlaps"]),
                "overflow": len(v["overflow_elements"]),
                "focus": v["focus_visible"],
                "reduced": v["motion"]["moving_count"] == 0 or v["motion"]["has_rule"],
                "text": v["text_count"],
                "colors": v["image"]["colors"],
            }
            for v in report.get("viewports", [])
        ],
        "note": report.get("note", ""),
    }
    (ROOT / "site" / "visual-samples.js").write_text(
        "window.MOSAIC_VISUAL = " + json.dumps(data, indent=2) + ";\n", encoding="utf-8"
    )
    print(json.dumps({"ok": True, "status": data["status"], "gates": f"{data['gates_passed']}/{data['gates_total']}", "shots": shots}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())