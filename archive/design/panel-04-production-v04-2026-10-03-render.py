"""Compose the selected evidence-to-promise infographic with controlled lettering."""

from pathlib import Path
from html import escape
import hashlib
import importlib.util
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / '07_drafts/design'
PREFIX = 'panel-04-production-v04-2026-10-03'
MASTER = DESIGN / 'panel-04-selected-content-and-visual-v03-2026-10-03.md'
spec = importlib.util.spec_from_file_location('hand_lettering', DESIGN / 'hand-drawn-lettering-layout-v01.py')
lettering = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lettering)
title = lettering.HandLettering('/System/Library/Fonts/MarkerFelt.ttc')
body = lettering.HandLettering('/System/Library/Fonts/Noteworthy.ttc')
old_art_path = DESIGN / 'panel-04-production-v01-2026-10-03-generated-art.png'
art_path = DESIGN / (PREFIX + '-generated-art-corrected.png')
logo_path = DESIGN / 'panel-01-production-v01-2026-10-03-logo.png'
old_art, art, logo = map(lettering.image_uri, (old_art_path, art_path, logo_path))
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1280" viewBox="0 0 1800 1280">',
         '<rect width="1800" height="1280" fill="#fffdf5"/>',
         '<path d="M29 38 Q480 30 899 38 T1763 40 Q1769 560 1758 1240 Q1340 1234 900 1242 T34 1238 Q25 680 29 38Z" fill="none" stroke="#264654" stroke-width="3"/>',
         '<path d="M39 47 Q690 41 1210 46 T1750 50" fill="none" stroke="#68c9cd" stroke-width="2"/>',
         '<path d="M81 153 Q270 147 471 153 T680 150" fill="none" stroke="#f7cc46" stroke-width="13" stroke-linecap="round" opacity=".72"/>']
manifest, cue_boxes, placements = [], [], []


def measure(value, size, font):
    return sum(font.width(chunk, size) for chunk in value.split('→')) + value.count('→') * size * 1.2


def text(value, x, baseline, size, font=body, width=None, line_height=None, lines=None, role='master'):
    lines = lines or (font.wrap(value, size, width) if width else [value])
    assert ' '.join(lines) == value
    line_height = line_height or size * 1.45
    bounds = []
    for index, line in enumerate(lines):
        y = baseline + index * line_height
        if '→' in line:
            # The handwriting font lacks U+2192; draw that exact approved symbol as a pen path.
            prefix, suffix = line.split('→')
            cursor = x + font.width(prefix, size)
            end = cursor + size * 1.2
            parts.append(font.svg(prefix, x, y, size))
            parts.append(f'<g aria-label="→"><title>→</title><path d="M{cursor} {y-size*.36} Q{cursor+size*.5} {y-size*.4} {end-size*.12} {y-size*.36} M{end-size*.4} {y-size*.58} L{end-size*.12} {y-size*.36} L{end-size*.4} {y-size*.14}" fill="none" stroke="#173a47" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
            parts.append(font.svg(suffix, end, y, size))
        else:
            parts.append(font.svg(line, x, y, size))
        bounds.append({'text': line, 'x': x, 'baseline': y, 'advance': round(measure(line, size, font), 2)})
    manifest.append({'text': value, 'role': role, 'font_file': font.path, 'font_size': size, 'lines': bounds})


def sprite(uri, crop, target, name, stretch=False):
    content = lettering.sprite(uri, crop, target)
    if stretch:
        content = content.replace('preserveAspectRatio="xMidYMid meet"', 'preserveAspectRatio="none"')
    parts.append(content)
    placements.append({'name': name, 'crop': crop, 'target': target})


def logo_at(x, y, width, height):
    parts.append(f'<image href="{logo}" x="{x}" y="{y}" width="{width}" height="{height}" preserveAspectRatio="xMidYMid meet"/>')


def pen_arrow(start, end):
    x, y = start
    ex, ey = end
    parts.append(f'<path d="M{x} {y} Q{(x+ex)/2} {(y+ey)/2-8} {ex} {ey} M{ex-18} {ey-12} L{ex} {ey} L{ex-18} {ey+12}" fill="none" stroke="#173a47" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


text('4. Brand & Promise', 77, 128, 77, title)
text('GLOBAL IDENTITY', 90, 237, 43, title)
text('APP-CHOICE CUES', 625, 237, 43, title)
parts.append('<path d="M90 256 Q270 250 517 258 M625 256 Q1040 250 1600 257" fill="none" stroke="#68c9cd" stroke-width="4" stroke-linecap="round"/>')
logo_at(90, 294, 465, 98)
sprite(old_art, (515, 178, 550, 146), (90, 428, 215, 55), 'cyan-swatch', True)
sprite(old_art, (515, 332, 560, 154), (324, 428, 215, 55), 'yellow-swatch', True)
text('Teal / cyan · Yellow-gold', 90, 529, 34)
text('One brand across markets.', 90, 602, 38)
pen_arrow((555, 350), (608, 350))

cue_data = [
    ('57% · Lower price', (625, 284), (45, 70, 445, 405), 'price'),
    ('22% · App used from habit', (1170, 284), (560, 55, 455, 425), 'habit'),
    ('18% · Easier app to use', (625, 440), (1120, 55, 390, 425), 'ease'),
    ('11% · Reassurance from trip visibility', (1170, 440), (40, 525, 470, 430), 'visibility'),
]
for value, (x, y), crop, name in cue_data:
    width, height = 530, 132
    cue_boxes.append({'text': value, 'x': x, 'y': y, 'width': width, 'height': height})
    parts.append(f'<path d="M{x+6} {y+8} Q{x+260} {y+2} {x+width-6} {y+8} L{x+width-2} {y+height-7} Q{x+260} {y+height-2} {x+7} {y+height-8} Z" fill="#e9f8f6" fill-opacity=".52" stroke="#68b8bd" stroke-width="2" stroke-linejoin="round"/>')
    sprite(art, crop, (x+14, y+23, 86, 86), name)
    text(value, x+118, y+52, 35, width=390, line_height=48)
text('Capital Region app-choice sample · n = 79 · multiple responses', 625, 627, 31)
sprite(old_art, (1116, 93, 416, 440), (1605, 672, 78, 83), 'small-denmark-signal')

text('CAMPAIGN RESPONSE', 90, 724, 42, title)
text('Keep the identity. Make the local promise easy to judge.', 625, 722, 37, width=1080, line_height=50)
parts.append('<path d="M1190 747 Q1186 773 1190 790 M1178 779 L1190 790 L1202 779" fill="none" stroke="#173a47" stroke-width="3" stroke-linecap="round"/>')
text('PROPOSED PROMISE · TEST WITH TARGET RIDERS', 90, 820, 34, title)
sprite(old_art, (530, 685, 610, 185), (80, 842, 1630, 121), 'promise-marker-ribbon', True)
tagline = 'Clear terms. Local care.'
text(tagline, (1800-title.width(tagline, 73))/2, 931, 73, title)
appeal = 'Trip control and fair treatment: appeal to test.'
text(appeal, (1800-body.width(appeal, 37))/2, 989, 37)
text('Danish first · English second', 90, 1107, 32, width=380, line_height=44)

# Proposed campaign touchpoints; the blank sheet is not a tested application screen.
sprite(art, (540, 570, 465, 390), (550, 996, 245, 184), 'proposed-ad')
sprite(art, (1090, 500, 410, 490), (1070, 992, 160, 191), 'generic-app-touchpoint')
logo_at(603, 1024, 142, 27)
text(tagline, 621, 1073, 17, title, line_height=22, lines=['Clear terms.', 'Local care.'], role='touchpoint-repeat')
logo_at(1111, 1035, 83, 18)
text(tagline, 1119, 1078, 16, title, line_height=27, lines=['Clear terms.', 'Local care.'], role='touchpoint-repeat')
pen_arrow((839, 1080), (1018, 1080))
caption = 'One promise in the ad → Green SM app'
text(caption, (1800-measure(caption, 33, body))/2, 1216, 33)
parts.append('</svg>')
(DESIGN / (PREFIX + '.svg')).write_text('\n'.join(parts))
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-o', str(DESIGN / (PREFIX + '.png')), str(DESIGN / (PREFIX + '.svg'))], check=True)
approved = re.findall(r'`([^`]+)`', MASTER.read_text().split('## Selected visual route')[0])
display = [item['text'] for item in manifest if item['role'] == 'master']
assert sorted(display) == sorted(approved)
copy = '## Branding and Identity\n<!-- budget: 120 -->\n\n' + '\n\n'.join(approved) + '\n'
(DESIGN / (PREFIX + '.md')).write_text(copy)
record = {
    'panel': 4, 'authority': 'D-074', 'size': [1800, 1280], 'master': str(MASTER.relative_to(ROOT)),
    'text_objects': manifest, 'cue_boxes': cue_boxes, 'sprite_placements': placements,
    'official_logo': str(logo_path.relative_to(ROOT)), 'logo_sha256': hashlib.sha256(logo_path.read_bytes()).hexdigest(),
    'art_source_file': str(art_path.relative_to(ROOT)), 'art_sha256': hashlib.sha256(art_path.read_bytes()).hexdigest(),
    'retained_art_file': str(old_art_path.relative_to(ROOT)), 'retained_art_sha256': hashlib.sha256(old_art_path.read_bytes()).hexdigest(),
    'font_glyphs_are_paths': True, 'fonts_embedded': False, 'controlled_arrow_symbol': 'U+2192 rendered as a pen path',
    'internal_source_mapping': {'E-010': {'key': 'green-sm-2026f', 'locator': 'PDF p. 1'}, 'E-185': {'key': 'green-sm-denmark-aps-ndc', 'locator': 'PDF p. 1'}, 'E-024': {'key': 'konkurrence-og-forbrugerstyrelsen-2026b', 'locator': 'PDF pp. 150–151'}, 'E-187': {'key': 'konkurrence-og-forbrugerstyrelsen-2026b', 'locator': 'PDF pp. 150–151'}},
    'cue_basis': 'Capital Region app-choice sample; n = 79; multiple responses; separate non-cumulative reasons',
    'touchpoints': 'Illustrative proposed expression; no new app capabilities or executed creative claimed',
    'display_policy': 'poster-citation-display-policy-v01-2026-10-03.md', 'visible_citations': False,
}
(DESIGN / (PREFIX + '-text-manifest.json')).write_text(json.dumps(record, indent=2) + '\n')
print(f'Created {PREFIX}.png; {len(approved)} approved display objects plus two exact tagline repeats.')
