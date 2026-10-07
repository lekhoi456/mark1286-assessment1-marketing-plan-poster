# Content-upgrade proof v01 — production brief

7 October 2026. D-157 proposal, D-158 authorisation. Source: `poster-references-v04-2026-10-07.svg` as uploaded by the student. Status: proof awaiting student review; nothing accepted.

## What was produced

| File | Use |
|---|---|
| `poster-content-upgrade-v01-2026-10-07.svg` / `.pdf` / `-preview.png` | A0 front (1189 × 841 mm) |
| `poster-content-upgrade-v01-2026-10-07-back.svg` / `.pdf` / `-back-preview.png` | A0 back: nineteen Harvard References |
| `…-references.md` | Exact back-of-chart list |
| `…-changes.json` / `…-checks.json` | Change log and automated checks |
| `…-render.py`, `…-check.py`, `glyph-reuse-lettering.py` | Reproducible build and checks |
| `presentation-script-v02-2026-10-07` / `presentation-study-guide-v02-2026-10-07` (`.md`, `.docx`) | Speaking materials for the new content |

Rebuild locally: `python3 -B poster/poster-content-upgrade-v01-2026-10-07-render.py poster/poster-references-v04-2026-10-07.svg poster`, then the check script with the same arguments.

## Method

The approved lettering was set locally with CoreText fonts that the cloud session lacks. `glyph-reuse-lettering.py` splits each existing lettering path into per-character outlines, gathers every string in the same font (Noteworthy-style body, Marker Felt-style headings; italics are the body glyphs with skewX −10), normalises sizes and fits pair spacing from the existing strings. New lettering therefore reuses the approved glyph shapes. Only ± (from + and −) and æ (from a and e) are assembled glyphs. Unchanged lettering is byte-identical (244 strings), as are embedded images and external image links. Apart from the interior of the Section 5 page mock (decorative houses and two blank bars replaced by the Danish example), cell outlines, artwork, figures and the header are untouched.

## Edits on the front

Section 1: Owned fleet (590 registered) · Employed drivers. Section 2: Later: visitors · business accounts. Section 3: (part to be sold) under Dantaxi; Shared line adds Similar fares (Dantaxi/Drivr). Section 5: n=79 · ±11 pp; / Content; Copenhagen page mock shows the search field bestil taxa and Elektrisk taxa / Tjek prisen. / Book i appen. instead of decorative houses; voucher box DKK15 vs DKK30 with Post-launch · 400 riders · 1 each; asterisks and *Proposed removed. Section 6: header tag removed; CTR, CPC / app installs / conversion diagnostics. Section 7: Nov 2026–Oct 2027; two-line unit check; app build joins the outside-budget list. Section 8: paid-campaign scope note; n=400 per wave; TRACKING. Section 9: PILOTS header; neuromarketing creative test replaces the duplicated exclusion line. Cloud: Dr; one italic global proposal statement. Footer: References move to the back; a Member contributions strip with three pending slots.

## Not verified here

Car/harbour background PNGs are external files absent from the cloud session, so the previews and PDFs omit them; the SVG keeps the original links and renders fully in the local poster folder. Cloud text uses the original live Chalkboard SE font stack; check its fit on macOS. Run `presentcheck.py` on the changed copy, obtain a native Danish check, re-read KFST 2026b p.49 for E-213, and check actual-size legibility. Member contributions must come from the group.
