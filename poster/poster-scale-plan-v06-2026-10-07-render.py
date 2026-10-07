"""Build proof v06 (D-165): proof v05 without the cloud line "All targets and pilots are group proposals".

The remaining seven cloud lines move down 2 units to stay centred in the cloud.
Every other byte of the v05 front is unchanged apart from the SVG title and description.
The back of chart is unchanged (poster-scale-plan-v04-2026-10-07-back.*).

Usage: python3 -B poster/poster-scale-plan-v06-2026-10-07-render.py SOURCE.svg OUT_DIR
"""
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEM = 'poster-scale-plan-v06-2026-10-07'
LINE = '\n    <text x="1387" y="125.5" font-size="8.6" font-style="italic">All targets and pilots are group proposals</text>'
SHIFT = 2.0


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def drop_cloud_line(v05_front):
    assert v05_front.count(LINE) == 1
    i = v05_front.find('<g fill="#173a47" text-anchor="middle" font-family="Chalkboard SE')
    j = v05_front.find('</g>', i)
    block = v05_front[i:j].replace(LINE, '')
    block = re.sub(r'(<text x="1387" y=")([\d.]+)"', lambda m: f'{m.group(1)}{float(m.group(2)) + SHIFT:.1f}"', block)
    out = v05_front[:i] + block + v05_front[j:]
    out = out.replace('scaled plan proof v05</title>', 'scaled plan proof v06</title>', 1)
    return out.replace('D-164 proof v05: proof v04', 'D-165 proof v06: proof v04', 1).replace(
        'without the connecting arrows.', 'without the connecting arrows or the cloud line on group proposals.', 1)


def main():
    source, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    v04 = load('v04', 'poster-scale-plan-v04-2026-10-07-render.py')
    r5 = load('r5', 'poster-scale-plan-v05-2026-10-07-render.py')
    front, _ = v04.build(source.read_text())
    (out_dir / f'{STEM}.svg').write_text(drop_cloud_line(r5.strip_connectors(front)))
    print('written', out_dir / f'{STEM}.svg')


if __name__ == '__main__':
    main()
