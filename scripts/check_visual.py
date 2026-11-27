#!/usr/bin/env python3
"""CI gate: fail unless the real site and a generated page pass strict visual gates."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mosaic_tools import h_design, h_visual  # noqa: E402


def report(label: str, payload: dict) -> bool:
    ok = bool(payload.get("strict_visual_guarantee"))
    print(json.dumps({
        "label": label,
        "ok": ok,
        "status": payload.get("status"),
        "visual_guarantee": payload.get("visual_guarantee"),
        "strict_visual_guarantee": payload.get("strict_visual_guarantee"),
        "gates": f"{payload.get('gates_passed')}/{payload.get('gates_total')}",
        "soft": f"{payload.get('soft_passed')}/{payload.get('soft_total')}",
        "blockers": payload.get("blockers", []),
        "warnings": payload.get("warnings", []),
        "evidence_id": payload.get("evidence_id"),
    }, indent=2))
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", help="URL of the built site")
    parser.add_argument("--generated", action="store_true", help="also render a generated page")
    parser.add_argument("--strict", action="store_true", default=True,
                        help="require strict_visual_guarantee (default)")
    args = parser.parse_args()
    if not args.site and not args.generated:
        parser.error("pass --site and/or --generated")
    results = []
    if args.site:
        results.append(report(args.site, json.loads(h_visual({"target": args.site}))))
    if args.generated:
        page = json.loads(h_design({
            "brief": "A quiet portfolio for a type designer who needs clients to trust the process",
            "mode": "page",
        }))
        results.append(report("generated", json.loads(h_visual({
            "source": page["page"]["files"][0]["content"],
        }))))
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())