"""Compose the selected About-inspired section using unchanged and new native art."""
from pathlib import Path
from html import escape
import hashlib
import importlib.util
import json
import subprocess
import math
import re
from fontTools.pens.boundsPen import BoundsPen

HERE = Path(__file__).resolve().parent
PREFIX = 'panel-03-production-v05-2026-10-03'
MASTER = 'panel-03-selected-content-and-visual-v03-2026-10-03.md'
helper = HERE / 'hand-drawn-lettering-layout-v01.py'
spec = importlib.util.spec_from_file_location('panel_3_lettering', helper)
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)
heading = layout.HandLettering('/System/Library/Fonts/MarkerFelt.ttc', 0)
body = layout.HandLettering('/System/Library/Fonts/Noteworthy.ttc', 0)
old_art = HERE / 'panel-03-production-v02-2026-10-03-generated-art.png'
new_art = HERE / f'{PREFIX}-generated-art.png'
logo = HERE / 'panel-01-production-v01-2026-10-03-logo.png'
previous = json.loads((HERE / 'panel-03-production-v04-2026-10-03-text-manifest.json').read_text())
master = (HERE / MASTER).read_text()
segments = re.findall(r'^\| (Audience|Offer|Value|Delivery) \| (.+) \|$', master, re.M)
parts, objects, placements = [], [], []

def pen(path, colour='#476a70', width=1.8, opacity=1, dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ''
    parts.append(f'<path d="{path}" fill="none" stroke="{colour}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"{extra}/>')

def letter(ident, content, x, y, size, face='body', anchor='start', width=None, lines=None, angle=0):
    font = heading if face == 'heading' else body
    lines = lines or (font.wrap(content, size, width) if width else [content])
    markup, boxes = [], []
    for index, line in enumerate(lines):
        start = x - font.width(line, size) / 2 if anchor == 'middle' else x
        baseline = y + index * (size + 9)
        markup.append(font.svg(line, start, baseline, size, angle=angle))
        cursor, scale = start, size / font.units
        for char in line:
            name = font.cmap[ord(char)]
            bounds = BoundsPen(font.glyphs)
            font.glyphs[name].draw(bounds)
            if bounds.bounds:
                l, b, r, t = bounds.bounds
                corners = [(cursor+l*scale, baseline-t*scale), (cursor+r*scale, baseline-t*scale),
                           (cursor+l*scale, baseline-b*scale), (cursor+r*scale, baseline-b*scale)]
                rad = math.radians(angle)
                for px, py in corners:
                    boxes.append((start+(px-start)*math.cos(rad)-(py-baseline)*math.sin(rad),
                                  baseline+(px-start)*math.sin(rad)+(py-baseline)*math.cos(rad)))
            cursor += font.metrics[name][0] * scale
    bbox = [min(v[0] for v in boxes), min(v[1] for v in boxes),
            max(v[0] for v in boxes), max(v[1] for v in boxes)]
    parts.append(f'<g id="{ident}" data-approved-string="{escape(content, quote=True)}">{"".join(markup)}</g>')
    objects.append({'id': ident, 'approved_string': content, 'x': x, 'y': y, 'font_px': size,
                    'font_file': font.path, 'font_index': 0, 'font_face': face, 'lines': lines,
                    'angle': angle, 'bbox': bbox, 'rendered_as': 'explicit local-font glyph outlines'})

def sprite(ident, sheet, crop, target, clip=None):
    cx, cy, cw, ch = crop
    x, y, w, h = target
    bounds = ident + '-source-bounds'
    custom = f' clip-path="url(#{clip})"' if clip else ''
    parts.append(f'<svg id="{ident}" x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{cx} {cy} {cw} {ch}" overflow="hidden" preserveAspectRatio="xMidYMid meet">'
                 f'<defs><clipPath id="{bounds}" clipPathUnits="userSpaceOnUse"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}"/></clipPath></defs>'
                 f'<g clip-path="url(#{bounds})"><use href="#{sheet}"{custom}/></g></svg>')
    placements.append({'id': ident, 'sheet': sheet, 'source_bbox': crop, 'target': target,
                       'clip': clip, 'explicit_source_rect_clip': bounds})

parts.append('<rect width="1800" height="1488" fill="#fffdf7"/>')
pen('M31 31C351 23 701 33 1060 28S1510 38 1769 30L1773 501L1769 937L1776 1467C1352 1474 819 1464 31 1470L27 996L35 531Z', '#173c4b', 2.2)
pen('M43 45L615 43L1187 49L1752 43', '#24bcc6', 2, .4)
letter('heading', '3. Why Green SM?', 70, 107, 66, 'heading', angle=-.35)
letter('subtitle', 'Positioning Strategy', 73, 149, 31, angle=.2)
pen('M76 166C182 161 358 170 527 164', '#f2cd52', 13, .58)
pen('M81 195L330 191M77 206L341 210M83 216L334 214', '#f5d45d', 18, .35)
letter('qualifier', 'Proposed position', 94, 218, 30, angle=-.4)
columns = [(73, 530), (674, 258), (1008, 335), (1412, 298)]
for (label, segment), (x, width) in zip(segments, columns):
    letter('strip-label-' + label.lower(), label, x, 264, 32, 'heading')
    letter('strip-' + label.lower(), segment, x, 307, 29, width=width)
for x in [623, 959, 1362]:
    pen(f'M{x} 334Q{x+10} 330 {x+24} 335L{x+18} 328M{x+24} 335L{x+17} 341', '#52777d', 1.7)
pen('M73 433C514 428 983 439 1730 431', '#5aa9ad', 1.3, .5)

pen('M287 518C297 471 650 468 713 510C742 587 740 782 709 844C645 878 331 873 287 835C262 768 258 584 287 518Z')
pen('M293 516C345 473 646 477 709 514M284 803C328 873 639 872 708 843', '#8fafb1', 1.1, .55)
pen('M1082 515C1132 474 1438 469 1514 510C1544 578 1540 785 1510 844C1439 878 1125 870 1082 834C1060 770 1058 580 1082 515Z')
pen('M1087 514C1141 478 1437 477 1510 514M1079 804C1138 874 1438 873 1508 844', '#b9aa70', 1.1, .55)
pen('M334 552L672 548M1132 552L1471 548', '#49b8c1', 27, .21)
letter('benefit-clear', 'Clear terms', 500, 562, 56, 'heading', 'middle', angle=-.25)
letter('benefit-care', 'Local care', 1300, 562, 56, 'heading', 'middle', angle=.15)
sprite('service-area-icon', 'old-sheet', (85, 65, 395, 293), (295, 589, 84, 72))
sprite('hours-icon', 'old-sheet', (49, 389, 261, 260), (303, 678, 72, 74))
sprite('fare-icon', 'old-sheet', (317, 370, 242, 290), (300, 760, 74, 85), 'fare-clip')
letter('service-area', 'Service area ·', 395, 640, 34)
letter('hours', 'Operating hours ·', 395, 724, 34, angle=.2)
letter('fare', 'Fare terms', 395, 807, 34, angle=-.2)
sprite('trip-reference-icon', 'old-sheet', (1055, 94, 363, 221), (1084, 590, 86, 69))
sprite('local-help-icon', 'old-sheet', (1190, 329, 299, 310), (1090, 695, 74, 78))
letter('trip-reference', 'Trip reference ·', 1190, 640, 33)
letter('local-help', 'A clear route to local help', 1190, 730, 33, lines=['A clear route', 'to local help'])
pen('M736 675C762 661 788 693 815 709M1062 675C1036 661 1003 693 955 709', '#3b6169', 2)
parts.append(f'<image id="authentic-logo" href="{layout.image_uri(logo)}" x="756" y="467" width="287" height="78" preserveAspectRatio="xMidYMid meet"/>')
letter('service-label', 'App-booked electric rides', 900, 581, 30, anchor='middle')
sprite('green-sm-focal', 'old-sheet', (500, 75, 650, 685), (766, 600, 269, 284), 'focal-clip')
letter('uber-label', 'Uber', 155, 558, 32, 'heading', 'middle', angle=-.3)
letter('bolt-label', 'Bolt', 1645, 558, 32, 'heading', 'middle', angle=.25)
sprite('uber-neutral', 'old-sheet', (45, 687, 355, 295), (78, 582, 155, 145))
sprite('bolt-neutral', 'old-sheet', (1167, 681, 337, 304), (1568, 582, 155, 145))
letter('uber-model', 'Taxi partners operate rides', 155, 767, 26, anchor='middle', lines=['Taxi partners', 'operate rides'])
letter('bolt-model', 'Taxi partners operate rides', 1645, 767, 26, anchor='middle', lines=['Taxi partners', 'operate rides'])
pen('M641 904Q649 898 657 904M641 912Q649 906 657 912', '#617f82', 1.2)
letter('ev-character', 'Generally quieter than combustion-engine vehicles', 930, 918, 28, anchor='middle')
pen('M610 975L1184 970', '#49b8c1', 18, .18)
letter('green-sm-model', 'Green SM: Owned fleet · Employed drivers', 900, 963, 34, anchor='middle')
letter('approach-heading', 'Company service approach', 900, 1044, 37, 'heading', 'middle')
sprite('trained-drivers-art', 'approach-sheet', (35, 150, 680, 550), (336, 1080, 232, 142))
sprite('standards-art', 'approach-sheet', (788, 110, 432, 582), (848, 1077, 110, 154))
sprite('procedures-art', 'approach-sheet', (1302, 180, 632, 470), (1233, 1088, 234, 145))
pen('M615 1157Q705 1150 793 1159L780 1151M793 1159L780 1167')
pen('M1009 1157Q1098 1166 1193 1159L1180 1151M1193 1159L1181 1167')
letter('trained-drivers', 'Trained drivers', 450, 1270, 31, anchor='middle')
letter('standards', 'Operational standards', 900, 1270, 31, anchor='middle')
letter('procedures', 'Customer service procedures', 1350, 1270, 30, anchor='middle', lines=['Customer service', 'procedures'])
pen('M900 1298Q909 1313 900 1349', '#6b8a8d', 1.6, .85, '5 5')
pen('M900 1349L894 1338M900 1349L907 1339', '#6b8a8d', 1.6)
pen('M106 1383C465 1378 967 1388 1680 1380', '#547a80', 1.4, .5)
letter('delivery-label', 'Delivery plan', 107, 1432, 31, 'heading')
letter('delivery-plan', 'Use direct fleet and driver control to support clear terms and local help.', 395, 1431, 31)

defs = f'<defs><image id="old-sheet" href="{layout.image_uri(old_art)}" width="1536" height="1024"/><image id="approach-sheet" href="{layout.image_uri(new_art)}" width="1942" height="809"/><clipPath id="focal-clip"><path d="M590 75H945V430L1150 480V760H506V599L598 535Z"/></clipPath><clipPath id="fare-clip"><path d="M375 370L555 390L489 658L315 625Z"/></clipPath></defs>'
svg = '<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1488" viewBox="0 0 1800 1488"><title>3. Why Green SM? Selected About-inspired revision</title>' + defs + ''.join(parts) + '</svg>'
(HERE / f'{PREFIX}.svg').write_text(svg)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
registry = json.loads((HERE.parent.parent / '04_references/references.json').read_text())
sources = []
for key, pages, evidence in [('konkurrence-og-forbrugerstyrelsen-2026b', [119, 174], ['E-019', 'E-184']), ('green-future-usa-inc-ndc', [3], ['E-200', 'E-203'])]:
    entry = next(e for e in registry['entries'] if e['key'] == key)
    pdf = HERE.parent.parent / '04_references' / entry['file']
    sources.append({'key': key, 'source_pdf': '../../04_references/' + entry['file'],
                    'physical_pages': pages, 'evidence_ids': evidence, 'sha256': sha(pdf),
                    'registry_verified_sha256': entry['verification']['pdf_text']['sha256'],
                    'accessed': entry.get('accessed'), 'organisation': entry.get('organisation'),
                    'title': entry['title'], 'url': entry.get('url')})
manifest = {'section': 'Panel 3 — 3. Why Green SM?', 'authority_master': MASTER,
            'decisions': ['D-051', 'D-055', 'D-056', 'D-072'], 'canvas_px': [1800, 1488],
            'copy_source': f'{PREFIX}.md', 'text_objects': objects, 'raster_placements': placements,
            'positioning_strip': [{'label': label, 'exact_segment': text, 'text_object_id': 'strip-'+label.lower()} for label, text in segments],
            'reconstructed_statement': ' '.join(text for label, text in segments), 'statement_words': 39,
            'source_records': sources, 'citation_visible': False, 'qualifier_occurrences': 1,
            'reused_art_asset': old_art.name, 'reused_art_sha256': sha(old_art),
            'new_art_asset': new_art.name, 'new_art_sha256': sha(new_art), 'new_art_dimensions': [1942, 809],
            'authentic_logo_source': logo.name, 'authentic_logo_sha256': sha(logo),
            'excluded_optional_caption': previous['excluded_optional_caption'],
            'local_font_files': [heading.path, body.path], 'font_rendering': 'outlined glyphs; no font fallback',
            'helper': helper.name, 'helper_sha256': sha(helper), 'render_source': Path(__file__).name,
            'new_native_image_calls': 1, 'native_output_original': '/Users/KHOILQ/.codex/generated_images/01a10052-be76-7750-8e04-af9a43fd23fe/exec-67e6a9c2-67da-4aa2-a0f1-a4d4d2571acc.png',
            'inference_boundary': 'Corporate service approach informs selected proposed Copenhagen implementation; it is not proof of completed local delivery or competitor superiority.',
            'illustration_boundaries': previous['illustration_boundaries'] + ['Generic training/checklist/support pictograms; no actual class, certification, employee or support event depicted.', 'Noise cue is general EV versus combustion-vehicle character, not an exclusive brand advantage.'],
            'plan_connector': 'Dashed pen connector from corporate approach to Delivery plan indicates selected inference.'}
(HERE / f'{PREFIX}-text-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-o', str(HERE / f'{PREFIX}.png'), str(HERE / f'{PREFIX}.svg')], check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-w', '900', '-h', '744', '-o', str(HERE / f'{PREFIX}-small-preview.png'), str(HERE / f'{PREFIX}.svg')], check=True)
print('Complete v05 PNG saved. Strip lines:', [(o['id'], len(o['lines'])) for o in objects if o['id'].startswith('strip-')])

