"""Render supplied Vingroup paths with vector pen/marker texture and place them.
Run: python3 -B <this file>. Native vector-logo exception; no raster repaint.
Only the building icon and first callout row's permitted alignment change.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import copy, hashlib, json, random, re, runpy

BASE = Path(__file__).resolve().with_name('panel-01-production-v11-2026-10-03')
OLD = BASE.with_name('panel-01-production-v10-2026-10-03')
SOURCE = Path('/Users/khoilq/Downloads/Vingroup_logo.svg')
SOURCE_HASH = '3c6531a266ac19cbe9a88e6966ac0105905bf63ccb6a99d290f71f57b71365f4'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
tag = lambda name: '{' + NS + '}' + name
rough_contours = runpy.run_path(str(Path(str(BASE)+'-pen-contour.py')))['rough_contours']
saved_source = Path(str(BASE)+'-vingroup-source.svg')
if not saved_source.exists():
    saved_source.write_bytes(SOURCE.read_bytes())
raw = saved_source.read_bytes()
assert hashlib.sha256(raw).hexdigest() == SOURCE_HASH
source = ET.fromstring(raw)
layer = next(c for c in source if c.get('id') == 'layer1')
paths = [copy.deepcopy(c) for c in layer if c.tag == tag('path')]
assert len(paths) == 15
native = ET.Element(tag('svg'), {'viewBox':source.get('viewBox'),
    'width':source.get('width'), 'height':source.get('height'),
    'role':'img', 'aria-label':'Full supplied Vingroup identity: circle, bird, five stars and VINGROUP'})
ET.SubElement(native, tag('title')).text = 'Full Vingroup logo, extracted native paths'
native_group = ET.SubElement(native, tag('g'), {'transform':layer.get('transform')})
for path in paths:
    native_group.append(copy.deepcopy(path))
ET.indent(native, space='  ')
native_file = Path(str(BASE)+'-vingroup-native-paths.svg')
native_file.write_text(ET.tostring(native, encoding='unicode')+'\n')

# Every source d/translation remains exact; overlays change surface/stroke only.
drawn = ET.Element(tag('svg'), {'viewBox':'-.25 -.25 42.359302 26.069493',
    'width':'423.59302', 'height':'260.69493', 'role':'img',
    'aria-label':'Hand-drawn full Vingroup logo', 'id':'vingroup-hand-drawn-asset'})
ET.SubElement(drawn, tag('title')).text = 'VINGROUP: complete supplied identity with pen/marker texture'
ET.SubElement(drawn, tag('desc')).text = ('Fifteen original source paths and original layer translation. '
    'Bright red VIN/circle, yellow bird/five stars, burgundy GROUP preserved. '
    'Clipped marker/pencil streaks and fine double pen contours; no retyped wordmark.')
defs = ET.SubElement(drawn, tag('defs'))
group = ET.SubElement(drawn, tag('g'), {'transform':layer.get('transform')})
palette = []
rng = random.Random(20261003)
for index, path in enumerate(paths):
    path_id = path.get('id')
    colour = re.search(r'(?:^|;)fill:(#[0-9a-fA-F]+)', path.get('style')).group(1)
    palette.append(colour)
    clip_id = 'vg-clip-'+path_id
    clip = ET.SubElement(defs, tag('clipPath'), {'id':clip_id, 'clipPathUnits':'userSpaceOnUse'})
    ET.SubElement(clip, tag('path'), {'d':path.get('d')})
    ET.SubElement(group, tag('path'), {'id':'drawn-'+path_id,
        'data-source-path':path_id, 'd':path.get('d'), 'fill':colour, 'opacity':'.95',
        'stroke':colour, 'stroke-width':'.045', 'stroke-linejoin':'round', 'stroke-linecap':'round'})
    surface = ET.SubElement(group, tag('g'), {'clip-path':'url(#'+clip_id+')',
        'data-treatment':'Clipped irregular marker bands and fine pencil hatch'})
    # Uneven translucent bands reveal individual marker passes inside exact shapes.
    y = 89.8
    while y < 117:
        y += rng.uniform(.37,.79)
        start, end = rng.uniform(-77,-72), rng.uniform(-33,-29)
        wobble = rng.uniform(-.42,.42)
        finish = y+rng.uniform(-.2,.2)
        middle = [(start+(end-start)*j/6, y+rng.uniform(-.2,.2)) for j in range(1,6)]
        stroke = f'M {start:.3f} {y:.3f} '+' '.join(f'L {x:.3f} {yy:.3f}' for x,yy in middle)+f' L {end:.3f} {finish:.3f}'
        ET.SubElement(surface, tag('path'), {'d':stroke,
            'fill':'none', 'stroke':'#FFFDF4', 'stroke-width':str(round(rng.uniform(.035,.12),3)),
            'opacity':str(round(rng.uniform(.055,.15),3)), 'stroke-linecap':'round'})
    x = -86
    while x < -27:
        x += rng.uniform(.35,.88)
        bend, end_y = rng.uniform(-.45,.45), rng.uniform(115,119)
        shade = '#FFFDF4' if rng.random() < .65 else colour
        ET.SubElement(surface, tag('path'), {'d':f'M {x:.3f} 89 Q {x+6+bend:.3f} 103 {x+12:.3f} {end_y:.3f}',
            'fill':'none', 'stroke':shade, 'stroke-width':str(round(rng.uniform(.018,.05),3)),
            'opacity':str(round(rng.uniform(.075,.19),3)), 'stroke-linecap':'round',
            'stroke-dasharray':f'{rng.uniform(.15,1.5):.3f} {rng.uniform(.1,1):.3f}'})
    # A faint second contour preserves the native silhouette while showing pen passes.
    ET.SubElement(group, tag('path'), {'d':path.get('d'), 'fill':'none', 'stroke':colour,
        'stroke-width':'.065', 'stroke-linejoin':'round', 'stroke-linecap':'round',
        'opacity':'.45', 'transform':'translate(.026 -.018)', 'data-treatment':'Second pen contour'})
    ET.SubElement(group, tag('path'), {'d':rough_contours(path.get('d'),20261003+index),
        'fill':'none', 'stroke':colour, 'stroke-width':'.085', 'opacity':'.52',
        'stroke-linejoin':'round', 'stroke-linecap':'round',
        'data-treatment':'Separate wandering pen contour; original source path unchanged'})
ET.indent(drawn, space='  ')
drawn_file = Path(str(BASE)+'-vingroup-hand-drawn.svg')
drawn_file.write_text(ET.tostring(drawn, encoding='unicode')+'\n')

root = ET.parse(Path(str(OLD)+'.svg')).getroot()
manifest = copy.deepcopy(json.loads(Path(str(OLD)+'-manifest.json').read_text()))
building = root.find('.//*[@id="background-building-icon"]')
index = list(root).index(building)
root.remove(building)
placed = copy.deepcopy(drawn)
placed.attrib.update({'id':'background-vingroup-logo', 'x':'883', 'y':'70',
    'width':'75', 'height':str(75*26.069493/42.359302), 'overflow':'visible'})
root.insert(index, placed)
label = root.find('.//*[@id="background-vingroup"]')
label.set('transform', 'translate(10 0)')
for record in manifest['visible_text']:
    if record['id'] == 'background-vingroup':
        record['x'] += 10
        record['approx_bounds'] = [[a+10,b,c+10,d] for a,b,c,d in record['approx_bounds']]
root.find(tag('desc')).text = ('D-065 replaces only the generic building with a full supplied Vingroup logo '
    'in pen/marker treatment and moves the first backing label 10 units for separation. '
    'Sixteen ordinary strings/glyphs/sizes, calendar/foundation row, eight flags and all other objects/artwork remain unchanged.')
manifest['version'] = 'v11'
manifest['approval'].append('D-065')
manifest['content_master'] = 'panel-01-selected-content-and-visual-v10-2026-10-03.md'
manifest['status'] = 'D-065 hand-drawn full Vingroup-logo preview; final imagery acceptance and physical A0 proof pending'
manifest['composition_source'] = str(Path(str(BASE)+'-compose.py').resolve())
manifest['text_editing'] = 'All sixteen strings and native glyph shapes/sizes retained; only Vingroup-backed outer placement shifts +10 x.'
manifest['background_callout_history_v10'] = copy.deepcopy(manifest['background_callout'])
manifest['background_callout']['icon_ids'] = ['background-vingroup-logo','background-calendar-icon']
manifest['background_callout']['icon_bounds'] = [[883,70,958,70+75*26.069493/42.359302],[903,138,942,176]]
manifest['background_callout'].pop('generic_building_not_vingroup_logo', None)
manifest['background_callout']['logo_amendment_authority'] = 'D-065'
manifest['background_callout']['existing_geometry_unchanged'] = 'Except approved logo replacement and first-label +10 x alignment'
provenance = {'authority':'D-065', 'source_origin':'Student-supplied SVG; not an official download or bibliographic source',
    'original_file':str(SOURCE), 'saved_original_file':str(saved_source.resolve()),
    'source_sha256':SOURCE_HASH, 'source_bytes':len(raw), 'source_copy_bytes_unchanged':True,
    'native_extraction_file':str(native_file.resolve()), 'native_layer_transform':layer.get('transform'),
    'native_path_ids':[p.get('id') for p in paths], 'native_path_count':15,
    'native_path_geometry_unchanged':True, 'full_wordmark_path_count':8, 'star_path_count':5,
    'components':['Red circular emblem','Yellow bird','Five yellow stars','Full intrinsic VINGROUP wordmark'],
    'source_colours_preserved':sorted(set(palette)), 'unused_defs_glyph_uses_omitted':True,
    'treatment':'Clipped uneven marker passes, broken pencil hatching and separate locally wandering pen contours; native d/translation retained',
    'texture_seed':20261003, 'separate_pen_contour_amplitude_source_units':.065,
    'hand_drawn_svg':str(drawn_file.resolve()), 'placed_svg_id':'background-vingroup-logo',
    'placed_rect':[883,70,75,75*26.069493/42.359302], 'caption_shift':[10,0],
    'minimum_logo_caption_gap_svg_units':17, 'imagegen_used':False, 'python_raster_repaint':False,
    'execution_strategy':'Imagegen skill native vector/logo exception',
    'background_factual_claim_source':'E-199 unchanged; graphic adds no ownership assertion'}
manifest['vingroup_hand_drawn_logo'] = provenance
ET.indent(root, space='  ')
Path(str(BASE)+'.svg').write_text(ET.tostring(root, encoding='unicode')+'\n')
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
Path(str(BASE)+'-vingroup-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
crop = copy.deepcopy(root)
crop.attrib.update({'viewBox':'54 45 1490 165','width':'2235','height':'247.5'})
Path(str(BASE)+'-header-crop.svg').write_text(ET.tostring(crop,encoding='unicode')+'\n')
print('Created full v11, header crop and reusable complete hand-drawn Vingroup paths')
