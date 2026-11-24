"""Deterministic, local audit for generic and inaccessible design patterns.

This is a heuristic text scan, not a browser test and not a security review.
It reads one local text file or a caller-supplied source string. It never
executes the source, fetches a URL, or writes anything.
"""

from __future__ import annotations

import re
from pathlib import Path

MAX_CHARS = 300_000
TEXT_SUFFIXES = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx",
                 ".ts", ".tsx", ".vue", ".svelte", ".astro", ".md", ".txt"}


def _rule(rule: str, pattern: str, note: str, fix: str, *, threshold: int = 1) -> dict:
    return {"rule": rule, "pattern": re.compile(pattern, re.I | re.M), "note": note,
            "fix": fix, "threshold": threshold}


RULES = [
    _rule("transition-all", r"\btransition\s*:\s*all\b",
          "Animating every property hides layout thrash and makes interaction unpredictable.",
          "Name the properties: transform, opacity, color, box-shadow."),
    _rule("generic-inter", r"font-family\s*:[^;{}]*\bInter\b",
          "Inter on every surface is a default, not a point of view.",
          "Pick a display face and a body face by contrast; keep a utility face separate."),
    _rule("purple-gradient", r"(#667eea|#764ba2|#8b5cf6|#7c3aed|#3b82f6|#6366f1)",
          "A purple-to-blue gradient is the most common generic AI-page signal.",
          "Replace it with one accent and a type or material idea that belongs to the brief."),
    _rule("glass-overload", r"backdrop-filter\s*:\s*[^;{}]*blur",
          "Glass is being used more than once; it will fight text and frame rate.",
          "Use one material and a solid fallback; never put blur behind body copy."),
    _rule("pill-overload", r"border-radius\s*:\s*(9999|999)px",
          "Pills are carrying too many unrelated elements.",
          "Reserve full pills for one control family; use a smaller radius elsewhere."),
    _rule("spinner-only", r"(animate-spin|spinner|loading\.\.\.)",
          "A spinner with no named work is the least informative loading state.",
          "Use a named step list, honest progress, and a slow/error state."),
    _rule("outline-none", r"outline\s*:\s*none",
          "Removing the focus outline without a replacement blocks keyboard users.",
          "Keep :focus-visible with a clear ring; remove outlines only with a replacement."),
    _rule("important-spam", r"!important",
          "Repeated !important usually means the cascade is fighting the design system.",
          "Fix the specificity at the token/component boundary; keep exceptions rare.",
          threshold=6),
]


def _count(source: str, pattern: re.Pattern) -> list[int]:
    return [i for i, line in enumerate(source.splitlines(), 1) if pattern.search(line)]


def audit_source(source: str, label: str = "<source>") -> dict:
    """Scan a string. Returns findings with line numbers and a 0-100 score."""
    if len(source) > MAX_CHARS:
        return {"ok": False, "error": f"source is larger than {MAX_CHARS} characters", "label": label}
    findings = []
    lines = source.splitlines()
    for rule in RULES:
        hits = _count(source, rule["pattern"])
        if len(hits) < rule["threshold"]:
            continue
        findings.append({
            "rule": rule["rule"],
            "line": hits[0],
            "count": len(hits),
            "note": rule["note"],
            "fix": rule["fix"],
            "sample": lines[hits[0] - 1].strip()[:180] if hits and hits[0] <= len(lines) else "",
        })

    has_motion = bool(re.search(r"\b(animation|transition)\s*:", source, re.I))
    has_reduce = "prefers-reduced-motion" in source
    if has_motion and not has_reduce:
        findings.append({
            "rule": "no-reduced-motion",
            "line": 1,
            "count": 1,
            "note": "Motion exists, but there is no reduced-motion path.",
            "fix": "Add a @media (prefers-reduced-motion: reduce) block or a matchMedia guard.",
            "sample": "",
        })

    score = max(0, 100 - 9 * len(findings))
    return {
        "ok": True,
        "label": label,
        "chars": len(source),
        "findings": findings,
        "finding_count": len(findings),
        "score": score,
        "note": "Heuristic text scan. It does not replace browser, keyboard, contrast or performance tests.",
    }


def audit_path(path: str) -> dict:
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        return {"ok": False, "error": f"not a file: {p}"}
    if p.suffix.lower() not in TEXT_SUFFIXES:
        return {"ok": False, "error": f"unsupported text suffix: {p.suffix or '<none>'}"}
    try:
        source = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return {"ok": False, "error": f"read failed: {exc}"}
    return audit_source(source, label=str(p))
