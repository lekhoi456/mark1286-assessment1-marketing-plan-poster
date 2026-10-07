# Scaled-plan proof v04 — production brief

7 October 2026. D-163. Base: proof v03 (D-160). Copy: [v46](10-sections-scale-copy-v46-2026-10-07.md). Numbers: [scale-plan model](scale-plan-v01-2026-10-07-model.py). Status: proof awaiting student review.

**Plan scale.** The DKK600,000 test budget becomes a proposed DKK30.0M gated market-entry budget (objective-and-task; about 6% of an assumed base-case revenue of 450 cars × 15 trips/day × DKK200, stated on the poster as assumptions). Eight bars on one 0–8M scale; cumulative caps DKK7.5M at M4 and DKK13.5M at M6, DKK16.5M held at M6. Section 8 targets: ≥50% aided awareness, 150,000 first paid riders, 2.5M paid trips (15/car/day by M12), ≥50% 90-day repeat, media CAC ≤DKK100 (defined on the poster); M4 and M6 review floors; ≥100 business accounts.

**Segments and campaign.** Section 2 shows four segments with 25–44 highlighted as the focus (M1+), then all adults (M1+), business accounts (M4+) and visitors + airport (M6+). The city-wide launch campaign is *Copenhagen, meet Green SM*, with *Go Green / For a Green Future.* as its tagline in Section 4 and a Danish-first line. Section 5 gains a Channel → KPI table and a LAUNCH CAMPAIGN box; the DATA box, taxi drawing and 30-day calendar are removed (their content stays in Sections 6 and 9).

**Connected cells.** Ten cyan dashed arrows (#28bdbf, 1.7 stroke, 3.2/2.4 dash) cross the gutters where one cell feeds the next: 1→2, 2→3, 3→4, 1→5, 2→6, 5→6, 7⇄8, 6→9, 8→10, 9→10.

**Lettering.** New strings reuse the approved glyph outlines ([glyph-reuse library](glyph-reuse-lettering.py)); ø, ×, ≤ and æ come from the source poster or are composed from its glyphs. 156 unchanged strings are byte-identical to the v03 build. Lettered words: 712 (v03: 681 on the same count), so the plan's extra content costs about 5% more text.

**Back of chart.** 21 Harvard entries, adding European Commission (2025) and Green SM Denmark ApS (no date a); the reported 3,000-driver ambition is not registered and stays off the poster.

**Checks** (`poster-scale-plan-v04-2026-10-07-checks.json`): model pass; every bar, cap and KPI matches the model; no DKK600,000-plan figure remains; ten connectors; palette clean; back list alphabetical.

Rebuild: `python3 -B poster/poster-scale-plan-v04-2026-10-07-render.py poster/poster-references-v04-2026-10-07.svg poster`, then the v04 check script with the same arguments.
