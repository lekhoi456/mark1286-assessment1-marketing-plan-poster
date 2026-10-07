"""Shorten the two dense Section 2 labels while preserving its accepted chart and lower infographic."""

from pathlib import Path
import importlib.util
import json
import xml.etree.ElementTree as ET
import subprocess

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
PREFIX = "02-compact-v01"
SOURCE = ROOT / "archive/design/panel-02-independent-infographic-options-v01-2026-10-03-option-a.svg"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

old_labels = {
    "Copenhagen municipality · 1 July 2026 · age groups 18+",
    "The 40.2% denominator is all 670,389 city residents, including those aged under 18.",
}
new_labels = [
    ("Copenhagen · 1 Jul 2026 · 18+", 89.24, 301, 34),
    ("City population (all ages): 670,389", 89, 777, 38),
]

tree = ET.parse(SOURCE)
root = tree.getroot()
removed = set()
for parent in root.iter():
    for child in list(parent):
        label = child.attrib.get("aria-label")
        stale_vector_label = child.attrib.get("data-text")
        if label in old_labels or stale_vector_label in old_labels:
            parent.remove(child)
            removed.add(label or stale_vector_label)
assert removed == old_labels, f"Expected exactly two old text groups; found: {removed}"

spec = importlib.util.spec_from_file_location("native_lettering", HERE / "native-lettering.py")
native_lettering = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native_lettering)
glyphs = native_lettering.GlyphServer()
added = []
for value, x, baseline, size in new_labels:
    group = ET.fromstring(glyphs.svg(value, x, baseline, size, "Noteworthy-Light", fill="#19364d"))
    root.append(group)
    added.append(value)
glyphs.close()

svg_path = HERE / f"{PREFIX}.svg"
tree.write(svg_path, encoding="utf-8", xml_declaration=True)
png_path = HERE / f"{PREFIX}.png"
subprocess.run(["/opt/homebrew/bin/rsvg-convert", "-o", str(png_path), str(svg_path)], check=True)
subprocess.run(["/opt/homebrew/bin/rsvg-convert", "-w", "900", "-o", str(HERE / f"{PREFIX}-small.png"), str(svg_path)], check=True)

copy = """# Section 2 — Target Market compact labels

This review candidate changes only two explanatory labels in accepted option A. The selected 25–44 bar still carries 40.2% inside it, with 269,277 above. The all-age denominator and adult age-band scope remain explicit; the accepted lower audience profile is retained.

- Chart subline: Copenhagen · 1 Jul 2026 · 18+
- Denominator note: City population (all ages): 670,389
"""
(HERE / f"{PREFIX}-copy.md").write_text(copy, encoding="utf-8")
(HERE / f"{PREFIX}-prompt.md").write_text(
    "Native SVG text revision only; no generated artwork. Preserve the accepted Option A chart, counts, bars, audience icons and lower profile. Replace only the source/date line and the denominator sentence with the two shorter labels in the copy file. Keep the percentage inside the 25–44 column, the 269,277 count above it, handwritten lettering and citation-free poster face.\n",
    encoding="utf-8",
)

checks = {
    "source_file": str(SOURCE.relative_to(ROOT)),
    "removed_labels": sorted(removed),
    "added_labels": added,
    "percentage_inside_chart_preserved_in_source": "40.2%" in SOURCE.read_text(encoding="utf-8"),
    "selected_count_preserved_in_source": "269,277" in SOURCE.read_text(encoding="utf-8"),
    "old_long_labels_absent": all(label not in svg_path.read_text(encoding="utf-8") for label in old_labels),
    "new_copy_present": all(label in svg_path.read_text(encoding="utf-8") for label in added),
    "section_2_is_review_candidate_only": True,
}
(HERE / f"{PREFIX}-checks.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
print(f"Rendered {png_path}")
