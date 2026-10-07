"""Fill the A0 scene while preserving the native car cells and cloud lettering."""

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


def node(tag, attrs=None, parent=None):
    result = ET.Element(f"{{{SVG}}}{tag}", attrs or {})
    if parent is not None:
        parent.append(result)
    return result


plan = json.loads((HERE / "poster-car-cells-v01-2026-10-04.json").read_text())
base = ET.parse(HERE / "poster-draft-car-background-v09-2026-10-04.svg").getroot()
defs = base.find(f"{{{SVG}}}defs")
vehicle = node("clipPath", {"id": "preserved-vehicle-silhouette"}, defs)
node("path", {"d": (
    "M17 730 L25 714 L21 658 L30 617 L47 536 L47 516 "
    "Q111 449 204 416 L391 254 Q474 199 612 183 "
    "L671 167 Q860 158 1027 158 L1041 174 L1294 177 "
    "Q1332 156 1395 153 L1398 156 L1374 190 "
    "L1539 229 L1556 235 L1558 244 L1534 286 "
    "L1598 409 L1617 431 L1631 572 L1647 648 "
    "L1654 658 L1650 725 L1640 776 L1581 810 "
    "Q1564 860 1500 881 Q1432 904 1365 877 "
    "Q1287 861 1250 815 L386 816 Q349 870 286 887 "
    "Q219 903 150 878 Q92 860 73 818 L25 773 Z"
)}, vehicle)

# Only the car from the original full-scene raster is restored over the new sky/quay.
base_image = base.find(f"{{{SVG}}}image")
base_image.set("clip-path", "url(#preserved-vehicle-silhouette)")
for child in list(base):
    if child.tag == f"{{{SVG}}}path" and child.get("d", "").startswith("M0 0 H428"):
        base.remove(child)

height = plan["a0_viewbox"][1]
page = node("svg", {
    "width": "1189mm", "height": "841mm",
    "viewBox": f"0 0 1672 {height:.6f}",
})
node("title", parent=page).text = "Step 1 — A0 edge-to-edge Copenhagen background v02"
node("desc", parent=page).text = (
    "The sky and quay fill the A0 page. Vehicle scale, ten cell paths, "
    "cloud identities and flag layers retain their preceding coordinates. "
    "Human review is pending; no section content is assembled."
)
node("rect", {"width": "1672", "height": str(height), "fill": "#eefafa"}, page)
asset = "poster-a0-layout-v02-2026-10-04-background.png"
node("image", {
    "id": "full-page-copenhagen-background", "x": "0", "y": "0",
    "width": "1672", "height": f"{height:.6f}",
    "preserveAspectRatio": "none", "href": asset, f"{{{XLINK}}}href": asset,
}, page)
placed = node("g", {
    "id": "proportional-car-placement",
    "transform": f"translate(0 {plan['a0_art_y']:.6f})",
}, page)
for child in base:
    placed.append(copy.deepcopy(child))

stem = "poster-a0-layout-v02-2026-10-04"
target = HERE / f"{stem}.svg"
ET.ElementTree(page).write(target, encoding="unicode", xml_declaration=False)
for ext, args in [("png", ["-w", "1672"]), ("pdf", ["-f", "pdf"])]:
    subprocess.run(["/opt/homebrew/bin/rsvg-convert", *args,
                    "-o", str(HERE / f"{stem}.{ext}"), str(target)], check=True)

plan.update({
    "version": 2, "status": "Step 1 full-page background revision awaiting human review",
    "a0_svg": target.name, "a0_pdf": f"{stem}.pdf", "a0_background": asset,
    "cell_geometry_change": False,
})
(HERE / "poster-car-cells-v02-2026-10-04.json").write_text(
    json.dumps(plan, indent=2) + "\n"
)
print("Rendered full-page A0 v02; preserved native cells, lettering and vehicle scale.")
