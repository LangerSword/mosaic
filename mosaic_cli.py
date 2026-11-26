#!/usr/bin/env python3
"""Thin CLI over the Mosaic tool handlers.

Same handlers, same JSON; useful for a demo or a CI smoke test without Hermes.
"""
from __future__ import annotations

import argparse
import json

from mosaic_tools import (TOOL_SPECS, h_audit, h_components, h_critique, h_design, h_forge,
                         h_index, h_invent, h_recipe, h_stacks, h_study)


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

    study = sub.add_parser("study", help="map a reference observation set")
    study.add_argument("--reference", required=True, help="reference name or URL")
    study.add_argument("--observations", default="{}", help="JSON object of observations")
    study.add_argument("--brief", default="")
    study.add_argument("--constraints", default="")

    design = sub.add_parser("design", help="direct a brief into a design and optional page")
    design.add_argument("--brief", required=True)
    design.add_argument("--audience", default="")
    design.add_argument("--constraints", default="")
    design.add_argument("--references", default="")
    design.add_argument("--mood", default="")
    design.add_argument("--stack", default="HTML/CSS/JS")
    design.add_argument("--mode", choices=("direction", "page"), default="direction")
    design.add_argument("--seed", type=int)

    critique = sub.add_parser("critique", help="critique a local source for design specificity")
    critique.add_argument("--path")
    critique.add_argument("--source")
    critique.add_argument("--brief", default="")

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
    elif args.cmd == "study":
        try:
            observations = json.loads(args.observations)
        except json.JSONDecodeError:
            observations = {}
        out = h_study({"reference": {"name": args.reference, "observations": observations},
                       "brief": args.brief, "constraints": args.constraints})
    elif args.cmd == "design":
        references = [item.strip() for item in args.references.split(";") if item.strip()]
        out = h_design({"brief": args.brief, "audience": args.audience,
                        "constraints": args.constraints, "references": references,
                        "mood": args.mood, "stack": args.stack,
                        "mode": args.mode, "seed": args.seed})
    elif args.cmd == "critique":
        out = h_critique({"path": args.path, "source": args.source, "brief": args.brief})
    else:
        out = h_audit({"path": args.path, "source": args.source})
    print(out)
    try:
        return 0 if json.loads(out).get("ok") else 1
    except json.JSONDecodeError:
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
