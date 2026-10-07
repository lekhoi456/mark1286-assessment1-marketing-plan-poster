# Section 6 v04 — exact art prompt and provenance

No external image model was used, so no model prompt exists. The artwork was drawn locally as editable SVG vectors and all lettering was placed by the layout script.

The exact local illustration brief implemented in `06-v04-render.py` was:

> Make a compact five-stage sales journey on warm cream paper, using friendly hand-drawn navy outlines with cyan and yellow marker accents. Draw a simple Copenhagen street/building scene, a first-ride voucher, a taxi with app and support cues, a feedback bubble with a star, and a phone beside a limited monthly bundle card. Connect five equal cards from left to right with small arrows and return the final card to app booking with one curved loop. Use no generated or decorative lettering inside the icons. Keep all visible copy as controlled native SVG text, separate from the drawings. Use the supplied Green SM hand-drawn logo unchanged.

The implementation follows this brief with local SVG paths, circles and shapes. The only raster content is `shared-logo.png`, embedded byte-for-byte as a PNG data URI. SHA-256: `36a99749e3cc9585573fedda5fb1dbcf6a76483872cadc2d0f6651ec95430db9`.

The SVG is self-contained, 1800 × 1260, and keeps the logo, all copy and all illustrations editable or embedded. No citations or evidence IDs appear on the candidate face. Small-scale screen inspection does not establish A0 print readability or whole-poster fit.
