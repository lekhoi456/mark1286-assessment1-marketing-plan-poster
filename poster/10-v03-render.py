"""Render the Section 10 v03 strategy-to-growth infographic."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess

from PIL import Image

HERE = Path(__file__).resolve().parent
PREFIX = '10-v03'
COPY = HERE / f'{PREFIX}-copy.md'
GLYPHS = HERE / f'{PREFIX}-glyphs.swift'
SPEC = importlib.util.spec_from_file_location('section10_v03_layout', HERE / f'{PREFIX}-layout.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
W, H = 2400, 1800
LAYOUT = MODULE.Layout(W, H, GLYPHS)
INK, CYAN, GOLD, PAPER = MODULE.INK, MODULE.CYAN, MODULE.GOLD, MODULE.PAPER
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

clean = re.sub(r'<!--.*?-->', '', COPY.read_text(), flags=re.S)
strings = [re.sub(r'^#+\s*', '', block.strip()).replace('**', '').strip()
           for block in clean.split('\n\n') if block.strip()]
assert strings[0] == '10. Business Goals & Growth', strings[0]
assert len(strings) == 22, (len(strings), strings)

LAYOUT.frame('outer-pen-frame', 30, 30, W-60, H-60, stroke=INK, thick=2.8)
LAYOUT.text(strings[0], 82, 132, size=88, font='MarkerFelt-Thin', role='heading')
LAYOUT.rule(86, 164, 1510, colour='#f6d452', thick=9)
LAYOUT.text(strings[1], 86, 220, size=38, font='Noteworthy-Light', role='proposal-status')

LAYOUT.frame('mobility-foundation-band', 78, 280, 2244, 190,
             fill='#f0fbf8', stroke='#83afb1', thick=2.5)
LAYOUT.text(strings[2], 116, 342, size=36, font='MarkerFelt-Thin',
            role='company-strength')
LAYOUT.text(strings[3], 116, 394, size=29, font='Noteworthy-Light', width=2150,
            role='local-promise-and-limit')

# One continuous route carries the argument; four open stations mark its outcomes.
LAYOUT.text(strings[4], 116, 548, size=30, font='MarkerFelt-Thin',
            role='strategy-route-heading')
route = 'M315 660 C440 635 510 685 675 660 S930 635 1070 660 S1330 685 1470 660 S1760 635 2070 660'
LAYOUT.line(route, colour='#8dcfce', width=8)

stations = [
    {'cx': 315, 'x': 88, 'icon': 'consideration', 'heading': 5, 'metric': 6, 'body': 7,
     'id': 'local-consideration'},
    {'cx': 895, 'x': 665, 'icon': 'trial', 'heading': 8, 'metric': 9, 'body': 10,
     'id': 'paid-trial'},
    {'cx': 1475, 'x': 1240, 'icon': 'service', 'heading': 11, 'metric': 12, 'body': 13,
     'id': 'stable-service'},
    {'cx': 2055, 'x': 1815, 'icon': 'repeat', 'heading': 14, 'metric': 15, 'body': 16,
     'id': 'repeat-growth'},
]
for index, station in enumerate(stations):
    cx, sid = station['cx'], station['id']
    LAYOUT.parts.append(f'<circle cx="{cx}" cy="660" r="58" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>')
    LAYOUT.parts.append(f'<circle cx="{cx}" cy="660" r="47" fill="#f0fbf8" stroke="{CYAN}" stroke-width="3"/>')
    LAYOUT.station_icon(station['icon'], cx, 660)
    LAYOUT.text(strings[station['heading']], station['x'], 796, size=29,
                font='MarkerFelt-Thin', width=470, role='business-objective', owner=sid)
    metric_size = 72 if index != 2 else 50
    LAYOUT.text(strings[station['metric']], station['x'], 905, size=metric_size,
                font='MarkerFelt-Thin', width=480,
                role='service-gate' if index == 2 else 'proposed-target', owner=sid)
    body_y = 970
    LAYOUT.text(strings[station['body']], station['x'], body_y, size=30,
                font='Noteworthy-Light', width=465, role='target-explanation', owner=sid)

# Hand-drawn arrowheads keep each transition readable at poster distance.
for x in [600, 1180, 1760]:
    LAYOUT.line(f'M{x} 660 l-20 -13 M{x} 660 l-20 13', colour='#4f9aa0', width=4)

LAYOUT.frame('business-outcome-band', 78, 1190, 2244, 195,
             fill='#fff8d8', stroke='#b4b984', thick=2.6)
LAYOUT.text(strings[17], 116, 1250, size=25, font='MarkerFelt-Thin',
            role='business-outcome-label')
LAYOUT.text(strings[18], 116, 1325, size=37, font='MarkerFelt-Thin', width=2140,
            role='business-outcome')

LAYOUT.text(strings[19], 116, 1480, size=40, font='MarkerFelt-Thin', width=2140,
            role='m12-decision')
LAYOUT.text(strings[20], 116, 1560, size=30, font='Noteworthy-Light', width=2140,
            role='m12-review-basis')
LAYOUT.text(strings[21], 116, 1680, size=29, font='Noteworthy-Light', width=2140,
            role='economic-limit')

svg = LAYOUT.close()
(HERE / f'{PREFIX}.svg').write_text(svg)
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-o', str(HERE / f'{PREFIX}.png'),
                str(HERE / f'{PREFIX}.svg')], check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-w', '1200', '-o',
                str(HERE / f'{PREFIX}-small-preview.png'), str(HERE / f'{PREFIX}.svg')], check=True)

manifest = {
    'section': 10,
    'version': 'v03',
    'status': 'Student-accepted Section 10 v03 text and artwork on 4 October 2026; use for assembly; group approval and A0/print acceptance unverified',
    'copy_source': COPY.name,
    'copy_sha256': sha(COPY),
    'canvas_px': [W, H],
    'text_objects': LAYOUT.texts,
    'frames': LAYOUT.frames,
    'art_asset': None,
    'render_source': Path(__file__).name,
    'layout_source': f'{PREFIX}-layout.py',
    'glyph_source': GLYPHS.name,
    'native_image_calls': 0,
    'citation_visible': False,
    'logo_used': False,
    'objective_mapping': {
        'local-consideration': 'become known in the Copenhagen market',
        'paid-trial': 'turn awareness into first paid riders',
        'stable-service': 'protect stable local operation through service and mature-repeat gates',
        'repeat-growth': 'use mature 90-day repeat as the long-term growth test',
        'business-outcome': 'retention sets the growth test; stable operation supports sustainable growth',
    },
    'source_claim_boundaries': [
        'Targets are proposed, not achieved results',
        'Green, smart and sustainable mobility are company strengths; local performance is not established here',
        'The controlled fleet/driver model is framed as a proposed capability that may support the promise',
        'No customer demand, emissions saving or Copenhagen service outcome is claimed',
        'The illustrative year-one model does not break even',
    ],
    'cross_panel_basis': {
        'S6': 'completed, paid first trip defines a sale',
        'S7': 'capped market-entry spend and non-break-even illustrative model',
        'S8': 'proposed consideration, rider, repeat and service targets',
        'integrated-plan-12': 'business-objective alignment and sustainable-growth rationale',
    },
    'whole_poster_or_print_verified': False,
}
(HERE / f'{PREFIX}-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(HERE / f'{PREFIX}.png')
