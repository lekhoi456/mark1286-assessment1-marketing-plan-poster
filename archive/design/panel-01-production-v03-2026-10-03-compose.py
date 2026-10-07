"""Apply D-055 citation display amendments to the preserved handwriting panel.
Run: uv run --with fonttools python -B <this file>. No image generation.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import copy, hashlib, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
BASE=Path(__file__).resolve().with_name('panel-01-production-v03-2026-10-03')
OLD=BASE.with_name('panel-01-production-v02-2026-10-03')
NS='http://www.w3.org/2000/svg';ET.register_namespace('',NS)
REMOVE=['vietnam-launch-citation','denmark-launch-citation','service-citation','operating-model-citation']
FOOTPRINT='Eight markets · as at 26 September 2026 · Netherlands: pilot.'
root=ET.parse(Path(str(OLD)+'.svg')).getroot()
old_manifest=json.loads(Path(str(OLD)+'-manifest.json').read_text())
manifest=copy.deepcopy(old_manifest)
removed=[copy.deepcopy(t) for t in manifest['visible_text'] if t['id'] in REMOVE]
for e in list(root):
    if e.tag.endswith('a') and any(e.find('.//*[@id="'+rid+'"]') is not None for rid in REMOVE):root.remove(e)
# Strip the mixed-line source link from the rendered layout, retaining provenance below.
old_line=root.find('.//*[@id="footprint-context"]')
parent=next(e for e in root if old_line in list(e));ix=list(root).index(parent);root.remove(parent)
font=TTFont('/System/Library/Fonts/Noteworthy.ttc',fontNumber=0)
cmap=font.getBestCmap();glyphs=font.getGlyphSet();metrics=font['hmtx'].metrics
size=28;scale=size/font['head'].unitsPerEm;names=[cmap.get(ord(c)) for c in FOOTPRINT]
assert all(names),'Required handwriting glyph unavailable'
width=sum(metrics[n][0] for n in names)*scale;left=800-width/2;y=466;pos=0
new=ET.Element('{'+NS+'}g',{'id':'footprint-context','data-text':FOOTPRINT,'aria-label':FOOTPRINT,'data-font-file':'/System/Library/Fonts/Noteworthy.ttc','data-font-index':'0'})
ET.SubElement(new,'{'+NS+'}title').text=FOOTPRINT
for name in names:
    pen=SVGPathPen(glyphs);glyphs[name].draw(pen);d=pen.getCommands()
    if d:ET.SubElement(new,'{'+NS+'}path',{'d':d,'transform':f'translate({left+pos*scale:.4f} {y:.4f}) scale({scale:.7f} {-scale:.7f})','fill':'#143B4A'})
    pos+=metrics[name][0]
root.insert(ix,new)
# Move the existing service drawing slightly upwards into the space made by removal.
root.find('.//*[@id="generated-hand-drawn-decoration"]').set('y','650')
root.find('{'+NS+'}desc').text='Complete approved panel 1 with handwriting glyphs and unchanged official logo. Eight flags, both launch dates, dated Dutch-pilot context, Copenhagen service and operating model are retained. Visible author/year/page citations removed under D-055 and LG-004; internal source records remain in the companion manifest. Existing generated artwork is reused unchanged.'
manifest['visible_text']=[t for t in manifest['visible_text'] if t['id'] not in REMOVE]
for t in manifest['visible_text']:
    if t['id']=='footprint-context':
        old_text=t['text'];source_url=t.pop('source_url',None)
        t.update({'text':FOOTPRINT,'baseline_y':y,'approx_bounds':[[left,y-size,left+width,y+size*.26]],'internal_source_url':source_url})
manifest['version']='v03';manifest['citation_display_authority']={'decision':'D-055','lecturer_guidance':'LG-004','policy':'poster-citation-display-policy-v01-2026-10-03.md'}
manifest['citation_amendments']={'removed_objects':removed,'mixed_line':{'id':'footprint-context','previous':old_text,'current':FOOTPRINT,'removed':'(Green SM, 2026a)','source_url':source_url},'retained_object_ids':[t['id'] for t in manifest['visible_text']],'sources_preserved':True}
manifest['authentic_logo']['file']=str(Path(str(BASE)+'-logo.svg').resolve())
manifest['generated_decoration']['reused_from_version']='v02';manifest['generated_decoration']['file']=str(Path(str(BASE)+'-art.png').resolve());manifest['generated_decoration']['layout_y']=650
manifest['composition_source']=str(Path(str(BASE)+'-compose.py').resolve())
manifest['art_reuse_sha256']=hashlib.sha256(Path(str(BASE)+'-art.png').read_bytes()).hexdigest()
ET.indent(root,space='  ');Path(str(BASE)+'.svg').write_text(ET.tostring(root,encoding='unicode')+'\n')
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('Created complete citation-free display composition',BASE)
