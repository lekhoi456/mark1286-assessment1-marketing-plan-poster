"""Render exact local handwriting-font glyphs into a controlled SVG layout."""

from html import escape
from pathlib import Path
import base64

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen


class HandLettering:
    def __init__(self, path, index=0):
        self.path = path
        self.font = TTFont(path, fontNumber=index)
        self.glyphs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.units = self.font['head'].unitsPerEm
        self.metrics = self.font['hmtx'].metrics

    def width(self, text, size):
        return sum(self.metrics[self.cmap[ord(char)]][0] for char in text) * size / self.units

    def wrap(self, text, size, width):
        lines, current = [], ''
        for word in text.split():
            candidate = (current + ' ' + word).strip()
            if current and self.width(candidate, size) > width:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        return lines

    def svg(self, text, x, baseline, size, fill='#173a47', angle=0):
        scale = size / self.units
        paths, cursor = [], x
        for char in text:
            glyph_name = self.cmap[ord(char)]
            pen = SVGPathPen(self.glyphs)
            self.glyphs[glyph_name].draw(pen)
            commands = pen.getCommands()
            if commands:
                paths.append(
                    f'<path d="{commands}" transform="matrix({scale} 0 0 {-scale} {cursor} {baseline})"/>'
                )
            cursor += self.metrics[glyph_name][0] * scale
        rotation = f' transform="rotate({angle} {x} {baseline})"' if angle else ''
        return f'<g fill="{fill}" aria-label="{escape(text, quote=True)}"{rotation}><title>{escape(text)}</title>{"".join(paths)}</g>'


def image_uri(path):
    return 'data:image/png;base64,' + base64.b64encode(Path(path).read_bytes()).decode('ascii')


def sprite(uri, crop, target):
    cx, cy, cw, ch = crop
    x, y, w, h = target
    clip_id = f'crop-{cx}-{cy}-{cw}-{ch}-{x}-{y}'
    return (
        f'<svg x="{x}" y="{y}" width="{w}" height="{h}" '
        f'viewBox="{cx} {cy} {cw} {ch}" overflow="hidden" preserveAspectRatio="xMidYMid meet">'
        f'<defs><clipPath id="{clip_id}" clipPathUnits="userSpaceOnUse">'
        f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}"/></clipPath></defs>'
        f'<g clip-path="url(#{clip_id})"><image href="{uri}" x="0" y="0" width="1536" height="1024"/></g></svg>'
    )
