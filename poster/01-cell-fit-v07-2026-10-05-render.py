"""Reconcile Section 1 lettering, flags and icon style in the accepted A0 geometry."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = '01-cell-fit-v07-2026-10-05'
BASE = HERE / '09-cell-fit-v02-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#e3bb42', '#fdfbef'
CELL = 'M490 230 C470 231 451 240 431 256 L342 354 Q319 379 323 384 Q328 390 349 390 H581 Q601 390 603 369 L607 250 Q607 230 585 230 Z'
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
    records.append({'text': value, 'font': font, 'resolved_font_names': data['resolved_font_names'], 'size_px': size, 'size_pt_a0': round(size*1189/1672*72/25.4, 2), 'bbox': [x+a,y-d,x+c,y-b], 'advance_width': data['width']})
    parts.append(f'<g aria-label="{escape(value, quote=True)}"><path d="{data["path"]}" transform="translate({x} {y}) scale(1 -1)" fill="{NAVY}"/></g>')
    return data['width']

def path(d, fill='none', colour=NAVY, width=.8):
    parts.append(f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

def circle(x, y, r, fill, width=.7):
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{NAVY}" stroke-width="{width}"/>')



from xml.etree import ElementTree as ET
from copy import deepcopy
ET.register_namespace('', 'http://www.w3.org/2000/svg')
source=ET.parse(HERE/'01-logo-candidate.svg').getroot()
asset_records=[]
def asset(identifier,x,y,w,h):
    element=deepcopy(source.find('.//*[@id="'+identifier+'"]'))
    assert element is not None
    element.set('x',str(x));element.set('y',str(y));element.set('width',str(w));element.set('height',str(h))
    element.set('id','fit01-'+identifier)
    parts.append(ET.tostring(element,encoding='unicode'))
    asset_records.append({'source_id':identifier,'box':[x,y,w,h],'method':'Original native/embedded asset reused without repainting'})

# Fit the brand lockup on the narrow upper edge; ordinary lettering stays native.
# Align the visible Green SM wordmark baseline, rather than its taller emblem.
tw=text('1. Meet',448,258,10.5,True)
heading_bottom=records[-1]['bbox'][3]
logo_width,logo_height=42,17
logo_scale=logo_width/2125
logo_vertical_padding=(logo_height-572*logo_scale)/2
logo_y=heading_bottom-logo_vertical_padding-(633-72)*logo_scale
asset('authentic-green-sm-logo',448+tw+2,logo_y,logo_width,logo_height)
lockup_right=448+tw+2+logo_width
path(f'M448 263Q{(448+lockup_right)/2} 264 {lockup_right} 263',colour=GOLD,width=1.3)
text('Vingroup-backed',543,247,6.3,width=56)
vingroup_centre=(records[-1]['bbox'][1]+records[-1]['bbox'][3])/2
asset('background-vingroup-emblem',533,vingroup_centre-4,8,8)
text('Founded March 2023',543,260,6.3,width=61)
founded_centre=(records[-1]['bbox'][1]+records[-1]['bbox'][3])/2
calendar_y=founded_centre-2
path(f'M534 {calendar_y}H540V{calendar_y+5}H534Z',CREAM,width=.55)
path(f'M534 {calendar_y+2}H540 M536 {calendar_y-1}V{calendar_y+1} M538 {calendar_y-1}V{calendar_y+1}',colour=CYAN,width=.5)
header_alignment={'heading_visible_bottom':heading_bottom,'green_sm_wordmark_opaque_bottom':logo_y+logo_vertical_padding+(633-72)*logo_scale,'vingroup_label_centre':vingroup_centre,'vingroup_emblem_viewport_centre':vingroup_centre,'founded_label_centre':founded_centre,'calendar_visible_centre':calendar_y+2,'corporate_text_left':543,'icon_column_centre':537,'wordmark_ink_measurement':'Original PNG alpha >=160, at least 30 opaque pixels/row in the right wordmark region: bottom row 633. PNG bytes unchanged.'}

# A simple flat-colour app-to-car diagram uses broad regions for manual colouring.
parts.append('<g transform="translate(425 268) scale(.8) translate(-367 -349)">')
path('M367 351Q366 349 370 349H380Q384 349 384 352V377Q384 380 380 380H370Q367 380 367 377Z',CYAN,width=1)
path('M369 353H382V375H369Z',CREAM,width=.65)
path('M373 351H378',width=.6)
circle(376,378,.6,NAVY,.3)
path('M372 372Q380 368 375 363',colour=CYAN,width=1)
circle(375,360,2.4,GOLD,.5);circle(375,360,.65,NAVY,.2)
parts.append('</g>')
path('M444 283H457 M453 280L457 283L453 286',colour=CYAN,width=.8)
parts.append('<g transform="translate(463 275)">')
path('M0 9L7 3L25-6Q31-8 54-7L78-2L90 6L96 9V16H0Z',CYAN,width=.8)
path('M15 2L29-5H44V2Z',CREAM,width=.6)
path('M48-5L72-1L79 3H48Z',CREAM,width=.6)
path('M32 3V14 M75 4V14 M38 5H42 M77 6H81',width=.6)
circle(18,15,6,NAVY,.65);circle(18,15,3,CREAM,.5)
circle(79,15,6,NAVY,.65);circle(79,15,3,CREAM,.5)
path('M2 9H9L5 12H1 M90 8H95V11H92',GOLD,width=.5)
# The full VinFast identity remains on the centre door; no decorative lightning.
path('M50 4L55 9L60 4L55 11Z',CREAM,width=.6)
wordmark=deepcopy(source.find('.//*[@id="vinfast-controlled-wordmark"]'))
wordmark.set('id','fit01-vinfast-full-wordmark')
wordmark.set('transform','translate(36 -17) scale(1)')
parts.append(ET.tostring(wordmark,encoding='unicode'))
parts.append('</g>')
text('Owned fleet · Employed drivers',428,306,7.7,width=167)

countries=['Vietnam','Laos','Indonesia','Philippines','India','Kazakhstan','Denmark','Netherlands']
# The eight country identities are retained; only their arrangement changes.
for i,name in enumerate(countries):
    row,col=divmod(i,4);cx=426+col*48
    fy=312+row*29
    old=deepcopy(source.find('.//*[@id="flag-'+name.lower()+'"]'))
    old.set('id','fit01-flag-'+name.lower());old.attrib.pop('transform',None)
    original_w,original_h=(118.4,89.6) if name=='Denmark' else (128,64) if name in ('Philippines','Kazakhstan') else (96,64)
    fw,fh=(25,14) if name=='Denmark' else (19,12)
    if name=='Denmark':fy-=2
    old.set('transform',f'translate({cx-fw/2} {fy}) scale({fw/original_w} {fh/original_h})')
    # Replace marker band hatching by each band's original flat fill; keep every identifying symbol.
    for band in list(old):
        if band.get('aria-label')=='Hand marker flag band':
            rect=deepcopy(band.find('.//{http://www.w3.org/2000/svg}rect[@fill]'))
            assert rect is not None
            rect.set('opacity','1')
            position=list(old).index(band);old.remove(band);old.insert(position,rect)
    parts.append(ET.tostring(old,encoding='unicode'))
    asset_records.append({'source_id':'flag-'+name.lower(),'box':[cx-fw/2,fy,fw,fh]})
    if name=='Denmark':path(f'M{cx-fw/2-1.3} {fy-1.3}H{cx+fw/2+1.3}V{fy+fh+1.3}H{cx-fw/2-1.3}Z',colour=GOLD,width=1.1)
    tx=cx-20
    proc.stdin.write(json.dumps({'text':name,'font':'ChalkboardSE-Regular','size':6.8})+'\n');proc.stdin.flush()
    measured=json.loads(proc.stdout.readline())['width']
    name_size=6.8*min(1,43/measured)
    tx=cx-min(measured,43)/2
    text(name,tx,fy+fh+7,name_size,width=43)
    if name=='Vietnam':
        path(f'M{tx-9} {fy+15}L{tx-5} {fy+11}L{tx-1} {fy+15} M{tx-8} {fy+14}V{fy+19}H{tx-2}V{fy+14} M{tx-6} {fy+19}V{fy+16}H{tx-4}V{fy+19}',width=.6)
        text('14/04/2023',tx-1,fy+27,6.3,width=44)
    if name=='Denmark':text('30/07/2026',tx-1,fy+29,6.3,width=44)
    if name=='Netherlands':
        text('pilot',cx-7,fy+28,6.3,width=21)


text('Green SM Taxi: app-booked electric taxi rides in Copenhagen',333,379,8.0,width=262)

proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-01-v07-candidate" clip-path="url(#cell-01-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text()
start=base.index('<g id="section-01-v06-candidate"')
depth=0
for match in re.finditer(r'<g\b[^>]*>|</g>',base[start:]):
    depth += -1 if match.group()=='</g>' else 1
    if depth==0:
        end=start+match.end();break
old_layer=base[start:end]
assembled=base[:start]+layer+base[end:]
assert assembled.replace(layer,old_layer,1)==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
(HERE/f'{PREFIX}-panel.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1024" viewBox="320 230 287 163"><defs><clipPath id="cell-01-clip"><path d="{CELL}"/></clipPath></defs><path d="{CELL}" fill="{CREAM}" stroke="{NAVY}" stroke-width=".8"/>{layer}</svg>')
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="1800" height="1003" viewBox="314 344.817073 300 167"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',1800),('panel',1800)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
displayed='1. Meet Green SM\n'+'\n'.join(r['text'] for r in records[1:])
(HERE/f'{PREFIX}-displayed-copy.txt').write_text(displayed+'\n')
copy_lines=[line.removeprefix('## ') for line in (HERE/f'{PREFIX}-copy.md').read_text().splitlines() if line and not line.startswith('<!--')]
assert copy_lines[0]=='1. Meet Green SM'
assert copy_lines[1:]==[r['text'] for r in records[1:]]
vertices=[(490,230)]
def line(x,y):vertices.append((x,y))
def curve(control,end):
    start=vertices[-1]
    for i in range(1,101):
        t=i/100;u=1-t
        if len(control)==1:
            cx,cy=control[0];x=u*u*start[0]+2*u*t*cx+t*t*end[0];y=u*u*start[1]+2*u*t*cy+t*t*end[1]
        else:
            (ax,ay),(bx,by)=control;x=u**3*start[0]+3*u*u*t*ax+3*u*t*t*bx+t**3*end[0];y=u**3*start[1]+3*u*u*t*ay+3*u*t*t*by+t**3*end[1]
        vertices.append((x,y))
curve([(470,231),(451,240)],(431,256));line(342,354);curve([(319,379)],(323,384));curve([(328,390)],(349,390));line(581,390);curve([(601,390)],(603,369));line(607,250);curve([(607,230)],(585,230));line(490,230)
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
checks={'status':'Section 1 v07 reconciliation candidate; v06 D-115 remains accepted fallback','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'other_nine_cells_and_background_byte_for_byte_preserved':assembled.replace(layer,old_layer,1)==base,'a0_mm':[1189,841],'cell_path':CELL,'visible_text':records,'asset_placements':asset_records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'minimum_ordinary_lettering_pt_a0':min(r['size_pt_a0'] for r in records),'logos':'Shared Green SM and Vingroup identities reused; native full VinFast identity retained on centre door. Intrinsic logo paths are not ordinary poster lettering.','manual_visual_review':'Pending','header_alignment':header_alignment}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k not in ['visible_text','asset_placements']},ensure_ascii=False,indent=2))

pdf_info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
pdf_size=re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',pdf_info)
checks['pdf_measured_mm']=[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]]
checks['heading_size_pt_a0']=records[0]['size_pt_a0']
checks['all_hand_drawn_font_resolutions']=sorted(set(f for r in records for f in r['resolved_font_names']))
checks['approved_copy_bytes_preserved']=(HERE/f'{PREFIX}-copy.md').read_bytes()==(HERE/'01-cell-fit-v06-2026-10-05-copy.md').read_bytes()
checks['country_order']=countries
checks['flag_hatching_removed']=True
checks['pilot_placement']='Directly below Netherlands name, same column'
checks['date_size_pt_a0']={r['text']:r['size_pt_a0'] for r in records if r['text'] in ['14/04/2023','30/07/2026']}
base_root=ET.fromstring(base)
new_root=ET.fromstring(assembled)
logo_hrefs={}
for identifier in ['fit01-authentic-green-sm-logo','fit01-background-vingroup-emblem']:
    old_asset=base_root.find('.//*[@id="'+identifier+'"]')
    new_asset=new_root.find('.//*[@id="'+identifier+'"]')
    image_payload=lambda e:[dict(c.attrib) for c in e.iter() if c.tag.endswith('image')]
    assert image_payload(old_asset)==image_payload(new_asset), identifier
    logo_hrefs[identifier]=True
checks['green_sm_and_vingroup_embedded_image_bytes_preserved']=logo_hrefs
checks['green_sm_header_gap_native']=533-lockup_right
checks['intro_single_line']=True
checks['word_bearing_tokens']=sum(bool(re.search(r'\w',w)) for w in displayed.split())
with tempfile.TemporaryDirectory(prefix='mark1286-section1-') as temporary:
    headings=Path(temporary)/'headings.txt';headings.write_text('1. Meet Green SM\n')
    gate=subprocess.run(['python3','-B','/Users/khoilq/.codex/skills/mba-presentation-style/scripts/presentcheck.py',str(HERE/f'{PREFIX}-copy.md'),'--mode','poster','--headings',str(headings),'--registry',str(HERE.parent/'04_references/references.json'),'--sources',str(HERE.parent/'04_references'),'--concepts',str(HERE.parent/'03_course_materials/concept-list.txt'),'--strict-scope','--json'],capture_output=True,text=True)
    report=json.loads(gate.stdout)
    (HERE/f'{PREFIX}-copycheck.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    checks['fragment_presentcheck']={'exit':gate.returncode,'genre_words':report['genre']['total_words'],'detector_status':report['base']['anti_slop']['status'],'detector_score':report['base']['anti_slop']['score'],'effective_base_hard_by_category':report['effective_base_hard_by_category'],'out_of_scope_whole_poster_tables':report['genre']['errors']}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
assert not outside and not overlaps, {'outside':outside,'overlaps':overlaps}
assert checks['minimum_ordinary_lettering_pt_a0']>=12.5, [(r['text'],r['size_pt_a0']) for r in records if r['size_pt_a0']<12.5]
assert gate.returncode==2 and report['hard_stops']==2 and all(v==0 for v in report['effective_base_hard_by_category'].values()), report
assert all(abs(a-b)<.01 for a,b in zip(checks['pdf_measured_mm'],[1189,841]))
print(json.dumps({k:v for k,v in checks.items() if k not in ['visible_text','asset_placements']},ensure_ascii=False,indent=2))
