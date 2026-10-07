"""Add the approved background callout using pen vectors and native glyphs.
Run: uv run --with fonttools python -B <this file>.
Every pre-existing object is reused unchanged from production v08.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import copy, importlib.util, json

BASE = Path(__file__).resolve().with_name('panel-01-production-v09-2026-10-03')
OLD = BASE.with_name('panel-01-production-v08-2026-10-03')
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
tag = lambda name: '{' + NS + '}' + name
root = ET.parse(Path(str(OLD)+'.svg')).getroot()
manifest = copy.deepcopy(json.loads(Path(str(OLD)+'-manifest.json').read_text()))
helper = BASE.with_name('hand-drawn-lettering-layout-v01.py')
spec = importlib.util.spec_from_file_location('hand_lettering', helper)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
font_file = '/System/Library/Fonts/Noteworthy.ttc'
font = module.HandLettering(font_file, 0)

def pen(parent, d, colour='#143B4A', width=1.8, opacity=1):
    return ET.SubElement(parent, tag('path'), {'d':d, 'fill':'none',
        'stroke':colour, 'stroke-width':str(width), 'opacity':str(opacity),
        'stroke-linecap':'round', 'stroke-linejoin':'round'})

building = ET.Element(tag('g'), {'id':'background-building-icon', 'role':'img',
    'aria-label':'Generic building group icon', 'transform':'translate(900 80)'})
ET.SubElement(building, tag('title')).text = 'Generic building group'
pen(building, 'M 6 29 L 6 37 M 10 27 L 10 37 M 22 11 L 22 37 M 26 11 L 26 37 M 38 25 L 38 37', '#20C7CB', 3.5, .45)
pen(building, 'M 0 42 L 44 41 M 2 40 L 2 22 L 16 22 M 16 40 L 16 3 L 31 2 L 31 40 M 31 19 L 42 20 L 42 40')
pen(building, 'M 20 9 L 23 9 M 26 9 L 28 9 M 20 16 L 23 16 M 26 16 L 28 16 M 20 23 L 23 23 M 26 23 L 28 23 M 6 29 L 10 29 M 35 26 L 38 26', width=1.3)
pen(building, 'M 21 40 L 21 31 L 27 31 L 27 40', width=1.5)

calendar = ET.Element(tag('g'), {'id':'background-calendar-icon', 'role':'img',
    'aria-label':'Generic calendar icon without printed dates',
    'transform':'translate(902 137)'})
ET.SubElement(calendar, tag('title')).text = 'Generic calendar'
pen(calendar, 'M 4 11 Q 18 9 36 11 M 4 15 Q 19 13 36 14', '#FFCA00', 4.3, .55)
pen(calendar, 'M 1 7 Q 20 5 39 7 L 40 37 Q 21 39 1 37 Z M 1 17 Q 19 16 39 17')
pen(calendar, 'M 10 2 L 10 11 M 30 1 L 30 11', width=2)
pen(calendar, 'M 8 24 L 12 24 M 19 24 L 23 24 M 30 24 L 33 24 M 8 31 L 12 31 M 19 31 L 23 31', width=1.6)
pen(calendar, 'M 28 30 L 30 33 L 35 27', '#20C7CB', 2.1)

additions = [building, calendar]
for object_id, text, baseline in [('background-vingroup', 'Vingroup-backed', 114),
                                   ('background-founded', 'Founded March 2023', 168)]:
    glyphs = ET.fromstring(font.svg(text, 965, baseline, 32, '#143B4A'))
    for element in glyphs.iter():
        element.tag = tag(element.tag.split('}')[-1])
    glyphs.attrib.update({'id':object_id, 'data-text':text,
        'data-font-file':font_file, 'data-font-index':'0'})
    additions.append(glyphs)
    manifest['visible_text'].append({'id':object_id, 'text':text, 'x':965,
        'baseline_y':baseline, 'anchor':'start', 'font_size':32, 'role':'display',
        'font_kind':'body', 'font_file':font_file, 'font_index':0,
        'approx_bounds':[[965, baseline-32, 965+font.width(text,32), baseline+8.32]],
        'rendering':'Exact native glyph outlines; no font-family fallback'})
insert = list(root).index(root.find('.//*[@id="authentic-green-sm-logo"]'))+1
for i, element in enumerate(additions):
    root.insert(insert+i, element)
root.find(tag('desc')).text = ('D-063 adds only the approved upper-right Vingroup-backed / Founded March 2023 callout '
    'with generic hand-drawn building and calendar icons. All fifteen prior strings, nine flags and their placements, '
    'authentic Green SM logo and raw car/VINFAST artwork remain unchanged from v08. No new corporate logo or optional EV label.')
manifest['version'] = 'v09'
manifest['approval'].append('D-063')
manifest['content_master'] = 'panel-01-selected-content-and-visual-v08-2026-10-03.md'
manifest['status'] = 'D-063 background callout preview; student imagery acceptance and physical A0 proof pending'
manifest['composition_source'] = str(Path(str(BASE)+'-compose.py').resolve())
manifest['text_editing'] = 'All fifteen v08 text objects retained unchanged. Two approved lines added with native Noteworthy glyph paths.'
manifest['background_callout'] = {'authority':'D-063',
    'visible_lines':['Vingroup-backed','Founded March 2023'],
    'icon_ids':['background-building-icon','background-calendar-icon'],
    'text_ids':['background-vingroup','background-founded'],
    'location':'Existing upper-right header space beside title/logo and above the flag row',
    'icon_bounds':[[900,80,944,122],[903,138,942,176]],
    'generic_building_not_vingroup_logo':True, 'new_native_raster_edit':False,
    'existing_geometry_unchanged':True, 'optional_ev_labels_selected':False}
manifest['background_source'] = {'evidence_id':'E-199',
    'key':'green-future-usa-inc-ndc',
    'pdf':'04_references/green-future-usa-inc-ndc-story-and-humanity.pdf',
    'physical_page':2, 'url':'https://www.greensm.com/us-en/about',
    'accessed':'2026-10-03',
    'verified_by':'Parent headed-Comet/source-PDF inspection and automatic identity match',
    'verification_scope':'Parent verification reused; no independent section source audit',
    'source_phrases':['Green SM is an all-electric mobility platform backed by Vingroup',
                      'Founded in March 2023'],
    'meaning':'Backing is not legal subsidiary ownership; month of foundation is distinct from April taxi launch',
    'unsupported_claims_excluded':['Legal subsidiary ownership','Precise foundation day','Optional EV/tailpipe labels']}
ET.indent(root, space='  ')
Path(str(BASE)+'.svg').write_text(ET.tostring(root, encoding='unicode')+'\n')
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
crop = copy.deepcopy(root)
crop.set('viewBox', '54 45 1490 165')
crop.set('width', '2235')
crop.set('height', '247.5')
Path(str(BASE)+'-header-crop.svg').write_text(ET.tostring(crop, encoding='unicode')+'\n')
print('Created complete v09 and header/callout crop SVGs')
