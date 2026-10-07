"""Verify the three hand-drawn-logo substitutions against the stable v04 baseline."""

from pathlib import Path
import base64
import hashlib
import json

from PIL import Image, ImageChops

DESIGN = Path(__file__).resolve().parent
ROOT = DESIGN.parents[1]
OLD = 'panel-04-production-v04-2026-10-03'
NEW = 'panel-04-production-v05-2026-10-03'


def uri(path):
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode('ascii')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


old = json.loads((DESIGN / (OLD + '-text-manifest.json')).read_text())
new = json.loads((DESIGN / (NEW + '-text-manifest.json')).read_text())
source = ROOT / old['official_logo']
display = ROOT / new['display_logo']
old_svg = (DESIGN / (OLD + '.svg')).read_text()
new_svg = (DESIGN / (NEW + '.svg')).read_text()
before = Image.open(DESIGN / (OLD + '.png')).convert('RGB')
after = Image.open(DESIGN / (NEW + '.png')).convert('RGB')
asset = Image.open(display)
diff = ImageChops.difference(before, after)
outside = diff.copy()
for box in new['logo_boxes']:
    outside.paste((0, 0, 0), (box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))
red, green, blue = diff.split()
mask = ImageChops.lighter(ImageChops.lighter(red, green), blue)
pixel_count = diff.width * diff.height - mask.histogram()[0]
writing = json.loads((DESIGN / (OLD + '-writing-check.json')).read_text())
checks = {
    'three shared hand-drawn logo instances embedded': new_svg.count(uri(display)) == 3,
    'original corporate raster no longer displayed': uri(source) not in new_svg,
    'all non-logo SVG bytes identical': new_svg.replace(uri(display), uri(source)) == old_svg,
    'all nineteen text records and exact placements identical': old['text_objects'] == new['text_objects'],
    'display-copy Markdown identical': (DESIGN / (OLD + '.md')).read_bytes() == (DESIGN / (NEW + '.md')).read_bytes(),
    'cue notes geometry and data identical': old['cue_boxes'] == new['cue_boxes'],
    'all decorative art placements identical': old['sprite_placements'] == new['sprite_placements'],
    'all source mappings and proposal limits identical': all(old[key] == new[key] for key in ('internal_source_mapping', 'cue_basis', 'touchpoints', 'display_policy', 'visible_citations')),
    'all three original logo boxes and aspect-fit settings retained': all(f'x="{box["x"]}" y="{box["y"]}" width="{box["width"]}" height="{box["height"]}" preserveAspectRatio="xMidYMid meet"' in new_svg for box in new['logo_boxes']),
    'shared hand-drawn alpha preserved in embedded bytes': asset.mode == 'RGBA' and asset.getchannel('A').getextrema()[0] == 0 and digest(display) == new['display_logo_sha256'],
    'canvas dimensions retained': before.size == after.size == (1800, 1280),
    'actual pixel changes confined to the three logo boxes': outside.getbbox() is None,
    'actual logo raster appearance changed': pixel_count > 0,
    'baseline v04 PNG unchanged': digest(DESIGN / (OLD + '.png')) == 'd51fe2c06dd9a026be96644ea9b4c7e9871f3d5a874640140e9cd32c9ff0d5e5',
    '900px proof created': Image.open(DESIGN / (NEW + '-small.png')).size == (900, 640),
    'prior writing gate applicable to identical copy': all(value == 0 for value in writing['effective_base_hard_by_category'].values()),
}
result = {
    'scope': 'Three logo raster substitutions only; D-074 content retained.',
    'checks': checks, 'all_pass': all(checks.values()),
    'changed_pixels': pixel_count, 'changed_pixel_bbox_exclusive': diff.getbbox(),
    'logo_boxes': new['logo_boxes'], 'shared_logo_dimensions': asset.size,
    'shared_logo_alpha_range': asset.getchannel('A').getextrema(),
    'shared_logo_sha256': digest(display), 'new_png_sha256': digest(DESIGN / (NEW + '.png')),
    'visual_inspection': 'Complete PNG and 900px proof inspected; no overlap/clipping. Main wordmark clear; tiny touchpoint lettering requires close view.',
    'writing_gate': 'v04 result reused for byte-identical copy; no new whole-poster gate.',
    'actual_A0_tested': False, 'user_image_approval_inferred': False,
}
(DESIGN / (NEW + '-checks.json')).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['all_pass'] else 1)
