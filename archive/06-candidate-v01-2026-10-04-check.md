# Section 6 candidate v01 — focused check

Prepared 4 October 2026. This is a standalone panel check, not a full-poster review or group acceptance.

## Copy and interface

- Display title is exactly `6. From Clicks to Rides`; the unnumbered subtitle is `Sales Strategy`.
- Five-stage flow reads left to right: Lead → Prospect → First paid ride → After-sales help → Consented repeat.
- Website/local page informs and hands riders to the app; direct app booking is the sales channel. A completed, paid trip is the sale. Installs and accounts remain leads.
- Prospect message is opt-in, one-time, and directed to installers who have not ridden, with verified service area and help route.
- Voucher is labelled proposed, DKK30 once per new rider, capped at 400. This corresponds to the DKK12,000 reserve shown by the approved plan.
- After-sales card is explicitly an in-car help card showing trip reference and support route; the copy says it is never a booking card.
- Consented repeat, clear fare terms and available help, and an unpaid app-store review invitation carry the requested relationship/value/soft-selling cues.
- Driver briefing and confirmation of help-route staffing and response standards are conditions before advertising. No service feature, conversion result or visible citation is claimed.
- Panel 5 hand-off aligns to search/social → local information page → app. Panel 7 remains the source for the DKK12,000 reserve. No screens are added to this sales flow.

## Visual and technical checks

- Candidate PNG is 1800 × 1600 RGB. The 2172 × 724 transparent illustration sheet is placed as one full-width pictogram ribbon. Its viewport includes the complete non-transparent art bounds plus padding; only transparent margins are trimmed, and no pictogram is cropped individually. The source alpha range is 0–255. No logo is used.
- Editable SVG embeds the illustration PNG as a data URI and keeps display copy in native SVG text elements. No linked image asset is required.
- The local renderer checked 48 text groups against canvas bounds and pairwise text overlap; all passed. Each stage’s text also stays within its card. The exported PNG was visually inspected for hierarchy, legibility at candidate scale, clipping and unintended text collisions; none observed.
- A0 print-size readability, group acceptance and final-assembly fit remain unverified.

## Writing gate

The protected `presentcheck.py` poster gate ran on the 160-word display copy only, against its 185-word section budget. The base writing checks reported zero effective hard stops; anti-slop detection ran with score 0 (`Clean`), and no out-of-register concepts were detected. The two label-colon findings were returned as poster genre review items, not hard stops.

The command exited 2 because the poster-mode checker requires exactly one budget-table marker and one KPI-table marker. This standalone panel intentionally contains neither full-poster table, so the gate cannot pass in fragment scope. Those two structural errors are recorded as scope limitations, not represented as a writing pass.
