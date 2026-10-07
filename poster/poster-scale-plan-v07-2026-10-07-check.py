"""Check the final front, proof v07 (D-166), against model v02, the v03 build and proof v06.

Usage: python3 -B poster/poster-scale-plan-v07-2026-10-07-check.py SOURCE.svg OUT_DIR
Reads OUT_DIR/poster-scale-plan-v07-2026-10-07{.svg,-changes.json}; writes
OUT_DIR/poster-scale-plan-v07-2026-10-07-checks.json. The back of chart is
poster-scale-plan-v04-2026-10-07-back.* (checked by the v04 check).
"""
import contextlib
import importlib.util
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEM = 'poster-scale-plan-v07-2026-10-07'


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r3 = load('r3', 'poster-content-upgrade-v03-2026-10-07-render.py')
c3 = load('c3', 'poster-content-upgrade-v03-2026-10-07-check.py')
c4 = load('c4', 'poster-scale-plan-v04-2026-10-07-check.py')
r7 = load('r7', 'poster-scale-plan-v07-2026-10-07-render.py')
MODEL = load('model2', 'scale-plan-v02-2026-10-07-model.py')

# bar labels are checked against the model below, so the v04 bar strings are dropped here
REQUIRED = [r7.TEXT.get(s, s) for s in c4.REQUIRED if not re.fullmatch(r'\d\.\dM / \d+%', s)] + list(r7.TEXT.values())
FORBIDDEN = c4.FORBIDDEN + ['6.0M / 20%', '2.4M / 8%', 'base revenue', 'Base case', '15/car/day average',
                            'trips per car per day', 'All targets and pilots are group proposals']


def main():
    source, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    src = source.read_text()
    front = (out_dir / f'{STEM}.svg').read_text()
    log = json.loads((out_dir / f'{STEM}-changes.json').read_text())['changes']
    with contextlib.redirect_stdout(io.StringIO()):
        base, _, _ = r3.build(src)
    checks = {}
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        argv, sys.argv = sys.argv, [sys.argv[0]]
        MODEL.main()
        sys.argv = argv
    model = json.loads(buf.getvalue())
    checks['model_v02_pass'] = model['pass']

    old, new = c4.labels(base), c4.labels(front)
    old_c, new_c = Counter(l for l, _, _ in old), Counter(l for l, _, _ in new)
    declared_from = {c['from'] for c in log if 'from' in c}
    removed = sorted(l for l in old_c if new_c[l] < old_c[l])
    checks['removed_labels_all_declared'] = sorted(set(removed) - declared_from)
    keep = {(l, d, t) for l, d, t in old if l not in declared_from}
    checks['unchanged_lettering_byte_identical'] = len(keep - {(l, d, t) for l, d, t in new}) == 0
    checks['unchanged_lettering_count'] = len(keep)
    # '≥2,500 paid trips a day' is the D-166 M6 floor; any other 2,500 would be the old 2,500-ride target
    text = '\n'.join(l for l, _, _ in new if l != '≥2,500 paid trips a day')
    checks['required_missing'] = [r for r in REQUIRED if r not in new_c]
    checks['forbidden_present'] = [f for f in FORBIDDEN if f in text]

    bars = re.findall(r'<path d="M925 ([\d.]+)H([\d.]+)V[\d.]+H925Z" fill="(#28bdbf|#e3bb42)"', front)
    values = [round((float(x) - 925) / 65 * 8, 2) for _, x, _ in sorted(bars, key=lambda b: float(b[0]))]
    checks['bar_values_dkk_m'] = values
    checks['bars_match_model'] = values == [v for _, v in MODEL.BUDGET]
    shares = model['budget_shares_pct']
    checks['bar_labels_match_model'] = all(f'{v:.1f}M / {shares[k]}%' in new_c for k, v in MODEL.BUDGET)
    g, k = MODEL.GATES, MODEL.KPI
    checks['caps_match_model'] = (f"DKK{g['M4 cumulative cap']}M" in new_c and f"DKK{g['M6 cumulative cap']}M" in new_c
                                  and f"DKK{g['M7-12 scale release'] + g['contingency held']}M" in new_c)
    checks['kpis_match_model'] = (f"{k['first_paid_riders_m12']:,}" in new_c
                                  and f"≥{k['first_paid_riders_m4']:,} first paid riders" in new_c
                                  and f"≥{k['first_paid_riders_m6']:,} first paid riders" in new_c
                                  and f"≤DKK{k['media_cac_cap_m12']}" in new_c
                                  and f"Media CAC ≤DKK{k['media_cac_cap_m4_m6']}" in new_c
                                  and f"{k['paid_trips_run_rate_m12'] / 1e6}M" in new_c
                                  and f"≥{k['paid_trips_per_day_m6_floor']:,} paid trips a day" in new_c)
    checks['six_percent_matches_model'] = round(model['checks']['budget_share_of_run_rate_revenue_pct']) == 6

    checks['connector_groups_left'] = len(re.findall(r'id="(?:connected-cells-v01|link-\d+-\d+)"', front))
    allowed = c3.ALLOWED_CELL_COLOURS | {'#f7ebc6'}
    body = re.sub(r'data:image/[^"]+', '', front)
    checks['old_off_palette_colours_remaining'] = sorted(c for c in r3.COLOUR_MAP if re.search(re.escape(c), body, re.I))
    i = body.find('id="section-01-v07-candidate"')
    j = body.find('id="proportional-car-placement"', i)
    cells = body[i:j if j > i else None]
    for flagged in ('fit01-flag-', 'fit01-vinfast', 'fit01-background-vingroup', 'drawn-path'):
        cells = re.sub(rf'<(?:g|svg|path) id="{flagged}[^"]*".*?</(?:g|svg)>|<path id="{flagged}[^"]*"[^>]*/>', '', cells, flags=re.S)
    used = {c.lower() for c in re.findall(r'#[0-9a-fA-F]{6}\b', cells)}
    checks['cell_colours_outside_palette_unprotected'] = sorted(used - allowed - c3.PROTECTED)
    cloud = re.findall(r'<text x="1387" y="[\d.]+"[^>]*>([^<]*)</text>', front)
    checks['cloud_lines'] = cloud
    for needle in ('href="poster-a0-layout-v02-2026-10-04-background.png"',
                   'href="poster-draft-car-background-v09-art-2026-10-04.png"'):
        checks[f'external_link_kept {needle[6:-1]}'] = front.count(needle) == base.count(needle)
    checks['no_contribution_strip'] = 'member-contributions-strip' not in front

    checks['pass'] = bool(
        checks['model_v02_pass'] and not checks['removed_labels_all_declared']
        and checks['unchanged_lettering_byte_identical'] and not checks['required_missing']
        and not checks['forbidden_present'] and checks['bars_match_model'] and checks['bar_labels_match_model']
        and checks['caps_match_model'] and checks['kpis_match_model'] and checks['six_percent_matches_model']
        and not checks['connector_groups_left'] and not checks['old_off_palette_colours_remaining']
        and not checks['cell_colours_outside_palette_unprotected'] and len(cloud) == 7
        and checks['no_contribution_strip'])
    checks['not_checked_here'] = [
        'car/harbour background PNGs are external and absent from the cloud session; previews omit them',
        'Chalkboard SE rendering of the cloud text (macOS font) — verify locally',
        'mba-presentation-style presentcheck.py on changed copy — run locally',
        'native Danish check: København, mød Green SM; Elektrisk taxa. Tjek prisen. Book i appen.',
        'actual-size print legibility',
    ]
    (out_dir / f'{STEM}-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=1))
    print(json.dumps(checks, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
