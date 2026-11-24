#!/usr/bin/env python3
"""Load the real plugin entry point against a recording context and dispatch tools."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class RecordingContext:
    def __init__(self):
        self.tools = {}
        self.hooks = []

    def register_tool(self, **kwargs):
        self.tools[kwargs["name"]] = kwargs

    def register_hook(self, name, fn):
        self.hooks.append((name, fn))


def load_plugin():
    spec = importlib.util.spec_from_file_location(
        "mosaic_plugin", ROOT / "__init__.py",
        submodule_search_locations=[str(ROOT)],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    ctx = RecordingContext()
    module.register(ctx)
    return module, ctx


def main():
    module, ctx = load_plugin()
    declared = {"mosaic_index", "mosaic_components", "mosaic_recipe", "mosaic_audit"}
    assert set(ctx.tools) == declared, (set(ctx.tools), declared)
    assert not ctx.hooks
    idx = json.loads(ctx.tools["mosaic_index"]["handler"]({}))
    assert idx["ok"] and len(idx["families"]) == 10
    comps = json.loads(ctx.tools["mosaic_components"]["handler"]({"family": "press"}))
    assert comps["ok"] and comps["count"] >= 5
    rec = json.loads(ctx.tools["mosaic_recipe"]["handler"](
        {"brief": "A tactile collectible deck for a racing game", "mood": "tactile"}))
    assert rec["ok"] and rec["signature_moves"]
    audit = json.loads(ctx.tools["mosaic_audit"]["handler"](
        {"source": ".x { transition: all 1s; }"}))
    assert audit["ok"] and audit["finding_count"] >= 1
    print("smoke_load ok:", module.__version__, sorted(ctx.tools), "hooks", len(ctx.hooks))


if __name__ == "__main__":
    main()
