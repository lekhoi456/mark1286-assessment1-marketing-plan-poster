# Section 5 v03 — lettering correction

Status: HUMAN-REVIEW candidate. The user accepted the v02 direction; this correction applies the requested hand-drawn lettering and heading-length underline. Final v03 acceptance is not inferred.

Body text now resolves to the real `ChalkboardSE-Regular` font. The older `ChalkboardSE` alias had silently resolved to Helvetica. Headings remain `MarkerFelt-Wide`. The new glyph helper records actual CoreText run font names. Unicode arrows previously fell back to STSongti; they are now deliberately drawn as simple native vector arrows. No letter uses Helvetica or an unreported font fallback.

All 90 word-bearing whitespace tokens, every number, proposal qualifier and illustration placement match v02 exactly. No font shrinking was needed. The heading underline ends at x=473.284 rather than extending across the whole cell; the exact advance width is recorded in checks. Base geometry and artwork are unchanged. V09 illustrations retain their existing shading/detail; simplifying those illustrations for large hand colouring remains separate future style work.

Outputs use this prefix: `05-cell-fit-v03-2026-10-04`. Open `-poster.png`, `-close-up.png` and `-poster.pdf`. Source: `-poster.svg`, `-layout.svg`, `-render.py`, `-glyphs.swift`; exact copy: `-copy.md`, `-displayed-copy.txt`; checks: `-checks.json`.

Focused checks: real glyph-box corners fall inside the native curved cell; exact copy comparison passes; assembled source reconstructs the unchanged A0 base when the candidate layer is removed; native PDF MediaBox is 1189×841 mm; output widths are 1672 px and 1600 px. The unchanged copy gate was not rerun. The inherited v02 mapping and focused checker remain applicable in `05-cell-fit-v02-2026-10-04-notes.md` and `-copy-check.json`.

Minimum type remains 11.49 pt; main labels generally13–15pt. Reading distance and final hand-colouring suitability remain unverified. This is a lettering correction, not acceptance of the full poster or a simplified-art completion.
