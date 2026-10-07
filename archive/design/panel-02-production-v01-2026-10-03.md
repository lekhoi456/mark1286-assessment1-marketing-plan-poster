# Panel 2 — Target Market production package

Prepared: 3 October 2026. Content authority: D-043–D-046. This package freezes approved panel wording and chart text from selected specification/chart v04. Native vector geometry, typography and physical placement are production proposals for the consolidated proof; they are not whole-poster approval.

## Exact display-copy block

The following block is the complete visible text inventory, in layout reading order. The six profile labels are placed beside their corresponding icons. Joining each three-label group with ` · ` reproduces the selected specification verbatim. Line wrapping and icon placement do not change wording. Research IDs, review notes and mappings below are not displayed on the poster.

<!-- display-copy-start -->
```text
Target Market
Copenhagen residents aged 25–44
Self-paying · Existing taxi users · Recurring local trips
COPENHAGEN RESIDENTS BY AGE
Copenhagen municipality · 1 July 2026 · age groups 18+
0
100,000
200,000
300,000
Residents
72,396
18–24
269,277
25–44
143,668
45–64
74,728
65+
40.2%
of city residents
Source: Statistics Denmark (2026b), FOLK1A; calculated sums of single-year ages.
The 40.2% denominator is all 670,389 city residents, including those aged under 18.
Copenhagen — within the service area
Proposed rider profile
Price-conscious
Values trip control
Expects fair treatment
Already uses taxis
Recurring local trips
Pays personally
Recurring local trips create opportunities for repeat rides.
```
<!-- display-copy-end -->

## Production files and geometry

- [Complete section SVG](panel-02-production-v01-2026-10-03.svg): 1,800 × 1,360 user units; every letter and numerical value is an editable text object.
- [PNG preview](panel-02-production-v01-2026-10-03.png): a rendered copy for visual review, not the text master.
- [Text-placement manifest](panel-02-production-v01-2026-10-03-text-manifest.json): exact strings, IDs, coordinates, hierarchy, data and grouping rules.
- [Decorative illustration prompt](panel-02-production-v01-2026-10-03-illustration-prompt.md): a ready prompt for later approved artwork production; no image-model call has been made.

The panel uses a cream inset bounded by cyan, with navy text, a yellow share pill and rationale strip. Its rectangular footprint is intended for the cyan vehicle's usable interior; it does not add another panel or a vehicle shell. A proposed 330 × 249.3 mm placement gives the smallest 23-unit lettering approximately 4.22 mm (12 pt). This is a geometric estimate. The existing whole-poster schematic is not a tested full-copy layout, and its row heights may need reflow. Actual A0 integration, viewing distance, physical print and upload-image legibility remain unverified. No arbitrary word cap is adopted.

## Behind-the-scenes source and approval mapping

| Display content | Basis and scope | Source record |
|---|---|---|
| Priority 25–44, residence, usable service area, existing recurring taxi use and self-payment | Group-selected campaign scope, not observed customer performance | D-043; selected specification v04 |
| Psychographic and behavioural labels; Proposed rider profile | Approved planning hypothesis; the illustration is not a real survey respondent | D-044; E-024/E-187 inform price/control motives but do not establish an age-specific profile |
| Age columns and population counts | Copenhagen municipality, persons, 1 July 2026; 18+ comparisons | E-193; source PDF pp. 7–12; single-year calculation JSON |
| 40.2% pill and 269,277 separate count | 269,277 ÷ all 670,389 city residents × 100, rounded; children are included in the denominator | D-046; E-191; source PDF pp. 6 and 8 |
| Date, source line and denominator note | Exact selected chart v04 strings; no separate population-share badge | D-045/D-046; chart v04 |
| Repeat-opportunity caption | Approved prioritisation rationale; no claim that ages 25–44 are the most frequent or profitable taxi users | D-045; selected specification v04 |

Saved source: [Statistics Denmark dataset PDF](../../04_references/statistics-denmark-2026b-population-quarter-age.pdf). Source registry: [references.json](../../04_references/references.json), key `statistics-denmark-2026b`. Source URL is preserved in that registry and the PDF footer. Calculation: [age-segmentation-calculation-2026-10-03.json](../../02_research/marketing-plan/age-segmentation-calculation-2026-10-03.json). Evidence: [evidence-log.md](../../02_research/evidence-log.md), E-191/E-193. Content authority: [decision-log.md](../../01_context/decision-log.md), D-043–D-046.

The PDF hash matches both the saved calculation and the registry's accepted bytes. The automatic author-text check is an author mismatch because the API table omits organisation prose. The registry records an audited manual identity acceptance for that specific mismatch; this remains distinct from an automatic identity match. This package does not change the registry. The historical calculation/E-191 targeting status predates the later student approvals; D-043–D-046 govern the current marketing selection.

## Behind-the-scenes brief, rubric and module mapping

| Assessment ask | What this section visibly supplies | Boundary |
|---|---|---|
| Brief element 3: identify and describe the target | Priority age group, residence/service area and payment/use filters | Eligibility is a campaign selection, not measured population take-up |
| Brief element 3: demographic, psychographic and behavioural characteristics | Age chart, location, Proposed rider profile and six labelled symbols | No invented income, occupation, household type or taxi-frequency figure |
| Brief element 3: segmentation and prioritisation | Age comparison and highlighted range connect to the profile; filters and approved repeat-opportunity caption explain the priority | Unequal age spans and population totals do not prove optimal taxi targeting |
| C2: Target Market, Segmentation & Branding | Targeting/segmentation portion of the 15% criterion | Branding and the rest of C2 are assessed elsewhere; no separate panel mark |
| C7: visual/presentation quality | Hierarchy, counted columns, distinct share/count labels, readable profile labels and illustrative symbols | This preview does not establish final A0 or live-pitch quality |
| Module-first concepts | `target-market-analysis` (w04-lecture s6); `segmentation-bases` (w04-tutorial s5; w04-lecture s6); `targeting` (w04-lecture s7; w04-tutorial s5); `customer-personas` (w04-tutorial s4) | Registered module concepts; illustrative persona remains a planning device |

Controls: [brief.md](../../00_brief_and_criteria/brief.md), [rubric.md](../../00_brief_and_criteria/rubric.md), [concept-register.md](../../03_course_materials/concept-register.md). The approved short display heading Target Market maps to the canonical Target Market Analysis element; it does not remove that element.

## Integration limits

Retain the proposed-profile qualifier, source/date and all-city denominator at the same legibility standard as the labels. Do not add the optional stronger caption, a household/income/job restriction, a secondary segment, or the regional app-choice chart. The parent session retains consolidated integration and approval.
