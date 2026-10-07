"""Place the full student-supplied VinFast logo on the preserved panel.
Run: python3 -B <this file>. Exact whole SVG bytes embedded without cropping.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import base64, copy, hashlib, json

BASE = Path(__file__).resolve().with_name('panel-01-production-v06-2026-10-03')
OLD = BASE.with_name('panel-01-production-v04-2026-10-03')
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
root = ET.parse(Path(str(OLD)+'.svg')).getroot()
manifest = copy.deepcopy(json.loads(Path(str(OLD)+'-manifest.json').read_text()))
asset_file = Path(str(BASE)+'-vinfast-full-logo.svg')
raw = asset_file.read_bytes(); sha = hashlib.sha256(raw).hexdigest()
assert sha == '9d676729f71ddfcc6322c368ca1d446b1047fff3afc50cf847f22b5c67941f00'
logo = ET.Element('{'+NS+'}image', {'id':'full-vinfast-vehicle-logo',
    'x':'834','y':'737','width':'80','height':'82.5',
    'preserveAspectRatio':'xMidYMid meet',
    'href':'data:image/svg+xml;base64,'+base64.b64encode(raw).decode(),
    'role':'img','aria-label':'Complete student-supplied VinFast emblem and VINFAST wordmark'})
ix = list(root).index(root.find('.//*[@id="generated-hand-drawn-decoration"]'))
root.insert(ix+1, logo)
root.find('{'+NS+'}desc').text = 'Panel 1 D-059 correction: the complete student-supplied silver V and intrinsic VINFAST wordmark are embedded as unchanged full SVG bytes on the front door. Proportions and both components are retained without crop or reflow. All fourteen approved text objects, eight flags, dates, heading, house, Danish frame, pilot, Green SM logo and generated drawing are unchanged. The earlier emblem-only v05 is superseded and not accepted.'

manifest['version'] = 'v06'
manifest['approval'] = list(dict.fromkeys(manifest['approval']+['D-058','D-059']))
manifest['content_master'] = 'panel-01-selected-content-and-visual-v05-2026-10-03.md'
manifest['status'] = 'Selected D-059 full-logo preview; student image acceptance and physical A0 integration remain pending'
manifest['authentic_logo']['file'] = str(Path(str(BASE)+'-logo.svg').resolve())
manifest['generated_decoration']['file'] = str(Path(str(BASE)+'-art.png').resolve())
manifest['generated_decoration']['reused_from_version'] = 'v04; original raw art generated in v02'
manifest['composition_source'] = str(Path(str(BASE)+'-compose.py').resolve())
manifest['text_editing'] = 'All v04/v05 native glyph paths retained unchanged; intrinsic VinFast wordmark is part of whole supplied artwork, not separately typeset.'
provenance = json.loads(Path(str(BASE)+'-vinfast-provenance.json').read_text())
manifest['vinfast_full_vehicle_logo'] = {**provenance,'svg_id':'full-vinfast-vehicle-logo',
    'placed_rect':[834,737,80,82.5],'placement':'Front-door body; enlarged to keep the intrinsic wordmark readable',
    'embedding':'Exact original complete SVG bytes as an isolated SVG image resource',
    'provenance_file':str(Path(str(BASE)+'-vinfast-provenance.json').resolve()),
    'components_independently_changed':False,'crop_applied':False,'original_art_altered':False,
    'generic_lightning_retained':True,'no_caption_added':True,'no_danish_model_deployment_claim':True}
context = provenance['manufacturer_context']
manifest['sources'].append({'key':context['source_key'],'pdf':context['pdf'],
    'url':context['url'],'sha256':context['pdf_sha256'],'registered_verification':'match',
    'registered_check_date':'2026-10-03','current_bytes_match':True,'registry_status':'candidate',
    'use':'Manufacturer brand/vehicle-range context, distinct from the user-supplied logo origin','pdf_page':1})
manifest['proposals_excluded'] = ['Literal Vietnamese origin label (superseded by icon)',
    'Full legal company name','Ninth country','Specific Danish Limo Green fleet identity',
    'Separate VinFast electric vehicles caption','VinFast logo outside the vehicle',
    'Vingroup name/logo addition']
manifest['vehicle_logo_amendment'] = {'authority':'D-059','visible_copy_changed':False,
    'new_image_generation':False,'complete_supplied_logo_used':True,
    'previous_emblem_only_v05':'Historical, superseded and not accepted'}
ET.indent(root, space='  ')
Path(str(BASE)+'.svg').write_text(ET.tostring(root,encoding='unicode')+'\n')
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('Created complete panel 1 with full unchanged supplied VinFast logo', BASE)
