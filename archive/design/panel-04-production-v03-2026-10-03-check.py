"""Check only the numbered-heading amendment against the complete v02 baseline."""

from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops


DESIGN = Path(__file__).resolve().parent
OLD = 'panel-04-production-v02-2026-10-03'
NEW = 'panel-04-production-v03-2026-10-03'
ROOT = DESIGN.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


before = json.loads((DESIGN / (OLD + '-text-manifest.json')).read_text())
after = json.loads((DESIGN / (NEW + '-text-manifest.json')).read_text())
old_title, new_title = before['text_objects'][0], after['text_objects'][0]
old_svg = (DESIGN / (OLD + '.svg')).read_text().splitlines()
new_svg = (DESIGN / (NEW + '.svg')).read_text().splitlines()
old_heading = [line for line in old_svg if 'aria-label="Brand &amp; Promise"' in line]
new_heading = [line for line in new_svg if 'aria-label="4. Brand &amp; Promise"' in line]
old_other = [line for line in old_svg if line not in old_heading]
new_other = [line for line in new_svg if line not in new_heading]
old_group = ET.fromstring(old_heading[0])
new_group = ET.fromstring(new_heading[0])
old_glyphs = list(old_group)[1:]
new_glyphs = list(new_group)[1:]
# "4." adds two visible glyphs. Space advances the remaining glyphs unchanged.
retained_glyphs = new_glyphs[2:]
glyph_shapes_identical = len(old_glyphs) == len(retained_glyphs) and all(
    a.attrib['d'] == b.attrib['d'] for a, b in zip(old_glyphs, retained_glyphs)
)

old_pixels = Image.open(DESIGN / (OLD + '.png')).convert('RGB')
new_pixels = Image.open(DESIGN / (NEW + '.png')).convert('RGB')
diff = ImageChops.difference(old_pixels, new_pixels)
bbox = diff.getbbox()
heading_envelope = (60, 50, 700, 144)
outside = diff.copy()
outside.paste((0, 0, 0), heading_envelope)
red, green, blue = diff.split()
changed_mask = ImageChops.lighter(ImageChops.lighter(red, green), blue)
changed_pixels = diff.width * diff.height - changed_mask.histogram()[0]

old_copy = (DESIGN / (OLD + '.md')).read_text()
expected_copy = old_copy.replace('\nBrand & Promise\n', '\n4. Brand & Promise\n').replace(
    'D-053 D-054 D-055;', 'D-053 D-054 D-055 D-056 D-073;'
)
new_copy = (DESIGN / (NEW + '.md')).read_text()
heading_inside_underline = new_title['lines'][0]['x'] + new_title['lines'][0]['advance'] <= 680
checks = {
    'exact numbered heading': new_title['text'] == '4. Brand & Promise',
    'eleven controlled text objects retained': len(after['text_objects']) == 11,
    'ten non-heading strings and complete placement records identical': before['text_objects'][1:] == after['text_objects'][1:],
    'heading font file and size identical': all(old_title[key] == new_title[key] for key in ('font_file', 'font_size')),
    'heading x and baseline identical': all(old_title['lines'][0][key] == new_title['lines'][0][key] for key in ('x', 'baseline')),
    'heading rotation and ink identical': all(old_group.attrib[key] == new_group.attrib[key] for key in ('transform', 'fill')),
    'retained heading glyph shapes identical': glyph_shapes_identical,
    'heading remains inside retained underline width': heading_inside_underline,
    'all non-heading SVG bytes identical': old_other == new_other,
    'exact display-copy amendment only': new_copy == expected_copy,
    'official logo file and SHA-256 retained': before['official_logo'] == after['official_logo'] and before['logo_sha256'] == after['logo_sha256'] == digest(ROOT / after['official_logo']),
    'original generated art file and SHA-256 retained': before['art_source_file'] == after['art_source_file'] and before['art_sha256'] == after['art_sha256'] == digest(ROOT / after['art_source_file']),
    'internal E-010 E-185 source mapping identical': before['internal_source_mapping'] == after['internal_source_mapping'],
    'citation removal and display policy retained': all(before[key] == after[key] for key in ('removed_display_objects', 'display_policy')),
    'canvas dimensions identical': old_pixels.size == new_pixels.size == tuple(before['size']) == tuple(after['size']),
    'actual PNG has a visible heading difference': bbox is not None and changed_pixels > 0,
    'all changed PNG pixels confined to heading': outside.getbbox() is None,
    'glyphs are controlled paths with no font redistribution': after['font_glyphs_are_paths'] is True and after['fonts_embedded'] is False,
}
result = {
    'authority': 'D-053/D-055/D-056/D-073',
    'scope': 'Heading-only amendment; body, art and source mapping retained.',
    'checks': checks,
    'all_pass': all(checks.values()),
    'changed_pixel_count': changed_pixels,
    'changed_pixel_bbox_exclusive': bbox,
    'permitted_heading_envelope': heading_envelope,
    'new_heading_advance': new_title['lines'][0]['advance'],
    'old_png_sha256': digest(DESIGN / (OLD + '.png')),
    'new_png_sha256': digest(DESIGN / (NEW + '.png')),
    'physical_A0_tested': False,
    'whole_poster_gate_run': False,
    'user_image_approval_inferred': False,
}
(DESIGN / (NEW + '-checks.json')).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['all_pass'] else 1)
