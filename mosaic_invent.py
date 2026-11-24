"""Mosaic Invent: generate interaction candidates and score them with a rubric.

The output is a hypothesis, not a finished design. The generator combines a
small typed grammar; the scorer applies hard accessibility/state gates and a
transparent taste rubric. Human or browser evidence still decides what ships.
"""
from __future__ import annotations

import hashlib
import json
import random

from mosaic_forge import KINDS

OBJECTS = ["card", "field", "rail", "token", "ring", "stack", "ledger", "lens"]
INPUTS = ["hold", "swipe", "drag", "tap", "hover", "scroll", "key"]
PHYSICS = ["pour", "spring", "fold", "orbit", "settle", "breathe", "cascade"]
FEEDBACKS = ["check", "ring", "trail", "label", "tick", "ripple", "dissolve"]
METAPHORS = ["paper", "tide", "loom", "compass", "archive", "signal", "weather", "workshop"]
FIRST = ["Quiet", "Paper", "Tide", "Signal", "Loom", "Compass", "Field", "Soft", "Open", "After"]
SECOND = ["Gate", "Turn", "Fold", "Ledger", "Drift", "Pulse", "Thread", "Mark", "Pass", "Choir"]

PHYSICS_FOR = {
    "hold": ["pour", "settle", "breathe"],
    "swipe": ["spring", "settle", "trail"],
    "drag": ["spring", "orbit", "settle"],
    "tap": ["spring", "fold", "pour"],
    "hover": ["breathe", "orbit", "settle"],
    "scroll": ["cascade", "breathe", "orbit"],
    "key": ["settle", "fold", "spring"],
}

KNOWN = {
    ("hold", "pour", "check"), ("swipe", "spring", "check"),
    ("hover", "settle", "tick"), ("scroll", "cascade", "label"),
    ("tap", "spring", "tick"), ("drag", "spring", "check"),
}

RUBRIC = {
    "coherence": "Does the input cause the physics and feedback, or is it decoration?",
    "legibility": "Can the state be understood without motion, and without hover?",
    "novelty": "Is this a new state transition, not a renamed known component?",
    "restraint": "One object, one input, one feedback. Does it avoid stacking tricks?",
    "fit": "Does it belong to this brief and its audience?",
}


def _seed_for(brief: str, seed: int | None) -> int:
    if seed is not None:
        return int(seed)
    return int(hashlib.sha256(brief.encode()).hexdigest()[:8], 16)


def _has(brief: str, *words: str) -> int:
    low = brief.lower()
    return sum(1 for word in words if word in low)


def _state_machine(input_name: str) -> list[dict]:
    if input_name in {"hold", "swipe", "drag"}:
        return [
            {"state": "idle", "event": "press or grab", "result": "surface responds"},
            {"state": "contact", "event": "hold or drag", "result": "progress is visible and cancellable"},
            {"state": "armed", "event": "threshold", "result": "label states the consequence"},
            {"state": "resolved", "event": "release", "result": "check or explicit result"},
            {"state": "reset", "event": "acknowledge", "result": "surface returns without a ghost action"},
        ]
    if input_name == "scroll":
        return [
            {"state": "rest", "event": "enter viewport", "result": "one reveal, no hidden content"},
            {"state": "progress", "event": "scroll", "result": "rail matches position"},
            {"state": "settled", "event": "leave", "result": "content remains readable"},
        ]
    if input_name == "hover":
        return [
            {"state": "rest", "event": "pointer or focus", "result": "preview is a bonus"},
            {"state": "preview", "event": "enter", "result": "same information is available on focus"},
            {"state": "leave", "event": "leave or blur", "result": "no layout shift"},
        ]
    return [
        {"state": "idle", "event": "press or key", "result": "contact is visible"},
        {"state": "active", "event": "release", "result": "one action, with a result"},
        {"state": "reset", "event": "result acknowledged", "result": "surface returns"},
    ]


def _forge_kind(input_name: str, feedback: str) -> str:
    if input_name in {"hold", "swipe", "drag"}:
        return "hold" if input_name == "hold" else "swipe-confirm"
    if input_name == "tap":
        return "paper-plane"
    if input_name == "scroll":
        return "thinking"
    if input_name == "hover":
        return "checklist" if feedback in {"check", "tick"} else "thinking"
    return "segmented"


def _score(candidate: dict, brief: str, constraints: str) -> dict:
    known = (candidate["input"], candidate["physics"], candidate["feedback"]) in KNOWN
    hover_only = candidate["input"] == "hover" and "no hover" not in constraints.lower()
    irreversible = candidate["input"] in {"hold", "swipe", "drag"}
    keywords = _has(brief, "quiet", "calm", "editorial", "music", "archive", "bank", "design", "onboarding", "live", "agent")
    fit = min(10, 5 + keywords)
    coherence = 9 if candidate["physics"] in PHYSICS_FOR[candidate["input"]] else 5
    legibility = 8
    if hover_only:
        legibility -= 2
    if candidate["feedback"] in {"trail", "dissolve", "ripple"}:
        legibility -= 1
    novelty = 4 if known else 8
    if candidate["metaphor"] in {"weather", "signal"}:
        novelty += 1
    restraint = 9
    if candidate["input"] == "scroll" and candidate["physics"] == "orbit":
        restraint -= 2
    if candidate["feedback"] == candidate["physics"]:
        restraint -= 1
    taste = {
        "coherence": max(0, min(10, coherence)),
        "legibility": max(0, min(10, legibility)),
        "novelty": max(0, min(10, novelty)),
        "restraint": max(0, min(10, restraint)),
        "fit": max(0, min(10, fit)),
    }
    overall = round(
        taste["coherence"] * 0.30
        + taste["legibility"] * 0.25
        + taste["novelty"] * 0.20
        + taste["restraint"] * 0.15
        + taste["fit"] * 0.10,
        1,
    )
    gates = ["mouse, keyboard and focus reach the same state", "prefers-reduced-motion keeps the result"]
    if irreversible:
        gates.append("cancel is explicit and releases the action")
    if hover_only:
        gates.append("hover is a preview, not the only path")
    return {"scores": taste, "overall": overall, "known": known, "gates": gates}


def invent(brief: str, constraints: str = "", count: int = 3, seed: int | None = None) -> str:
    brief = (brief or "").strip()
    if len(brief) < 8:
        raise ValueError("brief must be at least 8 characters")
    if count < 1 or count > 5:
        raise ValueError("count must be between 1 and 5")
    constraints = (constraints or "").strip()
    rng = random.Random(_seed_for(brief, seed))
    candidates = []
    seen = set()
    attempts = 0
    while len(candidates) < count * 8 and attempts < 300:
        attempts += 1
        input_name = rng.choice(INPUTS)
        if "no hover" in constraints.lower() and input_name == "hover":
            continue
        physics = rng.choice(PHYSICS_FOR[input_name])
        feedback = rng.choice(FEEDBACKS)
        object_name = rng.choice(OBJECTS)
        metaphor = rng.choice(METAPHORS)
        key = (object_name, input_name, physics, feedback, metaphor)
        if key in seen:
            continue
        seen.add(key)
        candidate = {
            "id": f"{object_name}-{input_name}-{physics}-{feedback}-{len(candidates)}",
            "name": f"{rng.choice(FIRST)} {rng.choice(SECOND)}",
            "thesis": f"A {metaphor} {object_name} that answers a {input_name} with {physics}, then makes the result visible with {feedback}.",
            "object": object_name,
            "input": input_name,
            "physics": physics,
            "feedback": feedback,
            "metaphor": metaphor,
            "state_machine": _state_machine(input_name),
            "forge_kind": _forge_kind(input_name, feedback),
            "why": f"The {input_name} is the cause; {physics} is the physical response; {feedback} is the honest result.",
            "risk": "The metaphor may overpower the action; keep one object and one transition.",
        }
        candidate.update(_score(candidate, brief, constraints))
        candidates.append(candidate)
    candidates.sort(key=lambda c: (-c["overall"], c["id"]))
    # Keep the top candidates but avoid three versions of the same input.
    chosen = []
    used_inputs = set()
    for candidate in candidates:
        if candidate["input"] in used_inputs and len(chosen) < count:
            continue
        chosen.append(candidate)
        used_inputs.add(candidate["input"])
        if len(chosen) == count:
            break
    if len(chosen) < count:
        for candidate in candidates:
            if candidate not in chosen:
                chosen.append(candidate)
            if len(chosen) == count:
                break
    return json.dumps({
        "ok": True,
        "brief": brief,
        "constraints": constraints,
        "seed": _seed_for(brief, seed),
        "rubric": RUBRIC,
        "candidates": chosen,
        "note": "Scores are a transparent heuristic, not a substitute for a rendered browser test or a human verdict.",
    }, ensure_ascii=False, indent=2)


TOOL_SPECS = [
    {
        "name": "mosaic_invent",
        "handler": None,
        "emoji": "💡",
        "description": "Invent interaction candidates from a brief using a typed grammar and a transparent taste rubric.",
        "schema": {
            "type": "object",
            "properties": {
                "brief": {"type": "string"},
                "constraints": {"type": "string"},
                "count": {"type": "integer", "minimum": 1, "maximum": 5},
                "seed": {"type": "integer"},
            },
            "required": ["brief"],
        },
    },
]
