# Independent review of the overnight research decision packet

**Review date:** 28 September 2026. **Object:** A1 research and decision support, not a finished poster. **Authority:** the actual A1 rubric and D-021–D-027. No mark is predicted, no group choice is made, and no lecturer endorsement of the strategy is inferred.

## 1. Overall judgement and review contract

The packet makes a defensible **conditional recommendation**, not a demonstrated commercially viable plan. Its strongest features are the distinction between evidence fitness and marks, explicit counterevidence, practical module application, and a financial scenario that exposes losses rather than disguising assumptions as a successful forecast. Two specific correctness issues remain: the conversion denominator is inconsistent between the proposed KPI and the arithmetic; and one marketing-activity reconciliation still calls available VinClub evidence unverified. These should be corrected before the packet becomes the basis of approved wording. Neither justifies changing the frozen weights or automatically rejecting Denmark.

The strongest strategic reservation is more consequential than a citation-format issue: Copenhagen's evidence establishes a difficult customer-acquisition and operating problem, but does not establish that the proposed clarity/service proposition solves it economically. This is a genuine decision and validation condition, not proof that the research failed to finish a poster.

### Locator shorthand

All paths are relative to the workspace root. Line numbers identify the reviewed versions; headings, row names, source keys and PDF pages remain the durable locators if integration shifts lines.

| Alias | File |
|---|---|
| FOCUS | `02_research/business-selection/focus-market-selection.md` |
| INPUT / RESULT | `02_research/business-selection/market-selection-inputs.json` / `market-selection-results.json` |
| INDEX | `02_research/business-selection/market-source-index.json` |
| OPTIONS | `02_research/marketing-plan/segment-positioning-options.md` |
| MAP | `02_research/marketing-plan/module-rubric-evidence-map.md` |
| BUDGET | `02_research/marketing-plan/budget-kpi-scenarios.md` |
| DOSSIER | `02_research/business-dossier/green-sm-company-dossier.md` |
| REC1 | `02_research/perplexity/reconciliation-01-focus-market-screen.md` |
| REC2 | `02_research/perplexity/reconciliation-02-green-sm-marketing-activity.md` |

**Severity:** high = materially misleading recommendation or unsafe factual foundation; medium = a substantive definition/evidence defect that can affect decisions; low = a bounded handover or presentation correction. Judgement calls and operational preconditions are separately labelled, not counted as bugs.

## 2. Ranked correctness findings

### F1 — Medium: modelled conversion and the proposed KPI use different denominators

- **Exact locators:** BUDGET lines 70–72 and 105; `06_workflow/scripts/model_marketing_scenarios.py`, `funnel()`, lines 74–79; `budget-scenario-inputs.json`, `performance_assumptions.illustrative`; `budget-scenario-results.json`, `budgets.middle.performance_cases.illustrative`.
- **Finding:** the model applies 3% to all 9,000 purchased search clicks and 1.5% to all 10,000 social clicks. The KPI instead defines conversion as first completed paid riders divided by **eligible landing-page clicks**. No eligibility/landing-page stage is represented, and the packet does not explicitly assume that every purchased click is an eligible landing-page click. Those are not interchangeable measurement populations.
- **Consequence:** a later dashboard could appear to meet or beat the assumed conversion while producing fewer payers than the budget arithmetic. As a purely illustrative counterexample, 270 payers divided by 9,000 purchased clicks is 3%; the same payers divided by 4,500 eligible landing-page clicks is 6%. This is a denominator example, not observed traffic or a proposed eligibility assumption.
- **Actionable fix:** choose one definition for the cost model and headline KPI. Either use all recorded paid clicks consistently, retaining eligibility as a separate diagnostic, or explicitly show the eligible-landing stage and its assumed/measured count before conversion. Do not invent an eligibility coefficient merely to preserve 378 payers. State whether counts are clicks, sessions or unique people, and distinguish pre-deduplication channel conversions from the deduplicated payer total.
- **Verification after correction:** recompute the middle case and confirm that the denominator named in the KPI is exactly the stage multiplied by its conversion assumption. Exercise a hypothetical case with ineligible/non-landing clicks and ensure the reported rate cannot silently change denominator.
- **Remaining group precondition:** approve the objective and measurement population, not an invented company baseline. Operational event access and lawful attribution remain separate prerequisites under BUDGET line 113.

### F2 — Medium: the marketing-activity reconciliation still understates verified VinClub evidence

- **Exact locators:** REC2 line 56, row “VinClub account linking, VPoint tiers, launch discounts and ecosystem redemption”; REC1 line 107, VN-R11; INDEX source `vingroup-2025b`, claims `VN-LOYAL-01` and `VN-LOYAL-02`; `04_references/vingroup-2025b-xanh-sm-vinclub-lien-ket.pdf`, pp. 2–3.
- **Finding:** REC2 calls these mechanisms “Not yet verified” and refers to related-news teasers. The saved original Vingroup announcement already states 3%/4.5%/6% VPoint accrual for Gold/Platinum/Diamond, trip/ecosystem redemption, and the 20–31 March 2025 linking promotion. I inspected the actual PDF pages. REC1 and the canonical index correctly recognise this bounded evidence.
- **Consequence:** the two reconciliations give incompatible evidence-availability advice. A downstream writer could unnecessarily discard a supported historical loyalty mechanism, repeat acquisition work, or fail to distinguish it from the still-unsupported claims of retention uplift and current applicability.
- **Actionable fix:** split the row: **historical company-announced linking/tier/redemption mechanism supported**; complete operative terms/current status and realised outcomes unverified. Route to the existing key and canonical claim IDs rather than creating a duplicate source. PDF p. 3 directs detailed conditions to the app, so the announcement is not a complete audited contract or proof the offer remains live.
- **Verification after correction:** compare REC2 with REC1 VN-R11 and the two INDEX claims; retain the March 2025 window, corporate attribution and no-outcome qualification. No new web research is necessary for this correction.
- **Remaining group precondition:** none to correct the evidence status. Any transfer of a Vietnamese mechanism to Europe remains an unapproved proposal needing local demand, terms, capacity and economics.

### H1 — Low: complete the live integration handover without rewriting historical checkpoints

- **Exact locators:** OPTIONS lines 9–15; MAP lines 10–14 and 62; DOSSIER lines 7 and 161; REC2 lines 23 and 103. FOCUS line 66 and REC1 lines 22/164 describe the earlier 84-reference comparison checkpoint.
- **Finding:** several files still direct the reader to provisional staging/temporary manifests or describe parent integration as pending. During this review the canonical index gained the company section with `CO-I01`–`CO-I34` and durable evidence IDs. This is a live integration dependency, not evidence that the quoted company facts are fabricated.
- **Actionable fix:** once the parent verification gate is complete, make current routing point to the registry and canonical index. Preserve accurately labelled historical checkpoint counts rather than replacing every historical “84” with a current total. Pack-only research reserves must remain distinguishable from promoted sources.
- **Consequence/precondition:** unresolved routing increases the risk of stale keys entering a draft; group approval is not needed to finish it. This review does not certify the newly added sources' identity-verification state.

## 3. Strategic and measurement cautions — not arithmetic bugs

### J1 — Material decision-readiness caution: the favoured consumer option and the costed mixed route are not the same plan

OPTIONS lines 73–85 favours a concentrated S1 resident-user route and explicitly warns against simultaneous segment launches. BUDGET lines 51 and 74 correctly disclose that its combined model does not select two segments or establish a local account product. Nevertheless, **720 of 1,395.675 middle-case ride equivalents, or 51.6%, come from B2B accounts**. The largest component of the illustrated ride total therefore depends on the conditional S2 capability.

This is honestly labelled, not a false forecast. Before seeking a decision on CPH-1, show a consumer-only bridge beside the mixed illustration and identify which sales/support costs are removed, reassigned or retained. Holding the full DKK600,000 envelope unchanged and removing only account rides gives 675.675 ride equivalents, DKK153,378 booking-value proxy and approximately **−DKK553,987** at the same assumed 30% contribution. That is a stress calculation, **not** a revised recommended budget. It makes the dependency visible without manufacturing B2B availability or changing conversion assumptions.

**Group preconditions:** choose S1 versus an explicitly justified combined/account route; accept a capped learning loss if appropriate; agree the period and funding limit. **Operational preconditions:** actual account booking/payment capability, buyer access, support responsibility, sales-cycle evidence and trip-level deduplication. Vietnam's business sign-up page is not proof these exist in Copenhagen (OPTIONS lines 49–59; DOSSIER line 100).

### J2 — Medium design caution: accepted-booking completion does not measure availability

BUDGET line 108 proposes ≥95% completion of **accepted** bookings and a service-cancellation ceiling. These are useful integrity measures, but they cannot by themselves test whether acquisition traffic can obtain a booking: a service accepting 100 of 1,000 otherwise eligible requests and completing all 100 would show 100% accepted-booking completion. This illustrative example is not a report of Green SM performance.

The packet separately requires capacity checks (BUDGET lines 117–120; OPTIONS lines 45, 77 and 83), so this is not an allegation that it promises unlimited supply. Make the eventual scale gate join those checks explicitly: distinguish outside-coverage requests, eligible requests receiving no available offer, accepted bookings, completion and refunds, with lawful aggregate reporting. Do not invent a numerical availability target before a baseline and service promise are agreed. This protects C3.3/C5 from a denominator that could reward rejecting difficult demand.

## 4. Lens one — local first-marker: explicit module application and practical coherence

This lens uses the supplied rubric, not a speculative lecturer personality. The actual handbook's A1 rubric is at `00_brief_and_criteria/source/mark1286-module-handbook-2026-27.docx`, extracted lines 227–237; its wording matches `rubric.md` Part A, lines 13–19. C3 and C7 each carry 20%, C2 and C4 each 15%, and C1/C5/C6 each 10%. No official criterion-level grade bands were supplied.

All eleven canonical headings occur as exact rows in MAP lines 20–30, checked against `poster-headings.txt`. The mapping does not pretend that a research file earns C7. The useful question now is whether each future panel can show a decision-producing application rather than a theory label, as D-022 requires (`decision-log.md`, lines 119–125).

| Canonical heading | Rubric connection and practical assessment of the packet | Legitimate remaining precondition |
|---|---|---|
| Student/Business Details | MAP line 20 correctly uses confirmed identities/business rather than inventing a marketing concept or contributions; C1/C7.3, R18–R21/R29. | Actual contributions and any group identifier. Agent research is not evidence of each member's effort. |
| Company/Business Introduction | MAP line 21 and DOSSIER §§2–4 connect Vietnamese origin, dated footprint and local operating model to the problem; C1, R30–R33. | Select concise material for one market; preserve Dutch pilot status and dated company facts. |
| Target Market Analysis | OPTIONS lines 32–75 applies segmentation by payer/occasion, then compares consumer, organisation and visitor routes; MAP line 22, C2, R34–R39. This is more useful than a fabricated named persona. | Approve priority and exclusions; demographic, psychographic and behavioural descriptions still need explicit fact/assumption boundaries. “Adult resident” alone is a thin eventual demographic profile, but arbitrary ages/incomes would not improve it. |
| Positioning Strategy | OPTIONS lines 94–101 offers target/benefit/reason-to-believe alternatives and rejection tests; MAP line 23, C2, R40–R42. | Validate customer relevance and comparative delivery. “Clear/local/accountable” is a hypothesis, not yet a proven unique advantage. |
| Branding and Identity | OPTIONS line 103 favours retaining the actual identity; MAP line 24, C2, R43–R46. | Observe/attribute the logo and palette, select an actual message and explain audience fit. Missing final artwork is not a research-packet defect. |
| Digital Marketing Tactics | OPTIONS lines 109–117 gives concrete search/content/social roles and links them to booking; MAP line 25, C3, R47–R49. | Select the actual platform/geography and funded content. National social reach and a seller's DOOH rate card do not justify a buy by themselves. |
| Sales Strategies | OPTIONS lines 111–119 applies lead generation → discovery/prospecting → deliverable paid trial → review; MAP line 26, C3, R50–R54. | Confirm channel and fulfilment capability. The consultative sequence is correctly labelled the agent's application, not a fully specified module framework or existing local corporate programme. |
| Budget and Resource Allocation | BUDGET lines 23–51 supplies quantities, hours, currency, period and a reconciled table; MAP line 27, C4, R55–R59. | Resolve J1, actual supplier/tax/resource assumptions and acceptable learning cost before adopting an envelope. A table that sums is not sufficient feasibility evidence. |
| Measurement and Evaluation | BUDGET lines 102–113 joins objectives, definitions, tools, cadence and response; MAP line 28, C5, R60–R65. | Correct F1; join availability to the service gate; select targets rather than describing hypothetical values as historical baselines. |
| Creativity and Innovation | OPTIONS lines 129–138 explains personalisation/omnichannel mechanisms and reasons to defer AI/subscription/neuromarketing; MAP line 29, C6, R66–R67. | Select a feasible mechanism with resource and measurement consequences. Consideration/deferment is the packet's reasoned interpretation, not a fabricated lecturer waiver of the brief's trend wording. |
| Alignment with Business Objectives | MAP line 30 and lines 58–60 make the causal chain explicit; BUDGET lines 89–96 challenges its economics; C5 and cross-panel coherence, R68–R70. | Approve a commercial/learning objective consistent with stable local operations, not automatically “rapid growth”. |

The module checks matter. `03_course_materials/extracted/w04-lecture.md`, slides 6–9, actually teaches STP, branding and lead generation/prospecting/conversion; `w04-tutorial.md`, slide 7, names consultative/value-based selling. Slide 10 defines CAC as including marketing and sales effort and retention broadly as customers returning. Therefore the packet is right to call DKK523.81/553.81 **paid-acquisition measures rather than full CAC** (BUDGET line 91), and its explicit mature 90-day repeat-purchase cohort is a defensible application of this module's retention wording. A generic external formula or compulsory fictional persona should not be imposed as if it were the rubric.

## 5. Lens two — UK moderation: evidence, definitions and overclaim control

### Frozen-anchor comparability

The score arithmetic independently reproduces Denmark **92.5**, Hanoi **88.5**, Amsterdam **84.5**, Delhi **76.0** from INPUT. These are evidence-fitness indices, not marks. FOCUS lines 5, 13–17 and 92 correctly attribute the thresholds/half-points to the agent and deny statistical calibration. The saved 57-run result reports 54 Danish raw wins, one Vietnamese win and two ties; the preference rule choosing Denmark in all 57 is not 100% confidence. The joint stress can favour Vietnam (FOCUS lines 98–102; RESULT `joint_stress_cases_excluded_from_majority_rule`).

- **K1 — judgement, not demonstrated scoring bug:** Copenhagen's 4.5 relies on city demographics, national travel/attitude evidence and a small regional app-choice subgroup; Hanoi's 4.5 relies on multi-city/national commercial surveys. Both lack a representative chosen-city target. The Danish 79 respondents specifically answered why they used Uber/Bolt/TaxiToGo rather than a classic dispatch office, not why all Copenhagen residents choose taxis. Preserve that narrower question when compressing INDEX `DK-I07` or OPTIONS line 21. REC1 DK-R2 states it most precisely. Amsterdam has more direct municipal context but lacks the taxi-choice survey; Delhi's local study is older. These differences justify debate about half-points, not an invented universal population equivalence (FOCUS line 85; INDEX `IN-GS-01`, `VN-QME-01`).
- **K2 — bounded rather than falsely precise:** FOCUS line 86 separates supply counts, historical revenue ranges, recent usage and opaque market estimates. A registered taxi is not an active vehicle or a trip; app use/MAU is not exclusive market share; GMV is not company net revenue. No new common-denominator market-size comparison should be manufactured to make the countries look commensurable.
- **K3 — the most contestable availability judgement:** the frozen 5-anchor requires fares, own terms and a published channel-cost **or volume** benchmark (FOCUS line 27). Denmark's genuine DOOH card satisfies an availability reading, but not the paid-search/social economics of the favoured route. Vietnam also has company volume claims, discounted fare observations and membership terms, yet receives 4.5 because those are less usable/current/local (FOCUS line 87). That is reasoned judgement, not an arithmetic defect; explicitly defend **fitness of the benchmark**, not merely the number of PDFs. Dutch 4.5 is similarly generous when its own numeric fare is missing. Do not revise weights or thresholds after the fact to force a European winner.
- **K4–K6 — attractive story is not delivered customer value:** the competition authority supplies an unusually concrete Danish challenge, but its company-model passages still originate with Green SM. Its assessment of marketing/network barriers is independent analysis. Existing Vietnamese mechanisms make K5 plausible; neither a corporate mechanism nor the European-entry story proves results or C7 quality (FOCUS lines 88–92).

The recorded eight-market screen was not eight equal-depth audits (FOCUS lines 36–60; REC1 lines 7–9). Four-finalist evidence collection and source-discovery differences remain a limitation. This review did not independently authenticate the historical “frozen before scoring” timing; it assessed consistency with the saved frozen specification.

### Claim boundaries retained successfully in the inspected scope

1. **Tariff and wage:** the Danish product PDF p. 3 really separates Day (Min)/Night (Max) meter charges from higher app maxima and a holiday time charge per hour. The DKK227 example is a calculation, not an app transaction or average fare. Driver recruitment p. 3 really says base salary **from** DKK185/hour in the initial employee model; it is neither fully loaded operating cost nor the assumed DKK600 marketing-professional rate (BUDGET lines 16–21; DOSSIER lines 79 and 111–121).
2. **Source independence:** REC1 line 139 and DOSSIER line 145 correctly reject counting corporate releases and their reproductions as separate confirmation. Q&Me and Rakuten have distinct restricted samples; Decision Lab's landing page and blog are one study. The accessible Indian complaint is an allegation, not proven breach or representative pay evidence (DOSSIER lines 138–145; REC2 lines 85–99).
3. **First and green claims:** the accepted first is **Green SM's own** first European entry. Neither that wording nor Vietnamese origin proves a first Asian/Vietnamese taxi operator in Europe. Amsterdam already has an electric-comfort rival. Precise direct-tailpipe wording does not establish lifecycle neutrality or that displacing walking/public transport improves emissions (OPTIONS lines 22, 26 and 138; DOSSIER lines 68 and 130).
4. **Privacy and capability:** the proposed use of preferences/minimal identifiers, no inferred sensitive traits and no driver-camera marketing is appropriately bounded; it is not a GDPR compliance opinion. No employer trip-data sharing, local B2B integration, airport entitlement or public-AI upload of identifiable journeys is authorised (OPTIONS lines 57, 69 and 131–138; BUDGET lines 107 and 113). Private-data access is a future lawful organisational prerequisite, not a task for the student to supply during this research.

## 6. Strongest counterargument to Denmark

The best argument against the recommendation is not that Europe lacks data. It is that **good evidence of an obstacle can be mistaken for good evidence of a solution**. The Danish authority documents a new entrant facing entrenched apps, network effects, driver/customer acquisition barriers and substantial marketing investment (saved decision pp. 150–151 and 174–179). Its 79-person choice subgroup puts price ahead of the proposed clarity/service benefit; it does not establish that the chosen resident segment values a new provider's proposed resolution route enough to switch or return. Competitors already offer usable booking features, and the company-controlled employee model is an input, not measured superior service.

The scenario then fails to finance itself even while assuming an account contribution not established as locally available. Hanoi offers stronger direct Green SM customer-experience evidence and existing loyalty/distribution mechanisms, albeit with city/sample and disputed-share qualifications (Q&Me pp. 1–2; REC1 VN-R3–R6/VN-R11). A group prioritising a demonstrable retention intervention over an entry narrative could reasonably prefer it. The four-point base gap is fragile to a Danish K1 downgrade; joint K1/K3 judgement changes reverse the preference (FOCUS lines 98–101).

**Response that is defensible:** Denmark remains a conditional evidence-led choice if the group wants a tightly scoped, explicitly loss-limited learning/market-development problem and accepts the operational validation gates. **Response that is not defensible:** “92.5 proves the market is profitable, the service is distinctive, or the poster will earn a particular mark.” No re-engineering of weights is needed to preserve this distinction.

## 7. Financial assessment

This is **not a pretty fake success forecast**. BUDGET labels the envelopes and funnel assumptions, excludes unverified DOOH conversions, caps incentives, distinguishes gross booking-value proxy from revenue/profit, and reports negative results even in the middle upside case (lines 3–21, 66–96). Actual source-page inspection confirmed the DKK191 DOOH CPM, DKK4,995 setup, five motifs and VAT/production exclusions. All three saved allocations sum to their totals and 100%; independent arithmetic gives DKK38,200 for 200,000 impressions, DKK227 for the standardised trip, DKK316,818.225 middle booking-value proxy and −DKK504,954.53 at the assumed 30% contribution less the full envelope.

That is useful falsification, but it does not itself pass C4's feasibility requirement. The source-derived inputs price a meter illustration and an optional outdoor inventory; CPC, social CPM/CTR, conversion, deduplication, repeat behaviour, account demand and margins remain explicit assumptions. Contingency and incentive reserve are conservatively charged in full, not actual accrued spending (BUDGET line 87). Full CAC, realised net receipts, marginal service cost, actual available support hours and contribution-supported scale remain unestablished. F1 and J1 should be resolved before one scenario is attached to an approved segment.

## 8. Own checks and unreviewed limits

### Direct saved-PDF spot checks

These were **local `pdftotext -layout` page extractions**, not reliance on prose summaries and not a new website visit. All paths below are in `04_references/`.

| Saved PDF / pages inspected | Result relevant to this review |
|---|---|
| `konkurrence-og-forbrugerstyrelsen-2026b-uber-dantaxi-afgoerelse.pdf`, 43–44, 150–151, 174–179 | Confirmed national n=1,005 methodology/recall qualification; 79-person particular app-choice question; company-attributed fleet model; potential versus active capacity; independent acquisition/scale challenge. Did not treat the whole 357-page decision as audited. |
| `green-sm-denmark-aps-ndb-green-sm-car.pdf`, 3 | Confirmed meter/app/holiday distinctions and existing 30-day scheduling claim. |
| `afa-decaux-2026-prisliste.pdf`, 3 | Confirmed 41-screen Digital Copenhagen, CPM191/setup4,995 and exclusions; not a platform CPM or a committed quote. |
| `green-sm-denmark-aps-nda-driver-recruitment.pdf`, 3 | Confirmed advertised base pay and initial employee-model wording, not actual earnings. |
| `q-and-me-nd-car-ride-hailing-usage-habits-2024.pdf`, 1–2 | Confirmed satisfaction figures and 600 weekly car-app users aged 22–55 in four localities; no Hanoi-only probability sample. |
| `ngo-nd-vietnams-digital-dynamics-q4-2025.pdf`, 3 | Confirmed 65%/61% is past-three-month car usage, not revenue share; retained Grab's feature/performance strengths. |
| `vingroup-2025b-xanh-sm-vinclub-lien-ket.pdf`, 2–3 | Confirmed historical mechanism underlying F2; detailed conditions directed to app; no measured uplift. |
| `stultiens-2026-uber-elektrische-premiumrit.pdf`, 2 | Confirmed Amsterdam/Rotterdam Comfort Elektrisch competitor report; electricity/comfort is not exclusive. |
| `ramos-2025-emission-free-zones-amsterdam.pdf`, 1 | Confirmed implementation account says taxis follow passenger-car rules; an older taxi proposal is not proof of an enacted 2025 mandate. |
| `bl-mumbai-bureau-2026-green-sm-india-bet.pdf`, 4 | Confirmed company refusal to confirm circulating pre-launch prices; INR8/km is not an accepted standard tariff. |

Read the complete substantive sections of FOCUS, OPTIONS, MAP, BUDGET, DOSSIER and both reconciliations, the market/budget inputs, selected canonical claim entries and saved result summaries, the actual A1 handbook rubric, requirements R29–R92 and relevant people/format rows, and D-021–D-027. Examined `analyse_market_selection.py`'s evaluation/analysis functions and the scenario `funnel()` function for the definitions relevant to this report. Performed read-only arithmetic and exact-heading membership checks; no implementation/shared document was edited, and no build, formatter, test suite or registry-verification run was performed.

**Limits:** this is not an independent audit of every PDF, every source-index quotation, all four full evidence packs, all raw Perplexity inputs, reference formatting or the reference-verification implementation. Newly integrated company claims were not all independently reopened; current registry identity clearance belongs to the separate verification pass. No claim is made to have checked live app quotes, actual service availability, private data, buyer willingness, legal compliance, authentic member contributions, an A0 proof, upload packaging or rehearsal. Extracted source text does not prove visual poster legibility. No blanket “no issues” clearance follows beyond the stated checks.

## 9. Group decisions versus evidence work

**Reserved to the group:** one focus country/city/service, priority segment, position and desired proof, brand/message, planning period, channel mix, budget/risk appetite, acceptable learning loss, targets, final wording/design and actual contribution statements (D-027, `decision-log.md`, lines 149–153; OPTIONS line 150).

**Reachable without a group decision:** correct F1/F2; complete H1's canonical routing after verification; present J1's consumer/mixed-route bridge; preserve J2's availability distinction and evidence limitations. These are research-quality improvements, not covert adoption of a market or campaign.

**Not failures of this overnight deliverable:** absent final poster, unapproved segment/budget, missing artwork, unperformed interviews, undisclosed private company margins and unconfirmed member contributions. They remain approval, evidence or production gates. D-021 records only student-relayed lecturer agreement to the AI-made hand-drawn-style route; it does not approve the marketing strategy or guarantee C7 quality. D-022 still requires explicit analytical application in the eventual poster without relying on the pitch to rescue missing reasoning.

## Parent resolution addendum — 28 September 2026

The independent findings above are preserved; this section records subsequent changes and exercised checks.

| Item | Resolution |
|---|---|
| F1 | Model and headline KPI now use all recorded paid-channel clicks, with pre-deduplication channel first-payer numerators. Eligible landings are separately named diagnostics. Actual arithmetic: search 270/9,000 = 3%; the same 270/4,500 eligible landings = 6% is explicitly a different measure, never a silently improved headline rate. Combined 378 remains the deduplicated payer count. |
| F2 | Reconciliation 02 now recognises `vingroup-2025b` pp. 2–3 / `VN-LOYAL-01/02`: historical tiers, redemption and the 20–31 March 2025 promotion supported; full/current terms, continued availability and realised uplift still unverified. No duplicate source or new research was needed. |
| H1 | Canonical registry/index/E-ID routing completed across dossier, options, map, reconciliations and pack integration notices. The earlier 84-source comparison checkpoint remains labelled historical. Current collection: 97 candidates; index: 167 claim rows, including 34 additional company passages and two existing Danish-offer passages; ledger: E-001–E-181. |
| J1 | Added a consumer-only bridge, not a new adopted budget. Executing the existing model with account leads set to zero and all costs retained gives 675.675 ride equivalents and −DKK553,986.5325 at 30% contribution. DKK54,000 account/partnership effort remains in that stress; a genuine S1 allocation must remove or justify reassignment before approval. |
| J2 | Added eligible-request → usable-offer availability diagnostics, distinguishing outside-coverage/no-offer/declined/accepted/completed stages. No availability target invented. Availability, completion and economics now jointly govern the proposed scale gate. |
| Additional consistency | Module map now says DOOH prices are not paid-social CPM, rather than incorrectly implying DOOH is not digital. It also respects D-026's settled ‘no group number’ answer. The Danish 79-person question is explicitly scoped to choosing Uber/Bolt/TaxiToGo over a classic dispatch office. |

The strategic objections are **not resolved by wording**: differentiated value, actual service capacity, local account capability, willingness to pay and viable contribution economics still require evidence. They remain visible rejection/approval conditions. No market, segment, budget, target, final copy or contribution statement was adopted.
