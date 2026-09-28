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
