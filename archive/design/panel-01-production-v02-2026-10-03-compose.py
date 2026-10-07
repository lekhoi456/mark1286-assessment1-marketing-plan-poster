"""Compose the approved panel using exact local handwriting glyphs and new art.
Run from workspace: uv run --with fonttools python -B <this file>.
No font files are redistributed and no family-name fallback is possible.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import base64, copy, hashlib, json, math, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
BASE = Path(__file__).resolve().with_name('panel-01-production-v02-2026-10-03')
OLD = BASE.with_name('panel-01-production-v01-2026-10-03')
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
RNG = random.Random(3101)
FONT_PATHS = {'heading': ('/System/Library/Fonts/MarkerFelt.ttc', 0),
              'body': ('/System/Library/Fonts/Noteworthy.ttc', 0),
              'strong': ('/System/Library/Fonts/Noteworthy.ttc', 1)}
FONTS = {k: TTFont(p, fontNumber=i) for k, (p, i) in FONT_PATHS.items()}
def add(parent, tag, attrs, text=None):
    e = ET.SubElement(parent, '{'+NS+'}'+tag, {k: str(v) for k,v in attrs.items()})
    e.text = text
    return e
def outline_string(parent, text, x, y, size, kind, anchor):
    font = FONTS[kind]; cmap = font.getBestCmap(); glyphs = font.getGlyphSet()
    scale = size/font['head'].unitsPerEm; metrics = font['hmtx'].metrics
    names = [cmap.get(ord(ch)) for ch in text]
    if any(name is None for name in names):
        raise ValueError('Missing glyph in explicit font: '+text)
    width = sum(metrics[name][0] for name in names)*scale
    left = x-width/2 if anchor=='middle' else x
    pos = 0
    for name in names:
        pen = SVGPathPen(glyphs); glyphs[name].draw(pen); d = pen.getCommands()
        if d:
            add(parent,'path',{'d':d, 'transform':f'translate({left+pos*scale:.4f} {y:.4f}) scale({scale:.7f} {-scale:.7f})', 'fill':'#143B4A'})
        pos += metrics[name][0]
    return [left, y-size, left+width, y+size*.26]
root = ET.parse(Path(str(OLD)+'-generated-section.svg')).getroot()
manifest = copy.deepcopy(json.loads(Path(str(OLD)+'-manifest.json').read_text()))
for e in list(root):
    if e.tag.endswith('style') or e.attrib.get('id')=='generated-hand-drawn-decoration': root.remove(e)
    if e.attrib.get('d')=='M 37 39 Q 193 31 352 38 L 1188 35 Q 1438 29 1563 43': root.remove(e)
for e in root:
    if e.tag.endswith('path') and e.attrib.get('stroke-width')=='5': e.set('stroke-width','2.3')
    if e.attrib.get('d')=='M 82 194 Q 464 204 819 194':
        e.set('stroke-width','8');e.set('opacity','.55');e.set('d','M 81 195 Q 280 202 487 193 T 814 198')
    if e.attrib.get('d')=='M 78 511 Q 820 517 1521 510':
        e.set('stroke-width','1.3');e.set('stroke','#143B4A');e.set('opacity','.55')
# Loose marker fills, clipped to the exact national flag bands.
for group in root.findall('.//{'+NS+'}g[@data-country]'):
    for rect in list(group):
        if not rect.tag.endswith('rect'): continue
        a=rect.attrib; x=float(a.get('x',0));y=float(a.get('y',0));w=float(a['width']);h=float(a['height']);colour=a.get('fill','none')
        idx=list(group).index(rect); group.remove(rect)
        if colour=='none':
            d=f'M {x-.4} {y+.4} Q {x+w*.45} {y-1.0} {x+w+.5} {y+.6} L {x+w-.5} {y+h-.4} Q {x+w*.52} {y+h+1.0} {x+.4} {y+h-.5} Z'
            e=ET.Element('{'+NS+'}path',{'d':d,'fill':'none','stroke':'#143B4A','stroke-width':'1.3','stroke-linejoin':'round'});group.insert(idx,e);continue
        g=ET.Element('{'+NS+'}g',{'aria-label':'Hand marker flag band'})
        cid=group.attrib['id']+'-band-'+str(idx);defs=add(g,'defs',{});clip=add(defs,'clipPath',{'id':cid})
        add(clip,'rect',{'x':x,'y':y,'width':w,'height':h})
        strokes=add(g,'g',{'clip-path':'url(#'+cid+')'})
        add(strokes,'rect',{'x':x,'y':y,'width':w,'height':h,'fill':colour,'opacity':'1' if colour=='white' else '.16'})
        for n in range(math.ceil(h/6)+1):
            yy=y+3+n*6; drift=RNG.uniform(-.8,.8)
            add(strokes,'path',{'d':f'M {x-1} {yy+drift:.2f} Q {x+w*.48:.2f} {yy-1.1:.2f} {x+w+1} {yy+.4:.2f}', 'fill':'none','stroke':colour,'stroke-width':RNG.uniform(5.4,6.9),'opacity':'.72','stroke-linecap':'round'})
        group.insert(idx,g)
    for symbol in group:
        if symbol.tag.endswith('polygon'): symbol.set('opacity','.88')
# Replace the digital Danish highlight with sparse, translucent marker strokes.
for e in root:
    if e.tag.endswith('path') and e.attrib.get('fill')=='#FFF3AC':
        e.set('fill','none');e.set('stroke-width','7');e.set('opacity','.55')
        e.set('d','M 1164 240 Q 1228 232 1320 238 M 1165 372 Q 1249 379 1316 373')
        e.set('stroke-linecap','round')
# Exact text is rendered from paths in explicit font files, never through substitution.
for t in manifest['visible_text']:
    old_el=root.find('.//*[@id="'+t['id']+'"]'); parent=next(e for e in root.iter() if old_el in list(e))
    ix=list(parent).index(old_el);parent.remove(old_el)
    kind='heading' if t['id']=='heading-meet' else ('strong' if t['id'] in ['service-line','operating-model','vietnam-launch','denmark-launch'] else 'body')
    size=90 if kind=='heading' else (50 if t['id'] in ['service-line','operating-model'] else (30 if kind=='strong' else (32 if t['id'].startswith('country-') else (23 if t['id'] in ['vietnam-launch-citation','denmark-launch-citation'] else 28))))
    g=ET.Element('{'+NS+'}g',{'id':t['id'],'data-text':t['text'],'aria-label':t['text'],'data-font-file':FONT_PATHS[kind][0],'data-font-index':str(FONT_PATHS[kind][1])})
    add(g,'title',{},t['text']);lines=t.get('wrap',[t['text']]);bounds=[]
    for i,line in enumerate(lines):
        y=t['baseline_y'] if i==0 else t['second_line_y'];bounds.append(outline_string(g,line,t['x'],y,size,kind,t['anchor']))
    parent.insert(ix,g);t.update({'font_size':size,'font_kind':kind,'font_file':FONT_PATHS[kind][0],'font_index':FONT_PATHS[kind][1],'approx_bounds':bounds,'rendering':'Exact native glyph outlines; no font-family fallback'})
raw=Path(str(BASE)+'-art.png').read_bytes();art=ET.Element('{'+NS+'}svg',{'id':'generated-hand-drawn-decoration','x':'210','y':'680','width':'1180','height':'270','viewBox':'40 94 2110 568','preserveAspectRatio':'xMidYMid meet'})
add(art,'image',{'x':0,'y':0,'width':2172,'height':724,'href':'data:image/png;base64,'+base64.b64encode(raw).decode()})
ix=next(i for i,e in enumerate(root) if e.attrib.get('id')=='operating-model');root.insert(ix,art)
root.find('{'+NS+'}desc').text='Complete approved panel 1, revised to manual pen/marker style. Exact lettering uses native glyph outlines from Marker Felt and Noteworthy local font files; authentic corporate logo paths are unchanged. Eight flags, two launch dates, source context and five citations are preserved. The generated phone-to-cyan-electric-MPV picture is symbolic.'
ET.indent(root,space='  ');Path(str(BASE)+'.svg').write_text(ET.tostring(root,encoding='unicode')+'\n')
manifest['version']='v02';manifest['style_authority']='shared-hand-drawn-style-revision-v01-2026-10-03.md'
manifest['fonts']={k:{'file':p,'index':i,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for k,(p,i) in FONT_PATHS.items()}
manifest['generated_decoration']={'tool':'built-in image_gen.imagegen','file':str(Path(str(BASE)+'-art.png').resolve()),'raw_sha256':hashlib.sha256(raw).hexdigest(),'native_dimensions_px':[2172,724],'original_file':'/Users/KHOILQ/.codex/generated_images/01a10028-2e2f-7a92-8df7-45fa2e0976f8/exec-2f524710-2115-409c-a418-fd72a2f1fdaf.png','prompt_file':str(Path(str(BASE)+'-prompt.txt').resolve()),'style_reference':'/var/folders/j7/k3hwp19s0614s73_m5cj2hn80000gn/T/codex-clipboard-18eec81c-4572-4828-868e-e1f10d3009a6.png','alterations':'Raw generated PNG retained unchanged; only embedded in the SVG layout'}
manifest['authentic_logo']['file']=str(Path(str(BASE)+'-logo.svg').resolve())
manifest['authentic_logo']['preview']=None
manifest['generated_decoration']['style_reference_copy']=str(Path(str(BASE)+'-style-reference.png').resolve())
manifest['composition_source']=str(Path(str(BASE)+'-compose.py').resolve())
manifest['text_editing']='Edit the owned composition/placement source, regenerate explicit native glyphs, and recheck exact copy.'
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('Created revised complete handwriting panel', BASE)
