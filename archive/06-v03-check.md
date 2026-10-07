# Section 6 v03 — focused check

Prepared 4 October 2026. This is a Section 6 candidate check, not whole-poster acceptance or group approval.

## Content and interface

- Exact title: `6. From Clicks to Rides`. Unnumbered subtitle: `Sales Strategy`.
- Journey: Copenhagen awareness → app booking → target experience → feedback → consented repeat test. Reach and installs/accounts are leads. A sale is a completed, paid trip booked direct in the app.
- Existing first-ride incentive remains DKK30, one per new rider, capped at 400 riders (DKK12,000 reserve under the approved plan). No additional voucher budget is proposed.
- “Experience to earn” labels excellence as a target. The service-gate callout requires operating and staffed-help standards to be verified before any quality claim.
- Feedback asks one trip-clarity question and invites an unpaid app-store review only after a resolved or well-rated trip.
- Repeat notifications require consent. Any repeat voucher needs separate approval and funding. A tailored, capped, time-limited monthly promo bundle is a pilot hypothesis conditional on observed rider frequency and unit economics; no repeat-voucher budget, Copenhagen launch, subscriber base, retention lift or revenue lift is approved, claimed or forecast.
- The page contains no evidence IDs, visible citations, channel spend, extra line items, or Section 9 innovation change. The existing DKK600,000 plan assumptions are not revised.

## Visual and technical checks

- The rendered PNG is 1800 × 1500 RGB and was visually inspected at full and 900 × 750 preview sizes. Five stages, direct arrows and the return loop to app booking read clearly; no clipping or visible text collisions were observed.
- The editable SVG embeds the provided Green SM logo as a data URI, with all other art and display copy editable as vector shapes and native SVG text. The embedded logo bytes match `shared-logo.png` exactly; SHA-256 is recorded in the provenance file.
- Renderer bounds and pairwise-overlap checks cover 45 text groups and pass. Parsed SVG copy matches the copy source for the required title/subtitle, all five stages and both callouts. No evidence IDs appear in the displayed text.
- A0 reproduction, integration with adjacent panels and operational launch readiness have not been verified.

## Writing gate

The protected `presentcheck.py` poster gate was run against the display copy only. The section contains 143 whitespace-token words against its 185-word budget. Anti-slop detection ran with score 0 (`Clean`); there were zero effective base-copy hard stops and no out-of-register concepts.

The command exited 2 solely because poster mode requires one full-poster budget-table marker and one KPI-table marker, absent from this standalone panel. It returned no label-colon review items. This is a fragment-scope structural limit, not a failed copy check or a whole-poster pass.
