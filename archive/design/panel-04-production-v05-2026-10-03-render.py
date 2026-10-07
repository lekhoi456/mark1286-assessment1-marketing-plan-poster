"""Replace three logo rasters while preserving every other v04 SVG byte."""

from pathlib import Path
import base64
import hashlib
import json
import subprocess

DESIGN = Path(__file__).resolve().parent
ROOT = DESIGN.parents[1]
OLD = 'panel-04-production-v04-2026-10-03'
NEW = 'panel-04-production-v05-2026-10-03'
SOURCE = DESIGN / 'panel-01-production-v01-2026-10-03-logo.png'
DISPLAY = DESIGN / 'green-sm-hand-drawn-logo-v01-2026-10-03.png'


def uri(path):
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode('ascii')


original = (DESIGN / (OLD + '.svg')).read_text()
assert original.count(uri(SOURCE)) == 3
revised = original.replace(uri(SOURCE), uri(DISPLAY))
(DESIGN / (NEW + '.svg')).write_text(revised)
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-o', str(DESIGN / (NEW + '.png')), str(DESIGN / (NEW + '.svg'))], check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-w', '900', '-o', str(DESIGN / (NEW + '-small.png')), str(DESIGN / (NEW + '.svg'))], check=True)
(DESIGN / (NEW + '.md')).write_bytes((DESIGN / (OLD + '.md')).read_bytes())
manifest = json.loads((DESIGN / (OLD + '-text-manifest.json')).read_text())
manifest.update({
    'visual_authority': 'Student-directed shared hand-drawn Green SM logo revision; D-074 content retained.',
    'display_logo': str(DISPLAY.relative_to(ROOT)),
    'display_logo_sha256': hashlib.sha256(DISPLAY.read_bytes()).hexdigest(),
    'logo_treatment': 'Shared hand-drawn rendition; original corporate raster retained as provenance only.',
    'logo_boxes': [
        {'role': 'main', 'x': 90, 'y': 294, 'width': 465, 'height': 98},
        {'role': 'proposed-ad', 'x': 603, 'y': 1024, 'width': 142, 'height': 27},
        {'role': 'generic-app', 'x': 1111, 'y': 1035, 'width': 83, 'height': 18},
    ],
    'baseline': str((DESIGN / (OLD + '.svg')).relative_to(ROOT)),
    'reused_writing_gate': str((DESIGN / (OLD + '-writing-check.json')).relative_to(ROOT)),
})
(DESIGN / (NEW + '-text-manifest.json')).write_text(json.dumps(manifest, indent=2) + '\n')
print(f'Created {NEW}.png and 900px proof; only three embedded logo rasters changed.')
