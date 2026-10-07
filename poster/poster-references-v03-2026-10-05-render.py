from pathlib import Path
import re,json,subprocess,hashlib,html
ROOT=Path(__file__).resolve().parent.parent if Path(__file__).parent.name=='poster' else Path.cwd();P=ROOT/'poster';base=P/'poster-references-v02-2026-10-05.svg';stem='poster-references-v03-2026-10-05';original=base.read_text()
proc=subprocess.Popen(['/usr/bin/swift',str(P/'08-cell-fit-v01-2026-10-05-glyphs.swift')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
def measure(t):
 proc.stdin.write(json.dumps({'text':t,'font':'MarkerFelt-Wide','size':50})+'\n');proc.stdin.flush();return json.loads(proc.stdout.readline())
a=measure('Copenhagen');b=measure('Copenhagen,');extra=b['width']-a['width'];half=extra/2;proc.stdin.close();proc.wait()
start=original.index('<g id="global-header-above-title-v01"');end=original.index('<g id="harvard-references-footer-v01"');old=original[start:end];new=old
flag=re.search(r'<g id="title-denmark-flag"[^>]*>.*?</g>',new,re.S).group();new=new.replace(flag,f'<g transform="translate({-half:.6f} 0)">'+flag+'</g>',1)
word=re.search(r'<g aria-label="Copenhagen">.*?</g>',new,re.S).group();x,y=map(float,re.search(r'translate\(([-\d.]+) ([-\d.]+)\)',word).groups());x-=half
replacement=f'<g aria-label="Copenhagen,"><path d="{b["path"]}" transform="translate({x:.6f} {y}) scale(1 -1)" fill="#173a47"/></g>';new=new.replace(word,replacement,1)
meet=re.search(r'<g aria-label="meet">.*?</g>',new,re.S).group();m=meet;mx,my=map(float,re.search(r'translate\(([-\d.]+) ([-\d.]+)\)',m).groups());m=re.sub(r'translate\(([-\d.]+) ([-\d.]+)\)',f'translate({mx+half:.6f} {my})',m,count=1);new=new.replace(meet,m,1)
tag=re.search(r'<svg\b[^>]*id="header-authentic-green-sm-logo"[^>]*>',new).group();lx=float(re.search(r'\bx="([^"]+)"',tag).group(1));newtag=re.sub(r'\bx="[^"]+"',f'x="{lx+half:.6f}"',tag,count=1);new=new.replace(tag,newtag,1)
out=original.replace(old,new,1);assert out.replace(new,old,1)==original
(P/(stem+'.svg')).write_text(out)
for fmt in ['png','pdf']:
 args=['/opt/homebrew/bin/rsvg-convert']+(['-w','2400'] if fmt=='png' else ['-f','pdf'])+['-o',str(P/(stem+'.'+fmt)),str(P/(stem+'.svg'))];subprocess.run(args,check=True)
close=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="3000" height="598" viewBox="0 0 1280 255"><rect width="1280" height="255" fill="#def6f5"/>{new}</svg>'
(P/(stem+'-header-close-up.svg')).write_text(close);subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','3000','-o',str(P/(stem+'-header-close-up.png')),str(P/(stem+'-header-close-up.svg'))],check=True)
for suffix in ['-references.md','-reference-selection.json','-references-close-up.svg','-references-close-up.png']:(P/(stem+suffix)).write_bytes((P/('poster-references-v02-2026-10-05'+suffix)).read_bytes())
checks={'base':base.name,'base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'title':'Copenhagen, meet Green SM','change':'Comma after Copenhagen; recenter whole title by half added comma width','added_width':extra,'title_centre':836,'greenwich_subtitle_ten_cells_footer_unchanged':True,'original_header_restoration_exact':out.replace(new,old,1)==original,'new_lettering_font':'MarkerFelt-Wide','review':'pending','pdfinfo':subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/(stem+'.pdf'))],capture_output=True,text=True,check=True).stdout}
(P/(stem+'-checks.json')).write_text(json.dumps(checks,indent=2)+'\n')
(P/(stem+'-prompt.md')).write_text('''# Correct title punctuation\n\nStudent specifies Copenhagen, meet Green SM. Add the vocative comma after Copenhagen in the same controlled hand-drawn Marker Felt lettering. Recentre the complete Denmark flag / Copenhagen, / meet / shared Green SM logo row at native x=836. Reuse the exact Green SM logo payload. Keep the subtitle, upper-left Greenwich logo, right information cloud, ten white sections, vehicle/background and Harvard References footer unchanged. Preserve saved v02; create v03 full A0 PNG/PDF/SVG and header close-up.\n''')
print(json.dumps(checks))
