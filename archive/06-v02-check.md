# Section 6 candidate v02 — focused review

Prepared 4 October 2026. This is a standalone panel copy clarification, not A0 acceptance or group approval.

## Focused diff from v01

The Prospect sentence now names the audience directly: “people who installed the app but have not taken a ride”. It retains the opt-in, verified service-area and help-route conditions. All other displayed copy is unchanged; artwork, card/arrow geometry, colours and typography are unchanged.

## Copy and interface

- Display title is exactly `6. From Clicks to Rides`; the unnumbered subtitle is `Sales Strategy`.
- Five-stage flow reads left to right: Lead → Prospect → First paid ride → After-sales help → Consented repeat.
- Website/local page informs and hands riders to the app; direct app booking is the sales channel. A completed, paid trip is the sale. Installs and accounts remain leads.
- Prospect message is opt-in and one-time, directed to people who installed the app but have not taken a ride, with the verified service area and help route.
- V02 changes only the audience wording; opt-in, verified service-area/help-route language and all other copy/art/geometry remain fixed.
- Voucher is labelled proposed, DKK30 once per new rider, capped at 400. This corresponds to the DKK12,000 reserve shown by the approved plan.
- After-sales card is explicitly an in-car help card showing trip reference and support route; the copy says it is never a booking card.
- Consented repeat, clear fare terms and available help, and an unpaid app-store review invitation carry the requested relationship/value/soft-selling cues.
- Driver briefing and confirmation of help-route staffing and response standards are conditions before advertising. No service feature, conversion result or visible citation is claimed.
- Panel 5 hand-off aligns to search/social → local information page → app. Panel 7 remains the source for the DKK12,000 reserve. No screens are added to this sales flow.

## Visual and technical checks

- Candidate PNG is 1800 × 1600 RGB. The 2172 × 724 transparent illustration sheet is byte-identical to v01 and is placed as one full-width pictogram ribbon. Its viewport includes the complete non-transparent art bounds plus padding; only transparent margins are trimmed, and no pictogram is cropped individually. The source alpha range is 0–255. No logo is used.
- Editable SVG embeds the illustration PNG as a data URI and keeps display copy in native SVG text elements. No linked image asset is required.
- The v02 renderer checked 49 text groups against canvas bounds and pairwise text overlap; all passed. Each stage’s text also stays within its card. The exported PNG was visually inspected for hierarchy, legibility at candidate scale, clipping and unintended text collisions; none observed.
- Exact-text check confirms the Prospect SVG lines reassemble to the v02 Markdown sentence, including the opt-in and verified service-area/help-route conditions. The card uses eight lines versus seven in v01.
- A v01/v02 comparison confirms identical canvas dimensions, all static path geometry, embedded art bytes and every non-Prospect text position. The rendered pixel difference is confined to the Prospect copy area: `(442, 978)–(674, 1193)`.
- A0 print-size readability, group acceptance and final-assembly fit remain unverified.

## Writing gate

The protected `presentcheck.py` poster gate ran on the 166-word v02 display copy only, against its 185-word section budget. The base writing checks reported zero effective hard stops; anti-slop detection ran with score 0 (`Clean`), and no out-of-register concepts were detected. The two label-colon findings were returned as poster genre review items, not hard stops.

The command exited 2 because the poster-mode checker requires exactly one budget-table marker and one KPI-table marker. This standalone panel intentionally contains neither full-poster table, so the gate cannot pass in fragment scope. Those two structural errors are recorded as scope limitations, not represented as a writing pass.
