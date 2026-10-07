"""Apply approved numbered-heading and origin/pilot amendments to panel 1.
Run: uv run --with fonttools python -B <this file>. Reuses existing generated art.
The exact lettering comes from explicit local font files, without substitution.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import copy, hashlib, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

BASE = Path(__file__).resolve().with_name('panel-01-production-v04-2026-10-03')
OLD = BASE.with_name('panel-01-production-v03-2026-10-03')
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
root = ET.parse(Path(str(OLD)+'.svg')).getroot()
manifest = copy.deepcopy(json.loads(Path(str(OLD)+'-manifest.json').read_text()))
FONT_PATHS = {'heading': ('/System/Library/Fonts/MarkerFelt.ttc', 0),
              'body': ('/System/Library/Fonts/Noteworthy.ttc', 0),
              'strong': ('/System/Library/Fonts/Noteworthy.ttc', 1)}
FONTS = {kind: TTFont(path, fontNumber=index) for kind, (path, index) in FONT_PATHS.items()}

def glyph_group(t):
    font = FONTS[t['font_kind']]
    cmap = font.getBestCmap(); glyphs = font.getGlyphSet(); metrics = font['hmtx'].metrics
    scale = t['font_size']/font['head'].unitsPerEm
    g = ET.Element('{'+NS+'}g', {'id': t['id'], 'data-text': t['text'],
        'aria-label': t['text'], 'data-font-file': t['font_file'],
        'data-font-index': str(t['font_index'])})
    ET.SubElement(g, '{'+NS+'}title').text = t['text']
    bounds = []
    for i, line in enumerate(t.get('wrap', [t['text']])):
        names = [cmap.get(ord(ch)) for ch in line]
        assert all(names), 'Required handwriting glyph unavailable'
        width = sum(metrics[name][0] for name in names)*scale
        left = t['x']-width/2 if t['anchor']=='middle' else t['x']
        y = t['baseline_y'] if i==0 else t['second_line_y']; pos = 0
        for name in names:
            pen = SVGPathPen(glyphs); glyphs[name].draw(pen); d = pen.getCommands()
            if d:
                ET.SubElement(g, '{'+NS+'}path', {'d': d,
                    'transform': f'translate({left+pos*scale:.4f} {y:.4f}) scale({scale:.7f} {-scale:.7f})',
                    'fill': '#143B4A'})
            pos += metrics[name][0]
        bounds.append([left, y-t['font_size'], left+width, y+t['font_size']*.26])
    t['approx_bounds'] = bounds
    return g

removed_context = next(t for t in manifest['visible_text'] if t['id']=='footprint-context')
root.remove(root.find('.//*[@id="footprint-context"]'))
manifest['visible_text'] = [t for t in manifest['visible_text'] if t['id']!='footprint-context']
for t in manifest['visible_text']:
    if t['id']=='heading-meet':
        t.update({'text':'1. Meet', 'font_size':76.5, 'baseline_y':155})
    elif t['id'] in ['vietnam-launch','denmark-launch']:
        t['font_size'] = 25.5
    elif t['id'] in ['service-line','operating-model']:
        t['baseline_y'] -= 40
        if 'second_line_y' in t: t['second_line_y'] -= 40
    else:
        continue
    old = root.find('.//*[@id="'+t['id']+'"]'); ix = list(root).index(old)
    root.remove(old); root.insert(ix, glyph_group(t))

pilot = {'id':'netherlands-pilot','text':'pilot','x':1500,'baseline_y':340,
         'anchor':'start','font_size':20,'role':'display','font_kind':'body',
         'font_file':FONT_PATHS['body'][0],'font_index':0,
         'rendering':'Exact native glyph outlines; no font-family fallback',
         'relationship':'Raised annotation at the upper right of Netherlands label; no caret'}
label_ix = list(root).index(root.find('.//*[@id="country-netherlands"]'))
root.insert(label_ix+1, glyph_group(pilot)); manifest['visible_text'].append(pilot)

# Simple redrawable pen pictogram; no new image model or generated lettering.
home = ET.Element('{'+NS+'}g', {'id':'vietnam-origin-home','role':'img',
    'aria-label':'Home icon denoting Vietnam as the origin market'})
ET.SubElement(home, '{'+NS+'}title').text = 'Vietnam origin home icon'
for d, colour, width, opacity in [
    ('M 68 351 L 68 359 M 72 352 L 72 360 M 83 351 L 83 359', '#20C7CB', 3, '.45'),
    ('M 63 348 L 76 336 L 90 348 M 66 346 L 66 363 L 87 363 L 87 346', '#143B4A', 1.8, '1'),
    ('M 74 363 L 74 354 L 80 354 L 80 363', '#143B4A', 1.5, '1')]:
    ET.SubElement(home, '{'+NS+'}path', {'d':d,'fill':'none','stroke':colour,
        'stroke-width':str(width),'opacity':opacity,'stroke-linecap':'round','stroke-linejoin':'round'})
ix = list(root).index(root.find('.//*[@id="country-vietnam"]')); root.insert(ix, home)

# Replace the former two strokes with one closed four-sided marker frame.
old_highlight = next(e for e in root if e.get('d')=='M 1164 240 Q 1228 232 1320 238 M 1165 372 Q 1249 379 1316 373')
ix = list(root).index(old_highlight); root.remove(old_highlight)
frame_d = 'M 1176 228 Q 1240 225 1310 229 L 1311 330 Q 1244 334 1176 331 L 1175 229 Z'
frame = ET.Element('{'+NS+'}path', {'id':'denmark-focus-frame','d':frame_d,
    'fill':'none','stroke':'#FFCA00','stroke-width':'7','opacity':'.65',
    'stroke-linecap':'round','stroke-linejoin':'round','aria-label':'Four-sided yellow frame around the Danish flag'})
root.insert(ix, frame)
logo = root.find('.//*[@id="authentic-green-sm-logo"]')
logo.attrib.update({'x':'355','y':'49','width':'433.5','height':'117.3'})
underline = next(e for e in root if e.get('d')=='M 81 195 Q 280 202 487 193 T 814 198')
underline.set('d','M 81 183 Q 274 189 479 181 T 787 185')
divider = next(e for e in root if e.get('d')=='M 78 511 Q 820 517 1521 510')
divider.set('d','M 78 471 Q 820 477 1521 470')
root.find('.//*[@id="generated-hand-drawn-decoration"]').set('y','610')
root.find('{'+NS+'}desc').text = 'Panel 1 revised under D-056/D-057: numbered reduced heading, Vietnam home icon, smaller dates, yellow four-sided Danish frame and raised Dutch pilot annotation. Entire dated footprint line is removed from the face; its evidence date/count remain internal. Eight flags, exact service/model, handwriting treatment and original logo/artwork are retained. No visible citations or added corporate names.'

manifest['version'] = 'v04'; manifest['display_heading'] = '1. Meet Green SM'
manifest['status'] = 'Selected D-056/D-057 section revision preview; student imagery acceptance and actual A0 integration remain pending'
manifest['citation_display_history_v03'] = manifest.pop('citation_amendments')
manifest['citation_display_history_v03']['applied_in_version'] = 'v03'
manifest['approval'] = list(dict.fromkeys(manifest['approval']+['D-055','D-056','D-057']))
manifest['content_master'] = 'panel-01-selected-content-and-visual-v03-2026-10-03.md'
manifest['numbering_master'] = 'approved-poster-display-copy-v02-2026-10-03.md'
manifest['authentic_logo']['file'] = str(Path(str(BASE)+'-logo.svg').resolve())
manifest['authentic_logo']['placed_rect'] = [355,49,433.5,117.3]
manifest['generated_decoration']['file'] = str(Path(str(BASE)+'-art.png').resolve())
manifest['generated_decoration']['layout_y'] = 610
manifest['generated_decoration']['reused_from_version'] = 'v03; original raw art generated in v02'
manifest['composition_source'] = str(Path(str(BASE)+'-compose.py').resolve())
manifest['origin_icon'] = {'id':'vietnam-origin-home','type':'Controlled pen/marker SVG pictogram',
    'bounds':[63,336,90,363],'country_label_left':101.76,
    'meaning':'Vietnam origin; supersedes the literal Vietnamese origin label proposal'}
manifest['denmark_focus_frame'] = {'id':'denmark-focus-frame','type':'Closed four-sided yellow marker path',
    'path':frame_d,'stroke_width':7,'flag_rect':[1183.8,235.4,118.4,89.6]}
manifest['feedback_amendments'] = {'authority':['D-056','D-057'],
    'heading_font_scale_vs_v03':.85,'logo_width_height_scale_vs_v03':.85,
    'number_prefix_added':'1. ','date_font_scale_vs_v03':.85,'removed_display_context':removed_context,
    'added_visible_annotation':'pilot','added_origin_symbol':'Home icon before Vietnam',
    'body_translation_y':-40,'new_image_generation':False,'corporate_additions_approved':False,
    'current_display_object_ids':[t['id'] for t in manifest['visible_text']]}
manifest['footprint_metadata'] = {'count':8,'as_at':'26 September 2026','netherlands_status':'pilot',
    'evidence_id':'E-009','source_key':'green-sm-2026a','pdf_page':1,
    'scope':'Dated source context remains internal; removing its face line does not refresh the evidence'}
manifest['proposals_excluded'] = ['Literal Vietnamese origin label (superseded by approved icon)',
    'Full legal company name','Ninth country','Specific Danish Limo Green fleet identity',
    'VinFast name/logo addition','Vingroup name/logo addition']
manifest['sources'] = copy.deepcopy(manifest['sources'])
ET.indent(root, space='  ')
Path(str(BASE)+'.svg').write_text(ET.tostring(root,encoding='unicode')+'\n')
Path(str(BASE)+'-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('Created complete panel 1 feedback revision', BASE)
