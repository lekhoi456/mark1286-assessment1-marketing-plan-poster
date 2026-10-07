"""Display four complete source previews together without changing their content."""

from pathlib import Path
import importlib.util
import json
import subprocess

from PIL import Image

HERE = Path(__file__).resolve().parent
PREFIX = 'four-panel-hand-drawn-review-v02-2026-10-03'
spec = importlib.util.spec_from_file_location('lettering', HERE / 'hand-drawn-lettering-layout-v01.py')
lettering = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lettering)
heading = lettering.HandLettering('/System/Library/Fonts/MarkerFelt.ttc')
body = lettering.HandLettering('/System/Library/Fonts/Noteworthy.ttc')
sources = [
    'panel-01-production-v03-2026-10-03.png',
    'panel-02-production-v05-2026-10-03.png',
    'panel-03-production-v03-2026-10-03.png',
    'panel-04-production-v02-2026-10-03.png',
]
labels = ['1 · Meet Green SM', '2 · Target Market', '3 · Why Green SM?', '4 · Brand & Promise']
positions = [(45, 260), (1515, 260), (45, 1510), (1515, 1510)]
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="3000" height="2740" viewBox="0 0 3000 2740">',
         '<rect width="3000" height="2740" fill="#ffffff"/>',
         heading.svg('Panels 1–4 · No visible citations', 55, 105, 72),
         body.svg('Content approved · Images for review · Separate sections, not the A0 layout', 55, 169, 35)]
manifest = []
for filename, label, (x, y) in zip(sources, labels, positions):
    path = HERE / filename
    w, h = Image.open(path).size
    scale = min(1430 / w, 1150 / h)
    rw, rh = w * scale, h * scale
    parts.append(heading.svg(label, x + 10, y - 25, 44))
    parts.append(f'<image href="{lettering.image_uri(path)}" x="{x}" y="{y}" width="{rw}" height="{rh}"/>')
    manifest.append({'panel': label, 'source': filename, 'source_size': [w, h], 'display_box': [x, y, rw, rh]})
parts.append('</svg>')
svg = HERE / (PREFIX + '.svg')
svg.write_text('\n'.join(parts))
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-o', str(HERE / (PREFIX + '.png')), str(svg)], check=True)
(HERE / (PREFIX + '-manifest.json')).write_text(json.dumps(manifest, indent=2))
print('Four source images embedded unchanged in the comparison layout.')
