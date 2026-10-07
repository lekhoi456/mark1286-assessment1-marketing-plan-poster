# Poster v05 — local first-marker review, 3 October 2026

**Reviewed:** `../poster-v05-2026-09-28.md`, design concept v03, the official brief/rubric, requirements matrix, approved Copenhagen plan and local source PDFs. This is an independent agent review, not lecturer feedback or an awarded grade. No official criterion-level grade bands were supplied.

**Verdict: fix the subscription rationale and clarify the repeat-rate denominator before copy approval.** The plan is coherent and materially more defensible than a generic channel list. Its weakest commercial link remains whether clarity and help can overcome price and habit. That is a declared hypothesis, not a falsified company fact. Copenhagen, S1/P1, the DKK600,000 envelope and the agreed production route remain settled (D-031–D-034). Final artwork, contributions and delivery have not been assessed.

## Verified defects and precise fixes

### B1. False 90-day comparison — Creativity, line 170

**Confidence: high.** “Under two rides per new rider within 90 days” uses 675.675 annual ride equivalents divided by all 378 first riders. The model assumes only 75% have a full observation window. For a mature cohort the same assumptions give **1 + 35% × 3 additional rides = 2.05 rides per first rider**, not fewer than two. Sources: `../../02_research/marketing-plan/budget-kpi-scenarios.md`, lines 95, 102 and 126; `../../06_workflow/scripts/model_marketing_scenarios.py`, lines 82–87. This is a model contradiction under the audit taxonomy; it does not reverse the approved subscription deferral.

**Replace:** “A subscription model waits, as the plan expects under two rides per new rider within 90 days.”

**With:** “A subscription model waits until frequent paid use is evidenced.”

### F2. Repeat-rate denominator lost in compression — Measurement, line 150; Gate B, line 157

**Confidence: high.** “Customer retention rate within 90 days” does not identify another paid trip or exclude riders who have not yet had 90 days. The approved plan §10 explicitly defines both, and Gate B uses the mature M3 cohort. The poster could otherwise apply the 35% target to a different denominator. No observed rate is claimed or disproved.

**Word-neutral row replacement:**

`| 90-day paid repeat | O3 repeat | ≥35% of fully observed first riders | Rider cohorts | Monthly from month 6 |`

Use this same measure for Gate B. Keep its approved 20% continuation floor and 35% screen-release threshold. Explain the M3 cohort in the pitch, without inventing a rehearsal.

## C1–C7 assessment

Ranges predict criterion credit from the current evidence; they are not official bands or deductions calculated from findings. Content confidence is **moderate**. C7 confidence is **unknown**.

| Criterion | Provisional credit | Evidence and remaining limit |
|---|---:|---|
| C1 — background/context, 10 | 7.5–8.5 | Origin, service, dated European entry and eight-market footprint are clear (lines 12, 23–27). The operating-model contrast explains P1. KFST PDF pp. 119 and 174 supports it; it does not prove better service. |
| C2 — target/segmentation/branding, 15 | 11–12.5 | Three alternatives, demographic/geographic/behavioural/psychographic bases, persona, UVP and message are applied (lines 34–74). KFST pp. 150–151 supports 57%, 22%, 11% and n=79. These are app-choice respondents, not representative S1 demand. The interpretation is labelled. Logo/colour fit is mainly continuity, with the actual visual still absent. |
| C3 — digital/sales, 20 | 14.5–16 | Journey stages lead to concrete search, content, social, follow-up and direct sales tactics (lines 81–105). Help is explicitly staffed outside the budget and conditional on its standard. National social-media identities support broad reach, not chosen-city conversion. Local capability remains a prerequisite. |
| C4 — budget/resources, 15 | 11–13 | DKK600,000, period, VAT basis, 460 hours, line quantities, contingency and staged exposure are visible (lines 110–134). Published screen rates are reproducible: AFA PDF p. 3. DKK46,000 recovered against DKK600,000 makes the shortfall clear; it is not a profitability claim. Professional rates, conversion and contribution remain assumptions. |
| C5 — KPIs/objectives, 10 | 7–8.5 | Nine target/tool/rhythm rows and actionable gates link to O1–O4 (lines 144–157, 180). Paid-click denominator and channel cost numerator survive. F2 needs repair. The mature-cohort rule is more consequential than adding another metric. |
| C6 — emerging concepts, 10 | 6–7.5 | Consented personalisation, the shared trip reference and illustrative reminder explain mechanisms; AI/subscription/neuromarketing are considered with reasons (lines 164–171). B1 weakens the subscription rationale. Originality lies in the entry promise and integration, not a demonstrated new technology or tested effect. |
| C7 — visual/presentation, 20 | Unscored | Eleven headings and truthful name/number pairs exist. A0 layout, charts, contrast, logo, text fidelity, reference packaging, contribution evidence and actual pitch cannot be verified from Markdown/design instructions. |

**Content subtotal: approximately 61/80, provisional range 57–66/80.** A future C7 outcome of 12–16/20 would put the central estimate around 73–77/100. That is a conditional planning estimate, not the current poster's verified total. The missing proof and contribution evidence could materially change it.

## v04 repairs checked against v05

**N2–N8 survive.** The rebrand now separates unified name/identity from Danish values (line 70; rebrand PDF p. 1 and Danish About PDF p. 1). Selling “rather than competing on discounts” is consistent with a capped voucher. Screen setup attribution, Digital Copenhagen awareness role, service-area search, explicit Gate A conditions, first-rider conversion denominator and labelled psychographic interpretation are restored. The core-product label, reliability mechanism, residual contingency, initial-phase employment and “as at” date also survive.

**N1 is correctly treated as pending proof.** Concept v03 labels its fit calculations as inference, identifies overflow and targets the relevant columns. Its numbers do not establish actual typeset fit or print legibility. No layout defect can be declared fixed merely by correcting an estimate. Lights remain unlit and their legend uses approved copy; segment signposts are not called gates.

## Defensible limits and release work

- **C2/C3 challenge:** 11% reporting safety from app transparency does not establish demand for complaint resolution or willingness to switch. The labelled P1 hypothesis and funded research/gates are a defensible response. Do not turn it into “customers demand” or “proven differentiation”.
- **C3/C5 prerequisite:** live coverage, usable offers and staffed help remain unverified. The approved plan §§3, 10 and 14 retains service checks and availability logging. Preserve these in implementation and pitch; do not invent a numeric availability baseline or change approved gate thresholds.
- **C4 challenge:** the year-one economics are negative. Staged exposure limits loss but does not prove the learning is worth DKK600,000. The group must defend the chosen market-entry objective and evidence needed for year two. Reclassifying the campaign as profitable, or silently substituting a smaller envelope, would be wrong.
- **Minor referencing work:** final-set year suffixes remain a recorded P8 task. Relabel the registry and both citation directions together. A correct PDF does not itself settle final Harvard lettering.

## Checks and unresolved items

Fresh checks: **1,424 words**, counting panel headings, table text and citations, excluding title/references/comments; every panel within its internal budget. `refs.py check-draft`: **0 errors, 0 warnings**, 14 listed works identical to the generated list. `presentcheck.py`: detector ran; anti-slop and module-scope hard findings **0**; budget **600000 / 100.00%**; nine KPI rows. It exits **2**, retaining the known frozen base-checker failure to parse the digits in “TAXA 4x35”. The dedicated citation check and the local TAXA PDF p. 4 support that citation. This is recorded, not suppressed or called a clean gate. Poster label fragments and bold hierarchy are legitimate here; they do not repair B1 or F2.

Selected factual passages and calculations were re-extracted from all fourteen cited PDFs. The recruitment passage is on p. 3; Denmark's mission/values on p. 1; the app fare/advance-booking text on p. 3. The logo/colour description was not independently inspected as rendered artwork in this review. No browser, protected-checker edit, source change or contribution claim was made.

**Unresolved:** group approval of revised wording; authentic contributions/speaking responsibility (Q-S5); actual A0/export proof; reference placement/upload format; final AI disclosure and local assessment administration; operational and customer evidence prerequisites already listed in the approved plan. No lecturer answer or completed pitch exists in this review.
