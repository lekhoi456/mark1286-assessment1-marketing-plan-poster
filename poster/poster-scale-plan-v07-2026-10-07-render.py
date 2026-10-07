"""Build the final front, proof v07 (D-166).

Proof v06 (v04 without connecting arrows or the cloud line on group
proposals) with the D-166 number corrections from scale-plan model v02:
- the 2.5M trips target is the M12 annualised run-rate, not a year-one total;
- the 6% budget logic refers to run-rate revenue;
- the M6 floor counts paid trips a day;
- DKK1.0M moves from Social to Team & creative (bars and labels follow the model).
The back of chart is unchanged (poster-scale-plan-v04-2026-10-07-back.*).

Usage: python3 -B poster/poster-scale-plan-v07-2026-10-07-render.py SOURCE.svg OUT_DIR
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEM = 'poster-scale-plan-v07-2026-10-07'
TEXT = {  # v04 display string -> final display string
    'Objective-and-task · about 6% of base revenue*': 'Objective-and-task · 6% of run-rate revenue*',
    '*Base case, assumed: 450 cars × 15 trips/day × DKK200': '*Run-rate, assumed: 450 cars × 15 trips/day × DKK200',
    'Paid trips': 'Paid trips a year',
    '15/car/day average': 'run-rate by M12',
    '≥10 trips per car per day': '≥2,500 paid trips a day',
    'Entry investment: about 6% of base revenue': 'Entry investment: 6% of run-rate revenue',
}
TITLE = 'Copenhagen meet Green SM — final poster v07'
DESC = ('A0 landscape marketing-plan poster, final version v07 (D-166): proposed DKK30M gated market-entry plan, '
        'four segments with 25–44 as focus, campaign Copenhagen, meet Green SM with Go Green / For a Green Future. '
        'Figures come from scale-plan model v02. Lettering reuses the approved glyph outlines.')


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(src):
    v04 = load('v04', 'poster-scale-plan-v04-2026-10-07-render.py')
    r5 = load('r5', 'poster-scale-plan-v05-2026-10-07-render.py')
    r6 = load('r6', 'poster-scale-plan-v06-2026-10-07-render.py')
    v04.MODEL = load('model2', 'scale-plan-v02-2026-10-07-model.py')
    used = set()

    class FinalBuilder(v04.Builder):
        def rep(self, label, text, *a, **k):
            used.add(text) if text in TEXT else None
            return super().rep(label, TEXT.get(text, text), *a, **k)

        def add_after(self, anchor_label, text, *a, **k):
            used.add(text) if text in TEXT else None
            return super().add_after(anchor_label, TEXT.get(text, text), *a, **k)

    v04.Builder = FinalBuilder
    front, log = v04.build(src)
    assert used == set(TEXT), set(TEXT) - used
    out = r6.drop_cloud_line(r5.strip_connectors(front))
    out = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', out, count=1)
    out = re.sub(r'<desc>[^<]*</desc>', f'<desc>{DESC}</desc>', out, count=1)
    return out, log


def main():
    source, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    out, log = build(source.read_text())
    (out_dir / f'{STEM}.svg').write_text(out)
    (out_dir / f'{STEM}-changes.json').write_text(json.dumps(
        {'source': source.name, 'base': 'proof v04 build without connectors (v05) or the cloud line (v06)',
         'model': 'scale-plan-v02-2026-10-07-model.py', 'copy': '10-sections-scale-copy-v47-2026-10-07.md',
         'text_corrections': TEXT, 'changes': log}, ensure_ascii=False, indent=1))
    print('written', out_dir / f'{STEM}.svg', len(log), 'changes')


if __name__ == '__main__':
    main()
