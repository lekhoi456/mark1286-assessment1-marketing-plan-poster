"""Add the selected United States market through controlled vectors only.
Run: uv run --with fonttools python -B <this file>.
The native car artwork and all non-row objects are reused unchanged from v07.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import copy, importlib.util, json, math

BASE = Path(__file__).resolve().with_name('panel-01-production-v08-2026-10-03')
OLD = BASE.with_name('panel-01-production-v07-2026-10-03')
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
tag = lambda name: '{' + NS + '}' + name
root = ET.parse(Path(str(OLD) + '.svg')).getroot()
manifest = copy.deepcopy(json.loads(Path(str(OLD) + '-manifest.json').read_text()))
countries = manifest['flags'] + ['United States']
centres = [145, 315, 485, 655, 825, 995, 1165, 1335, 1505]
old_centres = [151, 333, 515, 697, 879, 1061, 1243, 1425]

# Row placement changes only: retain every previous flag and lettering path.
for country, old_x, new_x in zip(countries, old_centres, centres):
    key = country.lower().replace(' ', '-')
    flag = root.find(f'.//*[@id="flag-{key}"]')
    flag.set('transform', flag.get('transform') + f' translate({new_x-old_x} 0)')
    label = root.find(f'.//*[@id="country-{key}"]')
    label.set('transform', f'translate({new_x-old_x} 0)')
    for record in manifest['visible_text']:
        if record['id'] == 'country-' + key:
            record['x'] = new_x
            record['approx_bounds'] = [[a+new_x-old_x, b, c+new_x-old_x, d]
                                       for a, b, c, d in record['approx_bounds']]
for object_id, dx in [('vietnam-origin-home', -6), ('vietnam-launch', -6),
                       ('denmark-focus-frame', -78), ('denmark-launch', -78),
                       ('netherlands-pilot', -90)]:
    root.find(f'.//*[@id="{object_id}"]').set('transform', f'translate({dx} 0)')
    for record in manifest['visible_text']:
        if record['id'] == object_id:
            record['x'] += dx
            record['approx_bounds'] = [[a+dx, b, c+dx, d]
                                       for a, b, c, d in record['approx_bounds']]

# A 13-stripe / 50-star flag with marker streaks and a slightly uneven pen frame.
width, height = 121.6, 64
us = ET.Element(tag('g'), {'id': 'flag-united-states', 'data-country': 'United States',
    'transform': f'translate({centres[-1]-width/2} 261)',
    'data-stripe-count': '13', 'data-star-count': '50'})
ET.SubElement(us, tag('title')).text = 'United States flag'
defs = ET.SubElement(us, tag('defs'))
clip = ET.SubElement(defs, tag('clipPath'), {'id': 'us-flag-clip'})
ET.SubElement(clip, tag('rect'), {'width': str(width), 'height': str(height)})
bands = ET.SubElement(us, tag('g'), {'clip-path': 'url(#us-flag-clip)'})
ET.SubElement(bands, tag('rect'), {'width': str(width), 'height': str(height), 'fill': 'white'})
stripe_h = height/13
for stripe in range(0, 13, 2):
    clip = ET.SubElement(defs, tag('clipPath'), {'id': f'us-red-{stripe}'})
    ET.SubElement(clip, tag('rect'), {'y': str(stripe*stripe_h), 'width': str(width),
                                     'height': str(stripe_h)})
    band = ET.SubElement(bands, tag('g'), {'clip-path': f'url(#us-red-{stripe})'})
    ET.SubElement(band, tag('rect'), {'y': str(stripe*stripe_h), 'width': str(width),
        'height': str(stripe_h), 'fill': '#B31942', 'opacity': '.18'})
    y = (stripe+.5)*stripe_h
    ET.SubElement(band, tag('path'), {'d': f'M -1 {y+.25:.3f} Q 58 {y-.48:.3f} 123 {y+.13:.3f}',
        'fill': 'none', 'stroke': '#B31942', 'stroke-width': '5.4',
        'stroke-linecap': 'round', 'opacity': '.78'})
canton_w, canton_h = width*.4, stripe_h*7
clip = ET.SubElement(defs, tag('clipPath'), {'id': 'us-canton'})
ET.SubElement(clip, tag('rect'), {'width': str(canton_w), 'height': str(canton_h)})
canton = ET.SubElement(bands, tag('g'), {'clip-path': 'url(#us-canton)'})
ET.SubElement(canton, tag('rect'), {'width': str(canton_w), 'height': str(canton_h),
                                  'fill': '#234477', 'opacity': '.18'})
for i in range(7):
    y = (i+.5)*canton_h/7
    ET.SubElement(canton, tag('path'), {'d': f'M -1 {y+.2:.3f} Q 23 {y-.4:.3f} 50 {y+.1:.3f}',
        'fill': 'none', 'stroke': '#234477', 'stroke-width': '5.4',
        'stroke-linecap': 'round', 'opacity': '.9'})
for row in range(9):
    count = 6 if row % 2 == 0 else 5
    for column in range(count):
        x = canton_w*(column+(.5 if count == 6 else 1))/6
        y = canton_h*(row+.7)/9.4
        points = []
        for point in range(10):
            angle = -math.pi/2+point*math.pi/5
            radius = 1.74 if point % 2 == 0 else .74
            points.append((x+radius*math.cos(angle), y+radius*math.sin(angle)))
        d = 'M '+' L '.join(f'{x:.3f} {y:.3f}' for x, y in points)+' Z'
        ET.SubElement(canton, tag('path'), {'d': d, 'fill': '#FFFDF4',
            'stroke': '#FFFDF4', 'stroke-width': '.25', 'stroke-linejoin': 'round',
            'data-us-star': 'true'})
ET.SubElement(us, tag('path'), {'d': 'M -.3 1 Q 59 -1.1 121.2 .5 L 122 63.6 Q 58 65.1 .3 63.7 Z',
    'fill': 'none', 'stroke': '#143B4A', 'stroke-width': '1.5',
    'stroke-linecap': 'round', 'stroke-linejoin': 'round'})

# Use the exact local handwriting font for two centred lines, never a fallback.
helper = BASE.with_name('hand-drawn-lettering-layout-v01.py')
spec = importlib.util.spec_from_file_location('hand_lettering', helper)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
font_file = '/System/Library/Fonts/Noteworthy.ttc'
font = module.HandLettering(font_file, 0)
label = ET.Element(tag('g'), {'id': 'country-united-states', 'data-text': 'United States',
    'aria-label': 'United States', 'data-font-file': font_file, 'data-font-index': '0'})
ET.SubElement(label, tag('title')).text = 'United States'
bounds = []
for line, baseline in [('United', 363), ('States', 399)]:
    line_width = font.width(line, 32)
    x = centres[-1]-line_width/2
    letter_svg = ET.fromstring(font.svg(line, x, baseline, 32, '#143B4A'))
    for element in letter_svg.iter():
        element.tag = tag(element.tag.split('}')[-1])
    label.append(letter_svg)
    bounds.append([x, baseline-32, x+line_width, baseline+8.32])
insert = list(root).index(root.find('.//*[@id="netherlands-pilot"]'))+1
root.insert(insert, us)
root.insert(insert+1, label)
manifest['visible_text'].append({'id': 'country-united-states', 'text': 'United States',
    'x': centres[-1], 'baseline_y': 363, 'second_line_y': 399,
    'anchor': 'middle', 'font_size': 32, 'role': 'display', 'font_kind': 'body',
    'font_file': font_file, 'font_index': 0, 'wrap': ['United', 'States'],
    'approx_bounds': bounds, 'rendering': 'Exact native glyph outlines; no font-family fallback'})
root.find(tag('desc')).text = ('D-061: United States added as the ninth market/presence in one horizontal flag row. '
    'Existing lettering sizes and wording, Denmark emphasis, Vietnam home, two launch dates and raised Dutch pilot remain. '
    'All non-row geometry, native car artwork and controlled VINFAST paths are unchanged from v07. '
    'No US launch date, completed-ride claim, citation footer or new caption.')
manifest['version'] = 'v08'
manifest['approval'].append('D-061')
manifest['content_master'] = 'panel-01-selected-content-and-visual-v07-2026-10-03.md'
manifest['status'] = 'D-061 nine-country preview; student imagery acceptance and physical A0 proof pending'
manifest['flags'] = countries
manifest['flag_row'] = {'centres': centres, 'shared_bottom_y': 325,
    'existing_flag_sizes_unchanged': True, 'label_sizes_unchanged': True,
    'us_flag_dimensions': [width, height], 'us_stripes': 13, 'us_stars': 50,
    'us_label_wrap': ['United', 'States'], 'authority': 'D-061'}
manifest['origin_icon']['bounds'] = [57, 336, 84, 363]
manifest['origin_icon']['country_label_left'] -= 6
manifest['denmark_focus_frame']['placement_transform'] = 'translate(-78 0)'
manifest['denmark_focus_frame']['flag_rect'] = [1105.8, 235.4, 118.4, 89.6]
manifest['proposals_excluded'] = [p for p in manifest['proposals_excluded'] if p != 'Ninth country']
manifest['historical_footprint_metadata_v07'] = manifest.pop('footprint_metadata')
manifest['footprint_metadata'] = {'count': 9, 'as_at': '3 October 2026',
    'scope': 'Selected country market/presence row; not nine verified completed commercial launches',
    'netherlands_status': 'pilot', 'us_status': 'Official US-facing presence and service offer',
    'us_launch_date': None, 'us_completed_paid_rides_observed': False,
    'authority': 'D-061', 'historical_eight_market_record_preserved': True}
manifest['us_source_addition'] = {'authority': 'D-061',
    'verification': 'Parent headed-Comet capture, saved-PDF visual inspection and refs.py verify --offline: both automatic match, 0 failures, 3 October 2026',
    'url': 'https://www.greensm.com/us-en', 'operator': 'Green Future USA Inc.',
    'source_pdfs': ['04_references/green-future-usa-inc-ndb-us-homepage.pdf',
                    '04_references/green-future-usa-inc-nda-green-sm-car.pdf'],
    'source_records': [
        {'key': 'green-future-usa-inc-ndb', 'evidence_id': 'E-197',
         'pdf': '04_references/green-future-usa-inc-ndb-us-homepage.pdf',
         'physical_pages': [6], 'use': 'US presence, Green Future USA Inc. operator and California address',
         'url': 'https://www.greensm.com/us-en', 'registry_status': 'candidate',
         'parent_pdf_verification': 'match', 'checked_on': '2026-10-03',
         'sha256': 'f38c1f3462d071f7c1c135ba7d1c2fa845e354445d0dd0693747e53469ec947e'},
        {'key': 'green-future-usa-inc-nda', 'evidence_id': 'E-198',
         'pdf': '04_references/green-future-usa-inc-nda-green-sm-car.pdf',
         'physical_pages': [1, 2], 'use': 'US app-facing service offer and booking instructions; p.2 app image names Los Angeles International Airport and Santa Monica Pier',
         'url': 'https://www.greensm.com/us-en/greensm-car', 'registry_status': 'candidate',
         'parent_pdf_verification': 'match', 'checked_on': '2026-10-03',
         'sha256': '94087335bf27fddef7cc5f3ae80cf8b0090e8186d1093abb6327db012d50ca1b'}],
    'source_registry_and_evidence_owner': 'Parent agent; registration/verification and E-197/E-198 source mapping complete',
    'independent_section_source_audit': False,
    'unsupported_claims_excluded': ['US launch date', 'Observed completed paid rides']}
manifest['composition_source'] = str(Path(str(BASE)+'-compose.py').resolve())
manifest['text_editing'] = ('Fourteen prior strings and their glyph geometry retained; row objects translated only. '
    'United States is the fifteenth ordinary face object, using native Noteworthy paths at the existing country size.')
manifest['flag_amendment'] = {'authority': 'D-061', 'new_visible_text': ['United States'],
    'native_raster_edit': False, 'art_car_and_vinfast_unchanged': True,
    'date_and_font_sizes_unchanged': True, 'changes_confined_to_flag_row': True}
ET.indent(root, space='  ')
Path(str(BASE)+'.svg').write_text(ET.tostring(root, encoding='unicode')+'\n')
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
crop = copy.deepcopy(root)
crop.set('viewBox', '36 218 1540 211')
crop.set('width', '2310')
crop.set('height', '316.5')
Path(str(BASE)+'-flag-row-crop.svg').write_text(ET.tostring(crop, encoding='unicode')+'\n')
print('Created complete v08 and flag-row crop SVGs')
