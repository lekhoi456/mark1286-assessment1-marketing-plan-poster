"""Draw the selected top-star/lower-bird emblem only, using supplied native paths.
Run: python3 -B <this file>. Native vector exception; no raster repaint.
Production v10 remains the exact preservation baseline for all ordinary content.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import copy, hashlib, json, random, re, runpy

BASE = Path(__file__).resolve().with_name('panel-01-production-v13-2026-10-03')
OLD = BASE.with_name('panel-01-production-v10-2026-10-03')
SOURCE = Path('/Users/khoilq/Downloads/Vingroup_logo.svg')
REFERENCE = Path('/var/folders/j7/k3hwp19s0614s73_m5cj2hn80000gn/T/codex-clipboard-d262a310-31aa-4b5e-ac09-e737c91fc43a.jpg')
SOURCE_HASH = '3c6531a266ac19cbe9a88e6966ac0105905bf63ccb6a99d290f71f57b71365f4'
REFERENCE_HASH = '2145c238eb0a94cef24849ca52323563922b6f3ab2941912ca293a27f71fb973'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
tag = lambda name: '{' + NS + '}' + name
rough_contours = runpy.run_path(str(Path(str(BASE)+'-pen-contour.py')))['rough_contours']
saved_source = Path(str(BASE)+'-vingroup-source-history.svg')
saved_reference = Path(str(BASE)+'-vingroup-updated-reference.jpg')
if not saved_source.exists(): saved_source.write_bytes(SOURCE.read_bytes())
if not saved_reference.exists(): saved_reference.write_bytes(REFERENCE.read_bytes())
assert hashlib.sha256(saved_source.read_bytes()).hexdigest() == SOURCE_HASH
assert hashlib.sha256(saved_reference.read_bytes()).hexdigest() == REFERENCE_HASH
source = ET.fromstring(saved_source.read_bytes())
layer = next(c for c in source if c.get('id') == 'layer1')
ids = ['path43790','path43792','path43794','path43796','path43798','path43800','path43802']
paths = [copy.deepcopy(next(c for c in layer if c.get('id') == key)) for key in ids]

def bounds(path):
    numbers = list(map(float,re.findall(r'[-+]?(?:\d*\.\d+|\d+)',rough_contours(path,1,0))))
    xs, ys = numbers[::2], numbers[1::2]
    return [min(xs),min(ys),max(xs),max(ys)]

centre_x, centre_y, radius = -52.71705, 100.3209, 9.197
reference_circle = [400,318,149]
factor = radius/reference_circle[2]
target = lambda x,y:(centre_x+(x-400)*factor, centre_y+(y-318)*factor)
component_transforms = {'path43790':None}
bird = paths[1]
left,top,right,bottom = bounds(bird.get('d'))
new_left,new_top = target(300,247)
new_right,new_bottom = target(447,438)
sx,sy = (new_right-new_left)/(right-left),(new_bottom-new_top)/(bottom-top)
component_transforms['path43792'] = f'matrix({sx} 0 0 {sy} {new_left-sx*left} {new_top-sy*top})'
star_targets = {'path43794':[400,201,22], 'path43796':[467,224,16],
    'path43798':[333,224,16], 'path43800':[506,268,16], 'path43802':[293,268,16]}
for path in paths[2:]:
    left,top,right,bottom = bounds(path.get('d'))
    x,y,size = star_targets[path.get('id')]
    new_x,new_y = target(x,y)
    scale = 2*size*factor/max(right-left,bottom-top)
    component_transforms[path.get('id')] = f'matrix({scale} 0 0 {scale} {new_x-scale*(left+right)/2} {new_y-scale*(top+bottom)/2})'

def asset(title):
    svg = ET.Element(tag('svg'), {'viewBox':'11.48 -.14 18.95 18.95','width':'640','height':'640',
        'role':'img','aria-label':title})
    ET.SubElement(svg,tag('title')).text = title
    return svg

native = asset('Updated Vingroup emblem only: five top stars and lower bird')
native_group = ET.SubElement(native,tag('g'),{'transform':layer.get('transform')})
for path in paths:
    part = copy.deepcopy(path)
    if component_transforms[path.get('id')]: part.set('transform',component_transforms[path.get('id')])
    native_group.append(part)
native_file = Path(str(BASE)+'-vingroup-emblem-paths.svg')
ET.indent(native,space='  ')
native_file.write_text(ET.tostring(native,encoding='unicode')+'\n')

drawn = asset('Hand-drawn Vingroup emblem only: five top stars and lower bird')
ET.SubElement(drawn,tag('desc')).text = ('Updated arrangement follows the student JPG. '
    'Seven reused native paths with component transforms; no intrinsic wordmark. '
    'Clipped wandering marker/pencil passes and separate uneven pen contours.')
defs = ET.SubElement(drawn,tag('defs'))
group = ET.SubElement(drawn,tag('g'),{'transform':layer.get('transform')})
rng = random.Random(20261003)
for index,path in enumerate(paths):
    key = path.get('id')
    colour = re.search(r'(?:^|;)fill:(#[0-9a-fA-F]+)',path.get('style')).group(1)
    transform = component_transforms[key]
    clip_id = 'vg-emblem-clip-'+key
    clip = ET.SubElement(defs,tag('clipPath'),{'id':clip_id,'clipPathUnits':'userSpaceOnUse'})
    attrs = {'d':path.get('d')}
    if transform: attrs['transform'] = transform
    ET.SubElement(clip,tag('path'),attrs)
    ET.SubElement(group,tag('path'),dict(attrs,**{'id':'drawn-'+key,'data-source-path':key,
        'fill':colour,'opacity':'.95','stroke':colour,'stroke-width':'.045',
        'stroke-linejoin':'round','stroke-linecap':'round'}))
    surface = ET.SubElement(group,tag('g'),{'clip-path':'url(#'+clip_id+')',
        'data-treatment':'Uneven marker passes and broken pencil hatch'})
    y = 90
    while y < 110:
        y += rng.uniform(.32,.7)
        start,end = rng.uniform(-64,-61),rng.uniform(-44,-41)
        points = [(start+(end-start)*j/7,y+rng.uniform(-.22,.22)) for j in range(8)]
        d = 'M '+' L '.join(f'{x:.3f} {yy:.3f}' for x,yy in points)
        ET.SubElement(surface,tag('path'),{'d':d,'fill':'none','stroke':'#FFFDF4',
            'stroke-width':str(round(rng.uniform(.035,.12),3)),
            'opacity':str(round(rng.uniform(.065,.17),3)),'stroke-linecap':'round'})
    x = -75
    while x < -39:
        x += rng.uniform(.32,.88)
        bend = rng.uniform(-.4,.4)
        ET.SubElement(surface,tag('path'),{'d':f'M {x:.3f} 90 Q {x+5+bend:.3f} 100 {x+10:.3f} 111',
            'fill':'none','stroke':'#FFFDF4','stroke-width':str(round(rng.uniform(.018,.05),3)),
            'opacity':str(round(rng.uniform(.06,.18),3)),'stroke-linecap':'round',
            'stroke-dasharray':f'{rng.uniform(.15,1.5):.3f} {rng.uniform(.1,1):.3f}'})
    contour_attrs = {'fill':'none','stroke':colour,'stroke-width':'.085','opacity':'.6',
        'stroke-linejoin':'round','stroke-linecap':'round',
        'data-treatment':'Separate wandering pen contour; native d unchanged'}
    if transform: contour_attrs['transform'] = transform
    ET.SubElement(group,tag('path'),dict(contour_attrs,d=rough_contours(path.get('d'),20261003+index)))
drawn_file = Path(str(BASE)+'-vingroup-emblem-hand-drawn.svg')
ET.indent(drawn,space='  ')
drawn_file.write_text(ET.tostring(drawn,encoding='unicode')+'\n')

root = ET.parse(Path(str(OLD)+'.svg')).getroot()
manifest = copy.deepcopy(json.loads(Path(str(OLD)+'-manifest.json').read_text()))
building = root.find('.//*[@id="background-building-icon"]')
index = list(root).index(building)
root.remove(building)
placed = copy.deepcopy(drawn)
placed.attrib.update({'id':'background-vingroup-emblem','x':'897','y':'70',
    'width':'50','height':'50','overflow':'visible'})
root.insert(index,placed)
root.find(tag('desc')).text = ('D-067 replaces the generic building with a hand-drawn emblem only: '
    'red circle, lower yellow bird and five top stars with larger centre. No intrinsic wordmark. '
    'All sixteen ordinary text objects and every unaffected v10 object/artwork remain unchanged.')
manifest['version'] = 'v13'
manifest['approval'] += ['D-065','D-066','D-067']
manifest['content_master'] = 'panel-01-selected-content-and-visual-v12-2026-10-03.md'
manifest['status'] = 'D-067 updated emblem-only preview; final imagery acceptance and physical A0 proof pending'
manifest['composition_source'] = str(Path(str(BASE)+'-compose.py').resolve())
manifest['text_editing'] = 'All sixteen ordinary string/glyph/size/position records retained exactly from v10.'
manifest['background_callout_history_v10'] = copy.deepcopy(manifest['background_callout'])
manifest['background_callout']['icon_ids'] = ['background-vingroup-emblem','background-calendar-icon']
manifest['background_callout']['icon_bounds'] = [[897,70,947,120],[903,138,942,176]]
manifest['background_callout'].pop('generic_building_not_vingroup_logo',None)
manifest['background_callout']['logo_amendment_authority'] = 'D-067'
manifest['background_callout']['existing_geometry_unchanged'] = 'Except the selected building-to-emblem substitution'
provenance = {'authority':'D-067','arrangement_authority':'D-066 student JPG',
    'source_origin':'Student-supplied identity references; no independently verified rebrand date',
    'original_svg':str(SOURCE),'saved_svg_history':str(saved_source.resolve()),'svg_sha256':SOURCE_HASH,
    'original_updated_jpg':str(REFERENCE),'saved_updated_jpg':str(saved_reference.resolve()),'jpg_sha256':REFERENCE_HASH,
    'references_copied_byte_unchanged':True,'native_source_path_ids':ids,'native_source_path_count':7,
    'source_d_paths_reused_unchanged':True,'component_transforms':component_transforms,
    'reference_circle_px':reference_circle,'reference_bird_bounds_px':[300,247,447,438],
    'reference_star_targets_px':star_targets,'source_colours':['#e32823','#f8eb00'],
    'visible_components':['Red circle','Lower yellow bird','Five yellow top stars, larger centre'],
    'intrinsic_wordmark_visible':False,'intrinsic_wordmark_paths_in_asset':0,
    'treatment':'Clipped uneven marker passes, broken pencil hatching, separate locally wandering pen contours',
    'texture_seed':20261003,'separate_pen_contour_amplitude_source_units':.065,
    'native_emblem_file':str(native_file.resolve()),'hand_drawn_emblem_file':str(drawn_file.resolve()),
    'placed_rect':[897,70,50,50],'logo_caption_gap_svg_units':18,'calendar_vertical_gap_svg_units':18,
    'imagegen_used':False,'python_raster_repaint':False,'execution_strategy':'Native vector/logo exception',
    'history':'v11 bottom-star full-wordmark attempt superseded; v12 full-wordmark production not generated before D-067'}
manifest['vingroup_hand_drawn_emblem'] = provenance
ET.indent(root,space='  ')
Path(str(BASE)+'.svg').write_text(ET.tostring(root,encoding='unicode')+'\n')
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
Path(str(BASE)+'-vingroup-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
crop = copy.deepcopy(root)
crop.attrib.update({'viewBox':'54 45 1490 165','width':'2235','height':'247.5'})
Path(str(BASE)+'-header-crop.svg').write_text(ET.tostring(crop,encoding='unicode')+'\n')
print('Created current v13 emblem-only panel/header/reusable assets')
