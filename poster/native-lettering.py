"""Small CoreText bridge for exact, dependency-free handwritten SVG lettering."""

from html import escape
from pathlib import Path
import json
import subprocess


class GlyphServer:
    def __init__(self):
        script = Path(__file__).resolve().parent / "08-v02-glyphs.swift"
        self.process = subprocess.Popen(
            ["swift", str(script)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, bufsize=1,
        )

    def outline(self, value, font, size):
        request = {"text": value, "font": font, "size": float(size)}
        self.process.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
        self.process.stdin.flush()
        response = self.process.stdout.readline()
        if not response:
            error = self.process.stderr.read()
            raise RuntimeError(f"CoreText glyph process stopped: {error}")
        result = json.loads(response)
        if "error" in result:
            raise RuntimeError(result["error"])
        if result["resolved_font"] != font:
            raise RuntimeError(f"Requested {font}, CoreText resolved {result['resolved_font']}")
        if not result["path"]:
            raise RuntimeError(f"No glyph outline produced for {value!r}")
        return result

    def width(self, value, font, size):
        return self.outline(value, font, size)["width"]

    def svg(self, value, x, baseline, size, font, fill="#19364d", angle=0):
        result = self.outline(value, font, size)
        rotation = f' transform="rotate({angle} {x} {baseline})"' if angle else ""
        return (
            f'<g aria-label="{escape(value, quote=True)}" fill="{fill}"{rotation}>'
            f'<title>{escape(value)}</title><path d="{result["path"]}" '
            f'transform="translate({x:.3f} {baseline:.3f}) scale(1 -1)"/></g>'
        )

    def close(self):
        if self.process.poll() is None:
            self.process.stdin.close()
            self.process.wait(timeout=10)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
