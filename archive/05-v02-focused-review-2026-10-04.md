# Panel 5 v02 focused checks and review

Candidate v02 · 4 October 2026. Proposed for parent review; selection remains with the parent, and group approval is not claimed.

## Copy and plan alignment

- Display heading is exactly **5. Digital Marketing**. Display copy is 192 words against the 210-word panel budget.
- Paid social names the approved S1 priority: Copenhagen residents aged 25–44 who pay personally for repeat local taxi trips in the verified service area. This follows the approved age-scope amendment D-043; it no longer addresses Copenhagen adults generally.
- The visible footer now reads: “Search + social: paid click → first completed paid ride → 90-day repeat.” It contains no panel-workflow reference. This keeps campaign activity distinct from S8's sale definition, a completed paid trip. DOOH is labelled impressions-only; no screen-generated ride or conversion is credited.
- The route remains search/social → one local information page → Green SM app booking. The audience-facing note now reads “LOCAL PAGE = INFO · RIDE BOOKINGS IN APP”. Website checkout is not evidenced and app checkout was not tested; that caveat remains internal (E-188). CRM/email follows the first trip with consent, and the 30-day advance-booking claim remains attributed as advertised (E-016).
- Costs and ownership remain aligned with §9: PPC DKK108,000; social DKK90,000; creative/localisation 120 h / DKK72,000; CRM/support handover 120 h / DKK72,000; tools 12 × DKK2,500 / DKK30,000. Professional time uses the plan's assumed DKK600/hour. No subtotal is shown; panel 7 owns campaign management (160 h / DKK96,000) and the full budget.
- DOOH is conditional on Gate B and 90-day repeat ≥35%. The displayed arithmetic now states both the CPM divisor and unit: 200,000 ÷ 1,000 × DKK191 CPM = DKK38,200; + DKK4,995 setup = DKK43,195. This equals the §9 rate-card lines; VAT and production are excluded. No screen rides are assumed (E-029). Gate B's preceding continuation condition remains in S8: mature repeat ≥20% and paid cost per first rider ≤ DKK1,829.
- E-016, E-029, E-042 and E-188 remain internal comments in the copy Markdown; the poster face has no visible citations. E-042 is used only to qualify national reach as insufficient evidence of local prospect demand.

## Artwork and geometry

- SVG parses as XML with a 1800 × 1400 viewBox; PNG render is 1800 × 1400. All 19 SVG text objects were rendered individually for pixel bounds: each is inside the canvas, no text-object bounds intersect, and all card text is inside its own card. The DOOH copy bounds are x=842–1446, y=1045–1189. The full candidate render was visually inspected; target copy, route note and complete CPM calculation are legible, with no clipping or visible collision.
- The embedded display logo is byte-for-byte `poster/shared-logo.png` (SHA-256 `36a99749e3cc9585573fedda5fb1dbcf6a76483872cadc2d0f6651ec95430db9`), preserving the approved hand-drawn lock-up. The blank art is unchanged from v01 (SHA-256 `8640a69a1dab14faa8b977a26cbb8b82d7a7f1729cb5abbeb2a8e2512f976bd8`). All lettering is editable SVG text.
- Focused content assertions passed for the 25–44 audience, revised footer, all tactic amounts, the exact DOOH formula and total, Gate B/35% trigger, impressions-only treatment, internal E-ID comments, embedded asset bytes and image dimensions.

## Writing gate and limits

`presentcheck.py` ran in poster mode on the display-copy section only, with the exact heading, registry, source directory, concept list and strict-scope flag. It reports 192 words / 210 and zero effective grammar, style, integrity, reference, figure, word-limit or module-scope hard stops. Its two fragment errors are expected: the standalone panel has no full-poster budget table or KPI table. This is not a whole-poster gate pass. Six genre label-colon reviews were checked as clear infographic labels; the detector reported minimal signals and one formatting review for seven bold channel labels.

Still open: parent selection, group visual acceptance, fit in the assembled A0 layout and print-distance legibility. Runtime advertising, app checkout, operational support and service capacity were not tested here.
