"""Number the approved heading without rebuilding any other panel object.

Run: uv run --no-project --with fonttools python -B <this file>
Preserved v05 SVGs and explicit macOS Marker Felt glyphs are the inputs.
"""
from pathlib import Path
from html import escape
import copy
import hashlib
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTCollection
from fontTools.pens.svgPathPen import SVGPathPen

HERE = Path(__file__).resolve().parent
OLD = 'panel-02-production-v05-2026-10-03'
NEW = 'panel-02-production-v06-2026-10-03'
HEADING = '2. Target Market'
NS = {'s': 'http://www.w3.org/2000/svg'}


def heading_match(source, element):
    pattern = rf'<{element}\b[^>]*\bid="p2-heading"[^>]*>.*?</{element}>'
    matches = list(re.finditer(pattern, source, flags=re.DOTALL))
    assert len(matches) == 1
    return matches[0]


manifest = json.loads((HERE / (OLD + '-text-manifest.json')).read_text())
previous = copy.deepcopy(manifest)
heading = next(obj for obj in manifest['text_objects'] if obj['id'] == 'p2-heading')
font = TTCollection(heading['font_file']).fonts[heading['font_collection_index']]
glyphs, cmap, metrics = font.getGlyphSet(), font.getBestCmap(), font['hmtx'].metrics
assert all(ord(char) in cmap for char in HEADING), 'Missing explicit font glyph'
scale = heading['font_size'] / font['head'].unitsPerEm
width = sum(metrics[cmap[ord(char)]][0] for char in HEADING) * scale
x, y = heading['x'], heading['baseline_y']
assert x + width <= 555, 'Existing underline would need separate review'
parts, advance = [], 0
for char in HEADING:
    name = cmap[ord(char)]
    pen = SVGPathPen(glyphs)
    glyphs[name].draw(pen)
    if pen.getCommands():
        parts.append(f'<path d="{pen.getCommands()}" transform="translate({x + advance * scale:.6f} {y}) scale({scale:.9f} {-scale:.9f})"/>')
    advance += metrics[name][0]
common = f'id="p2-heading" data-text="{escape(HEADING, quote=True)}" data-font-file="{escape(heading["font_file"])}" data-font-index="{heading["font_collection_index"]}"'
rotation = f'rotate({heading["rotation"]} {x} {y})'
outlined = f'<g {common} fill="#1b344c" transform="{rotation}">{"".join(parts)}</g>'
native = f'<text {common} x="{x}" y="{y}" font-family="{heading["font_family"]}" font-size="{heading["font_size"]}" font-weight="{heading["font_weight"]}" font-kerning="none" text-anchor="{heading["text_anchor"]}" fill="#1b344c" transform="{rotation}">{escape(HEADING)}</text>'

checks = {'date': '2026-10-03', 'authority': ['D-056'], 'changed_object': 'p2-heading', 'heading': HEADING}
for suffix, element, replacement in (('.svg', 'g', outlined), ('-editable.svg', 'text', native)):
    source = (HERE / (OLD + suffix)).read_text()
    match = heading_match(source, element)
    revised = source[:match.start()] + replacement + source[match.end():]
    new_match = heading_match(revised, element)
    assert source[:match.start()] + source[match.end():] == revised[:new_match.start()] + revised[new_match.end():]
    assert 'id="p2-source"' not in revised
    (HERE / (NEW + suffix)).write_text(revised)
    old_root, new_root = ET.fromstring(source), ET.fromstring(revised)
    old_objects = {obj.attrib['id']: obj for obj in old_root.iter() if obj.attrib.get('data-text')}
    new_objects = {obj.attrib['id']: obj for obj in new_root.iter() if obj.attrib.get('data-text')}
    assert len(new_objects) == 30 and old_objects.keys() == new_objects.keys()
    assert all(ET.tostring(old_objects[key]) == ET.tostring(new_objects[key]) for key in old_objects if key != 'p2-heading')
    checks[suffix + '_29_other_text_objects_and_all_non_heading_bytes_unchanged'] = True

heading.update(text=HEADING, measured_advance_width=width, origin='selected specification v05; heading numbering D-056')
manifest.update(version='v06', approved_source='panel-02-selected-content-and-proposals-v05-2026-10-03.md')
manifest['authority'].append('D-056')
manifest['approved_strings']['heading'] = HEADING
manifest['illustrations']['art_file'] = NEW + '-generated-art.png'
manifest['numbering_amendment'] = {
    'baseline': OLD,
    'changed_object': 'p2-heading',
    'unchanged_text_objects': 29,
    'underline_changed': False,
    'all_other_display_bytes_unchanged': True,
    'image_approval': 'Awaiting student section 2 image review; section 1 D-068 does not approve this image.'
}
assert manifest['data'] == previous['data']
assert manifest['chart_geometry'] == previous['chart_geometry']
assert [obj for obj in manifest['text_objects'] if obj['id'] != 'p2-heading'] == [obj for obj in previous['text_objects'] if obj['id'] != 'p2-heading']
(HERE / (NEW + '-text-manifest.json')).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
shutil.copyfile(HERE / (OLD + '-generated-art.png'), HERE / (NEW + '-generated-art.png'))
art_sha = hashlib.sha256((HERE / (NEW + '-generated-art.png')).read_bytes()).hexdigest()
assert art_sha == previous['illustrations']['art_sha256']
prompt = (HERE / (OLD + '-illustration-prompt.md')).read_text().replace(OLD, NEW).replace('Reused unchanged for v05', 'Reused unchanged for v06')
(HERE / (NEW + '-illustration-prompt.md')).write_text(prompt)
for suffix, render_width, render_height in (('.png', 1800, 1360), ('-small-preview.png', 900, 680)):
    subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-w', str(render_width), '-h', str(render_height), str(HERE / (NEW + '.svg')), '-o', str(HERE / (NEW + suffix))], check=True)
checks.update(
    text_objects=30, unchanged_text_objects=29, underline_changed=False,
    heading_advance_width=width, heading_right_advance=x + width,
    explicit_font_glyphs=True, art_sha256=art_sha, original_art_bytes_unchanged=True,
    data_and_chart_geometry_unchanged=True, visible_source_attribution=False,
    counts=manifest['data']['counts'], denominator_all_residents=670389,
    selected_share_percent=40.2, zero_baseline=True,
    pill_and_count_are_separate_objects=True,
    native_image_generation_rerun=False, full_wrapper_pass_claimed=False,
    physical_a0_verified=False, section_image_approval='pending'
)
(HERE / (NEW + '-checks.json')).write_text(json.dumps(checks, ensure_ascii=False, indent=2) + '\n')
print(f'Complete PNG ready. Heading advance {width:.3f}; 29 other text objects and every other SVG byte unchanged.')
