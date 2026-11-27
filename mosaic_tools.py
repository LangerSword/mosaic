"""Tool handlers and schemas for Mosaic."""

from __future__ import annotations

import hashlib
import json

try:
    from .mosaic_audit import audit_path, audit_source
    from .mosaic_critique import critique_path, critique_source
    from .mosaic_data import BASE_TOKENS, COMPONENTS, FAMILIES, MOODS
    from .mosaic_design import design
    from .mosaic_forge import KINDS, STACKS, forge
    from .mosaic_invent import invent
    from .mosaic_score import score_path, score_source
    from .mosaic_study import study_reference
    from .mosaic_visual import visual, visual_source
except ImportError:  # standalone CLI / tests
    from mosaic_audit import audit_path, audit_source
    from mosaic_critique import critique_path, critique_source
    from mosaic_data import BASE_TOKENS, COMPONENTS, FAMILIES, MOODS
    from mosaic_design import design
    from mosaic_forge import KINDS, STACKS, forge
    from mosaic_invent import invent
    from mosaic_score import score_path, score_source
    from mosaic_study import study_reference
    from mosaic_visual import visual, visual_source

DIRECTIONS = ["The Quiet Instrument", "Paper Teeth", "Soft Machinery", "The Long Table",
              "Field Notes", "After Hours", "The Slow Signal", "Open Studio"]
COMPONENT_HINTS = {
    "cards": ["face-card", "live-card", "card-arc", "join-group"],
    "type": ["script-over", "beat-wordmark", "quanta"],
    "press": ["hold-to-confirm", "publish-bar", "live-card", "join-group", "story-pills"],
    "drag": ["card-arc", "channel-rail", "story-pills"],
    "hover": ["face-card", "glass-month", "live-cursors"],
    "select": ["flow-canvas", "segmented-control"],
    "loading": ["thinking-shimmer"],
}
KEYWORDS = {
    "cards": ("card", "deck", "collect", "ticket", "wallet", "stack", "fan"),
    "press": ("hold", "confirm", "delete", "pay", "publish", "send", "destructive"),
    "drag": ("drag", "reorder", "sort", "kanban", "move", "timeline", "scrub"),
    "hover": ("hover", "preview", "cursor", "gallery", "row", "magnetic"),
    "select": ("select", "segment", "tab", "filter", "picker", "toggle", "view"),
    "shader": ("shader", "webgl", "noise", "field", "globe", "heat", "atmosphere"),
    "type": ("type", "wordmark", "editorial", "font", "headline", "label", "quote"),
    "scroll": ("scroll", "story", "chapter", "pinned", "timeline", "parallax"),
    "loading": ("agent", "loading", "thinking", "wait", "job", "stream", "status"),
    "ascii": ("ascii", "terminal", "monospace", "night", "field", "text field"),
    "glass": ("glass", "translucent", "lens", "material", "frosted"),
}


def _j(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _text(value, name: str, limit: int = 2000) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    value = value.strip()
    if len(value) > limit:
        raise ValueError(f"{name} must be at most {limit} characters")
    return value


def _optional(value, limit: int = 2000) -> str:
    return value.strip()[:limit] if isinstance(value, str) else ""


def _family(fid: str) -> dict:
    for family in FAMILIES:
        if family["id"] == fid:
            return family
    raise ValueError(f"unknown family: {fid}")


def _pick_families(brief: str, mood: str) -> list[str]:
    low = brief.lower()
    scored = []
    for fid, words in KEYWORDS.items():
        score = sum(1 for word in words if word in low)
        if score:
            scored.append((score, fid))
    scored.sort(key=lambda item: (-item[0], item[1]))
    picks = []
    for _, fid in scored:
        if fid not in picks:
            picks.append(fid)
        if len(picks) == 2:
            break
    if not picks:
        picks = ["paper-ink"]
    if len(picks) == 1:
        complement = "type" if picks[0] != "type" else "select"
        if mood == "tactile":
            complement = "cards"
        if mood == "technical" and picks[0] != "loading":
            complement = "loading"
        if complement == picks[0]:
            complement = "type" if picks[0] != "type" else "select"
        picks.append(complement)
    return picks[:2]


def _accent(mood: str) -> dict:
    return MOODS.get(mood, MOODS["quiet"])


def h_study(args: dict) -> str:
    reference = args.get("reference")
    if not isinstance(reference, (str, dict)):
        raise ValueError("reference must be a string or an object")
    brief = _optional(args.get("brief"), 2400)
    constraints = _optional(args.get("constraints"), 800)
    return _j(study_reference(reference, brief, constraints))


def h_design(args: dict) -> str:
    brief = _text(args.get("brief"), "brief", 2400)
    audience = _optional(args.get("audience"), 200)
    constraints = _optional(args.get("constraints"), 900)
    mood = str(args.get("mood") or "").strip().lower()
    stack = _text(args.get("stack") or "HTML/CSS/JS", "stack", 200)
    mode = str(args.get("mode") or "direction").strip().lower()
    references = args.get("references") or []
    if isinstance(references, (str, dict)):
        references = [references]
    if not isinstance(references, list) or len(references) > 6:
        raise ValueError("references must be an array of at most 6 strings or objects")
    seed = args.get("seed")
    if seed is not None:
        seed = int(seed)
    return _j(design(brief, audience, constraints, references, mood, stack, mode, seed))


def h_critique(args: dict) -> str:
    source = args.get("source")
    path = args.get("path")
    if bool(source) == bool(path):
        raise ValueError("pass exactly one of source or path")
    brief = _optional(args.get("brief"), 2000)
    if path:
        return _j(critique_path(_text(path, "path", 1000), brief))
    return _j(critique_source(_text(source, "source", 300_000), brief))


def h_index(args: dict) -> str:
    return _j({
        "ok": True,
        "plugin": "mosaic",
        "version": "0.8.1",
        "families": [
            {"id": f["id"], "name": f["name"], "skill": f["skill"],
             "signature": f["signature"], "use_when": f["use_when"], "avoid": f["avoid"]}
            for f in FAMILIES
        ],
        "methods": [
            {"id": "study", "skill": "mosaic-study", "tool": "mosaic_study",
             "purpose": "Turn observed references into principles without inventing visual facts."},
            {"id": "design", "skill": "mosaic-design", "tool": "mosaic_design",
             "purpose": "Read the brief, propose three concepts, choose one and define the system and page."},
            {"id": "critique", "skill": "mosaic-critique", "tool": "mosaic_critique",
             "purpose": "Critique the source against design specificity, copy, focus and content-slot discipline."},
            {"id": "score", "skill": "mosaic-score", "tool": "mosaic_score",
             "purpose": "Run a transparent pre-awards score across design, usability, creativity, content and originality."},
            {"id": "visual", "skill": "mosaic-visual", "tool": "mosaic_visual",
             "purpose": "Render the built page in Chromium and pass or fail hard visual gates with screenshot evidence."},
        ],
        "base_tokens": BASE_TOKENS,
        "moods": sorted(MOODS),
        "note": "Families are moves, not templates. Study the brief and references before writing code.",
    })


def h_score(args: dict) -> str:
    source = args.get("source")
    path = args.get("path")
    if bool(source) == bool(path):
        raise ValueError("pass exactly one of source or path")
    brief = _optional(args.get("brief"), 2000)
    references = args.get("references") or []
    if isinstance(references, (str, dict)):
        references = [references]
    if not isinstance(references, list) or len(references) > 6:
        raise ValueError("references must be an array of at most 6 objects")
    if path:
        return _j(score_path(_text(path, "path", 1000), brief, references))
    return _j(score_source(_text(source, "source", 300_000), brief, references))


def h_visual(args: dict) -> str:
    target = args.get("target") or args.get("url") or args.get("path")
    source = args.get("source")
    if bool(target) == bool(source):
        raise ValueError("pass exactly one of target or source")
    if source:
        return _j(visual_source(_text(source, "source", 300_000)))
    return _j(visual(_text(target, "target", 1000)))


def h_recipe(args: dict) -> str:
    brief = _text(args.get("brief"), "brief", 2000)
    mood = str(args.get("mood") or "quiet").lower()
    if mood not in MOODS:
        raise ValueError(f"mood must be one of: {', '.join(sorted(MOODS))}")
    stack = str(args.get("stack") or "HTML/CSS/JS").strip()[:200]
    constraints = str(args.get("constraints") or "").strip()[:500]
    picks = _pick_families(brief, mood)
    base = _family(picks[0]) if picks[0] == "paper-ink" else _family("paper-ink")
    accent = _accent(mood)
    direction = DIRECTIONS[int(hashlib.sha256(brief.encode()).hexdigest(), 16) % len(DIRECTIONS)]
    signature = [_family(fid) for fid in picks]
    avoid = []
    for family in signature:
        avoid.append(family["avoid"])
    avoid.extend(["purple-blue gradient as the identity", "glass on every surface",
                  "fake progress or spinner-only loading", "ten identical rounded cards"])
    checks = ["One loud line and one quiet paragraph", "Body measure 45-75ch",
              "Visible focus and 4.5:1 body contrast", "Reduced-motion path",
              "No copied assets or reference code"]
    for family in signature:
        checks.extend(family["check"])
    tokens = {
        "--paper": accent["field"],
        "--ink": accent["ink"],
        "--muted": "#6b6a66" if mood != "technical" else "#a3a3a3",
        "--line": "#e7e3d8" if mood != "technical" else "#2a2a2a",
        "--accent": accent["accent"],
        "--accent-deep": accent["deep"],
        "--display": "clamp(2.6rem, 6vw, 6rem)",
        "--body": "1rem/1.55",
        "--radius": "2px" if mood in {"quiet", "editorial"} else "18px",
        "--ease-out": "cubic-bezier(.22, 1, .36, 1)",
        "--ease-spring": "cubic-bezier(.2, 1.35, .4, 1)",
    }
    type_system = {
        "display": "Instrument Serif" if mood == "editorial" else ("IBM Plex Mono" if mood == "technical" else "Satoshi"),
        "body": "Satoshi" if mood != "technical" else "IBM Plex Sans",
        "utility": "JetBrains Mono",
    }
    return _j({
        "ok": True,
        "direction": direction,
        "thesis": f"{accent['note']} The page is built around {signature[0]['name'].lower()} and {signature[1]['name'].lower()}.",
        "base": base["name"],
        "mood": mood,
        "stack": stack,
        "signature_moves": [
            {"id": f["id"], "name": f["name"], "skill": f["skill"], "signature": f["signature"]}
            for f in signature
        ],
        "tokens": tokens,
        "type": type_system,
        "composition": [
            "First screen: one loud line, one quiet paragraph, one action, one proof object.",
            "Second screen: the first signature move at full size; no second hero.",
            "Middle: alternate a dense instrument with a quiet section; break the grid once.",
            "Final: a plain-language close and a real next action; no fake logo wall.",
        ],
        "motion": {
            "feedback_ms": 160,
            "scene_ms": 520,
            "ease": "--ease-out",
            "spring": "--ease-spring",
            "reduced": "Freeze transforms and parallax; keep state changes and content.",
        },
        "avoid": avoid,
        "build_order": [
            "Write the reference map and the not-doing list.",
            "Set tokens and type; test the first screen without images.",
            "Build the structural signature move; verify at 390px.",
            "Build the behavioral signature; test pointer, keyboard and reduced motion.",
            "Add content, then run the audit and three-width screenshots.",
        ],
        "acceptance": checks,
        "constraints": constraints,
        "skills": [f["skill"] for f in signature],
        "component_candidates": list(dict.fromkeys(
            cid for pick in picks for cid in (
                COMPONENT_HINTS.get(pick, []) + [c["id"] for c in COMPONENTS if c["family"] == pick]
            )
        ))[:8],
        "caveat": "This is a direction. The builder must still study the reference, write original code and verify in a browser.",
    })


def h_components(args: dict) -> str:
    family = str(args.get("family") or "").strip().lower()
    query = str(args.get("query") or "").strip().lower()
    rows = COMPONENTS
    if family:
        rows = [c for c in rows if c["family"] == family]
    if query:
        rows = [c for c in rows if query in (c["name"] + " " + c["state"] + " " + c["use_when"]).lower()]
    return _j({
        "ok": True,
        "count": len(rows),
        "families": sorted({c["family"] for c in COMPONENTS}),
        "components": rows,
        "note": "Public observations only. The source URL is a public preview; it is not a licence to copy the implementation.",
    })


def h_stacks(args: dict) -> str:
    return _j({
        "ok": True,
        "stacks": [
            {"id": key, "label": value["label"], "adapter": value["file"],
             "skills": value["skills"]}
            for key, value in STACKS.items()
        ],
        "motion": ["css", "gsap"],
        "kinds": sorted(KINDS),
        "note": "Mosaic does not vendor these skills; it routes the agent to the installed skill set. Load at most three per phase.",
    })


def h_forge(args: dict) -> str:
    kind = str(args.get("kind") or "").strip()
    stack = str(args.get("stack") or "html").strip().lower()
    motion = str(args.get("motion") or "css").strip().lower()
    brief = str(args.get("brief") or "").strip()
    return forge(kind, stack, motion, brief)


def h_invent(args: dict) -> str:
    brief = str(args.get("brief") or "").strip()
    constraints = str(args.get("constraints") or "").strip()
    count = int(args.get("count") or 3)
    seed = args.get("seed")
    if seed is not None:
        seed = int(seed)
    return invent(brief, constraints, count, seed)


def h_audit(args: dict) -> str:
    source = args.get("source")
    path = args.get("path")
    if bool(source) == bool(path):
        raise ValueError("pass exactly one of source or path")
    if path:
        return _j(audit_path(_text(path, "path", 1000)))
    return _j(audit_source(_text(source, "source", 300_000)))


TOOL_SPECS = [
    {
        "name": "mosaic_index",
        "handler": h_index,
        "emoji": "🗂️",
        "description": "List the reference families, design methods, skills and base design tokens.",
        "schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "mosaic_study",
        "handler": h_study,
        "emoji": "🔬",
        "description": "Turn observed references into principles, transferable moves and a do-not-copy contract. A URL alone returns a capture checklist, not invented facts.",
        "schema": {
            "type": "object",
            "properties": {
                "reference": {
                    "type": ["object", "string"],
                    "description": "A reference object with name/url/observations, or a name/URL string.",
                },
                "brief": {"type": "string"},
                "constraints": {"type": "string"},
            },
            "required": ["reference"],
        },
    },
    {
        "name": "mosaic_design",
        "handler": h_design,
        "emoji": "✳️",
        "description": "Act as a design director: read the brief, study references, propose three concepts, select one, define the system and optionally emit a complete page starter.",
        "schema": {
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": "What is being built, for whom, and why."},
                "audience": {"type": "string"},
                "constraints": {"type": "string"},
                "references": {
                    "type": "array",
                    "maxItems": 6,
                    "items": {"type": ["object", "string"]},
                },
                "mood": {"type": "string", "enum": sorted(MOODS)},
                "stack": {"type": "string"},
                "mode": {"type": "string", "enum": ["direction", "page"]},
                "seed": {"type": "integer"},
            },
            "required": ["brief"],
        },
    },
    {
        "name": "mosaic_components",
        "handler": h_components,
        "emoji": "🧩",
        "description": "List the public component observations (state model, timing, parameters, a11y) filtered by family or query.",
        "schema": {
            "type": "object",
            "properties": {
                "family": {"type": "string", "description": "press, drag, hover, select, shader, type, scroll or loading"},
                "query": {"type": "string", "description": "Text to match against name, state and use_when."},
            },
        },
    },
    {
        "name": "mosaic_stacks",
        "handler": h_stacks,
        "emoji": "🧱",
        "description": "Return the framework matrix (HTML, React, Next, Svelte, Vue, Astro) and the Hermes web skills that pair with each target.",
        "schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "mosaic_forge",
        "handler": h_forge,
        "emoji": "🛠️",
        "description": "Generate an original component starter for a framework and either CSS or GSAP motion.",
        "schema": {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": sorted(KINDS)},
                "stack": {"type": "string", "enum": list(STACKS) + ["all"]},
                "motion": {"type": "string", "enum": ["css", "gsap"]},
                "brief": {"type": "string"},
            },
            "required": ["kind"],
        },
    },
    {
        "name": "mosaic_invent",
        "handler": h_invent,
        "emoji": "💡",
        "description": "Invent interaction candidates from a brief with a state machine and a transparent taste score.",
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
    {
        "name": "mosaic_recipe",
        "handler": h_recipe,
        "emoji": "🧪",
        "description": "Turn a product brief into an original design direction with tokens, type, two signature moves and checks.",
        "schema": {
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": "What is being built, for whom, and why."},
                "mood": {"type": "string", "enum": sorted(MOODS)},
                "stack": {"type": "string", "description": "Target stack, e.g. Next.js + Tailwind."},
                "constraints": {"type": "string", "description": "Hard constraints: brand, content, a11y, performance."},
            },
            "required": ["brief"],
        },
    },
    {
        "name": "mosaic_visual",
        "handler": h_visual,
        "emoji": "👁️",
        "description": "Render a URL or local HTML page in Chromium and return a measured visual guarantee: screenshots, contrast, overlap, overflow, focus, reduced motion, control size and explicit blockers.",
        "schema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "A public http(s) URL or a local .html file."},
                "source": {"type": "string", "description": "Complete HTML source to render instead of a target."},
            },
        },
    },
    {
        "name": "mosaic_audit",
        "handler": h_audit,
        "emoji": "🔎",
        "description": "Scan local HTML/CSS/JS text for generic gradients, transition-all, missing reduced motion and other design slop.",
        "schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Local text file to scan."},
                "source": {"type": "string", "description": "Source text to scan instead of a path."},
            },
        },
    },
    {
        "name": "mosaic_critique",
        "handler": h_critique,
        "emoji": "🪞",
        "description": "Critique a local source for generic copy, heading hierarchy, focus, content-slot discipline, radius/font noise and generic CSS patterns.",
        "schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Local text file to critique."},
                "source": {"type": "string", "description": "Source text to critique instead of a path."},
                "brief": {"type": "string"},
            },
        },
    },
    {
        "name": "mosaic_score",
        "handler": h_score,
        "emoji": "🏁",
        "description": "Score a built source before an awards-style review: design, usability, creativity, content and originality, with blockers and next moves.",
        "schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Local text file to score."},
                "source": {"type": "string", "description": "Source text to score instead of a path."},
                "brief": {"type": "string"},
                "references": {"type": "array", "maxItems": 6, "items": {"type": "object"}},
            },
        },
    },
]
