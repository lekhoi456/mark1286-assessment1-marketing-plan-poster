# References workflow and supporting scripts

Adapted from the existing reference workflow for **MARK1286 Assessment 1: Marketing Plan Poster (group)**. P0 setup and P1 extraction are complete. At the 28 September 2026 research checkpoint, 97 candidate sources are registered for Green SM and the four-market comparison; no poster citation set is approved. Run commands below from `assessment1-marketing-plan-poster/`. Use `python3 -B`; package, browser and model caches stay outside iCloud.

## 1. Governing rules

- **No PDF, no citation.** A cited work needs its actual PDF in `04_references/`, a registry entry, an effective verified identity state (`match` or an explicitly audited `accepted-manual`) and manual checking of the work and the claim. A webpage needs a dated PDF snapshot. A DOI, search snippet, abstract, slide bibliography or generated reference alone is not evidence.
- `04_references/references.json` is the single source of truth. Edit it; generate `references.html` and `reference-list.md` with `refs.py build`. Never hand-edit generated outputs. The HTML is an offline report suitable for sharing with the lecturer after the audit, not evidence that an empty registry has been researched.
- **Never fabricate** metadata, quotes, dates, DOIs, page numbers, claims or contributions. Record unresolved details as `UNVERIFIED` in `notes`; do not cite the source until resolved. Agents never invent a student email for Crossref.
- **Module-first, not module-only** (D-010). Record the module deck/slide in `module_source` when applicable. Outside concepts are allowed with a verified PDF and an `outside` flag in `03_course_materials/concept-register.md`; set `outside: true` on their reference entries too. External market evidence need not pretend to have been taught. Manual concept-scope review remains necessary.
- Cite original slides, cases and the handbook, not Study Hub lesson text. Study Hub PDF conversions can serve as copies of the original course material after checking slide/page fidelity. Perplexity outputs are leads only, never sources.
- Module slide references are not trusted bibliographic records: the discrepancies recorded in D-005 require verification at the original source. Do not import another assessment's references or scope restrictions.

## 2. Style authority

Use **Cite Them Right Harvard, 13th edition (2025)** as directed by the workspace. The saved authorities under `00_brief_and_criteria/source/` are:

| Saved file | Role |
|---|---|
| `greenwich-library-referencing-libguide.pdf` | Greenwich points students to Cite Them Right; the full online resource requires sign-in. |
| `greenwich-referencing-generative-ai-2026.pdf` | Greenwich guidance on acknowledging/referencing generative AI. |
| `ou-cite-them-right-harvard-quick-guide.pdf` | In-text rules and common source formats. |
| `cccu-cite-them-right-harvard-guide-2025.pdf` | 13th-edition guidance, including tutor material on the VLE. |
| `cumbria-cite-them-right-quick-guide-2025.pdf` | 13th-edition conventions, including no place of publication and DOI treatment. |
| `newcastle-cite-them-right-harvard-style-sheet-2025.pdf` | Webpages, reports, suffixes and other source types. |
| `worcester-cite-them-right-13th-edn-short-guide-2025.pdf` | Common source formats and chronological multiple citations. |

The saved Sheffield 2023 guide is based on an older edition; it is not authority for overriding 13th-edition rules. The renderer is ported from the source workspace; its prior verification is not claimed as a new MARK1286 test.

### Adopted conventions

- One author: `(Surname, 2025)`; two: `(Surname and Surname, 2025)`; three: name all three; four or more: first author plus italic *et al.*. List every author in the reference list.
- Organisation author when credited as author; title when genuinely no author. Do not manufacture an organisation author from an unrelated website owner.
- `no date`, not `n.d.` in rendered citations; JSON accepts `n.d.`. Same author/year uses suffixes in alphabetical title order. Multiple works in one citation are earliest first.
- Give precise locators for quoted words and non-obvious claims. A PDF page index and a printed page number can differ: keep both in the evidence log and cite the appropriate printed locator.
- Alphabetical reference list; sentence-case work titles; journal titles retain title case; single quotation marks around article/chapter titles; italic book, journal and webpage titles.
- No place of publication. Non-first editions use `nth edn.`. DOI as `https://doi.org/...`, without an accessed date; URLs without DOI require `(Accessed: day month year)`.

| Type | Renderer pattern (fields, not invented references) |
|---|---|
| Journal article | Author (Year) ‘Title’, *Journal*, volume(issue), pp. first–last. Available at: DOI. |
| Book | Author (Year) *Title*. nth edn. Publisher. |
| Chapter | Author (Year) ‘Title’, in I. Editor (ed.) *Book title*. Publisher, pp. first–last. |
| Webpage/report | Author or organisation (Year) *Title*. Available at: URL (Accessed: date). Reports may add number/publisher. |
| Course deck | Presenter (Year) ‘Title’, *MARK1286: Marketing and Sales in the Future Economy*. University of Greenwich. Available at: Moodle URL (Accessed: date). |
| News article (online) | Author (Year) ‘Title’, *Newspaper*, Day Month. Available at: URL (Accessed: date). With no personal author the newspaper title takes the author position and is not repeated after the title: VietnamPlus (2023a) ‘Title’, 14 April. Available at: URL (Accessed: date). Basis: CCCU Cite Them Right guide 2025, "If no author is given, use the newspaper title instead"; confirm the final form in Cite Them Right Online. Registry type `news-article` (added 27 September 2026) with `container` and `day_month`. |

The parent should confirm disputed details in Cite Them Right Online through Greenwich: final DOI punctuation; `(eds.)`; social-media/dataset templates; same-author no-date suffix spacing; slide locator syntax; and the publication year for genuinely undated VLE material. Do not guess a presenter or silently infer a deck's date from the current year. Public-guide patterns are working conventions, not a claim of institutional confirmation.

## 3. Retrieval order

1. **Agent finds open access.** Check the publisher, Unpaywall (using a real supplied email if needed), author/institutional repositories, then Scholar's versions. Prefer the version of record; record accepted/submitted manuscript versions accurately and check pagination. For a publicly accessible publisher PDF use ordinary retrieval or `save_web_pdf.py LANDING_URL NAME.pdf --fetch-pdf PDF_URL`.
2. **Parent agent uses the student's Comet session.** Subagents never access Comet. Supply the parent with title, DOI/URL, reason needed and failed OA routes. Use Greenwich SSO through `https://go.openathens.net/redirector/gre.ac.uk?url=<encoded article URL>`.
3. **Student inbox.** If institutional retrieval fails, ask the student to download the identified work into `04_references/_inbox/`. The agent checks, renames, verifies and registers the actual file. Never register a download request as a retrieved source.

### Parent-only Comet procedure

1. Student enables remote debugging at `chrome://inspect/#remote-debugging`; Comet writes `~/Library/Application Support/Comet/DevToolsActivePort`.
2. Run `python3 -B 06_workflow/scripts/comet_cdp_shim.py --port 9333` as a named service. It listens on loopback only and supplies `/json/version`; it is discovery, not a browser proxy.
3. Parent attaches a dedicated tab using `cdp_url: "http://127.0.0.1:9333"`; student accepts Comet's remote-debugging prompt. Never navigate the student's existing tab.
4. Open the OpenAthens redirector. If Greenwich MFA appears, the student completes it. Do not store credentials or codes.
5. Fetch the authorised PDF inside the publisher page with session credentials. Confirm `%PDF-`, then inspect `pdfinfo`/`pdftotext`, title, authors, year/version and quoted pages before registering (`retrieval.method: "comet-sso"`). Publisher terms may need the student's acceptance.
6. Stop the shim and tell the student remote debugging may be unticked. The worker does not exercise this route.

## 4. Naming and registry schema

Key: ASCII kebab-case `{authors}-{year}{suffix}`. One/two authors use family names; three or more use `{first}-et-al`. Organisations use their name. No date becomes `nd`. The internal three-author key does not change the in-text three-author rule. PDF: `{key}-{short-title}.pdf`. Set `file` to the basename only, never a URL or a path through `_inbox`.

Top level is `{"meta": {...}, "entries": []}`. `meta` contains `title`, `module`, `assessment`, `style`, `style_sources` (saved paths) and `mailto` (blank until a real email is supplied; `REFS_MAILTO` overrides it).

| Entry fields | Meaning |
|---|---|
| `key`, `type`, `status` | Unique key; type below; `candidate`, `cited` or `archived`. |
| `authors`, `editors` | Lists of `{"family": "...", "given": "..."}` in printed order; renderer generates initials. |
| `organisation` | Credited organisational author when no personal author. |
| `year`, `suffix`, `title` | Printed year or `n.d.`; optional same-year suffix; verified title. |
| `container`, `volume`, `issue`, `pages`, `article_number` | Journal/book details; pages such as `45-64`. |
| `edition`, `publisher`, `report_number` | Type-specific metadata. `place` can be retained for the record but is not rendered. |
| `module`, `institution`, `platform`, `day_month` | Course details, social platform or upload/post date as appropriate. |
| `doi`, `url`, `accessed` | Bare DOI; actual URL; ISO viewed date `YYYY-MM-DD` (required with ordinary URL). |
| `file` | Actual PDF basename in `04_references/`; in `_archived/` only when archived. |
| `retrieval` | `{"method": "...", "from": "source URL or original path", "date": "YYYY-MM-DD"}`. Methods: `open-access`, `comet-sso`, `user-download`, `course-material`, `web-snapshot`. |
| `verification` | `crossref`, `pdf_text`, `checked_on` written by `verify`; `notes` records the manual title/author/year/claim checks with date and evidence locators. Do not fabricate automated results. |
| `verification_accept` | Documented Crossref differences: list of `{"field": "title", "reason": "PDF-backed reason", "accepted_on": "YYYY-MM-DD"}`. Only title/container/volume/issue/pages. Never DOI/year/author differences. |
| `pdf_identity_accept` | Optional explicit audit for a correct PDF whose title/author is not captured by the text check. Bound to the exact PDF and bibliographic identity; effective status is `accepted-manual`, never an automatic match. Full contract below. |
| `module_source`, `outside` | Module provenance, e.g. `[{"slug": "w01-lecture", "slide": 7, "cited_as": "verbatim slide reference"}]`, only when true; `outside: true` for an outside concept. |
| `used_for`, `notes`, `citation_aliases` | Poster panel/pitch section; uncertainties/version notes; optional credited organisation abbreviations. |

Supported types: `journal-article`, `book`, `ebook`, `chapter`, `webpage`, `report`, `vle-slides`, `social-media`, `dataset`, `video`, `news-article`. Required type fields are defined in `refs.py` and checked by `build`. This schema is descriptive; never add sample entries to the live registry.

## 5. Register, verify, use and archive

### Academic work or report

1. Establish why it is needed; identify genuine module provenance or the outside concept. Never copy a slide reference unverified.
2. Retrieve and inspect the PDF, name it, add a `candidate` entry from the PDF and publisher metadata.
3. Run `refs.py verify --key KEY`. Crossref compares title, family names, year, container, volume, issue and pages; PDF matching checks title words and first author/organisation on the first two pages. Web snapshots also check the printed accessed date.
4. **Manual second check:** open the saved PDF; confirm full title, all authors, year, version/edition, DOI and actual pages. Read the claim in context, record the exact quote/locator in `02_research/evidence-log.md`, and put a dated account in `verification.notes`. Automated matching is approximate: it does not establish year from the PDF, all authors, claim meaning or reliable OCR.
5. Resolve differences, never alter verified bibliography merely to appease Crossref. A permitted `verification_accept` needs a specific PDF-backed explanation. A DOI/year/author mismatch needs correction or dropping the source, not an override.
6. Run `verify` again, then `build`. Mark `cited` only when the work is actually cited and both manual/automated gates are complete. Copy references from generated output. `check-draft` audits citations and the References section against the registry.

### Explicit PDF identity exceptions — added 28 September 2026

Genuine source identity can be absent from a text layer: an image-only Commission logo, a Statbank API table with only its official source URL, an English title starting after a Hindi section, a byline on page 3, or an official bilingual corporate name. **Do not alter metadata merely to make matching pass.** Inspect the actual page/provenance first, then record the specific evidence.

The optional entry-level `pdf_identity_accept` object requires exactly these eight fields:

| Field | Required meaning |
|---|---|
| `sha256` | Lower-case SHA-256 of the actual PDF bytes; obtain with `refs.pdf_sha256(path)`. |
| `identity_sha256` | `refs.pdf_identity_sha256(entry)`: exact title, authors, editors, organisation, year, type, accessed, URL, DOI and retrieval method. |
| `fields` | Sorted list exactly matching the automatic mismatches; only `author` and/or `title`. |
| `checked_on` | Real, non-future ISO date of the actual inspection. |
| `verified_by` | Who actually inspected it; never invent a student's check. |
| `locator` | Exact PDF page/region and any saved provenance-source locator. |
| `evidence` | What was actually read/seen and how it establishes the correct identity. |
| `reason` | Why this correct identity is missing from the automatic text check. |

Run `verify` before binding an inspected exception so the automatic record contains current hashes. `verification.pdf_text` retains its **mismatch**, details and hashes; `pdf_state(entry)` derives the separate **accepted-manual** state. The CLI, HTML cards, build report and citation gate disclose that distinction. Changing the PDF or a bound identity field invalidates the acceptance and requires a new inspection/binding.

No exception can accept a missing/invalid PDF, extraction error, unsupported/incomplete source type, stale automatic check, missing/wrong accessed stamp, or a DOI/year/author disagreement with Crossref. Crossref remains an independent gate with the same restricted difference-acceptance list. A manual identity exception does **not** validate a quotation's meaning, survey representativeness, company performance or current legal applicability.

Observed integration: 79 automatic matches and 18 audited manual acceptances across 97 candidates; **14 isolated regression cases passed**. Real-source before/after checks reproduced and then rejected stale snapshot metadata and stale Crossref year/DOI acceptance. The Statistics Denmark API-table path retained its author mismatch and passed only with the PDF/provenance-backed audit; changing its metadata rejected that acceptance. No original source bytes were rewritten to manufacture an author.

Regression command: `python3 -B -m unittest discover -s 06_workflow/scripts -p test_refs_pdf_identity.py -v`.

### Cached-verification freshness — corrected after independent review

Every cached automatic PDF **match**, not only manual exceptions, now requires current PDF-byte and bibliographic-identity hashes. A replaced file or changed accessed date cannot inherit an earlier green badge/citation clearance. Missing old bindings require a new `verify`.

Crossref comparisons separately bind `title`, `authors`, `editors`, `organisation`, `year`, `type`, `doi`, `container`, `volume`, `issue`, `pages` and `article_number`. Changing those fields invalidates the stored comparison. `--offline` may refresh the PDF check but cannot silently refresh Crossref; run online `verify` for an absent/stale binding. Build, HTML and draft citation consumers use the same effective state without new network calls. The existing live DOI entry was reverified online after this cutover.

**28 September build audit:** 0 errors, 17 advisory warnings, 18 explicit manual-acceptance notes. Four ordinary title-capitalisation cases were corrected. Remaining warnings are reviewed, not suppressed: 13 internal key suggestions concern stable acronym/English-name/transliteration choices (for example ACEA, ILT, TCA, `faerdselsstyrelsen`, `kjaergaard` and `q-and-me`); four title heuristics flag the proper series/programme/body/legal names *The Connected Consumer*, *Special Eurobarometer*, *Technical Group on Population Projections* and the *Delhi Motor Vehicle Aggregator and Delivery Service Provider Scheme*. These keys are not Harvard display authors. Preserve correct credited names rather than rewriting them to satisfy ASCII heuristics; reassess only actual citation formatting when a poster citation set is selected.

Browser interaction confirmed search, current counts and the separate `accepted-manual`/automatic-mismatch disclosure on a real Statistics Denmark card. The browser screenshot helper and a separate headed attach timed out; standalone Chrome nevertheless wrote a screenshot before its process deadline, and that image was visually inspected. Evidence: `07_drafts/reviews/reference-audit-2026-09-28.png`. This is a reference-report check, not a poster/A0 legibility check.


### Webpage

Save `save_web_pdf.py URL KEY-SHORT-TITLE.pdf`. It prints title, full URL, page number and accessed timestamp on every page. Before printing it repairs two layout problems found on the Green SM site on 27 September 2026, and reports both in its output ("Print repairs: …"): fixed elements parked outside the viewport (closed navigation drawers) are hidden and visible fixed headers are pinned once, so they no longer cover the article on every printed page; fixed-height scroll containers are expanded, so a long article no longer prints as one truncated page. Always check the page count and the word count, and look at one rendered middle page (`pdftoppm -f 2 -l 2 -r 60 -png FILE /tmp/p`) for real content, not a login, consent wall, block page, overlay or truncated page. Hiding consent overlays is not consent acceptance. Use `--keep-banners` when removal would hide substantive content. Do not use `--no-header-footer` for citation snapshots.

Use the actual displayed author/year; no publication date means `n.d.`, not the snapshot year. Store the printed ISO date in `accessed`; `retrieval` describes the actual retrieval. If refreshed before submission, replace deliberately (`--force`), update the accessed date and re-verify. Never treat a publisher PDF fetched with `--fetch-pdf` as a dated webpage snapshot.

### Green SM pages: Comet, headed (D-025)

Every page on the Green SM websites (greensm.com, id.greensm.com and the country sites) is opened in the student's Comet browser, visibly, never in headless Chrome. Parent agent only:

1. Start the shim as a named service: `python3 -B 06_workflow/scripts/comet_cdp_shim.py --port 9333` (Comet must have remote debugging enabled; `~/Library/Application Support/Comet/DevToolsActivePort` exists).
2. In the JavaScript eval: `const { openCometTab, cometSave } = await import('<workspace>/06_workflow/scripts/comet_capture.mjs'); await openCometTab(browser);` The student may have to click **Allow** in Comet.
3. `await cometSave(browser, URL, '/tmp/<name>.pdf', { delay: 6000 })` prints the page to PDF from the dedicated tab with the same header, footer and print repairs as `save_web_pdf.py`; the header ends with "[Comet]". Consent banners are hidden, never accepted.
4. Check pages, words and one rendered middle page; move the file to `04_references/` with its final name; register with `"retrieval": {"method": "web-snapshot", "from": URL, "date": ..., "browser": "Comet (headed, D-025)"}`; run `refs.py verify`.
5. Country sites name their publisher in the footer (for example "Green SM Denmark ApS", "Green and Smart Mobility Netherlands B.V."): register that entity as the organisation, which also keeps identical page titles on different country sites apart. `refs.py verify` accepts a web page's publisher found anywhere in the snapshot and records where.
6. At the end of the session stop the shim and close the tab.

### Course deck

Check the original title slide, credited presenter and dates; do not cite the Study Hub's lesson author. Check PDF page N corresponds to slide N before saving a copy into `04_references/`. Set type `vle-slides`, the MARK1286 module and Greenwich institution; use the real Moodle URL and actual accessed date. Unknown attribution/date remains unresolved, not invented. Same presenter/year requires title-ordered suffixes when multiple decks are registered.

### Archive unused work

Move the actual PDF into `_archived/`, keep its basename in `file`, set status `archived`, preserve its metadata and retrieval history, then rebuild. Before submission archive unused candidates and reconcile `_inbox/`. Do not delete inconvenient evidence or imply an archived source supports an active citation.

## 6. Commands and exit behaviour

```sh
python3 -B 06_workflow/scripts/refs.py build
python3 -B 06_workflow/scripts/refs.py verify
python3 -B 06_workflow/scripts/refs.py verify --key KEY
python3 -B 06_workflow/scripts/refs.py verify --key KEY --offline
python3 -B 06_workflow/scripts/refs.py check-draft 07_drafts/DRAFT.md
python3 -B 06_workflow/scripts/save_web_pdf.py URL KEY-SHORT-TITLE.pdf --delay 8000
python3 -B 06_workflow/scripts/save_web_pdf.py LANDING_URL KEY-SHORT-TITLE.pdf --fetch-pdf PDF_URL
python3 -B 06_workflow/scripts/comet_cdp_shim.py --port 9333
python3 -B 06_workflow/scripts/analyse_market_selection.py
python3 -B 06_workflow/scripts/model_marketing_scenarios.py
```

- `build`: renders offline HTML and the `cited`-only Markdown list; exits 1 on registry errors. It still writes a diagnostic report when errors exist: generation is not approval to cite.
- `verify`: repeat `--key` for multiple entries; default checks all entries. `--offline` skips Crossref and does not turn a missing/old online check into a new success. Missing PDFs fail and replace stale PDF-success records. An empty registry is honestly zero entries checked, not completed research.
- `check-draft`: exits 1 on unknown citations, missing PDFs, incomplete verification or registry/reference-list errors. It also reports style warnings and globally cited entries absent from this draft. For separate poster/pitch audits, review those absence warnings in context without hiding real mismatches.
- `save_web_pdf.py`: additional options `--out-dir DIR`, `--timeout SECONDS`, `--chrome PATH`, `--keep-banners`, `--force`, `--no-header-footer` (not for citation snapshots). Uses temporary Chrome profile outside the workspace; needs installed Google Chrome and Poppler (`pdfinfo`, `pdftotext`). No logged-in Comet session is used.
- Every script supports `--help`. `refs.py` subcommands also support it. Python standard library except PowerPoint extraction (`python-pptx` via `uv`); PDF/OCR dependencies below are system binaries.

The two research calculation scripts use saved JSON inputs and write deterministic JSON outputs beside them in `02_research/`. The first implements the pre-scoring K1–K6 method and sensitivity; the second calculates unapproved budget/funnel/contribution scenarios. Neither predicts academic marks or establishes commercial feasibility. Their human-readable interpretation remains in the focus-market and budget/KPI notes.

## 7. Material extraction and concept tools (P1 complete; commands retained)

```sh
# Narrow integration smoke: one deck, then the Tesla PDF only.
uv run --with python-pptx python -B 06_workflow/scripts/extract_materials.py --slug w01-lecture
python3 -B 06_workflow/scripts/extract_materials.py --slug w04-tesla
# Full P1 extraction completed 27 September; rerun only when inputs change.
uv run --with python-pptx python -B 06_workflow/scripts/extract_materials.py
# Replace extracts after source/script changes if needed.
uv run --with python-pptx python -B 06_workflow/scripts/extract_materials.py --slug w01-lecture --force
python3 -B 06_workflow/scripts/check_register_quotes.py
python3 -B 06_workflow/scripts/check_register_quotes.py --self-test
python3 -B 06_workflow/scripts/make_concept_list.py
```

Extractor reads `../study-hub/content/materials.json` as a file catalogue, not a source of claims. `--slug` is repeatable; positional slugs also work. Default and explicit selection exclude weeks 7–9 and Assessment 2 vlogs; invalid/out-of-scope slugs fail. The handbook is retained as the A1 authority even though it mentions the other assessment. No recordings are transcribed by this script; Lecture 6 transcription remains P1.

PPTX output has numbered `## Slide N` sections, tables, available SmartArt/alt text/hyperlinks and speaker notes. PDF output has `## Page N`; `pdftotext -layout` is supplemented by `pdftoppm` and English `tesseract` OCR on low-text pages. Temporary images stay outside iCloud and are removed. DOCX uses macOS `textutil`; image exemplars record paths/dimensions (`sips`) only, not supposed handwriting transcriptions. Dependencies: `uv`, `python-pptx`, Poppler, Tesseract with English data, and macOS `textutil`/`sips` as applicable.

For the Tesla smoke, inspect `extracted/w04-tesla.md` for `(OCR)`, word counts and the explicit manual-verification warning. **Every OCR quote must be checked against the rendered original page.** A checker match to OCR does not verify that OCR is correct. For the deck smoke, inspect numbered slides and a notes-bearing slide against the original; no concept register is produced by extraction.

The concept register is intentionally absent in P0. Both default concept commands return `PENDING` and exit 1 until it exists; never create a dummy register merely to turn a gate green. Headings use `### ` followed by a backticked concept ID, an em dash and the concept title. The list generator derives terms from those headings only; it imports no concepts or aliases from the other assessment.

Quote format is one or more `> ` lines immediately followed by `— ` and a backticked extracted slug plus `sN`/`p. N`; semicolons separate sources. Every quoted line must appear exactly in every named location. For an outside concept, use the registered reference key plus PDF page index `p. N`; the checker reads that active saved PDF via `pdftotext`. Check the printed locator and outside/PDF approval manually. Do not use blockquotes for commentary in files passed to this checker. `module-handbook` is a whole-file exception because DOCX extraction has no page markers. `--self-test` uses an isolated synthetic fixture outside the workspace and does not assert that a real register exists or passes.

## 8. Poster counts and pitch timing

```sh
python3 -B 06_workflow/scripts/wordcount.py 07_drafts/POSTER.md --mode poster
python3 -B 06_workflow/scripts/wordcount.py 07_drafts/PITCH.md --mode pitch --wpm 130
python3 -B 06_workflow/scripts/wordcount.py 07_drafts/PITCH.md --json
```

`--mode auto` (default) detects pitch speaker/time comments; otherwise poster. Poster `##` panels carry `<!-- budget: N -->`; heading words count. Pitch `##` sections carry `<!-- speaker: Name -->` and `<!-- time: m:ss -->`, where time is that section's allocated **duration**, not its start timestamp. Speaker names must match the confirmed roster; no speaking contribution is inferred by the counter.

Both modes exclude title/front matter, comments, code fences, images, Markdown-only markers, table separator rows and the References section onwards. Link labels count but destinations do not. Pitch additionally excludes headings, `Owner:` lines and `[stage directions]`. Default citations count; `--exclude-citations` excludes parenthetical Harvard citations. `--exclude-headings` optionally excludes poster headings. A word is a whitespace-delimited token containing a letter/digit. These are working counting conventions, not a lecturer-issued poster limit.

Reports give each section and, for pitch, each speaker's words, allocated duration and estimated duration at `--wpm` (default 130). Missing metadata, panel overruns and sections whose estimated speaking time exceeds their allocation exit 1. JSON fields: `mode`, `wpm`, `total_words`, `sections` (`heading`, `words`, `budget`, `speaker`, `time_seconds`, `estimated_seconds`), `speakers`, `total_estimated_seconds`, `total_time_seconds`, `errors`. No inherited 1,000-word cap applies. The presentation checker handles the overall 15-minute/three-speaker requirements and poster budget/KPI tables. Rehearsal must allow pauses, handovers and pointing to the poster; word-rate estimates are not proof of actual timing.

## 9. Final reference audit

- Every cited work has the correct saved PDF, current verification, and a dated manual title/all-author/year/version/claim check.
- Every factual claim links to a verbatim quote and locator in the evidence log; OCR quotes are manually checked.
- Every concept is module-backed or explicitly outside with a verified PDF; no slide bibliography is blindly copied.
- `verify`, `build` and final `check-draft` have no unresolved errors; all warnings have been read and resolved or explicitly explained.
- Web snapshot dates match `accessed`; decks have confirmed presenter, year, Moodle URL and slide fidelity.
- Final design contains the approved Markdown text unchanged; reference italics, suffixes, alphabetical order and locators survive layout.
- Unused sources are archived, inbox reconciled, and the lecturer's active references folder contains the actual PDFs plus generated HTML/Markdown. Do not claim approval of the AI hand-drawn-style production route: compliance remains to be confirmed.

## P0 port verification record

The script worker exercised all seven `--help` interfaces; both default concept commands returned `PENDING` with exit 1 because the real register is absent. A temporary pitch input counted four spoken words while excluding its heading, Owner line, stage direction, image, comment and reference section; the temporary input was removed. Explicit selection of an Assessment 2 vlog was rejected with exit 2 before extraction. These are scoped CLI observations only: parent integration still owns reference generation, the one-deck/Tesla extraction smoke and any browser checks. No full extraction, concept research or P1 register has been completed by this port.
