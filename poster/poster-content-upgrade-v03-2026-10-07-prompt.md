# Content-upgrade proof v03 — production brief

7 October 2026. D-160. Base: proof v02 (D-159). Status: proof awaiting student review.

**Colour.** Off-palette vector colours map to the brand pair and its tints: cell outlines and cloud outline to ink #173a47; cloud inner line to #28bdbf; Section 2 comparison bars to cyan 15% (#dff5f5); Section 4 panel and Section 5 timeline/DATA boxes to cyan 10% (#eaf8f9); Section 5 bar tracks to cyan 20% (#d4f2f2), divider to cyan 40% (#a9e5e5), DATA outline to cyan 60% (#7ed7d9); the test-phase box to yellow 30% (#f7ebc6); Section 3 cream to white. The page colour #eefafa is already cyan 8%. National flags, the Vingroup emblem and the VinFast wordmark keep their own colours; raster artwork (background, car, logos) is unchanged and was not available to the cloud session.

**De-cluttering.** Removed lines that repeated other cells: Section 6 *Test frequency + unit economics / Cost pilots separately and the two pilot asterisks; Section 10 Proposed 12-month plan | Local outcomes untested box; Section 10 Repeat: full 90-day follow-up.

**Legibility.** The Section 5 keyword bestil taxa moves from the browser bar (1.5 mm x-height) into a full-width search box (about 2.1 mm, close to the poster's smallest existing lettering at 2.26 mm). Key figures (DKK600,000, 269,277, the five Section 8 targets) were already the largest lettering, so they were not enlarged.

**Checks** (`poster-content-upgrade-v03-2026-10-07-checks.json`): 237 unchanged strings byte-identical; no unexpected label changes; no old off-palette colour left; every remaining cell colour is in the palette or a protected flag/logo colour.

Rebuild: `python3 -B poster/poster-content-upgrade-v03-2026-10-07-render.py poster/poster-references-v04-2026-10-07.svg poster`, then the v03 check script. Back of chart: `poster-content-upgrade-v01-2026-10-07-back.*` (unchanged).
