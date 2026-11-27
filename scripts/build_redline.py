#!/usr/bin/env python3
"""Build the failing/fixed candidate pages used by the Redline film."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path("/home/lakshaya/projects/mosaic")
OUT = ROOT / "demo" / "redline"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT))

from mosaic_design import design  # noqa: E402

BRIEF = "A quiet portfolio for a type designer who needs clients to trust the process"


def main() -> int:
    page = design(BRIEF, mode="page")["page"]["files"][0]["content"]
    (OUT / "fixed.html").write_text(page, encoding="utf-8")
    # A candidate, not a fake: this is the real page with a failing token and a
    # too-small range target. The visual gate is expected to catch both.
    fail = page.replace("--signal: #be402d;", "--signal: #d89a84;")
    fail = fail.replace(
        "</style>",
        "\n.specimen-controls input{height:16px}\n</style>",
    )
    (OUT / "fail.html").write_text(fail, encoding="utf-8")
    print(json.dumps({"ok": True, "fixed": str(OUT / "fixed.html"), "fail": str(OUT / "fail.html")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())