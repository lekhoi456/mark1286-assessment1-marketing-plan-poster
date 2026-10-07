#!/usr/bin/env python3
"""Render the editable Section 5 v06 SVG to its PNG preview."""
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SVG = HERE / "05-v06-candidate-2026-10-04.svg"
PNG = HERE / "05-v06-candidate-2026-10-04.png"


def main() -> None:
    root = ET.parse(SVG).getroot()
    if root.attrib.get("width") != "1800" or root.attrib.get("height") != "1400":
        raise SystemExit("Unexpected canvas size; expected 1800 × 1400")
    subprocess.run(["rsvg-convert", "-o", str(PNG), str(SVG)], check=True)
    print(f"Rendered {PNG.name} from {SVG.name}")


if __name__ == "__main__":
    main()
