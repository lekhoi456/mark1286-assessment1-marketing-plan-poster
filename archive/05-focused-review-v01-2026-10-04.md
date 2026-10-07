# Panel 5 focused checks and review

Candidate v01 · 4 October 2026. Status: proposal for review; group approval and A0 fit are not claimed.

## Copy and content

- Display heading is exactly **5. Digital Marketing**. Display copy is 177 words against the 210-word panel budget.
- D-031–D-033 remain fixed. Search/social lead to one local information page and the advertised Green SM app route. The page is not presented as checkout, and the app checkout was not tested (E-188).
- PPC is limited to verified service area/hours. The page covers map/coverage, hours, fare terms and the help route. Social explains fare/help. The opt-in CRM follow-up supports repeat without claiming a lift; the 30-day booking capability is labelled as advertised (E-016).
- E-042 is represented only by its limitation: national social-media identities do not establish unique Copenhagen prospects. No national reach percentage appears on the panel.
- Proposed/planned line amounts match the integrated plan: PPC DKK108,000; social DKK90,000; creative/localisation 120 h / DKK72,000; CRM/support handover 120 h / DKK72,000; tools 12 × DKK2,500 / DKK30,000. Professional time is an assumed DKK600/h. Panel 5 shows no combined subtotal; panel 7 owns campaign management and the full budget.
- DOOH remains conditional on Gate B and 90-day repeat ≥35%. The rate-card calculation is 200,000 impressions × DKK191 CPM = DKK38,200, plus DKK4,995 setup = DKK43,195. The panel states that VAT and production are excluded and no rides are assumed (E-029).
- E-016, E-029, E-042 and E-188 remain internal comments in the copy Markdown. The poster face has no citations. The E-042 figure itself is omitted to avoid treating national audience identities as local demand.

## Artwork and geometry

- SVG parses as XML, has an 1800 × 1400 viewBox and embeds the blank generated illustration and exact `poster/shared-logo.png` bytes. All displayed lettering is SVG text; no image model generated words or numbers.
- Rendered PNG is 1800 × 1400. The exact title, channel amounts, DOOH threshold and cost calculation appear in the render.
- Font-metric bounds found all 19 text objects inside the canvas, with card text inside its card. Text-object bounding boxes do not overlap. The four cards have 22 px gaps; the card row, DOOH callout and footer occupy separate regions. Thresholded visible illustration ends around y=624, 26 px before the cards begin at y=650.
- The full-size render was inspected. Logo, lettering, card edges and DOOH arithmetic are legible with no clipping or visible overlap.

## Writing gate

Ran `presentcheck.py` in poster mode on the display-copy section only, with the exact heading, registry, source directory, concept list and strict-scope flag. Result: 177 words / 210; zero effective grammar, style, integrity, reference, figure, word-limit or module-scope hard stops; the detector ran and reported no hard findings.

The fragment exits 2 for exactly two expected full-poster requirements: no allocation table and no KPI table. These belong to panels 7 and 8. This is not a whole-poster gate pass. The detector returned review items for parallel paragraph rhythm and bold channel labels; both are intentional comparison/card labels in this poster genre. The gate's label-colon genre reviews were read manually and are clear as infographic labels.

## Panel interfaces and remaining limits

- Panel 6 owns the DKK30 first-ride incentive and the completed-paid-trip sale definition. The help route and in-car help card remain proposals that depend on staffed support.
- Panel 7 must carry the same search, social, creative/localisation, CRM/support, tools and conditional DOOH amounts. Its 160 h / DKK96,000 campaign-management line remains panel 7's responsibility.
- Panel 8 should track paid clicks to first completed paid trips by channel and 90-day repeat. No screen-generated rides are credited.
- Still open: group image acceptance, fit in the assembled A0 layout and print-distance legibility. Runtime advertising, app checkout, service coverage and operational capacity were not tested here.
