# Budget and KPIs: selected Copenhagen budget and comparison scenarios

Prepared 28 September 2026; selected plan added the same day. Copenhagen is the chosen focus market (D-031). The group chose segment S1 with positioning P1 and the **DKK600,000 market-entry envelope** (D-032). The line items and every performance assumption remain **agent proposals**, not Green SM budgets, forecasts or agreed targets. The lean, middle and expanded envelopes in §2 onwards are kept as the comparison record. Period: **12 months, M1–M12; start date unapproved; DKK throughout**.

**Main finding:** the illustrative acquisition assumptions do **not** make any envelope financially self-funding in year one. Do not present a neat allocation or the market-selection K3 score as proof of feasibility. The useful output is a transparent cost model, the required break-even conditions and a measurement design that can reject the proposal.

## Selected plan budget — Copenhagen S1, DKK600,000 (D-032)

The total and the objective (market entry: awareness and trial among S1, with repeat use as the scale gate) are group choices. The allocation below is the agent's proposal for approval, derived from the middle envelope. Account/partner sales (90 hours, DKK54,000) is removed because S2 was not chosen. Its hours move to CRM and customer support (+60), which delivers P1's route to resolution and opted-in post-trip follow-up, and to local content and creative (+30), for the service-area, fare and help pages. Media, DOOH, tools, incentive reserve and contingency are unchanged. The model gives the moved hours **no conversion credit**.

| Activity | DKK | Share |
|---|---:|---:|
| Research and service validation: 60 hours × 600 | 36,000 | 6.00% |
| Creative production and localisation: 120 hours × 600 | 72,000 | 12.00% |
| Campaign management and optimisation: 160 hours × 600 | 96,000 | 16.00% |
| CRM and customer-support handover: 120 hours × 600 | 72,000 | 12.00% |
| Paid search envelope | 108,000 | 18.00% |
| Paid social envelope | 90,000 | 15.00% |
| Digital Copenhagen DOOH: 200,000 / 1,000 × 191 | 38,200 | 6.37% |
| One assumed DOOH setup | 4,995 | 0.83% |
| Analytics/CRM tools: 12 months × 2,500 | 30,000 | 5.00% |
| Proposed first-ride incentive reserve | 12,000 | 2.00% |
| Uncommitted contingency | 40,805 | 6.80% |
| **Total** | **600,000** | **100.00%** |

Consumer-only results, same performance assumptions as §3; no account rides. DKK, rounded for display; `budget-scenario-results.json` keeps full precision.

| Case | First payers | Ride equivalents | Booking-value proxy | Contribution less DKK600,000 at 30% | At 50% |
|---|---:|---:|---:|---:|---:|
| Downside | 108.2 | 156.9 | 35,625 | −589,313 | −582,188 |
| Illustrative | 378 | 675.7 | 153,378 | −553,987 | −523,311 |
| Upside | 1,262.8 | 2,683.4 | 609,128 | −417,262 | −295,436 |

**What the group has chosen, stated plainly:** a year-one market-entry investment that does not pay for itself under any modelled case. Full-envelope break-even needs 8,811 rides at 30% contribution (5,287 at 50%); the illustrative case produces about 676. Covering paid media and the voucher per new payer needs about 8.1 rides at 30%, against 1.79 modelled within the window. The poster and pitch must present this as a deliberate, capped entry investment with stop and scale rules, not as ROI. It must not be bridged with an invented lifetime value. The strongest objection to expect in Q&A is "why spend DKK600,000 before proving repeat use?"; the answer is the staged release in §6 and the repeat-use scale gate, and the lean envelope is the fallback if the group changes its mind.

## 1. Reproduce and distinguish the inputs

Run `python3 -B 06_workflow/scripts/model_marketing_scenarios.py`. Inputs are in `budget-scenario-inputs.json`; all three allocations and nine budget/performance combinations are in `budget-scenario-results.json`. The script calculates actual line totals, percentages, capped incentives, conditional acquisition/repeat/account quantities and contribution break-even cases. No external package or company account is required.

| Input | Value / basis | Evidence status and boundary |
|---|---|---|
| Copenhagen digital-out-of-home (DOOH) list CPM | DKK191 per 1,000 impressions; 41-screen network | `afa-decaux-2026`, PDF p. 3. Published 2026 media-owner list price, not a paid-social CPM. Minimum order, inventory and negotiated price unconfirmed. |
| DOOH setup | DKK4,995 for the assumed single campaign | Same rate card p. 3, including five creative variants. The model assumes one setup, not one per month. Creative production is separately allocated. |
| DOOH exclusions | VAT and production excluded | Same page. Tax recovery and supplier configuration require verification; no cross-year price guarantee. |
| Illustrative fare calculation | DKK39 + 10 km × DKK11 + 12 min × DKK6.5 = **DKK227** | `green-sm-denmark-aps-ndb`, PDF p. 3, published **Day (Min) meter** schedule, last updated 24 June 2026. **Not** an app maximum, observed transaction or average fare. No price-leadership claim. |
| Professional time | DKK600/hour across the modelled roles | **Assumption**, not an external benchmark or the company's wage. The advertised DKK185/hour driver rate is operational recruitment evidence, not a marketing labour price. |
| Search CPC, social CPM/CTR and conversion | Three explicit performance cases below | **Assumptions**, not extracted market benchmarks, probabilities or forecasts. |
| Contribution before marketing | 30% and 50% of the illustrative booking-value proxy | **Assumptions**, not Green SM margins. Intended to represent vehicle/driver/energy and other variable service costs before this programme's incentives. |

Marketing costs are on a provisional net-of-recoverable-VAT basis; actual tax treatment is unresolved. Vehicles, depot, charging infrastructure, licence fees and ordinary driver payroll are **not** inside this marketing budget. Those resources must already be available and costed in a real operating/contribution model before approval. Additional campaign-induced operating costs would worsen the results if not already captured. Rates extending beyond 2026 must be re-quoted.

## 2. Three costed envelopes

| Alternative | Proposed total | Professional hours across M1–M12 | Paid search / paid social | DOOH impressions | Incentive reserve | Uncommitted contingency |
|---|---:|---:|---:|---:|---:|---:|
| Lean learning route | 240,000 | 180 | 48,000 / 24,000 | 0 | 6,000 | 36,000 |
| Middle comparison case | 600,000 | 460 | 108,000 / 90,000 | 200,000 | 12,000 | 40,805 |
| Expanded comparison case | 1,200,000 | 860 | 252,000 / 216,000 | 400,000 | 30,000 | 56,605 |

The totals are round agent-selected envelopes. Quantity/people choices produce the line costs; contingency is the disclosed residual, not a hidden revenue balancing item. The expanded option has the smallest percentage buffer despite greater execution exposure: a reason to reject premature scale, not a claim of efficiency. Hours are combined professional effort, **not assigned or completed work by group members**.

### Middle allocation — calculation example

| Activity | DKK | Share |
|---|---:|---:|
| Research and service validation: 60 hours × 600 | 36,000 | 6.00% |
| Creative production and localisation: 90 hours × 600 | 54,000 | 9.00% |
| Campaign management and optimisation: 160 hours × 600 | 96,000 | 16.00% |
| Partner/account prospecting and consultative sales: 90 hours × 600 | 54,000 | 9.00% |
| CRM and customer-support handover: 60 hours × 600 | 36,000 | 6.00% |
| Paid search envelope | 108,000 | 18.00% |
| Paid social envelope | 90,000 | 15.00% |
| Digital Copenhagen DOOH: 200,000 / 1,000 × 191 | 38,200 | 6.37% |
| One assumed DOOH setup | 4,995 | 0.83% |
| Analytics/CRM tools: 12 months × 2,500 | 30,000 | 5.00% |
| Proposed first-ride incentive reserve | 12,000 | 2.00% |
| Uncommitted contingency | 40,805 | 6.80% |
| **Total** | **600,000** | **100.00%** |

No purchase or partner contact has been made. DOOH is a costed alternative for consideration, not a justified selected channel merely because its price is observable. A lean digital/partner learning option remains available. Likewise the combined consumer/account model below tests resource implications; it does not approve two target segments or establish an available local business-account product.

## 3. Conditional funnel, not a performance forecast

| Explicit assumption | Downside stress | Illustrative arithmetic | Upside stress |
|---|---:|---:|---:|
| Search CPC, DKK | 18 | 12 | 8 |
| Social CPM, DKK | 135 | 90 | 65 |
| Social click-through rate | 0.7% | 1.0% | 1.5% |
| Search click → first completed paid ride | 1.5% | 3.0% | 6.0% |
| Social click → first completed paid ride | 0.8% | 1.5% | 2.5% |
| Duplicate proportion of combined attributed acquisitions | 15% | 10% | 5% |
| Eligible first-payer cohort repeating within 90 days | 20% | 35% | 50% |
| Qualified account lead → active paying account | 10% | 25% | 35% |

Additional assumptions: 75% of annual new payers have a full 90-day observation window at year end; each repeater takes three additional rides in that window; an active account produces eight rides/month over six average active months. Leads: 24/60/120 in the lean/middle/expanded cases. These are discovery hypotheses, not a measured demand curve. The same rates across spend levels are a convenience for comparison, **not evidence of linear scalability**.

Middle illustrative arithmetic:

1. Search: 108,000 / 12 = 9,000 clicks; × 3% = 270 attributed first payers.
2. Social: 90,000 / 90 × 1,000 = 1,000,000 impressions; × 1% × 1.5% = 150 attributed first payers.
3. Deduplicate combined acquisitions: (270 + 150) × 90% = **378 first payers**. An install, lead or unpaid booking is not a payer.
4. Retention: 378 × 75% eligible × 35% repeat × three extra rides = **297.675 additional ride equivalents**. Do not include immature cohorts in a real 90-day denominator.
5. Accounts: 60 qualified leads × 25% × eight rides × six months = **720 ride equivalents**. These account rides are assumed disjoint from the consumer attribution cohort; real rider/booking IDs must prevent double counting.
6. Total conditional rides: 378 + 297.675 + 720 = **1,395.675**. Fractional values reflect conditional arithmetic, not actual customers or trips. **No DOOH conversions are invented or added.**

**Measurement contract:** ‘clicks’ means all recorded paid-channel clicks, not unique visitors, sessions or eligible landing-page visits. The conversion assumptions use the channel-attributed first-payer counts **before** cross-channel deduplication: 270/9,000 = 3% for search and 150/10,000 = 1.5% for social. Deduplicated 378 is the combined acquisition total, not either channel's conversion numerator. Ineligible clicks, failed landings and tracking losses are separate diagnostics; they cannot be removed from the headline denominator to improve the reported rate. For example, 270 payers and 4,500 eligible landings still give 3% of 9,000 paid clicks; 6% is a differently named eligible-landing rate, not achievement against a changed 3% model.

**Consumer-only bridge (superseded by the selected plan above):** B2B supplied 720/1,395.675 = 51.6% of the mixed middle case's ride equivalents. Removing only those rides gave 675.675 ride equivalents and −DKK553,987 at 30%, with the DKK54,000 account effort still inside the envelope. The selected S1 allocation removes that effort and reassigns its hours; its funnel result is identical because the reassigned hours receive no conversion credit.

A proposed DKK30 one-time voucher has a maximum of floor(12,000 / 30) = **400 recipients** in the middle envelope. The model uses min(first payers, 400), so illustrative redemption is DKK11,340 and the unused reserve DKK660. Upside conversions do not imply every payer receives a voucher. These proposed terms are not the company's expiring September launch offer. Legal approval, eligibility, abuse controls and company funding are prerequisites to execution.

## 4. Financial challenge and falsification

| Illustrative case | First-payer equivalents | Active-account equivalents | Total ride equivalents | Gross booking-value proxy before incentives | Contribution less full reserved budget at assumed 30% margin |
|---|---:|---:|---:|---:|---:|
| Lean | 144 | 6 | 545.4 | 123,806 | −202,858 |
| Middle | 378 | 15 | 1,395.675 | 316,818 | −504,955 |
| Expanded | 891 | 30 | 3,032.6625 | 688,414 | −993,476 |

Booking value multiplies every ride equivalent by the **standardised DKK227 calculation**, including the account rides. That is a deliberately visible scenario proxy, not actual billed revenue, service mix, average trip length or attributable incremental revenue. A real finance review must replace it with realised net receipts and relevant operating costs. The table subtracts the **full reserved envelope**, including contingency and incentive reserve; it is a conservative funding comparison, not an accrual profit forecast. Incentives are not also subtracted from the contribution proxy, avoiding double counting.

For the middle option:

- Paid-media cost / first payer = 198,000 / 378 = **DKK523.81**. Including modelled redeemed incentives gives **DKK553.81**. Neither is a fully loaded CAC: creative, management, tools and sales/support costs remain outside that numerator. Dividing all programme spend by consumer payers would also misallocate the account route.
- At a hypothetical 30% contribution, DKK227 × 30% = **DKK68.10 per ride**. Covering DKK600,000 requires **8,811 rides** (rounded up), not the illustrative 1,396. At 50%, the threshold is **5,287 rides**.
- Paid media plus the illustrative voucher alone would require about **8.13 rides per new payer** at 30% contribution, before shared overhead. The model's consumer average is only 1.7875 rides per acquired payer within the included window. Do not invent long-term CLV to bridge that gap.
- Middle upside stress produces about 3,691 ride equivalents and DKK837,944 booking-value proxy; at 30% contribution it still leaves about **DKK348,617 below the full envelope**. This is not a profitable best-case forecast.

**Decision implication:** reject a claim that these assumptions justify annual scale. A subsequent group plan could justify a genuinely limited learning investment or a longer-horizon brand objective, but must explicitly accept its cost and validation gates; it cannot relabel this deficit as ROI. Better actual conversion, repeat frequency, account volume, contribution or lower cost would need evidence. No scenario is silently selected here.

## 5. Proposed KPI specification and decision rules

All targets below are **unapproved hypotheses**, not company baselines. Responsibilities are organisational roles, not assignments of group-member work.

| Proposed objective / measure | Exact definition and illustrative target | Data/tool, cadence and accountable role | Interpretation / stop or change rule |
|---|---|---|---|
| Trial by eligible local riders | Unique first-time payers with a completed, settled ride; middle arithmetic 378 over M1–M12 | Company booking/settlement events joined to permitted campaign identifiers; weekly campaign/analytics review | Reconcile refunds, duplicates, new/existing status and geography. Do not optimise on installs alone. Compare observed acquisition cost with contribution-supported limits before raising spend. |
| Improve conversion from paid-channel demand | Channel-attributed first completed paid riders before cross-channel deduplication / all recorded paid-channel clicks; illustrative search 270/9,000 = 3%, social 150/10,000 = 1.5% | Channel click logs + server-side completed/settled booking record, with one stated attribution window and lawful attribution; weekly | Report search/social separately; 378 is the deduplicated cross-channel total. Keep eligibility/landing loss as separately named diagnostics, not exclusions silently changing this denominator. Price, availability or tracking may explain weak conversion; attribution is not causal lift. |
| Repeat use after a credible first experience | First-payer cohort with ≥1 additional completed paid ride within 90 days / first payers with a full 90-day window; illustrative 35% | Pseudonymised booking cohorts; monthly cohort review by CRM/analytics | Exclude immature cohorts rather than calling them churned. Compare offer/non-offer groups only under an approved valid design. No lifetime-value claim from one repeat window. |
| Account sales — **not selected (D-032)** | Retained as record only. Active paying accounts / qualified leads | — | Reopen only if the group changes segment and local account capability is verified. |
| Service integrity before acquisition scale | Proposed internal validation floor: ≥95% of accepted bookings completed; monitor service-caused cancellations separately, with a provisional ≤2% ceiling | Dispatch reason codes and completed rides; daily operations, weekly marketing/operations review | Assumed floors, not industry benchmarks or customer guarantees. Pause geographical expansion if supply cannot meet the internally approved floor. Use a pre-agreed observation window and minimum volume; do not act on a tiny day's percentage. |
| Availability before acquisition scale | Eligible in-area/in-hours service requests receiving a usable offer / all such requests; separately report outside-coverage requests, no-offer requests and customer-declined offers | Aggregate request/dispatch events using distinct request IDs; daily operations, weekly capacity and campaign review | No invented numeric target before baseline and service promise. Join this diagnostic to the completion/economic scale gates: 100% completion of accepted bookings does not establish that most eligible demand received an offer. Lawful data access and an approved minimum observation volume remain prerequisites. |
| Promise/experience consistency | Arrival within the specifically communicated booking window; complaints by reason and post-ride CSAT with response rate | Dispatch timestamps and optional short survey; weekly operations/customer-experience review | Numeric punctuality/CSAT targets require an observed baseline and an approved promise. Do not announce ‘always on time’, guaranteed pickup or superior safety from recruitment statements. |
| Spend control and unit economics | Actual committed + spent marketing cost versus approved envelope; paid acquisition measures separately from allocated full CAC; contribution per net ride | Purchase ledger, media invoices, settlement and operations data; weekly spend, monthly finance review | Reconcile vouchers redeemed/reserved, tax, agency time and refunds. Stop scale if acquisition cost cannot be covered under a defensible contribution/retention horizon. Unknown margin means the economic gate is not passed. |
| Brand consideration — **selected objective (D-032)** | Share of a consistent S1 survey sample in the service area who would consider Green SM for their next taxi trip, before and after activity; same wording and sampling frame | Research lead, baseline in M1–M2 and agreed follow-up | No invented starting awareness or percentage-point lift. Set the target after the baseline and an adequately powered design; platform impressions and DOOH plays are not awareness. |

A future implementation needs a written event dictionary: recorded paid-channel click (not person/session), eligibility/landing diagnostic, attribution window, in-area/in-hours request, usable offer/no offer, booking accepted, completed, settled/refunded, service-caused cancellation, first payer, account ride and mature cohort. Data minimisation, purpose, permissions, retention, direct-marketing rules and processor contracts require local legal review. This research does not grant access to customer data or establish GDPR compliance. Avoid uploading identifiable trip histories into public AI tools.

## 6. Stage-gated resources, not an authorised schedule

For the selected plan, the staged release, gate thresholds and maximum exposure at each gate are set out in `integrated-plan-copenhagen.md` §9–§10. The stages below remain the general rule.

- **M1–M2, if later authorised:** confirm service area and operational capacity, inspect real matched-route fares/terms, obtain supplier quotes, validate event definitions and collect a lawful baseline. Qualitative discovery must not be invented as completed research.
- **M3–M4:** a capped acquisition/account test with distinct channel and service failure diagnostics. Release only a separately approved test amount; this document does not authorise 1/12 of annual spend automatically.
- **M5–M9:** expand only where mature customer/financial evidence and service capacity support it. Re-quote DOOH before using that optional line; do not assign its unmeasured conversions to paid search.
- **M10–M12:** review mature cohorts, account activity, net contribution and resource burden. Do not report late cohorts as 90-day results. Renew, revise or stop against the approved objectives.

Module links: `budget-and-resource-allocation` and `marketing-budget-line-items`; `sales-process` and `selling-techniques`; `kpis-and-metrics`, `customer-acquisition-cost`, `customer-retention-rate`, `campaign-tracking-and-analytics`; `alignment-with-objectives`. Exact teaching locators are in `module-rubric-evidence-map.md`. Segment, positioning, total and objective are decided (D-032). Still for group approval: the proposed line items and channel mix, material assumptions and KPI targets. Actual corporate data/quotes are a separate evidence prerequisite, not information the student is expected to invent.
