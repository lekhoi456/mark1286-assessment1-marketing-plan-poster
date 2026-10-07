"""Compose the citation-free panel 4 face with retained internal source mapping."""

from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / '07_drafts/design'
PREFIX = 'panel-04-production-v02-2026-10-03'
spec = importlib.util.spec_from_file_location('hand_lettering', DESIGN / 'hand-drawn-lettering-layout-v01.py')
lettering = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lettering)
title_font = lettering.HandLettering('/System/Library/Fonts/MarkerFelt.ttc')
body_font = lettering.HandLettering('/System/Library/Fonts/Noteworthy.ttc')
art_path = DESIGN / 'panel-04-production-v01-2026-10-03-generated-art.png'
logo_path = DESIGN / 'panel-01-production-v01-2026-10-03-logo.png'
art = lettering.image_uri(art_path)
logo = lettering.image_uri(logo_path)
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1180" viewBox="0 0 1800 1180">',
         '<rect width="1800" height="1180" fill="#fffdf5"/>',
         '<path d="M29 38 Q480 30 899 38 T1763 40 Q1769 500 1758 1140 Q1340 1134 900 1142 T34 1138 Q25 580 29 38Z" fill="none" stroke="#264654" stroke-width="3"/>',
         '<path d="M39 47 Q690 41 1210 46 T1750 50" fill="none" stroke="#68c9cd" stroke-width="2"/>',
         '<path d="M81 153 Q270 147 471 153 T680 150" fill="none" stroke="#f7cc46" stroke-width="13" stroke-linecap="round" opacity=".72"/>',
         '<path d="M768 265 Q757 560 767 952" fill="none" stroke="#9db5ad" stroke-width="2" stroke-dasharray="9 12"/>']
manifest = []


def text(value, x, baseline, size, font=body_font, width=None, line_height=None, angle=0, fill='#173a47', lines_override=None):
    lines = lines_override or (font.wrap(value, size, width) if width else [value])
    assert ' '.join(lines) == value
    line_height = line_height or size * 1.48
    bounds = []
    for n, line in enumerate(lines):
        y = baseline + n * line_height
        parts.append(font.svg(line, x, y, size, fill, angle))
        bounds.append({'text': line, 'x': x, 'baseline': y, 'advance': round(font.width(line, size), 2)})
    manifest.append({'text': value, 'font_file': font.path, 'font_size': size, 'lines': bounds})


def art_item(crop, target):
    parts.append(lettering.sprite(art, crop, target))


text('Brand & Promise', 77, 128, 77, title_font, angle=-.2)
text('Global identity', 98, 240, 48, title_font)
text('Copenhagen promise', 847, 239, 48, title_font)
parts.append('<path d="M95 261 Q330 253 617 263" fill="none" stroke="#54bbc4" stroke-width="5" stroke-linecap="round" opacity=".55"/>')
parts.append('<path d="M844 261 Q1190 252 1468 263" fill="none" stroke="#54bbc4" stroke-width="5" stroke-linecap="round" opacity=".55"/>')
parts.append(f'<image href="{logo}" x="107" y="305" width="589" height="124" preserveAspectRatio="xMidYMid meet"/>')

# Original generated sprite bytes remain unchanged in the embedded plate.
art_item((515, 178, 550, 146), (91, 476, 359, 109))
text('Teal / cyan', 470, 558, 36, angle=-.35)
art_item((515, 332, 560, 154), (94, 601, 359, 111))
text('Yellow-gold', 470, 686, 36, angle=.3)
art_item((38, 58, 425, 460), (88, 750, 234, 253))
text('One brand across markets.', 347, 823, 41, width=380, line_height=65)

text('Proposed promise', 850, 310, 31, angle=-.3)
art_item((1116, 93, 416, 440), (1490, 268, 231, 243))
art_item((530, 685, 610, 185), (830, 364, 625, 238))
text('Clear terms. Local care.', 1004, 446, 54, title_font, line_height=91, angle=-.4, lines_override=['Clear terms.', 'Local care.'])
text('For self-paying Copenhagen riders who value trip control and fair treatment.', 845, 665, 39, width=790, line_height=62)
text('Danish first · English second', 849, 852, 36, width=785)
text('Same promise across campaign channels.', 849, 928, 36, width=530, line_height=61)
art_item((25, 590, 485, 360), (1425, 860, 287, 204))
art_item((1128, 637, 400, 275), (677, 520, 155, 131))
parts.append('</svg>')
svg = '\n'.join(parts)
svg_path = DESIGN / (PREFIX + '.svg')
svg_path.write_text(svg)
png_path = DESIGN / (PREFIX + '.png')
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-o', str(png_path), str(svg_path)], check=True)
(DESIGN / (PREFIX + '-text-manifest.json')).write_text(json.dumps({
    'panel': 4, 'authority': 'D-053/D-054/D-055', 'size': [1800, 1180],
    'text_objects': manifest, 'official_logo': str(logo_path.relative_to(ROOT)),
    'art_sha256': hashlib.sha256(art_path.read_bytes()).hexdigest(),
    'logo_sha256': hashlib.sha256(logo_path.read_bytes()).hexdigest(),
    'fonts_embedded': False, 'font_glyphs_are_paths': True,
    'removed_display_objects': ['(Green SM, 2026f; Green SM Denmark ApS, no date c)'],
    'internal_source_mapping': {'E-010': {'key':'green-sm-2026f','locator':'PDF p. 1'}, 'E-185': {'key':'green-sm-denmark-aps-ndc','locator':'PDF p. 1'}},
    'art_source_file': str(art_path.relative_to(ROOT)),
    'display_policy': 'poster-citation-display-policy-v01-2026-10-03.md',
}, indent=2))
print(f'Created {png_path.name}; {len(manifest)} exact controlled text objects.')
