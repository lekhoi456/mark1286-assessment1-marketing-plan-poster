"""Render the controlled Section 10 v02 growth map."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess
from PIL import Image

HERE = Path(__file__).resolve().parent
PREFIX = '10-v02'
COPY = HERE / f'{PREFIX}-copy.md'
ART = HERE / f'{PREFIX}-art.png'
GLYPHS = HERE / f'{PREFIX}-glyphs.swift'
SPEC = importlib.util.spec_from_file_location('section10_v02_layout', HERE / f'{PREFIX}-layout.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
W, H = 2400, 1800
LAYOUT = MODULE.Layout(W, H, GLYPHS)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
clean = re.sub(r'<!--.*?-->', '', COPY.read_text(), flags=re.S)
strings = [re.sub(r'^#+\s*', '', block.strip()).replace('**', '').strip()
           for block in clean.split('\n\n') if block.strip()]
assert len(strings) == 21, (len(strings), strings)
assert strings[0] == '10. Business Goals & Growth'

LAYOUT.frame('outer-pen-frame', 30, 30, W-60, H-60, stroke=MODULE.INK, thick=2.8)
LAYOUT.text(strings[0], 82, 133, size=91, font='MarkerFelt-Thin', role='heading')
LAYOUT.rule(86, 164, 1510, colour='#f6d452', thick=9)
LAYOUT.text(strings[1], 86, 214, size=38, font='Noteworthy-Light', role='proposal-status')
LAYOUT.text(strings[2], 86, 273, size=38, font='MarkerFelt-Thin', role='budget-gate')

LAYOUT.frame('company-foundation-band', 78, 292, 2244, 164, fill='#f0fbf8', stroke='#83afb1', thick=2.5)
LAYOUT.text(strings[3], 112, 355, size=34, font='Noteworthy-Light', width=2160,
            role='company-foundation')

uri = ART.name
im = Image.open(ART)
placements = []
def sprite(key, source, target):
    sx, sy, sw, sh = source
    x, y, w, h = target
    clip = key + '-source-clip'
    LAYOUT.parts.extend([
        f'<svg id="{key}" x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{sx} {sy} {sw} {sh}" preserveAspectRatio="xMidYMid meet" overflow="hidden">',
        f'<defs><clipPath id="{clip}" clipPathUnits="userSpaceOnUse"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}"/></clipPath></defs>',
        f'<g clip-path="url(#{clip})"><image href="{uri}" x="0" y="0" width="{im.width}" height="{im.height}"/></g></svg>'
    ])
    placements.append({'id': key, 'source': source, 'target': target,
                      'role': 'reused conceptual artwork; not a local result'})

cards = [
    {'x': 80, 'title': 4, 'body': [5, 6, 7], 'art': [0, 512, 768, 512], 'id': 'market-to-focus'},
    {'x': 650, 'title': 8, 'body': [9, 10], 'art': [768, 0, 768, 512], 'id': 'digital-to-trial'},
    {'x': 1220, 'title': 11, 'body': [12, 13], 'art': [0, 0, 768, 512], 'id': 'service-to-repeat'},
    {'x': 1790, 'title': 14, 'body': [15, 16, 17], 'art': [768, 512, 768, 512], 'id': 'evidence-to-growth'},
]
def paragraph(index, x, baseline, size, width, role, owner):
    end = LAYOUT.text(strings[index], x, baseline, size=size, font='Noteworthy-Light',
                      width=width, role=role, owner=owner)
    return end + size * 1.42

for card in cards:
    x, y, w, h = card['x'], 500, 530, 765
    key = card['id']
    LAYOUT.frame(f'{key}-frame', x, y, w, h, fill='#fffefb', stroke='#88aaad', thick=2.3)
    LAYOUT.text(strings[card['title']], x+27, y+55, size=36, font='MarkerFelt-Thin',
                width=w-52, role='growth-stage', owner=key)
    sprite(key+'-art', card['art'], [x+94, y+76, 342, 228])
    LAYOUT.rule(x+28, y+316, w-56, colour='#b9e8e6', thick=7)
    text_x = x + 32
    cursor = y + 375
    if key == 'market-to-focus':
        cursor = paragraph(5, text_x, cursor, 32, 466, 'audience', key)
        cursor = paragraph(6, text_x, cursor + 1, 30, 466, 'local-evidence', key)
        paragraph(7, text_x, cursor + 2, 31, 466, 'positioning-promise', key)
    elif key == 'digital-to-trial':
        cursor = paragraph(9, text_x, cursor, 33, 466, 'acquisition-route', key)
        paragraph(10, text_x, cursor + 1, 32, 466, 'sale-and-target', key)
    elif key == 'service-to-repeat':
        cursor = paragraph(12, text_x, cursor, 33, 466, 'service-target', key)
        paragraph(13, text_x, cursor + 1, 32, 466, 'feedback-to-repeat', key)
    else:
        cursor = paragraph(15, text_x, cursor, 31, 466, 'proposed-outcome-targets', key)
        cursor = paragraph(16, text_x, cursor + 1, 29, 466, 'service-gates', key)
        paragraph(17, text_x, cursor + 1, 30, 466, 'scale-condition', key)

for arrow_x in [616, 1186, 1756]:
    LAYOUT.parts.append(f'<path d="M{arrow_x} 886 Q{arrow_x+17} 880 {arrow_x+33} 886 M{arrow_x+23} 876 L{arrow_x+34} 886 L{arrow_x+23} 896" fill="none" stroke="#4f9aa0" stroke-width="3.1" stroke-linecap="round" stroke-linejoin="round"/>')

LAYOUT.frame('conditional-innovation-band', 78, 1300, 2244, 190, fill='#f0fbf8', stroke='#83afb1', thick=2.5)
LAYOUT.text(strings[18], 112, 1375, size=32, font='Noteworthy-Light', width=2160,
            role='conditional-innovation')

LAYOUT.frame('m12-decision-band', 78, 1520, 2244, 244, fill='#fff8d8', stroke='#b4b984', thick=2.6)
LAYOUT.text(strings[19], 112, 1580, size=40, font='MarkerFelt-Thin', width=2160,
            role='m12-decision')
LAYOUT.text(strings[20], 112, 1652, size=36, font='Noteworthy-Light', width=2160,
            role='economic-limit')

svg = LAYOUT.close()
(HERE / f'{PREFIX}.svg').write_text(svg)
pdf_path = HERE.parent / '04_references' / 'konkurrence-og-forbrugerstyrelsen-2026b-uber-dantaxi-afgoerelse.pdf'
manifest = {
    'section': 10,
    'version': 'v02',
    'status': 'delegated visual candidate; parent selection pending; not group-approved',
    'copy_source': COPY.name,
    'copy_sha256': sha(COPY),
    'canvas_px': [W, H],
    'text_objects': LAYOUT.texts,
    'frames': LAYOUT.frames,
    'raster_placements': placements,
    'art_asset': ART.name,
    'art_sha256': sha(ART),
    'art_dimensions': list(im.size),
    'art_mode': im.mode,
    'art_alpha_extrema': list(im.getchannel('A').getextrema()),
    'art_origin': '10-candidate-v01-2026-10-04-generated-art.png; byte-identical reuse',
    'art_embedded': False,
    'render_source': Path(__file__).name,
    'layout_source': f'{PREFIX}-layout.py',
    'glyph_source': GLYPHS.name,
    'native_image_calls': 0,
    'citation_visible': False,
    'logo_used': False,
    'objective_mapping': {
        'market-to-focus': ['local rider evidence', 'S1', 'O1 awareness'],
        'digital-to-trial': ['O1 awareness', 'O2 paid trial', 'completed paid trip is sale'],
        'service-to-repeat': ['O4 service integrity', 'O3 repeat', 'consented feedback loop'],
        'evidence-to-growth': ['O1-O4 proposed targets', 'service gates', 'scale only after evidence'],
    },
    'cross_panel_basis': {
        'S5': 'search/social to one local information page then app booking',
        'S6': 'completed paid trip; target experience; feedback and consented repeat',
        'S7': 'DKK600,000 excluding VAT with stage gates',
        'S8': 'proposed awareness, rider, repeat and service targets',
        'S9': 'conditional AI, dispatch, connected support and bundle tests',
    },
    'internal_source_records': [{
        'key': 'konkurrence-og-forbrugerstyrelsen-2026b',
        'pdf': '../04_references/konkurrence-og-forbrugerstyrelsen-2026b-uber-dantaxi-afgoerelse.pdf',
        'physical_pages': [150, 151],
        'table': '5.12',
        'evidence_ids': ['E-024'],
        'sha256': sha(pdf_path.resolve()),
        'verification': 'Opened PDF pages 150-151; n=79 and multi-response reasons verified on 2026-10-04',
    }],
    'source_claim_boundaries': [
        'E-024 is a regional subsample, not representative and not causal',
        'Company model is a capability, not proof of Copenhagen service performance',
        'Targets are proposed, not achieved results',
        'No emissions saving, AI performance, subscription sale or Copenhagen success claimed',
        'Illustrative year-one model does not break even',
    ],
    'whole_poster_or_print_verified': False,
}
(HERE / f'{PREFIX}-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
for name, width in [(f'{PREFIX}.png', None), (f'{PREFIX}-small-preview.png', 1200)]:
    command = ['/opt/homebrew/bin/rsvg-convert']
    if width:
        command += ['-w', str(width)]
    command += ['-o', str(HERE / name), str(HERE / f'{PREFIX}.svg')]
    subprocess.run(command, check=True)
print(HERE / f'{PREFIX}.png')
