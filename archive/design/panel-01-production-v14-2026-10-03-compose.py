"""Replace only the header Green SM lockup with the shared transparent PNG.
Run with python3 -B. The image bytes and all other SVG objects are preserved.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import base64
import copy
import hashlib
import json

BASE = Path(__file__).resolve().with_name('panel-01-production-v14-2026-10-03')
OLD = BASE.with_name('panel-01-production-v13-2026-10-03')
SHARED = BASE.with_name('green-sm-hand-drawn-logo-v01-2026-10-03.png')
ASSET = Path(str(BASE) + '-green-sm-logo.png')
LOGO_HASH = '36a99749e3cc9585573fedda5fb1dbcf6a76483872cadc2d0f6651ec95430db9'
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
tag = lambda name: '{' + SVG + '}' + name
if not ASSET.exists():
    ASSET.write_bytes(SHARED.read_bytes())
asset_bytes = ASSET.read_bytes()
assert hashlib.sha256(asset_bytes).hexdigest() == LOGO_HASH
root = ET.parse(Path(str(OLD) + '.svg')).getroot()
logo = root.find('.//*[@id="authentic-green-sm-logo"]')
assert logo is not None
assert [logo.get(k) for k in ('x', 'y', 'width', 'height')] == ['355', '49', '433.5', '117.3']
for child in list(logo):
    logo.remove(child)
# The viewport excludes only empty transparent padding. Original PNG bytes remain embedded.
logo.set('viewBox', '18 72 2125 572')
logo.set('preserveAspectRatio', 'xMidYMid meet')
logo.set('aria-label', 'Hand-drawn Green SM mark and GREEN SM wordmark')
ET.SubElement(logo, tag('title')).text = 'Green SM hand-drawn lockup'
ET.SubElement(logo, tag('image'), {
    'id': 'green-sm-shared-hand-drawn-png', 'x': '0', 'y': '0',
    'width': '2171', 'height': '724',
    'href': 'data:image/png;base64,' + base64.b64encode(asset_bytes).decode('ascii'),
})
root.find(tag('desc')).text = (
    'Only the Green SM header lockup is replaced by the selected shared hand-drawn '
    'transparent PNG. All sixteen ordinary text objects, eight flags, callouts and '
    'app-to-car/VinFast artwork are unchanged from accepted production v13.'
)
ET.indent(root, space='  ')
Path(str(BASE) + '.svg').write_text(ET.tostring(root, encoding='unicode') + '\n')
crop = copy.deepcopy(root)
crop.attrib.update({'viewBox': '54 45 1490 165', 'width': '2235', 'height': '247.5'})
Path(str(BASE) + '-header-crop.svg').write_text(ET.tostring(crop, encoding='unicode') + '\n')
proof = copy.deepcopy(root)
proof.attrib.update({'viewBox': '340 40 460 138', 'width': '920', 'height': '276'})
Path(str(BASE) + '-logo-proof.svg').write_text(ET.tostring(proof, encoding='unicode') + '\n')
manifest = json.loads(Path(str(OLD) + '-manifest.json').read_text())
manifest['version'] = 'v14'
manifest['status'] = 'Logo-only revision of D-068 accepted v13; new image feedback and A0 proof pending'
manifest['composition_source'] = str(Path(__file__).resolve())
manifest['green_sm_original_logo_history_v13'] = copy.deepcopy(manifest['authentic_logo'])
manifest['authentic_logo'] = {
    'file': str(ASSET.resolve()), 'shared_file': str(SHARED.resolve()),
    'source_origin': 'Controller-supplied shared hand-drawn Green SM lockup',
    'source_sha256': LOGO_HASH, 'copy_bytes_unchanged': True,
    'png_dimensions': [2171, 724], 'alpha_present': True,
    'alpha_content_bounds_px': [18, 72, 2125, 572],
    'placed_rect': [355, 49, 433.5, 117.3],
    'visible_fitted_rect': [355, 49.30588235294118, 433.5, 116.68823529411765],
    'textual_equivalent': 'Green SM', 'components': ['Brand mark', 'GREEN SM wordmark'],
    'embedding': 'Original complete PNG bytes embedded in the SVG; no external asset dependency',
    'fit': 'Aspect ratio retained; viewport omits transparent-only padding',
    'alpha_retained': True, 'colour_or_raster_changes': False,
    'authority': 'Explicit student request relayed by controller on 3 October 2026',
    'not_original_pdf_paths': 'Selected hand-drawn reinterpretation replaces the original clean PDF extraction',
    'historical_identity_source_key': manifest['green_sm_original_logo_history_v13']['source_key'],
}
manifest['text_editing'] = 'All sixteen ordinary strings, glyphs, sizes and positions retained exactly from v13.'
manifest['logo_revision_scope'] = {
    'actual_green_sm_lockups_replaced': 1,
    'baseline': str(Path(str(OLD) + '.svg').resolve()),
    'unaffected_objects_unchanged': True,
    'imagegen_used': False,
    'method': 'Native editable SVG image-resource substitution; no raster repaint',
    'preservation': 'All other identities, source apparatus, text, flag geometries and artwork retained',
}
Path(str(BASE) + '-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print('Created v14 full SVG, manifest and header/logo proofs.')
