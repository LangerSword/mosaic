#!/usr/bin/env python3
"""Thin CLI over the Mosaic tool handlers.

Same handlers, same JSON; useful for a demo or a CI smoke test without Hermes.
"""
from __future__ import annotations

import argparse
import json

from mosaic_tools import TOOL_SPECS, h_audit, h_components, h_index, h_recipe


def main() -> int:
    parser = argparse.ArgumentParser(prog="mosaic", description="Design direction for Hermes")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("index", help="list reference families")

    recipe = sub.add_parser("recipe", help="build a design direction")
    recipe.add_argument("--brief", required=True)
    recipe.add_argument("--mood", default="quiet")
    recipe.add_argument("--stack", default="HTML/CSS/JS")
    recipe.add_argument("--constraints", default="")

    audit = sub.add_parser("audit", help="scan a local text source")
    audit.add_argument("--path")
    audit.add_argument("--source")

    comps = sub.add_parser("components", help="list public component observations")
    comps.add_argument("--family")
    comps.add_argument("--query")

    args = parser.parse_args()
    if args.cmd == "index":
        out = h_index({})
    elif args.cmd == "components":
        out = h_components({"family": args.family, "query": args.query})
    elif args.cmd == "recipe":
        out = h_recipe({"brief": args.brief, "mood": args.mood,
                        "stack": args.stack, "constraints": args.constraints})
    else:
        out = h_audit({"path": args.path, "source": args.source})
    print(out)
    try:
        return 0 if json.loads(out).get("ok") else 1
    except json.JSONDecodeError:
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
