# Poster v01 review: integrated findings and v02 changes

Reviewed version: `07_drafts/poster-v01-2026-09-28.md` (1,362 counted words). Revised version: `07_drafts/poster-v02-2026-09-28.md` (1,581 counted words). Reviewer reports: [local-marker lens](poster-v01-review-local-marker.md), [UK-moderator lens](poster-v01-review-uk-moderator.md). Both are agent mock reviews of Markdown only; scores are estimates, not marks, and C7 cannot be judged before design.

## 1. Estimates and agreement

| Criterion (weight) | Local marker | UK moderator |
|---|---|---|
| C1 (10) | 6.5 (5.5–7.5) | 7 (6–8) |
| C2 (15) | 10 (8.5–11.5) | 10 (8.5–11.5) |
| C3 (20) | 14 (12–16) | 14 (12–16) |
| C4 (15) | 11 (9.5–12.5) | 11 (9–12.5) |
| C5 (10) | 7 (6–8.5) | 7 (6–8) |
| C6 (10) | 6 (5–7.5) | 6.5 (5.5–7.5) |
| C7 (20) | 13 (9–16) | 13 (9–16) |
| **Total** | **≈67 (58–75)** | **≈68 (56–80)** |

The two lenses agreed on every blocking and significant issue. Both verified the numbers against the model and found every checked claim supported by its PDF page, with two claims narrower than written (E-015, E-024).

## 2. Fix log

| ID | Issue (both reviews unless noted) | v02 disposition |
|---|---|---|
| F1 | "Price is level" overstated: DKK227 is the meter; the same page publishes a higher app maximum | Fixed: "because meter prices are level"; added "App fares have a separate published maximum, so we promise clear fare terms, not a lower price." TAXA's figure named as its door price, dated 1 December 2023 |
| F2 | Help route promised but unfunded; no KPI measures the promise | Fixed: budget line renamed "CRM set-up and help-route handover"; "frontline support ... outside this budget" stated; Sales step 4 says the route is staffed outside the budget and promoted only once it meets its standard; two KPI rows added (help requests answered on time; riders who found area and fare clear); Gate A names the help-route standard |
| F3 | Segmentation asserted, not shown | Fixed: three segments named; reasons for not targeting organisations and visitors given, labelled as our judgement |
| F4 | UVP not labelled; contrast only with platforms | Fixed: "Positioning statement and unique value proposition"; Drivers of change now cites the authority's contrast with dispatch offices that rely on self-employed operators (new E-186, p. 174) |
| F5 | Price/habit evidence not linked to the clarity position; survey population unstated | Fixed: population stated (79 Capital Region riders who chose Uber, Bolt or TaxiToGo over a traditional taxi firm, pp. 150-151); psychographic hypothesis now reasons from level meter prices |
| F6 | Internal code "E-029" printed in the budget table (local marker, blocking) | Fixed: both screen rows now read "Assumption: ... at AFA Decaux (2026) list price/fee", which is accurate because the quantity is assumed and the price is sourced. The checker accepts only E-IDs after "Evidence:", so E-IDs stay in comments |
| F7 | Break-even line not reproducible; exposure not stated | Fixed: "30% contribution on a DKK227 trip ... about DKK46,000 of DKK600,000. Break-even needs about 8,800 rides"; "If Gate A fails, spending stops at DKK177,000" |
| F8 | Gate B ambiguous; DKK1,829 unexplained | Fixed: full Gate B sentence; "Floors and targets are planning assumptions" (floors = downside case, per plan §10) |
| F9 | No sales channel | Fixed: "Sales channel: direct to consumer, through Green SM's own app and website" |
| F10 | Trend list partly answered (neuromarketing, revenue model); AI looks refused | Fixed: revenue model (pay per trip, usage-based), subscription deferred with reason, AI chatbot test condition, neuromarketing not used |
| F11 | Company panel thin on core product | Fixed: "The core product there is Green SM Car, app-booked electric taxi rides". Vietnamese car tiers (E-162) left out for space |
| F12 | Awareness is not a decision-process stage | Fixed: stages renamed (need recognition, information search, evaluation, purchase, post-purchase); screens described separately as awareness after Gate B |
| F13 | Minor wording | Fixed: "Copenhagen Municipality"; ACEA figure marked as calculated; "nationally" added to the app-count survey; "app users who have not ridden"; drivers employed "in the initial phase"; brand kept "because the April 2026 rebrand unified it across markets"; contingency basis includes in-car card printing; "within 90 days of the first ride" |
| F14 | En dashes for ranges (local marker) | Declined: house style bans dashes in prose; hyphens used ("40-50%") |
| F15 | "Amount (DKK)" header and thousands separators (both) | Declined for the checking copy: the presentcheck contract requires the exact header "Amount" and plain numbers. Currency and period are stated beside the table. Revisit display formatting at P7 as an approved presentation copy |
| F16 | Density (UK moderator) | Accepted risk: v02 is 1,581 words because the fixes add reasoning the moderator needs without the pitch. P7 actual-size proof decides further cuts; description goes before reasons |

## 3. Challenges to prepare for Q&A (not defects)

- "Easy to judge before you book" is not unique: Uber shows a price estimate before booking (KFST p. 150) and TAXA's app quotes a fixed price. The UVP therefore leads with employed drivers and help after the ride.
- A 92% year-one shortfall may look unrealistic: answer with the authority's view that entry needs substantial marketing (p. 179) and the gates that cap exposure.
- O1 awareness is measured while the only awareness buy waits for Gate B.
- Segment size is unknown: 670,389 is the municipality, and launch coverage was Inner Copenhagen.
- KFST p. 151 shows 11% chose an app for greater safety and security; this partially supports the psychographic hypothesis but is not yet an evidence-log row.
- "Danish first" but only English copy is shown: a Danish line needs a native-speaker check before use.

## 4. Gate results

| Check | v01 | v02 |
|---|---|---|
| `wordcount.py` | 1,362 words; all panels within budget after trims | 1,581 words; all panels within revised budgets |
| `refs.py check-draft` | 0 errors, 0 warnings; reference list identical (14) | 0 errors, 0 warnings; reference list identical (14) |
| `presentcheck.py --strict-scope` | Detector ran; anti-slop 0; module scope 0; 1 hard stop | Detector ran; anti-slop 0; module scope 0; budget table sums to 600000 and 100.00; 9 KPI rows; 1 hard stop |
| Remaining hard stop | Base checker cannot parse the digits in "TAXA 4x35" and reports the reference as uncited. `refs.py check-draft` matches it. The base checker is frozen until 12 October 2026 (AGENTS rule 11), so this is recorded, not suppressed | Same |

Label-colon findings (18 in v02) are the poster-label genre exception and were read for meaning.

## 5. Still open before content approval

- Contribution statement (Q-S5).
- Year suffixes for the final cited set (e.g. Green SM 2026a/2026f, Kemp 2025a) before P8.
- Group reading and approval of v02 wording (G5).
