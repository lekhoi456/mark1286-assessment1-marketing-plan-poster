"""Build proof v05 (D-164): proof v04 without the connecting arrows.

Builds proof v04 and removes its connected-cells group; every other byte
of the front stays as in v04 apart from the SVG title and description.
The back of chart is unchanged (poster-scale-plan-v04-2026-10-07-back.*).

Usage: python3 -B poster/poster-scale-plan-v05-2026-10-07-render.py SOURCE.svg OUT_DIR
"""
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEM = 'poster-scale-plan-v05-2026-10-07'
TITLE = 'Copenhagen meet Green SM — scaled plan proof v05'
DESC = ('A0 landscape marketing-plan poster, D-164 proof v05: proof v04 (scaled DKK30M gated market-entry plan, '
        'four segments with 25–44 as focus, campaign Copenhagen, meet Green SM with Go Green / For a Green Future.) '
        'without the connecting arrows. Lettering reuses the approved glyph outlines. Awaits student review.')


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def strip_connectors(v04_front):
    r3 = load('r3', 'poster-content-upgrade-v03-2026-10-07-render.py')
    i, j = r3.group_span(v04_front, 'connected-cells-v01')
    out = v04_front[:i] + v04_front[j:]
    out = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', out, count=1)
    return re.sub(r'<desc>[^<]*</desc>', f'<desc>{DESC}</desc>', out, count=1)


def main():
    source, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    v04 = load('v04', 'poster-scale-plan-v04-2026-10-07-render.py')
    front, _ = v04.build(source.read_text())
    (out_dir / f'{STEM}.svg').write_text(strip_connectors(front))
    print('written', out_dir / f'{STEM}.svg')


if __name__ == '__main__':
    main()
