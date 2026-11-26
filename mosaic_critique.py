"""Mosaic Critique: a design-specific text critique.

This is deliberately not a visual QA tool. It reads a local source string and
checks the things that can be known from text: generic copy, heading structure,
token discipline, focus/reduced-motion paths and the content-slot contract.
A browser screenshot and a human eye still decide whether the result is accurate.
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    from .mosaic_audit import TEXT_SUFFIXES, audit_source
except ImportError:  # standalone CLI / tests
    from mosaic_audit import TEXT_SUFFIXES, audit_source

MAX_CHARS = 300_000

GENERIC_COPY = (
    "seamless", "unlock", "empower", "revolutionary", "next-generation", "next generation",
    "world-class", "cutting-edge", "game-changing", "effortless", "we build", "we make",
    "built different", "reimagine", "supercharge",
)

DESIGN_RULES = (
    ("generic-copy", r"\b(seamless|unlock|empower|revolutionary|next[ -]generation|world[ -]class|cutting[ -]edge|game[ -]changing|effortless|supercharge)\b",
     "Generic product copy is doing the work of a specific claim.",
     "Replace it with the product's actual action, object and evidence."),
    ("heading-count", r"<h1\b",
     "More than one h1 makes the page hierarchy ambiguous.",
     "Keep one h1; use h2/h3 for sections.", 2),
    ("no-focus-visible", r"(?!)",
     "No explicit focus-visible treatment was found.",
     "Add a visible focus ring and verify it against the actual ground colour."),
    ("no-slot-contract", r"(?!)",
     "No data-slot contract was found in an HTML source.",
     "Mark editable content slots so the design can be filled with real content without guessing."),
    ("radius-noise", r"border-radius\s*:\s*([^;}]+)",
     "Too many unrelated radius values weaken the material system.",
     "Use one radius token per object family.", 4),
    ("font-noise", r"font-family\s*:\s*([^;}]+)",
     "Too many families are competing for the same voice.",
     "Use one display face, one body face and one utility face.", 4),
)

STRENGTHS = (
    "Has a visible content contract",
    "Has a focus-visible path",
    "Has a reduced-motion path",
    "Uses named colour tokens",
    "Keeps one primary heading",
    "Avoids generic product copy",
)


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


def _unique_count(source: str, pattern: str) -> int:
    values = {match.strip().lower() for match in re.findall(pattern, source, re.I | re.M)}
    return len(values)


def critique_source(source: str, brief: str = "", label: str = "<source>") -> dict:
    source = source[:MAX_CHARS]
    audit = audit_source(source, label=label)
    findings = []
    strengths = []

    def add(rule: str, note: str, fix: str, sample: str = "") -> None:
        findings.append({"rule": rule, "note": note, "fix": fix, "sample": sample[:180]})

    if re.search(r"\b(seamless|unlock|empower|revolutionary|next[ -]generation|world[ -]class|cutting[ -]edge|game[ -]changing|effortless|supercharge)\b", source, re.I):
        add("generic-copy", "Generic product copy is doing the work of a specific claim.",
            "Replace it with the product's actual action, object and evidence.", "")
    else:
        strengths.append("Avoids generic product copy")

    if re.search(r"<h1[^>]*>[^<]*(portfolio for|who needs|that needs|for a [^<]{0,40} who)", source, re.I):
        add("prompt-leak", "The headline repeats the brief instead of addressing a visitor.",
            "Write a client-facing headline; keep the brief in the content contract, not the h1.", "")
    else:
        strengths.append("Headline is not the raw brief")

    if len(re.findall(r"<h1\b", source, re.I)) > 1:
        add("heading-count", "More than one h1 makes the page hierarchy ambiguous.",
            "Keep one h1; use h2/h3 for sections.", "")
    elif source.strip():
        strengths.append("Keeps one primary heading")

    if "focus-visible" not in source and "<button" in source:
        add("no-focus-visible", "Interactive elements have no explicit focus-visible treatment.",
            "Add a visible focus ring and verify it against the actual ground colour.", "")
    elif "focus-visible" in source:
        strengths.append("Has a focus-visible path")

    if "<html" in source and "data-slot" not in source:
        add("no-slot-contract", "The page has no content-slot contract.",
            "Mark editable content slots so the design can be filled with real content without guessing.", "")
    elif "data-slot" in source:
        strengths.append("Has a visible content contract")

    if "prefers-reduced-motion" in source:
        strengths.append("Has a reduced-motion path")
    if "--" in source and re.search(r":root\s*\{", source):
        strengths.append("Uses named colour tokens")

    radius_values = _unique_count(source, r"border-radius\s*:\s*([^;}]+)")
    if radius_values > 3:
        add("radius-noise", f"{radius_values} distinct radius values are in play.",
            "Use one radius token per object family.", f"{radius_values} values")
    font_values = _unique_count(source, r"font-family\s*:\s*([^;}]+)")
    if font_values > 3:
        add("font-noise", f"{font_values} font-family declarations compete.",
            "Use one display face, one body face and one utility face.", f"{font_values} families")

    # Existing generic-pattern audit remains useful; keep its findings separate.
    audit_findings = audit.get("findings", []) if audit.get("ok") else []
    score = max(0, round(100 - 9 * len(audit_findings) - 6 * len(findings)))
    if score >= 90:
        verdict = "pass"
    elif score >= 70:
        verdict = "revise"
    else:
        verdict = "reject"
    return {
        "ok": True,
        "label": label,
        "brief": brief.strip()[:2000],
        "score": score,
        "verdict": verdict,
        "findings": findings,
        "finding_count": len(findings),
        "audit_findings": audit_findings,
        "strengths": list(dict.fromkeys(strengths)),
        "next_actions": [
            "Replace every data-slot with supplied content.",
            "Run a real browser pass at 1440x900 and 390x844.",
            "Check focus, keyboard and reduced-motion paths.",
            "Compare the rendered silhouette against the chosen concept; do not judge from source alone.",
        ],
        "note": "Heuristic text critique only. It cannot prove visual accuracy, contrast or motion quality.",
    }


def critique_path(path: str, brief: str = "") -> dict:
    source, label = _path_source(path)
    if source is None:
        return {"ok": False, "error": label}
    return critique_source(source, brief, label)