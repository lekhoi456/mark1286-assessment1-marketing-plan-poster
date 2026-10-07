# Section 8 v03 — focused review

**Status:** DONE_WITH_CONCERNS. Candidate for parent selection under the delegated task; no group approval or A0 acceptance claimed.

The visual reduces the section to 195 visible whitespace-separated words, including the shared logo lettering. The main route is awareness → paid trial → repeat. It preserves +10 percentage points from the M1–2 baseline to M12; 378 first paid riders; search 3% and social 1.5% of all paid clicks; ≤DKK524 per first paid rider for search/social only; fully observed 90-day paid repeat ≥35%; and the four service guardrails. Gate A retains all five M4 thresholds, the minimum-volume agreement, and pass/fail actions. Gate B retains the mature-cohort ≥20% and ≤DKK1,829 continuation thresholds, the ≥35% street-screen release, and the stop-scale-up branch. M12 retains renew/revise/stop.

The footer distinguishes installs from sales, counts completed paid trips after refunds, limits repeat to full 90-day observation, limits DKK524 to search/social, and restricts advertising to verified areas with usable offers. The service denominator for completion and cancellations is accepted bookings. No results are plotted.

## Focused checks

- `presentcheck.py --mode poster`: **169 / 380 words**; detector ran with zero effective base hard findings and no genre-review items. Exit 2 is only for the two absent full-poster markers (`budget-table` and `kpi-table`), which do not belong in this standalone dashboard. No whole-poster pass is claimed.
- Geometry and content checks in [08-v03-checks.json](08-v03-checks.json): all requested labels present; search/social bars are exactly 2:1; Gate A pass/fail and Gate B continue/screens/stop branches present; 48 text glyph boxes; zero text overlaps and zero out-of-canvas text.
- The final 2200 × 2520 px PNG was visually inspected. The unchanged shared logo hash matches `shared-logo.png`; the reused icon strip hash matches v02 art.

Confidence: high for target fidelity and the inspected on-screen layout. Remaining limits: actual A0 fit, physical legibility and print output are untested; parent selection and group approval remain open.
