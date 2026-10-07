# Section 8 v05 — tracking method proposal

Date: 4 October 2026. Discussion proposal only; do not treat this note as approved panel copy.

## Big Data premise

**Supported at group level, with a strict limit.** Vingroup's English *Annual Report 2024* places “SMART DATA SERVICES” under VinBigdata and describes it as a data-management and analytics service. It says the service “is being implemented for GSM” to enhance operational efficiency and enable swift decision-making. Locator: PDF page 26 is a two-page spread for printed pp.48–49; the statement is on printed p.49, Chapter 2, lower-right Smart Data Services panel. The adjacent VinBigdata description also identifies Big Data and AI among its technology areas.

This is a Vingroup corporate statement about GSM in 2024. It supports a group capability and an implementation claim. It does **not** establish a Copenhagen or Green SM Denmark deployment, which rider/ad/service feeds are connected, Copenhagen data access or permissions, or any measured outcome. Treat the Copenhagen dashboard connection as a proposal pending a local data-access and integration check in M1–2.

The downloaded report copy is [vingroup-2025-annual-report-2024-report.pdf](../04_references/vingroup-2025-annual-report-2024-report.pdf), SHA-256 `a45d56457de0ff885d927da8ccb8365346acf13625108c2fd8d32f070adfd3e8`. Cover letter identifies Vingroup Joint Stock Company and its 2024 Annual Report; visual inspection confirms the page 49 panel and wording.

The issuer's English PDF URL is [Vingroup IR CDN](https://ircdn.vingroup.net/storage/Uploads/0_Bao%20cao%20thuong%20nien/2024/ENG_%20Vingroup%20AR24_250418.pdf). Direct retrieval returned HTTP 403 and the web PDF reader rejected its 26 MB size. The saved 7.2 MB English copy was retrieved from [FIINGroup's public report media library](https://cmsv5.fiingroup.vn/medialib/FG/2025/2025-04/2025-04-22/20250422_VIC-250422-Annual-Report-2024.pdf). The active registry's `vingroup-2024` key is a separate Indonesia-launch webpage, not this annual report.

### Candidate registry metadata

- Key: `vingroup-2025-annual-report-2024`; type: `report`; status: `candidate`.
- Organisation: Vingroup Joint Stock Company; publication year: 2025 (disclosure letter, physical p.1, 18 April 2025); title: *Annual Report 2024*.
- Canonical URL: issuer IR CDN above; file: `vingroup-2025-annual-report-2024-report.pdf`.
- Retrieval: `open-access`; `from`: FIINGroup report-media URL above; date: `2026-10-04`.
- Proposed use: Section 8 company-level data capability only. Manual locator: PDF p.26 spread / printed p.49.

Controller registered this source and checked its identity manually against physical p.1 and its claim against physical p.26. See E-207 in the evidence log. The first two PDF pages have no extractable text; the scoped automated mismatch is retained with a hash-bound manual identity acceptance.

## Compact tracking method

Keep the existing targets, denominators and gates. Proposed flow:

**Ad clicks by channel + app booking/settlement + trip/dispatch + referenced help records → proposed dashboard → weekly channel/service actions and monthly cohort/clarity review.**

Measure O1 separately with the same S1-in-area consideration question at the M1–2 baseline and M12 endline. Keep O2 by channel; count only completed paid first trips and remove refunds. Build O3 from first-paid-trip cohorts only after each rider has a full 90-day window. Use accepted bookings and dispatch reason codes for service rates, support timestamps for the 24-hour response measure, in-area requests for offer availability, and the post-trip question for clarity. These sources and rhythms follow integrated-plan §10; the dashboard does not imply they are already connected in Copenhagen.

### Proposed display wording — unapproved

“**TRACKING PROPOSAL** · Ads + app/trip + dispatch/help → dashboard → weekly/monthly decisions”

“**O1** · S1 consideration survey · M1–2 baseline → M12”

“**DATA LINK** · Copenhagen access/integration to verify in M1–2”

Confidence: high that the annual report makes the group-level statement; moderate that it is useful as a poster capability rationale; low that it proves any Copenhagen-level feed or data integration.
