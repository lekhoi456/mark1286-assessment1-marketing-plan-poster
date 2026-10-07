# Panel 1 hand-drawn Green SM lockup revision

Status: DONE_WITH_CONCERNS. Date: 3 October 2026. Scope: replace the sole Green SM header lockup in accepted v13 with the controller-supplied shared hand-drawn PNG.

## Delivery

- [Full v14 PNG](../design/panel-01-production-v14-2026-10-03.png), 2400 × 1680.
- [Small logo proof](../design/panel-01-production-v14-2026-10-03-logo-proof.png) and [complete header crop](../design/panel-01-production-v14-2026-10-03-header-crop.png).
- [Self-contained editable SVG](../design/panel-01-production-v14-2026-10-03.svg), [byte-unchanged transparent logo](../design/panel-01-production-v14-2026-10-03-green-sm-logo.png), [reproduction source](../design/panel-01-production-v14-2026-10-03-compose.py), [exact copy/package notes](../design/panel-01-production-v14-2026-10-03.md), [manifest](../design/panel-01-production-v14-2026-10-03-manifest.json) and [focused checks](../design/panel-01-production-v14-2026-10-03-checks.json).

## Result and evidence

The complete shared mark and GREEN SM wordmark use the existing placement box and proportional fitting. Only transparent padding is excluded from the viewport. Embedded PNG bytes match shared SHA256 `36a99749e3cc9585573fedda5fb1dbcf6a76483872cadc2d0f6651ec95430db9`; original alpha is retained.

Eighteen narrow checks pass. Sixteen ordinary strings/glyphs/sizes/positions, eight flags/date/home/frame/pilot details, Vingroup emblem/calendar, raw car art and full hand-drawn VinFast identity remain unchanged. All non-logo SVG objects match v13 except intended description metadata. Pixel comparison confines all 48,788 changed pixels to the header logo region, bounds 651 × 175 at +532,+74. The comparison's exit 1 denotes the expected selected image difference.

Actual full PNG and close proof inspected: hand-drawn treatment visible, GREEN SM legible, no observed overlap/clipping. No other logo, source apparatus, historical version, shared control or panel changed. No generation, raster repaint, broad writing/source gate or whole-poster check was performed.

Concerns: new logo-treatment feedback and physical A0 proof remain pending. Confidence: high within this narrow revision. Dedicated agent retained. Unresolved implementation questions: none.
