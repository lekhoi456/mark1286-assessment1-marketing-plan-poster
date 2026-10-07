"""Compose the selected branding panel with exact glyph paths and shared artwork."""

from pathlib import Path
from html import escape
import hashlib
import importlib.util
import json
import subprocess

from fontTools.pens.boundsPen import BoundsPen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREFIX = '04-candidate-v01-2026-10-04'
spec = importlib.util.spec_from_file_location('lettering', ROOT / 'archive/design/hand-drawn-lettering-layout-v01.py')
lettering = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lettering)
title = lettering.HandLettering('/System/Library/Fonts/MarkerFelt.ttc')
body = lettering.HandLettering('/System/Library/Fonts/Noteworthy.ttc')
art_path = HERE / (PREFIX + '-generated-art.png')
logo_path = HERE / 'shared-logo.png'
COPY = [
    '4. Branding & Identity',
    'GLOBAL GREEN SM IDENTITY',
    'One brand across markets.',
    'Teal / cyan · Yellow-gold',
    'COPENHAGEN PROMISE · PROPOSED · TEST WITH TARGET RIDERS',
    'Clear terms. Local care.',
    'Danish first · English second',
    'For Copenhagen’s self-paying repeat taxi riders: clear terms + a route to local help',
    'SAME LOGO · SAME PALETTE · SAME PROMISE',
    'Taxi · Green SM app · Local ad',
]
parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1400" viewBox="0 0 1800 1400">',
    '<rect width="1800" height="1400" fill="#fffdf5"/>',
    '<defs>',
    f'<image id="shared-logo" href="{lettering.image_uri(logo_path)}" width="2171" height="724"/>',
    f'<image id="illustration-sheet" href="{lettering.image_uri(art_path)}" width="2172" height="724"/>',
    '</defs>',
    '<path d="M34 38 Q470 26 900 35 T1765 38 Q1778 710 1764 1363 Q1330 1377 900 1370 T35 1365 Q23 710 34 38Z" fill="none" stroke="#264654" stroke-width="3"/>',
    '<path d="M45 49 Q870 40 1751 49" fill="none" stroke="#68c9cd" stroke-width="2" opacity=".6"/>',
    '<path d="M83 151 Q415 145 802 151" fill="none" stroke="#f7cc46" stroke-width="13" stroke-linecap="round" opacity=".74"/>',
]
texts, logos, illustrations = [], [], []


def glyph_box(line, x, baseline, size, font):
    scale, cursor, boxes = size / font.units, x, []
    for char in line:
        glyph_name = font.cmap[ord(char)]
        pen = BoundsPen(font.glyphs)
        font.glyphs[glyph_name].draw(pen)
        if pen.bounds:
            left, bottom, right, top = pen.bounds
            boxes.append([cursor + left * scale, baseline - top * scale,
                          cursor + right * scale, baseline - bottom * scale])
        cursor += font.metrics[glyph_name][0] * scale
    return [round(min(b[0] for b in boxes), 3), round(min(b[1] for b in boxes), 3),
            round(max(b[2] for b in boxes), 3), round(max(b[3] for b in boxes), 3)]


def text(value, x, baseline, size, font=body, role='master', lines=None, line_height=None):
    lines = lines or [value]
    assert ' '.join(lines) == value
    identifier = f'text-{len(texts)}'
    parts.append(f'<g id="{identifier}" data-role="{role}" aria-label="{escape(value, quote=True)}">')
    bounds = []
    for index, line in enumerate(lines):
        y = baseline + index * (line_height or size * 1.35)
        parts.append(font.svg(line, x, y, size))
        bounds.append({'text': line, 'bbox': glyph_box(line, x, y, size, font), 'baseline': y})
    parts.append('</g>')
    texts.append({'id': identifier, 'text': value, 'role': role, 'font': font.path,
                  'font_size': size, 'lines': bounds})


def centred(value, baseline, size, font=body, role='master'):
    text(value, (1800 - font.width(value, size)) / 2, baseline, size, font, role)


def logo(x, y, width, name):
    height = width * 724 / 2171
    parts.append(f'<g data-logo="{name}" transform="translate({x} {y}) scale({width / 2171})"><use href="#shared-logo"/></g>')
    logos.append({'name': name, 'bbox': [x, y, x + width, y + height]})


def sprite(crop, target, name):
    cx, cy, cw, ch = crop
    x, y, width, height = target
    parts.append(f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="{cx} {cy} {cw} {ch}" overflow="hidden" preserveAspectRatio="xMidYMid meet"><use href="#illustration-sheet"/></svg>')
    illustrations.append({'name': name, 'crop': crop, 'target': target})


text(COPY[0], 80, 127, 80, title)
text(COPY[1], 100, 225, 40, title)
logo(100, 266, 555, 'global-identity')
text(COPY[2], 848, 289, 46)
for x, colour in [(850, '#26c6cf'), (1140, '#ffd400')]:
    for index in range(5):
        y = 335 + index * 8
        parts.append(f'<path d="M{x} {y} Q{x + 120} {y - 5} {x + 240} {y + 1}" fill="none" stroke="{colour}" stroke-width="11" stroke-linecap="round" opacity=".63"/>')
text(COPY[3], 850, 420, 40)
parts.append('<path d="M90 474 Q870 483 1710 473" fill="none" stroke="#68b8bd" stroke-width="2" opacity=".6"/>')
centred(COPY[4], 542, 37, title)
for index in range(5):
    y = 598 + index * 15
    parts.append(f'<path d="M502 {y} Q890 {y - 6} 1297 {y + 1}" fill="none" stroke="#ffd400" stroke-width="18" stroke-linecap="round" opacity=".3"/>')
centred(COPY[5], 655, 86, title)
centred(COPY[6], 724, 40)
centred(COPY[7], 787, 31)
parts.append('<path d="M90 823 Q900 829 1710 822" fill="none" stroke="#68b8bd" stroke-width="2" opacity=".6"/>')
centred(COPY[8], 886, 38, title)

# The single approved touchpoint line is spaced across three equal specimens.
identifier = f'text-{len(texts)}'
parts.append(f'<g id="{identifier}" data-role="master" aria-label="{escape(COPY[9], quote=True)}">')
label_runs = [('Taxi', 350), ('·', 623), ('Green SM app', 900), ('·', 1177), ('Local ad', 1450)]
label_bounds = []
for value, centre in label_runs:
    x = centre - body.width(value, 40) / 2
    parts.append(body.svg(value, x, 943, 40))
    label_bounds.append({'text': value, 'bbox': glyph_box(value, x, 943, 40, body), 'baseline': 943})
parts.append('</g>')
texts.append({'id': identifier, 'text': COPY[9], 'role': 'master', 'font': body.path,
              'font_size': 40, 'lines': label_bounds})

sprite((0, 90, 1220, 565), (87, 1014, 526, 276), 'taxi-exterior')
sprite((1235, 10, 390, 700), (790, 968, 221, 397), 'generic-app')
sprite((1710, 30, 440, 660), (1325, 974, 250, 375), 'local-ad')

# Specimen surfaces receive the exact shared lockup and repeated selected promise.
parts.append('<path d="M261 1134 Q355 1130 448 1134 L449 1240 Q355 1244 260 1240Z" fill="#fffdf5" fill-opacity=".93"/>')
logo(274, 1137, 162, 'taxi')
text(COPY[5], 285, 1213, 21, title, 'specimen-repeat', ['Clear terms.', 'Local care.'], 24)
logo(829, 1040, 145, 'generic-app')
text(COPY[5], 837, 1161, 28, title, 'specimen-repeat', ['Clear terms.', 'Local care.'], 38)
logo(1373, 1049, 150, 'local-ad')
text(COPY[5], 1381, 1177, 30, title, 'specimen-repeat', ['Clear terms.', 'Local care.'], 40)
parts.append('</svg>')

(HERE / (PREFIX + '.svg')).write_text('\n'.join(parts), encoding='utf-8')
for suffix, options in [('.png', []), ('-small.png', ['-w', '900'])]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert', *options, '-o', str(HERE / (PREFIX + suffix)), str(HERE / (PREFIX + '.svg'))], check=True)
(HERE / (PREFIX + '-copy.md')).write_text('## Branding and Identity\n<!-- budget: 75 -->\n\n' + '\n\n'.join(COPY + [COPY[5]] * 3) + '\n', encoding='utf-8')
manifest = {'panel': 4, 'authority': 'Student approval: Chốt 4, 4 October 2026; parent exact-copy task',
            'size': [1800, 1400], 'approved_copy': COPY, 'texts': texts, 'logos': logos,
            'illustrations': illustrations, 'logo_path': 'poster/shared-logo.png',
            'logo_sha256': hashlib.sha256(logo_path.read_bytes()).hexdigest(),
            'art_sha256': hashlib.sha256(art_path.read_bytes()).hexdigest(),
            'art_alpha_preserved': True, 'glyph_paths': True, 'visible_citations': False,
            'specimens': 'Proposed identity applications; generic app is illustrative, not deployed functionality'}
(HERE / (PREFIX + '-manifest.json')).write_text(json.dumps(manifest, indent=2) + '\n')
print('Rendered:', (HERE / (PREFIX + '.png')).resolve())
