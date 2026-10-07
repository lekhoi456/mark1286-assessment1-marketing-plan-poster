"""Build the compact visual Section 8 dashboard; v01 stays untouched."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import subprocess

HERE=Path(__file__).resolve().parent
def load(name):
    spec=importlib.util.spec_from_file_location(name,HERE/('08-v02-'+name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
layout, V=load('layout'),load('visuals')
W,H=2200,2030
L=layout.Layout(W,H,HERE/'08-v02-glyphs.swift')
old=json.loads((HERE/'08-candidate-v01-2026-10-04-manifest.json').read_text())
rows=copy.deepcopy(old['kpi_rows'])
for r in rows:r.pop('display_bounds',None)
art=HERE/'08-v02-art.png';V.install_art(L,art)
L.frame('outer-frame',32,32,W-64,H-64,stroke=layout.INK,thick=3)
L.text('8. Success Dashboard',80,133,92,'MarkerFelt-Wide',role='heading')
L.rule(82,157,1080,layout.GOLD,12)
L.text('Proposed targets, not achieved results.',83,198,35,'Noteworthy-Bold',role='assumption')
L.text('Below each measure: tool · review rhythm',1160,192,33,role='legend')
zones={
 'O1':{'label':'O1 awareness','rect':[70,230,1000,405]},
 'O2':{'label':'O2 paid trial','rect':[1130,230,1000,420]},
 'O3':{'label':'O3 repeat','rect':[70,665,1000,450]},
 'O4':{'label':'O4 service integrity','rect':[1130,665,1000,710]},
}
for key,z in zones.items():
 x,y,w,h=z['rect'];L.frame('zone-'+key,x,y,w,h,fill='#fffefa')
 L.text(z['label'],x+28,y+52,45,'MarkerFelt-Wide',role='objective',owner=key)
 L.rule(x+28,y+66,w-56,layout.CYAN,7)

def t(s,x,y,size=33,font='Noteworthy-Light',width=None,owner=None,role='metric'):
 return L.text(s,x,y,size,font,width,role,owner)

# Awareness is a delta, never an invented baseline percentage or a result series.
V.icon(L,0,100,337,260,215)
t('Would consider Green SM',380,342,37,'Noteworthy-Bold',owner='O1')
t('+10 pp',400,439,95,'MarkerFelt-Wide',owner='O1',role='target')
t('M1–2 baseline',382,499,35,owner='O1')
V.arrow(L,614,490,693,490)
t('M12',726,499,38,'Noteworthy-Bold',owner='O1')
t('pp = percentage points',383,545,33,owner='O1')
t('Resident panel survey · M1–2 and M12',100,606,33,width=940,owner='O1',role='tracking')

# Three acquisition measures: count, proportional target bars and paid-only cost.
V.icon(L,1,1150,304,175,147)
t('378',1335,410,96,'MarkerFelt-Wide',owner='O2',role='target')
t('First paid riders · M1–12',1160,452,36,'Noteworthy-Bold',owner='O2')
t('Booking/settlement data · Weekly',1160,495,33,width=490,owner='O2',role='tracking')
t('Search 3%',1700,332,40,'Noteworthy-Bold',owner='O2',role='target')
bars=[V.target_bar(L,'search-target',1700,360,3)]
t('Social 1.5%',1700,413,40,'Noteworthy-Bold',owner='O2',role='target')
bars.append(V.target_bar(L,'social-target',1700,440,1.5,colour=layout.GOLD))
t('First paid riders / all paid clicks',1670,481,33,width=440,owner='O2')
t('Ads and bookings · Weekly',1670,525,33,width=440,owner='O2',role='tracking')
L.rule(1160,540,940,'#98b9b5',2)
t('Search/social spend / first paid riders',1460,579,33,'Noteworthy-Bold',width=640,owner='O2')
t('≤DKK524',1160,625,52,'MarkerFelt-Wide',owner='O2',role='target')
t('Finance and bookings · Monthly',1460,625,33,width=640,owner='O2',role='tracking')

# The observation window carries the repeat denominator, before the target loop.
L.frame('first-trip-node',100,770,295,110,fill='#f4fbf5')
t('First paid trip',128,837,35,'Noteworthy-Bold',owner='O3')
V.arrow(L,405,827,470,827)
V.icon(L,2,465,752,205,184)
t('90 days',502,864,39,'Noteworthy-Bold',owner='O3')
V.arrow(L,678,827,734,827)
L.parts.append('<path d="M768 793 Q855 749 984 802 Q1045 855 1008 914 Q916 965 786 916" fill="none" stroke="#26c6cf" stroke-width="12" stroke-linecap="round"/>')
V.arrow(L,795,913,766,870,layout.GOLD,8)
t('≥35%',777,858,76,'MarkerFelt-Wide',owner='O3',role='target')
t('Paid repeat',792,905,35,'Noteworthy-Bold',owner='O3')
t('Full 90-day window · fully observed riders only',103,995,34,width=940,owner='O3')
t('Rider cohorts · Monthly from M6',103,1065,33,owner='O3',role='tracking')

# Four outlined percentage scales; no observed needle or completed progress fill.
V.icon(L,3,1940,686,153,121)
t('Completion / cancels: per accepted booking',1160,758,33,owner='O4')
t('0–100% scale · markers are proposed targets',1160,800,33,owner='O4',role='chart-key')
gauges=[]
gauges.append(V.gauge(L,'completion',1370,891,95,'minimum'))
gauges.append(V.gauge(L,'cancellations',1835,891,2,'maximum'))
t('≥95%',1285,920,68,'MarkerFelt-Wide',owner='O4',role='target')
t('≤2%',1770,920,68,'MarkerFelt-Wide',owner='O4',role='target')
t('Completed',1190,965,34,'Noteworthy-Bold',owner='O4')
t('Service-caused cancels',1655,965,34,'Noteworthy-Bold',owner='O4')
t('Dispatch data · Daily',1190,1007,33,owner='O4',role='tracking')
t('Dispatch reason codes · Daily',1655,1007,33,width=448,owner='O4',role='tracking')
gauges.append(V.gauge(L,'response',1370,1110,90,'minimum'))
gauges.append(V.gauge(L,'clarity',1835,1110,80,'minimum'))
t('≥90%',1285,1137,68,'MarkerFelt-Wide',owner='O4',role='target')
t('≥80% yes',1700,1137,62,'MarkerFelt-Wide',owner='O4',role='target')
t('Referenced complaints',1190,1174,33,'Noteworthy-Bold',owner='O4')
t('answered within 24h',1190,1219,33,owner='O4')
t('Area and fare terms clear',1655,1198,33,'Noteworthy-Bold',owner='O4')
t('Support log · Weekly',1190,1264,33,owner='O4',role='tracking')
t('Post-trip question · Monthly',1655,1264,33,owner='O4',role='tracking')
L.rule(1160,1277,940,'#98b9b5',2)
t('Usable offers / in-area requests',1160,1311,33,'Noteworthy-Bold',owner='O4')
t('Set after M1–2 area/hour baseline',1160,1354,33,owner='O4',role='target')
t('Request logs · Weekly',1760,1354,33,owner='O4',role='tracking')

# The eleventh measure is a budget-limit comparison, with no invented spend bars.
L.frame('spend-control',70,1148,1000,197,fill='#fff9dc',stroke='#d3b743')
t('Spend control',100,1196,42,'MarkerFelt-Wide',owner='Spend control')
t('Committed + spent',101,1245,36,'Noteworthy-Bold',owner='Spend control')
V.arrow(L,410,1234,475,1234)
t('Within approved stage totals',505,1245,34,'Noteworthy-Bold',owner='Spend control',role='target')
t('Finance · Weekly',101,1305,33,owner='Spend control',role='tracking')

L.rule(76,1390,2048,layout.CYAN,2.5)
t('Installs excluded from paid riders, refunds removed. Repeat: full 90-day windows only.',90,1429,34,width=2020,role='counting')
t('DKK524: paid search/social only, not total acquisition cost. Advertise only verified coverage with usable offers.',90,1475,33,width=2020,role='counting')
gate_a=['Completion ≥95% · service cancellations ≤2%',
 'Referenced complaints answered within 24h ≥90%',
 'Search conversion ≥1.5% · social ≥0.8%',
 'Agree minimum observed volume with operations.',
 'Fail → hold media, fix and re-test.','Pass → release M5–6.']
gate_b=['Mature-cohort 90-day repeat ≥20%',
 'and paid cost per first rider ≤DKK1,829 → continue.',
 'Repeat ≥35% → release street screens.','Fail → stop scale-up.']
for key,x,heading,lines in [('A',70,'Gate A / M4',gate_a),('B',1130,'Gate B / M6',gate_b)]:
 L.frame('gate-'+key,x,1500,1000,360,fill='#fff9dc',stroke='#d3b743')
 t(heading,x+30,1560,43,'MarkerFelt-Wide',role='gate-heading')
 for i,line in enumerate(lines):t(line,x+30,1610+i*44,33,'Noteworthy-Bold' if i>=len(lines)-2 else 'Noteworthy-Light',width=940,role='gate-'+key)
L.rule(77,1880,2047,layout.CYAN,2.5)
t('M12: evaluate O1 to O4 → renew, revise or stop for year two.',90,1920,37,'Noteworthy-Bold',role='review')
t('Floors and targets are planning assumptions.',91,1970,33,role='assumption')
svg=HERE/'08-v02.svg';svg.write_text(L.close())
for suffix,size in [('.png',[]),('-small.png',['-w','1100'])]:
 subprocess.run(['/opt/homebrew/bin/rsvg-convert',*size,'-o',str(HERE/('08-v02'+suffix)),str(svg)],check=True)
m=copy.deepcopy(old)
m['display_measure_mapping']=json.loads((HERE/'08-v02-display-map.json').read_text())
m.update({'version':'v02','status':'Delegated visual candidate; parent selection pending; no group approval',
 'canvas':[W,H],'copy_source':'08-v02-copy.md','kpi_rows':rows,'objective_zones':zones,
 'visible_text':L.texts,'frames':L.frames,'gate_a':gate_a,'gate_b':gate_b,'target_bars':bars,'target_gauges':gauges,
 'native_art':{'path':art.name,'sha256':hashlib.sha256(art.read_bytes()).hexdigest(),'generated_lettering_or_data':False},
 'minimum_body_size':33,'composition_source':'poster/08-v02-render.py',
 'print_width_mm_for_body_12pt':round(12/72*25.4*W/33,1),
 'print_width_mm_for_body_14pt':round(14/72*25.4*W/33,1),
 'size_vs_v01':{'height_ratio':H/2710,'area_ratio':H/2710,'at_330_mm':[330,330*H/W]},
 'A0_limitation':'More compact near-square candidate; actual A0 and printed fit remain unverified',
 'svg_sha256':hashlib.sha256(svg.read_bytes()).hexdigest()})
(HERE/'08-v02-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('Rendered compact visual dashboard:',str((HERE/'08-v02.png').resolve()))
