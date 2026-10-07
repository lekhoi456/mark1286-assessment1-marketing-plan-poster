"""Remove the US flag/label and restore the exact eight-country row from v07.
Run: python3 -B <this file>. No raster edits or regenerated glyphs.
All non-row objects, including the v09 background callout, are unchanged.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import copy, json

BASE = Path(__file__).resolve().with_name('panel-01-production-v10-2026-10-03')
OLD = BASE.with_name('panel-01-production-v09-2026-10-03')
ROW = BASE.with_name('panel-01-production-v07-2026-10-03')
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
tag = lambda name: '{' + NS + '}' + name
root = ET.parse(Path(str(OLD)+'.svg')).getroot()
row_root = ET.parse(Path(str(ROW)+'.svg')).getroot()
manifest = copy.deepcopy(json.loads(Path(str(OLD)+'-manifest.json').read_text()))
row_manifest = json.loads(Path(str(ROW)+'-manifest.json').read_text())
row_ids = {element.get('id') for element in row_root
           if element.get('id', '').startswith(('flag-', 'country-'))}
row_ids.update(['vietnam-origin-home', 'vietnam-launch', 'denmark-launch',
                'denmark-focus-frame', 'netherlands-pilot'])
for object_id in row_ids:
    existing = root.find(f'.//*[@id="{object_id}"]')
    replacement = copy.deepcopy(row_root.find(f'.//*[@id="{object_id}"]'))
    index = list(root).index(existing)
    root.remove(existing)
    root.insert(index, replacement)
for object_id in ['flag-united-states', 'country-united-states']:
    root.remove(root.find(f'.//*[@id="{object_id}"]'))
row_text = {record['id']:record for record in row_manifest['visible_text']}
removed_text = next(record for record in manifest['visible_text']
                    if record['id'] == 'country-united-states')
manifest['visible_text'] = [copy.deepcopy(row_text[record['id']])
    if record['id'] in row_ids else record for record in manifest['visible_text']
    if record['id'] != 'country-united-states']
root.find(tag('desc')).text = ('D-064 removes only the US flag and United States label. '
    'The eight-country launch/pilot row restores exact v07 spacing and annotations. '
    'All sixteen retained ordinary strings, v09 background callout, authentic logos and raw car artwork remain. '
    'No planned-market replacement, summary, face disclaimer, new lettering or raster edit.')
manifest['version'] = 'v10'
manifest['approval'].append('D-064')
manifest['content_master'] = 'panel-01-selected-content-and-visual-v09-2026-10-03.md'
manifest['status'] = 'D-064 eight-country correction preview; final imagery acceptance and physical A0 proof pending'
manifest['flags'] = copy.deepcopy(row_manifest['flags'])
manifest['historical_flag_row_v09'] = manifest['flag_row']
manifest['flag_row'] = {'centres':[151,333,515,697,879,1061,1243,1425],
    'shared_bottom_y':325, 'existing_flag_sizes_unchanged':True,
    'label_sizes_unchanged':True, 'spacing_source':'Production v07, exact row objects',
    'authority':'D-064'}
manifest['origin_icon'] = copy.deepcopy(row_manifest['origin_icon'])
manifest['denmark_focus_frame'] = copy.deepcopy(row_manifest['denmark_focus_frame'])
manifest['historical_footprint_metadata_v09'] = manifest['footprint_metadata']
manifest['footprint_metadata'] = copy.deepcopy(row_manifest['footprint_metadata'])
manifest['footprint_metadata']['display_selection_authority'] = 'D-064'
manifest['footprint_metadata']['display_selection_date'] = '2026-10-03'
manifest['footprint_metadata']['us_counted_in_current_row'] = False
manifest['historical_us_source_addition'] = manifest.pop('us_source_addition')
manifest['historical_us_source_addition_status'] = ('US web presence/promotion evidence preserved; '
    'D-061 flag inclusion superseded for display by D-064. Not evidence of completed commercial launch.')
manifest['composition_source'] = str(Path(str(BASE)+'-compose.py').resolve())
manifest['text_editing'] = ('Sixteen ordinary strings retained; only United States removed. '
    'Row glyph shapes/sizes retained with exact v07 anchors; all other glyph positions unchanged.')
manifest['us_removal_amendment'] = {'authority':'D-064',
    'removed_svg_ids':['flag-united-states','country-united-states'],
    'removed_ordinary_text_record':removed_text,
    'display_scope':'Established launch/pilot footprint; Netherlands remains a pilot',
    'spacing_restored_from':'v07', 'all_non_row_geometry_unchanged':True,
    'no_replacement_planned_country':True, 'no_face_summary_or_disclaimer':True,
    'new_raster_edit_or_generation':False,
    'parent_context':{'url':'https://tech.zingnews.vn/taxi-dien-green-sm-se-den-my-post1681536.html',
        'key':'dan-thanh-2026', 'evidence_id':'E-202',
        'pdf':'04_references/dan-thanh-2026-taxi-dien-green-sm-se-den-my.pdf',
        'article_date':'2026-09-09', 'plan_physical_page':2, 'byline_date_physical_page':1,
        'review_owner':'Parent agent',
        'verification':'Parent rendered/read saved p.2; automatic offline identity match passed',
        'scope':'Dated expansion plans; not proof of US service absence at every later date',
        'dated_pdf_and_source_correction_owner':'Parent agent; complete',
        'independent_section_source_audit':False}}
ET.indent(root, space='  ')
Path(str(BASE)+'.svg').write_text(ET.tostring(root, encoding='unicode')+'\n')
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
crop = copy.deepcopy(root)
crop.set('viewBox', '40 218 1520 211')
crop.set('width', '2280')
crop.set('height', '316.5')
Path(str(BASE)+'-flag-row-crop.svg').write_text(ET.tostring(crop, encoding='unicode')+'\n')
print('Created complete v10 and restored eight-country crop SVGs')
