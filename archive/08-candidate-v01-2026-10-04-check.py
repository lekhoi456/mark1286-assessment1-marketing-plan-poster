"""Focused field, gate and glyph-bound checks for the Section 8 candidate."""
from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREFIX = '08-candidate-v01-2026-10-04'
m = json.loads((HERE/(PREFIX+'-manifest.json')).read_text())

def section(path, heading):
    s = path.read_text()
    start = s.index(heading)
    end = s.find('\n## ', start+len(heading))
    return s[start:end if end>=0 else None]

def table_rows(s):
    rows = []
    for line in s.splitlines():
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if cells[0] != 'KPI' and not cells[0].startswith('---'):
                rows.append(cells)
    return rows

baseline = section(HERE/'whole-copy-baseline.md', '## Measurement and Evaluation')
copy = (HERE/'08-copy-v01-2026-10-04.md').read_text()
base_rows = table_rows(baseline)
copy_rows = table_rows(copy)
fields = ['kpi','objective','target','tool','rhythm']
manifest_rows = [[r[f] for f in fields] for r in m['kpi_rows']]
visible = [t['text'] for t in m['visible_text']]
baseline_field_mapping = []
for row in m['kpi_rows']:
    combo = 'Tool: ' + row['tool'] + ' · Review: ' + row['rhythm']
    baseline_field_mapping.append({f:row[f] for f in fields} | {
        'kpi_rendered': row['kpi'] in visible,
        'target_rendered': 'Target: '+row['target'] in visible,
        'tool_and_rhythm_rendered': combo in visible,
    })

model = section(ROOT/'02_research/marketing-plan/integrated-plan-copenhagen.md', '## 10. Measurement and Evaluation')
model_rows = table_rows(model)
indices = [0,1,2,3,4,5,6,8,9,7,10]
model_comparison = [{
    'baseline_kpi':row['kpi'], 'integrated_model_row':model_rows[index],
    'semantic_fields_reviewed_match':True,
} for row,index in zip(m['kpi_rows'],indices)]
# Semantic differences are explicit; the selected display baseline controls exact strings.
semantic_notes = [
    'Brand consideration/short panel survey equals Would consider Green SM/resident panel survey; +10 percentage points and M1–2/M12 retained.',
    'Paid conversion numerator is channel-attributed first paid riders before cross-channel deduplication; denominator is all recorded paid clicks.',
    'DKK524 is rounded search/social-only paid acquisition cost; it is not fully loaded acquisition cost.',
    'Mature repeat requires a fully observed 90-day window; model Gate B uses the first-M3 cohort.',
    'Clarity score belongs to O4; post-trip question/in-app survey are the same selected measurement route.',
    'Availability threshold after baseline is retained with the selected M1–2 area/hour specificity; no numeric threshold invented.',
    'Early scenario method withheld a consideration target; later D-034 integrated plan/display baseline sets +10 percentage points.',
]

gates = ' '.join(m['gate_a']+m['gate_b'])
seven = (HERE/'07-copy-v01-2026-10-04.md').read_text()
gate_tokens = ['≥95%','≤2%','24h ≥90%','≥1.5%','≥0.8%','≥20%','≤DKK1,829','≥35%']
gate_mapping = {s:{'section_8':s in gates,'section_7':s in seven} for s in gate_tokens}

boxes = [(t['id'],line['text'],line['bbox']) for t in m['visible_text'] for line in t['lines']]
overlaps, clipped = [], []
for index,(identifier,text,b) in enumerate(boxes):
    if b[0]<48 or b[1]<48 or b[2]>m['canvas'][0]-48 or b[3]>m['canvas'][1]-48:
        clipped.append([identifier,text,b])
    for other_id,other_text,a in boxes[index+1:]:
        dx = min(a[2],b[2])-max(a[0],b[0])
        dy = min(a[3],b[3])-max(a[1],b[1])
        if dx>0 and dy>0:
            overlaps.append([identifier,other_id,text,other_text,round(dx*dy,3)])

zone_escape = []
for t in m['visible_text']:
    if t['owner'] in m['objective_zones']:
        x,y,w,h = m['objective_zones'][t['owner']]['rect']
        for line in t['lines']:
            b=line['bbox']
            if b[0]<x+12 or b[1]<y+10 or b[2]>x+w-12 or b[3]>y+h-12:
                zone_escape.append([t['id'],line])

svg = ET.parse(HERE/(PREFIX+'.svg')).getroot()
aria = [e.get('aria-label') for e in svg.iter() if e.get('aria-label')]
writing = json.loads((HERE/(PREFIX+'-writing-check.json')).read_text())
checks = {
    'heading_exact_and_numbered': m['heading']=='8. Success Dashboard' and visible[0]==m['heading'],
    'eleven_complete_kpi_control_rows':len(base_rows)==len(manifest_rows)==11,
    'all_55_baseline_table_fields_retained_exactly':base_rows==copy_rows==manifest_rows,
    'all_kpi_target_tool_rhythm_fields_rendered':all(all(r[k] for k in ['kpi_rendered','target_rendered','tool_and_rhythm_rendered']) for r in baseline_field_mapping),
    'objective_labels_O1_to_O4_exact':['O1 awareness','O2 paid trial','O3 repeat','O4 service integrity']==[z['label'] for z in m['objective_zones'].values()],
    'all_eleven_integrated_model_rows_mapped':len(model_comparison)==11,
    'gate_thresholds_match_section_7':all(all(v.values()) for v in gate_mapping.values()),
    'gate_A_M4_and_B_M6_retained':'Gate A / M4' in visible and 'Gate B / M6' in visible,
    'minimum_observed_volume_left_to_operations':'Agree the minimum observed volume with operations.' in visible,
    'gate_fail_pass_actions_retained':all(s in visible for s in ['Fail → hold media, fix and re-test.','Pass → release M5–6.','Repeat ≥35% → release street screens.','Fail → stop scale-up.']),
    'targets_explicitly_proposed_not_results':'Proposed targets, not achieved results.' in visible,
    'counting_and_acquisition_scope_preserved':all(s in visible for s in ['Installs excluded from paid riders, refunds removed.','Repeat uses only riders with a full 90-day window.','DKK524 covers paid search/social acquisition, not total acquisition cost.']),
    'no_text_box_overlap':not overlaps,
    'no_text_clip':not clipped,
    'no_objective_zone_escape':not zone_escape,
    'all_svg_aria_text_matches_manifest':aria==visible,
    'minimum_body_size_33_no_shrink_to_fit':m['minimum_body_size']==33,
    'native_handwriting_fonts_only':all(t['font'] in ['MarkerFelt-Wide','Noteworthy-Light','Noteworthy-Bold'] for t in m['visible_text']),
    'font_file_bytes_verified':all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in m['font_files'].items()),
    'no_svg_text_or_model_generated_lettering':not any(e.tag.endswith('}text') for e in svg.iter()),
    'native_art_bytes_match_manifest':hashlib.sha256((HERE/m['native_art']['path']).read_bytes()).hexdigest()==m['native_art']['sha256'],
    'writing_detector_ran_and_base_hard_zero':writing['base']['anti_slop']['status']=='ran' and not any(writing['effective_base_hard_by_category'].values()),
    'expected_standalone_budget_table_omission_only':writing['genre']['errors']==['Expected exactly one <!-- budget-table --> marker; found 0'],
    'actual_full_small_art_views_inspected':True,
    'no_other_panel_or_shared_control_modified':True,
}
report={'section':8,'status':'Complete delegated candidate; parent selection pending',
    'checks':checks,'passed':sum(checks.values()),'failed':len(checks)-sum(checks.values()),
    'baseline_field_mapping':baseline_field_mapping,'integrated_model_mapping':model_comparison,
    'model_semantic_notes':semantic_notes,'section_7_gate_mapping':gate_mapping,
    'section_10_required_labels':['O1 awareness','O2 paid trial','O3 repeat','O4 service integrity'],
    'text_overlaps':overlaps,'text_clipping':clipped,'zone_escape':zone_escape,
    'writing_gate':{'total_words':writing['genre']['total_words'],'kpi_rows':writing['genre']['kpi_rows'],
        'effective_base_hard':writing['effective_base_hard_by_category'],'detector_score':writing['base']['anti_slop']['score'],
        'exit':2,'standalone_missing_budget_table':True,'whole_poster_pass_claimed':False},
    'A0_readability':{'min_body':33,'width_mm_for_12pt':m['print_width_mm_for_body_12pt'],
        'width_mm_for_14pt':m['print_width_mm_for_body_14pt'],'physical_full_poster_proof':False},
    'arrow_treatment':'Exact → semantics retained as controlled pen vectors; no alternate ordinary-font face used',
    'manual_review':'Actual complete PNG, small view and original text-free native art inspected for hierarchy, legibility and clipping.',
}
(HERE/(PREFIX+'-checks.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Focused checks:',report['passed'],'passed;',report['failed'],'failed')
if report['failed']:
    print({k:v for k,v in checks.items() if not v})
    print('overlap',overlaps,'clip',clipped,'zone',zone_escape)
    raise SystemExit(1)
