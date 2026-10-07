# Panel 1: decorative illustration prompt and exact placement manifest

Date: 3 October 2026. Based only on D-037/D-040/D-041 and the selected panel specification v02. This prompt is prepared, **not executed**. It requests a replaceable decorative asset only. The editable SVG already contains a symbolic vector version of the same relationship.

## Self-contained AI illustration prompt

Create a single isolated decorative illustration asset for a university marketing-plan poster panel. It should show a mobile phone on the left, a simple curved arrow in the centre, and a cyan electric taxi MPV on the right, read left to right. Use a transparent background, navy hand-drawn ink outlines, clean cyan fills and a restrained yellow accent. Match a deliberate felt-tip-and-coloured-pencil drawing: slight stroke variation, clear shapes, generous negative space and no photorealism.

The phone is an abstract booking symbol, with two location pins connected by a dotted route on a plain pale-cyan screen. It must not reproduce a real interface. The taxi is a stylised modern electric MPV with a long cabin, large windows, wheels and one small yellow electric-bolt symbol. Keep it symbolic; it must not claim to document an actual Danish vehicle model or fleet. Use no manufacturer badges, company logos, number plates or roof-sign wording.

Output only this horizontal phone-to-electric-taxi decorative asset, on transparent background, approximately 4.5:1 in aspect ratio. Keep the phone and vehicle entirely inside the canvas with clear margins. Do not produce a complete poster, panel background, title, flag row or chart. Do not render any lettering, words, digits, dates, names, country labels, captions, citations, logos, signatures or watermarks. All exact text, national flags, company branding and data will be placed separately by a layout tool from an approved manifest.

## Exact text placement manifest

Canvas: 1600 × 1120 SVG units. No physical A0 panel size is claimed. Coordinates are editable layout anchors, not approval of final poster geometry. Body font Avenir Next, with Arial/sans-serif fallbacks; native logo paths have no replacement font.

| Text-object ID | Exact selected or source/context text | Placement | Font size in SVG units |
|---|---|---|---|
| heading-meet | Meet | x=80; baseline y=165 | 80 |
| country-vietnam | Vietnam | x=151; baseline y=363 | 26 |
| country-laos | Laos | x=333; baseline y=363 | 26 |
| country-indonesia | Indonesia | x=515; baseline y=363 | 26 |
| country-philippines | Philippines | x=697; baseline y=363 | 25 |
| country-india | India | x=879; baseline y=363 | 26 |
| country-kazakhstan | Kazakhstan | x=1061; baseline y=363 | 25 |
| country-denmark | Denmark | x=1243; baseline y=363 | 26 |
| country-netherlands | Netherlands | x=1425; baseline y=363 | 25 |
| vietnam-launch | 14/04/2023 | x=151; baseline y=406 | 30 |
| denmark-launch | 30/07/2026 | x=1243; baseline y=406 | 30 |
| vietnam-launch-citation | (VietnamPlus, 2023a) | x=151; baseline y=439 | 22 |
| denmark-launch-citation | (Green SM, 2026d) | x=1243; baseline y=439 | 22 |
| footprint-context | Eight markets · as at 26 September 2026 · Netherlands: pilot (Green SM, 2026a). | x=800; baseline y=486 | 25 |
| service-line | Green SM Car: app-booked electric taxi rides in Copenhagen | x=800; baseline y=565; second baseline y=616 | 43 |
| service-citation | (Green SM Denmark ApS, no date b) | x=800; baseline y=657 | 24 |
| operating-model | Owned fleet · Employed drivers | x=800; baseline y=989 | 43 |
| operating-model-citation | (Konkurrence- og Forbrugerstyrelsen, 2026b, p. 174) | x=800; baseline y=1033 | 24 |

The **service-line** string is one controlled text object, wrapped after “rides” only. In production, join its two rendered lines with one space to recover the exact approved string. The country names identify their respective flags. **heading-meet** is accompanied by the original Green SM mark and wordmark; the wordmark supplies the heading's “Green SM”.

## Separately placed vector/assets

| Object | Placement | Contract |
|---|---|---|
| Authentic Green SM mark and wordmark | x=314, y=40, w=510, h=138 | Use `panel-01-production-v01-2026-10-03-logo.svg`; original PDF paths/colours, no image-model logo or substitute typeface. Source: `green-sm-denmark-aps-ndc`, p. 1; full provenance in production brief/JSON. |
| Flag row | Centres x=151, 333, 515, 697, 879, 1061, 1243, 1425; common bottom y=325 | Vietnam → Laos → Indonesia → Philippines → India → Kazakhstan → Denmark → Netherlands. Denmark larger, yellow surround. No ninth flag. |
| Native illustrated phone | x=267–412, y=699–909 | Replace only this decoration if generation is later authorised; no lettering/logo. |
| Native app-to-ride arrow | x=488–824, y=781–838 | Left-to-right service relationship, yellow/navy. |
| Native illustrated electric taxi | x=866–1378, y=700–907 | Symbolic cyan MPV, no claim about a specific Danish fleet model. |

## Locked qualifications and limits

- Keep **as at 26 September 2026** and **Netherlands: pilot** in the displayed source/context note. A flag is not proof of a national/full commercial rollout.
- Keep launch milestones beneath Vietnam and Denmark. Do not label them incorporation dates.
- Scope the owned-fleet/employed-driver line to the displayed Copenhagen offer. Do not generalise it across all flags.
- The small **Vietnamese origin** label remains unapproved. It is excluded from this placement manifest and artwork.
- Text and numerical content stay in editable layout objects. Image models render none of them. Do not shorten a source caveat to make artwork fit.
- Preserve all five claim-adjacent source links in SVG; include these works plus the logo's About source in the consolidated Harvard reference package.
- Physical A0 fit, print/readability and final consolidated proof approval remain unverified.

Confidence: **high** in the manifest's selected strings and source qualification. No image-model run, printing, manual redraw or whole-poster acceptance is claimed.

## Actual authorised generation now available

Following the section-specific authorisation relayed by the parent, a built-in image-generation run has now produced the section's decorative illustration. The prompt above remains a prepared standalone prompt; the exact executed prompt is separately preserved in `panel-01-production-v01-2026-10-03-generation-prompt.txt`. The complete actual composition is `panel-01-production-v01-2026-10-03-generated-section.svg` / `.png`. All text objects, flags, dates, logo and source links use the same controlled manifest. Native-vector illustration coordinates above refer to the earlier all-vector proof; the generated-asset placement and original-file/hash provenance are recorded in the JSON manifest.
