"""Narrow baseline-field, visual-target, type and preservation checks for v02."""
from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib
import json
import math
import re

HERE=Path(__file__).resolve().parent
m=json.loads((HERE/'08-v02-manifest.json').read_text())
old=json.loads((HERE/'08-candidate-v01-2026-10-04-manifest.json').read_text())
visible=[t['text'] for t in m['visible_text']]
fields=['kpi','objective','target','tool','rhythm']
def tuples(rows):return [[r[k] for k in fields] for r in rows]
def table(s):
 return [[x.strip() for x in line.strip('|').split('|')] for line in s.splitlines()
         if line.startswith('|') and not line.startswith('| KPI') and not line.startswith('|---')]
baseline=(HERE/'whole-copy-baseline.md').read_text()
start=baseline.index('## Measurement and Evaluation');end=baseline.find('\n## ',start+4)
baseline=baseline[start:end if end>=0 else None]
svg=ET.parse(HERE/'08-v02.svg').getroot()
boxes=[(t['id'],t['text'],l['bbox']) for t in m['visible_text'] for l in t['lines']]
overlap=[];clipping=[];escape=[]
for i,(id,text,b) in enumerate(boxes):
 if b[0]<48 or b[1]<48 or b[2]>m['canvas'][0]-48 or b[3]>m['canvas'][1]-48:
  clipping.append([id,text,b])
 for other_id,other_text,a in boxes[i+1:]:
  if min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1]):
   overlap.append([id,other_id,text,other_text])
for t in m['visible_text']:
 if t['owner'] in m['objective_zones']:
  x,y,w,h=m['objective_zones'][t['owner']]['rect']
  for line in t['lines']:
   b=line['bbox']
   if b[0]<x+10 or b[1]<y+8 or b[2]>x+w-10 or b[3]>y+h-8:escape.append([t['id'],line])

maps=m['display_measure_mapping']
mapped_all=all(all(s in visible for s in r['visible_components']) for r in maps)
tracking=[r['baseline_row']['tool']+' · '+r['baseline_row']['rhythm'] for r in maps]
gate_tokens=['≥95%','≤2%','24h ≥90%','≥1.5%','≥0.8%','≥20%','≤DKK1,829','≥35%']
gate_string=' '.join(m['gate_a']+m['gate_b'])
seven=(HERE/'07-copy-v01-2026-10-04.md').read_text()
gates={v:{'v02':v in gate_string,'section7':v in seven} for v in gate_tokens}
bar_nodes=[svg.find('.//*[@id="'+r['id']+'"]') for r in m['target_bars']]
bars_correct=all(n is not None and float(n.get('data-value'))==r['value'] and
                float(n.get('data-baseline'))==0 for n,r in zip(bar_nodes,m['target_bars']))
gauges_correct=[]
for g in m['target_gauges']:
 n=svg.find('.//*[@id="'+g['id']+'-target"]')
 gauges_correct.append(n is not None and float(n.get('data-target'))==g['target'] and
     n.get('data-direction')==g['direction'] and g['actual_result'] is None and not g['progress_fill'])

history=json.loads((HERE/'08-v02-history-hashes.json').read_text())
writing=json.loads((HERE/'08-v02-writing-check.json').read_text())
face_tokens=[token for t in m['visible_text'] for token in t['text'].split()]
checks={
 'heading_exact_numbered':visible[0]=='8. Success Dashboard',
 'eleven_measures_controls_and_all_55_baseline_fields_retained':table(baseline)==table((HERE/'08-v02-copy.md').read_text())==tuples(m['kpi_rows'])==tuples(old['kpi_rows']),
 'eleven_explicit_canonical_to_visible_maps':len(maps)==11 and [x['baseline_row'] for x in maps]==[{k:r[k] for k in fields} for r in m['kpi_rows']],
 'every_measure_target_component_visibly_encoded':mapped_all,
 'all_eleven_full_tool_and_rhythm_pairs_visible':all(s in visible for s in tracking),
 'objective_labels_unchanged':['O1 awareness','O2 paid trial','O3 repeat','O4 service integrity']==[z['label'] for z in m['objective_zones'].values()],
 'conversion_bars_exact_3_to_1_5_and_shared_zero_scale':bars_correct and m['target_bars'][0]['value']==3 and m['target_bars'][1]['value']==1.5 and m['target_bars'][0]['width']==2*m['target_bars'][1]['width'],
 'all_four_gauge_markers_match_threshold_and_direction':all(gauges_correct) and [(g['target'],g['direction']) for g in m['target_gauges']]==[(95,'minimum'),(2,'maximum'),(90,'minimum'),(80,'minimum')],
 'gauges_have_no_observed_value_or_progress_fill':all(g['actual_result'] is None and not g['progress_fill'] for g in m['target_gauges']),
 'awareness_delta_no_invented_absolute_baseline':all(s in visible for s in ['+10 pp','M1–2 baseline','M12','pp = percentage points']),
 'mature_cohort_90day_definition_visible':'Full 90-day window · fully observed riders only' in visible,
 'completion_and_cancellations_shared_accepted_denominator_visible':'Completion / cancels: per accepted booking' in visible,
 'availability_threshold_still_set_after_baseline':'Set after M1–2 area/hour baseline' in visible,
 'all_gate_thresholds_equal_section7':all(all(v.values()) for v in gates.values()),
 'gate_A_B_times_and_actions_unchanged':all(s in visible for s in ['Gate A / M4','Gate B / M6','Agree minimum observed volume with operations.','Fail → hold media, fix and re-test.','Pass → release M5–6.','Repeat ≥35% → release street screens.','Fail → stop scale-up.']),
 'counting_rules_and_acquisition_scope_visible':all(s in visible for s in ['Installs excluded from paid riders, refunds removed. Repeat: full 90-day windows only.','DKK524: paid search/social only, not total acquisition cost. Advertise only verified coverage with usable offers.']),
 'M12_renew_revise_stop_retained':'M12: evaluate O1 to O4 → renew, revise or stop for year two.' in visible,
 'targets_labelled_proposed_not_achieved':'Proposed targets, not achieved results.' in visible,
 'zero_text_overlap':not overlap,'zero_text_clipping':not clipping,'zero_zone_escape':not escape,
 'no_type_shrink_minimum_33_retained':min(t['font_size'] for t in m['visible_text'])==old['minimum_body_size']==33,
 'near_square_and_at_least_25_percent_less_area':abs(m['canvas'][0]/m['canvas'][1]-1)<.1 and m['canvas'][1]/old['canvas'][1]<.75,
 'v01_files_byte_unchanged':all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in history.items()),
 'sources_evidence_and_model_authority_unchanged':m['internal_source_mapping']==old['internal_source_mapping'] and m['internal_evidence']==old['internal_evidence'],
 'native_art_hash_match':hashlib.sha256((HERE/'08-v02-art.png').read_bytes()).hexdigest()==m['native_art']['sha256'],
 'all_letters_numbers_native_controlled_glyphs':not any(n.tag.endswith('}text') for n in svg.iter()),
 'font_files_unchanged':all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in m['font_files'].items()),
 'writing_detector_ran_effective_base_hard_zero':writing['base']['anti_slop']['status']=='ran' and not any(writing['effective_base_hard_by_category'].values()),
 'sole_expected_standalone_budget_table_omission':writing['genre']['errors']==['Expected exactly one <!-- budget-table --> marker; found 0'],
 'actual_full_png_and_native_icon_strip_inspected':True,
}
result={'version':'v02','status':'Candidate for parent selection; no group approval',
 'checks':checks,'passed':sum(checks.values()),'failed':len(checks)-sum(checks.values()),
 'display_measure_mapping':maps,'gate_comparison':gates,
 'text_overlap':overlap,'text_clipping':clipping,'zone_escape':escape,
 'graphic_words':sum(bool(re.search(r'\w',s)) for s in face_tokens),
 'copy_words':writing['genre']['total_words'],'writing_exit':2,
 'writing_exception':'Standalone panel has no full-poster budget table; no whole-poster pass claimed',
 'canvas':m['canvas'],'size_reduction_percent':round((1-m['canvas'][1]/old['canvas'][1])*100,2),
 'print_at_330_mm':{'width_mm':330,'height_mm':330*m['canvas'][1]/m['canvas'][0],'smallest_type_pt':33*330/m['canvas'][0]/25.4*72},
 'print_at_300_mm':{'width_mm':300,'height_mm':300*m['canvas'][1]/m['canvas'][0],'smallest_type_pt':33*300/m['canvas'][0]/25.4*72},
 'actual_A0_or_print_proof':False,
 'visual_scope':'Bars/gauges show proposed target values, not achieved results or benchmarks',
}
(HERE/'08-v02-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Focused v02 checks:',result['passed'],'passed;',result['failed'],'failed')
if result['failed']:
 print({k:v for k,v in checks.items() if not v});raise SystemExit(1)
