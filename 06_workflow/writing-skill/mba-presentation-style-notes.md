# mba-presentation-style installation notes

Date: 27 September 2026. Scope: MARK1286 Assessment 1 only, under D-011. No Assessment 2 or vlog materials are prepared.

## Installed specialist

- Claude: `~/.claude/skills/mba-presentation-style/`
- Codex: `~/.codex/skills/mba-presentation-style/`
- Both contain `SKILL.md`, `CHANGELOG.md`, `scripts/presentcheck.py` and references covering genres, checker contracts, exact-text design hand-off and calibration.
- The specialist follows the existing `mba-diary-writing-style` inheritance pattern. It does not edit either parent writing skill, the diary specialist, either copy of `draftcheck.py` or the avoid-ai-writing checkout.

## Project configuration, not global defaults

- Paper: **A0**, following the lecturer instruction relayed by the student (D-007), overriding the source's A1 requirement. Orientation and typography are design-phase decisions.
- Pitch: **15:00**, followed by **5:00** of questions. Every member speaks; the distribution is decided by the group, not hard-coded globally.
- `../../00_brief_and_criteria/poster-headings.txt`: canonical eleven H2 panel names. There is no second copy to keep in sync.
- `speakers.txt`: Nguyen Phi Giao, Le Quoc Khoi and Nguyen Ho Khanh Vy. This is a speaking/answer-ownership roster, not a claim about contributions already made.
- The poster must also carry confirmed student numbers: 001545326, 001545344 and 001545423 respectively. Identity and contribution truth require manual checks; the wrapper does not invent or authenticate them.
- No business has been chosen. These configuration files are not poster copy and contain no business facts or fabricated evidence.

The proposed AI-made hand-drawn-style production route is the student's decision (D-008). Compliance with the physically hand-drawn requirement and AI-use rules remains unconfirmed. Never call it lecturer-approved. Approved Markdown text is placed by a layout tool, not generated as image-model lettering.

## Use from the workspace root

```bash
python3 -B ~/.claude/skills/mba-presentation-style/scripts/presentcheck.py "$POSTER" \
  --mode poster --headings 00_brief_and_criteria/poster-headings.txt \
  --registry 04_references/references.json --sources 04_references \
  --concepts 03_course_materials/concept-list.txt --strict-scope

python3 -B ~/.claude/skills/mba-presentation-style/scripts/presentcheck.py "$PITCH" \
  --mode pitch --speakers 06_workflow/writing-skill/speakers.txt \
  --duration 15:00 --wpm 130 \
  --registry 04_references/references.json --sources 04_references \
  --concepts 03_course_materials/concept-list.txt --strict-scope

python3 -B ~/.claude/skills/mba-presentation-style/scripts/presentcheck.py "$QA" \
  --mode qa --speakers 06_workflow/writing-skill/speakers.txt \
  --registry 04_references/references.json --sources 04_references \
  --concepts 03_course_materials/concept-list.txt --strict-scope
```

Set `POSTER`, `PITCH` and `QA` to actual approved/versioned draft paths when they exist. Do not create fake drafts just to make these commands pass. `--json` retains full base findings and explicit genre reviews. A missing checker or detector is a failure, not a skipped layer.

## Contracts and integration

Read the installed `references/checker-contract.md` before drafting. Poster panels use positive integer budget comments. Every poster contains one `budget-table` marker with exact columns `Item | Amount | Share (%) | Basis` and one `kpi-table` marker with exact columns `KPI | Objective | Target | Tracking tool | Review rhythm`. Financial rows use plain decimal amounts/shares and a final Total row. All KPI cells are required. An allocation's Basis is `Assumption: explanation` or `Evidence: E-001`. These labels do not verify the underlying evidence.

Pitch sections use H2 headings, exact speaker comments and positive m:ss allocations. Q&A uses consecutive H3 Q-number headings and Owner lines. `wordcount.py` is the separate project counter; use its presentation counts rather than the inherited essay count. The agreed counting convention excludes reference sections, comments, Markdown markers, images, link destinations and table separator rows, counts poster headings, and excludes spoken headings/Owner lines/stage directions. See the parent-owned workflow for the operational sequence.

The wrapper delegates registry/source/concept checks to the unchanged base. It cannot prove that a PDF supports a claim, verify outside-concept flags, authenticate group contributions, judge KPI quality, establish feasibility, confirm approval or check the exported visual surface. It does not impose a universal poster size or an implicit 15-minute total. Real rehearsal and final artwork inspection remain required.

## Preservation and validation status

The worker was interrupted after writing the installation. Its proposed full before/after manifests were not saved; no full-tree preservation check is claimed. The baseline Claude base-checker SHA-256 retained in its notes is `5934dba184903e6dfe0859059e7691728a5c3da53308c311d948e854c45d6f6b`. Integration records observed checks and their limits in `protection-report.json` and `smoke-results.md`.

Integration ran the isolated calibration recipe on both Claude and Codex installations: all 14 expected outcomes passed on each. These cover clean poster/pitch/Q&A; invalid sums, panel budget, KPI, headings, inherited banned wording, timing, owners and Q&A numbering; permitted spoken question handling; and fail-closed behaviour when the detector is absent. Temporary fixtures were removed automatically. This is mechanical verification, not a writing-quality benchmark, lecturer validation or a completed assessment draft.

The installed `references/calibration-plan.md` retains further proposed human/model evaluation. The claude.ai copy is not updated automatically; local installation and Codex mirroring do not upload skills to that service.
