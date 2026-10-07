"""Check scaled-plan proof v04 (D-163) against the model, the v03 build and the back page.

Usage: python3 -B poster/poster-scale-plan-v04-2026-10-07-check.py SOURCE.svg OUT_DIR
Reads OUT_DIR/poster-scale-plan-v04-2026-10-07{.svg,-back.svg,-changes.json};
writes OUT_DIR/poster-scale-plan-v04-2026-10-07-checks.json.
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
STEM = 'poster-scale-plan-v04-2026-10-07'


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r3 = load('r3', 'poster-content-upgrade-v03-2026-10-07-render.py')
c3 = load('c3', 'poster-content-upgrade-v03-2026-10-07-check.py')
MODEL = load('model', 'scale-plan-v01-2026-10-07-model.py')
LABEL = re.compile(r'<g aria-label="([^"]*)"[^>]*>\s*(?:<title>[^<]*</title>)?\s*<path d="([^"]+)"\s*transform="([^"]+)"')

# every visible figure of the scaled plan (copy v46); each must appear in the lettering
REQUIRED = [
    'Proposed DKK30.0M', 'Objective-and-task · about 6% of base revenue*',
    '*Base case, assumed: 450 cars × 15 trips/day × DKK200',
    '7.0M / 23%', '6.0M / 20%', '5.0M / 17%', '4.6M / 15%', '2.4M / 8%', '2.0M / 7%', '1.0M / 3%',
    'DKK7.5M', 'DKK13.5M', 'DKK16.5M', 'Budget reviews · cumulative caps',
    '150,000', '2.5M', '15/car/day average', '≤DKK100', 'n=400 per wave',
    'Media CAC = (search + social) / first paid riders', '≥25,000 first paid riders', 'Media CAC ≤DKK120',
    '≥55,000 first paid riders', '≥10 trips per car per day', '≥35% 90-day repeat†', '≥100 business',
    'Focus: Copenhagen residents aged 25–44', '4 segments', '1  Focus: 25–44 · M1+', '2  All adults · M1+',
    '3  Business accounts · M4+', '4  Visitors + airport · M6+', 'Price-conscious · 57%', 'Green by habit · 41%',
    'Partner operators · Uber + Dantaxi 40–50%', 'App-booked electric taxi rides · Denmark = 1st EU market',
    'For green, fair-fare riders: 100% electric · one company runs app, car + driver',
    'Campaign: Copenhagen, meet Green SM', 'Danish first: København, mød Green SM', 'Go Green',
    'For a Green Future.', 'LAUNCH CAMPAIGN', 'Channel → KPI', 'Entry investment: about 6% of base revenue',
]
# figures of the DKK600,000 plan and dropped ideas; none may survive anywhere on the front
FORBIDDEN = ['600,000', '276,000', '108,000', '90,000', '43,195', '40,805', '1,200', '2,500', 'DKK165',
             '400 riders', '400 cap', '177,000', '265,000', '335,000', '460h', 'Når cyklen', 'DKK500',
             '3,000']


def labels(text):
    return [(c3.c2.unesc(m.group(1)), m.group(2), m.group(3)) for m in LABEL.finditer(text)]


def main():
    source, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    src = source.read_text()
    front = (out_dir / f'{STEM}.svg').read_text()
    back = (out_dir / f'{STEM}-back.svg').read_text()
    log = json.loads((out_dir / f'{STEM}-changes.json').read_text())['changes']
    with contextlib.redirect_stdout(io.StringIO()):
        base, _, _ = r3.build(src)
    checks = {}

    # model
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        sys_argv, sys.argv = sys.argv, [sys.argv[0]]
        MODEL.main()
        sys.argv = sys_argv
    model = json.loads(buf.getvalue())
    checks['model_pass'] = model['pass']

    # lettering against the v03 build
    old, new = labels(base), labels(front)
    old_c, new_c = Counter(l for l, _, _ in old), Counter(l for l, _, _ in new)
    declared_from = {c['from'] for c in log if 'from' in c}
    removed = sorted(l for l in old_c if new_c[l] < old_c[l])
    checks['removed_labels_all_declared'] = sorted(set(removed) - declared_from)
    keep = {(l, d, t) for l, d, t in old if l not in declared_from}
    checks['unchanged_lettering_byte_identical'] = len(keep - {(l, d, t) for l, d, t in new}) == 0
    checks['unchanged_lettering_count'] = len(keep)
    checks['labels_added'] = sum(max(0, new_c[l] - old_c[l]) for l in new_c)
    checks['labels_removed'] = sum(max(0, old_c[l] - new_c[l]) for l in old_c)

    text = '\n'.join(l for l, _, _ in new)
    checks['required_missing'] = [r for r in REQUIRED if r not in new_c]
    checks['forbidden_present'] = [f for f in FORBIDDEN if f in text]

    # bars: x = 925 + value / 8M × 65 units, against the model budget
    bars = re.findall(r'<path d="M925 ([\d.]+)H([\d.]+)V[\d.]+H925Z" fill="(#28bdbf|#e3bb42)"', front)
    values = [round((float(x) - 925) / 65 * 8, 2) for _, x, _ in sorted(bars, key=lambda b: float(b[0]))]
    checks['bar_values_dkk_m'] = values
    checks['bars_match_model'] = values == [v for _, v in MODEL.BUDGET]
    shares = model['budget_shares_pct']
    checks['bar_labels_match_model'] = all(f'{v:.1f}M / {shares[k]}%' in new_c for k, v in MODEL.BUDGET)
    g = MODEL.GATES
    checks['caps_match_model'] = (f"DKK{g['M4 cumulative cap']}M" in new_c and f"DKK{g['M6 cumulative cap']}M" in new_c
                                  and f"DKK{g['M7-12 scale release'] + g['contingency held']}M" in new_c)
    k = MODEL.KPI
    checks['kpis_match_model'] = (f"{k['first_paid_riders_m12']:,}" in new_c
                                  and f"≥{k['first_paid_riders_m4']:,} first paid riders" in new_c
                                  and f"≥{k['first_paid_riders_m6']:,} first paid riders" in new_c
                                  and f"≤DKK{k['media_cac_cap_m12']}" in new_c
                                  and f"Media CAC ≤DKK{k['media_cac_cap_m4_m6']}" in new_c
                                  and f"{k['paid_trips_year1'] / 1e6}M" in new_c)

    # connectors
    links = re.findall(r'<g id="link-(\d+)-(\d+)">(.*?)</g>', front, re.S)
    checks['connectors'] = [f'{a}→{b}' for a, b, _ in links]
    checks['connectors_cyan_dashed'] = all('stroke="#28bdbf"' in s and 'stroke-dasharray' in s for _, _, s in links)
    checks['connectors_count'] = len(links)

    # palette: v03 rule on the scaled front, plus the light yellow used for highlights
    allowed = c3.ALLOWED_CELL_COLOURS | {'#f7ebc6'}
    body = re.sub(r'data:image/[^"]+', '', front)
    checks['old_off_palette_colours_remaining'] = sorted(c for c in r3.COLOUR_MAP if re.search(re.escape(c), body, re.I))
    i = body.find('id="section-01-v07-candidate"')
    j = body.find('id="connected-cells-v01"')
    cells = body[i:j]
    for flagged in ('fit01-flag-', 'fit01-vinfast', 'fit01-background-vingroup', 'drawn-path'):
        cells = re.sub(rf'<(?:g|svg|path) id="{flagged}[^"]*".*?</(?:g|svg)>|<path id="{flagged}[^"]*"[^>]*/>', '', cells, flags=re.S)
    used = {c.lower() for c in re.findall(r'#[0-9a-fA-F]{6}\b', cells)}
    checks['cell_colours_outside_palette_unprotected'] = sorted(used - allowed - c3.PROTECTED)

    # front keeps external links, embedded images and the cloud
    for needle in ('href="poster-a0-layout-v02-2026-10-04-background.png"',
                   'href="poster-draft-car-background-v09-art-2026-10-04.png"'):
        checks[f'external_link_kept {needle[6:-1]}'] = front.count(needle) == base.count(needle)
    checks['cloud_global_statement'] = 'All targets and pilots are group proposals' in front
    checks['no_contribution_strip'] = 'member-contributions-strip' not in front

    # back of chart
    refs = (HERE / f'{STEM}-references.md').read_text().split('\n## Entries\n', 1)[1]
    entries = [e for e in refs.strip().split('\n\n') if e.strip()]
    starts = [e.split(' (')[0] for e in entries]
    joined = ''.join(l for l, _, _ in labels(back))
    checks['back_reference_entries'] = len(entries)
    checks['back_entries_alphabetical'] = starts == sorted(starts, key=str.lower)
    checks['back_all_entry_starts_lettered'] = all(s.split()[0] in joined for s in starts)
    checks['back_new_entries'] = all(n in refs for n in ('European Commission (2025)', 'Green SM Denmark ApS (no date a)'))

    checks['pass'] = bool(
        checks['model_pass'] and not checks['removed_labels_all_declared']
        and checks['unchanged_lettering_byte_identical'] and not checks['required_missing']
        and not checks['forbidden_present'] and checks['bars_match_model'] and checks['bar_labels_match_model']
        and checks['caps_match_model'] and checks['kpis_match_model'] and checks['connectors_count'] == 10
        and checks['connectors_cyan_dashed'] and not checks['old_off_palette_colours_remaining']
        and not checks['cell_colours_outside_palette_unprotected'] and checks['back_reference_entries'] == 21
        and checks['back_entries_alphabetical'] and checks['back_all_entry_starts_lettered']
        and checks['back_new_entries'] and checks['no_contribution_strip'])
    checks['not_checked_here'] = [
        'car/harbour background PNGs are external and absent from the cloud session; previews omit them',
        'Chalkboard SE rendering of the cloud text (macOS font) — verify locally',
        'mba-presentation-style presentcheck.py on changed copy — run locally',
        'native Danish check: København, mød Green SM; Elektrisk taxa. Tjek prisen. Book i appen.',
        'actual-size print legibility; arrow placement over the background art',
    ]
    (out_dir / f'{STEM}-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=1))
    print(json.dumps(checks, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
