import json
from pathlib import Path

from mosaic_forge import STACKS, forge

ROOT = Path('/home/lakshaya/projects/mosaic')
FORGE = ROOT / 'site' / 'forge'
FORGE.mkdir(parents=True, exist_ok=True)

# The live lab uses the real generated HTML cores.
for kind in ('paper-plane', 'swipe-confirm', 'download-ring', 'checklist', 'magnetic-link', 'cursor-lens'):
    out = json.loads(forge(kind, 'html', 'css', ''))
    core = next(f['content'] for f in out['files'] if f['path'] == f'{kind}.js')
    (FORGE / f'{kind}.js').write_text(core)

# The playground shows the real output for one family across every stack and motion.
samples = {}
for stack in STACKS:
    samples[stack] = {}
    for motion in ('css', 'gsap'):
        out = json.loads(forge('swipe-confirm', stack, motion, 'delete a saved board'))
        samples[stack][motion] = {
            'deps': out['deps'],
            'files': out['files'],
        }

payload = {
    'kind': 'swipe-confirm',
    'stacks': [{'id': k, 'label': v['label'], 'adapter': v['file']} for k, v in STACKS.items()],
    'samples': samples,
}
(ROOT / 'site' / 'forge-samples.js').write_text(
    'window.MOSAIC_FORGE = ' + json.dumps(payload, ensure_ascii=False, indent=2) + ';\n'
)
print('forge files', sorted(p.name for p in FORGE.iterdir()))
print('samples bytes', (ROOT / 'site' / 'forge-samples.js').stat().st_size)
