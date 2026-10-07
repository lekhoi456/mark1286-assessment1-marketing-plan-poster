"""Fit the five-stage sales loop into native cell 06, preserving all other nine populated cells."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess

HERE = Path(__file__).resolve().parent
PREFIX = '06-cell-fit-v04-2026-10-05'
BASE = HERE / '06-cell-fit-v03-2026-10-05-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#e3bb42', '#fdfbef'
CELL = 'M642 400 H821 Q844 400 844 423 V575 Q844 598 821 598 H642 Q619 598 619 575 V423 Q619 400 642 400 Z'
parts, records = [], []
proc = subprocess.Popen(['/usr/bin/swift', str(HERE / '05-cell-fit-v03-2026-10-04-glyphs.swift')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def text(value, x, y, size=6.6, heading=False, width=None):
    font = 'MarkerFelt-Wide' if heading else 'ChalkboardSE-Regular'
    def glyph(size):
        proc.stdin.write(json.dumps({'text': value, 'font': font, 'size': size}, ensure_ascii=False) + '\n')
        proc.stdin.flush()
        result = json.loads(proc.stdout.readline())
        if 'error' in result:
            raise RuntimeError(result['error'])
        assert all(f in (font, 'Native vector arrow') for f in result['resolved_font_names']), result
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


def icon(kind, y):
    parts.append(f'<g id="sales-{kind}-icon" transform="translate(634 {y}) scale(.85)">')
    if kind == 'discover':
        path('M2 0Q0 0 0 2V20Q0 22 2 22H16Q18 22 18 20V2Q18 0 16 0Z',CYAN)
        path('M3 5H15V17H3Z',CREAM,width=.6)
        path('M6 2H12',width=.6)
        circle(20,10,4.2,GOLD)
        path('M23 13L27 17',width=1.2)
    elif kind == 'ride':
        path('M0 13L4 5Q5 3 8 3H17L23 13L27 15V21H-2V16Z',CYAN)
        path('M7 6H16L20 13H4Z',CREAM,width=.7)
        path('M10 0H16V3H10Z',GOLD,width=.6)
        circle(4,21,3,NAVY)
        circle(21,21,3,NAVY)
        path('M8 17L11 20L17 14',colour=NAVY,width=1.1)
    elif kind == 'experience':
        circle(11,6,4,GOLD)
        path('M3 20V16Q4 12 11 12Q18 12 19 16V20Z',CYAN)
        path('M20 11C17 7 21 3 24 7C28 3 32 7 24 13Z',GOLD,width=.7)
        path('M-2 14H2V20H-2Z',CREAM,width=.7)
    elif kind == 'feedback':
        path('M2 1H24Q27 1 27 4V17Q27 20 24 20H10L3 25L4 20H2Q-1 20 -1 17V4Q-1 1 2 1Z',CYAN)
        path('M13 5L15 9L20 10L16 13L17 17L13 15L9 17L10 13L6 10L11 9Z',GOLD,width=.7)
    elif kind == 'repeat':
        path('M1 2H24V24H1Z',CREAM)
        path('M1 2H24V8H1Z',CYAN)
        path('M7 0V5 M18 0V5',width=1.1)
        path('M6 12H11V17H6Z',GOLD,width=.5)
        path('M15 12H20V17H15Z',GOLD,width=.5)
        path('M5 21H20',colour=CYAN,width=.8)
    parts.append('</g>')

# Five connected stops; smaller flat-fill icons free width for larger lettering.
title_width=text('6. From Clicks to Rides',633,420,10.5,True,width=196)
path(f'M633 424Q{633+title_width/2} 425 {633+title_width} 424',colour=GOLD,width=1.5)
text('Sales strategy • proposed',753,417.3,6.3,width=78)
stages=[
 ('discover',437,'Discover',['Search/social → leads','Fare check → prospect']),
 ('ride',471,'First paid ride',['App booking → completed trip','First-ride voucher']),
 ('experience',505,'Experience',['Check app · driver · car · care']),
 ('feedback',531,'Feedback',['Post-ride feedback + rating','Unpaid review: well-rated/resolved']),
 ('repeat',562,'Repeat',['Opt-in reminders + voucher pilots*','Tailored monthly paid bundle pilots*']),
]
for kind,y,label,body in stages:
    icon(kind,y-8)
    text(label,670,y,8.2,True,width=157)
    for i,value in enumerate(body):
        text(value,670,y+9+i*8.6,7.4,width=157)
for y in [454,490,518.5,549]:
    path(f'M646 {y-2}V{y+1} M644 {y-1}L646 {y+1}L648 {y-1}',colour=CYAN,width=1)
# A return arrow sits outside lettering, from repeat to first paid ride.
path('M833 570Q839 570 839 563V473Q839 469 833 469 M835 467L833 469L835 471',colour=CYAN,width=1)
text('*Test frequency + unit economics',638,587,6.2,width=195)
text('Cost pilots separately',638,595,6.2,width=194)
proc.stdin.close()
proc.wait(timeout=15)
if proc.returncode:
    raise RuntimeError(proc.stderr.read())
layer='<g id="section-06-v04-candidate" clip-path="url(#cell-06-clip)">'+'\n'.join(parts)+'</g>'
base=BASE.read_text()
start=base.index('<g id="section-06-v03-candidate"')
# Replace exactly this nested group, preserving all other SVG bytes.
depth=0
end=None
for match in re.finditer(r'<g\b[^>]*>|</g>',base[start:]):
    depth += -1 if match.group()=='</g>' else 1
    if depth==0:
        end=start+match.end()
        break
assert end is not None
old_layer=base[start:end]
assembled=base[:start]+layer+base[end:]
assert assembled.replace(layer,old_layer,1)==base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
standalone=f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1440" viewBox="613 394 237 210"><defs><clipPath id="cell-06-clip"><path d="{CELL}"/></clipPath></defs><path d="{CELL}" fill="{CREAM}" stroke="{NAVY}" stroke-width=".8"/>{layer}</svg>'
(HERE/f'{PREFIX}-panel.svg').write_text(standalone)
crop=re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="1600" height="1436" viewBox="613 514.817073 237 210"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('panel',1600),('close-up',1600)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
displayed='\n'.join(r['text'] for r in records)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text(displayed+'\n')
checks={'status':'Candidate for student review. D-135 amendment: first-ride voucher wording and right-aligned header note. Section 6 only.','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'other_nine_cells_and_background_byte_for_byte_preserved':assembled.replace(layer,old_layer,1)==base,'cell_path':CELL,'a0_mm':[1189,841],'art_translation_y':120.817073,'visible_text':records,'word_bearing_tokens':sum(bool(re.search(r'\w',w)) for w in displayed.split()),'minimum_size_pt_a0':min(r['size_pt_a0'] for r in records),'all_hand_drawn_font_resolutions':sorted(set(f for r in records for f in r['resolved_font_names'])),'raster_images_added':0}
def inside_cell(x, y):
    if not (619 <= x <= 844 and 400 <= y <= 598):
        return False
    inset = 0
    if y < 423:
        inset = 23 * (1 - math.sqrt((y - 400) / 23))**2
    elif y > 575:
        inset = 23 * (1 - math.sqrt((598 - y) / 23))**2
    return 619 + inset <= x <= 844 - inset

for i, record in enumerate(records):
    a = record['bbox']
    assert all(inside_cell(x,y) for x in [a[0],a[2]] for y in [a[1],a[3]]), record
    for other in records[i+1:]:
        b = other['bbox']
        assert not (min(a[2],b[2]) > max(a[0],b[0]) and min(a[3],b[3]) > max(a[1],b[1])), (record,other)
pdf_info = subprocess.run(['/opt/homebrew/bin/pdfinfo',str(HERE/f'{PREFIX}-poster.pdf')],capture_output=True,text=True,check=True).stdout
pdf_size = re.search(r'Page size:\s*([\d.]+) x ([\d.]+) pts',pdf_info)
checks.update({'glyph_bbox_corners_inside_native_cell':True,'pairwise_text_overlap_count':0,'pdf_measured_mm':[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]],'manual_visual_review':'Pending inspection of new standalone, assembled close-up and full A0.'})
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
