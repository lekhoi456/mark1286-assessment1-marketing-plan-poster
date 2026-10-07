# Final poster v07 — production brief

7 October 2026. D-166. Base: proof v06 (D-165). Status: **final version** at the student's request; the student delegated the remaining content decisions to Claude. Group acceptance, printing and submission remain separate.

**Number corrections** ([model v02](scale-plan-v02-2026-10-07-model.py)). A monthly cohort check showed that v04–v06 treated a full-fleet pace as a year-one total. The final front states:

| Where | v06 | Final v07 | Why |
|---|---|---|---|
| Section 8 trips card | 2.5M · Paid trips · 15/car/day average | 2.5M · Paid trips a year · run-rate by M12 | 150,000 riders, mostly acquired after M6, give about 1.16M trips in year one but a 2.62M pace at M12 |
| Section 7 logic line and footnote; Section 10 | about 6% of base revenue; *Base case | 6% of run-rate revenue; *Run-rate | DKK30M is 6.1% of DKK493M run-rate revenue (13.0% of modelled year-one revenue, stated in the script) |
| Section 8 M6 review | ≥10 trips per car per day | ≥2,500 paid trips a day | The cohort path gives about 2,900 a day at M6; trips per car depends on how many cars Green SM runs |
| Section 7 bars | Social 6.0M / 20% · Team/creative 2.4M / 8% | Social 5.0M / 17% · Team/creative 3.4M / 11% | 2.4M could not fund three campaign staff and agency production; media CAC becomes DKK80 (cap DKK100) |

Unchanged: DKK30.0M total, caps DKK7.5M / DKK13.5M, DKK16.5M held at M6, 150,000 first paid riders, ≥50% awareness, ≥50% repeat, M4 review, ≥100 business accounts, all other copy and artwork of v06. Text cuts were considered and rejected: each candidate line carries a cross-section link or a guardrail.

**Checks** (`poster-scale-plan-v07-2026-10-07-checks.json`): model v02 pass; bars, labels, caps and KPIs match the model; no superseded figure or wording remains; 156 unchanged lettering strings byte-identical to the v03 build; no connectors; palette clean; seven cloud lines.

**Final package:** `08_final/` (front + back PDF, single pages, SVG, PNG, script and study guide). Back of chart: `poster-scale-plan-v04-2026-10-07-back.*`.

Rebuild: `python3 -B poster/poster-scale-plan-v07-2026-10-07-render.py poster/poster-references-v04-2026-10-07.svg OUT`, then the v07 check script with the same arguments.
