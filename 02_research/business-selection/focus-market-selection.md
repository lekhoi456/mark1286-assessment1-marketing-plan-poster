# Focus-market selection: which Green SM market does the plan cover?

Status: **method frozen on 27 September 2026, before scoring; source-verified comparison completed on 28 September 2026**. Recommendation remains unapproved. Scores assess evidence fitness for an A1 plan, **not predicted academic marks, commercial attractiveness or probability of success**.

Decision owner: the group (D-023, D-027). The group expressed a preference for Denmark/Netherlands conditional on evidence. The numerical weights, gates, five-point margin and two-point tie rule below are the **agent's operationalisation**, not thresholds expressly approved by the group. This attribution correction does not change the pre-scoring method or numerical rules.

## 1. Question and rule

Which of Green SM's eight markets best supports a source-backed, analytically defensible plan under C1–C7, within the available evidence?

Group preference (D-023): Denmark or the Netherlands, unless their data are insufficient or another market supports a stronger plan. Agent operationalisation, saved before scoring:

1. **Data gate for a European choice.** A European candidate passes only if it scores at least 3 of 5 on K1 (customer evidence) and on K3 (budget and KPI grounding). If neither passes, rule (a) applies.
2. **Margin rule.** Take the higher-scoring eligible European candidate, subject to the tie rule. If no other market beats it by **more than 5 points** out of 100, recommend the European market. If another market beats it by more than 5 points in the base case **and** in most sensitivity runs, recommend that other market. Recommendation is not group adoption.
3. **Between Denmark and the Netherlands**, the higher weighted score wins; if they are within 2 points, the tie-break is K1, then K3.

The five-point margin is a conservative decision convention for ordinal judgements, **not a statistically calibrated error bound**. An uncertain score can move by approximately one point in the stress tests; simultaneous errors can exceed five weighted points. Report the raw ranking separately so the European preference remains visible.

## 2. Criteria and weights (frozen)

Each criterion is scored 1–5 from verified evidence (saved PDF, logged claim). Leads that are not yet verified may inform the stage 1 screen only, and are marked as leads.

| ID | Criterion | Weight | Rubric link | Score 1 | Score 3 | Score 5 |
|---|---|---:|---|---|---|---|
| K1 | Customer evidence: recent, method-disclosed data to describe target segments demographically, psychographically and behaviourally in the focus city | 25 | C2 (15%), feeds C3 | Almost none; would rely on assumptions | Official demographics plus one behavioural or attitudinal source with disclosed method | Official demographics, a travel or usage survey and an attitudinal survey, each with disclosed sample and year |
| K2 | Market and competitive context: market structure, named competitors and their offers, usage volume or size, regulation | 20 | C1 (10%), C3 (20%) | Competitors and rules unclear | Competitors and main rules documented; no size or volume | Competitors, rules and a usage volume or size figure, all verified |
| K3 | Budget and KPI grounding: verifiable fares or tariffs, Green SM's own offer and promotion terms, media or channel costs, volumes for realistic targets | 20 | C4 (15%), C5 (10%) | Every number would be an assumption | Fares and Green SM terms verified; channel costs assumed | Fares, Green SM terms and at least one published channel-cost or volume benchmark verified |
| K4 | Clarity of the marketing problem: a current, specific challenge for Green SM that a 12-month plan can answer and that serves company objectives | 15 | C3, C5, Alignment | Vague or already solved | Clear challenge, limited evidence on Green SM's position | Clear, evidenced challenge (for example launch or scale-up against named incumbents) with company objectives on record |
| K5 | Emerging-concept fit: credible use of AI, personalisation, omnichannel, subscription or membership, sustainability, grounded in the market's conditions | 10 | C6 (10%) | Trends would be decorative | Two trends plausibly apply | Several trends apply and the market context (regulation, EV adoption, digital habits) makes them matter |
| K6 | Distinctive, verifiable story for the markers (for example a first European entry) | 10 | C1, C7 | Nothing distinctive | Distinctive but partly unverified | Distinctive and verified in saved sources |

Weighted score = sum of (weight × score ÷ 5), out of 100.

## 3. Procedure

- **Stage 1 screen (all eight markets):** score from verified evidence where it exists and from Perplexity leads otherwise (marked "lead"). Purpose: find whether any non-European market is a serious contender. Output: screening table.
- **Stage 2 (finalists):** Denmark, the Netherlands and the strongest non-European contender(s) from stage 1. Evidence packs gathered and verified at source: `02_research/market-analysis/<market>-evidence-pack.md`, PDFs in `04_references/`, claims in `02_research/evidence-log.md`. Green SM's own pages are captured through Comet (D-025).
- **Sensitivity:** each weight moved ±20% of its value with the others renormalised; equal weights; each uncertain score moved ±1. Report the winner, the margin and any rank reversal.
- **Result and recommendation:** apply the rule in §1; state what evidence would change the result.

## 4. Stage 1 screen (27 September 2026)

Basis: Perplexity leads (`02_research/perplexity/prompt-01-result.md`, `prompt-02-result.md`), not yet verified, plus the company facts already verified (E-001 to E-014). Scores here only decide which markets go to stage 2; they are not the result.

| Market | K1 (25) | K2 (20) | K3 (20) | K4 (15) | K5 (10) | K6 (10) | Screen score | Main reason |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Vietnam | 5 | 5 | 4 | 5 | 5 | 3 | **92** | Several surveys with disclosed samples (leads: Rakuten n = 7,436; TGM n = 558), share estimates, published fares and memberships; a clear usage gap against Grab |
| India | 4 | 4.5 | 2.5 | 4 | 3.5 | 3.5 | 74 | TGM survey (lead, n = 860), aggregator rules, app-usage estimates; Green SM fares unconfirmed |
| Netherlands | 2 | 3 | 3 | 5 | 4 | 4 | 65 | Pilot-to-launch problem is sharp; leads found no consumer survey or market size; Amsterdam zero-emission taxi policy (lead) |
| Denmark | 2 | 3 | 3 | 4.5 | 3.5 | 5 | 64.5 | First European market (verified, E-008); driver cost verified (E-011); leads found no survey or market size |
| Indonesia | 2 | 4 | 3 | 4 | 4 | 2.5 | 63 | Market estimates and a duopoly; no survey with disclosed sample |
| Philippines | 2.5 | 3 | 3 | 3.5 | 3 | 2.5 | 58 | One purposive survey (n = 401); no market value |
| Kazakhstan | 1 | 2 | 2.5 | 3.5 | 3 | 3 | 45.5 | No market size, no survey |
| Laos | 1 | 2 | 2 | 3 | 3 | 2 | 40 | Forecast only; no survey |

Reading the screen:

- The leads understate Denmark and the Netherlands on K1 and K3, because the Perplexity prompt did not ask for official European statistics (national travel surveys, statistics offices, Eurobarometer, regulated taxi tariffs). Stage 2 tests this directly.
- Vietnam (+27) and India (+9) are more than 5 points above the better European market on leads, so both go to stage 2 as non-European contenders. Indonesia is not more than 5 points above and does not go forward; the Philippines, Kazakhstan and Laos are well below.
- **Stage 2 finalists: Denmark, the Netherlands, Vietnam, India.** Evidence packs: `02_research/market-analysis/{denmark,netherlands,vietnam,india}-evidence-pack.md`.

## 5. Stage 2 scoring

### 5.1 Evidence boundary

Four finalist packs were checked against saved PDFs, with 67 selected country sources promoted into `04_references/` alongside the 17 existing business sources. `market-source-index.json` maps **131 selected claim rows** to final keys, PDF pages, exact text or explicitly labelled visual chart transcriptions, scope and limitations. Registry identity verification succeeded for all 84 entries at this comparison checkpoint: 72 automatic matches and 12 explicitly audited manual identity acceptances for logos, API tables or attribution outside the first two pages. Manual exceptions retain the automatic mismatch and are bound to the PDF bytes and bibliographic identity; they do not validate claim meaning.

Geographical comparison: Copenhagen, Amsterdam, Hanoi and Delhi NCT, with national/regional context qualified. Delhi NCR is not one jurisdiction. Hanoi is not allowed to inherit an unqualified two-city/nationwide evidence advantage. All four retain city-level customer and operating-data gaps.

### 5.2 Finalist scores — agent judgements, not marks

| Market / focus city | K1 (25) | K2 (20) | K3 (20) | K4 (15) | K5 (10) | K6 (10) | Weighted evidence-fitness score |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Denmark / Copenhagen** | 4.5 | 4 | 5 | 5 | 4.5 | 5 | **92.5 / 100** |
| Vietnam / Hanoi | 4.5 | 4.5 | 4.5 | 4 | 5 | 4 | **88.5 / 100** |
| Netherlands / Amsterdam | 4 | 4 | 4.5 | 4.5 | 4.5 | 4 | **84.5 / 100** |
| India / Delhi NCT | 3.5 | 4 | 3 | 4.5 | 4 | 4.5 | **76.0 / 100** |

Both European candidates pass K1/K3 ≥ 3. Denmark leads Amsterdam by eight points and Hanoi by four points. The raw ranking already favours Denmark; the preference margin is not what creates its base-case lead.

### 5.3 Criterion-by-criterion reasons and counterevidence

| Criterion | Copenhagen | Amsterdam | Hanoi | Delhi NCT |
|---|---|---|---|---|
| **K1** | 4.5: official city demographics; DTU 2024 travel survey, n = 11,686; KFST 2026 taxi-user survey, n = 1,005; Eurobarometer 2025, n = 1,004. The particularly relevant Capital Region app-choice subgroup is only n = 79. No local willingness-to-pay study: not 5. Sources: `statistics-denmark-2026b`; `christiansen-anderson-2025`, p. 2; `konkurrence-og-forbrugerstyrelsen-2026b`, pp. 44, 150–151; `european-commission-2025a`. | 4: strong municipal demographics/travel and disclosed climate surveys, but no recent taxi-customer study. Municipal ODiN 2023 travel mix and climate sample n = 1,660 are not ride-hailing preferences. `gemeente-amsterdam-2026`, pp. 23, 27, 47; `european-commission-2025b`/`2025c`. | 4.5: official 2025 population/income; Rakuten n = 7,436 across five cities, TGM n = 558 nationally, Q&Me n = 600 frequent car users across four locations. None supplies an independently representative Hanoi-only target segment. `national-statistics-office-2026`; `rakuten-insight-2025`; `tgm-research-2025`; original Q&Me saved in the pack. | 3.5: official 2011-based population projection, not a recent census; national TGM 2025 fieldwork n = 860; Delhi empirical study n = 530 but 2021 fieldwork. Useful disclosed methods, weak recency/geographical alignment. `national-commission-on-population-2019`; `tgm-research-2026`; `gupta-sinha-2022`. |
| **K2** | 4: unusually strong official competitor/rule evidence, historical revenue-share ranges and current licence listing. However, absolute market value/trips are redacted or missing; registered taxis are supply, not usage volume. `konkurrence-og-forbrugerstyrelsen-2026b`, pp. 134, 174–179; `faerdselsstyrelsen-nd`; `statistics-denmark-2026c`. | 4: named incumbents, operator/driver rules and regulated street-hail/rank ceilings. Taxi-monitor fleet/cards/firms are national supply. No verified Amsterdam usage market size or reliable current Uber share. `ilt-ndb`, `netherlands-enterprise-agency-nd`, `rijksoverheid-nda`/`ndb`. The 2023 zero-emission taxi plan is not enacted 2025 law. | 4.5: offers/rules and market estimates available, but Mordor methods are opaque and earlier shares were challenged by Grab. Usage, car-only GMV and all-vehicle market estimates cannot be mixed. Current Decree 158/2024 is partially amended. `mordor-intelligence-nd`, `minh-khanh-2025`, `government-of-vietnam-2024`, `bao-chinh-phu-2026`. | 4: current entrants and Delhi's notified 2023 scheme documented, with NCR policy context. National app monthly users are not Delhi ride shares or revenue. BluSmart is a suspended/historical comparator. National 2025 guidelines are not automatically Delhi law. `transport-department-gnctd-2023`, `press-information-bureau-2025`, India pack §§3–4. |
| **K3** | 5 under the availability anchor: own meter tariffs and separate app maxima, competitor tariff, driver terms and genuine local DOOH list costs. `green-sm-denmark-aps-ndb`, p. 3; `taxa-4x35-nd`, p. 4; `afa-decaux-2026`, pp. 3–4. **No actual app quote, paid-social benchmark, conversion rate, margin or operating capacity is supplied.** This score is not a finding that a proposed budget is feasible. | 4.5: public tariffs, pilot terms and a local outdoor price example provide useful grounding. Own numerical fare remains unverified; One Media excludes printing/design, and no usable acquisition-cost baseline exists. `rijksoverheid-ndb`; `one-media-nd`; `green-sm-2026a`; local product PDF. | 4.5: saved Hanoi fare examples, membership terms and company volume claims. Mutable fare article and national cumulative volume are imperfect planning inputs; no sound current local paid-media cost benchmark. Comet fare/membership captures and `vingroup-2025b`, p. 3. AdCostly excluded. | 3: launch/offer terms and an attributed individual fare observation provide limited grounding; no current standard Green SM tariff or credible channel-cost benchmark. INR8/km is unconfirmed; June launch discount expired. `green-sm-2026b`, p. 5; India pack K3. |
| **K4** | 5: authority explicitly identifies the marketing-investment/awareness obstacle; company prioritises stable local operation before rapid expansion. `konkurrence-og-forbrugerstyrelsen-2026b`, pp. 175, 179; `green-sm-2026d`, p. 3. No fabricated awareness or repeat-use baseline. | 4.5: precise pilot-to-launch learning problem and limited initial districts; less independent assessment of its operating position. `green-sm-2026a`, pp. 1–4. A press-release-based report is not independent evidence of actual uptake. | 4: defensible retention/service-differentiation problem, but **not** the stage-1 claim that Xanh SM necessarily trails Grab in cars. Latest public Decision Lab car-use figures are 65% versus 61%; overall brand usage is another measure. `decision-lab-nd`, `ngo-nd`. | 4.5: premium new entrant, integrated service claim, airport/corporate ambitions and reported driver-payout concerns make a specific but risky execution problem. Targets such as 10,000 vehicles or intended sales mix are not outcomes. India pack K4; company launch and independent reports. |
| **K5** | 4.5: EV, payment and digital context supports service-oriented personalisation/omnichannel; local membership demand untested. `acea-2026`, p. 4; `jensen-helinck-2026`, pp. 3–4; `kemp-2025a`. Environmental attitudes do not imply electric-taxi willingness to pay. | 4.5: strong digital/EV context and local climate evidence; an electric service alone is not distinctive against Uber Comfort Elektrisch. Subscription willingness and local data permissions unverified. `kemp-2025c`, `acea-2026`, `stultiens-2026`. | 5: existing voucher memberships, business/airline channels and mobile use provide several concrete adaptation opportunities. No assumption of automatic renewal or measured loyalty lift. Current/historical Comet captures, `kemp-2025d`, `vingroup-2025b`. | 4: digital booking, EV policy and premium service make several concepts plausible; charging, operational constraints and customer/privacy validation limit readiness. `kemp-2025b`, Delhi scheme and India pack K5. |
| **K6** | 5: verified **Green SM's own first European entry**, independently discussed and assessed. `kjaergaard-2026`, p. 2; company launch; KFST decision. No ‘first Asian taxi in Europe’ claim. | 4: distinctive Amsterdam pilot/local adaptation, but second European entry and independent reporting largely repeats the release. Company pilot/source pack. | 4: distinctive Vietnamese-origin electric/hybrid-model scale and loyalty ecosystem, with a less novel entry story. Specificity matters, not nationality stereotypes or an assumed marker preference. | 4.5: seven-seat premium electric entry and integrated model provide a specific comparison; no unsupported first-entrant or guaranteed BluSmart-replacement claim. |

Half points reflect mixed evidence against the fixed anchors; no formal scoring reliability or independent statistical calibration is claimed. C7 still depends on a real poster, legibility and group contribution: no country dataset can satisfy it.

## 6. Sensitivity

Reproduce: `python3 -B 06_workflow/scripts/analyse_market_selection.py`. Inputs: `market-selection-inputs.json`; full outputs: `market-selection-results.json`. The script changes each weight by ±20%, keeping that changed weight fixed and renormalising the others to 100; adds equal weights; then changes each country/criterion score by ±1 within 1–5. Four already-maximal upward changes are excluded as no-op duplicates: **57 effective runs** = 12 weight + 1 equal-weight + 44 score runs.

- **Raw ranking:** Denmark alone leads 54 runs; Vietnam leads one; Denmark/Vietnam tie in two. Denmark's K1 downgrade from 4.5 to 3.5 yields **87.5 versus Hanoi 88.5**. K2 or K3 downgrades produce a tie at 88.5. These reversals are reported, not hidden by the preference.
- **Preference-rule result:** Denmark remains the per-run recommendation in all 57, because no non-European lead exceeds five points. This is deterministic scenario counting, **not a 100% confidence estimate**.
- **Weight-only/equal-weight margin over Hanoi:** 3.3–5.0 points. Equalising K6 at 3 for every country still leaves Denmark ahead, **88.5 versus 86.5**: its base advantage is not only the ‘first Europe’ story.
- **Joint stress exposes fragility:** reduce Denmark K1 to 3.5 and K3 to 4, while raising Vietnam K3 to 5: Hanoi **90.5**, Amsterdam **84.5**, Copenhagen **83.5**. The per-run preference then changes to Vietnam. This supplementary test is not included as an extra vote in the frozen majority rule.
- Simultaneously moving every score ±1 gives broad overlapping bounds: Denmark 72.5–100; Vietnam 68.5–100; Netherlands 64.5–100; India 56–93.5. These are **not confidence intervals** and cannot establish statistically significant superiority.

## 7. Result and conditions

**Agent recommendation: Denmark, with Copenhagen as the focus city. Chosen on 28 September 2026 (D-031).** Best available basis: a current, independently assessed acquisition/scale problem, disclosed customer research, usable own-fare/resource evidence and an actual local media price anchor. It is a stronger evidence package for a defensible plan, not a promised distinction grade or a commercial investment recommendation.

Keep **Hanoi as the strongest fallback**, not Amsterdam by default. Amsterdam remains a viable European alternative if pilot learning is the group's chosen strategic problem. India's tariff/channel-cost and jurisdictional gaps make it the weakest of these four for this particular evidence-led assignment.

Reopen the recommendation if (1) decisive Danish customer evidence proves inapplicable to the chosen segment; (2) the actual service area/capacity cannot support the proposed campaign; (3) tariff/offer or media evidence fails current verification; or (4) a genuinely Hanoi-specific customer study and credible local acquisition-cost evidence strengthen Vietnam enough to change several scores. Recompute with logged new inputs, not silently adjusted weights.

**Independent-review challenge:** good evidence of an acquisition barrier is not evidence that the proposed service-clarity benefit solves it. The small price/habit subgroup does not establish willingness to switch or pay for that benefit. The later budget/KPI packet tests three unapproved envelopes across nine performance combinations; all fail the assumed contribution break-even, including the mixed model's unverified local B2B contribution. A consumer-only stress is weaker still. Copenhagen is therefore a conditional case for a tightly scoped, explicitly loss-limited learning problem—not a validated scalable campaign. If the group instead wants a better-established retention mechanism, Hanoi is a defensible alternative. Do not change frozen weights to disguise this trade-off.

Next decision packet: `../marketing-plan/segment-positioning-options.md`, `../marketing-plan/module-rubric-evidence-map.md` and the separately labelled budget/KPI scenarios. None constitutes an adopted market, segment, position, budget or final poster text.
