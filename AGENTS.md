# AGENTS.md — MARK1286 Assessment 1: Marketing Plan Poster (group)

Workspace for one piece of assessed work: the group **Marketing Plan Poster** (50%, LO1–LO2) for **MARK1286 Marketing and Sales in the Future Economy**, University of Greenwich MBA Global, taught offline in Can Tho, Vietnam. Formal submission **14 October 2026** (handbook; the Can Tho date and time are still to be confirmed, Q-L1). A 15-minute pitch plus 5 minutes of questions in class (date not yet known, Q-S1). First-marked by the local lecturer, moderated by a UK marker.

Group of three (student numbers and names as supplied by the student on 27 September 2026; `01_context/group-roster.md`):

| Student number | Name |
|---|---|
| 001545326 | Nguyen Phi Giao |
| 001545344 | Le Quoc Khoi (the student this workspace serves) |
| 001545423 | Nguyen Ho Khanh Vy |

Assessment 2 (Individual Vlog) is out of scope here (D-001).

Business chosen by the group: **Green SM** (GSM Green and Smart Mobility JSC, Vietnam; Xanh SM until 13 April 2026), a multi-country company (D-018). **Focus market: Copenhagen, Denmark**, app-booked electric taxi rides (D-031). Segment S1 (resident self-paid repeat taxi users), positioning P1 and a DKK600,000 12-month market-entry budget are chosen (D-032); line items, channels, assumptions and targets still need approval. Company facts carry an "as at" date; eight-market context includes the Dutch pilot (D-019, D-024).

## Start of every session

1. Read `HANDOFF.md`: current phase, work in progress, next actions, what we are waiting for.
2. Read `01_context/decision-log.md` (settled decisions) and `01_context/open-questions.md`.
3. Read the current phase in `05_plans/master-plan.md`, then that phase's inputs.
4. Talk to the student in **Vietnamese**. Write **every saved file in English (UK)**.

## End of every session

1. Update `HANDOFF.md`: status, next actions, waiting-on, and a new entry at the top of the session log.
2. Record decisions in `01_context/decision-log.md` (append; never rewrite history) and new questions in `open-questions.md`.
3. Update the Status column of `05_plans/master-plan.md` and, after each draft review, of `00_brief_and_criteria/requirements-matrix.md`.

## The task in brief

During a "Marketing Business Bootcamp", the group develops a comprehensive marketing strategy for a real or hypothetical business from any country, summarises it on one poster and pitches it in class. The poster must include at least eleven elements: Student/Business Details; Company/Business Introduction; Target Market Analysis; Positioning Strategy; Branding and Identity; Digital Marketing Tactics; Sales Strategies; Budget and Resource Allocation; Measurement and Evaluation; Creativity and Innovation; Alignment with Business Objectives. Seven rubric criteria: company background and country context 10, target market, segmentation and branding 15, digital marketing and sales strategies 20, budget and resource allocation 15, KPIs aligned with objectives 10, creativity and emerging concepts 10, visual appeal and presentation quality 20. Verbatim brief: `00_brief_and_criteria/brief.md`; rubric: `00_brief_and_criteria/rubric.md`; requirements: `00_brief_and_criteria/requirements-matrix.md`.

## Non-negotiable rules

1. **Module-first scope** (D-010). Every marketing concept on the poster or in the pitch comes from the module's teaching resources and has an entry in `03_course_materials/concept-register.md`, quoted verbatim with its slide. An outside concept is allowed only with a verified PDF in `04_references/` and an `outside` flag in the register.
2. **Never fabricate.** No invented facts, figures, quotes, dates, authors, page numbers, DOIs or URLs. Plan figures are sourced calculations or explicit assumptions in `02_research/marketing-plan/`. Distinguish **unapproved agent scenarios** from **group-approved assumptions**; neither is observed company performance. Negative economics must remain visible.
3. **No PDF, no citation.** A work is cited only when its PDF is in `04_references/`, registered in `04_references/references.json` and verified (`refs.py verify`). Web pages are saved as dated PDF snapshots. Slide reference lists are never copied without verification: several are wrong (`06_workflow/references-workflow.md`). Procedure: `06_workflow/references-workflow.md`.
4. **Evidence log.** Every factual claim that reaches a draft has an entry in `02_research/evidence-log.md` (source key, locator, verbatim quote).
5. **Group integrity** (D-009). The poster states who contributed which part. Contribution statements, group decisions and anything the group did come only from the student's confirmed statements (`01_context/group-roster.md`, decision log). Never invent them.
6. **The group decides** (D-009). The agent drafts everything. The group's decisions (business, priority segment, positioning, brand identity, budget total, final wording, design) reach the agent through the student's prompts and are logged with the decider. The agent proposes with evidence and flags trade-offs.
7. **Poster format** (D-007, D-008, D-021, D-022). A0; the lecturer has agreed to the AI-made hand-drawn-style route, as relayed by the student. Content is written and approved in Markdown first, with explicit applied analysis sufficient for poster-only assessment. Place the exact approved text with a layout tool, never an image model's lettering. Use the brief's exact headings, all three names/numbers and truthful contributions. Do not reopen production-route approval or copy the old Tesla/2025 bullet-only approach.
8. **Numbers add up.** Budget lines sum to the stated total and to 100%; every KPI names its objective, target, tracking tool and review rhythm. Checked by script before each review.
9. **Timing.** Pitch 15:00 plus 5:00 of questions; every member speaks (three speakers, about 5:00 each unless the group decides otherwise).
10. **Language and style.** UK spelling; Cite Them Right Harvard (13th edn, 2025) as used by Greenwich; plain, specific marketing English on the panels; spoken British English in the pitch.
11. **Drafting tools** (D-011). Poster copy, pitch script and Q&A bank are written with `mba-presentation-style` (`~/.claude/skills/mba-presentation-style/SKILL.md`, a specialisation of `mba-writing-style`) and checked with its `presentcheck.py`, which runs the avoid-ai-writing detector through `draftcheck.py`. Do not update `draftcheck.py` or the avoid-ai-writing checkout before 12 October 2026: another assessment is calibrated to them.
12. **Research apparatus stays behind the scenes** (D-013). Research questions, scoring matrices, evidence logs and audit trails organise our work. The poster shows marketing analysis, not our method.
13. **Autonomous preparation** (D-027). Complete research, reconciliations, options, models and verification without overnight questions. Do not adopt country/segment/position/budget/wording, invent member activity or imply six hours were worked. Preserve group approval gates; do not stall independent research behind a deferred decision.

## Folder map

| Folder | Holds | Rules |
|---|---|---|
| `00_brief_and_criteria/` | Verbatim brief, rubric (Part A authoritative wording; Part B agent operational tests, not official grade bands), requirements, exemplar lessons and original sources | Verbatim text is never edited; notes go in `> Note:` blocks |
| `01_context/` | Course context, the student's requirements, group roster, decision log, open questions, message for the lecturer | Decision log is append-only |
| `02_research/` | `research-design.md`, `evidence-log.md`; `business-selection/` (P2), `business-dossier/` (P3), `market-analysis/` (P3: market, consumers, competitors), `marketing-plan/` (P4: STP, positioning, brand, channels, sales, budget model, KPIs, innovation, alignment), `perplexity/` (prompts and verbatim outputs) | Perplexity output is a lead, never a source |
| `03_course_materials/` | Catalogue, 23 A1 extracts, verified concept register/list and Lecture 6 transcript/guidance | Originals stay in `..`; Study Hub prose is not a source; P1 extraction is complete, with student review of the register still open |
| `04_references/` | One PDF per cited work, `references.json` (single source of truth), `references.html` and `reference-list.md` (generated); `_inbox/` for the student's downloads; `_archived/` for dropped works | Edit the JSON, then run `refs.py build`; never hand-edit generated files |
| `05_plans/` | `master-plan.md`; later `poster-blueprint.md` (P5: panel map, word budgets) and `pitch-plan.md` (P6) | — |
| `06_workflow/` | `workflow.md` (procedures), `references-workflow.md`, `checklists/`, `scripts/`, `writing-skill/` (notes on `mba-presentation-style`, backups) | Scripts: Python stdlib or `uv run --with …` |
| `07_drafts/` | `poster-vNN-YYYY-MM-DD.md`, `pitch-vNN-….md`, `qa-vNN-….md`; `reviews/`; `design/` (design brief, layout proofs, exports) | Never overwrite a version; create the next one |
| `08_final/` | Final poster copy, final design files (A0), the image or file submitted, printed reference list, final pitch script, submission receipts | — |
| `09_feedback/` | `formative/` (lecturer guidance log), `summative/` (marks, comments) | — |

## Naming

- Files: kebab-case. Drafts `07_drafts/poster-v01-2026-10-06.md`, `pitch-v01-…`, `qa-v01-…`; reviews `07_drafts/reviews/poster-v01-review.md`.
- Draft markup (read by `wordcount.py` and `presentcheck.py`): poster panels are `## <element name>` with `<!-- budget: N -->` under the heading; pitch sections are `## <section>` with `<!-- speaker: Name -->` and `<!-- time: m:ss -->`; Q&A items are `### Q<n>. <question>` with an `Owner: <Name>` line; stage directions in `[…]` are not spoken; evidence IDs go in `<!-- E-012 -->` comments. Details: `06_workflow/workflow.md` §6.
- Reference PDFs: `{key}-{short-title}.pdf`; key = Harvard kebab-case `{authors}-{year}{suffix}`: one or two authors by family name (`kotler-armstrong-2018`), three or more as `{first}-et-al-{year}` (`nazir-et-al-2025` for Nazir, Rizwan and Zhu), organisations by name (`world-bank-2025`), no date `nd`.
  Filename keys are not Harvard display strings: a three-author in-text citation normally names all three authors; four or more use *et al.*. Follow the verified Cite Them Right guides (D-017).
- Perplexity: `02_research/perplexity/prompt-NN-topic.md` and `output-NN-topic.md` (verbatim, with run date).
- IDs: requirements `R01`; decisions `D-001`; questions `Q-L1` (lecturer), `Q-S1` (student or group), `Q-I1` (internal); evidence `E-001`; rubric tests as in `rubric.md` Part B.

## Scripts (`06_workflow/scripts/`)

Run from this folder. Exact options: each script's `--help`.

| Script | Purpose | Run |
|---|---|---|
| `extract_materials.py` | Extract A1-relevant catalogued materials into `03_course_materials/extracted/` (slide-numbered decks with notes; PDFs by page with OCR flagged for verification); default excludes A2 vlogs and Weeks 7–9 | `uv run --with python-pptx python -B 06_workflow/scripts/extract_materials.py [--force]`; see `--help` for selected-file smoke |
| `refs.py` | Build report/list; verify current PDF bytes/identity and DOI metadata; `check-draft <file>`; audited manual identity exceptions remain visibly distinct and fail when stale | `python3 -B 06_workflow/scripts/refs.py build` |
| `save_web_pdf.py` | Dated headless snapshots of non-Green-SM sites only; all greensm.com visits use headed parent Comet under D-025 | `python3 -B 06_workflow/scripts/save_web_pdf.py URL NAME.pdf` |
| `wordcount.py` | Words per poster panel against `<!-- budget -->`; speaking time per pitch section and speaker at a words-per-minute rate | `python3 -B 06_workflow/scripts/wordcount.py <draft.md> [--wpm 130]` |
| `check_register_quotes.py` | Verify every `>` quote in the concept register against the extracted materials (exit 1 on failure; `--self-test`) | `python3 -B 06_workflow/scripts/check_register_quotes.py` |
| `make_concept_list.py` | Regenerate `03_course_materials/concept-list.txt` (permitted concepts for the scope check) from the concept register | `python3 -B 06_workflow/scripts/make_concept_list.py` |
| `comet_cdp_shim.py` | HTTP discovery shim so the browser tool can attach to Comet's remote-debugging session (parent agent only) | `python3 -B 06_workflow/scripts/comet_cdp_shim.py --port 9333` |
| `comet_capture.mjs` | Save a Green SM page (or any page that must be opened in Comet) as a dated PDF from a dedicated tab in the student's headed Comet browser (D-025; parent agent only) | JavaScript eval: `await import('…/comet_capture.mjs')`, then `openCometTab(browser)` and `cometSave(browser, URL, OUT)`; see `06_workflow/references-workflow.md` §5 |
| `analyse_market_selection.py` | Frozen K1–K6 weighted comparison, sensitivity and joint stresses; scores are not marks | `python3 -B 06_workflow/scripts/analyse_market_selection.py` |
| `model_marketing_scenarios.py` | Assumption-labelled allocations, funnel, incentives, repeat/B2B rides and contribution/break-even cases | `python3 -B 06_workflow/scripts/model_marketing_scenarios.py` |
| `test_refs_pdf_identity.py` | Isolated regressions for manual/automatic freshness, snapshot stamps and independent Crossref gates | `python3 -B -m unittest discover -s 06_workflow/scripts -p test_refs_pdf_identity.py -v` |
| `~/.claude/skills/mba-presentation-style/scripts/presentcheck.py` | Writing gate for poster copy, pitch scripts and Q&A (anti-slop, citations, scope, budgets, table sums, timing) | `06_workflow/workflow.md` §6 |

## Institutional access with Comet (parent agent only)

Paywalled articles are fetched through the student's Comet browser, where he is signed in with his University of Greenwich Microsoft account. Subagents never drive Comet. Proven on 2026-09-27 in the BUSI1764 workspace with SAGE, Emerald, JSTOR and Springer:

1. The student opens `chrome://inspect/#remote-debugging` in Comet and ticks "Allow remote debugging for this browser instance" (per browser instance: expect to redo it after Comet restarts). Comet writes `~/Library/Application Support/Comet/DevToolsActivePort`.
2. Start the shim as a named service: `python3 -B 06_workflow/scripts/comet_cdp_shim.py --port 9333` (Comet's own HTTP discovery returns 404 in this mode).
3. Attach with the browser tool: `browser.open({ name: "refs-sso", app: { cdp_url: "http://127.0.0.1:9333" }, url, persist: true })`. The student clicks **Allow** on Comet's "Allow remote debugging?" prompt. Always use this dedicated tab; never navigate the tab he is using.
4. Route through the university's OpenAthens redirector, which works across publishers: `https://go.openathens.net/redirector/gre.ac.uk?url=<encoded article URL>`. The first sign-in of a session may stop at Greenwich MFA (`login.gre.ac.uk`): bring the tab to the front and ask the student to enter the code.
5. Download inside the page with `fetch(pdfUrl, { credentials: "include" })` and write the bytes to disk; check the `%PDF` header, then title, authors and pages with `pdfinfo`/`pdftotext` before registering. JSTOR first requires its terms form (the student's session accepted JSTOR's standard terms on 2026-09-27).
6. At the end: stop the shim service; tell the student he can untick remote debugging.

Full reference procedure: `06_workflow/references-workflow.md`.

## Environment

- This folder is in iCloud Drive: never create virtualenvs, `node_modules`, `__pycache__` or caches here. Use `python3 -B` or `uv run --with <pkg> python -B`. Model and package caches stay in their default locations outside iCloud (`~/.cache`).
- The shell's `cp` is GNU; use `/bin/cp -c` for APFS clones.
- Paths contain spaces and square brackets: quote them.
- This folder is its own **private** git repository, `lekhoi456/mark1286-assessment1-marketing-plan-poster` (branch `main`), created 28 September 2026 at the student's request. The parent folder is a separate repository that excludes this folder through its local `.git/info/exclude`. This repository's `.gitignore` excludes PDF, DOCX, PPTX, JPG and ZIP files (copyrighted sources stay local in iCloud) but not PNG or SVG, so design exports would be tracked. Keep it private: it holds student numbers and extracted course material. Do not commit or push unless the student asks.
- Course sources: originals in `..`; PDF conversions in `../study-hub/public/materials/<slug>.pdf` (for a deck, PDF page N = slide N). The Study Hub's lesson text (`../study-hub/content/`) is a study aid and is never cited.
