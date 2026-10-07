from pathlib import Path
import re,json,subprocess,hashlib
ROOT=Path(__file__).resolve().parent.parent if Path(__file__).parent.name=='poster' else Path.cwd()
P=ROOT/'poster';oldstem='poster-references-v01-2026-10-05';stem='poster-references-v02-2026-10-05'
base=P/(oldstem+'.svg');s=base.read_text()
old=re.search(r'<image\b[^>]*id="greenwich-hand-drawn-logo"[^>]*/>',s).group();new=old
for k,v in [('x','45'),('y','10'),('width','310'),('height','105')]:new=re.sub(r'\b'+k+r'="[^"]*"',k+'="'+v+'"',new)
out=s.replace(old,new,1);assert out.replace(new,old,1)==s
(P/(stem+'.svg')).write_text(out)
for fmt in ['png','pdf']:
 args=['/opt/homebrew/bin/rsvg-convert']+(['-w','2400'] if fmt=='png' else ['-f','pdf'])+['-o',str(P/(stem+'.'+fmt)),str(P/(stem+'.svg'))];subprocess.run(args,check=True)
header=out[out.index('<g id="global-header-above-title-v01"'):out.index('<g id="harvard-references-footer-v01"')]
close=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="3000" height="598" viewBox="0 0 1280 255"><rect width="1280" height="255" fill="#def6f5"/>{header}</svg>'
(P/(stem+'-header-close-up.svg')).write_text(close)
subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','3000','-o',str(P/(stem+'-header-close-up.png')),str(P/(stem+'-header-close-up.svg'))],check=True)
for suffix in ['-references.md','-reference-selection.json','-references-close-up.svg','-references-close-up.png']:(P/(stem+suffix)).write_bytes((P/(oldstem+suffix)).read_bytes())
checks=json.loads((P/(oldstem+'-checks.json')).read_text());checks.update({'base':base.name,'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'greenwich_box':[45,10,355,115],'only_greenwich_placement_changed':True,'title_subtitle_cells_and_references_preserved_exactly':True,'logo_payload_preserved':re.search(r'href="([^"]+)"',old).group(1)==re.search(r'href="([^"]+)"',new).group(1),'visual_review':'pending','review':'pending','pdfinfo':subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/(stem+'.pdf'))],capture_output=True,text=True,check=True).stdout})
(P/(stem+'-checks.json')).write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
(P/(stem+'-prompt.md')).write_text('''# Greenwich at upper left; centred title and Harvard footer\n\nStudent clarification: University of Greenwich remains on the left, placed higher than the title and close to the page top. It must not be centred above the title. Reuse the exact hand-drawn logo payload at native x=45, y=10, width=310, height=105. Preserve the centred Denmark flag / Copenhagen meet / Green SM title and subtitle positions from the previous References proof, all ten white cells, group cloud, vehicle and landmarks. Keep the white lower footer and its seventeen alphabetical Harvard references unchanged. Export full A0 PNG/PDF/SVG and a header close-up for human review.\n''')
print(json.dumps({'stem':stem,'changed':'Greenwich logo position/size only','greenwich_box':checks['greenwich_box'],'a0_pdf':True}))
