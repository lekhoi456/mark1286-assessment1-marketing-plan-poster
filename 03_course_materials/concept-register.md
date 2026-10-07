# Concept register: MARK1286 Assessment 1 (module-first)

## Purpose

This register is the module-first concept base required by D-010 and `AGENTS.md` rule 1. Every marketing concept that reaches the poster, the pitch or the Q&A must have an entry here, with the module's own wording and an exact locator. Entries are grouped by the eleven poster panels in `00_brief_and_criteria/poster-headings.txt`, following the lecture mapping in the Assessment 1 Brief: Target Market Analysis (Lectures 3–4); Positioning, Branding, Sales, Budget and Measurement (Lecture 4); Digital Marketing (Lecture 2); Creativity and Innovation (Lectures 1–5, including AI, personalisation, omnichannel, neuromarketing, subscription and revenue models); Alignment (the group's own reflection and research). Student/Business Details needs no marketing concept, and Company/Business Introduction draws mainly on the Week 1 context concepts in section A.

## Format

- Heading: `### ` + backticked concept ID + ` — ` + concept title. `06_workflow/scripts/make_concept_list.py` builds `concept-list.txt` from these headings only.
- Quotations: one or more lines beginning `> `, each copied exactly from the extracted material, immediately followed by a locator line beginning `— ` with the backticked extract slug and slide (`sN`) or page (`p. N`). Semicolons separate several locations; every quoted line must occur in every named location. `module-handbook` is searched as a whole file because its DOCX conversion has no page markers. `06_workflow/scripts/check_register_quotes.py` verifies every quoted line; no `> ` line in this file is commentary.
- Quotations keep the source's spelling (often American) and punctuation. Everything outside a `> ` line is the agent's interpretation, written in UK English.
- `Panels:` lists the poster headings the concept serves. `Use:` is the agent's interpretation of how the concept can be applied, and its limits; it is not a quotation and not module wording. `Definition: not given in module` marks terms that the materials list or exemplify without defining; do not supply a definition for them from memory.
- `Primary work named on slide:` records the "Source:" line printed on the defining slide exactly as printed, as an unverified lead (D-005). Slide bibliographies contain known errors; none of these works may be cited until its PDF is saved in `04_references/`, registered and verified. `none` means the material names no source.
- `Outside:` every entry below is `no` (module material). None is marked outside.

## Adding an outside concept

An outside concept is allowed only when (1) the work's PDF is saved in `04_references/`, registered in `04_references/references.json` and verified with `refs.py verify`; (2) the entry carries the line `Outside: yes`; (3) its quotation's locator names the registry key in backticks followed by the PDF page index (`p. N`), which the checker reads with `pdftotext`. The group should add one only where the module is silent and the panel needs it. No verified outside PDF exists yet, so this register contains no outside entries.

## Status

- Built in P1 on 27 September 2026 by the agent from the Weeks 1–6 extracts, the Week 1, 2, 4 and 5 readings and cases, the handbook and the Assessment 1 Brief (`03_course_materials/index.md`). The module's Weeks 7–9 and Assessment 2 materials were not used.
- Quotations from `w04-tesla` come from OCR text; each quoted line was compared with the page rendered from the Study Hub PDF (110 dpi) and matches it word for word. Other quotations come from PPTX text or a PDF text layer.
- Plan figures are never taken from this register: module statistics and case figures are unverified claims, not evidence (D-005, D-006).
- Awaiting the student's review at the P1 handover. Lecture 6 spoken guidance is recorded separately in `lecture6-guidance.md`.
- Terms the module mentions but that are not registered here, because they add little to this poster: AR/VR in retail (`w01-tutorial` s20), gig and creator economies (`w01-tutorial` s22, only as context), retainer and licence revenue models beyond the listing in `recurring-revenue-model-types`. The module does not teach named budgeting methods, monthly recurring revenue or SMART objectives; these would be outside concepts.

---

## A. Context: future economy (Company/Business Introduction; Alignment with Business Objectives)

### `drivers-of-change` — Drivers of change in the future economy

> Technology, shifting consumer behavior, and evolving business models are key drivers of change.
— `w01-lecture` s20; `w01-tutorial` s23

Panels: Company/Business Introduction; Alignment with Business Objectives; Creativity and Innovation.
Use: a three-part frame for the business context (technology, consumer shift, business model). For an EV ride-hailing platform all three could apply, but each claim about the company needs its own sourced evidence.
Primary work named on slide: none.
Outside: no.

### `sales-and-marketing-future-economy` — Sales and marketing in the future economy

> Sales involves the process of selling products or services, focusing on personalized customer interactions, digital tools, and automation to improve efficiency (Wengler et al., 2021).
— `w01-lecture` s13

> Marketing is about creating demand and building brand awareness.
— `w01-lecture` s13

Panels: Company/Business Introduction; Sales Strategies; Digital Marketing Tactics.
Use: separates the demand-creation role of marketing from the selling process, which helps the poster keep the Digital Marketing and Sales panels distinct. The in-line citations are the slide's, not verified.
Primary work named on slide: Wengler et al., 2021; Harvard Business Review, 2024; Corsaro & Maggioni, 2021 (in-line) — unverified leads.
Outside: no.

### `future-economy-trends` — Future economy landscape: technology, sustainability, demographic shifts

> Rising awareness of environmental issues drives businesses toward sustainable practices.
— `w01-lecture` s14

> Tesla's electric vehicles promote eco-friendly alternatives in the automotive industry.
— `w01-lecture` s14

> The rise of Gen Z consumers has led to greater emphasis on digital-first marketing strategies.
— `w01-lecture` s14

Panels: Company/Business Introduction; Target Market Analysis; Alignment with Business Objectives.
Use: supports a country and industry context paragraph (sustainability concern, EVs, younger digital-first consumers). The module's example is Tesla; any claim about Vietnam or the chosen business must come from separate evidence.
Primary work named on slide: OECD (2025) — unverified lead.
Outside: no.

### `customer-experience-differentiator` — Shifting consumer behaviour: empowered, digital-first, experience over product

> Consumers now have instant access to information, driving demand for transparency and ethical practices.
— `w01-lecture` s17

> Online shopping and social media heavily influence purchasing decisions.
— `w01-lecture` s17

> Customer experience has become a key differentiator, with seamless engagement across channels.
— `w01-lecture` s17

Panels: Target Market Analysis; Positioning Strategy; Creativity and Innovation.
Use: justifies competing on experience (booking, service, app) rather than on the product alone. A claim that experience differentiates a particular brand needs market evidence.
Primary work named on slide: White, K. et al., (2019) — unverified lead.
Outside: no.

### `customer-centric-business-model` — From product-centric to customer-centric models

> Businesses are shifting focus from selling products to providing personalized customer experiences through innovative services.
— `w01-lecture` s19

> Future marketing and sales strategies must be adaptable, data-driven and customer-centric.
— `w01-lecture` s20

Panels: Alignment with Business Objectives; Creativity and Innovation; Company/Business Introduction.
Use: a test for the whole plan: each tactic should be adaptable, data-driven and centred on the customer. Note that `w01-tutorial` s23 prints the same sentence with a comma after "data-driven".
Primary work named on slide: Harvard Business Review (2024) — unverified lead.
Outside: no.

### `platform-business-model` — Platform-based business models

> Traditional industries are being transformed by platform-based businesses and the rise of the gig economy.
— `w01-lecture` s19

> Example: Uber disrupted the transportation industry by creating a platform connecting riders with freelance drivers.
— `w01-lecture` s19

> Platform-based Models (Airbnb, Uber to interact with users)
— `w01-tutorial` s22

Panels: Company/Business Introduction; Creativity and Innovation; Alignment with Business Objectives.
Use: the module's own frame for ride-hailing as a platform model, directly relevant to an app-based transport business. Whether a given company's drivers are freelance or employed is a factual question for P3, not something this concept settles.
Primary work named on slide: Harvard Business Review (2024) (s19); Smith & Jones (2023) (`w01-tutorial` s22) — unverified leads; Smith & Jones (2023) has no Crossref match (D-005).
Outside: no.

### `sustainable-ethical-business-model` — Sustainability and ethical business models

> Companies are adopting sustainable practices and focusing on ethical responsibility through circular economies and CSR initiatives.
— `w01-lecture` s19

> Demand for ethical brands: UK: 73% of consumers prefer sustainable and socially responsible brands.
— `w01-tutorial` s21

Panels: Alignment with Business Objectives; Branding and Identity; Positioning Strategy.
Use: supports a sustainability strand in positioning and long-term objectives. The 73% figure is a UK statistic printed without a checkable source; do not reuse it as evidence.
Primary work named on slide: Harvard Business Review (2024); Corsaro & Maggioni (2021) — unverified leads.
Outside: no.

---

## B. Target Market Analysis (Lectures 3–4)

### `consumer-behaviour` — Consumer behaviour and its influencing factors

> Consumer behaviour refers to the processes involved when individuals or groups select, use, and dispose of products, services, or experiences to satisfy their needs and desires.
— `w03-lecture` s3

> Psychological:
> Social:
> Personal:
— `w03-lecture` s3

Panels: Target Market Analysis.
Use: psychological (motivation, perception, learning), social (culture, reference groups, roles) and personal (age, lifestyle, personality) factors give a checklist for describing a segment's psychographics and behaviour.
Primary work named on slide: Solomon (2022) — unverified lead.
Outside: no.

### `consumer-decision-making-process` — Consumer decision-making process (CDMP)

> The Consumer Decision-Making Process (CDMP) is a five-stage model that describes how consumers go through the steps of recognising a need, searching for information, evaluating options, making a purchase, and evaluating their decision after the purchase.
— `w03-lecture` s5

> 1. Problem Recognition – Realising a Need
> 2. Information Search – Online Research, Reviews
> 3. Evaluation of Alternatives – Comparison
> 4. Purchase Decision – Influenced by UX and Trust
> 5. Post-Purchase Evaluation – Reviews, Returns
— `w03-tutorial` s3

Panels: Target Market Analysis; Digital Marketing Tactics; Sales Strategies.
Use: maps tactics to the stage they serve (for example awareness content at information search, app experience at purchase, reviews at post-purchase). The lecture slide's stage diagram is an image; the tutorial's SmartArt text is the quotable version.
Primary work named on slide: Engel et al., (1995) — unverified lead.
Outside: no.

### `digital-consumer-trends` — Consumer behaviour in the digital age

> 24/7 access to information
> Global connectivity and peer opinions
> Data-driven advertising and AI
> Reduced attention span and instant gratification
— `w03-lecture` s4

> Mobile-First Behaviour
> Social Commerce (Instagram, TikTok)
> Sustainability Consciousness
— `w03-tutorial` s4

Panels: Target Market Analysis; Digital Marketing Tactics.
Use: behavioural characteristics a segment description can test (mobile-first, social commerce, eco-consciousness). The tutorial's percentages are unsourced beyond the slide's source line and must not be quoted as facts.
Definition: not given in module (the terms are listed with examples).
Primary work named on slide: Kotler et al., (2021) (`w03-lecture` s4); PwC (2023) (`w03-tutorial` s4) — unverified leads.
Outside: no.

### `generational-digital-behaviour` — Generational digital behaviour

> Gen Z | Visual-first, social natives
— `w03-lecture` s8

> Millennials | Experience-focused
— `w03-lecture` s8

Panels: Target Market Analysis; Digital Marketing Tactics.
Use: an age-cohort lens for demographic segmentation and channel choice (Gen Z, Millennials, Gen X, Boomers). Cohort traits are generalisations; the group's segment profile should rest on market data for its own country.
Primary work named on slide: Fromm & Read (2018) — unverified lead.
Outside: no.

### `understanding-customer-needs` — Understanding customer needs

> In sales fundamentals, understanding customer needs is the starting point for any sales interaction.
— `w04-lecture` s5

> Research (Need, Want & Demand): Conduct surveys (offline-online) to understand what customers value most in a car, such as technology, speed, eco-friendliness, or design.
— `w04-tutorial` s4

Panels: Target Market Analysis; Sales Strategies.
Use: the first component of the Lecture 4 marketing plan; ties segment needs to the offer. The group has no primary survey data unless it collects some; secondary evidence must be labelled as such.
Primary work named on slide: Ries & Trout (2001) — unverified lead.
Outside: no.

### `customer-personas` — Customer personas

> Customer Personas: For example, a persona might be a 35-year-old tech-savvy urban professional who values innovation and eco-conscious choices—an ideal candidate for BMW’s electric iSeries.
— `w04-tutorial` s4

Panels: Target Market Analysis; Branding and Identity.
Use: a persona per priority segment makes demographic, psychographic and behavioural traits concrete on a poster. A persona is illustrative; it must be consistent with the evidence, not invented statistics.
Definition: not given in module (shown by example only).
Primary work named on slide: Ries & Trout (2001) — unverified lead.
Outside: no.

### `target-market-analysis` — Target market analysis

> Understanding your target market is crucial to ensuring that your marketing strategy speaks directly to the right audience.
— `w04-lecture` s6

> Segmentation: Demographic, psychographic, and behavioral characteristics.
> Prioritization: How did you segment and prioritize your target markets?
— `w04-lecture` s6

Panels: Target Market Analysis.
Use: the lecture restates the brief's three questions (identify, characterise, prioritise), so the panel should show all three explicitly.
Primary work named on slide: Smith (1956) — unverified lead.
Outside: no.

### `stp-model` — Segmentation, targeting and positioning (STP) model

> The Segmentation, Targeting, and Positioning (STP) model is a critical framework in marketing that helps businesses to focus on the right customers and effectively communicate their brand's value.
— `w04-lecture` s7

> 2. Target Market - Segmentation, Targeting, and Positioning (STP) Model
— `w04-lecture` s4; `w04-tutorial` s3

Panels: Target Market Analysis; Positioning Strategy.
Use: the backbone linking the Target Market and Positioning panels; show the logic from segments to chosen targets to position.
Primary work named on slide: Ries & Trout (2001) (s7); Kotler & Armstrong (2018) (s4, tutorial s3) — unverified leads.
Outside: no.

### `market-segmentation` — Market segmentation

> Segmentation is the process of dividing a broad consumer or business market, typically consisting of existing and potential customers, into sub-groups of consumers based on some type of shared characteristics.
— `w04-lecture` s7

> Dividing the market into distinct groups with common needs or characteristics.
— `w04-tutorial` s5

Panels: Target Market Analysis.
Use: defines the segmentation step; pair it with `segmentation-bases`. Both consumer and business markets are covered by the definition, which fits a business with consumer and corporate services.
Primary work named on slide: Ries & Trout (2001) — unverified lead.
Outside: no.

### `segmentation-bases` — Segmentation bases: demographic, geographic, psychographic, behavioural

> - Demographic: Age, income, occupation - Geographic: Urban vs. rural, region - Psychographic: Lifestyle, personality - Behavioral: Brand loyalty, usage
— `w04-tutorial` s5

> This includes segmenting the market based on characteristics like demographics (age, gender), psychographics (lifestyle, values), and behavioral traits (purchasing habits).
— `w04-lecture` s6

> Businesses divide consumers into groups based on psychographics, demographics, and geographics to create targeted marketing strategies.
— `w01-lecture` s18

> Segmentation: Tesla segments the market based on demographics (income level, tech affinity,
— `w04-tesla` p. 1

Panels: Target Market Analysis.
Use: the brief asks for demographic, psychographic and behavioural characteristics; geographic bases (city, urban/rural) are also taught and may matter for a transport service. The Tesla line is OCR, visually checked against the rendered page.
Primary work named on slide: Ries & Trout (2001) (`w04-tutorial` s5); Smith (1956) (`w04-lecture` s6); Theodorakopoulos & Theodoropoulou (2024) (`w01-lecture` s18) — unverified leads. Tesla case: none (case by Dr Muhammad Arsalan Nazir).
Outside: no.

### `targeting` — Targeting

> Targeting involves selecting which segments the company will serve. It is essential to evaluate the potential of each segment and choose the ones that align best with the company's resources, capabilities, and objectives.
— `w04-lecture` s7

> Selecting which segments to serve based on potential and strategic fit.
— `w04-tutorial` s5

> Targeting: Tesla primarily targets affluent, eco-conscious consumers, early tech adopters, and
— `w04-tesla` p. 1

Panels: Target Market Analysis; Alignment with Business Objectives.
Use: the module's prioritisation criteria are segment potential and fit with resources, capabilities and objectives; the poster should state why the priority segment wins on those criteria.
Primary work named on slide: Ries & Trout (2001) — unverified lead. Tesla case: none.
Outside: no.

### `targeting-strategies` — Differentiated and concentrated marketing

> Differentiated Marketing: Multiple models for different segments (e.g., BMW 3 Series, X5, i Series) / Concentrated Marketing: Focus on premium segment
— `w04-tutorial` s5

Panels: Target Market Analysis; Positioning Strategy.
Use: a business with several service lines could argue a differentiated approach (different offers per segment) or a concentrated one (one priority segment). The slide gives only examples.
Definition: not given in module.
Primary work named on slide: Ries & Trout (2001) — unverified lead.
Outside: no.

### `consumer-insights-and-big-data` — Consumer insights and big data analytics

> Consumer Insights Analysing customer behaviors, preferences, and feedback to understand their needs and enhance marketing strategies.
— `w01-lecture` s15

> Big Data & Analytics Using large volumes of structured and unstructured data to identify patterns, trends, and actionable insights for business decision-making.
— `w01-lecture` s15

Panels: Target Market Analysis; Measurement and Evaluation; Creativity and Innovation.
Use: justifies using platform data (trips, app behaviour, feedback) for segmentation and optimisation. Claims about what data a real company holds or uses need evidence; privacy limits apply.
Primary work named on slide: Smith & Jones (2023) — unverified lead; no Crossref match (D-005).
Outside: no.

---

## C. Positioning Strategy (Lecture 4)

### `positioning` — Positioning

> Positioning refers to how a brand or product is perceived in the minds of consumers in relation to its competitors.
— `w04-lecture` s7

> Defining how the brand is perceived in customers’ minds (USP) relative to competitors.
— `w04-tutorial` s5

> Positioning: Tesla’s positioning strategy emphasizes innovation, luxury, and sustainability.
— `w04-tesla` p. 1

Panels: Positioning Strategy; Branding and Identity.
Use: position is defined relative to competitors, so the panel needs a named competitor frame (for example a perceptual comparison). The Tesla line is OCR, visually checked.
Primary work named on slide: Ries & Trout (2001) — unverified lead. Tesla case: none.
Outside: no.

### `unique-value-proposition` — Unique value proposition (UVP)

> Effective positioning helps a brand to stand out and deliver a unique value proposition (UVP) that resonates with the target audience.
— `w04-lecture` s7

> Clear Value Proposition: Tesla emphasizes the long-term savings and environmental benefits of EV
— `w04-tesla` p. 2

Panels: Positioning Strategy; Sales Strategies.
Use: the brief asks for a UVP that resonates with the target audience; the Tesla case models a UVP built on savings and environmental benefit, which is close to an EV service's argument but must be supported by the group's own evidence. The module does not define "UVP" further. The Tesla line is OCR, visually checked.
Primary work named on slide: Ries & Trout (2001) — unverified lead. Tesla case: none.
Outside: no.

### `positioning-strategies` — Benefit, attribute and competitor positioning

> - Benefit Positioning: Ultimate driving experience - Attribute Positioning: Engineering, innovation, design - Competitor Positioning: Positioned as more performance-focused than Audi or Mercedes
— `w04-tutorial` s5

Panels: Positioning Strategy.
Use: three routes for the positioning statement (lead with a benefit, an attribute or a comparison with a named rival). Competitor comparisons need verified competitor facts.
Definition: not given in module (named with BMW examples only).
Primary work named on slide: Ries & Trout (2001) — unverified lead.
Outside: no.

### `positioning-statement` — Positioning statement

> Have you defined a clear positioning statement for the brand/product/service?
— `w06-lecture` s5; `w05-tutorial` s13

Panels: Positioning Strategy.
Use: the brief requires one, but no Weeks 1–6 slide gives a template or definition. The group may write a plain statement built from registered concepts (target, UVP, competitor frame); a named external template would be an outside concept.
Definition: not given in module.
Primary work named on slide: none.
Outside: no.

---

## D. Branding and Identity (Lecture 4)

### `brand-identity` — Brand identity

> Brand identity refers to the visual and verbal elements that create a brand’s unique image.
— `w04-lecture` s8

> Logo, colour scheme, and messaging.
— `w04-lecture` s8

Panels: Branding and Identity.
Use: the brief's three required elements (logo, colour scheme, messaging) are exactly the slide's list; the panel should cover each and show alignment with positioning and target market.
Primary work named on slide: Kapferer (2012) — unverified lead.
Outside: no.

### `brand-identity-components` — Brand identity components

> | Logo |
> | Color Scheme |
> | Typography |
> | Slogan/Tagline |
> | Brand Voice |
> | Visual Style |
— `w04-tutorial` s6

Panels: Branding and Identity.
Use: a six-row table (logo, colour, typography, tagline, voice, visual style) is a ready poster structure. If the group analyses an existing brand's identity, each element must be observed from the brand's own materials.
Primary work named on slide: Kapferer (2012) — unverified lead.
Outside: no.

### `brand-strategy-alignment` — Brand strategy: emotional connection and alignment with the target market

> Creating emotional connections through visual and verbal identity.
> Aligning brand identity with the target market’s values and preferences.
— `w04-lecture` s8

> It’s vital that the branding aligns with the target audience’s expectations and the positioning strategy, helping to foster trust and emotional engagement.
— `w04-lecture` s8

Panels: Branding and Identity; Positioning Strategy; Alignment with Business Objectives.
Use: the rubric tests whether branding is "aligned with the target audience"; this is the module's wording for that test.
Primary work named on slide: Kapferer (2012) — unverified lead.
Outside: no.

### `emotional-neuro-branding` — Emotional (neuro) branding

> Emotional (Neuro) Branding: BMW creates an emotional connection with customers through the driving experience, associating ownership with prestige, confidence, and passion.
— `w04-tutorial` s6

Panels: Branding and Identity; Creativity and Innovation.
Use: links branding to the neuromarketing trend listed in the brief; see `neuromarketing`.
Definition: not given in module (BMW example only).
Primary work named on slide: Kapferer (2012) — unverified lead.
Outside: no.

### `consistent-brand-messaging` — Consistent brand messaging

> Consistent Brand Messaging: Whether it’s an ad, a website, or a dealership visit, BMW communicates performance, innovation, and luxury.
— `w04-tutorial` s6

> Ensuring the same brand tone and message across social media, websites, and in-store experiences.
— `w03-lecture` s9

Panels: Branding and Identity; Digital Marketing Tactics.
Use: the brief asks for "brand messaging"; the module treats consistency across touchpoints as the standard. Supports a short message hierarchy used across app, social media and vehicles.
Primary work named on slide: Kapferer (2012) (`w04-tutorial` s6); Verhoef et al., (2017) (`w03-lecture` s9) — unverified leads.
Outside: no.

### `lifestyle-marketing` — Lifestyle marketing

> Lifestyle Marketing: The brand doesn't just sell cars—it sells a lifestyle of sophistication, speed, and success.
— `w04-tutorial` s6

Panels: Branding and Identity; Positioning Strategy.
Use: a possible branding angle (selling a way of living, such as a green urban lifestyle) if it fits the chosen segment.
Definition: not given in module (BMW example only).
Primary work named on slide: Kapferer (2012) — unverified lead.
Outside: no.

### `brand-equity` — Brand equity

> Brand Management: Proficiency in building, managing, and enhancing brand equity through effective branding strategies, positioning, and storytelling techniques.
— `module-handbook`

Panels: Branding and Identity; Alignment with Business Objectives.
Use: the handbook names brand equity as a skill the module develops, but no Weeks 1–6 slide defines or measures it. Use the term only loosely, or register a verified outside source if the poster needs a definition.
Definition: not given in module.
Primary work named on slide: none (handbook employability list).
Outside: no.

---

## E. Digital Marketing Tactics (Lecture 2)

### `digital-marketing` — Digital marketing in the future economy

> Digital marketing refers to using emerging technologies, data insights, and digital channels to promote brands.
— `w02-lecture` s3

Panels: Digital Marketing Tactics.
Use: the umbrella definition for the panel.
Primary work named on slide: Chaffey & Ellis-Chadwick (2019) — unverified lead.
Outside: no.

### `key-digital-marketing-strategies` — Key digital marketing strategies

> Social media marketing
> Content marketing
> Influencer marketing
> Email marketing
> SEO (Search Engine Optimization)
> PPC (Pay-Per-click)
> Customer Engagement and Support
> Cloud-Based Automation Tools
— `w02-lecture` s5; `w02-tutorial` s6

Panels: Digital Marketing Tactics.
Use: the module's full channel menu. The poster should choose a justified subset for the target segment rather than list all eight.
Primary work named on slide: Chaffey & Ellis-Chadwick (2019) — unverified lead.
Outside: no.

### `social-media-marketing` — Social media marketing (SMM)

> Social media marketing involves creating engaging content, running paid ads, and building community connections to strengthen brand presence and customer loyalty.
— `w02-lecture` s6

> Organic reach via posts and community building.
> Paid ads (sponsored posts, stories, etc.) for targeted visibility.
> Influencer collaborations and user-generated content.
— `w02-lecture` s6

Panels: Digital Marketing Tactics.
Use: organic, paid and influencer/UGC routes; the slide's cons (content load, uncertain paid ROI, clutter) are ready-made limits for the Q&A.
Primary work named on slide: Nazir et al., (2025) — unverified lead.
Outside: no.

### `content-marketing` — Content marketing

> Creating valuable, relevant content to attract and engage target audiences, positioning your brand as a thought leader.
— `w02-lecture` s7

> Content that addresses customer pain points and interests.
— `w02-lecture` s7

Panels: Digital Marketing Tactics.
Use: educational content (for example explaining EV benefits) suits a brand that must change habits; the slide warns that results are slow and content needs continual updating.
Primary work named on slide: Krowinska et al., (2023) — unverified lead.
Outside: no.

### `influencer-marketing` — Influencer marketing and influencer types

> Influencer marketing leverages the credibility and trust of individuals who have a large following on social media to endorse brands or products.
— `w02-lecture` s8

> Macro-Influencers: Celebrities or public figures with a large following.
> Micro-Influencers: Niche influencers with smaller, highly engaged audiences.
> Nano-Influencers: Extremely small, but often hyper-targeted audiences.
— `w02-lecture` s8

Panels: Digital Marketing Tactics; Budget and Resource Allocation.
Use: tiering (macro, micro, nano) is a budget decision as well as a reach decision. The slide's cons (cost, authenticity risk, hard-to-measure ROI) should appear in the risk discussion.
Primary work named on slide: Yesiloglu & Costello (2021) — unverified lead; the handbook's reading list gives the same book title as Costello and Yesiloglu, 2025.
Outside: no.

### `user-generated-content` — User-generated content (UGC)

> Campaign Example: #AsSeenOnMe—encouraging customers to share their outfits,
> leveraging user-generated content.
— `w02-mini-case-studies` p. 1

Panels: Digital Marketing Tactics; Creativity and Innovation.
Use: a low-cost engagement tactic (riders sharing trips or reviews). The module shows it by example only.
Definition: not given in module.
Primary work named on slide: none (mini case by Dr Muhammad Arsalan Nazir, May 2025).
Outside: no.

### `email-marketing` — Email marketing

> Email marketing involves sending targeted messages via email to nurture leads, retain customers, promote products/services, and build relationships.
— `w02-lecture` s9

Panels: Digital Marketing Tactics; Sales Strategies.
Use: retention and lead-nurture channel; the slide notes the need for an opted-in list, which is also a data-protection constraint.
Primary work named on slide: Chaffey & Ellis-Chadwick (2019) — unverified lead.
Outside: no.

### `search-engine-optimisation` — Search engine optimisation (SEO)

> Optimizing your website and content to rank higher in search engine results pages (SERPs) for targeted keywords.
— `w02-lecture` s10

> This cost-effective strategy increases website traffic by optimizing content for relevant keywords typed into search engines.
— `w02-tutorial` s12

Panels: Digital Marketing Tactics.
Use: the brief names SEO explicitly. For an app-first service SEO supports discovery searches and corporate enquiries; the slide says results take time.
Primary work named on slide: Rushing (2017) — unverified lead.
Outside: no.

### `pay-per-click` — Pay-per-click advertising (PPC)

> Running paid advertisements on search engines or social media platforms targeting specific keywords and audience segments.
— `w02-lecture` s11

> PPC offers immediate visibility for businesses willing to pay for ad space, and it targets consumers who are actively searching for products or services.
— `w02-lecture` s11

Panels: Digital Marketing Tactics; Budget and Resource Allocation; Measurement and Evaluation.
Use: immediate, measurable reach at a continuing cost; pair with `click-through-rate`, `cost-per-click` and `return-on-ad-spend`.
Primary work named on slide: Chaffey & Ellis-Chadwick (2019) — unverified lead.
Outside: no.

### `targeted-advertising` — Targeted advertising

> Targeted Advertising Delivering ads tailored to specific audiences based on demographics, online behavior, or purchase history.
— `w01-lecture` s15

Panels: Digital Marketing Tactics; Target Market Analysis.
Use: connects segmentation bases to paid media audiences.
Primary work named on slide: Smith & Jones (2023) — unverified lead; no Crossref match (D-005).
Outside: no.

### `customer-engagement-and-support` — Customer engagement and support

> Strategies to proactively engage customers and provide support across digital channels, creating positive experiences and building brand loyalty.
— `w02-lecture` s12

> Chatbots and AI-powered customer service.
> Real-time customer support through live chat, social media, and email.
> Community-building and customer forums.
— `w02-lecture` s12

Panels: Digital Marketing Tactics; Sales Strategies; Creativity and Innovation.
Use: service quality is part of the offer for a transport platform; the slide warns of investment cost and automation feeling impersonal.
Primary work named on slide: Rushing (2017) — unverified lead.
Outside: no.

### `ai-chatbots` — AI chatbots in customer service and sales

> Both brands leverage chatbots and AI-powered automation for basic customer queries
— `w02-mini-case-studies` p. 3

> Automation in Sales (CRM, Chatbots)
— `w01-tutorial` s20

Panels: Creativity and Innovation; Digital Marketing Tactics; Sales Strategies.
Use: a concrete AI application for the innovation panel (booking help, complaints triage). Whether the chosen company already uses chatbots is a fact to verify.
Definition: not given in module.
Primary work named on slide: none (mini case); Ali et al., (2021) (`w01-tutorial` s20) — unverified lead; the tutorial's reference list dates Ali et al. 2023.
Outside: no.

### `marketing-automation` — Cloud-based marketing automation tools

> Tools that automate repetitive digital marketing tasks such as email campaigns, social media posting, and lead generation to improve efficiency.
— `w02-lecture` s13

Panels: Digital Marketing Tactics; Budget and Resource Allocation.
Use: automation (welcome emails, scheduling, lead nurturing, CRM) reduces staff time; the slide notes learning curve and cost for small firms.
Primary work named on slide: Yesiloglu & Costello (2021) — unverified lead.
Outside: no.

### `integrated-digital-marketing` — Integration of digital marketing strategies

> Combining different digital marketing strategies to create a seamless and cohesive brand experience across multiple touchpoints.
— `w02-lecture` s14

> Integration of digital strategies are critical for long-term success.
— `w02-lecture` s15

Panels: Digital Marketing Tactics; Alignment with Business Objectives.
Use: argues for a coordinated channel mix with shared messaging and cross-channel tracking; the slide lists resource intensity and brand dilution as risks. The statistics on `w02-tutorial` s16 are unsourced beyond the slide and are not evidence.
Primary work named on slide: Nazir et al., (2025) — unverified lead.
Outside: no.

### `developed-vs-developing-market-trends` — Digital marketing trends in developed and developing markets; localisation

> Developing markets are innovating within constraints — focusing on mobile-first, social commerce, cost-effective influencer marketing, and localized digital strategies.
— `w02-tutorial` s3

> How can global brands localize their influencer marketing while maintaining a strong global identity?
— `w02-tutorial` s9

Panels: Digital Marketing Tactics; Company/Business Introduction; Target Market Analysis.
Use: supports adapting tactics to country context (the brief asks for country context and the business operates in several countries). The slide's classification of countries is the slide's, not verified.
Primary work named on slide: Nazir et al., (2025) (s3); none on s9 — unverified lead.
Outside: no.

### `social-influence-and-ewom` — Social influence and eWOM (electronic word of mouth)

> Social influence refers to how people’s thoughts, feelings, and actions are affected by others - especially through opinions, recommendations, and behaviours observed in social settings (offline and online).
— `w03-lecture` s7

> eWOM is any positive or negative information about a brand, product, or service shared by consumers online, including:
— `w03-lecture` s7; `w03-tutorial` s6

Panels: Digital Marketing Tactics; Target Market Analysis; Measurement and Evaluation.
Use: reviews, posts and influencer content shape the information-search stage; referral schemes and review management are the practical levers. The tutorial's "74%" figure is not evidence.
Primary work named on slide: Boerman et al., (2017) — unverified lead; the slide reference list prints no article title.
Outside: no.

---

## F. Sales Strategies (Lecture 4)

### `sales-fundamentals` — Sales fundamentals

> Sales Fundamentals are the essential principles and techniques used in selling products or services effectively.
— `w04-lecture` s3

> The core focus is on understanding the sales process and each stage within it.
— `w04-lecture` s3

Panels: Sales Strategies.
Use: frames the Sales panel as process plus relationships plus closing, the Lecture 4 structure.
Primary work named on slide: Kotler & Armstrong (2018) — unverified lead.
Outside: no.

### `modern-selling-techniques` — Modern selling techniques

> Modern Selling Techniques reflect updated, innovative approaches to sales in today’s dynamic business environment.
— `w04-lecture` s3

> They use tools like automation, AI, data analytics, and social media to improve customer engagement.
— `w04-lecture` s3

Panels: Sales Strategies; Creativity and Innovation.
Use: justifies app-based, data-driven and automated selling alongside face-to-face corporate sales.
Primary work named on slide: Kotler & Armstrong (2018) — unverified lead.
Outside: no.

### `sales-process` — Sales process: lead generation, prospecting, conversion

> Lead Generation - Identifying potential customers.
> Prospecting - Building relationships with prospects.
> Conversion - Turning prospects into customers.
— `w04-lecture` s9

> | Conversion Strategy | Turning potential customers (leads) into actual buyers.
— `w04-tutorial` s7

Panels: Sales Strategies.
Use: the brief names these three stages, so the panel should show one concrete action for each, per segment (for example consumer app sign-up versus corporate account). The Week 4 lecture's slide 11 also shows a seven-step "Sales Cycle" graphic, but it is an image not captured in the extract and is therefore not quoted here.
Primary work named on slide: Churchill & Peter (2015) — unverified lead.
Outside: no.

### `sales-channels` — Sales channels

> What channels will you use to reach customers? - Online stores, direct sales, social media, partnerships.
— `w04-lecture` s9

> | Sales Channels | Use of diverse platforms to reach and sell to customers |
— `w04-tutorial` s7

Panels: Sales Strategies; Budget and Resource Allocation.
Use: channel list for the panel (app or online, direct B2B sales, social media, partnerships).
Primary work named on slide: Churchill & Peter (2015) — unverified lead.
Outside: no.

### `relationship-building` — Building relationships and effective communication

> One of the core components of sales is relationship-building.
— `w04-lecture` s9

> In sales fundamentals, persuasive communication techniques, such as active listening, problem-solving, and addressing objections, are key.
— `w04-lecture` s9

Panels: Sales Strategies.
Use: especially relevant to corporate and premium accounts; also links to `relationship-selling` under subscriptions.
Primary work named on slide: Churchill & Peter (2015) — unverified lead.
Outside: no.

### `social-selling` — Social selling

> Modern techniques may include digital tools like email marketing, live chat, social selling (via platforms like LinkedIn), and webinars to engage customers in a more personalized and convenient way.
— `w04-lecture` s9

Panels: Sales Strategies; Digital Marketing Tactics.
Use: a B2B prospecting route (for example business transport accounts via LinkedIn).
Definition: not given in module.
Primary work named on slide: Churchill & Peter (2015) — unverified lead.
Outside: no.

### `selling-techniques` — Sales techniques: consultative, value-based and personalised selling

> | Sales Techniques | Approaches used to persuade customers and close sales. | Consultative selling, value-based selling, personalized offers, and product demos at showrooms. |
— `w04-tutorial` s7

> | Value-Based Selling | Focusing on the value delivered (performance, brand prestige, innovation) rather than just price |
— `w04-tutorial` s7

> | Personalized Selling | Tailoring the pitch based on customer preferences and lifestyle |
— `w04-tutorial` s7

Panels: Sales Strategies.
Use: the rubric asks for "the types of strategies and sales techniques proposed"; value-based selling suits a service that is not the cheapest option. Consultative selling is listed but not defined.
Definition: not given in module for consultative selling.
Primary work named on slide: Churchill & Peter (2015) — unverified lead.
Outside: no.

### `crm` — Customer relationship management (CRM)

> CRM Tools and Predictive Analytics: CRM tools centralize customer data, and predictive analytics helps forecast sales trends and customer needs.
— `w01-lecture` s16

> | CRM and Follow-Up | Maintaining long-term relationships through continuous engagement |
— `w04-tutorial` s7

> Integrate CRM systems for smarter relationship management and long-term value creation.
— `w04-lecture` s3

Panels: Sales Strategies; Measurement and Evaluation; Budget and Resource Allocation.
Use: CRM links acquisition, retention and KPI tracking; the Week 4 sample budget gives CRM its own lines.
Primary work named on slide: Ali, O. et al. (2023) (`w01-lecture` s16); Churchill & Peter (2015); Kotler & Armstrong (2018) — unverified leads.
Outside: no.

### `sales-marketing-integration` — Integration of sales and marketing; digital transformation in sales

> Integration of Sales and Marketing Efforts: Aligning sales and marketing teams using shared tools and data to ensure seamless collaboration and unified messaging.
— `w01-lecture` s16

> Virtual Sales Teams and Remote Selling: Sales teams leverage digital tools to engage clients, present solutions, and close deals without needing in-person interactions.
— `w01-lecture` s16

Panels: Sales Strategies; Alignment with Business Objectives.
Use: supports one funnel shared by marketing and sales, and remote selling to business clients.
Primary work named on slide: Ali, O. et al. (2023) — unverified lead.
Outside: no.

### `customer-acquisition-tactics` — Customer acquisition tactics

> | Customer Acquisition Tactics | Specific actions to attract and win new customers. | Loyalty programs, trade-in bonuses, referral discounts, influencer partnerships, and digital CRM tools. |
— `w04-tutorial` s7

Panels: Sales Strategies; Budget and Resource Allocation.
Use: the brief asks how sales will drive "customer acquisition"; referral discounts and partnerships are low-cost options for a ride-hailing app.
Primary work named on slide: Churchill & Peter (2015) — unverified lead.
Outside: no.

### `after-sales-service` — After-sales service

> | After-Sales Service | Building loyalty post-purchase through services, events, and support |
— `w04-tutorial` s7

Panels: Sales Strategies; Measurement and Evaluation.
Use: for a service business, the equivalent is post-trip support and follow-up that drives retention.
Primary work named on slide: Churchill & Peter (2015) — unverified lead.
Outside: no.

### `direct-to-consumer-sales` — Direct-to-consumer sales model

> Tesla uses a direct-to-consumer sales model, bypassing traditional dealerships.
— `w04-tesla` p. 1

Panels: Sales Strategies; Company/Business Introduction.
Use: an app platform already sells directly to users; the concept helps explain the channel choice. OCR line, visually checked against the rendered page.
Definition: not given in module beyond the Tesla case.
Primary work named on slide: none (case by Dr Muhammad Arsalan Nazir, May 2025).
Outside: no.

### `closing-techniques` — Sale closing techniques

> Sales fundamentals emphasize the importance of closing techniques, including asking for the sale, creating a sense of urgency, and offering incentives.
— `w04-lecture` s11

> | Assumptive Close |
> | Urgency Close |
> | Summary Close |
> | Alternative Close |
> | Direct Close |
— `w04-tutorial` s9

> Tesla employs a low-pressure, transparent sales strategy.
— `w04-tesla` p. 2

Panels: Sales Strategies.
Use: for an app, closing takes the form of limited-time offers (urgency), plan choices (alternative) and clear prices; for B2B accounts the named closes apply directly. Tesla line is OCR, visually checked.
Primary work named on slide: Kotler & Keller (2016) — unverified lead; the slide reference list prints the authors in a malformed way ("Kotler & Keller, K. L.").
Outside: no.

### `soft-selling` — Soft selling and social proof

> Modern selling includes closing strategies like ‘soft’ selling, which might involve allowing the customer to make decisions at their own pace, using customer testimonials, case studies, and leveraging online reviews to influence their choice.
— `w04-lecture` s11

Panels: Sales Strategies; Digital Marketing Tactics.
Use: reviews and testimonials as closing aids, linked to `social-influence-and-ewom`.
Primary work named on slide: Kotler & Keller (2016) — unverified lead.
Outside: no.

---

## G. Budget and Resource Allocation (Lecture 4)

### `budget-and-resource-allocation` — Budget and resource allocation

> Effective budgeting and resource allocation are critical for implementing your marketing strategy.
— `w04-lecture` s10

> Financial resources: Advertising, promotions, technology.
> Human resources: Sales team, digital marketing specialists.
— `w04-lecture` s10

Panels: Budget and Resource Allocation.
Use: the budget should show both money and people. The lecture names no budgeting method (such as percentage of sales); any method the group uses beyond a justified line-item plan would be an outside concept.
Primary work named on slide: Kotler & Armstrong (2018) — unverified lead.
Outside: no.

### `marketing-budget-line-items` — Line-item marketing budget with monitoring and contingency

> | Monitoring & Evaluation | Tracking campaign performance, sales analysis, and customer feedback | £40,000 |
> | Contingency Fund | Allocation for emergency adjustments or emerging opportunities | £30,000 |
> | Total Estimated Budget |  | £1,200,000 |
— `w04-tutorial` s8

Panels: Budget and Resource Allocation; Measurement and Evaluation.
Use: the module's model is a table of resource lines with descriptions, including monitoring and a contingency line; the rubric also asks for a visual budget such as a pie chart. Source defect: the slide's twelve lines sum to £1,330,000, not the stated £1,200,000 (checked on the rendered slide). Do not copy the example's figures; the group's own budget must add up.
Primary work named on slide: Kotler & Armstrong (2018) — unverified lead.
Outside: no.

### `strategic-budget-priorities` — Budget prioritisation towards high-impact areas

> Tesla spends less on traditional advertising and instead allocates its resources
> to digital marketing, influencer partnerships, and customer experience enhancements. The direct-
— `w04-tesla` p. 2

Panels: Budget and Resource Allocation; Digital Marketing Tactics.
Use: the case argues for weighting spend towards digital, influencer and experience lines; the group must justify its own weights with evidence. OCR lines, visually checked.
Definition: not given in module beyond the Tesla case.
Primary work named on slide: none (case by Dr Muhammad Arsalan Nazir).
Outside: no.

---

## H. Measurement and Evaluation (Lecture 4, plus Week 2 case)

### `kpis-and-metrics` — Key performance indicators (KPIs) and metrics

> KPIs (Key Performance Indicators) – your sales goals - provide measurable data that informs decision-making and strategy adjustments.
— `w04-lecture` s12

> (Impressive numbers) Conversion rate, customer lifetime value, sales growth, and ROI.
— `w04-lecture` s12

Panels: Measurement and Evaluation; Alignment with Business Objectives.
Use: KPIs are tied to goals, which is the rubric's "aligned with objectives" test. The Week 4 tutorial table labels some measures KPI and others metric; the lecture's KPI-versus-metric graphic is an image and is not quoted.
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `campaign-tracking-and-analytics` — Tracking and analysing campaign performance

> Use analytics tools to monitor the performance of marketing campaigns.
> Make data-driven decisions to optimize future strategies.
— `w04-lecture` s12

Panels: Measurement and Evaluation.
Use: answers the brief's "how will you track and analyse" question; the poster should name the tool and review rhythm for each KPI (workspace rule 8).
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `sales-conversion-rate` — Sales conversion rate

> | KPI | Sales Conversion Rate | Measures the percentage of leads that convert into actual sales. |
— `w04-tutorial` s10

> Lead Conversion Rate: Monitoring how well Tesla turns leads into actual customers.
— `w04-tesla` p. 2

Panels: Measurement and Evaluation; Sales Strategies.
Use: fits app funnels (downloads to first ride) and B2B leads to signed accounts. Tesla line is OCR, visually checked.
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `customer-acquisition-cost` — Customer acquisition cost (CAC)

> | KPI | Customer Acquisition Cost (CAC) | Measures the cost of acquiring a new customer, including marketing and sales efforts. |
— `w04-tutorial` s10

> Customer Acquisition Cost (CAC): Measuring the efficiency of marketing spend by tracking how
> much Tesla spends to acquire each new customer.
— `w04-tesla` p. 2

Panels: Measurement and Evaluation; Budget and Resource Allocation.
Use: links the budget to acquisition targets; the tutorial's BMW example gives the calculation (total spend divided by new customers). Tesla lines are OCR, visually checked.
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `customer-retention-rate` — Customer retention rate

> | KPI | Customer Retention Rate | Measures how often customers return to purchase or service again. |
— `w04-tutorial` s10

Panels: Measurement and Evaluation; Creativity and Innovation.
Use: central for a membership or subscription offer; pair with `churn`.
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `sales-growth` — Sales growth

> | KPI | Sales Growth | Measures the increase in sales over a period. |
— `w04-tutorial` s10

Panels: Measurement and Evaluation; Alignment with Business Objectives.
Use: the headline growth KPI; specify the period (month-over-month or year-over-year, as in the BMW example).
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `average-deal-size` — Average deal size

> | Metric | Average Deal Size | Tracks the average value of each sale, helping BMW assess customer spending. |
— `w04-tutorial` s10

Panels: Measurement and Evaluation.
Use: for a ride service the analogue is average fare or order value; say so explicitly if adapted.
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `lead-response-time` — Lead response time

> | Metric | Lead Response Time | Tracks how quickly BMW’s sales team follows up with leads. |
— `w04-tutorial` s10

Panels: Measurement and Evaluation; Sales Strategies.
Use: relevant to B2B enquiries (business transport accounts).
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `customer-satisfaction-csat` — Customer satisfaction (CSAT)

> | Metric | Customer Satisfaction (CSAT) | Measures customer satisfaction after the sales process and service. |
— `w04-tutorial` s10

Panels: Measurement and Evaluation.
Use: post-trip ratings or surveys; the module frames CSAT as post-purchase.
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `customer-lifetime-value` — Customer lifetime value (CLV)

> (Impressive numbers) Conversion rate, customer lifetime value, sales growth, and ROI.
— `w04-lecture` s12

> This emphasis on retention often increases customer lifetime value.
— `w05-lecture` s7

Panels: Measurement and Evaluation; Creativity and Innovation.
Use: links retention and membership plans to value over time. The module names CLV but gives no formula.
Definition: not given in module.
Primary work named on slide: Econsultancy (2018) (s12); Zahay et al., (2022) (`w05-lecture` s7) — unverified leads.
Outside: no.

### `return-on-investment` — Return on investment (ROI)

> A well-developed budget ensures that resources are allocated efficiently across all necessary channels, allowing for maximum impact and return on investment.
— `w04-lecture` s10

> Measurable ROI.
— `w02-lecture` s11

Panels: Measurement and Evaluation; Budget and Resource Allocation.
Use: a summary KPI for the whole plan; the module does not define its calculation.
Definition: not given in module.
Primary work named on slide: Kotler & Armstrong (2018) (s10); Chaffey & Ellis-Chadwick (2019) (`w02-lecture` s11) — unverified leads.
Outside: no.

### `click-through-rate` — Click-through rate (CTR)

> *CTR (Click-Through Rate): Measures the percentage of people who click on an ad after seeing it.
— `w02-mini-case-studies` p. 2

Panels: Measurement and Evaluation; Digital Marketing Tactics.
Use: a channel-level metric for paid and email campaigns.
Primary work named on slide: none (mini case by Dr Muhammad Arsalan Nazir, May 2025).
Outside: no.

### `cost-per-click` — Cost per click (CPC)

> *CPC (Cost Per Click): The amount paid for each click on an ad.
— `w02-mini-case-studies` p. 2

Panels: Measurement and Evaluation; Budget and Resource Allocation.
Use: links PPC budget lines to expected traffic.
Primary work named on slide: none (mini case).
Outside: no.

### `return-on-ad-spend` — Return on ad spend (ROAS)

> *ROAS (Return on Ad Spend): Evaluates revenue generated per dollar spent on ads.
— `w02-mini-case-studies` p. 2

Panels: Measurement and Evaluation; Budget and Resource Allocation.
Use: revenue per unit of ad spend; express it in the plan's currency.
Primary work named on slide: none (mini case).
Outside: no.

### `open-rate` — Email open rate

> Success Metrics: High open rates, click-through rates, and customer retention.
— `w02-tutorial` s10

Panels: Measurement and Evaluation; Digital Marketing Tactics.
Use: email-channel metric (Tesco example).
Definition: not given in module.
Primary work named on slide: Yesiloglu & Costello (2021) — unverified lead.
Outside: no.

### `churn` — Churn

> Retention Effort: Ongoing value delivery (e.g., updates, engagement) is key to prevent churn.
— `w05-lecture` s9

> Reduces churn by addressing concerns promptly.
— `w02-lecture` s12

Panels: Measurement and Evaluation; Creativity and Innovation.
Use: the loss side of retention for a membership plan; a churn KPI should sit next to retention rate. The module uses the term without a formula.
Definition: not given in module.
Primary work named on slide: Cheng & Zhao (2025) (`w05-lecture` s9); Rushing (2017) (`w02-lecture` s12) — unverified leads.
Outside: no.

---

## I. Creativity and Innovation (Lectures 1–5)

### `artificial-intelligence` — Artificial intelligence (AI) in marketing

> Artificial Intelligence: AI involves using algorithms to simulate human intelligence and improve decision-making.
— `w01-lecture` s15

> In the future economy, digital marketing will increasingly rely on AI, automation, and big data to engage consumers with hyper-personalized, data-driven content.
— `w02-lecture` s3

Panels: Creativity and Innovation; Digital Marketing Tactics.
Use: the brief lists AI first; applications taught include recommendations, chatbots, predictive CRM and personalisation. Ethical and privacy limits should be acknowledged.
Primary work named on slide: Smith & Jones (2023) (`w01-lecture` s15, no Crossref match, D-005); Chaffey & Ellis-Chadwick (2019) — unverified leads.
Outside: no.

### `personalisation` — Personalisation and hyper-personalisation

> Personalized marketing: This refers to tailoring marketing efforts to individual preferences and behaviors using data insights.
— `w01-lecture` s15

> The Power of Personalisation refers to how tailoring marketing messages, product offerings, or digital experiences to individual consumer preferences significantly boosts engagement, satisfaction, and loyalty.
— `w03-lecture` s6

> Reduces Cognitive Load
> Enhances Emotional Connection
> Builds Brand Loyalty
— `w03-lecture` s6

> Hyper-personalisation using AI
— `w02-tutorial` s4

Panels: Creativity and Innovation; Digital Marketing Tactics; Sales Strategies.
Use: personalised offers, routes or plans in an app; the three mechanisms explain why it works. Data consent is the obvious limit.
Primary work named on slide: Smith & Jones (2023) (`w01-lecture` s15); Tam & Ho (2020) (`w03-lecture` s6, citation as printed does not exist, D-005); Nazir et al., (2025) (`w02-tutorial` s4) — unverified leads.
Outside: no.

### `omnichannel` — Omnichannel strategy and decision-making

> In the future, marketing will be heavily influenced by big data, personalized content, and omnichannel (experience across all channels) strategies (Corsaro & Maggioni, 2021).
— `w01-lecture` s13

> Consumers use multiple digital and physical channels during their buying journey, combining the benefits of both online and offline experiences.
— `w03-lecture` s9

> Consistent Messaging
> Seamless Transitions
> Real-Time Customer Service
— `w03-lecture` s9

Panels: Creativity and Innovation; Digital Marketing Tactics; Sales Strategies.
Use: for a transport platform, online (app, social) and physical touchpoints (vehicles, drivers, partner locations) must carry one experience. The John Lewis mini case (`w03-tutorial` s8) and the HBR reading give examples; the Statista figure on s8 is not evidence.
Primary work named on slide: Corsaro & Maggioni (2021) (in-line); Verhoef et al., (2017) — unverified leads.
Outside: no.

### `omnichannel-channel-migration` — Omnichannel promotions: moving online customers to physical stores

> Encouraging online
> customers to visit a store
> increased profits, but
> incentivizing in-store
> customers to shop online
— `w01-omnichannel-retailing` p. 2

> That’s the winning
> omnichannel strategy,” Luo says.
— `w01-omnichannel-retailing` p. 2

Panels: Creativity and Innovation; Budget and Resource Allocation.
Use: evidence from the Week 1 HBR reading that channel incentives should be targeted by the customer's starting channel and distance, not sent to everyone. Its retail setting transfers to ride-hailing only by analogy. Quoted as separate printed lines because the text layer interleaves columns.
Primary work named on slide: HBR reading; "About the research" names a working paper, "Omnichannel Couponing", by Fue Zeng, Xueming Luo, Yifan Dou and Yuchi Zhang — unverified lead; the reading's own byline is not shown.
Outside: no.

### `neuromarketing` — Neuromarketing and emotional triggers

> Neuromarketing is the application of neuroscience and psychological principles to marketing.
— `w03-lecture` s10

> Neuromarketing studies how brain responses influence consumer decision-making, with a focus on how emotions shape purchasing decisions.
— `w03-lecture` s10

> Neuromarketing techniques tap into emotional triggers to enhance engagement.
— `w03-tutorial` s10

Panels: Creativity and Innovation; Branding and Identity.
Use: the brief lists neuromarketing. A poster can apply it as emotion-led creative and brand cues (colour, story, calm journeys), and can test creative with attention or emotion measures. It should not claim brain-imaging research the group has not done.
Primary work named on slide: Plassmann et al., (2012) — unverified lead.
Outside: no.

### `subscription-model` — Subscription model

> Customers pay a recurring fee to access products or services over time.
> This model provides predictable revenue streams and helps build long-term customer relationships.
— `w05-lecture` s3

> Subscription: A business model where customers pay a recurring fee (for subscription) at regular intervals (monthly, annually, etc.) to access products or services.
— `w05-tutorial` s3

Panels: Creativity and Innovation; Alignment with Business Objectives; Budget and Resource Allocation.
Use: the brief lists "subscription and revenue model"; the PureGym tier table on `w05-tutorial` s3 shows how tiers can be presented. Any plan price is the group's assumption unless sourced.
Primary work named on slide: Cheng & Zhao (2025) (s3); Kotler, P., & Armstrong, G. (2018). (`w05-tutorial` s3) — unverified leads.
Outside: no.

### `recurring-billing` — Subscription billing and recurring billing

> Refers specifically to the process of charging customers a recurring fee—often upfront—for continued access to a product or service.
— `w05-lecture` s3

> Emphasizes the repeated payment process, applicable to subscriptions or other regular payments (e.g., utility bills).
— `w05-lecture` s3

> Subscription models are a subset of the broader recurring payment model.
— `w05-lecture` s3

Panels: Creativity and Innovation.
Use: helps name the revenue mechanism precisely (subscription within a wider recurring-payment model).
Primary work named on slide: Cheng & Zhao (2025) — unverified lead.
Outside: no.

### `recurring-revenue-model-types` — Types of recurring revenue models

> Types of Models: Includes subscription, usage-based, freemium, membership, retainer, and license models.
— `w05-tutorial` s10

Panels: Creativity and Innovation; Alignment with Business Objectives.
Use: the menu of six types; the poster should justify the one or two that fit the business rather than list all.
Primary work named on slide: none on s10; the types table (`w05-tutorial` s5) cites Econsultancy (2018) and the lecture (`w05-lecture` s6) cites Acayip et al., (2025) — unverified leads; the Econsultancy attribution for a revenue-model table is doubtful.
Outside: no.

### `usage-based-model` — Usage-based (pay-as-you-go) model

> | Usage-Based (Pay-as-You-Go) Model | Customers are billed based on actual usage of a service. Ideal for users with variable or low usage needs. | Uber – customers are charged based on the distance traveled and time spent during each ride. |
— `w05-tutorial` s5

Panels: Creativity and Innovation; Company/Business Introduction.
Use: the module's own example of this model is ride-hailing, so it describes per-trip pricing directly; combining it with a membership layer is a revenue-model design choice for the group.
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `freemium-model` — Freemium model

> | Freemium Model | Basic features offered for free; premium features require payment. Attracts a large user base, then converts a portion to paid plans.
— `w05-tutorial` s5

Panels: Creativity and Innovation.
Use: relevant only if a free tier with paid upgrades fits the service.
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `membership-model` — Membership model

> | Membership Model | Recurring fee paid for access to exclusive benefits, often community-based. Encourages loyalty through perks and exclusivity. |
— `w05-tutorial` s5

Panels: Creativity and Innovation; Sales Strategies; Measurement and Evaluation.
Use: the closest module concept to a paid membership programme with perks; measure it with retention, churn and CLV.
Primary work named on slide: Econsultancy (2018) — unverified lead.
Outside: no.

### `recurring-revenue-benefits` — Benefits of recurring revenue models

> Predictability of revenueBusinesses can forecast their revenue more accurately.
— `w05-lecture` s7

> Business Benefits: Predictable revenue, increased customer loyalty, consistent cash flow, scalability, and growth opportunities.
— `w05-tutorial` s10

Panels: Creativity and Innovation; Alignment with Business Objectives.
Use: links a membership or subscription offer to business goals (predictable revenue, loyalty, scalability). Note the lecture slide's run-together headings ("revenueBusinesses") come from the original text boxes.
Primary work named on slide: Zahay et al., (2022) — unverified lead; the printed title concerns digital marketing curriculum design, a doubtful fit for this claim.
Outside: no.

### `retention-over-acquisition` — Focus on retention over acquisition

> | Focus on Retention Over Acquisition | Emphasize retaining existing customers through loyalty programs, exclusive offers, and continuous engagement. |
— `w05-lecture` s8

Panels: Creativity and Innovation; Budget and Resource Allocation; Alignment with Business Objectives.
Use: argues for budget on retention (loyalty, engagement) as well as acquisition.
Primary work named on slide: Cheng & Zhao (2025) — unverified lead.
Outside: no.

### `relationship-selling` — Shift to relationship selling

> | Shift to Relationship Selling | Focus on building long-term relationships rather than one-time transactions; demonstrate ongoing value to customers. |
— `w05-lecture` s8

Panels: Sales Strategies; Creativity and Innovation.
Use: the subscription-era version of `relationship-building`.
Primary work named on slide: Cheng & Zhao (2025) — unverified lead.
Outside: no.

### `subscription-bundling` — Subscription bundling

> | Subscription Bundling | Bundle services to increase perceived value and reduce churn. |
— `w05-lecture` s8

> Vodafone UK uses bundling (e.g., mobile + broadband + streaming services) to retain customers.
— `w05-tutorial` s6

Panels: Creativity and Innovation; Sales Strategies.
Use: bundling several service lines (for example rides and delivery) inside one plan. The tutorial asks whether bundling builds loyalty or locks customers in, a fair Q&A challenge.
Primary work named on slide: Cheng & Zhao (2025) — unverified lead.
Outside: no.

### `upselling-and-cross-selling` — Upselling and cross-selling

> | Upselling and Cross-Selling Opportunities | Include upselling premium plans or cross-selling complementary services to existing subscribers. |
— `w05-lecture` s8

> 6. Opportunity for Upselling and Cross-Selling: Vodafone maximizes revenue by:
— `w05-vodafone` p. 1

Panels: Sales Strategies; Creativity and Innovation.
Use: moving users to premium tiers or adding complementary services; revenue per customer rises.
Primary work named on slide: Cheng & Zhao (2025) — unverified lead. Vodafone case: none (by Dr Muhammad Arsalan Nazir).
Outside: no.

### `subscription-challenges` — Challenges of recurring revenue models

> Billing Complexity: Handling upgrades, cancellations, and refunds requires advanced billing systems.
> Price Sensitivity: Regular-fee customers are more reactive to price changes; mismanagement can lead to churn.
> Regulatory Compliance: Businesses must follow rules on transparency and ease of cancellation for subscriptions.
— `w05-lecture` s9

Panels: Creativity and Innovation; Alignment with Business Objectives.
Use: risk column for any membership proposal; answers the likely Q&A question on downsides.
Primary work named on slide: Cheng & Zhao (2025) — unverified lead.
Outside: no.

### `subscription-future-trends` — Future trends: AI personalisation in subscriptions

> Technological advancements, such as AI and personalization, are shaping the future of subscription models.
— `w05-lecture` s11

> Introduced AI personalization to tailor workouts.
— `w05-tutorial` s9

Panels: Creativity and Innovation.
Use: joins two brief trends (AI and subscription) in one innovation idea, such as personalised membership offers.
Primary work named on slide: Acayip et al., (2025) (`w05-lecture` s10) — unverified lead; none on s11 or `w05-tutorial` s9.
Outside: no.

### `loyalty-programmes` — Loyalty programmes

> Starbucks, the renowned coffee chain, has embraced personalization through its loyalty program and mobile app.
— `w03-tutorial` s5

> Virgin Telecom excels in personalized engagement and loyalty-driven retention, while Reliance Jio focuses
— `w02-mini-case-studies` p. 3

Panels: Creativity and Innovation; Sales Strategies; Measurement and Evaluation.
Use: loyalty points or tiers as a retention mechanism in an app.
Definition: not given in module (shown by example).
Primary work named on slide: Tam & Ho (2020) (`w03-tutorial` s5) — unverified lead; the citation as printed does not exist (D-005). Mini case: none.
Outside: no.

### `gamification` — Gamification

> Experience economy: From transactions to experiences - Pakistan: Foodpanda and Daraz have invested in immersive digital touchpoints to retain app users through gamification and loyalty points.
— `w01-tutorial` s21

Panels: Creativity and Innovation.
Use: app engagement idea (challenges, badges, green-trip milestones). Named but not developed in the module.
Definition: not given in module.
Primary work named on slide: Corsaro & Maggioni (2021) — unverified lead.
Outside: no.

---

## J. Alignment with Business Objectives (own reflection and research)

### `alignment-with-objectives` — Aligning marketing with business goals and objectives

> How does your marketing strategy align with the overall business goals and objectives? Have you considered the long-term sustainability and growth potential of your marketing initiatives?
— `w06-lecture` s7; `w05-tutorial` s14

> Strategic Thinking: Students will learn to analyze market trends, identify opportunities, and develop strategic marketing plans aligned with business goals and objectives.
— `module-handbook`

Panels: Alignment with Business Objectives.
Use: the brief treats this panel as the group's own reflection and research. The registered links are targeting fit with "resources, capabilities, and objectives" (`targeting`), KPIs as goals (`kpis-and-metrics`), and long-term value from retention (`recurring-revenue-benefits`). Company objectives themselves must come from the company's verified sources.
Definition: not given in module.
Primary work named on slide: none.
Outside: no.

### `long-term-sustainable-growth` — Long-term sustainability and growth

> The module aims to prepare students to adapt to emerging trends and changes in the future economy of digitalization and sustainability and enhance their understanding of knowledge and skills needed to succeed as marketing and sales professionals in this rapidly evolving landscape.
— `w01-lecture` s9; `w01-tutorial` s13

> Subscription models also boost customer retention and support long-term growth.
— `w05-lecture` s4

Panels: Alignment with Business Objectives; Creativity and Innovation.
Use: the brief asks about "long-term sustainability and growth potential"; the module links sustainability to the future economy and growth to retention. The poster should say what makes the plan sustainable in both senses (environmental and commercial) without conflating them.
Definition: not given in module.
Primary work named on slide: none (s9); Zahay et al., (2022) (`w05-lecture` s4) — unverified lead.
Outside: no.


## Outside concepts added for the current poster

### `marketing-mix-4ps` — Marketing mix and the 4Ps

> known as the 4Ps: product, price, place, and promotion (see Figure 1.4). Let’s look more closely.
— `openstax-2023` p. 1

Panels: Digital Marketing Tactics.
Use: organise the Copenhagen offer as app-booked electric taxi service (product), a capped first-trip offer and clear fare terms (price), verified service coverage and app access (place), and the planned search, social and outdoor mix (promotion). The framework structures decisions; it does not validate the proposed mix.
Outside: yes.

### `customer-data-platform` — Customer Data Platform (CDP)

> Customer Data Platform is defined by the CDP Institute, as of 2026, as “software that
> creates and maintains a persistent, unified customer record that is accessible to
> other systems. The CDP assumes primary responsibility for defining and maintaining
— `customer-data-platform-institute-nd` p. 1

Panels: Digital Marketing Tactics; Creativity and Innovation.
Use: use consented first-party app, trip, offer and service signals to inform segments and next messages only after privacy, data quality, access and system readiness are checked. CDP is a proposed capability, not a claim that Green SM currently operates one.
Outside: yes.

### `ride-hailing-dispatch-rl` — Reinforcement learning for ride-hailing task allocation

> We propose a special decomposition for the MDP actions by
> sequentially assigning tasks to the drivers.
— `feng-et-al-2020` p. 1

Panels: Creativity and Innovation.
Use: a research-backed concept for a separately costed dispatch pilot that tests driver-task assignment against a local baseline. The cited numerical experiment uses Didi data; it does not prove faster booking-to-driver matching, Copenhagen results or Green SM readiness.
Outside: yes.
