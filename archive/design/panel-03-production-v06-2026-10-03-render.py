"""Replace every actual Green SM lockup with the shared hand-drawn PNG."""
from pathlib import Path
import base64
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image

HERE = Path(__file__).resolve().parent
BASE = 'panel-03-production-v05-2026-10-03'
PREFIX = 'panel-03-production-v06-2026-10-03'
LOGO = HERE / 'green-sm-hand-drawn-logo-v01-2026-10-03.png'
SVG_NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG_NS)
tag = lambda name: '{' + SVG_NS + '}' + name
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
uri = lambda path: 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode('ascii')

manifest = json.loads((HERE / f'{BASE}-text-manifest.json').read_text())
original_logo = HERE / manifest['authentic_logo_source']
tree = ET.parse(HERE / f'{BASE}.svg')
root = tree.getroot()
shared = Image.open(LOGO)
crop = shared.getchannel('A').getbbox()
left, top, right, bottom = crop
crop_width, crop_height = right-left, bottom-top
replacements = []
old_uri = uri(original_logo)
for parent in list(root.iter()):
    for index, child in enumerate(list(parent)):
        if child.tag == tag('image') and child.get('href') == old_uri:
            ident = child.get('id', 'green-sm-logo')
            placement = {key: child.get(key) for key in ['x','y','width','height','preserveAspectRatio']}
            view = ET.Element(tag('svg'), {'id': ident, **placement,
                'viewBox': f'{left} {top} {crop_width} {crop_height}', 'overflow': 'hidden',
                'data-logo-style': 'shared hand-drawn Green SM lockup'})
            defs = ET.SubElement(view, tag('defs'))
            clip_id = ident + '-handdrawn-source-bounds'
            clip = ET.SubElement(defs, tag('clipPath'), {'id': clip_id, 'clipPathUnits': 'userSpaceOnUse'})
            ET.SubElement(clip, tag('rect'), {'x':str(left),'y':str(top),'width':str(crop_width),'height':str(crop_height)})
            group = ET.SubElement(view, tag('g'), {'clip-path': f'url(#{clip_id})'})
            ET.SubElement(group, tag('image'), {'id': ident+'-shared-png', 'href':uri(LOGO),
                'x':'0','y':'0','width':str(shared.width),'height':str(shared.height)})
            parent.remove(child)
            parent.insert(index, view)
            replacements.append({'id':ident,'placement':placement,'source_alpha_bbox':list(crop),
                                 'source_crop':[left,top,crop_width,crop_height]})
if not replacements:
    raise RuntimeError('No actual Green SM logo lockup found')
(HERE / f'{PREFIX}.svg').write_text(ET.tostring(root,encoding='unicode'))
(HERE / f'{PREFIX}.md').write_bytes((HERE / f'{BASE}.md').read_bytes())
manifest['previous_production'] = BASE
manifest['copy_source'] = f'{PREFIX}.md'
manifest['render_source'] = Path(__file__).name
manifest['baseline_acceptance'] = 'D-073'
manifest['logo_revision_authority'] = 'Parent-dispatched user instruction to apply the shared hand-drawn Green SM logo'
manifest['original_corporate_logo_source'] = manifest.pop('authentic_logo_source')
manifest['original_corporate_logo_sha256'] = manifest.pop('authentic_logo_sha256')
manifest['display_logo_asset'] = LOGO.name
manifest['display_logo_sha256'] = sha(LOGO)
manifest['display_logo_dimensions'] = list(shared.size)
manifest['display_logo_alpha_extrema'] = list(shared.getchannel('A').getextrema())
manifest['logo_replacements'] = replacements
manifest['revision'] = 'Shared hand-drawn logo substitution only; all copy, other art and placement unchanged'
manifest['current_revision_native_image_calls'] = 0
manifest['baseline_svg_sha256'] = sha(HERE / f'{BASE}.svg')
manifest['baseline_png_sha256'] = sha(HERE / f'{BASE}.png')
(HERE / f'{PREFIX}-text-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-o',str(HERE / f'{PREFIX}.png'),str(HERE / f'{PREFIX}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','900','-h','744','-o',str(HERE / f'{PREFIX}-small-preview.png'),str(HERE / f'{PREFIX}.svg')],check=True)

# Proof uses untouched complete PNGs through SVG viewports, not raster editing.
proof = ET.Element(tag('svg'),{'width':'900','height':'190','viewBox':'0 0 900 190'})
ET.SubElement(proof,tag('title')).text = 'Baseline logo left; hand-drawn shared logo right'
ET.SubElement(proof,tag('rect'),{'width':'900','height':'190','fill':'#fffdf7'})
for index, name in enumerate([BASE,PREFIX]):
    viewport = ET.SubElement(proof,tag('svg'),{'x':str(25+index*450),'y':'35','width':'400','height':'110',
        'viewBox':'756 467 287 78','overflow':'hidden','preserveAspectRatio':'xMidYMid meet'})
    ET.SubElement(viewport,tag('image'),{'href':uri(HERE / f'{name}.png'),'width':'1800','height':'1488'})
ET.SubElement(proof,tag('path'),{'d':'M450 19Q447 80 451 168','fill':'none','stroke':'#92a9ad','stroke-width':'1'})
(HERE / f'{PREFIX}-logo-proof.svg').write_text(ET.tostring(proof,encoding='unicode'))
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-o',str(HERE / f'{PREFIX}-logo-proof.png'),str(HERE / f'{PREFIX}-logo-proof.svg')],check=True)
print('Logo lockups replaced:',len(replacements),'source alpha crop:',crop,'output:',HERE/f'{PREFIX}.png')

