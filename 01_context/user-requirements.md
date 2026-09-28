# Student requirements

Recorded from the student's initial instructions and follow-up decisions. This file preserves scope; settled choices are in `decision-log.md`. The agent must not treat unanswered questions as decisions.

## Process and research

1. Work phase by phase, with detailed inputs, methods, outputs and gates. Explain the next phase before starting it; obtain decisions that belong to the student or group.
2. Reuse the BUSI1764 research discipline: brief-derived research questions; weighted selection criteria and sensitivity checks; claim-level evidence log; append-only decisions; versioned drafts; independent mock marking against the actual rubric.
3. Remove BUSI1764-specific Ashoka, venture eligibility, internationalisation gates, diary/reflection apparatus and word limit.
4. The agent drafts all components. The group chooses and sends decisions through the student's prompts. Do not invent group experience or individual contributions.
5. Never fabricate evidence, sources, figures, calculations, quotations, business activity or contribution statements.

## Language and organisation

6. Chat in Vietnamese. Save all files and assessment text in English (UK); preserve source quotations verbatim even where their spelling differs.
7. One workspace per assessment with `00_brief_and_criteria` through `09_feedback`, plus AGENTS.md, HANDOFF.md and CLAUDE.md (`@AGENTS.md`).
8. A1 first. A2 starts only after A1 is finished; do not create even an A2 skeleton now.
9. Keep memory and current phase in HANDOFF.md. Do not commit without a request.

## References and course materials

10. No PDF, no citation. Every cited source must have a verified PDF in `04_references/`, named `{authors}-{year}{suffix}-{short-title}.pdf` using the registry key convention.
11. Registry `references.json` is authoritative; generate `references.html` and the reference list. Move unused works to `_archived/`.
12. Cite Them Right Harvard, 13th edition (2025). Verify metadata and claims at the source; no blind copying from slide bibliographies.
13. Retrieval: agent open-access search, then parent agent using the student's Comet/UoG institutional session through OpenAthens, then student manual downloads to `_inbox/`.
14. Perplexity: agent writes prompts, student runs Deep Research, output saved verbatim in `02_research/perplexity/`. Verify leads at original sources; never cite Perplexity.
15. Study Hub is a learning aid and file catalogue, not a source. Cite original slides and publications.
16. Module-first concepts (selected option a): verified concept register from teaching materials; outside concepts only with a verified PDF and explicit outside flag. There is no imported BUSI1764 module-only rule.

## Tooling

17. Copy and adapt seven scripts: refs.py, save_web_pdf.py, comet_cdp_shim.py, wordcount.py, extract_materials.py, check_register_quotes.py and make_concept_list.py. Smoke-run the actual paths.
18. Adapt catalogue paths, module/assessment metadata and poster/pitch counting; do not retain the diary's 1,000-word constraint.
19. iCloud: no virtualenv, node_modules or __pycache__ in the workspace. Use `python3 -B` or `uv run --with ... python -B`; package/model caches outside iCloud.
20. Use mba-writing-style 2.0.0 and avoid-ai-writing. Create one specialist skill, mba-presentation-style, scoped to A1 rather than two poster/vlog skills. Preserve existing calibrated tools.

## Poster and group

21. Size A0, following the local lecturer's instruction relayed by the student. A1 printed in the separate brief is not the group's design size.
22. Content first in Markdown; final production is AI-designed in a hand-drawn style. Do not start artwork before content approval. This group choice is not evidence of lecturer approval of the production method.
23. Members: 001545326 Nguyen Phi Giao; 001545344 Le Quoc Khoi; 001545423 Nguyen Ho Khanh Vy.
24. Genuine contribution allocation and records are still required; agent assistance cannot be misreported as each member's completed work.
25. P0 discovery was completed before workspace creation. P0 setup is now being completed after the student chose A1, full-agent drafting, module-first scope and one presentation skill.
