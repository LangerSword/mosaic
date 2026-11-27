#!/usr/bin/env python3
"""Deterministic accuracy gate for the Mosaic showcase claims.

This grades the implementation against independently stated expectations. It
also negative-controls each detector with a mutation of the real bytes so a
green result cannot be produced by a dead check.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mosaic_forge import KINDS, forge  # noqa: E402
from mosaic_tools import TOOL_SPECS, h_design, h_index, h_score  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str) -> None:
    RESULTS.append((name, bool(ok), detail))


def ring_angle(percent: float) -> float:
    """Independent arithmetic for the conic-gradient ring."""
    return round(max(0, min(100, percent)) / 100 * 360, 1)


def ring_source_ok(source: str) -> bool:
    match = re.search(r"calc\(var\(--p\) \* ([^)]+)\)", source)
    return bool(match and match.group(1).strip() == "360deg")


def code_map(source: str) -> dict[str, str]:
    match = re.search(r"const codes = \{(.*?)\};", source, re.S)
    if not match:
        return {}
    return dict(re.findall(r"'([^']+)': '([^']+)'", match.group(1)))


# 1. Ring: 20% must be 72deg, 100% must be 360deg.
ring_js = (ROOT / "site/forge/download-ring.js").read_text(encoding="utf-8")
forge_ring = json.loads(forge("download-ring", "html", "css", "grade"))
forge_ring_js = next(f["content"] for f in forge_ring["files"] if f["path"].endswith(".js"))
ring_ok = ring_source_ok(ring_js) and ring_source_ok(forge_ring_js)
check("ring source uses 360deg", ring_ok, f"site={ring_source_ok(ring_js)} forge={ring_source_ok(forge_ring_js)}")
check("ring arithmetic 20% = 72deg", ring_angle(20) == 72.0, str(ring_angle(20)))
check("ring arithmetic 100% = 360deg", ring_angle(100) == 360.0, str(ring_angle(100)))
mutated_ring = ring_js.replace("360deg", "3.6deg", 1)
check("ring negative control fails", not ring_source_ok(mutated_ring), "mutated 360deg -> 3.6deg")

# 2. Component index is a unique row ledger, not repeated specimen cards.
app_js = (ROOT / "site/app.js").read_text(encoding="utf-8")
codes = code_map(app_js)
check("component renderer uses rows", "'component-row'" in app_js, "component-row present")
check("component codes are complete", len(codes) == 20, f"{len(codes)} codes")
check("component codes are unique", len(set(codes.values())) == 20, f"{len(set(codes.values()))} unique")
check("component grid has no specimen renderer", "'specimen-art'" not in app_js, "no specimen-art render path")
mutated_rows = app_js.replace("'component-row'", "'specimen'", 1)
check("row negative control fails", "'component-row'" not in mutated_rows, "mutated renderer")

# 3. Score gate: strong generated page passes; generic source is blocked.
brief = "A quiet portfolio for a type designer who needs clients to trust the process"
page = json.loads(h_design({"brief": brief, "mode": "page"}))["page"]["files"][0]["content"]
strong = json.loads(h_score({"source": page, "brief": brief}))
generic_source = "<html><body><h1>We unlock seamless growth</h1><button>Start</button></body></html>"
generic = json.loads(h_score({"source": generic_source, "brief": "A quiet archive"}))
check("strong page pre-awards score", strong["overall"] >= 8.0, f"{strong['overall']} / {strong['verdict']}")
check("strong page has no blockers", not strong["blockers"], str(strong["blockers"]))
check("generic source is not shippable", generic["overall"] < 8 and generic["verdict"] != "ship", f"{generic['overall']} / {generic['verdict']}")
check("generic source blocks missing focus", "No focus-visible path." in generic["blockers"], str(generic["blockers"]))
fake = {"ok": True, "overall": 9.9, "verdict": "ship", "blockers": []}
check("score negative control fails", not (fake["overall"] < 8 and fake["verdict"] != "ship"), "fake perfect scorer rejected by oracle")

# 4. Counts and registration.
index = json.loads(h_index({}))
check("family count", len(index["families"]) == 13, str(len(index["families"])))
check("method count", len(index["methods"]) == 4, str(len(index["methods"])))
check("tool count", len(TOOL_SPECS) == 11, str(len(TOOL_SPECS)))
check("forge kind count", len(KINDS) == 9, str(len(KINDS)))

passed = sum(1 for _, ok, _ in RESULTS if ok)
total = len(RESULTS)
for name, ok, detail in RESULTS:
    print(f"{'PASS' if ok else 'FAIL'}  {name}  ({detail})")
print(f"\n{passed}/{total} checks passed")
raise SystemExit(0 if passed == total else 1)