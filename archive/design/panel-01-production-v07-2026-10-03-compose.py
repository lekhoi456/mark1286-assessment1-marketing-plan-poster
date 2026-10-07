"""Compose actual native edited art and controlled VinFast wordmark paths.
Run: python3 -B <this file>. No raster repainting or image-model lettering.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import base64, copy, json

BASE = Path(__file__).resolve().with_name('panel-01-production-v07-2026-10-03')
OLD = BASE.with_name('panel-01-production-v06-2026-10-03')
NS = 'http://www.w3.org/2000/svg'; ET.register_namespace('', NS)
root = ET.parse(Path(str(OLD)+'.svg')).getroot()
manifest = copy.deepcopy(json.loads(Path(str(OLD)+'-manifest.json').read_text()))
root.remove(root.find('.//*[@id="full-vinfast-vehicle-logo"]'))
art = root.find('.//*[@id="generated-hand-drawn-decoration"]')
image = art.find('{'+NS+'}image')
raw = Path(str(BASE)+'-art-final.png').read_bytes()
image.set('href','data:image/png;base64,'+base64.b64encode(raw).decode())

# Preserve every original letter path; D-060 explicitly changes its pen treatment.
source = ET.parse(Path(str(BASE)+'-vinfast-reference.svg')).getroot()
paths = source.findall('{'+NS+'}path'); assert len(paths)==14
wordmark = ET.Element('{'+NS+'}g', {'id':'vinfast-controlled-wordmark',
    'data-logo-wordmark':'VINFAST','aria-label':'VINFAST intrinsic logo wordmark',
    'transform':'translate(965 735) scale(2.5)',
    'data-source':'Student-supplied VinFast SVG: fourteen original wordmark paths'})
ET.SubElement(wordmark,'{'+NS+'}title').text = 'VINFAST'
for p in paths:
    p = copy.deepcopy(p)
    p.attrib.update({'fill':'#143B4A','stroke':'#143B4A','stroke-width':'.045',
                    'stroke-linecap':'round','stroke-linejoin':'round','opacity':'.92'})
    wordmark.append(p)
ix = list(root).index(art); root.insert(ix+1, wordmark)
root.find('{'+NS+'}desc').text = 'D-060 panel-1 visual revision: actual native image edit puts a layered navy pen VinFast V in the middle door and one yellow bolt in the rear body above the rear wheel, with the former front badge location clean. Exact VINFAST source letter paths receive navy pen treatment below the drawn emblem. Fourteen ordinary face strings, eight flags, all other vector layout and the authentic Green SM logo are unchanged. No model lettering, caption, Vingroup or visible citation.'

generation = json.loads(Path(str(BASE)+'-generation.json').read_text())
manifest['version'] = 'v07'
manifest['approval'] = list(dict.fromkeys(manifest['approval']+['D-060']))
manifest['content_master'] = 'panel-01-selected-content-and-visual-v06-2026-10-03.md'
manifest['status'] = 'Selected D-060 hand-drawn middle-door logo/rear-bolt preview; student acceptance and physical A0 proof pending'
manifest['authentic_logo']['file'] = str(Path(str(BASE)+'-logo.svg').resolve())
manifest['generated_decoration'] = {**generation,'layout_rect':[210,610,1180,270],
    'layout_viewbox':[40,94,2110,568],'raw_postprocessing':'No raster edits; actual native PNG embedded unchanged'}
manifest['historical_v06_vehicle_logo'] = manifest.pop('vinfast_full_vehicle_logo')
manifest['historical_v06_vehicle_logo']['status'] = 'Glossy front-door treatment superseded by D-060'
manifest['vinfast_hand_drawn_logo'] = {'authority':'D-060',
    'meaning':'Complete logo: recognisable layered V emblem plus exact VINFAST wordmark',
    'source_reference':str(Path(str(BASE)+'-vinfast-reference.svg').resolve()),
    'source_sha256':'9d676729f71ddfcc6322c368ca1d446b1047fff3afc50cf847f22b5c67941f00',
    'source_origin':'Student-supplied; preserved unchanged as shape/reference authority',
    'emblem':'Actual native raster edit: navy layered V in the middle door',
    'wordmark':{'text':'VINFAST','source_path_count':14,'geometry_unchanged':True,
        'svg_id':'vinfast-controlled-wordmark','transform':'translate(965 735) scale(2.5)',
        'source_y_range_approx':[28.65,32.2444],'placed_y_range_approx':[806.625,815.611],
        'treatment':'Original source paths with flat navy fill and thin rounded pen stroke; no retyping',
        'fill':'#143B4A','stroke':'#143B4A','source_stroke_width':.045,'opacity':.92},
    'placement':'Middle/larger passenger-door body formerly containing the lightning',
    'location_interpretation':'Controller interpreted student typo as middle door; stated to student',
    'lightning':'Exactly one, moved to rear body above rear wheel; no middle-door duplicate',
    'former_front_badge_area':'Clean cyan body',
    'not_intact_3d_logo':'D-060 explicitly supersedes glossy/chrome treatment; the reference asset stays unchanged',
    'no_new_operational_claim':True}
manifest['composition_source'] = str(Path(str(BASE)+'-compose.py').resolve())
manifest['text_editing'] = 'All fourteen ordinary face glyph groups are untouched. VINFAST uses the supplied original paths, with authorised pen/marker colour treatment.'
manifest['vehicle_logo_amendment'] = {'authority':'D-060','visible_ordinary_copy_changed':False,
    'actual_native_image_edit':True,'image_model_wordmark_generated':False,
    'previous_glossy_front_logo_removed':True,'single_bolt_moved_rearwards':True}
ET.indent(root,space='  ')
Path(str(BASE)+'.svg').write_text(ET.tostring(root,encoding='unicode')+'\n')
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Created complete panel 1 with hand-drawn middle-door logo and rear bolt', BASE)
