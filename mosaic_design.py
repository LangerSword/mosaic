"""Mosaic Design: a local design director, not a template picker.

The tool reads a brief and optional reference observations, proposes three
distinct structural concepts, selects one with a transparent rubric, and turns
it into a design system, composition and (optionally) a complete static page
starter. It never fetches a reference, invents visual facts or copies assets.
"""
from __future__ import annotations

import html
import json
import re
from typing import Any

try:
    from .mosaic_data import MOODS
    from .mosaic_study import normalize_reference, study_reference
except ImportError:  # standalone CLI / tests
    from mosaic_data import MOODS
    from mosaic_study import normalize_reference, study_reference

DOMAINS = {
    "developer": {
        "label": "developer tools",
        "match": ("developer", "devtool", "sdk", "api", "agent", "repo", "terminal", "infra", "harness", "debug"),
        "audience": "developers and technical teams",
        "objects": ("repository", "agent", "run", "trace", "contract", "log"),
        "verbs": ("inspect", "run", "compare", "deploy", "trace"),
        "archetypes": ("bench", "index", "signal-room"),
        "mood": "technical",
    },
    "data": {
        "label": "data and operations",
        "match": ("dashboard", "analytics", "metric", "monitor", "observability", "log", "data", "telemetry"),
        "audience": "operators and analysts",
        "objects": ("signal", "source", "window", "alert", "record"),
        "verbs": ("scan", "compare", "drill", "watch", "verify"),
        "archetypes": ("signal-room", "index", "bench"),
        "mood": "technical",
    },
    "commerce": {
        "label": "commerce and collecting",
        "match": ("shop", "store", "product", "price", "checkout", "collection", "market", "sell", "buy", "ticket"),
        "audience": "curious buyers and collectors",
        "objects": ("object", "edition", "receipt", "collection", "detail"),
        "verbs": ("browse", "compare", "collect", "buy", "reserve"),
        "archetypes": ("specimen-table", "index", "programme"),
        "mood": "tactile",
    },
    "editorial": {
        "label": "editorial and knowledge",
        "match": ("editorial", "magazine", "article", "essay", "journal", "library", "docs", "documentation", "book", "writing"),
        "audience": "readers and researchers",
        "objects": ("essay", "note", "issue", "source", "index"),
        "verbs": ("read", "scan", "annotate", "save", "follow"),
        "archetypes": ("reading-room", "field-guide", "index"),
        "mood": "editorial",
    },
    "media": {
        "label": "media and performance",
        "match": ("music", "album", "film", "video", "stream", "podcast", "performance", "event", "festival", "stage"),
        "audience": "listeners and audiences",
        "objects": ("track", "scene", "programme", "cue", "note"),
        "verbs": ("listen", "watch", "follow", "book", "replay"),
        "archetypes": ("programme", "field-guide", "signal-room"),
        "mood": "playful",
    },
    "game": {
        "label": "games and play",
        "match": ("game", "deck", "card", "player", "quest", "table", "arena", "collect"),
        "audience": "players and collectors",
        "objects": ("card", "hand", "round", "rule", "table"),
        "verbs": ("play", "draw", "deal", "build", "counter"),
        "archetypes": ("specimen-table", "programme", "index"),
        "mood": "playful",
    },
    "portfolio": {
        "label": "portfolio and practice",
        "match": ("portfolio", "designer", "photographer", "artist", "studio", "freelance", "practice"),
        "audience": "clients and peers",
        "objects": ("work", "note", "project", "process", "specimen"),
        "verbs": ("browse", "read", "contact", "inspect", "save"),
        "archetypes": ("field-guide", "index", "bench"),
        "mood": "quiet",
    },
    "service": {
        "label": "service and studio",
        "match": ("agency", "studio", "service", "booking", "clinic", "consult", "team", "client"),
        "audience": "clients and collaborators",
        "objects": ("case", "offer", "process", "proof", "contact"),
        "verbs": ("book", "compare", "enquire", "choose", "start"),
        "archetypes": ("reading-room", "index", "specimen-table"),
        "mood": "quiet",
    },
    "generic": {
        "label": "product",
        "match": (),
        "audience": "the people who will use it",
        "objects": ("artifact", "note", "record", "path"),
        "verbs": ("browse", "inspect", "choose", "begin"),
        "archetypes": ("index", "field-guide", "bench"),
        "mood": "quiet",
    },
}

DOMAIN_COPY = {
    "developer": {
        "headline": "Make the system legible.",
        "subhead": "The interface, the traces and the contracts that make it run.",
        "nav": ("index", "systems", "contact"),
        "cta": "Open the index",
        "secondary": "Read the method",
        "artifact": "trace",
    },
    "data": {
        "headline": "What the system is doing.",
        "subhead": "A readable signal, its source and the caveat that keeps it honest.",
        "nav": ("signal", "sources", "notes"),
        "cta": "Inspect the signal",
        "secondary": "Read the source",
        "artifact": "signal",
    },
    "commerce": {
        "headline": "Objects with a history.",
        "subhead": "A small collection, its materials and the details that survive a second look.",
        "nav": ("collection", "details", "visit"),
        "cta": "Enter the collection",
        "secondary": "Read the notes",
        "artifact": "objects",
    },
    "editorial": {
        "headline": "Read the room.",
        "subhead": "A small catalogue of writing and the reasons it belongs together.",
        "nav": ("reading", "archive", "contact"),
        "cta": "Open the catalogue",
        "secondary": "Read the method",
        "artifact": "excerpt",
    },
    "media": {
        "headline": "A programme, not a playlist.",
        "subhead": "A sequence of work with a current cue, a running order and a reason for each move.",
        "nav": ("programme", "stage", "notes"),
        "cta": "Cue the programme",
        "secondary": "Read the notes",
        "artifact": "programme",
    },
    "game": {
        "headline": "The table is the product.",
        "subhead": "A hand, a rule and a clear consequence; the play is the proof.",
        "nav": ("table", "rules", "play"),
        "cta": "Take a seat",
        "secondary": "Read the rules",
        "artifact": "table",
    },
    "portfolio": {
        "headline": "The work, in the open.",
        "subhead": "Selected work, notes and the process behind them.",
        "nav": ("work", "notes", "contact"),
        "cta": "Start a conversation",
        "secondary": "Inspect the work",
        "artifact": "index",
    },
    "service": {
        "headline": "A practice, not a pitch.",
        "subhead": "The work, the method and the people who make it possible.",
        "nav": ("work", "method", "contact"),
        "cta": "Start a conversation",
        "secondary": "Read the method",
        "artifact": "index",
    },
    "generic": {
        "headline": "A clearer way through.",
        "subhead": "One artifact, one action and the evidence that makes it worth using.",
        "nav": ("index", "proof", "contact"),
        "cta": "Open the index",
        "secondary": "Read the proof",
        "artifact": "index",
    },
}


def _domain_copy(domain_id: str, brief: str) -> dict:
    copy = dict(DOMAIN_COPY.get(domain_id, DOMAIN_COPY["generic"]))
    if domain_id == "portfolio" and re.search(r"\b(type|typeface|font|typograph)", brief, re.I):
        copy.update({
            "headline": "Type, set to work.",
            "subhead": "A working specimen of letterforms, the pages they carry and the thinking behind them.",
            "nav": ("specimens", "process", "contact"),
            "artifact": "specimen",
            "cta": "Open the specimen",
            "secondary": "Read the practice",
        })
    return copy


ARCHETYPES = {
    "index": {
        "name": "The Working Index",
        "artifact": "a working index with a specimen pane",
        "adjacent": "library science / specimen catalogues",
        "first_screen": "A large title at the left edge with a live index running down the right edge; the first row is already open.",
        "sections": (
            ("arrival", "Title, one-sentence thesis, one action and the first index row visible without scrolling."),
            ("index", "A dense list of real entries; selecting one swaps the adjacent specimen rather than opening a modal."),
            ("proof", "Three artifacts with provenance, not three feature cards."),
            ("system", "A short note on the method: what is indexed, what is excluded, how it is maintained."),
            ("close", "A plain next action and a real contact or source."),
        ),
        "interaction": {
            "name": "scan to specimen",
            "input": "pointer, arrow keys, Home/End and focus",
            "state": "the active index row and the specimen share one selected id",
        },
        "novelty": 8,
        "restraint": 9,
        "risk": "An index can become a table of contents with no point of view; the specimen must carry real character.",
    },
    "bench": {
        "name": "The Bench",
        "artifact": "a workbench with three tools and one live specimen",
        "adjacent": "fine woodworking / instrument repair",
        "first_screen": "An asymmetric split: the claim and action occupy the left bench, the first tool is already picked up on the right.",
        "sections": (
            ("arrival", "The job to be done, the first tool and a proof artifact within one composition."),
            ("bench", "A small set of tools or modes arranged as objects; picking one changes the bench, not the page."),
            ("proof", "One detailed artifact with the marks of use: annotations, tolerances, a before/after."),
            ("method", "The working method stated as steps, not as brand values."),
            ("close", "A next action that starts the work; no generic sales close."),
        ),
        "interaction": {
            "name": "pick up a tool",
            "input": "pointer, focus, number keys 1–3",
            "state": "tool selection changes the example, the instruction and the active instrument",
        },
        "novelty": 9,
        "restraint": 8,
        "risk": "A bench can turn into decorative skeuomorphism; keep the tools functional and the labels plain.",
    },
    "field-guide": {
        "name": "The Field Guide",
        "artifact": "an annotated field guide with specimens and marginal notes",
        "adjacent": "field biology / annotated archives",
        "first_screen": "A central specimen with handwritten-looking margin notes and one index strip; the note is evidence, not decoration.",
        "sections": (
            ("arrival", "A specimen, a short observation and a live index of the other specimens."),
            ("specimens", "Three to five specimens with labels, provenance and one honest observation each."),
            ("annotation", "A single close reading of one specimen, with margin notes and a real method note."),
            ("index", "A compact index that reveals the rest without turning the page into a grid."),
            ("close", "A clear route to the source, the person or the next action."),
        ),
        "interaction": {
            "name": "open a specimen",
            "input": "hover as a preview, click/Enter to pin, arrow keys to move",
            "state": "preview and pinned specimen are distinct; focus always reveals the same content",
        },
        "novelty": 8,
        "restraint": 8,
        "risk": "Annotations can become decorative noise; every note must say something the specimen does not.",
    },
    "programme": {
        "name": "The Programme",
        "artifact": "a programme or score with cues and a running order",
        "adjacent": "concert programmes / broadcast rundowns",
        "first_screen": "A time-based sequence with one current cue, a running order and the first artifact already playing.",
        "sections": (
            ("arrival", "The promise, the current cue and the next real action; no autoplay takeover."),
            ("running-order", "A sequence of real items with times or durations that are supplied, never invented."),
            ("stage", "The current item at full scale with a quiet control surface."),
            ("notes", "A short programme note that explains the selection."),
            ("close", "A simple route to attend, play, book or follow."),
        ),
        "interaction": {
            "name": "cue the next item",
            "input": "click, Enter/Space, arrow keys and a visible play state",
            "state": "the selected cue, the stage and the progress label agree; pause is always available",
        },
        "novelty": 8,
        "restraint": 8,
        "risk": "A programme can feel like a media player clone; the sequence and the notes are the identity.",
    },
    "signal-room": {
        "name": "The Signal Room",
        "artifact": "a live instrument panel with one signal and a readable source rail",
        "adjacent": "radio rooms / observatories",
        "first_screen": "A single strong readout, a source rail and one control; the rest is silence and scale.",
        "sections": (
            ("arrival", "One real signal, its source and a control that changes the view."),
            ("signal", "The main artifact: a measured field, trace or list with units and provenance."),
            ("context", "The source, the window and the caveat; no fake live telemetry."),
            ("controls", "A small set of controls with visible state and a reduced-motion equivalent."),
            ("close", "A route to inspect the source or run the next operation."),
        ),
        "interaction": {
            "name": "tune the signal",
            "input": "pointer, keyboard, range control and direct values",
            "state": "the readout, the label and the source all update from one value",
        },
        "novelty": 9,
        "restraint": 7,
        "risk": "A signal room without a real source becomes fake telemetry; use supplied data or leave the state honestly empty.",
    },
    "specimen-table": {
        "name": "The Specimen Table",
        "artifact": "a specimen table where objects can be picked up and compared",
        "adjacent": "museum conservation / auction catalogues",
        "first_screen": "Three objects on a generous table, one picked up, with the detail card at the edge rather than over the object.",
        "sections": (
            ("arrival", "A few objects, the collection rule and one action to enter the collection."),
            ("table", "Objects laid out with real attributes; selection swaps a detail rail."),
            ("detail", "One object at full scale with materials, provenance and one honest note."),
            ("compare", "A quiet comparison state, at most two objects at a time."),
            ("close", "A source, a reservation or a next collection."),
        ),
        "interaction": {
            "name": "pick up and compare",
            "input": "click, focus, arrow keys; compare via explicit toggle",
            "state": "selected and compared objects are distinct; the detail rail never covers the table",
        },
        "novelty": 8,
        "restraint": 8,
        "risk": "A table can become a card grid; object scale, negative space and detail rail are what make it physical.",
    },
    "reading-room": {
        "name": "The Reading Room",
        "artifact": "a long reading table with a quiet index and a marginal note",
        "adjacent": "research libraries / annotated bibliographies",
        "first_screen": "A measured reading column, a short catalogue rail and one excerpt that earns the whitespace.",
        "sections": (
            ("arrival", "The proposition, the first reading and a catalogue rail with real entries."),
            ("reading", "A reading column at 45–75ch; one pull quote or annotation, not a card pile."),
            ("catalogue", "A compact index of issues, essays or sources with dates that come from data."),
            ("method", "A short note on selection, editorial rules and provenance."),
            ("close", "A route to read next, subscribe or contact."),
        ),
        "interaction": {
            "name": "open a reading",
            "input": "click, focus, arrow keys; no hover-only preview",
            "state": "the selected reading and the catalogue share one id; reading remains in flow",
        },
        "novelty": 7,
        "restraint": 9,
        "risk": "A reading room can become beige minimalism; typography, measure and one asymmetric note must carry it.",
    },
}

ACTIONS = ("build", "buy", "book", "browse", "choose", "collect", "compare", "contact", "deploy", "follow",
           "inspect", "join", "listen", "play", "read", "run", "scan", "start", "verify", "watch")

GENERIC_COPY = (
    "seamless", "unlock", "empower", "revolutionary", "next-generation", "next generation",
    "world-class", "cutting-edge", "game-changing", "effortless", "we build", "we make",
)


def _text(value: Any, limit: int = 2000) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()[:limit]


def _words(value: str) -> list[str]:
    return re.findall(r"[a-z0-9][a-z0-9+#./-]*", value.lower())


def _pick_domain(brief: str) -> dict:
    low = brief.lower()
    scored = []
    for key, domain in DOMAINS.items():
        score = sum(1 for word in domain["match"] if word in low)
        if key == "generic":
            score = 0
        if score:
            scored.append((score, key))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return DOMAINS[scored[0][1] if scored else "generic"]


def _subject(brief: str) -> str:
    value = re.sub(r"^(a|an|the)\s+", "", brief.strip(), flags=re.I)
    value = re.split(r"[.!?]\s", value)[0]
    value = re.split(r"\b(?:for|that|who|where|with|which)\b", value, maxsplit=1, flags=re.I)[0]
    words = value.split()
    value = " ".join(words[:6]).strip(" ,;:-")
    return value or "the work"


def _audience(brief: str, domain: dict, explicit: str) -> str:
    if explicit:
        return explicit.strip()[:180]
    match = re.search(r"\bfor\s+([a-z][a-z0-9 /&-]{2,60})", brief, re.I)
    if match:
        value = re.split(r"[,.;]\s|\bthat\b|\bwho\b", match.group(1), maxsplit=1, flags=re.I)[0]
        return value.strip()[:120] or domain["audience"]
    return domain["audience"]


def _action(brief: str, domain: dict) -> str:
    low = brief.lower()
    found = [verb for verb in ACTIONS if re.search(rf"\b{re.escape(verb)}\b", low)]
    if found:
        return found[0]
    return domain["verbs"][0]


def _flags(constraints: str) -> dict:
    low = constraints.lower()
    return {
        "no_hover": "no hover" in low or "keyboard" in low,
        "mobile_first": "mobile" in low,
        "low_bandwidth": "bandwidth" in low or "slow network" in low or "no images" in low,
        "no_webgl": "no webgl" in low or "no 3d" in low,
        "dark": "dark" in low,
        "light": "light" in low,
        "accessible": "accessib" in low or "wcag" in low,
    }


def _contrast(a: str, b: str) -> float:
    def rgb(value: str) -> tuple[int, ...]:
        value = value.lstrip("#")
        if len(value) == 3:
            value = "".join(ch * 2 for ch in value)
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    def lum(value: str) -> float:
        parts = []
        for channel in rgb(value):
            c = channel / 255
            parts.append(c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4)
        return .2126 * parts[0] + .7152 * parts[1] + .0722 * parts[2]
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return round((x + .05) / (y + .05), 2)


def _mood_key(mood: str, domain: dict, flags: dict) -> str:
    if mood in MOODS:
        return mood
    if flags["dark"]:
        return "technical"
    return domain["mood"] if domain["mood"] in MOODS else "quiet"


def _reference_results(references: list, brief: str, constraints: str) -> list[dict]:
    rows = []
    for index, raw in enumerate(references[:6]):
        normalized = normalize_reference(raw, index)
        rows.append(study_reference(normalized, brief, constraints))
    return rows


def _score(archetype_id: str, domain: dict, reference_results: list[dict]) -> dict:
    meta = ARCHETYPES[archetype_id]
    fit = 9 if archetype_id in domain["archetypes"] else 6
    if domain["archetypes"] and archetype_id == domain["archetypes"][0]:
        fit = 10
    evidence = next((r for r in reference_results if r.get("confidence") in {"high", "medium"}), None)
    distance = 8 if not evidence else 7
    scores = {
        "coherence": 9,
        "specificity": 8 if evidence else 9,
        "novelty": meta["novelty"] + (1 if evidence else 0),
        "usability": 9,
        "restraint": meta["restraint"],
        "reference_distance": distance,
        "fit": fit,
    }
    overall = round(
        scores["fit"] * .22 + scores["coherence"] * .18 + scores["specificity"] * .18 +
        scores["novelty"] * .16 + scores["usability"] * .16 + scores["restraint"] * .10,
        1,
    )
    return {**scores, "overall": min(10, overall)}


def _darken(value: str, amount: float = .18) -> str:
    value = value.lstrip("#")
    channels = [int(value[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{max(0, round(c * (1 - amount))):02x}" for c in channels)


def _tokens(mood: str, flags: dict) -> dict:
    palette = MOODS[mood]
    field, ink = palette["field"], palette["ink"]
    channel = int(field.lstrip("#")[0:2], 16)
    green = int(field.lstrip("#")[2:4], 16)
    blue = int(field.lstrip("#")[4:6], 16)
    dark = (0.2126 * channel + 0.7152 * green + 0.0722 * blue) / 255 < .45
    muted = "#b6b1a6" if dark else "#5f635c"
    line = "#30302e" if dark else "#ddd8cc"
    surface = "#141414" if dark else "#f7f3ea"
    signal = palette["accent"]
    if _contrast(signal, field) < 4.5:
        signal = _darken(signal, .2)
    focus = signal
    return {
        "--field": field,
        "--surface": surface,
        "--ink": ink,
        "--muted": muted,
        "--line": line,
        "--signal": signal,
        "--deep": palette["deep"],
        "--focus": focus,
        "--measure": "62ch",
        "--gutter": "clamp(18px, 3vw, 32px)",
        "--max": "1440px",
        "--radius": "0px" if mood in {"quiet", "editorial", "technical"} else "12px",
        "--display": "clamp(3.2rem, 9vw, 8.5rem)",
        "--display-font": _type_system(mood)["display"]["stack"],
        "--body": "clamp(1rem, .4vw + .9rem, 1.15rem)",
        "--body-font": _type_system(mood)["body"]["stack"],
        "--mono": "clamp(.65rem, .8vw, .78rem)",
        "--utility-font": _type_system(mood)["utility"]["stack"],
        "--ease": "cubic-bezier(.22, 1, .36, 1)",
        "--dur": "520ms",
        "--contrast": {
            "ink_on_field": _contrast(ink, field),
            "signal_on_field": _contrast(signal, field),
            "muted_on_field": _contrast(muted, field),
        },
    }


def _type_system(mood: str) -> dict:
    return {
        "display": {
            "stack": '"Fraunces", "Iowan Old Style", Georgia, serif' if mood == "editorial" else
                     '"Space Grotesk", "Helvetica Neue", sans-serif' if mood == "technical" else
                     '"Bricolage Grotesque", "Avenir Next", sans-serif',
            "role": "one loud line; never body copy",
        },
        "body": {
            "stack": '"Satoshi", "Avenir Next", "Segoe UI", sans-serif',
            "role": "reading; 45–75ch",
        },
        "utility": {
            "stack": '"JetBrains Mono", "SFMono-Regular", monospace',
            "role": "labels, data, captions",
        },
    }


def _content_contract(brief: str, audience: str, action: str, domain: dict) -> dict:
    return {
        "brand": {"slot": "brand", "rule": "the real name; do not invent a logo"},
        "headline": {"slot": "headline", "rule": "the one promise; no adjectives without a fact"},
        "thesis": {"slot": "thesis", "rule": "what the page does and for whom"},
        "action": {"slot": "action", "rule": f"the one primary action: {action}"},
        "inventory": {"slot": "inventory", "rule": f"real {', '.join(domain['objects'][:3])} entries; no lorem or invented metrics"},
        "proof": {"slot": "proof", "rule": "one real artifact with provenance; no logo wall"},
        "constraints": {"slot": "constraints", "rule": "keep the supplied limits visible in the build notes"},
    }


def _concept(archetype_id: str, domain: dict, analysis: dict, references: list[dict]) -> dict:
    meta = ARCHETYPES[archetype_id]
    evidence = next((r for r in references if r.get("confidence") in {"high", "medium"}), None)
    borrow = ""
    anchor = "first principles"
    if evidence:
        anchor = evidence["reference"]["name"]
        candidates = evidence.get("principles", [])
        if candidates:
            borrow = candidates[0]["observation"]
    scores = _score(archetype_id, domain, references)
    return {
        "id": archetype_id,
        "name": meta["name"],
        "artifact": meta["artifact"],
        "thesis": f"A {domain['label']} built as {meta['artifact']} for {analysis['audience']}, so {analysis['action']} is the first physical move.",
        "adjacent_field": meta["adjacent"],
        "first_screen": meta["first_screen"],
        "sections": [{"id": sid, "job": job} for sid, job in meta["sections"]],
        "interaction": meta["interaction"],
        "reference_anchor": anchor,
        "borrow": borrow or "No surface borrowing; derive the structure from the brief.",
        "translate": f"Keep the relationship between {meta['artifact']} and the primary action; change the subject, content and visual language to this brief.",
        "do_not_copy": [
            "exact layout, code, component structure or motion timing",
            "brand marks, photography, copy and proprietary assets",
            "a reference palette treated as an identity",
        ],
        "novelty_move": f"Pair {meta['adjacent'].split(' / ')[0]} with {domain['label']} instead of another page in the same category.",
        "risk": meta["risk"],
        "scores": scores,
    }


def _system(concept: dict, mood: str, flags: dict) -> dict:
    tokens = _tokens(mood, flags)
    material = {
        "primary": "ascii field" if mood == "technical" else "paper and ink",
        "secondary": "one glass lens" if mood in {"editorial", "playful", "tactile"} else "hairline rule",
        "rules": [
            "One material gesture per section; do not stack ASCII, glass, grain and glow.",
            "ASCII is a density field with a static fallback; glass is one object over a strong ground.",
            "Measure text contrast against the blended material, never the raw ground.",
            "No blur behind body copy; no ASCII under body copy.",
        ],
    }
    return {
        "mood": mood,
        "concept": concept["name"],
        "tokens": {key: value for key, value in tokens.items() if key != "--contrast"},
        "contrast": tokens["--contrast"],
        "type": _type_system(mood),
        "material": material,
        "composition": {
            "first_screen": concept["first_screen"],
            "sections": concept["sections"],
            "grid": {"columns": 12, "max": "var(--max)", "gutter": "var(--gutter)", "asymmetry": True},
            "measure": "45–75ch for body; display may break the grid intentionally",
        },
        "motion": {
            "feedback": "140–180ms; transform and opacity only",
            "scene": "420–620ms; one state change at a time",
            "ease": "cubic-bezier(.22, 1, .36, 1)",
            "reduced": "freeze transforms and parallax; keep state and content",
        },
        "avoid": [
            "purple-to-blue gradient as the identity",
            "three identical feature cards",
            "glass on every surface",
            "hover-only content or actions",
            "invented metrics, logos or testimonials",
        ],
    }


def _artifact_html(kind: str, objects: list[str]) -> str:
    labels = [obj.title() for obj in objects]
    if kind == "specimen":
        return (
            '<div class="artifact-head"><span>type specimen</span><span>01 / display</span></div>'
            '<div class="type-specimen">'
            '<span class="glyph" aria-hidden="true">Aa</span>'
            '<span class="typeface-slot" data-slot="typeface">typeface / replace</span>'
            '<p class="specimen-note">Letterforms first. The page is a working specimen, not a gallery of cards.</p>'
            '<div class="specimen-line" data-specimen-line>Hamburgefontsiv 0123</div>'
            '<div class="specimen-controls">'
            '<label>size <input type="range" min="2" max="8" step=".25" value="4.5" data-specimen-size /></label>'
            '<label>tracking <input type="range" min="-8" max="4" step="1" value="-3" data-specimen-tracking /></label>'
            '</div>'
            '<div class="specimen-scale"><span>display</span><span>text</span><span>utility</span></div>'
            '</div>'
        )
    if kind == "trace":
        return (
            '<div class="artifact-head"><span>working trace</span><span>03 moves</span></div>'
            '<ol class="trace">'
            + ''.join(f'<li><span>0{i+1}</span><b>{html.escape(label.lower())}</b><em>{html.escape(label)}</em></li>' for i, label in enumerate(labels))
            + '</ol>'
        )
    if kind == "signal":
        return (
            '<div class="artifact-head"><span>source rail</span><span>03 states</span></div>'
            '<div class="signal-list">'
            + ''.join(f'<div><span>0{i+1} / {html.escape(label.lower())}</span><b>{html.escape(label)}</b><em>source</em></div>' for i, label in enumerate(labels))
            + '</div>'
        )
    if kind == "objects":
        return (
            '<div class="artifact-head"><span>collection</span><span>03 objects</span></div>'
            '<div class="object-list">'
            + ''.join(f'<div><span>0{i+1}</span><b>{html.escape(label)}</b><em>detail</em></div>' for i, label in enumerate(labels))
            + '</div>'
        )
    if kind == "excerpt":
        return (
            '<div class="artifact-head"><span>reading rail</span><span>03 notes</span></div>'
            '<blockquote class="excerpt">“The measure is the first material.”</blockquote>'
            '<div class="excerpt-meta"><span>replace with a real excerpt</span><span>45–75ch</span></div>'
        )
    if kind == "programme":
        return (
            '<div class="artifact-head"><span>running order</span><span>03 cues</span></div>'
            '<ol class="programme-list">'
            + ''.join(f'<li><span>0{i+1}</span><b>{html.escape(label)}</b><em>cue</em></li>' for i, label in enumerate(labels))
            + '</ol>'
        )
    rows = ''.join(
        f'<button class="specimen" type="button" data-specimen data-cue="{i}" data-title="{html.escape(label)}" data-note="{html.escape(label.lower())}">'
        f'<span class="num">0{i + 1}</span><span class="title">{html.escape(label)}</span><span class="arrow">↗</span></button>'
        for i, label in enumerate(labels)
    )
    return f'<div class="artifact-head"><span>live index</span><span>03 entries</span></div><div data-index>{rows}</div>'


def _page(concept: dict, domain: dict, analysis: dict, system: dict) -> dict:
    subject = html.escape(analysis["subject"])
    copy = analysis["copy"]
    headline = html.escape(copy["headline"])
    subhead = html.escape(copy["subhead"])
    audience = html.escape(analysis["audience"])
    nav = copy["nav"]
    cta = html.escape(copy["cta"])
    tokens = system["tokens"]
    colors = "\n".join(f"  {key}: {value};" for key, value in tokens.items())
    objects = list(domain["objects"])[:3]
    artifact = _artifact_html(copy["artifact"], objects)
    options = "\n".join(
        f'<button class="cue" type="button" data-cue="{i}">0{i + 1} / {html.escape(obj)}</button>'
        for i, obj in enumerate(objects)
    )
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{headline} / design starter</title>
<style>
:root {{
{colors}
}}
* {{ box-sizing: border-box; }}
html {{ color-scheme: {'dark' if system['mood'] == 'technical' else 'light'}; }}
body {{ margin: 0; background: var(--field); color: var(--ink); font-family: var(--body-font); }}
a {{ color: inherit; }}
button {{ font: inherit; color: inherit; }}
:focus-visible {{ outline: 2px solid var(--focus); outline-offset: 4px; }}
.skip {{ position: absolute; left: -999px; top: 8px; min-height: 44px; display: inline-flex; align-items: center; padding: 10px 14px; background: var(--ink); color: var(--field); }}
.skip:focus {{ left: 8px; z-index: 9; }}
.shell {{ width: min(100% - 2 * var(--gutter), var(--max)); margin: 0 auto; }}
.bar {{ display: flex; justify-content: space-between; align-items: center; min-height: 64px; border-bottom: 1px solid var(--line); font-family: var(--utility-font); font-size: var(--mono); }}
.brand {{ display: inline-flex; align-items: center; min-height: 44px; text-decoration: none; font-weight: 700; letter-spacing: -.04em; }}
.bar nav {{ display: flex; gap: 18px; }}
.bar nav a {{ display: inline-flex; align-items: center; min-height: 44px; text-decoration: none; border-bottom: 1px solid transparent; }}
.bar nav a:hover {{ border-color: var(--signal); }}
main {{ overflow: clip; }}
@media (prefers-reduced-motion: no-preference) {{
  html.js [data-reveal] {{ opacity: 0; transform: translateY(10px); transition: opacity .5s var(--ease), transform .5s var(--ease); }}
  html.js [data-reveal].is-in {{ opacity: 1; transform: none; }}
}}
.arrival {{ display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(280px, .85fr); gap: var(--gutter); padding: clamp(56px, 10vw, 144px) 0 72px; border-bottom: 1px solid var(--line); }}
.layout-bench .arrival {{ grid-template-columns: minmax(0, 1fr); }}
.layout-bench .artifact {{ max-width: 760px; margin-top: 28px; }}
.layout-field-guide .arrival {{ display: block; text-align: center; }}
.layout-field-guide .artifact {{ max-width: 760px; margin: 48px auto 0; text-align: left; }}
.layout-field-guide h1 {{ margin-inline: auto; }}
.layout-programme .arrival {{ grid-template-columns: minmax(0, .8fr) minmax(0, 1.2fr); }}
.layout-programme .artifact {{ border-top-color: var(--signal); }}
.layout-signal-room .arrival {{ background: var(--surface); padding-inline: var(--gutter); }}
.layout-specimen-table .arrival {{ grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); }}
.layout-reading-room .arrival {{ grid-template-columns: minmax(0, 1.3fr) minmax(0, .7fr); }}
.kicker {{ margin: 0 0 24px; color: var(--signal); font: 700 var(--mono)/1 var(--utility-font); letter-spacing: .12em; text-transform: uppercase; }}
h1 {{ max-width: 9ch; margin: 0; font-family: var(--display-font); font-size: var(--display); font-weight: 500; line-height: .84; letter-spacing: -.075em; }}
.deck {{ max-width: var(--measure); margin: 28px 0 0; color: var(--muted); font-size: var(--body); line-height: 1.55; }}
.act {{ display: inline-flex; min-height: 46px; align-items: center; margin-top: 30px; padding: 0 16px; border: 1px solid var(--ink); background: var(--ink); color: var(--field); font: 700 var(--mono)/1 var(--utility-font); letter-spacing: .1em; text-decoration: none; text-transform: uppercase; }}
.artifact {{ align-self: end; border-top: 1px solid var(--ink); padding-top: 12px; }}
.arrival > *, .signature > * {{ min-width: 0; }}
.artifact-head {{ display: flex; justify-content: space-between; color: var(--muted); font: var(--mono)/1.3 var(--utility-font); text-transform: uppercase; }}
.type-specimen {{ padding: 18px 0 4px; }}
.type-specimen .glyph {{ display: block; font-family: var(--display-font); font-size: clamp(6rem, 18vw, 15rem); line-height: .7; letter-spacing: -.1em; color: var(--ink); }}
.type-specimen .specimen-note {{ max-width: 28ch; margin: 22px 0 16px; color: var(--muted); line-height: 1.5; }}
.typeface-slot {{ display: inline-block; margin-top: 8px; color: var(--muted); font: var(--mono)/1.2 var(--utility-font); letter-spacing: .08em; text-transform: uppercase; }}
.specimen-line {{ margin: 14px 0 10px; font-family: var(--display-font); font-size: var(--specimen-size, 4.5rem); line-height: .9; letter-spacing: var(--specimen-tracking, -.03em); white-space: nowrap; max-width: 100%; overflow: hidden; }}
.specimen-controls {{ display: flex; flex-wrap: wrap; gap: 12px 20px; margin: 10px 0 16px; color: var(--muted); font: var(--mono)/1.2 var(--utility-font); text-transform: uppercase; }}
.specimen-controls label {{ display: flex; align-items: center; min-height: 44px; gap: 8px; }}
.specimen-controls input {{ width: 88px; height: 44px; accent-color: var(--signal); }}
.specimen-scale, .excerpt-meta {{ display: flex; justify-content: space-between; gap: 8px; border-top: 1px solid var(--line); padding-top: 8px; color: var(--muted); font: var(--mono)/1.3 var(--utility-font); text-transform: uppercase; }}
.trace, .programme-list {{ display: grid; gap: 0; margin: 0; padding: 0; list-style: none; }}
.trace li, .programme-list li {{ display: grid; grid-template-columns: 34px 1fr auto; gap: 8px; align-items: baseline; padding: 14px 0; border-bottom: 1px solid var(--line); }}
.trace li span, .programme-list li span {{ color: var(--muted); font: var(--mono)/1 var(--utility-font); }}
.trace li em, .programme-list li em {{ color: var(--muted); font: var(--mono)/1 var(--utility-font); }}
.trace li b, .programme-list li b {{ font-size: 1.05rem; }}
.signal-list, .object-list {{ display: grid; gap: 0; margin-top: 10px; }}
.signal-list div, .object-list div {{ display: grid; grid-template-columns: 1fr auto; gap: 4px 12px; align-items: baseline; padding: 13px 0; border-bottom: 1px solid var(--line); }}
.signal-list span, .object-list span {{ color: var(--muted); font: var(--mono)/1.3 var(--utility-font); text-transform: uppercase; }}
.signal-list b, .object-list b {{ grid-row: span 1; font-size: 1.05rem; text-align: right; }}
.signal-list em, .object-list em {{ color: var(--muted); font: var(--mono)/1.2 var(--utility-font); text-transform: uppercase; }}
.excerpt {{ max-width: 28ch; margin: 16px 0; font-family: var(--display-font); font-size: clamp(1.8rem, 3.5vw, 3rem); line-height: 1.05; letter-spacing: -.05em; }}
.specimen {{ display: grid; grid-template-columns: 36px 1fr 24px; width: 100%; gap: 8px; align-items: center; min-height: 58px; padding: 10px 0; border: 0; border-bottom: 1px solid var(--line); background: transparent; text-align: left; cursor: pointer; }}
.specimen[aria-pressed="true"] {{ color: var(--signal); }}
.specimen .num {{ color: var(--muted); font: var(--mono)/1 var(--utility-font); }}
.specimen .title {{ font-size: 1.1rem; }}
.specimen .arrow {{ text-align: right; }}
.proof {{ padding: 72px 0; border-bottom: 1px solid var(--line); }}
.eyebrow {{ margin: 0 0 20px; color: var(--muted); font: 700 var(--mono)/1 var(--utility-font); letter-spacing: .1em; text-transform: uppercase; }}
h2 {{ max-width: 14ch; margin: 0; font-family: var(--display-font); font-size: clamp(2rem, 4.8vw, 4.6rem); font-weight: 500; line-height: .92; letter-spacing: -.055em; }}
.proof-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; margin-top: 38px; border: 1px solid var(--line); background: var(--line); }}
.proof-item {{ min-height: 150px; padding: 16px; background: var(--surface); }}
.proof-item b {{ display: block; margin-top: 52px; font-size: 1.05rem; }}
.proof-item span {{ color: var(--muted); font: var(--mono)/1.4 var(--utility-font); }}
.signature {{ display: grid; grid-template-columns: minmax(0, .75fr) minmax(0, 1.25fr); gap: var(--gutter); padding: 72px 0; border-bottom: 1px solid var(--line); }}
.cue {{ display: block; width: 100%; min-height: 44px; padding: 13px 0; border: 0; border-bottom: 1px solid var(--line); background: transparent; text-align: left; font: var(--mono)/1.3 var(--utility-font); cursor: pointer; }}
.cue[aria-pressed="true"] {{ color: var(--signal); }}
.readout {{ min-height: 190px; padding: 24px; border: 1px solid var(--ink); background: var(--surface); }}
.readout strong {{ display: block; font-family: var(--display-font); font-size: clamp(2rem, 5vw, 4rem); line-height: .9; }}
.readout p {{ max-width: 48ch; color: var(--muted); line-height: 1.55; }}
.close {{ padding: 72px 0 96px; }}
.close h2 {{ max-width: 16ch; }}
.foot {{ display: flex; justify-content: space-between; gap: 20px; padding: 18px 0 28px; border-top: 1px solid var(--line); color: var(--muted); font: var(--mono)/1.4 var(--utility-font); }}
@media (max-width: 760px) {{
  .arrival, .signature {{ grid-template-columns: 1fr; }}
  .proof-grid {{ grid-template-columns: 1fr; }}
  .bar nav {{ gap: 10px; }}
  .bar nav a:nth-child(n+3) {{ display: none; }}
  .proof-item {{ min-height: 110px; }}
  .specimen-line {{ white-space: normal; overflow-wrap: anywhere; font-size: clamp(2.2rem, 11vw, 3.4rem); }}
  .type-specimen .glyph {{ font-size: clamp(5rem, 20vw, 9rem); }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ scroll-behavior: auto !important; animation-duration: .01ms !important; transition-duration: .01ms !important; }}
}}
</style>
</head>
<body class="layout-{concept.get('id', 'index')}">
<a class="skip" href="#main">skip to content</a>
<header class="shell bar"><a class="brand" href="#main" data-slot="brand">{subject}</a><nav aria-label="sections"><a href="#proof">{nav[0]}</a><a href="#signature">{nav[1]}</a><a href="#close">{nav[2]}</a></nav></header>
<main id="main">
  <section class="shell arrival" data-reveal aria-labelledby="title">
    <div><p class="kicker" data-slot="audience">{audience}</p><h1 id="title" data-slot="headline">{headline}</h1><p class="deck" data-slot="thesis">{subhead}</p><a class="act" href="#proof" data-slot="action">{cta} ↗</a></div>
    <aside class="artifact" data-artifact="{html.escape(copy['artifact'])}" aria-label="design artifact">{artifact}</aside>
  </section>
  <section class="shell proof" id="proof" data-reveal aria-labelledby="proof-title"><p class="eyebrow">evidence / 01–03</p><h2 id="proof-title" data-slot="proof-title">Three artifacts, not three feature cards.</h2><div class="proof-grid">{''.join(f'<div class="proof-item"><span>0{i+1} / {html.escape(obj)}</span><b>{html.escape(obj.title())}</b></div>' for i, obj in enumerate(objects))}</div></section>
  <section class="shell signature" id="signature" data-reveal aria-labelledby="signature-title"><div><p class="eyebrow">signature / scan to specimen</p><h2 id="signature-title" data-slot="signature-title">One input. One change.</h2><div>{options}</div></div><div class="readout" aria-live="polite"><span class="eyebrow">selected</span><strong data-readout-title>{html.escape(objects[0].title())}</strong><p data-readout-note>Replace this note with the real artifact. No invented metrics.</p></div></section>
  <section class="shell close" id="close" data-reveal><p class="eyebrow">the next move</p><h2>{cta}.</h2><a class="act" href="#main" data-slot="close-action">{copy['secondary']} ↗</a></section>
</main>
<footer class="shell foot"><span>one principle / one artifact / one action</span><span>replace the content slots before shipping</span></footer>
<script>
const cues = [...document.querySelectorAll('[data-cue]')];
const readoutTitle = document.querySelector('[data-readout-title]');
const readoutNote = document.querySelector('[data-readout-note]');
const titles = {json.dumps([obj.title() for obj in objects])};
const notes = {json.dumps([f"A real {obj} entry belongs here. Replace this note with its source, state and one honest observation." for obj in objects])};
const select = (i) => {{
  cues.forEach((cue, n) => cue.setAttribute('aria-pressed', String(n === i)));
  readoutTitle.textContent = titles[i];
  readoutNote.textContent = notes[i];
}};
cues.forEach((cue, i) => {{
  cue.setAttribute('aria-pressed', String(i === 0));
  cue.addEventListener('click', () => select(i));
  cue.addEventListener('keydown', (event) => {{
    let next = null;
    if (event.key === 'ArrowDown' || event.key === 'ArrowRight') next = (i + 1) % cues.length;
    if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') next = (i - 1 + cues.length) % cues.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = cues.length - 1;
    if (next !== null) {{ event.preventDefault(); select(next); cues[next].focus(); }}
  }});
}});
const specimenLine = document.querySelector('[data-specimen-line]');
const specimenSize = document.querySelector('[data-specimen-size]');
const specimenTracking = document.querySelector('[data-specimen-tracking]');
const syncSpecimen = () => {{
  if (!specimenLine) return;
  if (specimenSize) specimenLine.style.setProperty('--specimen-size', `${{specimenSize.value}}rem`);
  if (specimenTracking) specimenLine.style.setProperty('--specimen-tracking', `${{Number(specimenTracking.value) / 100}}em`);
}};
[specimenSize, specimenTracking].forEach((control) => control?.addEventListener('input', syncSpecimen));
syncSpecimen();
document.documentElement.classList.add('js');
const revealEls = [...document.querySelectorAll('[data-reveal]')];
const reducedReveal = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reducedReveal || !('IntersectionObserver' in window)) {{
  revealEls.forEach((element) => element.classList.add('is-in'));
}} else {{
  const revealObserver = new IntersectionObserver((entries) => {{
    entries.forEach((entry) => {{
      if (entry.isIntersecting) {{
        entry.target.classList.add('is-in');
        revealObserver.unobserve(entry.target);
      }}
    }});
  }}, {{threshold: .08, rootMargin: '0px 0px -8% 0px'}});
  revealEls.forEach((element) => revealObserver.observe(element));
  requestAnimationFrame(() => document.querySelector('.arrival')?.classList.add('is-in'));
  setTimeout(() => revealEls.forEach((element) => element.classList.add('is-in')), 2400);
}}
</script>
</body>
</html>
"""
    return {
        "files": [{"path": "index.html", "language": "html", "content": page}],
        "notes": [
            "A complete static design starter, not a content-complete website.",
            "Replace the data-slot text and the three object labels with real content.",
            "The specimen selector is real: pointer, focus and arrow keys update the same readout.",
            "No external assets, fonts, copied code or invented metrics are included.",
        ],
        "acceptance": [
            "Rendered at 1440x900 and 390x844 without horizontal overflow.",
            "Tab and arrow keys update the selected specimen and readout.",
            "Body measure stays 45–75ch.",
            "No unresolved template tokens.",
        ],
    }


def design(brief: str, audience: str = "", constraints: str = "", references: list | None = None,
           mood: str = "", stack: str = "HTML/CSS/JS", mode: str = "direction", seed: int | None = None) -> dict:
    brief = _text(brief, 2400)
    if len(brief) < 8:
        raise ValueError("brief must be at least 8 characters")
    if mode not in {"direction", "page"}:
        raise ValueError("mode must be direction or page")
    if mood and mood not in MOODS:
        raise ValueError(f"mood must be one of: {', '.join(sorted(MOODS))}")
    references = references if isinstance(references, list) else []
    domain = _pick_domain(brief)
    flags = _flags(constraints)
    mood_key = _mood_key(mood, domain, flags)
    analysis = {
        "subject": _subject(brief),
        "audience": _audience(brief, domain, audience),
        "action": _action(brief, domain),
        "domain": domain["label"],
        "domain_id": next((key for key, value in DOMAINS.items() if value is domain), "generic"),
        "objects": list(domain["objects"]),
        "constraints": constraints,
        "flags": flags,
    }
    analysis["copy"] = _domain_copy(analysis["domain_id"], brief)
    reference_results = _reference_results(references, brief, constraints)
    concepts = [_concept(archetype, domain, analysis, reference_results) for archetype in domain["archetypes"]]
    concepts.sort(key=lambda c: (-c["scores"]["overall"], c["id"]))
    chosen = concepts[0]
    system = _system(chosen, mood_key, flags)
    contract = _content_contract(brief, analysis["audience"], analysis["action"], domain)
    output = {
        "ok": True,
        "mode": mode,
        "brief": brief,
        "audience": analysis["audience"],
        "domain": domain["label"],
        "action": analysis["action"],
        "mood": mood_key,
        "stack": stack,
        "seed": seed,
        "analysis": analysis,
        "reference_map": reference_results,
        "concepts": concepts,
        "chosen": chosen,
        "system": system,
        "content_contract": contract,
        "build_contract": {
            "first_file": "index.html or the framework route for the chosen artifact",
            "build_order": [
                "Write the content contract and replace every data-slot.",
                "Set tokens and type; render the first screen without images.",
                "Build the chosen artifact at full scale; verify 390px.",
                "Implement the signature interaction with keyboard and reduced motion.",
                "Audit the result with mosaic_critique and a real browser screenshot.",
            ],
            "skills": ["mosaic-design", "frontend-design", "web-workflow", "accessibility", "web-performance-optimization"],
            "acceptance": [
                "The first screen states the promise and exposes the first real artifact.",
                "The signature interaction has pointer, keyboard and focus parity.",
                "No invented metrics, logos or testimonials.",
                "One accent, one display voice, one material.",
                "45–75ch body measure and reduced motion.",
            ],
            "open_questions": [
                "What is the real brand name and first inventory entry?",
                "Which single artifact proves the claim?",
                "What is the source, date or provenance for each record?",
            ],
        },
        "critique_prompt": {
            "run": "mosaic_critique",
            "why": "The design is a direction until it is rendered; text checks cannot prove visual accuracy.",
        },
        "note": "The tool designs a system and a starting artifact. It does not claim the reference was studied unless observations were supplied.",
    }
    if mode == "page":
        output["page"] = _page(chosen, domain, analysis, system)
    return output