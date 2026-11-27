"""Mosaic Score: a transparent pre-awards gate for a built page.

The score is built from text evidence: token discipline, hierarchy, focus,
reduced motion, content-slot contract, originality cues and generic-copy
failures. It is not a visual verdict and never replaces a browser pass.
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    from .mosaic_critique import critique_source
    from .mosaic_audit import TEXT_SUFFIXES
except ImportError:  # standalone CLI / tests
    from mosaic_critique import critique_source
    from mosaic_audit import TEXT_SUFFIXES

MAX_CHARS = 300_000
GENERIC = re.compile(r"\b(seamless|unlock|empower|revolutionary|next[ -]generation|world[ -]class|cutting[ -]edge|game[ -]changing|effortless|supercharge)\b", re.I)


def _path_source(path: str) -> tuple[str | None, str]:
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        return None, f"not a file: {p}"
    if p.suffix.lower() not in TEXT_SUFFIXES:
        return None, f"unsupported text suffix: {p.suffix or '<none>'}"
    try:
        return p.read_text(encoding="utf-8", errors="replace")[:MAX_CHARS], str(p)
    except OSError as exc:
        return None, f"read failed: {exc}"


def _clamp(value: float) -> float:
    return round(max(0, min(10, value)), 1)


def score_source(source: str, brief: str = "", references: list | None = None, label: str = "<source>") -> dict:
    source = source[:MAX_CHARS]
    critique = critique_source(source, brief, label)
    findings = critique.get("findings", [])
    rules = {finding["rule"] for finding in findings}
    has_focus = "focus-visible" in source
    has_reduced = "prefers-reduced-motion" in source
    has_slots = "data-slot" in source
    has_artifact = bool(re.search(r"specimen|trace|signal|programme|excerpt|artifact|data-artifact|ascii|glass", source, re.I))
    has_custom = bool(re.search(r"<mosaic-[a-z-]+|<[a-z]+-(?:field|stack|card|panel)", source, re.I))
    has_tokens = bool(re.search(r":root\s*\{[^}]*--", source, re.S))
    has_type_roles = len(set(re.findall(r"font-family\s*:\s*([^;}]+)", source, re.I))) <= 3
    has_heading = bool(re.search(r"<h1\b", source, re.I))
    has_cta = bool(re.search(r'class="[^"]*(?:act|btn|cta)[^"]*"|<button\b', source, re.I))
    has_proof = bool(re.search(r"specimen|proof|evidence|source|provenance", source, re.I))
    prompt_leak = "prompt-leak" in rules
    generic = "generic-copy" in rules or bool(GENERIC.search(source))
    refs = references or []
    studied_refs = [r for r in refs if isinstance(r, dict) and r.get("status") == "studied"]
    confidence = max((r.get("confidence", "low") for r in studied_refs), default="low")
    originality = 4 + (2 if confidence == "medium" else 3 if confidence == "high" else 0)
    originality += 2 if has_artifact else 0
    originality += 1 if has_custom else 0
    originality -= 2 if generic else 0

    design = 4
    design += 2 if has_tokens else 0
    design += 1 if has_type_roles else 0
    design += 1 if has_artifact else 0
    design += 1 if not generic else 0
    design -= 2 if prompt_leak else 0
    design -= 1 if "radius-noise" in rules or "font-noise" in rules else 0

    usability = 5
    usability += 2 if has_focus else 0
    usability += 1 if has_reduced else 0
    usability += 1 if has_heading else 0
    usability += 1 if has_cta else 0
    usability -= 2 if "no-focus-visible" in rules else 0
    usability -= 2 if "no-reduced-motion" in rules else 0
    usability -= 1 if "heading-count" in rules else 0

    creativity = 3
    creativity += 2 if has_artifact else 0
    creativity += 2 if has_custom else 0
    creativity += 2 if has_tokens else 0
    creativity += 1 if studied_refs else 0
    creativity -= 1 if generic else 0
    creativity -= 1 if "glass-overload" in rules else 0

    content = 5
    content += 2 if has_slots else 0
    content += 1 if has_proof else 0
    content += 1 if not prompt_leak else 0
    content += 1 if not generic else 0
    content -= 2 if prompt_leak else 0
    content -= 2 if generic else 0

    scores = {
        "design": _clamp(design),
        "usability": _clamp(usability),
        "creativity": _clamp(creativity),
        "content": _clamp(content),
        "originality": _clamp(originality),
    }
    overall = round(
        scores["design"] * .34 + scores["usability"] * .25 +
        scores["creativity"] * .20 + scores["content"] * .12 +
        scores["originality"] * .09, 1
    )
    blockers = []
    if prompt_leak:
        blockers.append("Headline repeats the brief.")
    if generic:
        blockers.append("Generic product copy is carrying the claim.")
    if "no-focus-visible" in rules:
        blockers.append("No focus-visible path.")
    if "no-reduced-motion" in rules:
        blockers.append("No reduced-motion path.")
    if not has_slots:
        blockers.append("No content-slot contract.")
    if not has_heading:
        blockers.append("No clear h1.")
    if blockers:
        verdict = "reject" if len(blockers) >= 3 or overall < 6 else "revise"
    elif overall >= 8.5:
        verdict = "ship"
    else:
        verdict = "revise"
    return {
        "ok": True,
        "label": label,
        "brief": brief[:2000],
        "scores": scores,
        "overall": overall,
        "verdict": verdict,
        "blockers": blockers,
        "evidence": {
            "tokens": has_tokens,
            "type_roles": has_type_roles,
            "artifact": has_artifact,
            "custom_element": has_custom,
            "focus_visible": has_focus,
            "reduced_motion": has_reduced,
            "content_slots": has_slots,
            "proof_or_provenance": has_proof,
            "reference_studies": len(studied_refs),
            "reference_confidence": confidence,
        },
        "critique": critique,
        "next_moves": [
            "Replace the sample content slots with the brief's real artifacts.",
            "Render at 1440x900 and 390x844; inspect the first screen and one scroll chapter.",
            "Tab through every control and test the reduced-motion path.",
            "Add one authored motion cue, not five hover effects.",
            "Remove any decoration that cannot explain a state or a relationship.",
        ],
        "note": "A text-only pre-awards score. It cannot judge composition, motion feel, imagery or true visual craft. Follow it with mosaic_visual for rendered hard gates.",
    }


def score_path(path: str, brief: str = "", references: list | None = None) -> dict:
    source, label = _path_source(path)
    if source is None:
        return {"ok": False, "error": label}
    return score_source(source, brief, references, label)