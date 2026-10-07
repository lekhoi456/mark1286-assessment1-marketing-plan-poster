# Section 6 cell fit v01 — five-stage sales loop

Status: human-review candidate, 4 October 2026. Condensed wording and artwork await acceptance. The accepted Section 5 v04 is the assembly base. Confidence: high for file preservation, font resolution and geometry checks; unverified for normal-distance A0 reading and physical redraw.

## Display and coverage mapping

| v07 baseline meaning | Fitted display and retained coverage |
|---|---|
| Copenhagen visibility; installs are leads, not sales | Awareness shows Copenhagen visibility → leads and Installs ≠ sales. The roadside advertising billboard illustrates visibility, not a verified placement or operating asset. |
| App booking closes only when the trip is completed and paid | Book shows Green SM app booking → completed, paid trip = sale. A successful app installation or booking alone is not counted as a sale. |
| Capped percentage first-ride test | First-ride test: 10% vs 20% · max DKK30. This preserves the approved amendment and does not revive a fixed DKK30 discount. |
| One first paid ride per rider; 400-rider cap; single DKK12,000 reserve ceiling | The accepted neighbouring Section 5 already shows First paid ride, Max DKK30, 400 cap and 1/rider. Section 7 v05 retains the single reserve ceiling. These are cross-panel coverage, not a new pool. 400 × DKK30 = DKK12,000 maximum. Full assembly reconciliation remains necessary when Section 7 is fitted. |
| App, driver, car and support after service checks | Experience shows App / driver / car / care and Target quality after checks. The car, driver, phone and heart are intended quality/brand affinity, not a measured service result. |
| Post-ride feedback; unpaid review only after a resolved or well-rated ride | Feedback explicitly retains both conditions. The star illustrates a review, not a guaranteed rating or an incentive payment. |
| Consented reminder; voucher and tailored monthly bundle pilots only after frequency/unit economics testing; separate funding | Repeat shows Opt-in reminders, voucher pilots* and Tailored monthly paid bundle pilots*. The shared asterisk states After frequency/unit economics test; Separate costing. The return arrow ends at Book. Both pilots remain proposals and depend on observation/testing, not achieved retention. |

This is a visual compression of the supplied v07 baseline plus the controller's paid-bundle clarification. No new external fact, concept or source was added. The source copy remains preserved. New condensed copy is proposed for human review, not silently labelled approved.

## Focused checks

- Native cell 06 remains x619–844, y400–598. All controlled glyph-box corners are inside its curved boundary; no pairwise text-box overlap. The transparent layer is clipped to the existing cell-06 path.
- Removing the new Section 6 layer reconstructs the Section 5 v04 base byte-for-byte. The background, car translation, Section 5, all eight other empty cells, identities and flags are preserved.
- Native flat-colour illustrations use editable paths/circles: roadside billboard, voucher, app/driver/car/care, review bubble/star and reminder/bundle. The controller reviewed the first preview and requested the billboard to clarify Awareness. No new raster image, logo, gradient, hatching, shadow or calendar grid was added.
- Actual lettering resolves to ChalkboardSE-Regular and MarkerFelt-Wide. Unicode arrows use the existing helper's deliberate native vector arrow. No Helvetica fallback. The heading underline follows measured text advance width.
- Displayed word-bearing whitespace tokens: **63**, including the leading section number, headings and labels. The presentation checker reports **62** because its Markdown heading handling drops the leading numbered-heading token. Standalone arrows, equals signs, separators and slashes are excluded from the manual word-bearing convention.
- Stage labels: 16.13 pt at A0. Ordinary labels mainly 13.30 pt; width-limited labels may be smaller. Minimum lettering: 12.09 pt. The 1600-pixel crop is a placement preview, not proof of comfortable A0 reading distance.
- Actual PDF page: 1188.999 × 841.001 mm from PDF metadata, rounding to 1189 × 841 mm. Full SVG/PDF/PNG includes accepted Section 5 and candidate Section 6.
- Focused presentcheck ran with the exact Section 6 heading and a 90-word fragment budget. Detector ran, score 0; zero effective base hard stops. Exit 2 records only absent whole-poster budget/KPI tables, intentionally outside this fragment. No broad full-poster check was run. Manual meaning review retains proposed status, payment completion, unpaid reviews, consent and both pilot conditions.
- An additional strict-scope run using the current concept-list is preserved separately in `-copy-scope-check.json`. It flags the existing subtitle “Sales Strategy” because the list has specific sales concepts but lacks that generic panel-label alias. This is a reviewed label mismatch, not a newly introduced framework: v07 already uses the subtitle, and the concept register's sales-channel entry (Week 4 lecture s9/tutorial s7, register lines 722–735) explicitly maps to Sales Strategies. The subtitle/copy was preserved; no register, list or protected checker was changed. The strict run's one scope flag is retained, not silently reported as a mechanical pass.

Outputs share `06-cell-fit-v01-2026-10-04`: `-poster.svg`, `-poster.png` (2400 px wide), `-poster.pdf`; `-close-up.svg`, `-close-up.png` (1600 px wide); transparent `-layout.svg`; `-copy.md`, `-displayed-copy.txt`, `-checks.json`, `-copy-check.json`, `-copy-scope-check.json` and reproducible `-render.py`.

Unresolved: human acceptance of condensed copy/illustrations and A0 legibility. Section 7 ceiling coverage awaits its later fit. No group approval, final print acceptance, submission or commit is claimed.
