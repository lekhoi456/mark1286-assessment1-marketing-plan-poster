"""Rebuild the approved panel with explicit handwriting fonts and measured chart geometry.

Run with: uv run --no-project --with fonttools python -B <this file>
Fonts remain in macOS. No font files are redistributed or copied to this workspace.
"""
from pathlib import Path
from html import escape
import base64
import hashlib
import json
import math
import random
import shutil
from fontTools.ttLib import TTCollection
from fontTools.pens.svgPathPen import SVGPathPen

HERE = Path(__file__).resolve().parent
STEM = 'panel-02-production-v04-2026-10-03'
OLD = 'panel-02-production-v03-2026-10-03'
ART = Path('/Users/KHOILQ/.codex/generated_images/01a10027-ee09-7f53-8a59-14552f63a1f2/exec-33df8326-1f63-4742-ab19-4717f155912e.png')
NAVY, CYAN, YELLOW, PAPER = '#1b344c', '#16b7c5', '#f3d349', '#fffef8'
FONT_FILES = {'heading': ('/System/Library/Fonts/MarkerFelt.ttc', 0, 'Marker Felt'), 'body': ('/System/Library/Fonts/Noteworthy.ttc', 1, 'Noteworthy')}
FONTS = {k: TTCollection(v[0]).fonts[v[1]] for k, v in FONT_FILES.items()}
GLYPHS = {k: v.getGlyphSet() for k, v in FONTS.items()}
RNG = random.Random(1286)
SHAPES, OUTLINED, EDITABLE, TEXTS, BARS = [], [], [], [], []

def path(d, colour=NAVY, width=2.5, fill='none', opacity=1, extra=''):
    SHAPES.append(f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')

def marker(x, y, width, height, colour, opacity=.22, strokes=5, clip=''):
    for i in range(strokes):
        yy = y + height * (i + .5) / strokes
        offset = RNG.uniform(-3, 3)
        d = f'M {x+RNG.uniform(-3,3):.3f} {yy:.3f} Q {x+width*.5:.3f} {yy+offset:.3f} {x+width+RNG.uniform(-3,3):.3f} {yy+RNG.uniform(-2,2):.3f}'
        path(d, colour, height/strokes*1.25, opacity=opacity, extra=clip)

def lettering(obj):
    ident, string = obj['id'], obj['text']
    kind = 'heading' if ident in ('p2-heading', 'p2-chart-title') else 'body'
    font, glyphs = FONTS[kind], GLYPHS[kind]
    size = obj['font_size']; scale = size/font['head'].unitsPerEm
    cmap, metrics = font.getBestCmap(), font['hmtx'].metrics
    assert all(ord(c) in cmap for c in string), f'No glyph fallback allowed: {string}'
    width = sum(metrics[cmap[ord(c)]][0] for c in string)*scale
    anchor = obj['text_anchor']; x, y = obj['x'], obj['baseline_y']
    left = x - (width/2 if anchor == 'middle' else width if anchor == 'end' else 0)
    rotation = obj['rotation']; letter_parts = []; advance = 0
    for char in string:
        name = cmap[ord(char)]; pen = SVGPathPen(glyphs); glyphs[name].draw(pen)
        commands = pen.getCommands()
        if commands:
            letter_parts.append(f'<path d="{commands}" transform="translate({left+advance*scale:.6f} {y}) scale({scale:.9f} {-scale:.9f})"/>')
        advance += metrics[name][0]
    common = f'id="{ident}" data-text="{escape(string, quote=True)}" data-font-file="{escape(FONT_FILES[kind][0])}" data-font-index="{FONT_FILES[kind][1]}"'
    OUTLINED.append(f'<g {common} fill="{obj.get("fill", NAVY)}" transform="rotate({rotation} {x} {y})">{"".join(letter_parts)}</g>')
    EDITABLE.append(f'<text {common} x="{x}" y="{y}" font-family="{FONT_FILES[kind][2]}" font-size="{size}" font-weight="{400 if kind=="heading" else 700}" font-kerning="none" text-anchor="{anchor}" fill="{obj.get("fill", NAVY)}" transform="rotate({rotation} {x} {y})">{escape(string)}</text>')
    obj.update(font_file=FONT_FILES[kind][0], font_collection_index=FONT_FILES[kind][1], font_family=FONT_FILES[kind][2], font_weight=400 if kind=='heading' else 700, measured_advance_width=width, left=left)
    TEXTS.append(obj)

manifest = json.loads((HERE/(OLD+'-text-manifest.json')).read_text())
SHAPES.append(f'<rect width="1800" height="1360" fill="{PAPER}"/>')
path('M 49 31 Q 565 24 1210 30 Q 1590 26 1750 37 L 1764 339 Q 1758 655 1763 935 L 1757 1329 Q 1200 1337 810 1332 L 45 1330 Q 36 1032 42 732 L 40 40', width=2.2, opacity=.55)
marker(65, 71, 490, 28, YELLOW, .20, 4)
path('M 69 161 Q 356 164 749 158', CYAN, 3.5, opacity=.65)
marker(575, 320, 288, 71, YELLOW, .30, 6)
path('M 582 334 Q 583 323 607 322 L 838 324 Q 862 322 865 339 L 860 376 Q 859 390 839 389 L 595 387 Q 580 384 582 334', width=2.0, opacity=.8)
path('M 210 654 Q 634 656 1008 653 Q 1341 657 1629 655', width=2.3)
for tick in range(4):
    yy = 655 - tick*100000*253.8/350000*1.1
    path(f'M 205 {yy+1:.4f} Q 211 {yy-1:.4f} 218 {yy:.4f}', width=2)
centres = [175.096415*2.1-7.7, 348.669472*2.1-7.7, 522.242528*2.1-7.7, 695.815585*2.1-7.7]
for i, (centre, count) in enumerate(zip(centres, [72396, 269277, 143668, 74728])):
    width = 215.0570163; height = count*253.8/350000*1.1; top = 655-height; left = centre-width/2; right = centre+width/2
    ident = f'p2-bar-{i+1}'; clip = f'bar-clip-{i+1}'
    SHAPES.append(f'<defs><clipPath id="{clip}"><rect x="{left:.9f}" y="{top:.9f}" width="{width:.9f}" height="{height:.9f}"/></clipPath></defs>')
    marker(left+3, top, width-6, height, CYAN if i==1 else '#80bbc3', .36 if i==1 else .18, max(5, math.ceil(height/10)), f'clip-path="url(#{clip})"')
    d = f'M {left:.6f} 655 L {left+1.7:.6f} {655-height*.55:.6f} L {left+.2:.6f} {top+10:.6f} Q {left+22:.6f} {top+.6:.6f} {centre:.6f} {top:.6f} Q {right-23:.6f} {top+1.1:.6f} {right-1:.6f} {top+2:.6f} L {right-2:.6f} {top+height*.48:.6f} L {right:.6f} 655 Q {centre:.6f} 654.5 {left:.6f} 655 Z'
    path(d, width=2.2, extra=f'id="{ident}" data-count="{count}" data-baseline="655" data-true-top="{top:.9f}" data-true-height="{height:.9f}"')
    BARS.append({'id': ident, 'count': count, 'baseline': 655, 'true_top': top, 'true_height': height, 'width': width, 'marker_clip': clip})
path('M 725 795 Q 744 807 877 815 M 863 807 L 877 815 L 863 822', CYAN, 2.7)
marker(542, 844, 729, 26, CYAN, .11, 3)
path('M 567 839 Q 549 838 552 854 L 568 875 Q 587 854 582 844 Q 578 838 567 839 Z', width=2.3, fill='#f5e8a4')
path('M 566 848 Q 574 844 574 853 Q 568 860 565 853 Q 564 850 566 848 Z', width=1.5)
marker(749, 918, 313, 14, YELLOW, .13, 2)
path('M 83 951 Q 72 921 144 918 Q 152 893 213 911 Q 453 890 667 925 Q 712 913 719 951 Q 746 982 716 1192 Q 685 1227 621 1207 Q 333 1231 157 1206 Q 90 1228 94 1178 Q 62 1090 83 951', width=1.9, opacity=.4)
path('M 743 964 Q 754 955 762 966 Q 758 977 746 970 M 779 978 Q 784 972 788 979', width=1.8, opacity=.5)
path('M 1061 986 Q 1078 978 1091 980 M 1063 1101 Q 1082 1094 1094 1101', CYAN, 1.8, opacity=.45)
marker(109, 1271, 1580, 48, YELLOW, .24, 5)
path('M 103 1324 Q 895 1320 1689 1325', YELLOW, 2.5, opacity=.65)
art_bytes = ART.read_bytes(); shutil.copyfile(ART, HERE/(STEM+'-generated-art.png'))
SHAPES.append(f'<defs><image id="p2-generated-art" width="1536" height="1024" href="data:image/png;base64,{base64.b64encode(art_bytes).decode()}"/><clipPath id="p2-resident-clip"><path d="M 610 235 L 930 235 L 930 500 L 995 500 L 995 870 L 500 870 L 500 520 L 610 520 Z"/></clipPath></defs>')
islands = [('price',[80,95,440,285],[87,932,122,88]),('route',[65,385,435,300],[87,1018,122,94]),('support',[90,687,425,285],[87,1108,122,90]),('resident',[500,235,490,620],[777,936,250,304]),('taxi',[970,100,520,320],[1104,931,124,91]),('calendar',[1020,405,490,285],[1104,1020,124,90]),('wallet',[1010,697,485,285],[1104,1104,124,93])]
for name, source, target in islands:
    vx, vy, vw, vh = source; x, y, w, h = target
    use = '<g clip-path="url(#p2-resident-clip)"><use href="#p2-generated-art"/></g>' if name == 'resident' else '<use href="#p2-generated-art"/>'
    SHAPES.append(f'<svg id="p2-illustration-{name}" x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vx} {vy} {vw} {vh}" overflow="hidden" preserveAspectRatio="xMidYMid meet">{use}</svg>')
sizes = {'p2-heading':70,'p2-priority':46,'p2-filters':36,'p2-chart-title':40,'p2-chart-scope':30,'p2-axis-title':28,'p2-share':36,'p2-share-basis':28,'p2-source':28,'p2-denominator':28,'p2-location':34,'p2-profile-qualifier':36,'p2-rationale':38}
for i, obj in enumerate(manifest['text_objects']):
    obj['font_size'] = sizes.get(obj['id'], 27 if obj['id'].startswith('p2-y-') else 35 if obj['id'].startswith(('p2-count-', 'p2-age-')) else 36)
    obj['rotation'] = [0.25,-.35,.18,-.22,.28,-.15,.20][i%7]
    if obj['id']=='p2-heading': obj['rotation']=-.55
    if obj['id']=='p2-heading': obj['baseline_y']=100
    if obj['id']=='p2-filters': obj['baseline_y']=210
    if obj['id'].startswith('p2-y-'): obj['x']=195
    if obj['id']=='p2-share': obj['baseline_y']=353
    if obj['id']=='p2-share-basis': obj['baseline_y']=380
    if obj['id']=='p2-rationale': obj['baseline_y']=1304
    lettering(obj)
assert len(TEXTS)==31
prefix = '<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1360" viewBox="0 0 1800 1360"><title>Target Market — approved content, hand-drawn production revision</title>'
(HERE/(STEM+'.svg')).write_text(prefix+''.join(SHAPES)+''.join(OUTLINED)+'</svg>')
(HERE/(STEM+'-editable.svg')).write_text(prefix+''.join(SHAPES)+''.join(EDITABLE)+'</svg>')
manifest.update(version='v04', text_objects=TEXTS, typography={'rendering':'Portable SVG glyph outlines generated directly from explicit local font files, with a companion native-text editable SVG; no sans fallback or font redistribution','font_files':FONT_FILES,'minimum_size':27}, chart_geometry={'baseline':655,'pixels_per_resident':253.8/350000*1.1,'bars':BARS,'zero_baseline':True,'styling':'Thin irregular perimeter and translucent marker strokes clipped to true mathematical bar rectangles; no ruler grid or solid uniform bars'}, illustrations={'generated':True,'tool':'built-in image_gen__imagegen','art_file':STEM+'-generated-art.png','art_sha256':hashlib.sha256(art_bytes).hexdigest(),'native_bytes_retained':True,'viewports':[{'name':n,'source':s,'target':t} for n,s,t in islands]}, style_authority='shared-hand-drawn-style-revision-v01-2026-10-03.md; student style rejection/approved revision, parent log owner')
manifest['canvas']['minimum_native_font_size']=27
manifest['canvas']['physical_minimum_at_proposed_width_mm']=27*330/1800
manifest['canvas']['physical_minimum_at_proposed_width_pt']=27*330/1800*72/25.4
manifest['placement_rules']=['Exact approved strings are rendered through explicit handwriting font files; final portable SVG outlines avoid fallback and the companion SVG retains native editable text.','The 40.2% pill stays above the highlighted 25–44 bar, with 269,277 separate.','Every bar uses the unchanged counts and mathematical zero-baseline height; only the perimeter and clipped marker fill are irregular.','Keep source/date/all-city denominator and Proposed rider profile readable.','Joining the exact six profile labels with the approved middle-dot separator reproduces both selected triplets.','The original generated art bytes are retained. Native viewports and a resident-only clip exclude neighbouring icon fragments; no pixels or data are redrawn by an image model.']
(HERE/(STEM+'-text-manifest.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Wrote complete portable lettering SVG, editable text SVG, native generated art and exact text/data manifest.')
print('All 31 text objects use the explicit handwriting files; mathematical heights retained for all four bars.')
