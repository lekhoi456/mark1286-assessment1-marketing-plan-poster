"""Reconcile the branding board using two approved removals and a larger layered UI cue."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '04-cell-fit-v02-2026-10-05'
BASE = HERE / '03-cell-fit-v07-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#e3bb42', '#fdfbef'
CELL = 'M1286 231 Q1354 234 1401 250 Q1436 261 1456 287 L1497 367 Q1512 389 1495 390 H1293 Q1272 390 1271 370 L1264 251 Q1263 231 1286 231 Z'
parts, records = [], []
proc = subprocess.Popen(['/usr/bin/swift', str(HERE / '08-cell-fit-v01-2026-10-05-glyphs.swift')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def text(value, x, y, size=6.6, heading=False, width=None):
    font = 'MarkerFelt-Wide' if heading else 'ChalkboardSE-Regular'
    def glyph(size):
        proc.stdin.write(json.dumps({'text': value, 'font': font, 'size': size}, ensure_ascii=False) + '\n')
        proc.stdin.flush()
        result = json.loads(proc.stdout.readline())
        if 'error' in result:
            raise RuntimeError(result['error'])
        assert all(f in (font, 'Native vector arrow', 'Native vector maths') for f in result['resolved_font_names']), {'text':value, 'resolved':result['resolved_font_names']}
        return result
    data = glyph(size)
    if width and data['width'] > width:
        size *= width / data['width']
        data = glyph(size)
    a, b, c, d = data['bounds']
    records.append({'text': value, 'font': font, 'resolved_font_names': data['resolved_font_names'], 'size_px': size, 'size_pt_a0': round(size*1189/1672*72/25.4, 2), 'bbox': [x+a,y-d,x+c,y-b], 'advance_width': data['width'], 'maximum_width': width})
    parts.append(f'<g aria-label="{escape(value, quote=True)}"><path d="{data["path"]}" transform="translate({x} {y}) scale(1 -1)" fill="{NAVY}"/></g>')
    return data['width']

def path(d, fill='none', colour=NAVY, width=.8):
    parts.append(f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

def circle(x, y, r, fill, width=.7):
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{NAVY}" stroke-width="{width}"/>')



from xml.etree import ElementTree as ET
from copy import deepcopy
ET.register_namespace('', 'http://www.w3.org/2000/svg')
source=ET.parse(HERE.parent/'archive/04-candidate-v02-2026-10-04.svg').getroot()
logo=deepcopy(next(e for e in source if e.tag.endswith('image')))
# Reuse the exact approved-source hand-drawn logo pixels, placing them within the narrow roof portion.
logo.set('x','1278');logo.set('y','261');logo.set('width','100');logo.set('height','26')
parts.append(ET.tostring(logo,encoding='unicode'))

def centred(value,left,right,y,size=6.8,heading=False):
    w=text(value,left,y,size,heading,width=right-left)
    shift=(right-left-w)/2
    parts[-1]=parts[-1].replace(f'translate({left} {y})',f'translate({left+shift} {y})')
    records[-1]['bbox'][0]+=shift;records[-1]['bbox'][2]+=shift

w=text('4. Branding & Identity',1278,256,10.5,True,width=120)
path(f'M1278 260Q{1278+w/2} 261 {1278+w} 260',colour=GOLD,width=1.2)
text('Green SM =',1278,295,7.4,True,width=106)
text('Green and Smart Mobility',1278,307,7.4,width=114)
# Corporate slogan is the dominant message beneath the logo/name meaning.
text('Go Green For',1278,319,9.2,True,width=114)
text('a Green Future.',1278,331,9.2,True,width=114)
# Palette follows the expanding diagonal; swatches are broad solid colour shapes.
text('Primary',1394,275,6.6,width=45)
circle(1399,285,6,CYAN,.75)
text('New Cyan',1408,286,7.1,True,width=46)
text('#28bdbf',1394,298,6.6,width=62)
text('Pantone 319 C',1394,310,6.6,width=65)
text('Secondary',1394,322,6.6,width=65)
circle(1399,334,6,'#e3bb42',.75)
text('New Yellow',1408,335,7.1,True,width=68)
text('#e3bb42',1408,347,6.6,width=62)
# Keep the corporate typeface name without substituting a literal font specimen.
text('Xanh Display 2.0',1317,342,7.5,width=82)
# A larger phone with offset, solid-colour interface panels communicates layering.
path('M1285 337Q1280 337 1280 342V372Q1280 377 1285 377H1301Q1306 377 1306 372V342Q1306 337 1301 337Z',CREAM,width=.95)
path('M1284 343Q1292 342 1302 343V370Q1292 371 1284 370Z','#e9f7f5',colour=CYAN,width=.65)
path('M1286 347Q1292 346 1299 347V355Q1292 357 1286 355Z',CYAN,width=.55)
path('M1289 353Q1295 351 1302 353V361Q1295 363 1289 361Z',CREAM,colour=CYAN,width=.65)
path('M1287 361Q1293 359 1300 361V367Q1293 369 1287 367Z',GOLD,width=.55)
path('M1288 340H1298 M1290 374H1297',width=.55)
text('Modern Liquid Glass UI/UX',1317,355,7.3,True,width=153)
text('Layered · soft · clear',1317,367,7.0,width=153)
# Global secondary tagline belongs to the later header assembly; omit it here.
centred('Danish first · English second',1317,1487,381,7.0)
proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-04-v02-candidate" clip-path="url(#cell-04-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text()
start=base.index('<g id="section-04-v01-candidate"')
depth=0
for match in re.finditer(r'<g\b[^>]*>|</g>',base[start:]):
    depth += -1 if match.group()=='</g>' else 1
    if depth==0:
        end=start+match.end();break
old_layer=base[start:end]
assembled=base[:start]+layer+base[end:]
assert assembled.replace(layer,old_layer,1)==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
(HERE/f'{PREFIX}-panel.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1344" viewBox="1258 226 253 170"><defs><clipPath id="cell-04-clip"><path d="{CELL}"/></clipPath></defs><path d="{CELL}" fill="{CREAM}" stroke="{NAVY}" stroke-width=".8"/>{layer}</svg>')
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="2000" height="1344" viewBox="1258 344.817073 253 170"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',2000),('panel',2000)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text('\n'.join(r['text'] for r in records)+'\n')
vertices=[(1286,231)]
def line(x,y):vertices.append((x,y))
def curve(ctrl,end):
    start=vertices[-1]
    for i in range(1,101):
        t=i/100;u=1-t
        vertices.append((u*u*start[0]+2*u*t*ctrl[0]+t*t*end[0],u*u*start[1]+2*u*t*ctrl[1]+t*t*end[1]))
curve((1354,234),(1401,250));curve((1436,261),(1456,287));line(1497,367);curve((1512,389),(1495,390));line(1293,390);curve((1272,390),(1271,370));line(1264,251);curve((1263,231),(1286,231))
def inside(x,y):
    hit=False
    for (ax,ay),(bx,by) in zip(vertices,vertices[1:]+vertices[:1]):
        if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:hit=not hit
    return hit
outside=[];overlaps=[]
for i,r in enumerate(records):
    a=r['bbox']
    if not all(inside(x,y) for x in [a[0],a[2]] for y in [a[1],a[3]]):outside.append(r)
    for other in records[i+1:]:
        b=other['bbox']
        if min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1]):overlaps.append([r['text'],other['text']])
from collections import Counter
pdf_info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
pdf_size=re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',pdf_info)
copy_report=json.loads((HERE/f'{PREFIX}-copy-check.json').read_text())
expected=[line.removeprefix('## ') for line in (HERE/f'{PREFIX}-copy.md').read_text().splitlines() if line and not line.startswith(('# Section','<!--'))]
previous=json.loads((HERE/'04-cell-fit-v01-2026-10-05-checks.json').read_text())['visible_text']
removed=['Aa','Clear terms. Local care.']
image_hrefs=lambda markup: [e.attrib.get('{http://www.w3.org/1999/xlink}href',e.attrib.get('href')) for e in ET.fromstring(markup).iter() if e.tag.endswith('image')]
old_payloads=image_hrefs(old_layer)
new_payloads=image_hrefs(layer)
logo_sha=hashlib.sha256(new_payloads[0].encode()).hexdigest()
checks={
    'status':'Section 4 v02 candidate under D-134; student review pending',
    'base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),
    'other_nine_cells_and_background_byte_for_byte_preserved':assembled.replace(layer,old_layer,1)==base,
    'restored_base_sha256':hashlib.sha256(assembled.replace(layer,old_layer,1).encode()).hexdigest(),
    'replacement_layer_id':'section-04-v02-candidate',
    'old_layer_occurrences_after_replacement':assembled.count('id="section-04-v01-candidate"'),
    'new_layer_occurrences':assembled.count('id="section-04-v02-candidate"'),
    'cell_path':CELL,'native_cell_unchanged':CELL in base and CELL in assembled,
    'a0_mm':[1189,841],
    'pdf_measured_mm':[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]],
    'pdf_page_count':int(re.search(r'Pages:\s*(\d+)',pdf_info).group(1)),
    'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,
    'width_violations':[r for r in records if r['maximum_width'] and r['advance_width']>r['maximum_width']+1e-6],
    'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records[1:]),
    'heading_size_pt_a0':records[0]['size_pt_a0'],
    'exact_display_copy_multiset_matches':Counter(expected)==Counter(r['text'] for r in records),
    'all_other_v01_displayed_strings_preserved':Counter(r['text'] for r in previous if r['text'] not in removed)==Counter(r['text'] for r in records),
    'approved_removals':removed,
    'global_tagline_retained_in_notes_for_later_header_assembly':'Clear terms. Local care.',
    'global_tagline_not_added_to_other_cells_or_header':assembled.count('aria-label="Clear terms. Local care."')==base.count('aria-label="Clear terms. Local care."')-1,
    'logo_embedded_payload_unchanged':old_payloads==new_payloads,
    'logo_embedded_payload_sha256':logo_sha,
    'logo_matches_approved_archive_source':new_payloads==image_hrefs(ET.tostring(next(e for e in source if e.tag.endswith('image')),encoding='unicode')),
    'all_other_embedded_images_byte_for_byte_preserved':image_hrefs(base)==image_hrefs(assembled),
    'artwork_geometry_boxes_inside_cell':all(inside(x,y) for x in [1280,1306] for y in [337,377]),
    'layered_phone_native_box':[1280,337,1306,377],
    'heading_underline_width_native':records[0]['advance_width'],
    'heading_underline_matches_text_width':f'M1278 260Q{1278+records[0]["advance_width"]/2} 261 {1278+records[0]["advance_width"]} 260' in layer,
    'language_line_size_pt_a0':records[-1]['size_pt_a0'],
    'language_line_bottom_clearance_native':390-records[-1]['bbox'][3],
    'palette':{'navy':NAVY,'cyan':CYAN,'gold':GOLD,'cream':CREAM},
    'fragment_presentcheck':{'exit':2,'genre_words':copy_report['genre']['total_words'],'detector_status':copy_report['base']['anti_slop']['status'],'detector_score':copy_report['base']['anti_slop']['score'],'effective_base_hard_by_category':copy_report['effective_base_hard_by_category'],'whole_poster_tables_outside_fragment':copy_report['genre']['errors']},
    'manual_visual_review':'Producer inspected panel, fitted close-up and full A0: corporate identity remains dominant, overlapping flat phone panels read as layering, language line clears the bottom edge; controller/student review pending.'
}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
assert not outside and not overlaps, {'outside':outside,'overlaps':overlaps}
assert not checks['width_violations'] and checks['minimum_ordinary_lettering_pt_a0']>=12.5
assert checks['other_nine_cells_and_background_byte_for_byte_preserved'] and checks['restored_base_sha256']==checks['base_sha256']
assert checks['old_layer_occurrences_after_replacement']==0 and checks['new_layer_occurrences']==1
assert checks['exact_display_copy_multiset_matches'] and checks['all_other_v01_displayed_strings_preserved']
assert checks['logo_embedded_payload_unchanged'] and checks['logo_matches_approved_archive_source'] and checks['all_other_embedded_images_byte_for_byte_preserved']
assert checks['artwork_geometry_boxes_inside_cell'] and checks['global_tagline_not_added_to_other_cells_or_header']
assert checks['heading_underline_matches_text_width'] and checks['language_line_size_pt_a0']>=13
assert 20<=checks['heading_size_pt_a0']<=22 and checks['pdf_page_count']==1
assert all(abs(a-b)<.01 for a,b in zip(checks['pdf_measured_mm'],[1189,841]))
assert copy_report['hard_stops']==2 and all(v==0 for v in copy_report['effective_base_hard_by_category'].values())
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
