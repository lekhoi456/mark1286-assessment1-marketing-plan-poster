"""Place the authentic manufacturer emblem on the preserved panel-1 drawing.
Run: python3 -B <this file>. No text regeneration or image-model call.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import copy, hashlib, json

BASE = Path(__file__).resolve().with_name('panel-01-production-v05-2026-10-03')
OLD = BASE.with_name('panel-01-production-v04-2026-10-03')
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
root = ET.parse(Path(str(OLD)+'.svg')).getroot()
manifest = copy.deepcopy(json.loads(Path(str(OLD)+'-manifest.json').read_text()))
asset_file = Path(str(BASE)+'-vinfast-emblem.svg')
badge = ET.parse(asset_file).getroot()
badge.attrib.update({'id':'authentic-vinfast-vehicle-badge','x':'872','y':'785',
                     'width':'36','height':'28.8','overflow':'hidden'})
ix = list(root).index(root.find('.//*[@id="generated-hand-drawn-decoration"]'))
root.insert(ix+1, badge)
root.find('{'+NS+'}desc').text = 'Panel 1 D-058 amendment: an authentic manufacturer VinFast V emblem is placed as a small front-door badge on the illustrated cyan vehicle. All fourteen v04 strings, eight flags, dates, heading, origin house, Danish frame, pilot annotation, logo and original generated art are unchanged. No separate corporate caption, Vingroup addition, visible citations or dated footprint face line.'

manifest['version'] = 'v05'
manifest['approval'] = list(dict.fromkeys(manifest['approval']+['D-058']))
manifest['content_master'] = 'panel-01-selected-content-and-visual-v04-2026-10-03.md'
manifest['status'] = 'Historical emblem-only D-058 preview, superseded by the student request for the full supplied VinFast emblem and wordmark; not accepted'
manifest['superseded_by_feedback'] = {'instruction':'Use the full provided VinFast logo, including wordmark; do not crop',
    'supplied_asset':'/Users/khoilq/Downloads/Logo_of_VinFast_(3D).svg',
    'next_version':'v06, ownership/amendment to be supplied by parent'}
manifest['authentic_logo']['file'] = str(Path(str(BASE)+'-logo.svg').resolve())
manifest['generated_decoration']['file'] = str(Path(str(BASE)+'-art.png').resolve())
manifest['generated_decoration']['reused_from_version'] = 'v04; original raw art generated in v02'
manifest['composition_source'] = str(Path(str(BASE)+'-compose.py').resolve())
manifest['text_editing'] = 'All v04 native glyph paths preserved exactly. Later wording changes require controlled glyph regeneration and fidelity checks.'
provenance = json.loads(Path(str(BASE)+'-vinfast-provenance.json').read_text())
manifest['vinfast_vehicle_badge'] = {**provenance,'svg_id':'authentic-vinfast-vehicle-badge',
    'placed_rect':[872,785,36,28.8],'placement':'Small badge on front-door body, below the handle',
    'original_art_altered':False,'generic_lightning_retained':True,
    'source_asset_sha256':hashlib.sha256(asset_file.read_bytes()).hexdigest(),
    'provenance_file':str(Path(str(BASE)+'-vinfast-provenance.json').resolve()),
    'no_caption_added':True,'no_danish_model_deployment_claim':True}
manifest['sources'].append({'key':provenance['source_key'],'pdf':provenance['pdf'],
    'url':provenance['original_url'],'sha256':provenance['pdf_sha256'],
    'registered_verification':'match','registered_check_date':'2026-10-03',
    'current_bytes_match':True,'registry_status':provenance['registry_status'],
    'use':'Authentic manufacturer emblem, visual asset only','pdf_page':1})
manifest['proposals_excluded'] = ['Literal Vietnamese origin label (superseded by icon)',
    'Full legal company name','Ninth country','Specific Danish Limo Green fleet identity',
    'Separate VinFast electric vehicles caption','VinFast logo outside the vehicle',
    'Vingroup name/logo addition']
manifest['vehicle_logo_amendment'] = {'authority':'D-058','visible_copy_changed':False,
    'new_image_generation':False,'authentic_brand_asset_only':True,'placement':'Front-door badge'}
ET.indent(root, space='  ')
Path(str(BASE)+'.svg').write_text(ET.tostring(root,encoding='unicode')+'\n')
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('Created complete panel 1 with authentic vehicle badge', BASE)
