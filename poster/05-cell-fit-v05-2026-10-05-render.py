"""Section 5 trial reflow; preserve the A0 base byte-for-byte before insertion."""
from pathlib import Path
from html import escape
import json
import subprocess
import hashlib
import re
import runpy

HERE = Path(__file__).resolve().parent
PREFIX = '05-cell-fit-v05-2026-10-05'
INK, CYAN, GOLD = '#173a47', '#28bdbf', '#e3bb42'
BASE = HERE / '06-cell-fit-v04-2026-10-05-poster.svg'
CELL = 'M309 400 H587 Q610 400 611 423 V575 Q611 598 587 598 H374 Q338 598 310 578 Q260 541 260 499 Q260 448 285 419 Q296 400 309 400 Z'
proc = subprocess.Popen(['/usr/bin/swift', str(HERE / '05-cell-fit-v03-2026-10-04-glyphs.swift')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
parts, records = [], []

def glyph(value, size, heading=False):
    proc.stdin.write(json.dumps({'text': value, 'font': 'MarkerFelt-Wide' if heading else 'ChalkboardSE-Regular', 'size': size}, ensure_ascii=False)+'\n')
    proc.stdin.flush()
    result = json.loads(proc.stdout.readline())
    if 'error' in result:
        raise RuntimeError(result['error'])
    assert all(f in ('MarkerFelt-Wide','ChalkboardSE-Regular','Native vector arrow') for f in result['resolved_font_names']),result
    return result

def text(value, x, y, size=6.2, heading=False, width=None):
    data = glyph(value, size, heading)
    requested_size = size
    if width and data['width'] > width:
        size = size * width / data['width']
        data = glyph(value, size, heading)
    a,b,c,d = data['bounds']
    records.append({'text':value, 'requested_size_px':requested_size, 'resolved_font_names':data['resolved_font_names'], 'size_px':size, 'size_pt_a0':round(size*1189/1672*72/25.4,2), 'bbox':[x+a,y-d,x+c,y-b], 'advance_width':data['width']})
    parts.append(f'<g aria-label="{escape(value,quote=True)}"><path d="{data["path"]}" transform="translate({x} {y}) scale(1 -1)" fill="{INK}"/></g>')

def lines(values, x, y, size=6.2, step=7.7, heading=False, width=None):
    for i,value in enumerate(values):
        text(value,x,y+i*step,size,heading,width)

def stroke(d, colour=CYAN, width=1):
    parts.append(f'<path d="{d}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')

def arrow(x1,y,x2, colour=CYAN):
    stroke(f'M{x1} {y} L{x2} {y} M{x2-3} {y-2} L{x2} {y} L{x2-3} {y+2}',colour,.9)

def icon(kind,x,y):
    parts.append(f'<g transform="translate({x} {y})">')
    if kind == 'car':
        stroke('M0 5 L2 1 Q5 -1 9 1 L12 5 L11 8 L1 8Z',CYAN,.8)
        parts.append(f'<circle cx="3" cy="8" r="1.2" fill="{INK}"/><circle cx="9" cy="8" r="1.2" fill="{INK}"/>')
    elif kind == 'tag':
        stroke('M0 1 L8 1 L12 5 L8 9 L0 9Z',INK,.7)
        parts.append(f'<circle cx="3" cy="4" r="1" fill="{GOLD}"/>')
    elif kind == 'phone':
        stroke('M3 0 L8 0 Q10 0 10 2 L10 10 Q10 12 8 12 L3 12 Q1 12 1 10 L1 2 Q1 0 3 0Z M4 10 L7 10',INK,.7)
        stroke('M3 3 L8 3 M3 5 L8 5',CYAN,.55)
    elif kind == 'browser':
        stroke('M0 1 L12 1 L12 11 L0 11Z M0 4 L12 4 M3 7 L9 7',INK,.7)
        parts.append(f'<circle cx="2" cy="2.5" r=".5" fill="{GOLD}"/>')
    elif kind == 'speaker':
        stroke('M0 3 L9 0 L9 7 L0 5Z M2 5 L3 9 L5 9 L4 6 M11 1 L13 0 M11 4 L14 4 M11 7 L13 8',CYAN,.7)
    parts.append('</g>')


# Insight band: two source populations and three independent marks.
text('5. Digital Marketing',350,420,10.5,True,width=246)
heading_end=350+records[0]['advance_width']
stroke(f'M350 424Q{(350+heading_end)/2} 425 {heading_end} 424',GOLD,1.5)
text('Denmark · n=1,005',350,435,6.2,width=100)
text('40–50%',350,448,9.5,True)
text('one app',407,448,7,width=50)
stroke('M350 456H447','#d8e7e2',3)
stroke('M350 456H388.8',CYAN,3)
parts.append(f'<path d="M388.8 456H398.5" stroke="{CYAN}" stroke-width="3" stroke-dasharray="1 1"/>')
text('Capital Region · n=79',469,435,6.2,width=130)
text('Lower price',469,446,6.8,width=91)
text('57%',578,446,8,True,width=25)
stroke('M469 451H599','#d8e7e2',2.3)
stroke('M469 451H543.1',CYAN,2.3)
text('Usual app',469,462,6.8,width=91)
text('22%',578,462,8,True,width=25)
stroke('M469 467H599','#d8e7e2',2.3)
stroke('M469 467H497.6',GOLD,2.3)
stroke('M350 471H603','#b8d9d6',.6)

# Applied 4Ps occupy the curved left rail.
text('Marketing Mix',282,454,6.9,True,width=65)
text('4Ps*',282,463,7.5,True,width=65)
icon('car',282,467)
text('Product',298,472,7.1,True,width=47)
text('Electric + service',280,483,6.6,width=66)
icon('tag',277,490)
text('Price',293,498,7.1,True,width=47)
text('Clear fare + trial',277,508,6.6,width=67)
icon('browser',281,514)
text('Place',297,522,7.1,True,width=48)
text('Page → app',281,532,6.6,width=66)
icon('speaker',291,537)
text('Promotion',307,546,7.1,True,width=49)
text('Search / social',300,556,6.6,width=64)
text('/ reminders',306,565,6.6,width=64)
text('*Proposed',315,573,6.2,width=49)
stroke('M343 439V552','#b8d9d6',.6)

# One central acquisition journey; broad native vector shapes replace raster detail.
text('Omni Channel · Search / SEO / Social',350,479,7.6,True,width=250)
parts.append(runpy.run_path(str(HERE/f'{PREFIX}-illustrations.py'))['journey_art']())
arrow(426,508,439)
arrow(481,508,492)
text('Copenhagen page',350,540,7.1,True,width=82)
text('Green SM app',435,540,7.1,True,width=57)
text('Ride + help',516,540,7.5,True,width=84)
text('Same fares / offers / help',391,548,6.8,width=209)

# Activation offers on the left; a separately bounded data lane on the right.
parts.append(f'<path d="M358 555H424Q430 555 430 560V563Q423 567 430 571V578Q430 581 424 581H358Q354 581 354 577V571Q361 567 354 563V559Q354 555 358 555Z" fill="{GOLD}" stroke="{INK}" stroke-width=".7"/>')
text('10% vs 20%',362,566,8.3,True,width=64)
text('First paid ride',360,577,6.6,True,width=65)
stroke('M440 553H463V572H440Z M440 558H463 M445 551V556 M458 551V556',INK,.8)
text('30',445,570,9,True,width=16)
text('30-day paid*',433,580,6.2,True,width=63)
text('Max DKK30 · 400 cap · 1/rider',343,586,6.2,width=217)
parts.append('<rect x="474" y="554" width="130" height="29" rx="3" fill="#edf8f5" stroke="#8cc7c3" stroke-width=".75"/>')
text('DATA*',478,561,7,True,width=38)
text('Opt-in · proposed',523,561,6.2,width=77)
text('CDP join → Big Data patterns',478,571,6.6,True,width=122)
text('Marketing AI reminders · human review',478,579.5,6.2,width=122)

# Timeline sits on the lower shoulder; figures/check timing unchanged.
for x,w,label,fill in [(375,56,'M1–2 Verify','#e9f8f5'),(434,99,'M3–6 Test · M4/M6 checks','#fff4b9'),(535,65,'M7–12 Scale if OK','#e9f8f5')]:
    parts.append(f'<rect x="{x}" y="589" width="{w}" height="8" rx="1.5" fill="{fill}"/>')
    text(label,x+2,595.5,6.2,True,width=w-4)

proc.stdin.close();proc.wait(timeout=15)
if proc.returncode:raise RuntimeError(proc.stderr.read())
layer='<g id="section-05-v05-candidate" clip-path="url(#cell-05-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text();start=base.index('<g id="section-05-v04-candidate"');depth=0;end=None
for match in re.finditer(r'<g\b[^>]*>|</g>',base[start:]):
    depth+= -1 if match.group()=='</g>' else 1
    if depth==0:end=start+match.end();break
assert end is not None
old_layer=base[start:end]
assembled=base[:start]+layer+base[end:]
assert assembled.replace(layer,old_layer,1)==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
standalone=f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1036" viewBox="250 395 365 210"><defs><clipPath id="cell-05-clip"><path d="{CELL}"/></clipPath></defs><path d="{CELL}" fill="#fdfbef" stroke="{INK}" stroke-width=".8"/>{layer}</svg>'
(HERE/f'{PREFIX}-panel.svg').write_text(standalone)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="1800" height="1036" viewBox="250 515.817073 365 210"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
# Check rounded-cell containment and all text pairs before exporting.
vertices=[(309,400)]
def line(x,y):vertices.append((x,y))
def curve(ctrl,end):
    start=vertices[-1]
    for i in range(1,201):
        t=i/200;u=1-t
        vertices.append((u*u*start[0]+2*u*t*ctrl[0]+t*t*end[0],u*u*start[1]+2*u*t*ctrl[1]+t*t*end[1]))
line(587,400);curve((610,400),(611,423));line(611,575);curve((611,598),(587,598));line(374,598);curve((338,598),(310,578));curve((260,541),(260,499));curve((260,448),(285,419));curve((296,400),(309,400))
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
assert not outside,outside
assert not overlaps,overlaps
for suffix,width in [('poster',2400),('panel',1800),('close-up',1800)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text('\n'.join(r['text'] for r in records)+'\n')
info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
size=re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',info)
checks={'status':'D-134 Section 5 improvement candidate awaiting student review. Accepted Section 6 v04 D-136 preserved.','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'other_nine_cells_and_background_byte_for_byte_preserved':assembled.replace(layer,old_layer,1)==base,'cell_path':CELL,'visible_text':records,'glyph_bbox_corners_outside_native_cell':outside,'pairwise_text_overlaps':overlaps,'min_pt':min(r['size_pt_a0'] for r in records),'pdf_measured_mm':[round(float(size.group(i))*25.4/72,3) for i in [1,2]],'new_raster_assets':0,'source_scope':'Denmark n=1005; Capital Region n=79; separate samples, not age-25–44-specific. Independent multiselect 57%/22%, not a 100% split.','manual_visual_review':'Pending'}
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
