"""Compose new poster lettering from the glyph outlines already in a poster SVG.

The approved lettering was produced locally with CoreText (Noteworthy-Light,
MarkerFelt-Wide), which is unavailable outside macOS. Each lettering group in
the poster SVG is one path for a whole string, emitted glyph by glyph.
Splitting that path into subpaths and clustering consecutive subpaths that
overlap horizontally recovers one outline per character (ligatures fi/fl/ff
included). A Font gathers every string whose glyph proportions match a donor
string, normalises the sizes, and fits pair spacing as gap(a, b) = R[a] + L[b].
No outline is invented except the explicitly synthesised characters (± and æ),
which are assembled from existing glyphs.
"""
import re
from collections import defaultdict
from html import escape
from statistics import median

GROUP = re.compile(
    r'<g aria-label="([^"]*)"([^>]*)>\s*(?:<title>[^<]*</title>)?\s*'
    r'<path d="([^"]+)"\s*transform="([^"]+)"([^>]*)/>\s*</g>'
)
TOKEN = re.compile(r'[MLQCZ]|-?\d*\.?\d+(?:e-?\d+)?')
LIGS = ('ffi', 'ffl', 'ff', 'fi', 'fl')
NO_RATIO = set('.,·-–—\'"’‘:;•')


def unescape(v):
    return (v.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
             .replace('&quot;', '"').replace('&#x27;', "'").replace('&#39;', "'"))


def subpaths(d):
    toks = TOKEN.findall(d)
    out, cur, cmd, i = [], [], None, 0
    while i < len(toks):
        t = toks[i]
        if t in 'MLQCZ':
            cmd = t
            if t == 'M' and cur:
                out.append(cur)
                cur = []
            if t == 'Z':
                cur.append(('Z', []))
            i += 1
            continue
        n = {'M': 2, 'L': 2, 'Q': 4, 'C': 6}[cmd]
        cur.append((cmd, [float(x) for x in toks[i:i + n]]))
        i += n
        if cmd == 'M':
            cmd = 'L'
    if cur:
        out.append(cur)
    return out


def bbox(sp):
    xs = [v for _, vals in sp for v in vals[0::2]]
    ys = [v for _, vals in sp for v in vals[1::2]]
    return min(xs), max(xs), min(ys), max(ys)


def xform(sp, dx=0.0, dy=0.0, sx=1.0, sy=None):
    sy = sx if sy is None else sy
    return [(c, [v * sx + dx if k % 2 == 0 else v * sy + dy for k, v in enumerate(vals)])
            for c, vals in sp]


def fmt(sps):
    parts = []
    for sp in sps:
        for c, vals in sp:
            parts.append('Z' if c == 'Z' else c + ' '.join(f'{v:.3f}' for v in vals))
    return ' '.join(parts)


class Glyph:
    def __init__(self, char, sps):
        self.char = char
        self.sps = sps
        bs = [bbox(sp) for sp in sps]
        self.x0 = min(b[0] for b in bs)
        self.x1 = max(b[1] for b in bs)
        self.y0 = min(b[2] for b in bs)
        self.y1 = max(b[3] for b in bs)

    @property
    def w(self):
        return self.x1 - self.x0

    @property
    def h(self):
        return self.y1 - self.y0


def units(label, ligatures):
    out, i = [], 0
    while i < len(label):
        if label[i].isspace():
            out.append(' ')
            i += 1
            continue
        if ligatures:
            for lg in LIGS:
                if label.startswith(lg, i):
                    out.append(lg)
                    i += len(lg)
                    break
            else:
                out.append(label[i])
                i += 1
        else:
            out.append(label[i])
            i += 1
    return out


def _cluster(chars, d):
    groups = []
    for sp in subpaths(d):
        b = bbox(sp)
        if groups:
            g = groups[-1]
            ov = min(g['x1'], b[1]) - max(g['x0'], b[0])
            narrow = min(g['x1'] - g['x0'], b[1] - b[0])
            if ov > 0.25 * max(narrow, 1e-6):
                g['sps'].append(sp)
                g['x0'] = min(g['x0'], b[0])
                g['x1'] = max(g['x1'], b[1])
                continue
        groups.append({'sps': [sp], 'x0': b[0], 'x1': b[1]})
    if len(groups) != len(chars):
        return None
    return [Glyph(c, g['sps']) for c, g in zip(chars, groups)]


def cluster(label, d):
    for lig in (False, True):
        u = units(label, lig)
        res = _cluster([c for c in u if c != ' '], d)
        if res:
            return res, u
    return None, None


def parse_transform(t):
    m = re.match(r'translate\(([-\d.]+)[ ,]+([-\d.]+)\)(?: skewX\(([-\d.]+)\))? scale\(1 -1\)', t)
    return float(m.group(1)), float(m.group(2)), float(m.group(3) or 0)


class Sample:
    def __init__(self, m):
        self.match = m
        self.label = unescape(m.group(1))
        self.d = m.group(3)
        self.fill = re.search(r'fill="([^"]*)"', m.group(5)).group(1)
        self.tx, self.ty, self.skew = parse_transform(m.group(4))
        self.glyphs, self.units = cluster(self.label, self.d)
        bs = [bbox(sp) for sp in subpaths(self.d)]
        self.x0 = min(b[0] for b in bs)
        self.x1 = max(b[1] for b in bs)

    @property
    def left(self):
        return self.tx + self.x0

    @property
    def right(self):
        return self.tx + self.x1


def load(svg_text):
    return [Sample(m) for m in GROUP.finditer(svg_text)]


def find(samples, label, index=0):
    hits = [s for s in samples if s.label == label]
    if not hits:
        raise KeyError(label)
    return hits[index]


class Font:
    """Glyph set for one style, normalised to the size of the donor strings."""

    def __init__(self, samples, donors, tolerance=0.06, any_skew=False, scope=None):
        self.glyphs = defaultdict(list)
        self.pairs, self.space_gaps, self.members = [], [], []
        ref = defaultdict(list)
        for dl in donors:
            s = find(samples, dl)
            assert s.glyphs, f'donor {dl!r} did not cluster'
            for g in s.glyphs:
                ref[g.char].append(g)
        self.ref = {c: (median(g.w for g in gs), median(g.h for g in gs)) for c, gs in ref.items()}
        for s in samples:
            if not s.glyphs or (s.skew and not any_skew):
                continue
            if scope and not scope(s):
                continue
            ratios = [(g.w / self.ref[g.char][0], g.h / self.ref[g.char][1])
                      for g in s.glyphs
                      if g.char in self.ref and g.char not in NO_RATIO and g.w > 0 and g.h > 0]
            donor = s.label in donors
            if not ratios:
                continue
            flat = [r for pair in ratios for r in pair]
            k = median(flat)
            if not donor:
                if len(ratios) < 4:
                    continue
                spread = median(abs(r / k - 1) for r in flat)
                wh = median(a / b for a, b in ratios)
                if spread > tolerance or abs(wh - 1) > tolerance:
                    continue
            self.members.append((s.label, round(k, 3)))
            self._add(s, k)
        self._fit()

    def _add(self, s, k):
        idx, prev, space_before = 0, None, False
        for ch in s.units:
            if ch == ' ':
                space_before = True
                continue
            g = s.glyphs[idx]
            idx += 1
            self.glyphs[ch].append((g, k))
            if prev is not None:
                gap = (g.x0 - prev.x1) / k
                (self.space_gaps if space_before else self.pairs).append((prev.char, ch, gap))
            prev, space_before = g, False

    def _fit(self):
        base = median(p[2] for p in self.pairs) if self.pairs else 0.5
        R = defaultdict(lambda: base / 2)
        L = defaultdict(lambda: base / 2)
        for _ in range(30):
            acc = defaultdict(list)
            for a, b, g in self.pairs:
                acc[a].append(g - L[b])
            for c, v in acc.items():
                R[c] = (sum(v) + base / 2) / (len(v) + 1)
            acc = defaultdict(list)
            for a, b, g in self.pairs:
                acc[b].append(g - R[a])
            for c, v in acc.items():
                L[c] = (sum(v) + base / 2) / (len(v) + 1)
        self.R, self.L, self.base = R, L, base
        self.space = (median(g - R[a] - L[b] for a, b, g in self.space_gaps)
                      if self.space_gaps else base * 4)

    def measure(self, sample):
        """Size of an existing sample relative to the donor size, with spread."""
        r = []
        for g in sample.glyphs or []:
            if g.char in self.glyphs and g.char not in NO_RATIO and g.w > 0 and g.h > 0:
                h, k = self.best(g.char)
                r.append((g.w / (h.w / k), g.h / (h.h / k)))
        if not r:
            raise KeyError(f'no shared glyphs with {sample.label!r}')
        flat = [a for pair in r for a in pair]
        k = median(flat)
        return k, median(abs(a / k - 1) for a in flat)

    def best(self, ch):
        g, k = min(self.glyphs[ch], key=lambda t: abs(t[1] - 1))
        return g, k

    def normalised(self, ch):
        """Outline of ch at donor size with its left edge at x=0."""
        g, k = self.best(ch)
        return [xform(sp, dx=-g.x0 / k, sx=1 / k) for sp in g.sps]

    def synth(self, ch, parts, spacing_like):
        """Add ch assembled from existing glyphs: parts = [(src, dx, dy, sx, sy)]."""
        sps = []
        for src, dx, dy, sx, sy in parts:
            for sp in self.normalised(src):
                sps.append(xform(sp, dx=dx, dy=dy, sx=sx, sy=sy))
        self.glyphs[ch].append((Glyph(ch, sps), 1.0))
        self.R[ch] = self.R[spacing_like[1]]
        self.L[ch] = self.L[spacing_like[0]]

    def missing(self, text):
        toks = units(text, False)
        return sorted({c for c in toks if c != ' ' and c not in self.glyphs})

    def compose(self, text, size=1.0, tracking=0.0):
        """Return (path_d, width) with the first glyph's left edge at x=0."""
        miss = self.missing(text)
        if miss:
            raise KeyError(f'missing glyphs {miss} for {text!r}')
        toks = []
        for u in units(text, True):
            toks.extend(list(u) if len(u) > 1 and u not in self.glyphs else [u])
        sps, x, prev, pending = [], 0.0, None, False
        for ch in toks:
            if ch == ' ':
                pending = True
                continue
            g, k = self.best(ch)
            sc = size / k
            if prev is not None:
                x += (self.R[prev] + self.L[ch] + tracking + (self.space if pending else 0)) * size
            for sp in g.sps:
                sps.append(xform(sp, dx=x - g.x0 * sc, sx=sc))
            x += g.w * sc
            prev, pending = ch, False
        return fmt(sps), x

    def width(self, text, size=1.0):
        return self.compose(text, size)[1] if text.strip() else 0.0


def group(label, d, tx, ty, fill='#173a47', skew=0.0, extra=''):
    sk = f' skewX({skew:g})' if skew else ''
    return (f'<g aria-label="{escape(label, quote=True)}"{extra}><path d="{d}" '
            f'transform="translate({tx:.3f} {ty:.3f}){sk} scale(1 -1)" fill="{fill}"/></g>')


def subset(sample, start, stop):
    """Path of the sample's own glyphs[start:stop], original positions."""
    return fmt([sp for g in sample.glyphs[start:stop] for sp in g.sps])
