# Workflow: A1 poster, pitch and Q&A

Authority: `../AGENTS.md`, source brief/rubric, and append-only decisions. Reuse the research discipline of BUSI1764, not its diary constraints. The plan controls what is done and when; this file controls how.

## 1. Session and phase protocol

Read HANDOFF once at session start, then the requested panel/file. Search specific decisions, questions or evidence only when relevant; do not load the full control bundle. Follow the lightweight routine in `../AGENTS.md` (D-078). Update HANDOFF when state changes, append actual new decisions, and update plan/requirements/questions only when their subject changes. This document is a reference, not a checklist to run on every prompt.

Scope checks to the change: inspect altered artwork; check changed wording and supporting claims; recalculate changed figures. Use the complete review checklist for an explicit full review or final assembly. Preserve earlier validation of unchanged inputs without describing it as a new run. No automatic full-registry verification, concept-register audit, independent review or extra report for a local edit.

Source precedence: current assessment documents plus documented local lecturer instructions. Preserve conflicting original wording and explain which instruction controls. Group choices are not lecturer permission. Agent operational tests are not official rubric descriptors.

## 2. Evidence before prose

| Claim | Evidence requirement |
|---|---|
| Business/offer/location/price fact | Primary source saved as PDF; date and precise locator |
| Central customer need, competitive advantage or strategic claim | Two substantively independent sources where obtainable, including one independent of the business; otherwise narrow and disclose limits |
| Market statistic | Official/credible research source with population, year, geography, unit and relevant method |
| Concept | Module register with exact wording and locator; original work if actually read, otherwise the teaching source |
| Cost estimate | Quote/rate or transparent assumption, quantity, period, currency and calculation |
| Forecast/target | Label as proposed; identify inputs and uncertainty; never state it as performance achieved |
| Group action/contribution | Student-confirmed record; distinguish assignment from completion |

Record accepted claims in the evidence log. A registry check validates bibliographic handling, not whether the source proves the claim. References on slides can be wrong; retrieve and check rather than copy. OCR and automated transcripts are search aids until inspected against the source image/audio.

## 3. Research and selection

Follow `../02_research/research-design.md`. Freeze gates/weights before scoring; explain score reasons, uncertainty, sensitivity and alternatives. Group chooses the case and strategic choices. Save PDF candidates, register sources, collect locators, assess independence, then write. Keep failed leads and source conflicts visible in research notes. No disguised assumption fills a data gap.

P1 register protocol: extract the original A1 materials, record verbatim quotes and slide/page IDs, separate interpretation from source words, check quotations, then generate the concept list. A missing register is pending work, not a passing scope check. Outside concepts are allowed only under D-010, with the outside flag and PDF verification.

## 4. Perplexity protocol

1. Agent writes `02_research/perplexity/prompt-NN-topic.md` for the approved phase and bounded research question.
2. Student runs Deep Research. Save the full returned text and source list verbatim in `output-NN-topic.md`.
3. Preserve output body unchanged. Store run date and provenance in a separate `run-NN-topic.md` note; if the output itself includes a date, retain it.
4. Write `reconciliation-NN-topic.md` separately: original-source checks, accepted/rejected leads, evidence IDs and remaining gaps. Do not append commentary into the verbatim output.
5. Never cite Perplexity, the Study Hub or an agent as authority for business facts.

## 5. References and acquisition

Detailed procedure: `references-workflow.md`. Use the registry as the only bibliographic source of truth. Open access first; institutional Comet via OpenAthens only by the parent agent; manual `_inbox/` download if inaccessible. No account passwords or MFA codes in saved files. Filename key convention is separate from Harvard author display.

Run from the workspace root:

```bash
python3 -B 06_workflow/scripts/refs.py verify
python3 -B 06_workflow/scripts/refs.py build
python3 -B 06_workflow/scripts/refs.py check-draft 07_drafts/poster-v01-YYYY-MM-DD.md
```

Use actual filenames, not the symbolic example. Inspect title, authors, year, locators and claim support manually. An empty registry passing build means infrastructure works, not that the assessment is reference-ready. Archive dropped references only once no active artefact cites them; preserve the registry history and PDF.

## 6. Draft contracts and checks

### Poster copy

For complete internal Markdown checks, map all eleven elements to the canonical headings in `00_brief_and_criteria/poster-headings.txt`. The poster face uses the approved numbered display headings plus identity cloud (D-036–D-037, D-056, D-077), not eleven compulsory verbatim headings. Each checked panel has one `<!-- budget: N -->` comment. Budgets are internal readability limits, not an official assessment word limit. Check the changed panel rather than rebuilding the full draft for a local edit.

Retain evidence comments such as `<!-- E-001 -->` and Harvard/source mappings internally. No visible citations or source footers on the poster face (D-055/LG-004). Preserve the exact approved identity cloud; contribution records must be truthful, with final contribution/reference packaging resolved at finalisation. Generate any reference list from the registry.

Style (D-022): each panel names the module concept it applies and shows it working for Green SM in the focus market; a concept is never a bare label. Use short, complete statements wherever a claim, a reason or a causal link is made, and bullet fragments only for genuine lists (channels, KPIs, budget lines). The UK moderator may see only the poster, so the argument must be readable without the pitch. Do not copy the Tesla mini-case's structure; the eleven brief headings and the rubric govern.

For machine-readable arithmetic, put `<!-- budget-table -->` immediately before a Markdown table with exactly these column labels:

`Item | Amount | Share (%) | Basis`

Use non-negative decimal numbers with at most two decimal places, without currency symbols/thousands separators, in Amount and Share cells. State currency and planning period in adjacent prose. Each allocation's Basis must be `Evidence: E-001` (or multiple evidence IDs) or `Assumption: explanation`. End with a Total row. Check total amounts, percentages and row-share consistency; cost × quantity calculations belong in the linked underlying model as well.

Put `<!-- kpi-table -->` immediately before a table with these labels:

`KPI | Objective | Target | Tracking tool | Review rhythm`

Every cell must be meaningful, not just non-empty. Unit, baseline if known, target period and corrective-action rule must remain visible in the plan even when the short poster table is compressed. The checker cannot establish whether an objective or target is sensible.

```bash
python3 -B 06_workflow/scripts/wordcount.py 07_drafts/poster-v01-YYYY-MM-DD.md
python3 -B ~/.claude/skills/mba-presentation-style/scripts/presentcheck.py \
  07_drafts/poster-v01-YYYY-MM-DD.md --mode poster \
  --headings 00_brief_and_criteria/poster-headings.txt \
  --registry 04_references/references.json --sources 04_references \
  --concepts 03_course_materials/concept-list.txt --strict-scope
```

### Pitch

Each H2 section contains one `<!-- speaker: Name -->` and one `<!-- time: m:ss -->` allocation. Speaker names must match the supplied roster. Bracketed stage directions, e.g. `[Point to the budget]`, are not spoken. Keep citations/source notes available for checking without treating them as proof of spoken duration. Use a separate References section for bibliography rather than reading it aloud.

```bash
python3 -B 06_workflow/scripts/wordcount.py 07_drafts/pitch-v01-YYYY-MM-DD.md --wpm 130
python3 -B ~/.claude/skills/mba-presentation-style/scripts/presentcheck.py \
  07_drafts/pitch-v01-YYYY-MM-DD.md --mode pitch --wpm 130 --duration 15:00 \
  --speakers 06_workflow/writing-skill/speakers.txt \
  --registry 04_references/references.json --sources 04_references \
  --concepts 03_course_materials/concept-list.txt --strict-scope
```

The rate is a provisional estimate, not a fact about these speakers. All three must speak; approximate five-minute shares are a proposal until the group decides. Rehearse with actual members, pauses and handovers; record real timings and revise. Do not label an estimated runtime as a completed rehearsal.

### Q&A

Use `### Q1. <question>` etc., followed by `Owner: <confirmed name>`. Answers distinguish what is known, what is assumed and what would change the decision. Number sequentially; avoid unassigned items or scripted claims of research the group did not conduct.

```bash
python3 -B ~/.claude/skills/mba-presentation-style/scripts/presentcheck.py \
  07_drafts/qa-v01-YYYY-MM-DD.md --mode qa \
  --speakers 06_workflow/writing-skill/speakers.txt \
  --registry 04_references/references.json --sources 04_references \
  --concepts 03_course_materials/concept-list.txt --strict-scope
```

### Concept and style gate

After changing the register or re-extracting its sources:

```bash
python3 -B 06_workflow/scripts/check_register_quotes.py
python3 -B 06_workflow/scripts/make_concept_list.py
```

Read installed `--help` for exact options. `presentcheck.py` wraps the frozen base draft checker and its anti-slop detector. Poster fragments/labels and legitimate spoken questions are genre-specific review cases, not reasons to suppress integrity failures. Record justified overrides in the version review. Do not update the calibrated base checker/detector before the other assessment is submitted. A clean mechanical gate is not a content-quality judgement.

## 7. Review and revision loop

1. Draft from the approved plan with `mba-presentation-style`; write the hardest panel first and count it immediately.
2. Run counts, reference checks, concept checks and the presentation gate; resolve failures or document narrow intentional style exceptions.
3. Check manually: every factual claim follows from its PDF, key numbers reconcile, assumptions/targets are labelled, concepts actually inform choices, every requirement is covered.
4. Send the same version and source brief/rubric to two independent reviewers, without the writer's preferred grade. Local-marker lens: reference accuracy, practical fit, compliance. UK-moderator lens: reasoning, theory application, UK English and coherence. Both assess the full rubric, not just their lens.
5. Require criterion score/maximum, quoted weak point, evidence, risk and actionable revision. No official performance-band table is supplied; predicted scores are estimates with uncertainty. Reviewers do not claim to be the real markers.
6. Parent integrates agreement/disagreement and a prioritised fix list. Revise to vNN+1; never overwrite a reviewed version. Do not remove genuine analytical tension merely to please a reviewer.
7. Group approves the content. Update requirements and decisions from actual outcomes.

At P8 reviewers inspect the actual rendered poster/export as well as copy. If only Markdown was reviewed, say so; visual quality cannot be inferred from text.

## 8. Design and arithmetic controls

- Final design only after copy approval. A0, 841 × 1189 mm; orientation and tool confirmed at P7.
- Preserve approved text through a layout tool. Do not rely on an image model for names, citations, numbers, tables or lettering.
- Charts show values from the checked model; no decorative invented percentages or fabricated 'before/after' results.
- Validate physical-size legibility, citation size, contrast, colour-independent labels, reference-side inclusion and exported-file readability.
- Maintain one budget model and one KPI map. Propagate any changed figure to poster, script and Q&A; do not fix copies independently.
- Resolve production/AI permission questions once, recording the reply or absence of confirmation accurately.

## 9. Versioning, finalisation and submission

New working versions belong in `poster/`, using descriptive panel/version names. Never edit historical content through a shortcut. Existing drafts, renderers and their inputs are preserved in `archive/`; `07_drafts` is a compatibility symlink. Keep a renderer with the relative inputs it needs. Save a separate report only when a substantial review needs one; routine check results can be reported in chat. Final approved package: `08_final/`.

Use the full checklist for complete-artefact reviews and submission, not every panel adjustment. All three members upload the same approved poster independently; retain all three receipts and inspect the submitted preview. Agent does not send lecturer messages, submit work, claim permissions, or record contribution completion without instruction/evidence.

## 10. What tools do not prove

- Quote matching does not resolve slide context, OCR errors or applicability.
- DOI/PDF matches do not guarantee source credibility or support for a specific sentence.
- Budget sums do not establish commercial realism; non-empty KPI fields do not establish a valid measurement design.
- Estimated word timing does not replace real rehearsal.
- A skill/checker smoke run does not establish improved writing quality or predict a mark.
- An A0 digital export does not prove physical print quality or lecturer acceptance of its production route.
