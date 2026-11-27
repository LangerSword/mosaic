"""Mosaic Taste: deterministic proxies for design taste, with honest confidence.

This is not a universal taste oracle. It measures craft, specificity, restraint,
hierarchy, rhythm, tension, fit and originality proxies from source, then says
how much to trust them. A real taste model needs blind pairwise votes; the
output names that requirement instead of inventing a perfect score.
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    from .mosaic_audit import TEXT_SUFFIXES
except ImportError:  # standalone CLI / tests
    from mosaic_audit import TEXT_SUFFIXES

MAX_CHARS = 300_000
GENERIC = re.compile(r"\b(seamless|unlock|empower|revolutionary|next[ -]generation|world[ -]class|cutting[ -]edge|game[ -]changing|effortless|supercharge)\b", re.I)
STOP = {"the", "and", "for", "with", "that", "this", "from", "into", "your", "our", "who", "what", "when", "where", "are", "is", "of", "to", "a", "an"}


def _clamp(value: float) -> float:
    return round(max(0.0, min(10.0, value)), 1)


def _path_source(path: str) -> tuple[str | None, str]:
    p = Path(path).expanduser().resolve()
    if p.is_dir():
        p = p / "index.html"
    if not p.is_file():
        return None, f"not a file: {p}"
    if p.suffix.lower() not in TEXT_SUFFIXES:
        return None, f"unsupported text suffix: {p.suffix or '<none>'}"
    try:
        source = p.read_text(encoding="utf-8", errors="replace")[:MAX_CHARS]
        if p.suffix.lower() in {".html", ".htm"}:
            for href in re.findall(r'<link\b[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)', source, re.I):
                if href.startswith(("http://", "https://", "data:", "#")):
                    continue
                css = (p.parent / href.split("?")[0]).resolve()
                if css.is_file():
                    source += "\n/* linked: " + href + " */\n" + css.read_text(encoding="utf-8", errors="replace")
        return source[:MAX_CHARS], str(p)
    except OSError as exc:
        return None, f"read failed: {exc}"


def _fonts(source: str) -> list[float]:
    values = []
    declarations = re.findall(r"(?:font-size|--(?:display|body|mono|specimen-size))\s*:\s*([^;}]+)", source, re.I)
    for raw in declarations:
        for size, unit in re.findall(r"([\d.]+)(px|rem|em)", raw, re.I):
            n = float(size)
            values.append(n * 16 if unit.lower() in {"rem", "em"} else n)
    return [v for v in values if v > 0]


def _spacing(source: str) -> list[float]:
    values = []
    for raw in re.findall(r"(?:gap|margin(?:-[a-z]+)?|padding(?:-[a-z]+)?)\s*:\s*([^;}]+)", source, re.I):
        for number in re.findall(r"(-?[\d.]+)(px|rem|em)?", raw):
            n = float(number[0])
            if number[1].lower() in {"rem", "em"}:
                n *= 16
            if n > 0:
                values.append(n)
    return values


def _families(source: str) -> set[str]:
    return {re.sub(r"\s+", " ", v).strip().lower() for v in re.findall(r"font-family\s*:\s*([^;}]+)", source, re.I)}


def _colors(source: str) -> set[str]:
    found = set(re.findall(r"#[0-9a-fA-F]{3,8}\b", source))
    found |= {f"rgb({m})" for m in re.findall(r"rgba?\(([^)]+)\)", source, re.I)}
    return found


def _brief_overlap(source: str, brief: str) -> float:
    words = {w for w in re.findall(r"[a-z][a-z-]{3,}", brief.lower()) if w not in STOP}
    if not words:
        return 0.0
    text = source.lower()
    hits = sum(1 for word in words if word in text)
    return hits / len(words)


def taste_source(source: str, brief: str = "", label: str = "<source>") -> dict:
    source = source[:MAX_CHARS]
    sizes = _fonts(source)
    spacing = _spacing(source)
    families = _families(source)
    colors = _colors(source)
    h1 = len(re.findall(r"<h1\b", source, re.I))
    headings = len(re.findall(r"<h[1-6]\b", source, re.I))
    slots = source.count("data-slot")
    custom = len(re.findall(r"<mosaic-[a-z-]+|<[a-z]+-(?:field|stack|card|panel)", source, re.I))
    artifact = len(re.findall(r"specimen|trace|signal|programme|excerpt|artifact|provenance", source, re.I))
    generic = bool(GENERIC.search(source))
    radii = len(set(re.findall(r"border-radius\s*:\s*([^;}]+)", source, re.I)))
    shadows = len(re.findall(r"box-shadow\s*:", source, re.I))
    gradients = len(re.findall(r"(?:linear|radial|conic)-gradient\(", source, re.I))
    absolutes = len(re.findall(r"position\s*:\s*absolute", source, re.I))
    grids = len(re.findall(r"grid-template-columns\s*:\s*([^;}]+)", source, re.I))
    max_width = bool(re.search(r"max-width\s*:\s*(?:var\(--measure\)|[\d.]+ch)", source, re.I))
    line_height = bool(re.search(r"line-height\s*:\s*[\d.]+", source, re.I))
    focus = "focus-visible" in source
    reduced = "prefers-reduced-motion" in source
    alt = len(re.findall(r"<img\b[^>]*\balt=", source, re.I))
    imgs = len(re.findall(r"<img\b", source, re.I))
    aria = len(re.findall(r"aria-[a-z]+=", source, re.I))
    semantic = len(re.findall(r"<(?:main|nav|header|footer|section|article)\b", source, re.I))

    ratio = (max(sizes) / min(sizes)) if len(sizes) > 1 else 1.0
    rhythm_ratio = (sum(1 for v in spacing if round(v) % 4 == 0) / len(spacing)) if spacing else 0.0
    display_ratio = ratio if ratio <= 20 else 20
    overlap = _brief_overlap(source, brief) if brief else 0.0

    hierarchy = _clamp(4 + (2 if h1 else 0) + min(4, max(0, 6 - abs(ratio - 5.5))))
    rhythm = _clamp(4 + 6 * rhythm_ratio if spacing else 3.5)
    craft = _clamp(3 + (1 if focus else 0) + (1 if reduced else 0) + (1 if line_height else 0)
                   + (1 if max_width else 0) + (1 if h1 else 0) + (1 if alt or not imgs else 0)
                   + (1 if aria else 0) + (1 if semantic else 0))
    restraint = _clamp(
        9
        - min(4.0, max(0, len(colors) - 10) * .15)
        - min(2.0, max(0, len(families) - 4) * .5)
        - min(2.0, max(0, radii - 6) * .25)
        - min(2.0, shadows * .15 + gradients * .3)
    )
    specificity = _clamp(4 + min(3, slots * .4) + min(2, custom) + min(2, artifact)
                         - (2 if generic else 0))
    tension = _clamp(4 + min(4, max(0, display_ratio - 3) * .8) + min(2, absolutes * .3))
    fit = _clamp(4 + overlap * 6 if brief else 5)
    originality = _clamp(4 + min(2, custom) + min(2, artifact) + (1 if slots else 0)
                         + (1 if len(families) <= 2 else 0) - (2 if generic else 0))
    dimensions = {
        "hierarchy": hierarchy,
        "rhythm": rhythm,
        "craft": craft,
        "restraint": restraint,
        "specificity": specificity,
        "tension": tension,
        "fit": fit,
        "originality": originality,
    }
    weights = {"hierarchy": .18, "rhythm": .13, "craft": .16, "restraint": .14,
               "specificity": .14, "tension": .10, "fit": .08, "originality": .07}
    overall = round(sum(dimensions[k] * weights[k] for k in weights), 1)
    confidence = "low"
    if brief and (slots or custom or artifact) and len(source) > 1500:
        confidence = "medium"
    evidence = [
        f"type scale ratio {ratio:.1f}; {len(sizes)} size declarations; h1={bool(h1)}",
        f"{len(spacing)} spacing values; {rhythm_ratio:.0%} on a 4px unit" if spacing else "no spacing declarations",
        f"{len(colors)} colour values; {len(families)} font families; {radii} radius values",
        f"{slots} content slots; {custom} custom elements; {artifact} artifact references",
        f"focus-visible={focus}; reduced-motion={reduced}; max-width measure={max_width}",
    ]
    return {
        "ok": True,
        "label": label,
        "brief": brief[:2000],
        "taste_index": overall,
        "confidence": confidence,
        "dimensions": dimensions,
        "evidence": evidence,
        "generic_copy": generic,
        "calibration": {
            "status": "unpaired",
            "needed": ["blind pairwise votes", "held-out pairs", "judge agreement"],
            "method": "P(A > B) = sigmoid(w · (features(A) - features(B)))",
            "note": "This profile measures proxies. It is not a universal taste verdict.",
        },
        "next_moves": [
            "Ask two people to choose between this page and a controlled variant without labels.",
            "Change one dimension only (type pairing, spacing, density or accent) and re-run.",
            "If the profile does not move in the expected direction, treat that dimension as noise.",
        ],
    }


def taste_path(path: str, brief: str = "") -> dict:
    source, label = _path_source(path)
    if source is None:
        return {"ok": False, "error": label}
    return taste_source(source, brief, label)