# Panel 2 — citation-display removal

Date: 3 October 2026. **Status: DONE.** Confidence: **high** within this display amendment. Authority: D-055/LG-004, the lecturer's instruction relayed by the student and recorded in [poster citation display policy](../design/poster-citation-display-policy-v01-2026-10-03.md).

The full visible p2-source attribution object is removed from both SVGs, the complete/half-size PNGs and the display-copy block. Every remaining text object, handwriting glyph, position, chart shape and illustration is unchanged from v04. Sources remain in internal metadata and research; no reference-list/back/end waiver is inferred.

## Complete image first

- [Complete PNG](../design/panel-02-production-v05-2026-10-03.png), 1,800 × 1,360 pixels.
- [Small comparison PNG](../design/panel-02-production-v05-2026-10-03-small-preview.png), 900 × 680 pixels.
- [Portable SVG](../design/panel-02-production-v05-2026-10-03.svg).
- [Native-text editable SVG](../design/panel-02-production-v05-2026-10-03-editable.svg).
- [Exact visible copy/internal mapping](../design/panel-02-production-v05-2026-10-03.md).
- [Manifest](../design/panel-02-production-v05-2026-10-03-text-manifest.json).
- [Original reused art](../design/panel-02-production-v05-2026-10-03-generated-art.png).
- [Original executed prompt, reused](../design/panel-02-production-v05-2026-10-03-illustration-prompt.md).
- [Amendment source](../design/panel-02-production-v05-2026-10-03-layout.py).
- [Checks](../design/panel-02-production-v05-2026-10-03-checks.json).

## Removed and retained mapping

Removed object: `p2-source`. Actual former visible wording: **Source: Statistics Denmark (2026b), FOLK1A; calculated sums of single-year ages.** The shared policy transcribes FOLK1A1; the intended full attribution object was removed by its stable ID. The verified internal dataset remains FOLK1A. No shared policy file was edited by this agent.

The manifest retains that complete former object internally, the source key, evidence E-191/E-193, saved PDF/hash, calculation basis and display-policy authority. All four count labels, age bands, 40.2% pill, separate 269,277, dated municipality/18+ scope and exact all-city denominator note remain on the poster face. So do the selected priority/filter/service-area text, Proposed rider profile, six labels and approved repeat-opportunity caption.

## Focused verification

- Exactly 30 remaining text objects. After XML parsing, each portable glyph group and native editable text object is byte-equivalent to v04, apart from the one removed attribution.
- Manifest data, chart geometry and font metadata are identical to v04. Zero baseline and mathematical bar heights are unchanged.
- Adult counts sum to 560,069; plus 110,320 under 18 gives all 670,389 residents. 269,277 ÷ 670,389 rounds to 40.2%.
- Current source PDF hash matches preserved source metadata. Reused decorative PNG hash/bytes are unchanged. No image-generation call, font redraw or checker modification.
- Full/half-size PNGs inspected: author/year/source-attribution footer absent; retained date/scope, numbers, denominator, profile and caption visible. No observed new overlap/clipping. The resulting whitespace is retained to preserve all other geometry.
- Visible text is 86 words under the existing counting convention. All linked package/source/control files exist.

An intentional citation-free display is governed by the new lecturer instruction; no full writing/reference wrapper pass is asserted or protected check disabled. The verified source apparatus remains intact.

## Concerns and limits

No blocker within this amendment. Full-A0 integration, physical print/viewing/redraw and final submission-image acceptance remain unverified. Source/reference-list packaging is separate from this face-only removal. Earlier versions are preserved. No shared controls, registry, another panel, Comet session, commit, push or whole-A0 assembly changed. The same agent retains panel 2 ownership.
