"""Static reference families and the small base token set.

These are original abstractions from a public study of Construct Design
(https://www.tobiadonadon.com/projects/construct/design), not copied code or
assets. The families describe reusable design moves; the exact visual result
must come from the brief and the builder's own work.
"""

from __future__ import annotations

BASE_TOKENS = {
    "paper": "#faf8f2",
    "ink": "#17181a",
    "muted": "#6b6a66",
    "line": "#e7e3d8",
    "clay": "#ce4631",
    "deep": "#0c2342",
    "sky": "#38bdf8",
}

MOODS = {
    "quiet": {
        "field": "#faf8f2",
        "ink": "#17181a",
        "accent": "#ce4631",
        "deep": "#0c2342",
        "note": "Editorial paper, hairline rules, one warm accent, long silences.",
    },
    "tactile": {
        "field": "#f1ede4",
        "ink": "#17181a",
        "accent": "#e0512a",
        "deep": "#1c3a2e",
        "note": "Physical objects, contact shadows, short springs, a little grain.",
    },
    "technical": {
        "field": "#0d0d0d",
        "ink": "#f4f4f2",
        "accent": "#fd4239",
        "deep": "#38bdf8",
        "note": "Dark instrument panel, tabular numerals, thin luminous rules.",
    },
    "editorial": {
        "field": "#f2eee7",
        "ink": "#17130f",
        "accent": "#b93a26",
        "deep": "#0b1f3a",
        "note": "Serif display, warm stock, index numbers, asymmetric columns.",
    },
    "playful": {
        "field": "#fff8e7",
        "ink": "#1f1a14",
        "accent": "#e8a41f",
        "deep": "#2a52d6",
        "note": "A hand mark, bold shape, one loud colour, generous targets.",
    },
}

FAMILIES = [
    {
        "id": "paper-ink",
        "name": "Paper and ink",
        "skill": "palimpsest",
        "signature": "A neutral field, a huge tight display line, hairlines and one warm accent.",
        "use_when": "Editorial products, portfolios, libraries, thoughtful tools and any page that needs calm confidence.",
        "avoid": "Purple-to-blue gradients, glass on every surface, six accents, a card grid as the whole page.",
        "tokens": ["paper", "ink", "muted", "line", "clay", "deep"],
        "check": ["One loud line", "Body measure 45-75ch", "Hairlines at 1px", "One accent"],
    },
    {
        "id": "cards",
        "name": "Card objects",
        "skill": "palimpsest-cards",
        "signature": "Cards with edges, contact shadow and a small lift; stack or fan, never a flat grid of clones.",
        "use_when": "Collectibles, decks, saved items, layered previews, tickets and hands.",
        "avoid": "Rounded rectangles with no objecthood; ten identical glass cards.",
        "tokens": ["card-radius", "edge-light", "contact-shadow", "ambient-shadow"],
        "check": ["One dominant element per card", "Lift 4-12px", "Focus ring", "Touch has no hover-only action"],
    },
    {
        "id": "press",
        "name": "Press, hold and confirm",
        "skill": "palimpsest-press",
        "signature": "A physical state machine: contact, commitment, release and a visible consequence.",
        "use_when": "Delete, pay, publish, send, or any action that should not be a single accidental tap.",
        "avoid": "Fake progress, hold-only actions with no keyboard path, ghost timers that fire after cancel.",
        "tokens": ["press-scale", "hold-ms", "release-ms", "accent"],
        "check": ["Pointer cancel clears", "Keyboard equivalent", "Completion is announced", "Reduced motion keeps the action"],
    },
    {
        "id": "drag",
        "name": "Direct manipulation",
        "skill": "palimpsest-drag",
        "signature": "Pickup, ghost, drop target and a reversible settle; the object follows the pointer.",
        "use_when": "Sorting, kanban, moving between containers, timeline scrubbing, canvas panning.",
        "avoid": "Drag-only primary navigation, no keyboard path, dropping outside deletes silently.",
        "tokens": ["lift-scale", "ghost-offset", "drop-outline", "settle-ms"],
        "check": ["Pointer capture", "Escape cancels", "Arrow-key move", "Live announcements"],
    },
    {
        "id": "hover",
        "name": "Pointer reveal",
        "skill": "palimpsest-hover",
        "signature": "A small preview or lift that is a bonus, never the only way to reach content.",
        "use_when": "Galleries, dense indexes, previews, magnetic actions and playful cursor labels.",
        "avoid": "Hover-only prices or actions, cursor effects that cover text, per-row preview DOM.",
        "tokens": ["preview-offset", "lift-y", "reveal-ms"],
        "check": ["Focus reveals the same thing", "Touch fallback", "Viewport clamp", "Reduced motion"],
    },
    {
        "id": "select",
        "name": "Visible choice",
        "skill": "palimpsest-select",
        "signature": "Two to five options on one track, one moving indicator and a content change that stays put.",
        "use_when": "Segmented controls, tabs, filters, small pickers and view switches.",
        "avoid": "Dropdowns for three options, color-only active state, six-option pills on mobile.",
        "tokens": ["track", "indicator", "active-ink", "indicator-ms"],
        "check": ["Radio or tab semantics", "Arrow keys", "320px survives", "URL restores state"],
    },
    {
        "id": "shader",
        "name": "Atmosphere",
        "skill": "palimpsest-shader",
        "signature": "One field, one motion and a static fallback that still carries the page.",
        "use_when": "A hero material, a data field, grain, a dot globe or a single brand moment.",
        "avoid": "Rainbow palettes, bloom plus displacement plus aberration, WebGL-only content.",
        "tokens": ["field-a", "field-b", "field-scrim", "dpr-cap"],
        "check": ["Static fallback", "Paused offscreen", "Reduced motion still", "Readable text"],
    },
    {
        "id": "type",
        "name": "Type as image",
        "skill": "palimpsest-type",
        "signature": "One display voice, one body face and one utility face doing different jobs.",
        "use_when": "Heroes, wordmarks, editorial sections, labels and data-heavy surfaces.",
        "avoid": "Inter for everything, script body copy, gradient headline as the only identity.",
        "tokens": ["display", "body", "utility", "tracking-tight", "label-track"],
        "check": ["Display breaks intentionally", "Body measure", "Tabular numerals", "200% zoom"],
    },
    {
        "id": "scroll",
        "name": "Scroll as pacing",
        "skill": "palimpsest-scroll",
        "signature": "One pinned scene or reveal rhythm; the document still works without motion.",
        "use_when": "Product stories, timelines, chapters, galleries and scroll-linked demonstrations.",
        "avoid": "Scroll-jacking, 100vh hero after 100vh hero, content hidden behind animation.",
        "tokens": ["reveal-y", "reveal-ms", "pin-length", "progress-rail"],
        "check": ["Keyboard reaches every chapter", "Reduced motion in normal flow", "No horizontal overflow"],
    },
    {
        "id": "loading",
        "name": "Thinking, not spinning",
        "skill": "palimpsest-loading",
        "signature": "Named work, real steps and a slow state; shimmer is atmosphere, not the status.",
        "use_when": "Agents, long jobs, cold renders, data fetches and multi-step processes.",
        "avoid": "Fake percentages, infinite shimmer, spinner-only blank screens.",
        "tokens": ["working", "slow-after-ms", "skeleton", "shimmer-ms"],
        "check": ["Current step announced", "Slow state", "Cancel/retry", "No layout shift"],
    },
]

SKILL_BY_FAMILY = {family["id"]: family["skill"] for family in FAMILIES}
