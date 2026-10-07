"""Apply the approved citation-display amendment without changing other panel objects.

Uses preserved v04 files and Python standard library only. No new image generation,
font rendering, source change or chart re-computation is required for this removal.
"""
from pathlib import Path
import json
import re
import shutil

HERE = Path(__file__).resolve().parent
OLD = 'panel-02-production-v04-2026-10-03'
NEW = 'panel-02-production-v05-2026-10-03'

def remove_object(source, element):
    pattern = rf'<{element}\b[^>]*\bid="p2-source"[^>]*>.*?</{element}>'
    revised, count = re.subn(pattern, '', source, flags=re.DOTALL)
    assert count == 1, 'Expected exactly one source-attribution object'
    assert 'id="p2-source"' not in revised
    return revised

for suffix, element in (('.svg', 'g'), ('-editable.svg', 'text')):
    source = (HERE/(OLD+suffix)).read_text()
    (HERE/(NEW+suffix)).write_text(remove_object(source, element))

manifest = json.loads((HERE/(OLD+'-text-manifest.json')).read_text())
removed = [obj for obj in manifest['text_objects'] if obj['id']=='p2-source']
assert len(removed)==1
manifest['text_objects'] = [obj for obj in manifest['text_objects'] if obj['id']!='p2-source']
assert len(manifest['text_objects'])==30
manifest['version']='v05'
manifest['authority'].extend(['D-055','LG-004 (lecturer guidance relayed by student)'])
manifest['citation_display_policy']={
    'policy':'poster-citation-display-policy-v01-2026-10-03.md',
    'visible_attribution_removed':True,
    'removed_object':removed[0],
    'source_mapping_retained':True,
    'remaining_text_and_geometry':'Every remaining object and all chart/art geometry unchanged from v04',
    'note':'Policy text says FOLK1A1; the actual removed v04 object says FOLK1A. The intended attribution object was removed by its stable ID; the verified dataset remains FOLK1A internally.'
}
manifest['illustrations']['art_file']=NEW+'-generated-art.png'
manifest['placement_rules'].append('Under D-055/LG-004, the p2-source attribution object is absent from the poster face; source/calculation/verified-PDF metadata remains internal.')
(HERE/(NEW+'-text-manifest.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
shutil.copyfile(HERE/(OLD+'-generated-art.png'), HERE/(NEW+'-generated-art.png'))
print('Removed one visible attribution object from both SVGs; 30 remaining objects and all geometry retained.')
print('Original generated art copied unchanged; full source metadata retained internally.')
