# Overnight reference and model review — 28 September 2026

Scope: A1 only; English (UK); reference-verification code, market-selection arithmetic and conditional marketing-budget arithmetic. Recommendations and scenario choices remain unapproved. No code, shared data or generated deliverables were changed. No tests, verification commands, builds or formatters were executed.

## Decision summary

**Two high-severity correctness barriers remain in cached reference verification.** The manual-acceptance branch itself is appropriately narrow, but an automatic PDF match bypasses freshness checks, and the independent Crossref gate trusts old differences after bibliographic changes. Neither finding alleges that the current live registry contains an incorrect source; both identify a concrete edit path that the consumers would incorrectly accept.

No arithmetic defect was identified in the frozen market inputs or the nine saved budget/performance combinations. This is a static review plus read-only JSON/arithmetic inspection, not a fresh execution certification. The reported ten passing tests and earlier 84-entry verification with zero effective failures are accepted as supplied evidence, not rerun or contradicted.

## Correctness barriers

### R1 — High: automatic PDF matches bypass current-byte and identity freshness checks

- **Primary location:** `06_workflow/scripts/refs.py:583–588`. The no-manual-record branch returns the cached automatic status before the SHA-256/current-identity checks at `616–627`.
- **Affected consumers:** `find_problems` at `767–787`, `entry_badges` at `1067–1079`, HTML counts at `1126–1138`, and `cmd_check_draft` at `1545–1558`. `cmd_verify` instead reruns `check_pdf` at `1430–1434`, so its result can disagree with build/draft/HTML on the same changed entry.
- **Concrete failing input, not executed:** take the existing automatic-match entry `green-sm-2026a` (`04_references/references.json:21`), leave its saved PDF and `verification.pdf_text` unchanged, and change only `accessed` from `2026-09-27` to the valid date `2026-09-26`. No `pdf_identity_accept` is present. The saved automatic record already contains both hashes, but this branch never compares them. An equivalent byte-level case is replacing the PDF at its existing registered path while retaining the cached automatic match.
- **Reason:** only manual records trigger freshness validation. For the date-edit example, the path still exists, the date passes ordinary field validation, and `pdf_state` returns `match`. A fresh `check_pdf` would detect the original printed accessed stamp against the changed registry date at `1374–1384`.
- **Consumer consequence [INFERENCE from the traced branches]:** build and HTML continue to label the edited entry PDF-verified; promoting/citing it permits the PDF gate in check-draft to pass with an inconsistent snapshot date. A replaced, existing file can similarly inherit the previous file's match. A fresh verify would fail where these consumers accept.
- **Recommended fix:** validate current bytes and identity against the automatic record before any cached automatic success is returned, independently of whether a manual acceptance exists. Missing or stale bindings must require fresh verification; preserve the original automatic details for the audit. Reuse the existing hash helpers and effective-state function rather than adding another consumer-specific rule. Keep the manual restrictions unchanged.
- **Regression gap:** `test_refs_pdf_identity.py:118–141` checks changed bytes and metadata only on entries with a manual acceptance. Add the corresponding automatic-match cases, including changed accessed date and replacement bytes, with build/draft/HTML rejection before fresh verification. This is a specific consumer-visible gap, not a request for generic validation machinery.

### R2 — High: Crossref's independent gate accepts stale results after year/DOI changes, including offline verification

- **Primary location:** `06_workflow/scripts/refs.py:531–541`. `crossref_state` judges only the old `differences` and current acceptance list. It does not bind that result to the entry's current DOI or bibliographic fields.
- **Related locations:** Crossref is refreshed only when not offline (`1406–1417`); the final verify success decision still trusts `crossref_state` (`1451–1452`). Build's DOI gate is at `788–789`; check-draft's is at `1551–1557`.
- **Concrete failing input, not executed:** start with `gupta-sinha-2022` (`04_references/references.json:2252–2320`), whose saved Crossref result is a match for DOI `10.3390/su142113768` with issued year 2022. Change only the entry's year to `2021`, retaining the original PDF and cached Crossref record. Then request offline verification. Alternatively, replacing only the DOI with another syntactically valid DOI leaves `crossref_state` unable to notice that its saved `doi` belongs to the old request.
- **Reason:** the PDF check verifies title/author and any snapshot stamp, not publication year or DOI (`1333–1388`). Offline verification can therefore create a fresh PDF hash/identity record for the edited metadata while retaining a Crossref record with empty differences for the old metadata. `crossref_state` returns `match` because those old differences are empty. A key/year naming discrepancy is only a warning (`713–715`), not a blocking safeguard. Fixing R1 alone will not fix this path, because offline verification refreshes the PDF binding.
- **Consumer consequence [INFERENCE from the traced branches]:** offline verify can report effective success for the wrong year/DOI, and build/check-draft/HTML can represent that current bibliography as independently Crossref-verified. This defeats the intended non-overridable year/DOI check without using a manual PDF override or prohibited `verification_accept` field.
- **Recommended fix:** bind Crossref verification to the exact DOI and bibliographic fields compared when the record is fetched; invalidate that effective result on subsequent changes. Alternatively, recompare a sufficiently complete cached Crossref record against the current entry, explicitly checking the requested DOI. Offline mode must retain a stale/unverified state rather than upgrading a changed identity. No new network call is necessary inside build or check-draft.
- **Regression gap:** `test_refs_pdf_identity.py:192–206` confirms that already-recorded DOI/year/author differences remain blocking. It does not cover changing the current entry after a successful Crossref result. Add that state transition, including an offline verify after the edit and subsequent consumer rejection.

## Manual PDF acceptance review

No additional bypass was identified in the manual branch reviewed:

- `refs.py:591–615`: exact audit-record fields, non-empty audit text, real non-future checked date, lower-case SHA-256 formats, title/author-only field allowlist and required bibliographic fields.
- `refs.py:616–627`: manual identity digest, actual current PDF-byte digest and automatic-check digests must agree. Retrieval method participates in identity at `558–563`, so changing the snapshot requirement invalidates a manual binding.
- `refs.py:630–635`: a manual record cannot upgrade an unchecked, extraction-error or automatic-match result; it must match the sorted automatic title/author mismatch fields. An `accessed` mismatch cannot be accepted.
- `refs.py:1374–1388`: the automatic result records accessed-stamp failures separately and retains its details and hashes.
- `refs.py:577–578, 639, 772–774, 1075–1079, 1220–1229`: effective acceptance is separate from the original automatic mismatch, with manual audit details exposed in HTML and problem reporting.
- Crossref differences are not directly overridden by PDF acceptance. R2 concerns stale Crossref evidence, not an acceptance-list allowlist failure.

The test file contains ten regression methods covering valid manual acceptance, title acceptance, bytes/missing files, identity changes, snapshot stamps, wrong header/type, malformed audit records, unchecked/error automatic results, blanket-status rejection and independent Crossref differences. Their supplied passing result does not exercise R1 or R2.

## Market-selection arithmetic

Reviewed all of `analyse_market_selection.py`, complete input JSON and the saved output's base, 57 sensitivity cases, summary, joint stresses and score bounds.

| Requirement | Review result |
|---|---|
| Frozen 25/20/20/15/10/10 weights | Input lines `13–19`; `weighted` divides the 1–5 ordinal scores by five (`17–18`). Independent calculation gives Denmark 92.5, Vietnam 88.5, Netherlands 84.5, India 76.0. |
| Selected weight ±20%, others renormalised | `56–62` adjusts the chosen weight, then scales the remainder to keep 100. Stored sensitivity weight sums are 100. |
| Equal weights and clipped score ±1 | `63–72`; clipped no-ops are excluded before appending. Thirteen weight cases plus 44 changed-score cases give 57 runs. |
| European gate and within-two-point rule | `25–33`: K1 and K3 each at least three, then candidates within two weighted points of the top eligible European total are ordered by K1, then K3. |
| Strict non-European margin | `36` requires more than five, with a small floating-point tolerance. |
| Base AND most sensitivity runs | `82–86`: base challenger must exceed the margin and win the policy choice in more than half the sensitivity runs. The base case is not counted as an extra sensitivity vote. |
| Joint stresses not extra votes | Constructed separately at `73–81` and emitted separately at `99`; excluded from `runs` and its majority denominator. |
| Raw versus preference-adjusted result | Saved summary (`market-selection-results.json:3662` onwards): Denmark 54 raw wins, Vietnam one, two Denmark/Vietnam ties; Denmark is policy choice in all 57. The K1 Denmark downgrade causes the Vietnam win; K2/K3 Denmark downgrades cause the ties. |
| Interpretation | Code `101–102` and input status explicitly retain unapproved ordinal evidence-fitness status, not marks, statistical confidence or success probabilities. |

No defect was identified for the fixed countries, criteria, gates or supplied perturbations. No arbitrary public-API input validation is recommended.

## Budget-model arithmetic and interpretation

Reviewed all of `model_marketing_scenarios.py`, complete inputs and all three saved allocations/nine performance cases.

- Allocations: DKK240,000 / 600,000 / 1,200,000, each saved at 100%; professional hours 180 / 460 / 860; uncommitted contingency DKK36,000 / 40,805 / 56,605. `allocate` subtracts actual allocated line costs from the reserved total (`52–63`).
- DOOH: 200,000 ÷ 1,000 × DKK191 = DKK38,200; 400,000 gives DKK76,400, with DKK4,995 setup in the two DOOH cases. No DOOH conversions are invented. The source assignment is in input `10–11`; this review did not independently inspect the rate-card PDF.
- Search uses media spend ÷ CPC (`74`); social uses spend ÷ CPM × 1,000, then CTR (`75–76`). First paid riders use their respective conversion fractions (`77–78`).
- Acquisition deduplication is a stated fraction of combined channel acquisition (`79`). Repeat rides use the mature 75% cohort, the scenario repeat fraction and three extra rides (`80–82`), not all immature year-end cohorts.
- B2B rides are accounts × eight rides/month × six active months (`83–85`). The supplied model expressly assumes account and consumer ride groups are disjoint (`budget-scenario-inputs.json:26`; narrative `budget-kpi-scenarios.md:74`); it does not perform empirical booking-ID deduplication. This is an assumption boundary, not a demonstrated double-counting arithmetic bug.
- Vouchers use floor(reserve/30), then min(first payers, capacity) (`86–88`). The middle illustrative case redeems DKK11,340 of its DKK12,000 reserve, leaving DKK660; the upside is capped at DKK12,000. Fractional rider/redemption results are explicitly conditional arithmetic.
- DKK39 + 10 × DKK11 + 12 × DKK6.50 = DKK227 (`91–92`). Output names identify this as an illustrative trip, not average revenue. Booking value is ride equivalents × this proxy, not profit (`114–117`). Source tariff provenance is recorded in input `12–14`; the actual tariff PDF was outside this slice's direct inspection.
- Paid-media cost per first payer excludes DOOH/shared/B2B costs; the voucher-inclusive version adds redeemed incentives only (`89–90, 112–113`). It is not labelled fully allocated CAC.
- Contribution is the booking proxy × assumed 30% or 50% contribution, compared with the **full reserved envelope**, not actual spend (`94–101`). Incentives are not deducted twice. The narrative explicitly explains reserve versus accrual profit (`budget-kpi-scenarios.md:87`).
- Break-even uses ceiling (`100`): the middle thresholds independently calculate to 8,811 rides at 30% and 5,287 at 50%.

### Saved scenario evidence

Rounded display only; underlying JSON retains full precision. All monetary values are DKK. Deficits below compare contribution with the full reserved envelope, not observed accounting profit.

| Envelope / performance | First payers | Ride equivalents | Booking-value proxy | Deficit at 30% | Deficit at 50% |
|---|---:|---:|---:|---:|---:|
| Lean / downside | 42.4622 | 176.7702 | 40,126.84 | −227,961.95 | −219,936.58 |
| Lean / illustrative | 144 | 545.4 | 123,805.80 | −202,858.26 | −178,097.10 |
| Lean / upside | 473.5385 | 1,409.4692 | 319,949.52 | −144,015.15 | −80,025.24 |
| Middle / downside | 108.2333 | 444.9383 | 101,001.00 | −569,699.70 | −549,499.50 |
| Middle / illustrative | 378 | 1,395.675 | 316,818.23 | −504,954.53 | −441,590.89 |
| Middle / upside | 1,262.7692 | 3,691.3846 | 837,944.31 | −348,616.71 | −181,027.85 |
| Expanded / downside | 254.66 | 945.257 | 214,573.34 | −1,135,628.00 | −1,092,713.33 |
| Expanded / illustrative | 891 | 3,032.6625 | 688,414.39 | −993,475.68 | −855,792.81 |
| Expanded / upside | 2,979.3462 | 8,347.1106 | 1,894,794.10 | −631,561.77 | −252,602.95 |

The negative economics are explicit in the saved results and narrative, including upside cases. Inputs retain the assumptions/not-forecast warning and do not select or approve a scenario.

The independent evidence/strategy reviewer owns a separate wording issue: KPI narrative line 105 uses eligible landing-page clicks, while the model uses purchased channel clicks without an eligibility stage. This report does not duplicate that content finding or propose invented conversion factors.

## Maintainability and scope restraint

No cosmetic or general-framework findings are raised. The two fixes should remain within the existing effective-state functions and relevant regressions. The fixed research scripts do not need a generic schema framework, new retries, telemetry or scenario expansion to address this review.

## Actual read scope and verification limits

- `06_workflow/scripts/refs.py`: lines `1–243`, `501–649`, `664–789`, `1060–1093`, `1115–1142`, `1210–1268`, `1279–1461`, `1488–1605`, plus targeted declaration/call-path search. Citation parsing, reference-rendering internals and HTML/CSS implementation outside those ranges were not comprehensively reviewed.
- `06_workflow/scripts/test_refs_pdf_identity.py`: complete, lines `1–210`; read only.
- `06_workflow/scripts/analyse_market_selection.py`: complete, lines `1–119`.
- `06_workflow/scripts/model_marketing_scenarios.py`: complete, lines `1–148`.
- `02_research/business-selection/market-selection-inputs.json`: complete, lines `1–113`.
- `02_research/business-selection/market-selection-results.json`: complete JSON parsed read-only (3,890 lines); inspected base, sensitivity rows/counts, weight totals, rank reversals, joint stresses and bounds. No production analyser was invoked.
- `02_research/marketing-plan/budget-scenario-inputs.json`: complete, lines `1–78`.
- `02_research/marketing-plan/budget-scenario-results.json`: complete JSON parsed read-only (686 lines); inspected every allocation and all nine funnels/contribution cases. No production model was invoked.
- `04_references/references.json`: read-only JSON snapshot and targeted record inspection, including the automatic-match and Crossref examples above. During this review it contained 97 candidate entries: 79 stored automatic matches and 18 stored mismatches with manual records. These are stored-state counts, not fresh verification results; the parent was concurrently integrating additional corporate PDFs.
- `06_workflow/references-workflow.md`: targeted search of verification, snapshot, Crossref, offline and freshness promises, especially `96–99`, `139–141`, `186–190`.
- `02_research/business-selection/focus-market-selection.md`: targeted method/rule/interpretation passages.
- `02_research/marketing-plan/budget-kpi-scenarios.md`: targeted arithmetic/assumption passages and lines `79–122` in context.

Runtime counterexamples R1/R2 are explicitly unexecuted predictions from the shown control flow. No source PDF, browser surface, generated HTML or actual reference-verification command was exercised in this slice. The parent owns reproduction, fixes and subsequent end-to-end validation. Only this named review report was saved.

## Parent resolution and exercised verification — 28 September 2026

This addendum records subsequent implementation, not an expansion of the independent reviewer's read scope.

| Finding | Resolution and observed proof |
|---|---|
| R1 | Reproduced against a copy of actual `green-sm-2026a`: editing only the accessed date wrongly retained `match`. `pdf_state` now checks current byte/identity bindings for automatic matches as well as manual records; the same edit returns `error`. Isolated regressions also reject replaced PDF bytes and missing bindings through build/draft consumers. |
| R2 | Reproduced using actual Gupta/Sinha metadata: changed year/DOI plus a refreshed PDF check still yielded cached Crossref `match`. Crossref comparisons now bind the exact requested DOI/compared fields; offline verification cannot update that binding. After online reverification of the real baseline, the same altered year/DOI cases retain PDF `match` but produce Crossref `error`, as required. |
| Regression scope | Four freshness transition cases were added to the ten identity cases; all **14 passed** in the actual unittest run. Incidental wording assertions were removed rather than re-pinned. Tests use isolated temporary registries/PDFs and no live network. |
| Live integration | Actual `refs.py verify`: **97 entries, zero effective failures**. Actual build: **0 errors, 17 reviewed advisory warnings, 18 manual notes**; no source is prematurely marked cited. Real Statbank manual acceptance passes and a copied metadata change rejects it. |
| Model scenarios | Actual analyser/model runs produced the saved results. Additional throwaway execution exercised strict +5 versus +5.02 market override, zero acquisition, capped vouchers, the unchanged-cost consumer-only stress and the paid-click conversion denominator. No model arithmetic correction or extra performance assumption was needed. |
| UI proof and limit | Browser search displayed 97/97 identities, 18 explicit manual acceptances, 1/1 DOI check, and the real Statbank card's automatic mismatch/audit. Screenshot helper/headed-worker attempts timed out; standalone Chrome produced the linked image before its process deadline. The parent inspected that image. No poster or mobile/A0 proof is claimed. |

[Inspected reference-report screenshot](reference-audit-2026-09-28.png). The specialised reviewer backend originally rate-limited before producing work; this report came from the completed replacement reviewer, not from that failed attempt. All verification claims above are parent observations, not tests performed by the independent reviewer.
