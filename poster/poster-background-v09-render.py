"""Render the revised blank car cells and proportional A0 placement proof."""

from pathlib import Path
import copy
import json
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)


def element(tag, attrs=None, parent=None):
    node = ET.Element(f"{{{SVG}}}{tag}", attrs or {})
    if parent is not None:
        parent.append(node)
    return node


def image_reference(parent, filename, **attrs):
    attrs.update({"href": filename, f"{{{XLINK}}}href": filename})
    return element("image", attrs, parent)


plan = json.loads((HERE / "poster-car-cells-v01-2026-10-04.json").read_text())
# Conservative text rectangles are starting regions. Diagrams may use curved areas.
plan["cells"][0]["safe_box"] = [416, 292, 172, 82]
plan["cells"][3]["path"] = (
    "M1286 231 Q1354 234 1401 250 Q1436 261 1456 287 "
    "L1497 367 Q1512 389 1495 390 H1293 Q1272 390 1271 370 "
    "L1264 251 Q1263 231 1286 231 Z"
)
plan["cells"][4]["safe_box"] = [292, 449, 301, 124]

base = ET.parse(HERE / "poster-draft-car-background-v08-2026-10-04.svg").getroot()
defs = base.find(f"{{{SVG}}}defs")
body = element("clipPath", {"id": "body-cleanup-boundary"}, defs)
element("path", {"d": (
    "M480 220 C708 210 1240 214 1390 243 "
    "C1460 254 1493 334 1536 390 L1544 427 Q1570 466 1543 514 "
    "L1510 582 L1500 730 L1213 758 L415 758 "
    "Q393 755 384 725 L355 637 Q343 617 310 607 "
    "Q246 569 246 501 Q243 444 280 414 L326 378 "
    "L419 271 Q447 237 480 220 Z"
)}, body)
mirror = element("clipPath", {"id": "preserved-mirror"}, defs)
element("path", {"d": (
    "M232 425 L244 407 L260 392 Q259 382 272 377 "
    "Q309 366 337 379 Q346 383 345 393 L338 430 "
    "Q333 440 309 444 Q278 448 255 440 L232 432 Z"
)}, mirror)

layer = element("g", {"id": "revised-car-cell-layer"})
image_reference(
    layer, "poster-draft-car-background-v09-art-2026-10-04.png",
    x="0", y="0", width="1672", height="941",
    **{"clip-path": "url(#body-cleanup-boundary)"},
)
for cell in plan["cells"]:
    clip = element("clipPath", {"id": f"cell-{cell['id']:02d}-clip"}, defs)
    element("path", {"d": cell["path"]}, clip)
    group = element("g", {"id": f"cell-{cell['id']:02d}"}, layer)
    title = element("title", parent=group)
    title.text = f"{cell['id']}. {cell['heading']}"
    element("path", {
        "d": cell["path"], "fill": "#fdfbef", "stroke": "#11354a",
        "stroke-width": "2.8", "stroke-linejoin": "round",
    }, group)

image_reference(
    layer, "poster-draft-car-background-v06-art-2026-10-04.png",
    x="0", y="0", width="1672", height="941",
    **{"clip-path": "url(#preserved-mirror)"},
)
# Insert before the existing controlled cloud lettering and roof-mounted flag.
base.insert(2, layer)
bg_svg = HERE / "poster-draft-car-background-v09-2026-10-04.svg"
ET.ElementTree(base).write(bg_svg, encoding="unicode", xml_declaration=False)

page_height = plan["a0_viewbox"][1]
page = element("svg", {
    "width": "1189mm", "height": "841mm",
    "viewBox": f"0 0 1672 {page_height:.6f}",
})
title = element("title", parent=page)
title.text = "Step 1 — blank revised car-cell background on an A0 landscape page"
description = element("desc", parent=page)
description.text = (
    "Student review candidate. The 16:9 artwork is placed proportionately, "
    "with extra cream page area above and below. Section content and the "
    "main title/subtitle/tagline have not been assembled."
)
element("rect", {
    "width": "1672", "height": f"{page_height:.6f}", "fill": "#fdfbef",
}, page)
placed = element("g", {
    "id": "proportional-car-placement",
    "transform": f"translate(0 {plan['a0_art_y']:.6f})",
}, page)
for child in base:
    placed.append(copy.deepcopy(child))
a0_svg = HERE / "poster-a0-layout-v01-2026-10-04.svg"
ET.ElementTree(page).write(a0_svg, encoding="unicode", xml_declaration=False)

for source, output, args in [
    (bg_svg, bg_svg.with_suffix(".png"), []),
    (a0_svg, a0_svg.with_suffix(".png"), ["-w", "1672"]),
    (a0_svg, a0_svg.with_suffix(".pdf"), ["-f", "pdf"]),
]:
    subprocess.run(["/opt/homebrew/bin/rsvg-convert", *args,
                    "-o", str(output), str(source)], check=True)

plan["background"] = bg_svg.name
plan["a0_svg"] = a0_svg.name
plan["a0_pdf"] = a0_svg.with_suffix(".pdf").name
(HERE / "poster-car-cells-v01-2026-10-04.json").write_text(
    json.dumps(plan, indent=2) + "\n"
)
print("Rendered v09 blank background and A0 placement proof; no section content added.")
