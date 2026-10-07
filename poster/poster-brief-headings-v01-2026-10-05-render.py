from pathlib import Path
import re,json,subprocess,hashlib,html
P=Path('/Users/khoilq/Documents/GWMBA_iCloud/[MARK1286] Marketing and Sales in the Future Economy/assessment1-marketing-plan-poster/poster')
STEM='poster-brief-headings-v01-2026-10-05';BASE=P/'10-cell-fit-v02-2026-10-05-poster.svg'
S=BASE.read_text();original=S
prefixes=['01-cell-fit-v07','02-cell-fit-v04','03-cell-fit-v07','04-cell-fit-v03','05-cell-fit-v05','06-cell-fit-v04','07-cell-fit-v04','08-cell-fit-v02','09-cell-fit-v02','10-cell-fit-v02']
heads=(P.parent/'00_brief_and_criteria/poster-headings.txt').read_text().splitlines()[1:]
proc=subprocess.Popen(['/usr/bin/swift',str(P/'08-cell-fit-v01-2026-10-05-glyphs.swift')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
records=[];layers=[];original_layers=[]
def segment(s,start):
 dep=0
 for m in re.finditer(r'<g\b[^>]*>|</g>',s[start:]):
  dep+=-1 if m.group()=='</g>' else 1
  if dep==0:return start+m.end()
 raise ValueError('group')
def glyph(t,x,y,size):
 proc.stdin.write(json.dumps({'text':t,'font':'MarkerFelt-Wide','size':size})+'\n');proc.stdin.flush();d=json.loads(proc.stdout.readline());assert 'error' not in d,d
 a,b,c,e=d['bounds'];r={'text':t,'font':'MarkerFelt-Wide','resolved_font_names':d['resolved_font_names'],'size_px':size,'size_pt_a0':round(size*1189/1672*72/25.4,2),'bbox':[x+a,y-e,x+c,y-b],'advance_width':d['width']}
 return f'<g aria-label="{html.escape(t,quote=True)}"><path d="{d["path"]}" transform="translate({x} {y}) scale(1 -1)" fill="#173a47"/></g>',r
for i,(pre,title) in enumerate(zip(prefixes,heads),1):
 ck=json.loads((P/(pre+'-2026-10-05-checks.json')).read_text());old=ck['visible_text'][0]['text'];m=re.search(r'<g id="section-'+f'{i:02}'+r'-[^\"]+"',S);start=m.start();end=segment(S,start);lay=S[start:end];oldlay=lay
 m=re.search(r'<g aria-label="'+re.escape(html.escape(old,quote=True))+'"',lay);assert m,(i,old);a=m.start();b=segment(lay,a)
 oldmarkup=lay[a:b];tm=re.search(r'translate\(([-\d.]+) ([-\d.]+)\)',oldmarkup);x,y=map(float,tm.groups())
 size=10.5;newrecs=[]
 if i==1:
  x,y,size=448,255,8.4;mk,r=glyph('1. Company/Business',x,y,size);mk2,r2=glyph('Introduction',x,265,size);mk+=mk2;newrecs=[r,r2]
  logo=re.search(r'<svg\b[^>]*id="fit01-authentic-green-sm-logo"[^>]*>',lay);assert logo
  img=logo.group()
  for att,val in [('x','567'),('y','268'),('width','35'),('height','14')]:img=re.sub(r'\b'+att+r'="[^"]*"',att+'="'+val+'"',img)
  lay=lay[:logo.start()]+img+lay[logo.end():]
 elif i==7:
  size=9.1;mk,r=glyph(f'{i}. {title}',x,y,size);newrecs=[r]
 else:mk,r=glyph(f'{i}. {title}',x,y,size);newrecs=[r]
 # Locate again after asset repositioning because its tag length changed.
 m=re.search(r'<g aria-label="'+re.escape(html.escape(old,quote=True))+'"',lay);a=m.start();b=segment(lay,a);lay=lay[:a]+mk+lay[b:]
 # First gold unfilled path in each section is the heading underline.
 candidates=list(re.finditer(r'<path\b[^>]*/>',lay));u=next(m for m in candidates if 'stroke="#e3bb42"' in m.group() and 'fill="none"' in m.group())
 uy=267 if i==1 else float(re.search(r'M[-\d.]+ ([-\d.]+)',u.group()).group(1));w=max(r['advance_width'] for r in newrecs)
 under=f'<path d="M{x} {uy}Q{x+w/2} {uy+1} {x+w} {uy}" fill="none" stroke="#e3bb42" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>'
 lay=lay[:u.start()]+under+lay[u.end():]
 # Remove redundant exact positioning subtitle, now supplied by main heading.
 dropped=[]
 if i==3:
  m=re.search(r'<g aria-label="Positioning Strategy"',lay);a=m.start();b=segment(lay,a);lay=lay[:a]+lay[b:];dropped=['Positioning Strategy']
 body=[r for r in ck['visible_text'][1:] if r['text'] not in dropped]
 outside=[];overlap=[]
 # Dense polygon sample for curved native clip; numeric path parser supports M/L/H/V/Q/Z.
 cell=ck['cell_path'];tok=re.findall(r'[MLHVQCZ]|-?\d+(?:\.\d+)?',cell);pts=[];n=0;x0=y0=0
 while n<len(tok):
  c=tok[n];n+=1
  if c in ['M','L']:
   x0,y0=float(tok[n]),float(tok[n+1]);n+=2;pts.append((x0,y0))
  elif c=='H':x0=float(tok[n]);n+=1;pts.append((x0,y0))
  elif c=='V':y0=float(tok[n]);n+=1;pts.append((x0,y0))
  elif c=='C':
   c1x,c1y,c2x,c2y,ex,ey=map(float,tok[n:n+6]);n+=6
   for j in range(1,101):
    t=j/100;v=1-t;pts.append((v**3*x0+3*v*v*t*c1x+3*v*t*t*c2x+t**3*ex,v**3*y0+3*v*v*t*c1y+3*v*t*t*c2y+t**3*ey))
   x0,y0=ex,ey
  elif c=='Q':
   cx,cy,ex,ey=map(float,tok[n:n+4]);n+=4
   for j in range(1,101):
    t=j/100;v=1-t;pts.append((v*v*x0+2*v*t*cx+t*t*ex,v*v*y0+2*v*t*cy+t*t*ey))
   x0,y0=ex,ey
 def inside(x,y):
  hit=False
  for (ax,ay),(bx,by) in zip(pts,pts[1:]+pts[:1]):
   if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:hit=not hit
  return hit
 for r in newrecs:
  b=r['bbox']
  if not all(inside(x,y) for x in [b[0],b[2]] for y in [b[1],b[3]]):outside.append(r['text'])
  for o in body:
   a=o['bbox']
   if min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1]):overlap.append([r['text'],o['text']])
 print(i,title,'outside',outside,'overlap',overlap,flush=True)
 assert not outside and not overlap,(i,outside,overlap)
 records.append({'section':i,'heading':f'{i}. {title}','heading_records':newrecs,'old_heading':old,'duplicate_subtitle_removed':dropped,'body_text_geometry_preserved':True,'heading_containment_failures':outside,'heading_text_overlap_failures':overlap,'green_sm_logo_repositioned':i==1,'cell_path':cell,'source_prefix':pre+'-2026-10-05'})
 layers.append(lay);original_layers.append(oldlay);S=S[:start]+lay+S[end:]
proc.stdin.close();proc.wait()
restore=S
for lay,old in zip(layers,original_layers):restore=restore.replace(lay,old,1)
assert restore==original
(P/(STEM+'.svg')).write_text(S)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','2400','-o',str(P/(STEM+'.png')),str(P/(STEM+'.svg'))],check=True)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(P/(STEM+'.pdf')),str(P/(STEM+'.svg'))],check=True)
for r,lay in zip(records,layers):
 i=r['section'];cell=r['cell_path'];nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',cell)));xs=nums[::2];ys=nums[1::2]
 # Reuse standalone viewBox from current per-section panel where available.
 pre=r['source_prefix'];panel=P/(pre+'-panel.svg')
 if not panel.exists():panel=P/(pre+'-close-up.svg')
 raw=panel.read_text();vb=re.search(r'viewBox="([^"]+)"',raw).group(1)
 if '-panel.svg' not in panel.name:
  a,b,c,d=map(float,vb.split());vb=f'{a} {b-120.817073} {c} {d}'
 out=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="2000" height="1200" viewBox="{vb}"><defs><clipPath id="cell-{i:02}-clip"><path d="{cell}"/></clipPath></defs><path d="{cell}" fill="#fdfbef" stroke="#173a47" stroke-width=".8"/>{lay}</svg>'
 name=f'{i:02}-brief-heading-v01-2026-10-05';(P/(name+'-panel.svg')).write_text(out);subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','2000','-o',str(P/(name+'-panel.png')),str(P/(name+'-panel.svg'))],check=True)
 text=(P/(pre+'-copy.md')).read_text();text=text.replace(r['old_heading'],r['heading'])
 if i==1:text=re.sub(r'## 1\. Company/Business Introduction(?: Green SM)?','## 1. Company/Business Introduction',text)
 if i==3:text=text.replace('\nPositioning Strategy\n','\n')
 (P/(name+'-copy.md')).write_text(text)
 (P/(name+'-notes.md')).write_text(f'# {r["heading"]} — brief-heading fit\n\nCandidate; exact heading from handbook (content heading {i+1}; cloud holds Student/Business Details). Based on {pre}. Existing body copy/numbers and cell geometry preserved. '+('Heading wraps in two lines at 16.93 pt; shared logo moved beside app/taxi to clear the heading/corporate block. Embedded bytes unchanged. ' if i==1 else '')+('Long budget heading uses 18.35 pt to preserve the right-hand total and exact body placement. ' if i==7 else 'Other headings use 21.17 pt. ')+('Redundant Positioning Strategy subtitle removed; its complete text is now the main heading. ' if i==3 else '')+'Heading glyph containment and body-text overlap checks pass. Review in full poster; no physical print acceptance inferred.\n')
info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/(STEM+'.pdf'))],capture_output=True,text=True,check=True).stdout
checks={'status':'All ten brief headings candidate; body copy preserved; Section10 v02 layout also awaits review','base':BASE.name,'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'restore_original_headers_and_logo_reposition_restores_base_bytes':restore==original,'pdfinfo':info,'sections':records,'manual_visual_review':'Pending'}
(P/(STEM+'-checks.json')).write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print('COMPLETE',STEM,flush=True)
