# P0 integration smoke results

Date: 27 September 2026. Scope: apparatus for MARK1286 A1, not a finished assessment. Synthetic inputs were isolated in system temporary directories and removed. No fake business claims, concept register or references were inserted into the live workspace.

## Observed results

| Surface | Execution / observation | Outcome |
|---|---|---|
| Seven ported CLIs | Script worker ran all seven `--help` entry points | All succeeded |
| Reference output | Parent ran `refs.py build` | Generated `references.html` and `reference-list.md`; 0 entries, 0 cited; 0 errors/warnings/notes |
| Empty verification | `refs.py verify --offline` | Exit 0; explicitly 0 entries verified, not completed source research |
| Missing-PDF gate | Isolated registry with an absent PDF and stale prior match, actual `cmd_verify` | Exit 1; stored PDF verification changed to error; 'no PDF, no citation' reported |
| Real course extraction | `extract_materials.py --slug w01-lecture --slug w04-tesla` via uv/python-pptx | 22 numbered lecture slides and two Tesla pages; OCR on both Tesla pages; 2 written, 0 skipped, 0 failed |
| OCR warning | Opened resulting Tesla Markdown | OCR statistics, original text layer and explicit original-page verification warning present; visible OCR artefacts mean no accuracy certification |
| Quote checker | `check_register_quotes.py --self-test` | PASS: valid synthetic baseline accepted, 2/2 planted errors rejected |
| Absent real register | Script worker ran both default concept commands | Both returned PENDING/exit 1; no dummy register/list created |
| Concept list | Isolated register passed to actual list generator | Only two supplied concept headings emitted, case-insensitive duplicates removed; no inherited aliases |
| Poster word counter | Temporary panel, five words including heading | Budget 5 passed; budget 4 returned exit 1; reference text excluded |
| Pitch word counter | Script worker's temporary CLI fixture | Four spoken words; heading/Owner/stage/image/comment/reference exclusions and link-label retention observed |
| A1 scope guard | Script worker selected `sample-vlog-1` | Exit 2 before extraction; no A2 output |
| Dated PDF snapshot | Actual `save_web_pdf.py` on localhost generated report | One-page PDF; module text, accessed timestamp and exact URL found; temporary profile/output outside iCloud |
| HTML report behaviour | Opened generated report in browser; used search and Cited filter | Correct module/assessment/style and honest zero counts; empty filtered state remained 0 of 0 |
| Report visual proof | Chrome print-to-PDF rendered to PNG and opened | Actual print surface inspected; registry filename contrast defect fixed and re-rendered successfully |
| Comet discovery shim | Actual HTTP handler on a temporary loopback port, synthetic DevToolsActivePort file | `/json/version` and `/json/list` correct; missing file returned 503; server stopped |
| Protected base checker | SHA-256 compared with pre-install value retained in worker notes | Exact match; see `protection-report.json` |

## Presentation checker

The recipe in the installed skill's `references/calibration-plan.md` was executed independently against both Claude and Codex paths. All **14 expected outcomes passed on each installation**:

1. Valid poster: exit 0.
2. Invalid budget total: exit 2.
3. Exceeded panel budget: exit 2.
4. Missing KPI field: exit 2.
5. Wrong required heading: exit 2.
6. Inherited banned wording: exit 2.
7. Valid pitch: exit 0.
8. Invalid pitch allocation: exit 2.
9. Unknown/missing speaker: exit 2.
10. Purposeful spoken rhetorical question: exit 0 with explicit genre-review record.
11. Valid Q&A: exit 0.
12. Invalid Q&A numbering: exit 2.
13. Missing Q&A owner: exit 2.
14. Unavailable detector: exit 1, not a skipped/passing layer.

The actual inherited detector ran for the normal fixtures. Tests did not modify the base checker or detector. Fixtures are not assignment content and were not retained in `07_drafts/`.

## Integration correction

The generated report originally rendered `references.json` white on white in print: its inline `color:#fff` overrode the print header's black text. Changed that inline colour to `inherit` in the local `refs.py`, rebuilt and repeated the PDF render. The inspected corrected image shows the filename legibly; screen header still inherits its white text. No bibliography logic or template workspace was changed by this correction.

## Limits

- Browser screenshot calls timed out despite successful page inspection/actions, including in dedicated Chrome. Reported to tool QA. Visual confirmation used the actual Chrome-rendered PDF/PNG instead; browser screenshot coverage is not claimed.
- No real Comet login, MFA, publisher download or new Crossref network verification was attempted. The shim test proves only local discovery/error behaviour. Institutional access is documented, not newly certified.
- No cited business sources exist yet. Empty-registry success is setup evidence only.
- No full P1 extraction, concept register, Lecture 6 transcription, assignment draft, real rehearsal or final A0 artwork is complete.
- Skill validation is mechanical. No writing-quality, trigger or comparative model benchmark and no lecturer endorsement are claimed.
- A pre-install full-tree hash manifest did not survive the interrupted worker. Only the recorded base-checker fingerprint establishes a before/after match; do not imply a broader hash proof.
