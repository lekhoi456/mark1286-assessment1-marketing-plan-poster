from pathlib import Path
import base64,copy,html,importlib.util,itertools,json,re,subprocess,hashlib
ROOT=Path(__file__).resolve().parent.parent if Path(__file__).parent.name=='poster' else Path.cwd()
P=ROOT/'poster'; stem='poster-references-v01-2026-10-05'
sp=importlib.util.spec_from_file_location('refs',ROOT/'06_workflow/scripts/refs.py');refs=importlib.util.module_from_spec(sp);sp.loader.exec_module(refs)
KEYS=['afa-decaux-2026','aurora-vietnam-and-inspace-creative-2026','customer-data-platform-institute-nd','drivr-nd','feng-et-al-2020','green-future-usa-inc-ndc','green-sm-2026a','green-sm-2026d','green-sm-nd','green-sm-denmark-aps-ndc','gsm-green-and-smart-mobility-joint-stock-company-2024b','konkurrence-og-forbrugerstyrelsen-2026b','openstax-2023','statistics-denmark-2026b','vietnamplus-2023a','viggo-2025','vingroup-2025-annual-report-2024']
registry=json.loads((ROOT/'04_references/references.json').read_text()); entries=[];states={}
for key in KEYS:
 e=next(e for e in registry['entries'] if e['key']==key);states[key]=refs.pdf_state(e)['status'];assert states[key] in ('match','accepted-manual'),(key,states[key]);entries.append(copy.deepcopy(e))
# Display suffixes belong to the actual selected bibliography; canonical keys remain stable.
groups={}
for e in entries:groups.setdefault((refs.author_part(e),str(e['year'])),[]).append(e)
for group in groups.values():
 for i,e in enumerate(sorted(group,key=lambda e:refs.fold(e['title']))):e['suffix']=chr(97+i) if len(group)>1 else ''
entries.sort(key=refs.sort_key); bibliography=[refs.render(e) for e in entries]
proc=subprocess.Popen(['/usr/bin/swift',str(P/'08-cell-fit-v01-2026-10-05-glyphs.swift')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
cache={};records=[]
def measure(t,z,font='ChalkboardSE-Regular'):
 key=(t,z,font)
 if not t or t.isspace():
  return {'width':measure('a'+t+'a',z,font)['width']-2*measure('a',z,font)['width'],'bounds':[0,0,0,0],'path':''}
 if key not in cache:
  proc.stdin.write(json.dumps({'text':t,'font':font,'size':z})+'\n');proc.stdin.flush();d=json.loads(proc.stdout.readline());assert 'error' not in d;cache[key]=d
 return cache[key]
def glyph(t,x,y,z,italic=False,font='ChalkboardSE-Regular',url=None):
 if not t or t.isspace():return ''
 d=measure(t,z,font);a,b,c,e=d['bounds'];bb=[x+a,y-e,x+c,y-b];records.append({'text':t,'bbox':bb,'font':font,'italic':italic,'a0_pt':z*1189/1672*72/25.4})
 transform=f'translate({x:.3f} {y:.3f})'+(' skewX(-10)' if italic else '')+' scale(1 -1)'
 node=f'<g aria-label="{html.escape(t,quote=True)}"><path d="{d["path"]}" transform="{transform}" fill="#173a47"/></g>'
 return '<a href="'+html.escape(url,quote=True)+'">'+node+'</a>' if url else node

def wrap(ref,z,width):
 # Preserve italic title runs and clickable URLs while wrapping complete Harvard entries.
 lines=[];line=[];used=0.0;indent=0
 for kind,segment in ref.segs:
  for token in re.findall(r'\s+|\S+',segment):
   remaining=token
   while remaining:
    cap=width-indent-used
    w=measure(remaining,z)['width']
    if w<=cap:
     if not line and remaining.isspace():break
     line.append((kind,remaining));used+=w;break
    if remaining.isspace():
     if line:lines.append(line);line=[];used=0;indent=7
     break
    if line:
     lines.append(line);line=[];used=0;indent=7;continue
    # Very long URLs wrap at characters; the full URL remains the link target.
    lo,hi=1,len(remaining)
    while lo<hi:
     mid=(lo+hi+1)//2
     if measure(remaining[:mid],z)['width']<=width-indent:lo=mid
     else:hi=mid-1
    chunk=remaining[:lo];lines.append([(kind,chunk)]);remaining=remaining[lo:];indent=7
 if line:lines.append(line)
 return lines

colwidth=389; xcols=[24,435,846,1257];top=1049;bottom=1174
for size in [7.4,7.2,7.0,6.8,6.6]:
 lineheight=size*1.20; gap=size*.65
 all_lines=[wrap(r,size,colwidth-2) for r in bibliography]
 heights=[len(ls)*lineheight+gap for ls in all_lines]
 best=None
 for cuts in itertools.combinations(range(1,len(entries)),3):
  edges=(0,)+cuts+(len(entries),); sums=[sum(heights[edges[c]:edges[c+1]]) for c in range(4)]
  score=(max(sums),max(sums)-min(sums))
  if best is None or score<best[0]:best=(score,edges,sums)
 if best[0][0]<=bottom-top+lineheight:break
else:raise ValueError('References do not fit at minimum lettering size; adjust the footer, not the metadata.')

base=P/'poster-no-left-cloud-v01-2026-10-05.svg'; original=base.read_text();s=original
start=s.index('<g id="global-header-v02-candidate"');oldheader=s[start:-6];assert oldheader.endswith('</g>')
inside=oldheader[oldheader.index('>')+1:-4]
oldlogo=re.search(r'<image\b[^>]*id="greenwich-hand-drawn-logo"[^>]*/>',inside).group();inside=inside.replace(oldlogo,'',1)
newlogo=oldlogo
for key,val in [('x','711'),('y','10'),('width','250'),('height','90')]:newlogo=re.sub(r'\b'+key+r'="[^"]*"',key+'="'+val+'"',newlogo)
header='<g id="global-header-above-title-v01" aria-label="University of Greenwich above centred title">'+newlogo+'<g transform="translate(0 42)">'+inside+'</g></g>'
footer=['<g id="harvard-references-footer-v01" aria-label="References in Harvard style"><rect x="0" y="1020" width="1672" height="162.634146" fill="#ffffff"/>',glyph('References',24,1038,12.5,font='MarkerFelt-Wide')]
placement=[]
for col in range(4):
 y=top
 for idx in range(best[1][col],best[1][col+1]):
  e=entries[idx];ref=bibliography[idx];ls=all_lines[idx];first_y=y
  url=e.get('url') or e.get('doi')
  for n,line in enumerate(ls):
   x=xcols[col]+(7 if n else 0)
   merged=[]
   for kind,part in line:
    if merged and merged[-1][0]==kind:merged[-1]=(kind,merged[-1][1]+part)
    else:merged.append((kind,part))
   for kind,part in merged:
    footer.append(glyph(part,x,y,size,italic=(kind=='i'),url=url if kind=='u' else None));x+=measure(part,size)['width']
   assert x<=xcols[col]+colwidth+.05,(e['key'],x)
   y+=lineheight
  y+=gap
  placement.append({'key':e['key'],'column':col+1,'first_baseline':first_y,'last_baseline':y-gap-lineheight,'lines':len(ls),'display_suffix':e.get('suffix','')})
 assert y-lineheight<=bottom+0.1,(col,y)
footer.append('</g>');footer=''.join(footer)
out=s[:start]+header+footer+'</svg>'
assert out.replace(header+footer,oldheader,1)==original
(P/(stem+'.svg')).write_text(out)
proc.stdin.close();proc.wait()
for fmt in ['png','pdf']:
 args=['/opt/homebrew/bin/rsvg-convert']+(['-w','2400'] if fmt=='png' else ['-f','pdf'])+['-o',str(P/(stem+'.'+fmt)),str(P/(stem+'.svg'))];subprocess.run(args,check=True)
for label,box in [('header-close-up','350 0 930 255'),('references-close-up','0 1020 1672 162.634146')]:
 piece=header if label.startswith('header') else footer
 w,h=(2600,713) if label.startswith('header') else (5400,525)
 path=P/(stem+'-'+label+'.svg');path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="{box}"><rect x="0" y="0" width="1672" height="1183" fill="'+('#def6f5' if label.startswith('header') else '#ffffff')+f'"/>{piece}</svg>')
 subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w',str(w),'-o',str(path.with_suffix('.png')),str(path)],check=True)
md=['# Poster References — Harvard\n','Date: 5 October 2026. Generated from the selected verified registry entries. Alphabetical; italic work titles; access dates retained from actual retrieval. Display year suffixes normalised within this poster subset; canonical source keys are unchanged.\n']
for ref in bibliography:
 md.append(''.join('*'+t+'*' if k=='i' else '['+t+']('+t+')' if k=='u' else t for k,t in ref.segs)+'\n')
(P/(stem+'-references.md')).write_text('\n'.join(md))
checks={'base':base.name,'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'ten_cells_and_background_layers_preserved_exactly':True,'existing_header_letters_and_logos_preserved':True,'greenwich_box':[711,10,961,100],'title_and_subtitle_shift_y':42,'white_footer_y':1020,'footer_lettering_native':size,'footer_lettering_a0_pt':round(size*1189/1672*72/25.4,2),'reference_count':len(entries),'reference_source_states':states,'placements':placement,'lettering_bounds':records,'registry_build':'0 errors; existing 20 warnings and 20 informational notes retained in central registry report','review':'pending','pdfinfo':subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/(stem+'.pdf'))],capture_output=True,text=True,check=True).stdout}
(P/(stem+'-checks.json')).write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
(P/(stem+'-reference-selection.json')).write_text(json.dumps({'registry':'../04_references/references.json','entries':entries,'selection':'Current ten-panel evidence and concepts only; group proposals are not historical outcomes','canonical_keys':KEYS},ensure_ascii=False,indent=2)+'\n')
(P/(stem+'-prompt.md')).write_text('''# Header and References footer production brief\n\nMove the existing hand-drawn University of Greenwich logo to the centre above the title. Preserve the existing Denmark flag / Copenhagen meet / Green SM title, subtitle and shared logo payloads, shifting their complete row and subtitle down 42 native units. Leave ten white cells, body copy/numbers, vehicle, harbour, flags, right identity cloud and bounded left-cloud-removal patch unchanged.\n\nCover only the paving below native y=1020 with pure white through the A0 page edge. Add References in four alphabetical columns using controlled Chalkboard SE hand-drawn lettering, italic work titles, full clickable URLs and actual access dates. Render the selected verified references from the registry, normalising year suffixes within this selection while retaining canonical keys internally. Proposed budgets/KPIs/pilots are group proposals. No visible in-cell citation labels added. References are authorised by the latest student request, superseding the earlier no-visible-source decision for this footer. Produce full A0 PNG/PDF/SVG, header and References close-ups for human review.\n''')
print(json.dumps({'stem':stem,'reference_count':len(entries),'font_a0_pt':checks['footer_lettering_a0_pt'],'column_heights':best[2],'old_layers_preserved':True}))
