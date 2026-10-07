"""Build the Section 8 candidate from exact baseline KPI fields and local glyphs."""
from pathlib import Path
import base64
import hashlib
import importlib.util
import json
import subprocess

HERE = Path(__file__).resolve().parent
PREFIX = '08-candidate-v01-2026-10-04'
spec = importlib.util.spec_from_file_location('dashboard_layout', HERE / (PREFIX + '-layout.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
W, H = 2200, 2710
L = module.Layout(W, H, HERE / (PREFIX + '-glyphs.swift'))
copy = (HERE / '08-copy-v01-2026-10-04.md').read_text()
rows = []
for line in copy.splitlines():
    if not line.startswith('|'):
        continue
    cells = [s.strip() for s in line.strip('|').split('|')]
    if cells[0] != 'KPI' and not cells[0].startswith('---'):
        rows.append(dict(zip(['kpi', 'objective', 'target', 'tool', 'rhythm'], cells)))
assert len(rows) == 11
art = HERE / (PREFIX + '-generated-art.png')
L.frame('outer-frame', 32, 34, W-64, H-68, stroke=module.INK, thick=3)
L.text('8. Success Dashboard', 92, 145, 92, 'MarkerFelt-Wide', role='heading')
L.rule(93, 171, 1075, module.GOLD, 13)
L.text('Proposed targets, not achieved results.', 95, 232, 40, 'Noteworthy-Bold', role='assumption')
L.parts.append(f'<image id="native-tracking-art" x="1450" y="68" width="645" height="215" href="data:image/png;base64,{base64.b64encode(art.read_bytes()).decode()}"/>')

zones = {
    'O1': {'label': 'O1 awareness', 'rect': [85, 310, 980, 310]},
    'O2': {'label': 'O2 paid trial', 'rect': [85, 650, 980, 760]},
    'O3': {'label': 'O3 repeat', 'rect': [1135, 310, 980, 310]},
    'O4': {'label': 'O4 service integrity', 'rect': [1135, 650, 980, 1065]},
}

def metric(row, x, y, width, owner):
    start = y
    y = L.text(row['kpi'], x, y, 36, 'Noteworthy-Bold', width, 'kpi', owner) + 54
    y = L.text('Target: ' + row['target'], x, y, 43, 'Noteworthy-Bold', width, 'target', owner) + 48
    y = L.text('Tool: ' + row['tool'] + ' · Review: ' + row['rhythm'], x, y, 33,
        'Noteworthy-Light', width, 'tool-and-rhythm', owner) + 24
    row['display_bounds'] = [x, start-40, x+width, y]
    return y

for objective, zone in zones.items():
    x, y, width, height = zone['rect']
    L.frame('zone-' + objective, x, y, width, height, fill='#fffefa')
    L.rule(x+28, y+70, width-55, module.CYAN, 10)
    L.text(zone['label'], x+28, y+57, 46, 'MarkerFelt-Wide', role='objective', owner=objective)
    cursor = y+122
    objective_rows = [r for r in rows if r['objective'] == objective]
    for i, row in enumerate(objective_rows):
        cursor = metric(row, x+30, cursor, width-60, objective)
        if i != len(objective_rows)-1:
            L.rule(x+28, cursor+8, width-55, '#a9c2bd', 2)
            cursor += 44
    zone['content_bottom'] = cursor

L.frame('spend-control', 85, 1450, 980, 265, fill='#fff9dc', stroke='#d3b743')
L.text('Spend control', 115, 1507, 44, 'MarkerFelt-Wide', role='control-heading', owner='Spend control')
spend = next(r for r in rows if r['objective'] == 'Spend control')
metric(spend, 115, 1559, 920, 'Spend control')

L.frame('counting', 85, 1755, 2030, 305, fill='#f3faf5')
L.text('Counting rules', 116, 1816, 43, 'MarkerFelt-Wide', role='counting-heading')
counting = [
    'Installs excluded from paid riders, refunds removed.',
    'Repeat uses only riders with a full 90-day window.',
    'DKK524 covers paid search/social acquisition, not total acquisition cost.',
    'Advertise only verified coverage with usable offers.',
]
for i, line in enumerate(counting):
    L.text(line, 118, 1867+i*50, 36, 'Noteworthy-Light', 1940, 'counting')

gate_a = [
    'Completion ≥95% · service cancellations ≤2%',
    'Referenced complaints answered within 24h ≥90%',
    'Search conversion ≥1.5% · social ≥0.8%',
    'Agree the minimum observed volume with operations.',
    'Fail → hold media, fix and re-test.',
    'Pass → release M5–6.',
]
gate_b = [
    'Mature-cohort 90-day repeat ≥20%',
    'and paid cost per first rider ≤DKK1,829 → continue.',
    'Repeat ≥35% → release street screens.',
    'Fail → stop scale-up.',
]
for key, x, title, lines in [('A',85,'Gate A / M4',gate_a),('B',1135,'Gate B / M6',gate_b)]:
    L.frame('gate-'+key, x, 2100, 980, 415, fill='#fff9dc', stroke='#d3b743')
    L.text(title, x+30, 2160, 48, 'MarkerFelt-Wide', role='gate-heading')
    for i, line in enumerate(lines):
        L.text(line, x+30, 2216+i*49, 34, 'Noteworthy-Bold' if i>=len(lines)-2 else 'Noteworthy-Light',
            920, 'gate-'+key)
L.rule(88, 2550, 2025, module.CYAN, 3)
L.text('M12: evaluate O1 to O4, then renew, revise or stop for year two.', 110, 2602, 37, 'Noteworthy-Bold', 1980, 'review')
L.text('Floors and targets are planning assumptions.', 112, 2650, 34, 'Noteworthy-Light', 1950, 'assumption')
svg = L.close()
svg_path = HERE / (PREFIX + '.svg')
svg_path.write_text(svg)
for suffix, size in [('.png', []), ('-small.png', ['-w','1100'])]:
    subprocess.run(['/opt/homebrew/bin/rsvg-convert', *size, '-o', str(HERE/(PREFIX+suffix)), str(svg_path)], check=True)
manifest = {
    'section': 8, 'heading': '8. Success Dashboard', 'canvas': [W,H],
    'status': 'Complete delegated candidate; parent selection pending; no group approval claimed',
    'authority': 'Controller delegation on 4 October 2026',
    'copy_source': '08-copy-v01-2026-10-04.md', 'baseline': 'poster/whole-copy-baseline.md, Measurement and Evaluation',
    'kpi_rows': rows, 'objective_zones': zones, 'gate_a': gate_a, 'gate_b': gate_b,
    'visible_text': L.texts, 'frames': L.frames, 'minimum_body_size': 33,
    'font_files': {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path('/System/Library/Fonts/MarkerFelt.ttc'),Path('/System/Library/Fonts/Noteworthy.ttc')]},
    'fonts': ['MarkerFelt-Wide','Noteworthy-Light','Noteworthy-Bold'], 'fallback_fonts': False,
    'controlled_arrow_vectors': True, 'no_ordinary_font_fallback': True,
    'native_art': {'path': art.name, 'sha256':hashlib.sha256(art.read_bytes()).hexdigest(),
        'placement':[1450,68,645,215], 'generated_lettering_or_data':False},
    'internal_evidence': ['E-020','E-021'],
    'evidence_scope': 'Company-objective context only; numeric targets/floors remain planning assumptions, not source observations',
    'internal_decisions':['D-033','D-034'],
    'internal_source_mapping': [
        {'evidence':'E-020','key':'konkurrence-og-forbrugerstyrelsen-2026b',
         'pdf':'04_references/konkurrence-og-forbrugerstyrelsen-2026b-uber-dantaxi-afgoerelse.pdf',
         'physical_page':175,'scope':'Stable local operation before rapid expansion; internal objective/gate rationale only'},
        {'evidence':'E-021','key':'konkurrence-og-forbrugerstyrelsen-2026b',
         'pdf':'04_references/konkurrence-og-forbrugerstyrelsen-2026b-uber-dantaxi-afgoerelse.pdf',
         'physical_page':179,'scope':'Awareness investment challenge; no measured starting awareness or source support for proposed +10-point target'},
    ],
    'method_source':'02_research/marketing-plan/budget-kpi-scenarios.md, conversion measurement contract and §5 KPI recommendations',
    'target_authority':'Integrated plan §10/§13 A6, D-033 and D-034; exact selected display baseline values retained',
    'concept_locators': ['w04-lecture slide 12','w04-tutorial slide 10'],
    'visible_citations':False, 'observed_baselines_or_results':False,
    'print_width_mm_for_body_12pt':round(12/72*25.4*W/33,1),
    'print_width_mm_for_body_14pt':round(14/72*25.4*W/33,1),
    'A0_limitation': 'Dedicated tall panel footprint required; actual full-poster fit/printed readability not established',
    'svg_sha256':hashlib.sha256(svg_path.read_bytes()).hexdigest(),
}
(HERE/(PREFIX+'-manifest.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Rendered Section 8 candidate; zone content bottoms:', {k:z['content_bottom'] for k,z in zones.items()})
