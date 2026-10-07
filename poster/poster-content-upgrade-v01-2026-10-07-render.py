"""Build the D-158 content-upgrade proof from poster-references-v04-2026-10-07.svg.

Front: label-level edits inside existing cells (proposal v01, Tier 1/2 and
D1-D7), identity-cloud corrections and a member-contributions strip in the
former References band. Back: the Harvard References for the back of the chart.

All lettering reuses the approved CoreText glyph outlines already in the v04
SVG (see glyph-reuse-lettering.py); cell geometry, artwork, figures outside
the listed edits and external image links are unchanged.

Usage: python3 -B poster/poster-content-upgrade-v01-2026-10-07-render.py SOURCE.svg OUT_DIR
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('glyphs', HERE / 'glyph-reuse-lettering.py')
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)

STEM = 'poster-content-upgrade-v01-2026-10-07'
INK = '#173a47'
PENDING = '#b26b00'


class Editor:
    def __init__(self, text):
        self.text = text
        self.ops = []
        self.log = []

    def replace(self, start, end, new, note):
        self.ops.append((start, end, new))
        self.log.append(note)

    def apply(self):
        out = self.text
        last = None
        for start, end, new in sorted(self.ops, key=lambda o: (o[0], o[1]), reverse=True):
            if last is not None and end > last:
                raise ValueError('overlapping edits')
            out = out[:start] + new + out[end:]
            last = start
        return out


def size_in(font, sample):
    """Size of sample relative to the font's donor size."""
    for label, k in font.members:
        if label == sample.label:
            return k
    k, spread = font.measure(sample)
    if spread > 0.03:
        raise KeyError(f'{sample.label!r} does not match this font (spread {spread:.3f})')
    return k


def build_front(src):
    S = G.load(src)
    find = lambda label, i=0: G.find(S, label, i)
    body = G.Font(S, ['*Paid campaign cohort only', 'Max DKK30 · 400 cap · 1/rider',
                      'Cost pilots separately'], any_skew=True)
    head = G.Font(S, ['5. Digital Marketing Tactics'])
    # ± assembled from the existing + and hyphen; spacing as for +
    plus, hyph = body.best('+')[0], body.best('-')[0]
    pk = body.best('+')[1]
    pw, ph = plus.w / pk, plus.h / pk
    hk = body.best('-')[1]
    body.synth('±', [('+', 0, ph * 0.22, 1, 1),
                     ('-', 0, -(hyph.y0 / hk) + plus.y0 / pk - ph * 0.02, pw / (hyph.w / hk), 1)],
               spacing_like=('+', '+'))
    ed = Editor(src)
    changes = []

    def put(sample, text, font, x=None, y=None, size=None, anchor='left', fill=None, keep=False):
        size = size_in(font, sample) if size is None else size
        d, w = font.compose(text, size)
        if x is None:
            x = sample.left if anchor == 'left' else (sample.left + sample.right) / 2
        left = x - w / 2 if anchor == 'centre' else x
        y = sample.ty if y is None else y
        g = G.group(text, d, left, y, fill or sample.fill)
        if keep:
            ed.replace(sample.match.end(), sample.match.end(), g, f'add {text!r}')
        else:
            ed.replace(sample.match.start(), sample.match.end(), g, f'{sample.label!r} -> {text!r}')
        changes.append({'from': None if keep else sample.label, 'to': text,
                        'x': round(left, 2), 'y': round(y, 2), 'width': round(w, 2)})
        return left, w

    def append(sample, suffix, font):
        size = size_in(font, sample)
        last = sample.glyphs[-1].char
        first = suffix.lstrip()[0]
        gap = (font.R[last] + font.space + font.L[first]) * size
        d, w = font.compose(suffix.strip(), size)
        x = sample.right + gap
        ed.replace(sample.match.end(), sample.match.end(),
                   G.group(suffix.strip(), d, x, sample.ty, sample.fill),
                   f'append {suffix!r} to {sample.label!r}')
        changes.append({'append_to': sample.label, 'to': suffix.strip(),
                        'x': round(x, 2), 'y': sample.ty, 'right': round(x + w, 2)})

    def keep_glyphs(sample, start, stop, note, shift_to_left=True):
        d = G.subset(sample, start, stop)
        dx = 0.0
        if shift_to_left:
            dx = sample.glyphs[0].x0 - sample.glyphs[start].x0
        kept = ''.join(u for u in sample.units if u != ' ')
        label = note
        ed.replace(sample.match.start(), sample.match.end(),
                   G.group(label, d, sample.tx + dx, sample.ty, sample.fill),
                   f'{sample.label!r} -> {label!r}')
        changes.append({'from': sample.label, 'to': label, 'method': 'original glyphs kept'})

    def delete(sample):
        ed.replace(sample.match.start(), sample.match.end(), '', f'delete {sample.label!r}')
        changes.append({'from': sample.label, 'to': None})

    # Section 1 — U-05 scale line (E-020)
    s = find('Owned fleet · Employed drivers')
    put(s, 'Owned fleet (590 registered) · Employed drivers', body, anchor='centre')

    # Section 2 — U-08 prioritisation (D-032)
    s = find('Recurring local trips')
    k2 = size_in(body, s)
    fit = min(0.84, 92.0 / body.width('Later: visitors · business accounts', k2))
    put(s, 'Later: visitors · business accounts', body, x=799.0, y=339.2,
        size=k2 * fit, keep=True)

    # Section 3 — U-06 divestment (E-025) and U-07 fare parity (E-213, E-015)
    s = find('Drivr · Dantaxi')
    dan = s.glyphs[[u for u in s.units if u != ' '].index('D', 1)]
    put(s, '(part to be sold)', body, x=s.tx + dan.x0, y=338.6,
        size=size_in(body, s) * 0.82, keep=True)
    s = find('Shared: App booking · Electric options')
    put(s, 'Shared: App booking · Electric options · Similar fares (Dantaxi/Drivr)', body,
        anchor='centre')

    # Section 5
    s = find('Capital Region · n=79')
    append(s, ' · ±11 pp', body)
    s = find('Omni Channel · Search / SEO / Social')
    append(s, ' / Content', head)
    s = find('10% vs 20%')
    put(s, 'DKK15 vs DKK30', head, x=s.left - 1.0, size=size_in(head, s) * 0.86)
    s = find('Max DKK30 · 400 cap · 1/rider')
    put(s, 'Post-launch · 400 riders · 1 each', body)
    # D7 — repeated proposal tags (one global statement now sits in the cloud)
    delete(find('*Proposed'))
    s = find('4Ps*')
    keep_glyphs(s, 0, 3, '4Ps')
    s = find('DATA*')
    keep_glyphs(s, 0, 4, 'DATA')
    s = find('Opt-in · proposed')
    keep_glyphs(s, 0, 6, 'Opt-in')
    s = find('30-day paid*')
    keep_glyphs(s, 0, len(s.glyphs) - 1, '30-day paid')

    # Section 5 — U-10 Danish example on the Copenhagen page mock
    page_old = re.search(
        r'<path d="M356 503L365 495\.5L374 503V514H356Z"[^>]*/>\s*'
        r'<path d="M374 501L385\.5 496L397 501V514H374Z"[^>]*/>\s*'
        r'<path d="M397 503L407 495\.5L417 503V514H397Z"[^>]*/>\s*'
        r'<path d="M356 503H374 M374 501H397 M397 503H417"[^>]*/>\s*'
        r'<rect x="357" y="517\.5" width="58" height="4" rx="1\.5" fill="#ffffff"/>\s*'
        r'<rect x="357" y="523\.5" width="58" height="3\.5" rx="1\.5" fill="#28bdbf"/>', src)
    assert page_old, 'landing-page mock not found'
    ref_head = find('Copenhagen page')
    ref_body = find('Same fares / offers / help')
    hs = size_in(head, ref_head) * 0.95
    bs = size_in(body, ref_body) * 0.98
    lines = []
    d, w = head.compose('Elektrisk taxa', hs)
    lines.append(G.group('Elektrisk taxa', d, 386 - w / 2, 505.2, INK))
    for text, y in (('Tjek prisen.', 515.0), ('Book i appen.', 524.6)):
        d, w = body.compose(text, bs)
        lines.append(G.group(text, d, 386 - w / 2, y, INK))
    d, w = body.compose('bestil taxa', bs * 0.62)
    search = (f'<rect x="353.5" y="487.9" width="{w + 8.5:.2f}" height="3.9" rx="1.6" '
              f'fill="#ffffff" stroke="none"/>'
              f'<circle cx="356.4" cy="489.85" r="1.05" fill="none" stroke="#173a47" stroke-width="0.4"/>'
              + G.group('bestil taxa', d, 358.6, 491.05, INK))
    ed.replace(page_old.start(), page_old.end(),
               '<g id="section-05-danish-example-ad-v01" stroke="none">' + search + ''.join(lines) + '</g>',
               'page mock: houses/bars -> Danish search example')
    changes.append({'from': 'Copenhagen page mock (houses + two text bars)',
                    'to': 'search field "bestil taxa"; Elektrisk taxa / Tjek prisen. / Book i appen.'})

    # Section 6 — D7 and U-16 funnel diagnostics
    delete(find('Sales strategy • proposed'))
    append(find('Search/social → leads'), ' · CTR, CPC', body)
    append(find('Fare check → prospect'), ' · app installs', body)
    append(find('App booking → completed trip'), ' · conversion', body)

    # Section 7 — U-14a calendar (D3), U-14b exclusion, U-18 unit check (D1)
    put(find('12 months · excluding VAT'), 'Nov 2026–Oct 2027 · excluding VAT', body)
    put(find('Outside budget: cars, drivers,'), 'Outside budget: app build, cars,', body)
    put(find('charging / frontline support'), 'drivers, charging / frontline support', body)
    s = find('DKK / % · bars: 0–300,000')
    put(s, 'Unit check: DKK165 CAC repaid in about 2.4 rides', body)
    put(s, 'at an assumed DKK68 contribution per ride', body, y=s.ty + 8.2, keep=True)

    # Section 8 — U-04 cohort scope, U-15 survey sample, D7
    put(find('*Paid campaign cohort only'), '*Paid-campaign riders only, not all Green SM trips', body)
    s = find('Consideration')
    put(s, 'Consideration', body, y=474.0)
    put(s, 'n=400 per wave', body, y=484.0, keep=True)
    s = find('TRACKING PROPOSED')
    keep_glyphs(s, 0, 8, 'TRACKING')

    # Section 9 — D7 header tag and U-17 neuromarketing
    s = find('PROPOSED PILOTS · Local performance untested')
    keep_glyphs(s, 8, len(s.glyphs), 'PILOTS · Local performance untested')
    s = find('DKK600,000 excludes app/platform build + vehicle/driver/frontline operations')
    put(s, 'Neuro cue test: calm-ride vs fare-first ads → attention (CTR) · recall (survey)', body)

    # Identity cloud — U-01 and D7 global statement
    cloud_old = re.search(r'(<g fill="#173a47" text-anchor="middle" font-family="Chalkboard SE, Noteworthy, sans-serif">)(.*?)(</g>)', src, re.S)
    assert 'Lecturer: PhD Luu Tien Thuan' in cloud_old.group(2)
    rows = [('Green SM | Copenhagen', 11.8, ' font-weight="700"'),
            ('Market-Entry Plan', 11.8, ' font-weight="700"'),
            ('MARK1286 | Assessment 1', 10.8, ' font-weight="600"'),
            ('001545326 - Nguyen Phi Giao', 10.8, ''),
            ('001545344 - Le Quoc Khoi', 10.8, ''),
            ('001545423 - Nguyen Ho Khanh Vy', 10.8, ''),
            ('Lecturer: Dr Luu Tien Thuan', 10.8, ''),
            ('All targets and pilots are group proposals', 8.6, ' font-style="italic"')]
    texts = ''.join(f'\n    <text x="1387" y="{38 + 12.5 * i:.1f}" font-size="{fs}"{extra}>{t}</text>'
                    for i, (t, fs, extra) in enumerate(rows))
    ed.replace(cloud_old.start(2), cloud_old.end(2), texts + '\n  ', 'cloud: Dr; global proposal line')
    changes.append({'from': 'Lecturer: PhD Luu Tien Thuan', 'to': 'Lecturer: Dr Luu Tien Thuan'})
    changes.append({'from': None, 'to': 'All targets and pilots are group proposals (cloud)'})

    # Footer — D5 References move to the back; contributions strip (D6 pending)
    i = src.find('<g id="harvard-references-footer-v01"')
    depth, j = 0, i
    for m in re.finditer(r'<g\b|</g>', src[i:]):
        depth += 1 if m.group() != '</g>' else -1
        if depth == 0:
            j = i + m.end()
            break
    refhead = find('References')
    strip = ['<g id="member-contributions-strip-v01" aria-label="Member contributions — awaiting group confirmation">',
             '<rect x="0" y="1020" width="1672" height="162.634146" fill="#ffffff"/>']
    hsz = size_in(head, refhead)
    d, w = head.compose('Member contributions', hsz)
    strip.append(G.group('Member contributions', d, 40, 1082, INK))
    members = [('Nguyen Phi Giao', '001545326'), ('Le Quoc Khoi', '001545344'),
               ('Nguyen Ho Khanh Vy', '001545423')]
    nsz = size_in(body, find('Distinct first paid')) * 1.9
    for n, (name, sid) in enumerate(members):
        x = 330 + n * 450
        strip.append(f'<rect x="{x - 16}" y="1046" width="424" height="86" rx="12" fill="#ffffff" '
                     f'stroke="#28bdbf" stroke-width="1.6" stroke-dasharray="5 4"/>')
        d, w = body.compose(f'{name} · {sid}', nsz)
        strip.append(G.group(f'{name} · {sid}', d, x, 1078, INK))
        d, w = body.compose('Contribution: to be confirmed by the group', nsz * 0.8)
        strip.append(G.group('Contribution: to be confirmed by the group', d, x, 1110, PENDING))
    d, w = body.compose('References: back of chart', nsz * 0.8)
    strip.append(G.group('References: back of chart', d, 40, 1110, INK))
    strip.append('</g>')
    ed.replace(i, j, ''.join(strip), 'footer: References -> contributions strip')
    changes.append({'from': 'Harvard References footer (17 sources)',
                    'to': 'Member contributions strip with three pending slots; References on back'})

    out = ed.apply()
    out = re.sub(r'<title>[^<]*</title>', '<title>Copenhagen meet Green SM — content upgrade proof v01</title>', out, count=1)
    out = re.sub(r'<desc>[^<]*</desc>', '<desc>A0 landscape marketing-plan poster, D-158 content-upgrade proof. Label-level edits inside the ten existing cells; identity cloud uses Dr and one global proposal statement; the former References band holds a member-contributions strip awaiting group input. References move to the back of the chart. Lettering reuses the approved glyph outlines. Awaits student review.</desc>', out, count=1)
    return out, changes, body, head


def build_back(src, body, head, refs):
    W, H = 1672, 1182.634146
    S = G.load(src)
    hsz = size_in(head, G.find(S, 'References')) * 2.0
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1189mm" height="841mm" viewBox="0 0 {W} {H:.6f}">',
             '<title>Green SM Copenhagen poster — References (back of chart)</title>',
             '<desc>Back of the A0 chart: Harvard References for the content-upgrade proof v01, in the approved glyph lettering.</desc>',
             f'<rect width="{W}" height="{H:.6f}" fill="#ffffff"/>']
    d, w = head.compose('References', hsz)
    parts.append(G.group('References', d, 60, 92, INK))
    d, w2 = body.compose('Green SM · Copenhagen Market-Entry Plan · MARK1286 Assessment 1 · back of chart', 2.2)
    parts.append(G.group('back-of-chart identification', d, 60 + w + 30, 92, '#4a6670'))
    cols, gutter, top, bottom, left = 3, 46, 140, H - 50, 60
    colw = (W - 2 * left - (cols - 1) * gutter) / cols

    def layout(sz):
        lead = sz * 7.4
        placed, col, y = [], 0, top
        for entry in refs:
            lines = wrap(entry, sz, colw)
            hgt = len(lines) * lead + lead * 0.55
            if y + hgt > bottom and y > top:
                col, y = col + 1, top
            placed.append((col, y, lines))
            y += hgt
        return placed, col, lead

    sz = 4.2
    while True:
        placed, col, lead = layout(sz)
        if col < cols:
            break
        sz -= 0.05
    for col, y, lines in placed:
        x0 = left + col * (colw + gutter)
        for li, line in enumerate(lines):
            x = x0 + (0 if li == 0 else 14)
            for text, italic, xoff in line:
                d, w = body.compose(text, sz)
                parts.append(G.group(text, d, x + xoff, y + li * lead, INK, skew=-10 if italic else 0))
    parts.append('</svg>')
    return '\n'.join(parts), sz


def runs_of(entry):
    """Split '*italic*' markup into (text, italic) runs."""
    out = []
    for k, chunk in enumerate(entry.replace('\\*', '\x00').split('*')):
        if chunk:
            out.append((chunk.replace('\x00', '*'), k % 2 == 1))
    return out


def wrap(entry, sz, width, font=None):
    font = font or wrap.font
    words = []
    for text, italic in runs_of(entry):
        for tok in re.findall(r'\S+|\s+', text):
            words.append((tok, italic))
    space = font.space * sz + font.base * sz
    lines, cur, x = [], [], 0.0
    limit = width

    def emit():
        nonlocal cur, x
        lines.append(cur)
        cur, x = [], 0.0

    pending_space = False
    for tok, italic in words:
        if tok.isspace():
            pending_space = bool(cur)
            continue
        pieces = [tok]
        w = font.width(tok, sz)
        avail = (limit if not lines else limit - 14)
        if w > avail:
            pieces = re.findall(r'[^/\-_?&=.]*[/\-_?&=.]?', tok)
            pieces = [p for p in pieces if p]
        for pi, piece in enumerate(pieces):
            pw = font.width(piece, sz)
            gap = space if (pending_space and cur) else (font.base * sz if cur and pi > 0 else 0)
            avail = (limit if not lines else limit - 14)
            if cur and x + gap + pw > avail:
                emit()
                gap = 0
            cur.append((piece, italic, x + gap))
            x += gap + pw
            pending_space = False
            if pi == 0 and len(pieces) > 1:
                pass
    if cur:
        emit()
    return lines


def main():
    source, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    src = source.read_text()
    front, changes, body, head = build_front(src)
    (out_dir / f'{STEM}.svg').write_text(front)
    refs = (HERE / f'{STEM}-references.md').read_text().split('\n## Entries\n', 1)[1]
    entries = [e.strip() for e in refs.strip().split('\n\n') if e.strip()]
    # æ for the KFST 2026a title, assembled from the existing a and e
    a, ka = body.best('a')
    body.synth('æ', [('a', 0, 0, 1, 1), ('e', a.w / ka * 0.62, 0, 1, 1)], spacing_like=('a', 'e'))
    wrap.font = body
    back, sz = build_back(src, body, head, entries)
    (out_dir / f'{STEM}-back.svg').write_text(back)
    report = {'source': source.name, 'front': f'{STEM}.svg', 'back': f'{STEM}-back.svg',
              'reference_entries': len(entries), 'back_lettering_size': round(sz, 3),
              'synthesised_glyphs': ['± (from + and -)', 'æ (from a and e)'],
              'changes': changes}
    (out_dir / f'{STEM}-changes.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in report.items() if k != 'changes'}, ensure_ascii=False))
    print(len(changes), 'changes')


if __name__ == '__main__':
    main()
