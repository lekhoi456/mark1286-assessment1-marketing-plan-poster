"""Explicit local handwriting glyphs with a native-text editing companion."""
from html import escape
from fontTools.ttLib import TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

FILES = {
    'heading': ('/System/Library/Fonts/MarkerFelt.ttc', 0, 'Marker Felt', 400),
    'body': ('/System/Library/Fonts/Noteworthy.ttc', 0, 'Noteworthy', 400),
    'strong': ('/System/Library/Fonts/Noteworthy.ttc', 1, 'Noteworthy', 700),
}


class Lettering:
    def __init__(self, colour):
        self.colour = colour
        self.fonts = {k: TTCollection(v[0]).fonts[v[1]] for k, v in FILES.items()}
        self.objects, self.portable, self.native = [], [], []

    def width(self, text, size, kind):
        font = self.fonts[kind]
        cmap, metrics = font.getBestCmap(), font['hmtx'].metrics
        assert all(ord(c) in cmap for c in text), f'Unexpected font fallback: {text}'
        return sum(metrics[cmap[ord(c)]][0] for c in text) * size / font['head'].unitsPerEm

    def wrap(self, text, size, kind, maximum):
        result, line = [], ''
        for word in text.split():
            trial = (line + ' ' + word).strip()
            if line and self.width(trial, size, kind) > maximum:
                result.append(line)
                line = word
            else:
                line = trial
        return result + [line]

    def text(self, text, x, y, size, kind='body', maximum=None, role='display', centre=False):
        lines = self.wrap(text, size, kind, maximum) if maximum else [text]
        ident = f's9-text-{len(self.objects):02d}'
        font = self.fonts[kind]
        glyphs, cmap, metrics = font.getGlyphSet(), font.getBestCmap(), font['hmtx'].metrics
        scale, boxes, paths, native = size / font['head'].unitsPerEm, [], [], []
        for row, line in enumerate(lines):
            left = x - self.width(line, size, kind) / 2 if centre else x
            baseline, advance, bounds = y + row * size * 1.28, 0, []
            for char in line:
                name = cmap[ord(char)]
                pen = SVGPathPen(glyphs)
                glyphs[name].draw(pen)
                px = left + advance * scale
                if pen.getCommands():
                    paths.append(f'<path d="{pen.getCommands()}" transform="translate({px:.5f} {baseline:.5f}) scale({scale:.9f} {-scale:.9f})"/>')
                    bp = BoundsPen(glyphs)
                    glyphs[name].draw(bp)
                    a, b, c, d = bp.bounds
                    bounds.append([px + a * scale, baseline - d * scale, px + c * scale, baseline - b * scale])
                advance += metrics[name][0]
            boxes.append({'text': line, 'bbox': [min(b[0] for b in bounds), min(b[1] for b in bounds), max(b[2] for b in bounds), max(b[3] for b in bounds)]})
            native.append(f'<text x="{left:.5f}" y="{baseline:.5f}" font-family="{FILES[kind][2]}" font-size="{size}" font-weight="{FILES[kind][3]}" font-kerning="none">{escape(line)}</text>')
        common = f'id="{ident}" data-text="{escape(text, quote=True)}" data-role="{role}" fill="{self.colour}"'
        self.portable.append(f'<g {common}>{"".join(paths)}</g>')
        self.native.append(f'<g {common}>{"".join(native)}</g>')
        self.objects.append({'id': ident, 'text': text, 'kind': kind, 'font_file': FILES[kind][0], 'font_collection_index': FILES[kind][1], 'font_size': size, 'role': role, 'lines': boxes})
        return y + (len(lines) - 1) * size * 1.28
