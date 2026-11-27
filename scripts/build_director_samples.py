#!/usr/bin/env python3
"""Build the static design-director samples used by the showcase.

The data comes from the real Mosaic handlers, not a mocked carousel. Keep the
three briefs narrow enough that their concepts are different; the point is the
decision, not three colour swaps.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mosaic_tools import h_critique, h_design, h_score

OUT = Path(__file__).resolve().parents[1] / "site" / "director-samples.js"

CASES = [
    {
        "id": "type-practice",
        "label": "A type practice",
        "brief": "A quiet portfolio for a type designer who needs clients to trust the process",
        "audience": "independent studio founders",
        "constraints": "accessible, no hover-only actions, mobile-first, no invented metrics",
        "mood": "editorial",
        "references": [
            {
                "name": "DIA",
                "observations": {
                    "layout": "index and specimen split",
                    "type": "serif display, mono labels",
                    "motion": "small reveals, no scroll hijack",
                    "what_works": "the index is the navigation",
                    "avoid": "copied case-study cards",
                },
            }
        ],
    },
    {
        "id": "agent-run",
        "label": "An agent at work",
        "brief": "An agent that streams its work while it reads a repository",
        "audience": "developers and technical teams",
        "constraints": "keyboard-first, no fake telemetry, low bandwidth",
        "mood": "technical",
        "references": [
            {
                "name": "Signal Room",
                "observations": {
                    "layout": "one live readout and a source rail",
                    "type": "mono data, a narrow sans",
                    "motion": "state changes, no ambience",
                    "what_works": "the source is visible beside the signal",
                    "avoid": "fake numbers and decorative dashboards",
                },
            }
        ],
    },
    {
        "id": "racing-deck",
        "label": "A racing deck",
        "brief": "A collectible card deck for a racing game",
        "audience": "players and collectors",
        "constraints": "touch and keyboard, no hover-only actions, one dominant card",
        "mood": "tactile",
        "references": [
            {
                "name": "Specimen Table",
                "observations": {
                    "layout": "objects on a wide table with a detail rail",
                    "type": "condensed display, mono metadata",
                    "material": "card edges and contact shadows",
                    "what_works": "the object, not the frame, carries the hierarchy",
                    "avoid": "ten identical rounded cards",
                },
            }
        ],
    },
]


def main() -> None:
    samples = []
    for case in CASES:
        out = json.loads(h_design({
            "brief": case["brief"],
            "audience": case["audience"],
            "constraints": case["constraints"],
            "mood": case["mood"],
            "references": case["references"],
            "mode": "page",
        }))
        page = out["page"]["files"][0]["content"]
        critique = json.loads(h_critique({"source": page, "brief": case["brief"]}))
        awwwards = json.loads(h_score({"source": page, "brief": case["brief"], "references": out["reference_map"]}))
        samples.append({
            "id": case["id"],
            "label": case["label"],
            "brief": case["brief"],
            "audience": out["audience"],
            "domain": out["domain"],
            "action": out["action"],
            "chosen": out["chosen"],
            "concepts": out["concepts"],
            "system": out["system"],
            "copy": out["analysis"]["copy"],
            "content_contract": out["content_contract"],
            "reference_map": out["reference_map"],
            "page": page,
            "critique": {
                "score": critique["score"],
                "verdict": critique["verdict"],
                "strengths": critique["strengths"],
                "findings": critique["findings"],
            },
            "awwwards": {
                "overall": awwwards["overall"],
                "verdict": awwwards["verdict"],
                "scores": awwwards["scores"],
                "blockers": awwwards["blockers"],
            },
        })
    OUT.write_text(
        "window.MOSAIC_DIRECTOR = " + json.dumps(samples, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {len(samples)} samples)")


if __name__ == "__main__":
    main()