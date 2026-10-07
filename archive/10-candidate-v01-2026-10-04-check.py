"""Focused checks for exact candidate copy, handwriting, artwork and layout bounds."""
from pathlib import Path
import base64
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from PIL import Image

HERE=Path(__file__).resolve().parent
P='10-candidate-v01-2026-10-04'
M=json.loads((HERE/f'{P}-manifest.json').read_text())
C=HERE/M['copy_source']
S=re.sub(r'<!--.*?-->','',C.read_text(),flags=re.S)
strings=[s.strip().replace('**','').removeprefix('## ') for s in S.split('\n\n') if s.strip()]
root=ET.parse(HERE/f'{P}.svg').getroot()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
texts=M['text_objects']
boxes=[{'id':t['id'],'text':line['text'],'bbox':line['bbox']} for t in texts for line in t['lines']]
def intersects(a,b):
    x1,y1,x2,y2=a
    z1,v1,z2,v2=b
    return min(x2,z2)>max(x1,z1) and min(y2,v2)>max(y1,v1)
overlaps=[(a['id'],b['id']) for i,a in enumerate(boxes) for b in boxes[i+1:] if intersects(a['bbox'],b['bbox'])]
images=[e for e in root.iter() if e.tag.endswith('}image')]
art=(HERE/M['art_asset']).read_bytes()
original=Path(M['native_output_original'])
W=json.loads((HERE/f'{P}-writing-check.json').read_text())
expected=['Expected exactly one <!-- budget-table --> marker; found 0','Expected exactly one <!-- kpi-table --> marker; found 0']
checks={
 'exact-numbered-heading':strings[0]=='10. Business Goals & Growth',
 'complete-controlled-copy':strings==[t['text'] for t in texts],
 'all-rendered-lines-reconstruct-exact-text':all(' '.join(x['text'] for x in t['lines'])==t['text'] for t in texts),
 'explicit-proposed-plan':strings[1]=='Proposed 12-month plan',
 'four-goals-map-to-objectives-and-actions':all(len([t for t in texts if t['owner']==owner])==3 for owner in M['objective_mapping']),
 'stable-operation-before-rapid-expansion-and-gates':'before rapid expansion' in S and 'O4 service integrity' in S and 'Stage gates' in S,
 'search-social-before-gated-dooh':'Use search and social to win first paid rides.' in S and 'only after service and repeat gates pass' in S,
 'electric-mobility-mission-bounded':'Make app-booked electric rides easy to understand and use.' in S and 'lifecycle' not in S.lower() and 'zero emissions' not in S.lower(),
 'growth-depends-on-mature-repeat':'Scale only on mature-cohort repeat evidence.' in S,
 'm12-evidence-and-options':'Review O1 to O4, service delivery and contribution evidence.' in S and 'Renew · Revise · Stop' in S,
 'year-one-non-break-even-visible':'The year-one model does not break even.' in S,
 'no-visible-citation-or-logo':M['citation_visible'] is False and M['logo_used'] is False and not root.findall('.//{http://www.w3.org/2000/svg}text'),
 'exact-local-handwriting-only':all((t['font'],t['font_file']) in [('MarkerFelt-Thin','/System/Library/Fonts/MarkerFelt.ttc'),('Noteworthy-Light','/System/Library/Fonts/Noteworthy.ttc')] for t in texts),
 'text-inside-outer-frame':all(b['bbox'][0]>30 and b['bbox'][1]>30 and b['bbox'][2]<1870 and b['bbox'][3]<1610 for b in boxes),
 'no-text-bounds-overlap':not overlaps,
 'all-four-source-clips-explicit':all(root.find(f'.//*[@id="{p["id"]}-source-clip"]') is not None for p in M['raster_placements']),
 'embedded-raster-self-contained-and-byte-identical':len(images)==4 and all(base64.b64decode(e.get('href').split(',',1)[1])==art for e in images),
 'two-inherited-source-records-retain-matching-pdf-bytes':len(M['internal_source_records'])==2 and all(sha(HERE/r['pdf'])==r['sha256'] for r in M['internal_source_records']),
 'native-original-bytes-preserved':original.read_bytes()==art,
 'true-source-alpha-preserved':M['art_mode']=='RGBA' and M['art_alpha_extrema'][0]==0 and M['art_alpha_extrema'][1]>0,
 'full-and-small-canvas-sizes':Image.open(HERE/f'{P}.png').size==(1900,1640) and Image.open(HERE/f'{P}-small.png').size==(950,820),
 'writing-gate-detector-ran':W['base']['anti_slop']['status']=='ran',
 'zero-effective-writing-hard':all(v==0 for v in W['effective_base_hard_by_category'].values()),
 'writing-errors-only-standalone-table-markers':W['genre']['errors']==expected,
}
result={'status':'passed focused candidate checks' if all(checks.values()) else 'failed focused candidate checks','date':'2026-10-04','checks':checks,'all_checks_pass':all(checks.values()),'text_objects':len(texts),'text_overlaps':overlaps,'words':W['genre']['total_words'],'writing_gate_exit':2,'expected_fragment_limits':expected,'art_sha256':sha(HERE/M['art_asset']),'svg_sha256':sha(HERE/f'{P}.svg'),'png_sha256':sha(HERE/f'{P}.png'),'visual_inspection':['Native text-free sheet inspected; no observed letters, numbers, logo or measured-performance graphics','Actual full PNG and 950 px preview inspected; no observed text overlap/clipping or neighbouring sprite slivers','Marker objective ribbon wraps Stage gates clearly; business goals link visibly to objective and action'],'approval':'Candidate only; parent selection pending; no group approval','scope':'Only new poster/10-* files written; no other panel or shared/project-level file changed.','unverified':['Parent candidate selection','Actual A0 footprint','Physical print legibility']}
(HERE/f'{P}-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'all_checks_pass':result['all_checks_pass'],'failed':[k for k,v in checks.items() if not v],'words':result['words'],'text_objects':len(texts),'overlaps':overlaps},indent=2))
if not all(checks.values()):raise SystemExit(1)
