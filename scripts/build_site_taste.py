import json
from pathlib import Path

from mosaic_data import COMPONENTS
from mosaic_invent import invent

ROOT = Path('/home/lakshaya/projects/mosaic')
BRIEFS = [
    ("A quiet onboarding for a design tool that feels like a workshop", "keyboard first, no hover-only states"),
    ("A music archive where browsing feels like tuning a radio", "calm, one signal, no infinite scroll"),
    ("A banking app where a transfer feels deliberate", "irreversible action, explicit cancel"),
]
taste = []
for brief, constraints in BRIEFS:
    data = json.loads(invent(brief, constraints, 3, 11))
    taste.append({
        "brief": brief,
        "constraints": constraints,
        "candidates": [
            {
                "name": c["name"], "input": c["input"], "physics": c["physics"],
                "feedback": c["feedback"], "metaphor": c["metaphor"],
                "forge_kind": c["forge_kind"], "overall": c["overall"],
                "scores": c["scores"], "thesis": c["thesis"],
                "state_machine": c["state_machine"],
            }
            for c in data["candidates"]
        ],
    })

(ROOT / 'site' / 'invent-samples.js').write_text(
    'window.MOSAIC_INVENT = ' + json.dumps({"briefs": taste}, ensure_ascii=False, indent=2) + ';\n'
)

gallery = [
    {"id": c["id"], "name": c["name"], "family": c["family"], "state": c["state"],
     "use_when": c["use_when"]}
    for c in COMPONENTS
]
(ROOT / 'site' / 'component-gallery.js').write_text(
    'window.MOSAIC_COMPONENTS = ' + json.dumps(gallery, ensure_ascii=False, indent=2) + ';\n'
)
print('invent bytes', (ROOT / 'site' / 'invent-samples.js').stat().st_size)
print('gallery bytes', (ROOT / 'site' / 'component-gallery.js').stat().st_size, 'components', len(gallery))
