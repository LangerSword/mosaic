#!/usr/bin/env python3
"""Thin CLI over the Mosaic tool handlers.

Same handlers, same JSON; useful for a demo or a CI smoke test without Hermes.
"""
from __future__ import annotations

import argparse
import json

from mosaic_tools import TOOL_SPECS, h_audit, h_components, h_forge, h_index, h_invent, h_recipe, h_stacks


def main() -> int:
    parser = argparse.ArgumentParser(prog="mosaic", description="Design direction for Hermes")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("index", help="list reference families")
    sub.add_parser("stacks", help="list the framework and skill matrix")

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

    forge = sub.add_parser("forge", help="generate a component starter")
    forge.add_argument("--kind", required=True)
    forge.add_argument("--stack", default="html")
    forge.add_argument("--motion", default="css")
    forge.add_argument("--brief", default="")

    invent = sub.add_parser("invent", help="compose interaction candidates")
    invent.add_argument("--brief", required=True)
    invent.add_argument("--constraints", default="")
    invent.add_argument("--count", type=int, default=3)
    invent.add_argument("--seed", type=int)

    args = parser.parse_args()
    if args.cmd == "index":
        out = h_index({})
    elif args.cmd == "stacks":
        out = h_stacks({})
    elif args.cmd == "components":
        out = h_components({"family": args.family, "query": args.query})
    elif args.cmd == "forge":
        out = h_forge({"kind": args.kind, "stack": args.stack,
                       "motion": args.motion, "brief": args.brief})
    elif args.cmd == "invent":
        out = h_invent({"brief": args.brief, "constraints": args.constraints,
                        "count": args.count, "seed": args.seed})
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
