"""Compose panel 3 with generated flat-marker art and exact local-font outlines."""

from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess


HERE = Path(__file__).resolve().parent
PREFIX = 'panel-03-production-v03-2026-10-03'
helper = HERE / 'hand-drawn-lettering-layout-v01.py'
spec = importlib.util.spec_from_file_location('panel_3_hand_lettering', helper)
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)
heading = layout.HandLettering('/System/Library/Fonts/MarkerFelt.ttc', 0)
body = layout.HandLettering('/System/Library/Fonts/Noteworthy.ttc', 0)
art_path = HERE / 'panel-03-production-v02-2026-10-03-generated-art.png'
art_uri = layout.image_uri(art_path)
logo_path = HERE / 'panel-01-production-v01-2026-10-03-logo.png'
logo_uri = layout.image_uri(logo_path)
previous = json.loads((HERE / 'panel-03-production-v02-2026-10-03-text-manifest.json').read_text())
previous['illustration_boundaries'] = [
    'Conceptual app, not a screenshot or tested feature set',
    'Generic location image, not a verified coverage map',
    'Vehicle drawing, not evidence of Danish fleet model',
    'Two fleet vehicles are symbolic, not a fleet count',
    'Driver bust is generic, not an identified Green SM employee',
    'Two small neutral-grey app/taxi islands provide rival context; colour supplies no ranking',
    'Full A0 integration and physical print not tested',
]

previous['decisions'] = ['D-050', 'D-051', 'D-055']
previous['citation_display_policy'] = 'poster-citation-display-policy-v01-2026-10-03.md'
previous['lecturer_guidance'] = 'LG-004; reported by the student'
previous['previous_production'] = 'panel-03-production-v02-2026-10-03'
previous['removed_visible_text_objects'] = [item for item in previous['text_objects'] if item['id'] == 'citation']
previous['internal_reference_entry'] = (HERE / 'panel-03-production-v02-2026-10-03.md').read_text().split('\n## References\n', 1)[1].strip()
previous['retained_visible_string_map'] = [
    {'id': item['id'], 'previous_string': item['approved_string'], 'remaining_string': item['approved_string']}
    for item in previous['text_objects'] if item['id'] != 'citation'
]
previous['citation_visible'] = False
previous['reflow_note'] = 'Footer and bottom frame shifted up 42 px to close the removed citation gap; previous descender clearance retained.'

parts, text_objects, placements = [], [], []


def letter(ident, content, x, y, size, face='body', anchor='start', lines=None, angle=0):
    """Keep exact strings editable in the manifest; draw only local-font glyphs."""
    font = heading if face == 'heading' else body
    lines = lines or [content]
    markup = []
    for index, line in enumerate(lines):
        start = x - font.width(line, size) / 2 if anchor == 'middle' else x
        markup.append(font.svg(line, start, y + index * (size + 9), size, angle=angle))
    escaped = content.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
    parts.append(f'<g id="{ident}" data-approved-string="{escaped}">{"".join(markup)}</g>')
    text_objects.append({'id': ident, 'approved_string': content, 'x': x, 'y': y,
                         'font_px': size, 'font_file': font.path, 'font_index': 0,
                         'font_face': face, 'lines': lines, 'angle': angle,
                         'rendered_as': 'explicit local-font glyph outlines'})


def image(ident, crop, target, clip=None):
    cx, cy, cw, ch = crop
    x, y, width, height = target
    attr = f' clip-path="url(#{clip})"' if clip else ''
    bounds = ident + '-source-bounds'
    parts.append(f'<svg id="{ident}" x="{x}" y="{y}" width="{width}" height="{height}" '
                 f'viewBox="{cx} {cy} {cw} {ch}" overflow="hidden" preserveAspectRatio="xMidYMid meet">'
                 f'<defs><clipPath id="{bounds}" clipPathUnits="userSpaceOnUse">'
                 f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}"/></clipPath></defs>'
                 f'<g clip-path="url(#{bounds})"><use href="#generated-sheet"{attr}/></g></svg>')
    placements.append({'id': ident, 'source_bbox': crop, 'target': target, 'clip': clip,
                       'explicit_source_rect_clip': bounds})


parts.append('<rect width="1800" height="1446" fill="#fffdf7"/>')
parts.append('<path d="M31 31C351 23 701 33 1060 28S1510 38 1769 30L1773 501L1769 937L1776 1425C1352 1432 819 1422 31 1428L27 996L35 531Z" fill="none" stroke="#173c4b" stroke-width="2.2" stroke-linecap="round"/>')
parts.append('<path d="M43 45L615 43L1187 49L1752 43" fill="none" stroke="#24bcc6" opacity=".4" stroke-width="2"/>')
letter('heading', 'Why Green SM?', 70, 107, 66, 'heading', angle=-.35)
letter('subtitle', 'Positioning Strategy', 73, 149, 31, angle=.2)
parts.append('<path d="M76 166C182 161 358 170 527 164" fill="none" stroke="#f2cd52" opacity=".58" stroke-width="13" stroke-linecap="round"/>')
parts.append('<path d="M82 199L330 195M77 209L341 213M83 219L334 217" fill="none" stroke="#f5d45d" opacity=".35" stroke-width="18" stroke-linecap="round"/>')
letter('qualifier', 'Proposed position', 94, 221, 30, angle=-.4)
statement = next(item['approved_string'] for item in previous['text_objects'] if item['id'] == 'positioning-statement')
statement_lines = body.wrap(statement, 34, 1640)
letter('positioning-statement', statement, 73, 273, 34, lines=statement_lines)
parts.append('<path d="M74 370C422 368 922 374 1730 368" fill="none" stroke="#5aa9ad" opacity=".5" stroke-width="1.3"/>')

parts.append('<path d="M79 428C98 373 447 370 522 410C567 474 552 660 505 700C436 725 126 731 83 677C54 620 46 479 79 428Z" fill="none" stroke="#476a70" stroke-width="1.8"/>')
parts.append('<path d="M85 428C120 376 430 379 517 415M78 641C110 711 421 735 505 699" fill="none" stroke="#8fafb1" opacity=".55" stroke-width="1.1"/>')
parts.append('<path d="M1291 422C1338 375 1620 379 1708 414C1749 470 1740 643 1710 687C1630 732 1340 711 1294 678C1261 624 1258 476 1291 422Z" fill="none" stroke="#476a70" stroke-width="1.8"/>')
parts.append('<path d="M1297 421C1354 380 1622 387 1704 418M1290 653C1347 709 1632 729 1706 685" fill="none" stroke="#b9aa70" opacity=".55" stroke-width="1.1"/>')
parts.append('<path d="M533 548C581 544 610 574 669 604M1259 548C1224 542 1177 578 1138 603" fill="none" stroke="#3b6169" stroke-width="1.8" stroke-linecap="round"/>')
parts.append('<path d="M157 429L435 424M1355 429L1658 425" stroke="#49b8c1" opacity=".21" stroke-width="24" stroke-linecap="round"/>')
letter('benefit-clear', 'Clear terms', 296, 435, 40, 'heading', 'middle', angle=-.25)
letter('benefit-care', 'Local care', 1501, 435, 40, 'heading', 'middle', angle=.15)
image('service-area-icon', (85, 65, 395, 293), (101, 451, 100, 92))
image('hours-icon', (49, 389, 261, 260), (101, 548, 91, 94))
image('fare-icon', (317, 370, 242, 290), (103, 643, 91, 97), 'fare-clip')
letter('service-area', 'Service area ·', 222, 512, 34)
letter('hours', 'Operating hours ·', 222, 606, 34, angle=.2)
letter('fare', 'Fare terms', 222, 699, 34, angle=-.2)
image('trip-reference-icon', (1055, 94, 363, 221), (1290, 457, 126, 87))
image('local-help-icon', (1190, 329, 299, 310), (1305, 574, 100, 97))
letter('trip-reference', 'Trip reference ·', 1434, 514, 34)
letter('local-help', 'A clear route to local help', 1434, 612, 32, lines=['A clear route', 'to local help'])
image('green-sm-focal', (500, 75, 650, 685), (575, 396, 650, 685), 'focal-clip')
parts.append(f'<image id="authentic-logo" href="{logo_uri}" x="710" y="478" width="267" height="73" preserveAspectRatio="xMidYMid meet"/>')
letter('service-label', 'App-booked electric rides', 852, 595, 39, anchor='middle', lines=['App-booked', 'electric rides'])
letter('uber-label', 'Uber', 277, 783, 37, 'heading', 'middle', angle=-.3)
letter('bolt-label', 'Bolt', 1506, 783, 37, 'heading', 'middle', angle=.25)
image('uber-neutral', (45, 687, 355, 295), (135, 811, 282, 235))
image('bolt-neutral', (1167, 681, 337, 304), (1366, 805, 278, 251))
letter('uber-model', 'Taxi partners operate rides', 277, 1095, 32, anchor='middle', lines=['Taxi partners', 'operate rides'])
letter('bolt-model', 'Taxi partners operate rides', 1506, 1095, 32, anchor='middle', lines=['Taxi partners', 'operate rides'])
parts.append('<path d="M901 1092L898 1118M794 1124C852 1117 935 1129 1000 1122M794 1122L797 1140M1000 1122L998 1138" fill="none" stroke="#173c4b" stroke-width="1.8" stroke-linecap="round"/>')
image('owned-fleet', (437, 811, 460, 160), (686, 1136, 223, 83))
image('employed-driver', (918, 759, 218, 231), (947, 1129, 104, 110))
letter('green-sm-model-label', 'Green SM', 900, 1276, 31, 'heading', 'middle')
letter('green-sm-model', 'Owned fleet · Employed drivers', 900, 1320, 38, anchor='middle')
parts.append('<path d="M106 1347C465 1342 967 1352 1680 1344" fill="none" stroke="#547a80" opacity=".5" stroke-width="1.4"/>')
letter('delivery-label', 'Delivery plan', 107, 1390, 31, 'heading')
letter('delivery-plan', 'Use direct fleet and driver control to support clear terms and local help.', 395, 1389, 31)

defs = f'<defs><image id="generated-sheet" href="{art_uri}" width="1536" height="1024"/><clipPath id="focal-clip"><path d="M590 75H945V430L1150 480V760H506V599L598 535Z"/></clipPath><clipPath id="fare-clip"><path d="M375 370L555 390L489 658L315 625Z"/></clipPath></defs>'
svg = '<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1446" viewBox="0 0 1800 1446"><title>Why Green SM? Approved hand-drawn revision</title>' + defs + ''.join(parts) + '</svg>'
(HERE / f'{PREFIX}.svg').write_text(svg)
previous.update({'copy_source': f'{PREFIX}.md', 'text_objects': text_objects, 'raster_placements': placements,
                 'art_asset': art_path.name, 'art_sha256': hashlib.sha256(art_path.read_bytes()).hexdigest(),
                 'local_font_files': [heading.path, body.path], 'font_rendering': 'outlined glyphs; no font fallback',
                 'helper': helper.name, 'helper_sha256': hashlib.sha256(helper.read_bytes()).hexdigest(),
                 'render_source': Path(__file__).name, 'revision': 'D-055 citation-only display removal; all other approved content unchanged',
                 'canvas_px': [1800, 1446]})
(HERE / f'{PREFIX}-text-manifest.json').write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-o', str(HERE / f'{PREFIX}.png'), str(HERE / f'{PREFIX}.svg')], check=True)
print('Complete handwriting-font PNG saved:', HERE / f'{PREFIX}.png')
print('Statement lines:', len(statement_lines), 'Font rendering: exact Marker Felt / Noteworthy outlines')
