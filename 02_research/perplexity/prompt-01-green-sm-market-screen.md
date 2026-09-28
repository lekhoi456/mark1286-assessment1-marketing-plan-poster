# Perplexity prompt 01: Green SM market screen (eight markets)

Written 27 September 2026 for P2/P3 (D-006, D-018). Purpose: leads for the country context (C1), market prioritisation and target-market evidence (C2) across every market Green SM operates or pilots in. The output is a lead list only: every figure we use is re-checked at its original source, saved as a PDF and logged. Perplexity is never cited.

## How to run

1. Open Perplexity, choose **Deep Research**, paste the prompt below unchanged.
2. When it finishes, copy the **whole answer including its source list** into `output-01-green-sm-market-screen.md` in this folder, verbatim. Do not edit or summarise it.
3. In a separate file `run-01-green-sm-market-screen.md`, note the run date and time, and whether you changed anything (model, follow-up questions). If you ask follow-ups, paste them and their answers into the output file in order, labelled.
4. Tell the agent. The agent writes `reconciliation-01-green-sm-market-screen.md`.

## Prompt (copy everything inside the box)

```text
You are a market research analyst preparing an evidence base for a marketing plan. Research the urban ride-hailing and taxi markets in the eight countries where Green SM operates or runs a pilot as at September 2026. Green SM (formerly Xanh SM until an April 2026 rebrand) is the brand of GSM Green and Smart Mobility JSC, a Vietnamese company founded in 2023 that runs all-electric car taxi, motorbike ride-hailing and delivery services with VinFast vehicles. Its markets and entry dates according to the company: Vietnam (April 2023), Laos (November 2023), Indonesia (December 2024), the Philippines (June 2025), India (June 2026, Delhi NCR), Kazakhstan (June 2026, Almaty), Denmark (July 2026, Copenhagen) and the Netherlands (pilot from September 2026, Amsterdam).

For EACH of the eight countries, report the following, giving a source for every single claim:

1. Market size and growth of ride-hailing and taxi services (revenue, gross bookings or trips), with the year the data refers to, the currency, and the publisher. Say clearly when a figure is a consultancy or market-research estimate rather than official data.
2. The main competitors in the cities where Green SM operates (for example Grab, Gojek, Be, Maxim, inDrive, Uber, Bolt, Yandex Go, Ola, Rapido, BluSmart, Dantaxi, TCA, Viggo, local taxi companies) and any published market-share figures, with date and method.
3. Green SM's own reported facts in that country: launch date and cities, services offered (car, premium, bike, delivery, airport, business), fleet size, number of drivers, trips, pricing or fare positioning, launch promotions, driver employment model. Label all of these as company claims unless an independent source confirms them.
4. Consumer behaviour that matters when people choose a ride-hailing service there: price sensitivity, safety concerns, preference for cars or motorbikes, cash versus digital payment, app usage, attitudes to electric vehicles and sustainability. Cite surveys with sample size, method and year.
5. Regulation that affects ride-hailing or electric taxis: licensing of platforms and drivers, fare rules or caps, driver employment status, foreign ownership limits, and incentives for electric vehicles. Name the law, regulator or decision.
6. Electric-vehicle context: EV share of new car sales and charging infrastructure, with the year.
7. Digital marketing context: internet and smartphone penetration, social media use and the dominant platforms (for example Facebook, TikTok, Zalo, Instagram, LINE, WhatsApp, YouTube), with the year and source.

Then:
A. Give a comparison table with one row per country and these columns: market size (year, source); top three competitors; Green SM entry date and city; biggest regulatory constraint; EV adoption indicator (year); one key consumer insight.
B. List conflicting figures you found between sources, with both sources.
C. List the three biggest evidence gaps for a marketing plan.

Rules:
- Prefer primary and authoritative sources: company press releases and filings, regulators and ministries, national statistics offices, the World Bank, IEA, DataReportal/We Are Social, peer-reviewed research, and reputable news outlets. Avoid unsourced blogs and AI-generated content.
- Give the full URL and publication date for every source. Put the source next to the claim it supports.
- Do not estimate, round up or extrapolate numbers that are not published. If you cannot find something, write "not found".
- Prefer data from 2023 to 2026 and always state the year a figure refers to.
- Keep company claims and independent figures clearly separate.
```

## What the agent will do with the output

- Check every figure that might reach the poster at its original source; save that source as a PDF in `04_references/`, register it and log the claim in `02_research/evidence-log.md`.
- Record agreements, disagreements with our own research and rejected leads in the reconciliation file.
- Drop any figure whose original source cannot be found or saved.
