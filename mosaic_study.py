"""Mosaic Study: turn reference observations into transferable design principles.

This module does not fetch a URL, read a screenshot or invent what a reference
looks like. A URL alone produces a capture checklist. The useful output starts
when the caller supplies observations: layout, type, colour, material, motion,
content and what actually works.
"""
from __future__ import annotations

from typing import Any

OBSERVATION_FIELDS = (
    "layout", "type", "color", "material", "motion", "content", "what_works", "avoid",
)

CAPTURE_CHECKLIST = [
    "Capture the first screen at 1440x900 and 390x844.",
    "Record the layout relationship (split, vertical sequence, table, index, canvas), not the decoration.",
    "Record the display/body/utility type roles and the actual measure.",
    "Sample the palette by role: field, ink, muted, line, accent, deep.",
    "Describe the material: paper, steel, glass, ink, halftone, none.",
    "Describe the motion: what triggers it, what changes, what stays still, and the reduced-motion behaviour.",
    "Write the one thing that works and the one thing you refuse to copy.",
]


def _text(value: Any, limit: int = 1200) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        value = str(value)
    if not isinstance(value, str):
        return ""
    return value.strip()[:limit]


def _items(value: Any, limit: int = 12) -> list[str]:
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    return [item for item in (_text(v, 320) for v in value[:limit]) if item]


def normalize_reference(raw: Any, index: int = 0) -> dict:
    if isinstance(raw, str):
        raw_text = raw.strip()
        raw = {"url": raw_text} if raw_text.startswith(("http://", "https://")) else {"name": raw_text}
    if not isinstance(raw, dict):
        raw = {}
    name = _text(raw.get("name") or raw.get("title"), 160) or f"reference {index + 1}"
    url = _text(raw.get("url"), 500)
    obs_raw = raw.get("observations")
    observations = obs_raw if isinstance(obs_raw, dict) else {}
    observations = {
        key: _text(observations.get(key), 900)
        for key in OBSERVATION_FIELDS
        if observations.get(key) is not None
    }
    for key in ("what_works", "avoid"):
        if raw.get(key) is not None:
            observations.setdefault(key, " / ".join(_items(raw.get(key))) if isinstance(raw.get(key), list) else _text(raw.get(key)))
    return {
        "name": name,
        "url": url,
        "observations": {
            key: value for key, value in observations.items() if value
        },
        "keep": _items(raw.get("keep") or raw.get("borrow"), 8),
        "avoid": _items(raw.get("avoid") or raw.get("do_not_copy"), 8),
    }


def study_reference(reference: Any, brief: str = "", constraints: str = "") -> dict:
    """Return an evidence-bounded reference map.

    The study separates what was observed from what may be transferred. A
    reference with no observations is not analysed; it is returned with a
    capture checklist and low confidence.
    """
    ref = normalize_reference(reference)
    observations = ref["observations"]
    has_observations = bool(observations)
    has_intent = bool(ref["keep"] or observations.get("what_works") or observations.get("avoid") or ref["avoid"])

    if not has_observations and not has_intent:
        return {
            "ok": True,
            "status": "needs_observations",
            "confidence": "low",
            "reference": ref,
            "capture_checklist": CAPTURE_CHECKLIST,
            "note": "A URL or name alone is a lead, not a reference study. The tool will not invent the visual facts.",
        }

    principles = []
    for key in ("layout", "type", "color", "material", "motion", "content"):
        observed = observations.get(key)
        if observed:
            principles.append({
                "kind": key,
                "status": "observed",
                "observation": observed,
                "transfer": f"Keep the relational idea in {key}; change the subject, scale and visual language for the brief.",
            })
    for phrase in _items(observations.get("what_works")) + ref["keep"]:
        principles.append({
            "kind": "principle",
            "status": "stated",
            "observation": phrase,
            "transfer": "Translate this principle through the brief's own content and interaction; do not reuse the surface.",
        })

    avoid = _items(observations.get("avoid")) + ref["avoid"]
    confidence = "high" if ref["keep"] or observations.get("what_works") else "medium"
    if constraints and "no copy" in constraints.lower():
        confidence = "high" if confidence == "high" else "medium"
    return {
        "ok": True,
        "status": "studied",
        "confidence": confidence,
        "reference": ref,
        "principles": principles,
        "transferable": [p for p in principles if p["status"] in {"stated", "observed"}][:6],
        "not_transferable": list(dict.fromkeys([
            "exact layout, code or component structure",
            "brand marks, photography, copy and proprietary assets",
            "a surface palette or typography treated as an identity",
        ] + avoid)),
        "originality_contract": [
            "Borrow at most one principle per reference.",
            "Change the artifact and the content relationship, not just the colours.",
            "Name the new move in one sentence before writing code.",
            "Keep the reference URL in the provenance note; do not ship its assets.",
        ],
        "brief": _text(brief, 2000),
        "constraints": _text(constraints, 800),
    }