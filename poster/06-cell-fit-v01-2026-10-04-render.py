"""Fit the five-stage sales loop into native cell 06, preserving accepted cell 05."""
from pathlib import Path
from html import escape
import hashlib
import json
import math
import re
import subprocess

HERE = Path(__file__).resolve().parent
PREFIX = '06-cell-fit-v01-2026-10-04'
BASE = HERE / '05-cell-fit-v04-2026-10-04-poster.svg'
NAVY, CYAN, GOLD, CREAM = '#173a47', '#28bdbf', '#ffd400', '#fdfbef'
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
    parts.append(f'<g id="sales-{kind}-icon" transform="translate(634 {y})">')
    if kind == 'awareness':
        path('M1 0H42V19H1Z',CYAN)
        path('M9 19V25 M34 19V25',width=1.1)
        path('M10 6L28 2V15L10 11Z',GOLD,width=.7)
        path('M14 12L16 17H20L18 11Z',GOLD,width=.5)
        path('M32 4L36 2 M33 8H38 M32 13L36 15',colour=CREAM,width=1)
        path('M-2 27Q22 28 45 26',colour=CYAN)
    elif kind == 'book':
        path('M1 2Q20 0 35 2L44 13L35 24Q19 26 1 24L-3 13Z','#fff1a7')
        path('M8 4V22',colour=CYAN)
        circle(30,13,8,GOLD)
        path('M25 13L29 17L35 9',colour=NAVY,width=1.2)
        path('M-1 27Q17 29 43 26',colour=CYAN)
    elif kind == 'experience':
        path('M0 0H9Q11 0 11 2V20Q11 22 9 22H0Q-2 22 -2 20V2Q-2 0 0 0Z','#e8f8f0')
        path('M1 4H8V15H1Z',CREAM,colour=CYAN,width=.6)
        circle(4.5,18,1,GOLD,.3)
        path('M14 15Q17 7 24 7H33Q39 8 42 15L47 18L46 23H12L11 18Z',CYAN)
        path('M22 9H33L39 15H19Z',CREAM,width=.5)
        circle(19,23,3,NAVY,.2)
        circle(40,23,3,NAVY,.2)
        circle(28,12,2.4,'#ffd7b0',.4)
        path('M39 1C36 -2 33 2 39 7C45 2 42 -2 39 1Z',GOLD,width=.5)
    elif kind == 'feedback':
        path('M2 0H36Q43 0 43 6V17Q43 22 36 22H14L3 27L5 22H2Q-3 22 -3 17V6Q-3 0 2 0Z','#daf4ee')
        for x in [8,19,30]:
            circle(x,10,1.5,CYAN,.3)
        path('M37 17L40 21L45 22L41 26L42 30L37 28L32 30L33 26L29 22L34 21Z',GOLD,width=.5)
    elif kind == 'repeat':
        path('M0 0H15Q18 0 18 3V26Q18 29 15 29H0Q-3 29 -3 26V3Q-3 0 0 0Z','#daf4ee')
        path('M1 4H14V22H1Z',CREAM,colour=CYAN,width=.5)
        circle(7.5,26,1,GOLD,.3)
        circle(15,5,3,GOLD,.4)
        path('M24 6Q34 3 45 6L46 25Q35 28 24 25Z','#fff1a7')
        path('M28 11Q35 9 42 11 M28 16Q35 14 42 16 M28 21Q35 19 42 21',colour=CYAN,width=.8)
    parts.append('</g>')

# Heading and underline follow lettering width rather than the cell border.
title_width = text('6. From Clicks to Rides',633,420,12.2,True,width=197)
path(f'M633 424Q{633+title_width/2} 426 {633+title_width} 424',colour=GOLD,width=1.6)
text('Sales Strategy · proposed',633,433,6.3,width=195)

stages = [
    ('awareness',442,'Awareness',['Copenhagen visibility → leads','Installs ≠ sales']),
    ('book',473,'Book',['Green SM app booking → completed,','paid trip = sale','First-ride test: 10% vs 20% · max DKK30']),
    ('experience',507,'Experience',['App / driver / car / care','Target quality after checks']),
    ('feedback',536,'Feedback',['Post-ride feedback','Unpaid review after resolved/well-rated ride']),
    ('repeat',563,'Repeat',['Opt-in reminders · voucher pilots*','Tailored monthly paid bundle pilots*']),
]
for kind,y,label,body in stages:
    icon(kind,y-5)
    text(label,692,y,8,True,width=136)
    for i,value in enumerate(body):
        text(value,692,y+8+i*7.7,6.6,width=138)
# Native down arrows; repeat returns directly to the booking stage.
for y in [467,502,532,562]:
    path(f'M656 {y-4}Q658 {y-2} 657 {y} M654 {y-2}L657 {y}L660 {y-2}',colour=CYAN,width=.9)
path('M683 578Q686 579 686 572V482Q686 478 681 478L678 478 M680 476L678 478L680 480',colour=CYAN,width=.9)
text('*After frequency/unit economics test',692,587,6,width=138)
text('Separate costing',692,594,6,width=138)

proc.stdin.close()
proc.wait(timeout=15)
if proc.returncode:
    raise RuntimeError(proc.stderr.read())
layer = '<g id="section-06-v01-candidate" clip-path="url(#cell-06-clip)">'+'\n'.join(parts)+'</g>'
base = BASE.read_text()
assert base.endswith('</g></svg>')
assembled = base[:-len('</g></svg>')] + layer + '</g></svg>'
assert assembled.replace(layer,'') == base
(HERE/f'{PREFIX}-poster.svg').write_text(assembled)
transparent = f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1440" viewBox="619 400 225 198"><defs><clipPath id="cell-06-clip"><path d="{CELL}"/></clipPath></defs>{layer}</svg>'
(HERE/f'{PREFIX}-layout.svg').write_text(transparent)
crop = re.sub(r'width="1189mm" height="841mm" viewBox="0 0 1672 1182.634146"','width="1600" height="1436" viewBox="613 514.817073 237 210"',assembled,count=1)
(HERE/f'{PREFIX}-close-up.svg').write_text(crop)
for suffix,width in [('poster',2400),('close-up',1600)]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(width),'-o',str(HERE/f'{PREFIX}-{suffix}.png'),str(HERE/f'{PREFIX}-{suffix}.svg')],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(HERE/f'{PREFIX}-poster.pdf'),str(HERE/f'{PREFIX}-poster.svg')],check=True)
displayed='\n'.join(r['text'] for r in records)
(HERE/f'{PREFIX}-displayed-copy.txt').write_text(displayed+'\n')
word_count=sum(bool(re.search(r'\w',w)) for w in displayed.split())
checks={'status':'Human-review candidate; new condensed copy and artwork are not accepted','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'base_byte_for_byte_preserved':assembled.replace(layer,'')==base,'cell_path':CELL,'a0_mm':[1189,841],'art_translation_y':120.817073,'visible_text':records,'word_bearing_tokens':word_count,'minimum_size_pt_a0':min(r['size_pt_a0'] for r in records),'all_hand_drawn_font_resolutions':sorted(set(f for r in records for f in r['resolved_font_names'])),'raster_images_added':0}
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
checks.update({'glyph_bbox_corners_inside_native_cell':True,'pairwise_text_overlap_count':0,'pdf_measured_mm':[round(float(pdf_size.group(i))*25.4/72,3) for i in [1,2]],'manual_visual_review':'Close-up inspected. A0 reading distance and acceptance require human review.'})
(HERE/f'{PREFIX}-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='visible_text'},ensure_ascii=False,indent=2))
