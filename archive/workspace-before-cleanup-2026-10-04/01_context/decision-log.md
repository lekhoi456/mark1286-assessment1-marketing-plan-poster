# Decision log

Append-only. Each entry: what was decided, why, what was rejected, who decided. Superseded decisions stay, marked **Superseded by D-xxx**. Deciders: *student* (Le Quoc Khoi, for himself or relaying the group), *group*, *lecturer* (relayed by the student), *agent*.

---

### D-001 — Scope and order of work (2026-09-27, student)

One workspace per assessment in the module folder. Assessment 1 (Marketing Plan Poster, due 14 October 2026) is done first, in `assessment1-marketing-plan-poster/`. Assessment 2 (Individual Vlog, due 7 November 2026) starts only after Assessment 1 is finished; no Assessment 2 workspace, research or skill is prepared before then.
Rejected: the agent's proposal to create an Assessment 2 skeleton now.

### D-002 — Language (2026-09-27, student)

Chat with the student in Vietnamese. The poster, the pitch and **every saved file** in English (UK).

### D-003 — Folder structure (2026-09-27, student)

Reuse the BUSI1764 layout (`00_brief_and_criteria` … `09_feedback`, with `AGENTS.md`, `HANDOFF.md` and `CLAUDE.md` containing `@AGENTS.md`), adapted to a marketing plan: `02_research/{business-selection, business-dossier, market-analysis, marketing-plan, perplexity}`, `03_course_materials/extracted`, `04_references/{_inbox, _archived}`, `06_workflow/{scripts, checklists, writing-skill}`, `07_drafts/{reviews, design}`, `09_feedback/{formative, summative}`.
Dropped from BUSI1764: Ashoka and venture screening, the market gate (BUSI1764 D-015 to D-017), the recall pack and reflection templates, the diary word-count rule, COIL.

### D-004 — Reference integrity (2026-09-27, student)

- "No PDF, no citation": every cited work is saved as a PDF in `04_references/` before it is cited; web pages as dated PDF snapshots.
- File names `{key}-{short-title}.pdf`, key = Harvard kebab-case `{authors}-{year}{suffix}`.
- Retrieval order: (1) the agent finds an open-access copy; (2) the agent uses the student's Comet browser with University of Greenwich SSO through the OpenAthens redirector (procedure in `AGENTS.md`); (3) the student downloads what the agent cannot reach into `04_references/_inbox/`, and the agent renames, verifies and registers it.
- `04_references/references.json` is the single source of truth; `references.html` is generated from it and is fit to hand to the lecturer. Unused works move to `_archived/`.
- Style: Cite Them Right Harvard, 13th edition (2025).

### D-005 — Course materials as sources (2026-09-27, student; evidence added by the agent)

The Study Hub is a study aid and is never cited. Slides, cases and the handbook are cited from the original course files.
Agent's evidence (P0, Crossref, 27 September 2026): some reference lists on the module's slides are wrong. "Smith, A. and Jones, B. (2023) … *Journal of Business Ethics*, 174(1), 405–421" has no Crossref match; "Tam, L. and Ho, S.Y. (2020) *Journal of Interactive Marketing*, 50, 26–40" does not exist as printed (pages 17–31 and 32–44 of that volume are other papers). Consequence: no reference is copied from a slide; each work is verified at its source before use.

### D-006 — Perplexity Deep Research (2026-09-27, student)

The agent writes the prompt; the student runs it; the output is saved verbatim in `02_research/perplexity/` with the run date. Outputs are leads only: every claim is re-verified at its original source, and Perplexity is never cited.

### D-007 — Poster size A0 (2026-09-27, lecturer, relayed by the student)

The local lecturer told the class to use **A0** paper, not A1. This overrides the handbook's and the brief's "One Standard Size A1 Paper Chart" for our group.
Consequences: the poster has about twice the area of the A1 exemplars, so panel word budgets and text sizes are set for A0 (`05_plans/poster-blueprint.md`, P5); printing at A0 has to be arranged (Q-S7); legibility is checked at A0 viewing distance and in the submitted image.
Recorded in `09_feedback/formative/lecturer-guidance-log.md`.

### D-008 — Poster production route (2026-09-27, student, for the group) — **open risk closed by D-021 (lecturer agreed)**

The brief's "hand-drawn" requirement is met, in the group's view, by an **AI-made design in a hand-drawn style**. The agent's work is the content in Markdown; the design is the last step.
Risk recorded by the agent (not reargued): the handbook ("Hand-drawn paper chart"), the brief ("submit the poster (hand drawn chart)", headed "Strictly to be Followed") and rubric criterion 7 ("hand-drawn visuals… Evident effort from all group members", 20%) describe a physically hand-drawn chart. Mitigations for the group to choose from: ask the lecturer before printing (Q-L2); add genuine hand-drawn elements by the members to the printed poster; disclose the AI design if the module's rules require it (Q-L7).
Rule that follows: the approved Markdown text is placed on the design by a layout tool; an image model never generates or retypes poster text (`AGENTS.md` rule 7).

### D-009 — Roles: the agent drafts, the group decides (2026-09-27, student)

The agent drafts every component: research, marketing plan, poster copy, design brief, pitch script, Q&A bank and checklists. The group makes the decisions and sends them through the student's prompts; each is logged here with its decider.
Integrity rule that follows: the poster's contribution statement ("which part each member contributed") and anything the group did or decided come only from the student's confirmed statements (`01_context/group-roster.md`). The agent never infers or invents them.
Rejected: the agent drafting only the student's own share.

### D-010 — Concept scope: module-first (2026-09-27, student; option (a) of the agent's proposal)

The brief has no "module concepts only" rule, but it ties each element to lecture resources (Lectures 1–5). Decision: every concept comes from the module's teaching resources and is entered in `03_course_materials/concept-register.md` with verbatim module wording and its slide or page, checked by `check_register_quotes.py`. An outside concept is allowed only with a verified PDF in `04_references/` and an `outside` flag in the register.
Rejected: (b) strict module-only scope as in BUSI1764 (no brief rule requires it); unrestricted use of outside frameworks (the lecture mapping signals what markers expect).

### D-011 — Writing skill `mba-presentation-style` (2026-09-27, student)

Create one new skill, `mba-presentation-style`, now, scoped to what Assessment 1 needs (poster copy, visual design brief, group pitch script, Q&A preparation). It specialises `mba-writing-style` the way `mba-diary-writing-style` does, and is mirrored to Codex. No vlog skill (D-001).
Agent's constraints: `draftcheck.py` and the avoid-ai-writing checkout stay unchanged until BUSI1764 is submitted on 12 October 2026 (its gate is calibrated to them); the new skill's `presentcheck.py` wraps `draftcheck.py` and adds genre rules. Build notes: `06_workflow/writing-skill/mba-presentation-style-notes.md`.
Rejected: two separate skills for poster/pitch and vlog; no new skill.

### D-012 — Working format (2026-09-27, student)

Markdown for all working files. Design files (layout proofs, exports) appear only in the design phase (P7).

### D-013 — Research apparatus stays behind the scenes (2026-09-27, agent)

Research questions, scoring matrices, sensitivity checks, evidence logs, triangulation and mock marking govern how we work. They are not presented on the poster or in the pitch, which show marketing analysis.

### D-014 — Which dates govern (2026-09-27, agent)

The handbook dates govern: formal submission **14 October 2026** (Week 8). The Assessment 1 Brief document (17 June 2026) and the Week 1 slides (17 June and 13 July 2026) carry dates from an earlier cohort. Presentations "begin" in Week 6 per the handbook, so the pitch may come before the submission date. Internal submission target: 13 October 2026. The Can Tho dates and times are to be confirmed (Q-L1, Q-S1); the plan is re-dated backwards from the pitch date once it is known.

### D-015 — Lecture 6 recording transcribed in P1 (2026-09-27, agent; the student raised no objection)

Transcribe `Lecture + Tutorial 6/Lecture 6 - Poster Structure Recap.mp4` (23 minutes) in P1 with a local Whisper model, to capture spoken guidance on the poster that the slides may not carry. The transcript goes to `03_course_materials/extracted/`; model caches stay outside iCloud. Other recordings only if P1 shows a need.

### D-016 — Source attribution corrections to D-007 and D-014 (2026-09-27, agent)

The handbook's assessment schedule says "One Standard Size Paper Chart", without specifying A1. The separate Assessment 1 Brief says "(One Standard Size A1 Paper Chart)". D-007's attribution of A1 to both documents is corrected here; A0 remains the controlling local instruction. The physical sizes of the photographed exemplars are not established by their JPGs. A0 has twice the area of standard A1 paper, but no claim about the actual exemplar sheets follows from that.

The conflicting June/July dates in D-014 may be carried over from another cohort; that provenance is an inference, not confirmed fact. The current handbook's 14 October 2026 remains the working deadline, pending the local timetable and Moodle time.

### D-017 — P0 smoke scope and citation-key distinction (2026-09-27, agent)

P0 tests the adapted tools on selected A1 course materials and temporary fixtures. That does not authorise or complete P1's full extraction, concept register or Lecture 6 transcription. Default extraction is restricted to A1-relevant materials; no A2-specific exemplars or Weeks 7–9 are processed for this workspace.

Reference filename keys use `et-al` for three or more personal authors as an internal naming convention. This does not determine Harvard display: Cite Them Right normally names all three authors in a three-author in-text citation and uses *et al.* for four or more. Verify the exact source type against the saved guides; never copy the filename key directly into a citation.

### D-018 — Business: Green SM, a multi-country company (2026-09-27, group, relayed by the student)

The group has chosen **Green SM**: the ride-hailing, taxi and delivery brand of GSM Green and Smart Mobility Joint Stock Company (Hanoi), which traded as Xanh SM until the company's rebrand announced on 13 April 2026. The student added that the company operates "not only in Vietnam but in six countries in total", so the plan must treat it as a multi-country business.

Agent's verification of the country count (company sources, read and saved on 27 September 2026; evidence log E-001 to E-010):
- Six countries (Vietnam, Laos, Indonesia, the Philippines, India, Kazakhstan) is the company's own list from its Kazakhstan launch release of 23 June 2026. The same list is still used as boilerplate in its Denmark release of 30 July 2026.
- Since then Green SM has launched in Denmark (30 July 2026, its first European market) and started **pilot** operations in Amsterdam (25 September 2026), which the company calls its "eighth market globally".
- So "six" is correct as at June 2026, "seven" counts full launches to date, and "eight" includes the Dutch pilot. The poster must state the count with its reference date. The agent will not silently use six. Which count and which markets the plan covers is a group decision (Q-S9).

Consequence: P2 becomes a suitability audit of a chosen case (research design §3), not a shortlist. No weighted ranking or sensitivity test is run on alternatives that the group did not consider. Audit: `02_research/business-selection/green-sm-suitability-audit.md`.

### D-019 — Company facts carry a reference date (2026-09-27, agent)

Green SM added two markets in the two months before this assessment and its own pages disagree on some details (evidence log conflict ledger C-001 to C-003). Every company fact on the poster and in the pitch is therefore stated "as at" a date, from the latest saved official statement, and re-checked at the final content approval (P5 gate). If a new market or rebrand detail appears before submission, the group decides whether to update; the evidence log keeps the superseded statement.

### D-020 — How the Lecture 6 recording is used (2026-09-27, agent) — **design-input paragraph superseded by D-022**

The Lecture 6 recording (transcribed in P1, D-015; `03_course_materials/lecture6-guidance.md`) belongs to an earlier delivery: it gives presentation dates in June 2025, a 12 June 2025 deadline, a 40% weighting and an "80% Poster + 20% Presentation" split. The current handbook (50%, 14 October 2026) governs; the recording's dates and weights are not used. The 80/20 split is put to the lecturer as a question (Q-L5), not assumed.
The recording is used as the module team's spoken explanation of the same brief wording, for design inputs only: bullet points on the poster rather than long theory; examples explained in the pitch; the Tesla mini-case as a model of how to lay out the plan; concepts from Weeks 1–5. It repeatedly describes a drawn poster submitted as a phone photograph and says nothing about digital or AI-made posters, so it strengthens the case for asking the lecturer before production (Q-L2, D-008). It says naming each member's contribution is optional; our stricter rule (D-009) stays. Excerpts are machine-transcribed and cross-checked by two models; no human has listened yet. The recording is never cited on the poster.

### D-021 — Poster made with AI in a hand-drawn style; lecturer agreed (2026-09-27, student; lecturer approval relayed by the student)

The student decided to produce the poster with AI in a hand-drawn style and reports that the lecturer, Dr Luu Tien Thuan (Lưu Tiến Thuận), agreed. This answers Q-L2 and settles the production route left open in D-008. Unchanged: the approved Markdown text is placed by a layout tool and never generated or retyped by an image model (AGENTS.md rule 7). Whether a written AI-use disclosure is required remains Q-L7. Recorded as LG-002.

### D-022 — Do not adopt the 2025 recording's style advice (2026-09-27, student)

The student warned that following the Lecture 6 recording's advice (bullet points only, little theory, the Tesla case as a template) could lower the mark. This supersedes the "design inputs" paragraph of D-020. Rules that follow:
- Module concepts are applied explicitly and analytically on the poster: each panel names the concept it uses and shows it doing work for Green SM (concept register, D-010). A concept is never decoration, and never just a label.
- Panels use short, complete statements where an argument or a causal link is being made; bullet fragments only for lists (for example channels or KPIs). The UK moderator reads the poster without hearing the pitch (Q-L8).
- The Tesla mini-case is a teaching sample, not a structure to copy. The eleven headings in the brief and the rubric govern the layout.
D-020's other points stand: the recording's dates and weights do not govern, it is not cited, and the 80/20 question stays with the lecturer (Q-L5).

### D-023 — One focus market, chosen by data; Denmark or the Netherlands preferred (2026-09-27, group, relayed by the student)

A marketing plan for all eight markets on one A0 hand-drawn-style poster is not feasible. The plan is for **one focus market**, with the company background showing all eight markets. The group's preference is **Denmark or the Netherlands**, because they mark a Vietnamese (Asian) taxi company entering Europe. Rule set by the group: choose Denmark or the Netherlands **unless the data are insufficient or another market would support a higher-scoring plan**; the choice is made by data. Method and result: `02_research/business-selection/focus-market-selection.md`.
Agent's caution: "the first Vietnamese or Asian taxi company in Europe" is the group's framing, not yet a verified fact (the company's releases say only that Denmark is Green SM's own first European market, E-008). It needs its own sources before it can appear on the poster.
Supersedes the scope options in the suitability audit §4 (Q-S9 answered).

### D-024 — Footprint wording: eight markets (2026-09-27, group)

The poster states eight markets in total, with the "as at" date (D-019) and, where relevant, that the Netherlands is in pilot. Answers Q-S10.

### D-025 — Green SM web pages are opened in Comet, headed (2026-09-27, student)

Any page on the Green SM website is opened in the student's Comet browser, visibly, through the CDP shim (AGENTS.md, "Institutional access with Comet"); headless Chrome is not used for greensm.com. The seven Green SM snapshots saved earlier with headless Chrome are re-captured through Comet where the browser allows printing to PDF; the registry records the retrieval route. Other websites may still be saved with `save_web_pdf.py`.

### D-026 — Other answers from the student (2026-09-27)

- GSM's global CEO: Nguyen Van Thanh until 5 June 2026, Nguyen Quoc Tuan from 23 June 2026 (student). Consistent with the dated releases; conflict C-001 is closed as a change of CEO, not a contradiction.
- The rebrand is "Xanh SM to Green SM" (student), as in the Vietnamese release (C-003).
- No member works for GSM, Vingroup or a competitor (Q-S4).
- Local lecturer: Dr Luu Tien Thuan (Lưu Tiến Thuận), PhD. No group number has been assigned.
- Pitch date and Moodle submission time: left blank for now at the student's request; the plan keeps the handbook date, 14 October 2026.

### D-027 — Autonomous overnight research and preparation (2026-09-28, student)

The student authorised the agent to work independently during the night (a six-hour window) on tasks that do not require a student decision, without interrupting for questions. Complete evidence-led market selection, source/PDF integration, business and market research, and decision-ready alternatives where possible.

This does not delegate the group's choice of focus market, segment, position, budget, contributions or final copy. Any downstream option or numerical scenario prepared before those decisions is explicitly unapproved research, not an adopted marketing plan. A1-only scope, Comet-only access to Green SM pages, Markdown-before-design, no fabrication and no git commit remain unchanged. Record completed work and exact outstanding decisions in HANDOFF.md; do not invent time worked.

### D-028 — Completed focus-market comparison; recommendation is not adoption (2026-09-28, agent)

The agent operationalised D-023's broad preference before scoring using K1–K6 weights 25/20/20/15/10/10, European evidence gates and explicit tie/override rules. These numerical details and half-point judgements were **not stated or approved by the group**. Do not retrospectively attribute them to the student or interpret the result as an academic mark.

Source-backed base totals: Copenhagen 92.5, Hanoi 88.5, Amsterdam 84.5, Delhi 76.0. The agent conditionally recommends Copenhagen. Of 57 effective one-factor/equal-weight sensitivity runs, raw results favour Denmark 54 times, Vietnam once and tie twice; the preference policy chooses Denmark in all 57. Joint judgement stresses can reverse that preference. No probability or profit claim follows. Q-S13 is deferred, not answered by calculation.

### D-029 — Conditional strategy and financial scenarios, not approved commitments (2026-09-28, agent)

Three alternative segment types and positioning choices are prepared for Copenhagen/Amsterdam, with a bounded Hanoi fallback and exact module/rubric mapping. Budget envelopes of DKK240,000/600,000/1,200,000 and all conversion/retention/margin assumptions are **unapproved agent scenarios**, not company data or group decisions. Nine performance combinations fail contribution break-even even at the illustrative 50% margin. A consumer-only stress makes the mixed model's B2B dependency explicit. No budget, target, campaign, partner deal, customer interview or member contribution is adopted or claimed.

### D-030 — Source and tool corrections retained transparently (2026-09-28, agent)

The original Danish product PDF already contained tariffs; the earlier ‘no fares published’ note was a reading error, not website hydration. The inspected Dutch product page still does not establish a numerical fare; this does not prove none is published elsewhere. Unrelated Perplexity 02a/02b imports are preserved and excluded.

The 97-source collection retains automatic identity results separately from 18 audited exceptions bound to source bytes and metadata. Independent review exposed stale automatic-PDF and Crossref-cache acceptance; both were reproduced and repaired with fail-closed freshness gates. These verification results establish document identity, not independent truth of corporate claims. Group/lecturer approvals, source dates and genuinely unknown outcomes remain distinct.

### D-031 — Focus market: Copenhagen, Denmark (2026-09-28, the student)

The student instructed "Copenhagen đi" ("go with Copenhagen"), answering Q-S13. The marketing plan covers **one focus market: Copenhagen, Denmark**. This applies the group's D-023 rule and matches the agent's conditional recommendation (D-028); it is recorded as the student's instruction, without claiming separate contact with the other members.

Service scope follows the only Danish offer in the saved evidence: app-booked electric taxi rides sold by Green SM Denmark ApS (Green SM Car). No other Danish service line is evidenced. The company background still shows eight markets, dated, with the Dutch pilot (D-024). Amsterdam and Hanoi material stays as research record, not a parallel plan.

Not decided by this entry: priority segment, positioning, planning period and objective, budget total and acceptable learning loss. The D-029 envelopes and assumptions remain unapproved scenarios, and the D-028 challenge stands: evidence of an acquisition barrier does not prove the proposed solution works.

### D-032 — Copenhagen segment, positioning and budget envelope (2026-09-28, the student)

Answering Q-S14 and Q-S15 through the agent's option list, the student chose:

- **Priority segment S1:** adults living in the verified Copenhagen service area who already use taxis for some recurring trips and pay themselves. S2 (organisations) and S3 (visitors) are not targeted; eligible organic enquiries may still be served.
- **Positioning P1:** a clear local taxi choice, with a route to resolution. It is a hypothesis requiring proof, not a claim of superior service.
- **Budget:** DKK600,000 over 12 months with a **market-entry objective** (awareness and trial among S1, repeat use as the scale gate), rather than the recommended DKK240,000 learning pilot.

Consequences recorded by the agent: the account/partner sales line is removed and its 90 hours reassigned to CRM/support and local content (proposal awaiting approval; `02_research/marketing-plan/budget-kpi-scenarios.md`). Under the same assumptions the selected plan falls short of break-even in every modelled case (illustrative about −DKK554,000 at 30% contribution). The plan must present this as a deliberate, capped entry investment with stop and scale rules, not as ROI. Line items, channel mix, assumptions and KPI targets still need group approval.

### D-033 — Integrated Copenhagen plan v01 approved (2026-09-28, the student)

The student replied "đồng ý tất cả" ("agree to all") to approvals A1–A9 in `02_research/marketing-plan/integrated-plan-copenhagen.md` §13, answering Q-S16. Approved as proposed: the DKK600,000 line items (A1); five-stage release with Gate A at month 4 and Gate B at month 6 (A2); search, local page/SEO, social and CRM, with Digital Copenhagen screens only after Gate B (A3); the message "Know your ride before you book.", Danish first (A4); a DKK30 first-ride voucher capped at 400 riders (A5); objectives O1–O4 and the KPI targets (A6); personalised trip reminders plus one trip reference across channels, with AI chatbot and subscription deferred (A7); an illustrative persona, labelled as such (A8); in-car help card printed only after a quote and from contingency (A9).

Plan v01 is now the approved content basis for P5 poster copy. Targets and funnel rates remain planning assumptions, not Green SM data; every modelled case still falls short of break-even. Contribution statements remain open (Q-S5).

### D-034 — Poster v03 direction (2026-09-28, the student)

Chosen through the agent's option list:

- **Concept C, hybrid:** a hand-drawn taxi route runs through the eleven panels as reading order, customer journey and release timeline; the budget receipt, KPI dashboard and reminder-phone visuals use an app-screen style.
- **A0 landscape**, 1189 × 841 mm (the earlier portrait proposal in the blueprint is superseded).
- **Proposed numeric KPI targets**, labelled as assumptions: consideration +10 percentage points on the months 1–2 baseline by month 12; at least 80% of riders find area and fare clear; at least 90% of help requests answered within 24 hours.
- **About 1,400 counted words**, moving description into visual labels while keeping the reason for each choice.
- **A bold "Decision" line** at the start of each panel, **markers separating sourced facts from the group's assumptions**, and the **KFST p. 151 safety-motive evidence** (E-187) in the psychographic profile.

Not chosen at this point: members hand-drawing parts of the poster. "Evident effort from all group members" (C7) therefore rests on the contribution statement and the pitch (Q-S5).

### D-035 — Poster-led infographic direction and ten-panel car layout (2026-10-03, the student)

The student requested further brainstorming before execution because the existing drafts are unsatisfactory. The stated product direction is an A0 hand-drawn-style poster with recognisable Copenhagen surroundings and a stylised cyan VinFast VF MPV 7, following an idea the student attributes to Vy. The poster includes a title, subtitle and tagline; each marketing section should become an infographic/illustration rather than an unchanged bullet list.

The student then selected the chat option **ten marketing panels inside the car, with Student/Business Details in a separate strip**. All eleven required information elements remain identifiable; no content merger was selected.

Preparation is to work backwards from the assessed poster: complete content Markdown, a poster layout draft and an AI prompt, then an A0 production proof. The student intends to print the proof and redraw it by hand. This is intended future work, not a completed contribution or permission to invent others' activity. The approximately 1,400-word direction in D-034 is superseded as a fixed content cap: the student prioritises complete assessable content and its effective visual conversion, with actual-A0 legibility still required.

Unchanged: D-031–D-033 market, segment, positioning, budget and approved plan. Proposed and not yet approved: two-tier headings and their reader-facing titles, detailed panel geometry, final wording and reference packaging. The selected vehicle is an illustrative design concept; its use in the Danish fleet is not established. Exact lettering and references remain controlled by the approved Markdown/layout under D-007/D-008/D-021. This instruction authorises brainstorming first; it does not approve a new final poster or its production prompt.

### D-036 — Limo Green, accepted background and flexible display headings (2026-10-03, the student)

The student accepted the Copenhagen background and corrected the illustrative vehicle to **VinFast Limo Green**, replacing VF MPV 7 because the former is intended for transport-service business. This distinction is supported by the manufacturer's saved release (`vinfast-2025`, E-190); no Danish fleet inventory is inferred.

The student requested an information strip with the plan name, **student number followed by name**, and lecturer details, suggesting a stylised cloud and inviting alternatives. Lecturer identity remains Luu Tien Thuan, PhD (D-026 and current message). The student wants no per-member contribution detail in this strip, believing group marks will be equal. This is recorded as the student's preference/belief, not a verified marking rule or lecturer waiver. The source's conditional contribution clause and C7 remain visible for separate resolution; no completed work is invented.

Display headings may be renamed to fit the infographic. **Mandatory two-tier headings are rejected**; a small explanatory line is needed only when a heading is unclear. Avoid making every heading a question. This later instruction supersedes the earlier local exact-display-heading rule and the v01 paired-heading proposal; the full eleven-element mapping remains in working documents.

The student also requested stronger title/subtitle/tagline alternatives. Brainstorm v02 offers options; no new title set or replacement campaign line is adopted by this entry. Ten marketing panels, the current marketing plan, complete-content priority and intended print/redraw route remain unchanged. This remains a brainstorming stage.

### D-037 — Header, identity cloud and ten display headings approved (2026-10-03, the student)

The student explicitly selected **COPENHAGEN, MEET GREEN SM**, with the Danish flag beside Copenhagen, a separate Meet group and the official Green SM logo as the brand group. Approved subtitle: **A 12-month market-entry plan for local electric taxi rides**. Approved English poster tagline: **Clear terms. Local care.** This replaces the earlier displayed English tagline; a Danish translation and any wider campaign adaptation have not been selected.

The Student/Business Details cloud has these exact six lines:

```plaintext
Green SM | Copenhagen Market-Entry Plan
MARK1286 | Assessment 1
001545326 - Nguyen Phi Giao
001545344 - Le Quoc Khoi
001545423 - Nguyen Ho Khanh Vy
Lecturer: PhD Luu Tien Thuan
```

The student rejected the proposed taxi-booking-style identity card, referring to Green SM's app-booking model. This concerns the identity-strip alternative; the marketing-plan A9 in-car help card is unchanged.

Approved car-panel headings, in order: **Meet Green SM; Target Market; Why Green SM?; Brand & Promise; Digital Marketing; From Clicks to Rides; Budget & Resources; Success Dashboard; Ride Innovation; Business Goals & Growth**. Only panel 3 has the small subtitle **Positioning Strategy** and panel 6 **Sales Strategy**. The cloud plus these ten panels map to all eleven required information elements; the canonical mapping stays in the working documents.

Exact transcription: `07_drafts/design/approved-poster-display-copy-v01-2026-10-03.md`. This settles the display wording under Q-S18–Q-S19; panel body copy, detailed infographic geometry, reference packaging and final A0 proof remain to be prepared/reviewed. No new group activity, company performance or final poster approval is inferred.

### D-038 — Continue section-by-section content and infographic preparation (2026-10-03, the student)

After the agent proposed continuing with the assessable content and infographic conversion for each panel, the student replied “ok tiếp tục” (“OK, continue”). This authorises the preparatory drafting/brainstorm work: complete Markdown, content-to-visual map, layout sketch and AI-prompt draft, using the approved display copy and marketing plan.

The resulting v07 body text, 3+3+2+2 schematic, detailed infographic treatment and reference-package proposal are agent drafts for review, not newly adopted group choices. D-037 display approval and D-031–D-033 strategy/assumptions remain the authority. No new lecturer answer, contribution, actual campaign result or final-A0 approval is inferred.

### D-039 — Discuss and settle the proposal one panel at a time (2026-10-03, the student)

The student instructed the agent to treat the preceding version as the agent's proposal, then discuss and settle each item with the student in turn. The v07 body text, schematic, detailed content/visual map and prompt therefore remain proposals, not adopted final copy/design.

Start with panel 1, Meet Green SM. Present its explicit assessment requirements, proposed content and visual treatment; record actual amendments/approval before moving to panel 2. Track the sequence in `07_drafts/design/panel-review-and-approval-log-2026-10-03.md`. D-037's approved header/cloud/display labels and earlier marketing-plan decisions are not silently undone; explicit later amendments can revise them. No panel approval is inferred from this workflow instruction.

### D-040 — Panel 1 brand, flags, milestones and service illustration (2026-10-03, the student)

The student selected **Meet [official Green SM logo]**, using the brand only and omitting the full legal company name. Use a horizontal row of country flags, with Denmark enlarged/emphasised because Copenhagen is the focus. Place **14/04/2023** below Vietnam and **30/07/2026** below Denmark. Keep **Green SM Car: app-booked electric taxi rides in Copenhagen** and **Owned fleet · Employed drivers**, illustrated as **app → electric taxi ride**. The dates represent service launches; fleet/driver wording is scoped to Copenhagen.

The student also asserts a current nine-country footprint. Record this assertion without treating it as verified evidence: the D-024/E-009 baseline is eight markets including the Dutch pilot, and a parent-only headed Comet country-selector check on 3 October listed eight. The ninth country/launch remains unidentified. The preferred nine-flag design is therefore conditional on source verification, not silently changed to eight or adopted as fact. Country-of-origin clarity is addressed by the agent's proposed small **Vietnamese origin** label, not yet selected by the student.

Selected specification: `07_drafts/design/panel-01-selected-content-and-visual-v01-2026-10-03.md`. Panel 1 remains active under D-039; no panel 2/body, full poster or new production approval is inferred.

### D-041 — Correct panel 1 to eight country flags (2026-10-03, the student)

The student explicitly confirmed “đúng là 8, tôi sai” (“it is eight; I was mistaken”). Use eight flags: Vietnam, Laos, Indonesia, Philippines, India, Kazakhstan, Denmark and Netherlands. Retain the D-040 heading/logo, brand-only wording, two service-launch dates, Danish emphasis, exact service/model lines and app → electric taxi ride illustration. Preserve the Dutch pilot qualification and dated footprint evidence. Q-S21 is closed; no ninth country is invented.

Current selected specification: `07_drafts/design/panel-01-selected-content-and-visual-v02-2026-10-03.md`; v01 remains historical. The small **Vietnamese origin** label is still an agent wording proposal, not approved by this correction. The core panel-1 selections are settled; continue the D-039 discussion with panel 2, Target Market, while carrying the minor origin clarification to the consolidated wording/proof review. No panel-2 copy, whole-poster design or production approval is inferred.

### D-042 — Panel 2 must show age segmentation (2026-10-03, the student relaying lecturer guidance)

The student stated that **Adults 18+** is too broad and reported that the lecturer requires further age segmentation. Recorded as LG-003, a student-reported instruction, not a fabricated lecturer quotation. Refine the demographic element with age groups and an explicit priority selection. Retain S1's resident, self-paid and recurring-taxi-use basis unless explicitly revised. The instruction supplies no exact age bands or chosen priority.

Agent decision support in `02_research/marketing-plan/age-segmentation-options-2026-10-03.md`: compare 18–24, 25–44, 45–64 and 65+; propose 25–44 for the campaign. Checked official Copenhagen counts give 269,277 residents aged 25–44, 40.2% of all municipality residents on 1 July 2026. This is population context, not a taxi-customer count or proof of superior demand. Qualitative operator channel testimony is recorded with its limit. Exact age scope and panel-2 copy remain unapproved (Q-S22); no budget/funnel or positioning change is silently adopted.

### D-043 — Approve ages 25–44 as the priority target (2026-10-03, the student)

The student replied “đồng ý 25–44” (“agree with 25–44”). The Copenhagen campaign's priority segment is now residents aged **25–44**, within the confirmed usable service area, who already take recurring local taxi trips and pay personally. This refines the earlier adult S1 definition under D-032–D-033 and resolves Q-S22. It is a group-selected planning scope, not evidence that this age group uses taxis most or is the most profitable.

No separate secondary target, four-band display treatment, city-context badge, occupation, income threshold, household type, psychographic wording or completed panel-2 design is approved by this reply. Those remain for discussion. The budget total and existing funnel/KPIs are not recalibrated or represented as empirically validated for the narrower age scope.

Current panel-selection tracker: `07_drafts/design/panel-02-selected-content-and-proposals-v01-2026-10-03.md`. Continue panel 2 with psychographic and behavioural profile wording and the infographic treatment before panel 3. Preserve the older full poster proposals; carry the approved range into the next consolidated version.

### D-044 — Approve panel 2 psychographic and behavioural profile (2026-10-03, the student)

The student replied “đồng ý” (“agree”) to the presented panel-2 profile and its illustration associations. Approved psychographic labels: **Price-conscious · Values trip control · Expects fair treatment**. Approved behavioural labels: **Already uses taxis · Recurring local trips · Pays personally**. Use the proposed **Proposed rider profile** qualifier beside the illustrative person. Retain ages **25–44**, Copenhagen residence and the existing self-payment/recurring-taxi/service-area conditions.

The accepted icon associations are price/route-on-phone/customer-support for psychographics and taxi/repeat-calendar/wallet for behaviour. This is approval of the customer profile and basic content-to-icon mapping, not the full panel geometry, optional four-band age strip, population badge, regional survey bar chart or full-poster proof. The psychographic traits remain a group-selected planning hypothesis, not observed findings about all residents aged 25–44.

Current specification: `07_drafts/design/panel-02-selected-content-and-proposals-v02-2026-10-03.md`. Continue within panel 2 to settle infographic composition, data treatment and visible segmentation/prioritisation reasoning before panel 3. No new marketing budget, KPI, survey, customer observation or final-A0 production approval is inferred.

### D-045 — Approve Target Market composition with counted age columns (2026-10-03, the student)

The student instructed that the age strip become a **column chart with the number of people in each age group**, and said the rest of the proposed composition was OK. Use 18–24 / 25–44 / 45–64 / 65+ columns, with heights proportional to the source-bound counts 72,396 / 269,277 / 143,668 / 74,728 and 25–44 highlighted. The student approved the central resident/phone/location/Proposed rider profile treatment, approved-profile icons, age-population/date/citation badge and the caption **Recurring local trips create opportunities for repeat rides.**

Counts describe Copenhagen municipality residents on 1 July 2026, not taxi users or the eligible target audience. The 40.2% badge uses all 670,389 city residents, not the adult chart sum. Panel-2 core content/composition is settled; exact final A0 placement and print/pitch verification remain production tasks.

Current selected specification: `07_drafts/design/panel-02-selected-content-and-proposals-v03-2026-10-03.md`; current chart SVG/PNG v02; content review: `07_drafts/reviews/panel-02-target-market-review-2026-10-03.md`. The agent's optional stronger rationale caption is a proposal and must not silently replace the approved one. Continue sequential discussion with panel 3, **Why Green SM?**. No whole-poster approval, standalone numerical panel mark, new age-specific budget or actual campaign result is inferred.


### D-046 — Put the population percentage in the age-chart pill (2026-10-03, the student)

The student specified that the percentage belongs in the column-chart pill. Place **40.2%** with **of city residents** in the pill above the highlighted 25–44 column, keeping **269,277** as the separate resident-count label. Remove the separate repeated percentage badge/line from the chart composition. The all-city denominator, four population counts, source/date, selected profile and approved repeat-opportunity caption are unchanged.

Current selected panel specification: `07_drafts/design/panel-02-selected-content-and-proposals-v04-2026-10-03.md`; current chart SVG/PNG v04. The rendered preview has been inspected for pill/count separation; physical A0 fit remains a later task. Panel 3 remains next in the sequential discussion.


### D-047 — Produce settled sections with subagents while discussing the next section (2026-10-03, the student)

The student instructed that section work be delegated to a subagent while the parent discusses a different section with him, because the previous serial process is too slow. For each settled section, its worker prepares the exact-content Markdown, complete section infographic/layout draft and decorative AI prompt/text-placement manifest. The parent retains discussion, approval, shared controls and integration. This changes execution order, not the approved strategy or the need for truthful sources/data.

Catch-up production assigned to separate workers: panel 1 Meet Green SM and panel 2 Target Market, using their selected specifications. Their output prefixes and reports are separate; neither edits shared decisions, consolidated drafts, references or another section. Parent discussion proceeds to panel 3 Why Green SM? in parallel. The workers do not generate a final A0 or execute an image model before the relevant production approval. Other section wording remains proposed; no approval follows merely from delegation.


### D-048 — Dedicated section agents generate images after content approval and remain reusable (2026-10-03, the student)

The student clarified that each subagent must draw/generate an image for its own section once the section content is approved, and must be retained for later revisions rather than closed/replaced immediately. Assign one agent per section; the same agent handles the content-to-image work and subsequent visual changes. This authorises section-level image generation for approved content and supersedes the earlier parent restriction on image calls before whole-poster approval. Final A0 assembly remains a separate stage.

Panel 1 and panel 2 are already settled; parent sent both existing production workers the new authorisation to generate hand-drawn decorative artwork with the built-in image tool and compose complete section previews. Exact approved lettering, genuine logo/flags, numerical chart values and citations still use controlled layout. The approved 40.2% pill placement remains mandatory. Workers retain ownership of their panel-specific files and do not modify shared controls. Image results have not yet been accepted or claimed complete. Panel 3 is still under content discussion; this workflow instruction does not approve its proposed wording/composition.

Reuse `/root/produce_panel_01` for panel 1 and `/root/produce_panel_02` for panel 2. Completing a work turn leaves the agent available for follow-up; parent must not intentionally replace or terminate the section agent after delivery.


### D-049 — Reject panel-3 layout v01 and develop a unified focal composition (2026-10-03, the student)

The student stated that the Why Green SM? layout is not good. This rejects the proposed v01 composition, without approving or rejecting its proposed body wording and without reversing P1. Parent develops two spatial alternatives: A, central app with benefit satellites; B, dominant Green SM centre with small Uber/Bolt side context and integrated proposed benefits/neutral operator-model links. Both are proposals; neither is adopted. Parent preference B and worker preference A are design judgements, not student decisions.

A dedicated retained `/root/produce_panel_03` worker owns the section’s layout-thumbnail files and later image production after content/composition approval. No section-3 imagegen call is authorised by this rejection alone. Current parent discussion specification: `07_drafts/design/panel-03-discussion-proposal-v02-2026-10-03.md`. Panel 1/2 production packages were delivered with generated imagery and worker inspection; parent integration/user review and actual A0 checks remain separate.


### D-050 — Select composition B; assess content strength before section production (2026-10-03, the student)

The student selected **B** for Why Green SM? and expressed concern that the section may not do enough for high marks. Composition B is adopted. This does not by itself approve the strengthened display wording, establish a numerical grade or reverse P1. Parent and the retained panel-3 worker checked official brief element 4: the composition thumbnail lacks the complete positioning sentence and an explicit delivery-to-buyer-value argument.

Parent prepared `07_drafts/design/panel-03-discussion-proposal-v03-2026-10-03.md`: complete target/category/benefit/delivery-basis sentence, concrete Clear terms/Local care labels and a short Delivery plan implication. The buyer-benefit caption remains proposed. Worker delivered a B-only content-refinement sketch and narrow audit. Their copy variants are proposals; the parent master and student’s eventual approval control the executed version.

Source comparison remains the authority’s own-fleet/employed-driver versus platform/partner-operator facts (E-019/E-184). No evidence establishes unique or better clarity/help, or that ages 25–44 prefer the position. Existing regional price/habit evidence is retained as a strategy challenge; no new source, KPI, budget or campaign observation. Exact strengthened content awaits the student before the retained `/root/produce_panel_03` is sent the image-generation production task.


### D-051 — Approve strengthened panel 3 content and authorise its generated image (2026-10-03, the student)

The student replied “Chốt” to the parent’s final proposal: keep composition B, add the exact complete positioning sentence and the Delivery plan sentence, retain the Clear terms/Local care pictograms and sourced operating-model comparison. These display strings are transcribed in `07_drafts/design/panel-03-selected-content-and-visual-v01-2026-10-03.md`, which controls production over earlier sketch variants.

The optional buyer-benefit caption from earlier working proposals was not included in the final approval request and is not adopted. No new KPI, budget, measured superiority or unique/preferred-service claim is approved. The plan qualifier and source distinction remain.

Under D-048, the existing retained `/root/produce_panel_03` worker is authorised to generate its section artwork now and compose the exact approved text/facts with controlled layout. Parent moves to panel 4 Brand & Promise while production runs. Final image review/A0 integration remains separate.


### D-052 — Panel 4 inherits corporate branding; its promise addresses the focus market (2026-10-03, the student)

The student clarified: “Branding là đi theo tập đoàn mà, chỉ có Promise là target thị trường” (branding follows the group; the promise addresses the target market). Adopt this scope for Brand & Promise: present the existing Green SM corporate logo/observed palette as inherited identity and distinguish the proposed Copenhagen campaign promise. Do not imply that the group is developing a replacement brand or selecting new corporate values.

The parent prepared `07_drafts/design/panel-04-discussion-proposal-v02-2026-10-03.md`, with Global identity → Copenhagen promise regions. Remove v01's panel-wide Proposed brand expression and Selected brand values/value-to-emotion composition. The E-012 European/Vietnamese value difference remains source context, not a global-values claim. D-037's exact tagline and D-033's Danish-first campaign language remain approved.

This clarification approves the scope distinction, not the new supporting strings, full revised composition, section image or final poster. Q-S23 production allocation remains unanswered and the three retained workers remain available. No section-4 image generation or new agent is inferred.


### D-053 — Approve revised panel 4 content and connected composition (2026-10-03, the student)

The student replied “chốt” to the parent's revised Brand & Promise proposal. Adopt the inherited Global identity region (authentic logo, observed swatches, One brand across markets.) connected to the Copenhagen promise region (Proposed promise qualifier, exact approved tagline, audience-fit line, Danish-first language and same-promise consistency line). Exact master: `07_drafts/design/panel-04-selected-content-and-visual-v01-2026-10-03.md`; preceding v02 proposal remains history.

This settles panel-4 content/composition, not visual-style or A0 acceptance. The three existing section agents remain retained. The fourth-agent spawn failed earlier; parent temporarily produces this section to deliver the requested four-image review while preserving the existing dedicated workers. This is a disclosed execution fallback, not an invented student answer to Q-S23 or authorisation to close/rotate agents.


### D-054 — Reject current section images' style and revise all four consistently (2026-10-03, the student)

In the same message the student asked to see all four section images and stated that the current three are not acceptable: the hand-drawn style must be addressed. Reject the current visual treatment of panels 1–3; keep approved content/data and their selected compositions. Produce a consistent revision of all four after panel-4 content approval, addressing lettering, frames, flags/charts, lines/fills and illustration simplicity rather than only adding decorative drawings.

Parent inspected/displayed all three existing full previews and re-opened the supplied Oura poster. Shared production guide: `07_drafts/design/shared-hand-drawn-style-revision-v01-2026-10-03.md`. Existing agents 1–3 receive isolated follow-up revision tasks; parent produces panel 4 under the disclosed resource fallback. The guide is the parent's execution interpretation of the requested style, not a newly approved final image. Native image generation creates revised decorative art; all exact words, numerical geometry, authentic logo and citations remain controlled layout.

No new marketing claim, budget/KPI, corporate identity, contribution or final A0 approval is adopted. Show complete resulting images together for user review; retain rejected historical versions and all existing workers.


### D-055 — Remove visible poster citations following reported lecturer confirmation (2026-10-03, the student)

The student states that the poster does not need citations, that the sample posters omit them, and that he asked the lecturer who confirmed they are not needed. Recorded as LG-004, a student-reported lecturer instruction rather than a verbatim lecturer quotation. Adopt no visible author/year/page citations or source-attribution footers on the poster face; this supersedes earlier visible citation selections in the panel masters and preparation layouts.

Preserve approved factual content, dated footprint/chart scope, figures, denominators, planning qualifiers, evidence IDs, verified PDFs, internal source mappings and the Harvard reference library. Do not treat the display change as a waiver to invent claims or delete the research apparatus. Complete reference-list/back/end packaging remains a separate question: the student used “citation”, not an explicit reference-list waiver.

Exact controlled amendments are in `07_drafts/design/poster-citation-display-policy-v01-2026-10-03.md`. Existing retained agents revise panels 1–3 under new versioned prefixes; parent revises panel 4 and four-panel comparison. This is editable vector/copy work reusing the actual generated illustrations, not new imagery generation or approval of the current style/full A0 proof.


### D-056 — Number all marketing-panel headings and review sections again individually (2026-10-03, the student)

The student requires every heading to be numbered and says that the sections will be remade one at a time, beginning with panel 1. Adopt 1–10 for the ten marketing-panel display headings, without renumbering their small subtitles, giving sublabels extra numbers or turning the separate identity cloud into a marketing panel. Existing selected title/subtitle/tagline and cloud text remain. Keep the retained section agents available; only panel 1 receives a current production revision. Numbering is required for future revisions of the other sections, not approval of their current style or a new multi-panel redraw.

### D-057 — Adopt explicit panel-1 visual and face-copy feedback (2026-10-03, the student)

Reduce the Meet/Green SM heading; add a home icon before Vietnam; reduce the two launch-date sizes; replace the Danish top/bottom highlight with a yellow four-sided flag frame; add small raised pilot lettering above Netherlands; remove the entire dated Eight markets/Netherlands context line from the face. Keep the existing eight-country row, both exact dates, authentic logo, selected service/model copy and app-to-electric-taxi illustration. Home conveys origin and supersedes the earlier unapproved literal origin-label proposal. Internal source dates/evidence are retained; removal does not verify a newer footprint.

Exact master: `07_drafts/design/panel-01-selected-content-and-visual-v03-2026-10-03.md`. Retained panel-1 worker produces new v04 artifacts. No visible citations under D-055. The student's VinFast/Vingroup question requests advice only; neither name/logo/relationship statement is approved for addition yet. The parent will examine the existing verified sources and explain the content trade-off while panel production proceeds.


### D-058 — Identify VinFast with a logo on the illustrated vehicle (2026-10-03, the student)

The student states that using the VinFast logo in the car is sufficient. Adopt a small authentic VinFast vehicle emblem on the car body in panel 1. This replaces the parent's proposed separate VinFast electric vehicles caption; neither that caption nor any Vingroup name/logo/ownership chart is selected. All D-056/D-057 face copy and graphic refinements remain. The emblem is visual identification, not a new claim of Limo Green deployment in Copenhagen or final whole-panel/image acceptance.

Exact amendment: `07_drafts/design/panel-01-selected-content-and-visual-v04-2026-10-03.md`. Existing retained panel-1 worker produces v05 with asset provenance and controlled overlay, preserving prior versions, exact lettering/data and source apparatus. No new image-model lettering or whole-image redraw is required.


### D-059 — Correct emblem-only badge to the complete supplied VinFast logo (2026-10-03, the student)

The student explicitly says to use the full VinFast logo and supplies `/Users/khoilq/Downloads/Logo_of_VinFast_(3D).svg`. Parent rendered/inspected the attachment: it contains both the silver V emblem and VINFAST wordmark. Adopt that complete unchanged artwork on the car body. The prior emblem-only v05 is superseded, not accepted. Preserve complete logo proportions/colours, with enough size for the wordmark to read; no crop, generic V or separately rebuilt letters. No independent caption or Vingroup addition.

Exact amendment: `07_drafts/design/panel-01-selected-content-and-visual-v05-2026-10-03.md`; retained worker produces v06. Student asset SHA-256 `9d676729f71ddfcc6322c368ca1d446b1047fff3afc50cf847f22b5c67941f00`. This is user-supplied artwork provenance, not a newly registered external reference. All other selected D-056/D-057 face strings and layout remain; artwork-only identification does not claim Danish model deployment or whole-image approval.


### D-060 — Hand-drawn full VinFast logo in the middle door; lightning moved rearwards (2026-10-03, the student)

The student requests that the lightning move to the rear compartment and that the VinFast logo become hand drawn, with wording 'ở ô cửa sửa'. The controller states its interpretation as the middle door/body rectangle now containing the lightning. This placement interpretation is not an invented exact quotation. Adopt hand-drawn treatment while retaining the full emblem plus VINFAST wordmark; glossy unchanged-3D treatment from D-059 is superseded. Move the lightning rearwards, remove the previous middle-door bolt and leave the former front-door badge location clean.

Exact visual amendment: `07_drafts/design/panel-01-selected-content-and-visual-v06-2026-10-03.md`. Retained worker produces v07 using native raster editing for decoration and controlled exact wordmark/copy. All prior selected ordinary face strings, flags/dates/heading and citation-free policy remain. Source SVG is preserved as a shape reference, not overwritten. No new company claim, Vingroup addition or final image/A0 acceptance.


### D-061 — Add the United States to panel 1 after checking the official US presence (2026-10-03, the student)

The student requests one additional market, supplies the Hello Los Angeles / Book your ride with Green SM image, then identifies Green Future USA Inc. and https://www.greensm.com/us-en. The parent directly inspects the official US homepage in a dedicated headed Comet tab: Green SM Car, US-facing app/service invitations and recruitment, local operator and California address are present. Adopt a ninth country flag/label for the United States, appended after Netherlands. This revises the current poster footprint, not the historical eight-market September source record.

Scope is present US market/service offering. No precise US commercial launch date or completed paid ride is verified or added. Keep the Dutch pilot qualification; do not claim nine fully operational launches. All D-056–D-060 selected text/style, Denmark emphasis, Vietnam origin/dates and hand-drawn VinFast middle-door/rear-lightning remain. Exact amendment: 07_drafts/design/panel-01-selected-content-and-visual-v07-2026-10-03.md; retained panel-1 worker produces v08, preserving v07. Image/A0 acceptance is not inferred.


### D-062 — Review official US About page for possible panel-1 additions (2026-10-03, the student)

The student explicitly asks to read https://www.greensm.com/us-en/about and assess useful additions to Meet Green SM. This authorises research and recommendations, not adoption of new panel wording or imagery. Parent headed-Comet retrieval, source/PDF inspection and automatic verification completed (green-future-usa-inc-ndc; E-199–E-201). Company-background callout and optional EV labels are agent proposals in 07_drafts/design/panel-01-about-additions-proposal-v01-2026-10-03.md. Retained panel-1 agent gives read-only advice; no production changes. D-061 v08 remains current; student selection is pending.


### D-063 — Approve Vingroup-backed / Founded March 2023 introduction callout (2026-10-03, the student)

The student replies in agreement to the presented recommendation. Adopt the primary two-line company-background callout, exactly Vingroup-backed / Founded March 2023, at the upper right of panel 1 above the country row, with simple building/calendar icons. This is the controller's stated interpretation of agreement to the primary recommendation; optional EV/tailpipe labels remain unselected. The source is E-199 / registered official US About PDF physical p.2, already inspected and automatically verified. Foundation month does not replace the existing Vietnam taxi-launch date.

Selected amendment v08 controls the addition; retained panel-1 agent produces production v09 by controlled vector/layout, with all 15 old ordinary strings, nine flags, dates, authentic identities and raw artwork unchanged. Former absence of a Vingroup addition is superseded for this factual callout only. No subsidiary/ownership assertion, new corporate logo, headcount, broader cross-panel wording, final image/A0 approval, commit or push is selected. Q-S25 is answered for this primary selection.


### D-064 — Remove US flag: current row is established launch/pilot footprint (2026-10-03, the student)

The student supplies the Znews article Taxi điện Green SM sẽ đến Mỹ? and explicitly says to remove the US flag because it has not officially started. Parent directly reads the 9 September 2026 article: it reports future US expansion plans, not a completed commercial launch. Adopt removal of the US flag and United States label; restore the eight-country row with the Dutch pilot still qualified. D-061's website-presence addition is superseded for poster display. The website/operator/address/promo evidence remains true as web presence but cannot verify operating-service status. The September article is not retrospectively promoted to proof of current service absence.

Selected amendment v09 controls; retained panel-1 agent produces v10 with eight-row spacing, unchanged fourteen original ordinary strings plus the two selected D-063 backing/foundation strings, unchanged raw illustration/identities and all other selected refinements. Historical images/decisions/sources preserved. No new US-planned flag, launch date, other-panel alteration, citation-face change or inferred final image/A0 approval.


### D-065 — Replace backing icon with the supplied hand-drawn Vingroup logo (2026-10-03, the student)

The student supplies `/Users/khoilq/Downloads/Vingroup_logo.svg` and explicitly requests “[Vingroup logo] Vingroup-backed” with a hand-drawn logo. Adopt substitution of the generic building icon before the existing backing label with a hand-drawn rendition of that full identity. Parent rendered and inspected the supplied source: red circular emblem, yellow bird/five stars and VINGROUP wordmark beneath. Retain all of these intrinsic logo components, with a recognisable pen/marker treatment and a clear logo-to-label gap. The original user asset is preserved; SHA-256 `3c6531a266ac19cbe9a88e6966ac0105905bf63ccb6a99d290f71f57b71365f4`.

Selected amendment v10 controls; retained panel-1 agent produces new v11 assets. Only the first backing-callout row may shift minimally to accommodate the full logo. Calendar/Founded March 2023, sixteen ordinary face strings, eight-country row and all prior vehicle artwork/identity remain. This is a graphic identity change; E-199 and D-063 continue to support the unchanged backing/foundation wording. No further ownership claim, cross-panel edit, final image/A0 approval, commit or push is inferred.


### D-066 — Correct Vingroup identity reference to stars above the bird (2026-10-03, the student)

While D-065 production is in progress, the student supplies a new logo image and states that the Vingroup stars have moved above. Adopt the newly supplied image as the controlling visual reference: five yellow stars along the red circle's upper arc, larger central star, bird lower in the circle, full red/burgundy VINGROUP beneath. Parent inspected the local attachment; SHA-256 `2145c238eb0a94cef24849ca52323563922b6f3ab2941912ca293a27f71fb973`. This is the user's graphic correction, not independent verification of an official rebrand date.

Selected amendment v11 controls; retained panel-1 agent produces new v12 assets. Supersede only the earlier SVG's lower-star arrangement. Keep D-065 full hand-drawn identity and backing-label placement, existing calendar/foundation row and all other selected copy, flags and vehicle artwork. Preserve the earlier source and v11 attempt as history; do not deliver them as current. Final student image/A0 acceptance remains pending.


### D-067 — Remove intrinsic VINGROUP wordmark beside Vingroup-backed (2026-10-03, the student)

The student explicitly requests removal of the VINGROUP wordmark below the emblem because the adjacent Vingroup-backed wording already names the group. Adopt the hand-drawn circular emblem only, with the D-066 five-star upper arc and lower bird. The prior full-wordmark inclusion is superseded. Preserve complete original source assets for provenance; omit the intrinsic wordmark from the delivered visible logo and panel.

Selected amendment v12 controls; retained panel-1 agent produces new v13 assets. Emblem fits before the unchanged Vingroup-backed label, calendar/Founded March 2023 remains below. All sixteen ordinary strings, eight-country row and prior vehicle illustration/identity remain. No other company fact, poster wording, section layout or final image/A0 approval is selected.


### D-068 — Approve section 1 image and continue with section 2 (2026-10-03, the student)

The student explicitly approves section 1 and asks to continue with the next section at a similar level of care. Section 1 production v13 is now the approved section image, with its D-067 emblem-only treatment and all preceding selected refinements. Keep this version stable and retain its agent; no additional section-1 edit is requested. This approval does not establish physical A0 fit or whole-poster acceptance.

Resume the one-section-at-a-time image discussion at **2. Target Market**, using the already approved D-043–D-046 content/composition and D-055 citation-free face. Apply D-056's existing numbered-heading instruction in a new production v06; preserve all other selected copy, counts, denominator, profile qualification and generated artwork. Retained panel-2 agent owns this narrow amendment and read-only assessment/style advice. Any new copy/composition suggestion remains a proposal until the student selects it. No later-section or A0 approval, new targeting assumption, commit or push is inferred.


### D-069 — Keep section 2 lower portion; redesign compact upper infographic independently (2026-10-03, the student)

The student says the lower portion is satisfactory and the upper portion is not. Adopt preservation of the current lower composition: location/profile qualifier, person and six selected psychographic/behavioural icon-label associations, plus the approved repeat-opportunity caption. Do not apply the parent's unadopted Mindset/Ride habits labels to this accepted portion.

The student explicitly asks to make the chart approximately half its current size, put 40.2% inside the selected 25–44 column, and have one subagent think independently about a redesigned section-2 infographic. This supersedes D-046's external above-column percentage-pill position; it does not change 40.2%'s all-city denominator, the separate 269,277 count, four age-group counts, source date/geography, target filters or proposed-profile status. Treat half-size as an approximate design footprint, preserving legible labels and proportional zero-baseline quantities.

Authorise a fresh independent upper-layout proposal and a concrete revised review draft, not merely a scaled chart surrounded by empty space. The fresh agent receives only selected content/user constraints and isolated ownership; retained panel-2 agent remains the production owner. Both stay available. Any new copy or optional shortening remains a proposal, not a new observed audience fact or final section/A0 approval. Section 1 remains accepted and unchanged.


### D-070 — Approve section 2 independent proposal A and continue with section 3 (2026-10-03, the student)

The student replies "ok đó, tiếp section 3" to the complete independent proposal A. Adopt that displayed PNG/SVG as the accepted section-2 image: compact left chart with 40.2% inside the selected 25–44 column and 269,277 above, three equal audience conditions on the right, and the unchanged previously accepted lower composition. The accepted artefact retains its proposal filename for provenance; no duplicate production-v07 render is required. Internal alternative B is not selected. Selected amendment v07 records this approval. Section 1 remains accepted and stable; physical A0/whole-poster acceptance is separate.

Resume image discussion at **3. Why Green SM?**, small **Positioning Strategy**, using D-050/D-051 selected content and composition B with the D-055 citation-free face. Apply existing numbered-heading instruction D-056 in new production v04, preserving all nineteen non-heading text objects and other artwork/layout. Retained section-3 agent owns this narrow preparation and stays available for feedback. Selected amendment v02 controls numbering; no new positioning, promise, competitor superiority, section-3 image approval, later-section or A0 acceptance is inferred.


### D-071 — Revise section 3 and assess useful About-page ideas (2026-10-03, the student)

The student agrees that section 3 needs revision and asks whether https://www.greensm.com/us-en/about supplies useful ideas. This authorises source review and concrete content/infographic recommendations. It does not select new benefit labels, shorter statement, geometry or a replacement positioning. D-051 body/P1 and composition B remain the basis while revision options are discussed; the current section-3 image is not accepted. Sections 1 and 2 remain stable.

Parent re-read the existing same-day dated About snapshot and narrowly reverified its automatic identity, zero failures. Fresh headed-Comet reconnection through the required shim failed before any target/tab opened; no successful live reread is claimed. E-203/E-204 add service-approach/value locators; E-200 retains the bounded EV/noise scope. Retained section-3 agent provides read-only advice and stays available. Parent proposal: training plus standards/customer-service procedures as the primary delivery support for Clear terms / Local care, optional EV ride character, and smaller booking/vehicle imagery with benefits made prominent. Local Respect belongs mainly with section 4. Exact additions/geometry remain unselected in panel-03-about-inspired-proposal-v01-2026-10-03.md; no new artwork production, Copenhagen performance, competitor superiority, budget/KPI, final image/A0 approval or commit/push.


### D-072 — Approve About-inspired section-3 content and infographic revision (2026-10-03, the student)

The student replies "Đồng ý" to the parent's final source-inspired recommendation. Adopt the two dominant Clear terms / Local care groups, smaller central app/vehicle, immediate owned-fleet/employed-driver basis, service-approach illustrations for training/standards/customer-service procedures, small neutral Uber/Bolt comparison and connected audience → offer → value → delivery strip. Adopt a modest bounded quieter-EV cue as supporting ride character; Local Respect remains mainly with section 4.

Selected master v03 supplies exact approved body wording plus the selected new labels. The complete D-051 positioning sentence is reflowed into semantic segments, not replaced by the worker's unselected 32-word alternative. The EV caption includes Generally and the combustion-engine comparator to preserve E-200's scope. E-203 supplies the corporate service-approach basis; its proposed Copenhagen use does not establish completed local implementation. P1, existing benefits, neutral sourced model contrast, numbered heading and D-055 citation-free face remain.

Retained section-3 agent is authorised to produce new complete image v05, using built-in image generation for any new raster art and controlled exact lettering. Preserve historical versions, sources and other sections; no duplicate or concurrent producer. This selects content/visual direction, not the unseen resulting section image or whole A0. No new observed service result, rival inferiority, budget/KPI, contribution statement, commit or push is adopted.


### D-073 — Accept completed section-3 image and resume section-4 review (2026-10-03, the student)

The student replies "được" after the complete About-inspired section-3 production v05 is displayed. Adopt that PNG/SVG as the accepted section-3 image, using selected master v03 and D-072 content. Keep accepted sections 1–3 stable. This section-image approval does not accept the consolidated A0, print quality, actual service implementation or later panels.

Continue the existing one-section-at-a-time review at **4. Brand & Promise**, with the already approved inherited Global identity → proposed Copenhagen promise distinction D-052/D-053 and citation-free display D-055. Apply existing numbered-heading instruction D-056 in a narrow new production v03; selected amendment v02 controls. No new wording, values, art or composition is adopted merely by continuing.

Current agent capacity permits a dedicated retained section-4 producer, /root/produce_panel_04, without closing or rotating existing section agents. This resolves the earlier Q-S23 resource fallback operationally rather than inventing a user choice. Parent owns approval/control records; the worker owns only new section-4 production/review files. No new source, contribution statement, budget/KPI, commit, push or submission.


### D-074 — Approve evidence-led section-4 copy and visual route (2026-10-03, the student)

After reviewing the optional section-4 insight-alignment proposal, the student instructs the parent to continue with that proposal. Adopt the exact cue/promise/touchpoint wording and the compact flow recorded in `07_drafts/design/panel-04-selected-content-and-visual-v03-2026-10-03.md` for image production. The Capital Region app-choice data is shown as four separate multiple-response cues with n=79 and sample geography; no total/pie, EU-wide preference or 25–44-specific attitude is claimed. Retain authentic global identity, the approved proposed tagline, Danish-first localisation and campaign consistency. The old audience-fit sentence that implied a measured preference is superseded by the explicit trip-control/fair-treatment appeal-to-test qualifier.

Dedicated panel-4 agent is authorised to produce complete review image v04 with exact controlled lettering and separate hand-drawn decorative art. This approves content and visual direction only. The resulting image, A0 integration and printed legibility remain pending; no new app feature, local service outcome, price leadership, superiority, budget/KPI or mark is asserted. No commit, push or submission.


### D-075 — Apply a hand-drawn Green SM lockup across current panel images (2026-10-03, the student)

The student identifies that Green SM logos in the produced panel images still use a digital/vector appearance and instructs that the logo be converted to the hand-drawn treatment throughout. Apply one shared transparent hand-drawn lockup, preserving the recognisable checkmark, exact GREEN SM wording, arrangement and cyan/yellow brand colours. Replace all Green SM lockups in the current images where present: panel 1, panel 3 and panel 4. The selected panel-2 artwork contains no Green SM lockup and receives no added logo. Preserve all approved panel copy, figures, evidence boundaries and other brand marks. Keep historical versions unchanged. New images are review candidates, not newly accepted panel images; whole-poster A0 and printed legibility remain pending. Shared art and prompt are recorded in 07_drafts/design/green-sm-hand-drawn-logo-v01-2026-10-03-prompt.md.


### D-076 — Reopen section 4 to meet Branding and Identity (2026-10-04, the student)

The student judges that the current section-4 treatment does not read clearly as, or align sufficiently with, the required Branding and Identity element. Reopen section-4 copy and infographic structure; keep the D-074 version as history, not as the accepted direction for this panel. Preserve the student's earlier distinction: Green SM's corporate identity follows the parent brand, while only the Copenhagen promise is locally targeted. The numbered heading may be revised to the brief's explicit wording, **4. Branding and Identity**, subject to the student's review of the replacement proposal.

The parent and retained section-4 agent prepare a brand-first replacement proposal, not a new image. It removes the dominant app-choice cue grid and ad-to-app campaign flow, distinguishes inherited logo/colours from the proposed local promise, makes fit to the selected target/position visible, and shows consistent use of the identity across touchpoints without implying a sales funnel. [Brand-first proposal v01](../07_drafts/design/panel-04-brand-first-options-v01-2026-10-03.md) is for discussion only. Its heading, exact copy and visual structure are not selected; do not produce the replacement image until the student approves section-4 content. Sections 1–3 remain stable. No new customer preference, brand voice, service outcome, grade or A0 acceptance is inferred.


### D-077 — Confirm section-4 heading and keep its remit focused (2026-10-04, the student)

The student selects the numbered heading **4. Branding & Identity** and removes “Plain and respectful wording” from the replacement proposal. Keep this panel focused on Green SM's inherited corporate identity, the proposed Copenhagen promise and consistent brand expression. Sections 2 and 3 retain the detailed target and positioning analysis; include only a short target/position link needed to show that the local message fits the chosen plan. Do not repeat the audience profile, positioning statement, service model or digital/sales process here. The tagline, language-order line and illustrated touchpoints remain proposed pending review of [content v02](../07_drafts/design/panel-04-brand-first-content-v02-2026-10-04.md). No image production is authorised before exact copy approval.
