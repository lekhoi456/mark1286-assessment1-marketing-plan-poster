# Scaled-plan proof v05 — production brief

7 October 2026. D-164. Base: [proof v04](poster-scale-plan-v04-2026-10-07-prompt.md) (D-163). Status: proof awaiting student review.

**Change.** The student finds the ten cyan dashed arrows between cells useless and cluttered, so they are removed. Nothing else changes: all lettering, figures, shapes and colours of v04 stay byte-identical. The arrows inside cells (Section 1 phone → car, Section 6 repeat loop, Section 8 M4 → M6) are original artwork and stay. Copy v46's *Connections* list no longer applies.

**Back of chart.** Unchanged: `poster-scale-plan-v04-2026-10-07-back.*` (21 references).

**Checks** (`poster-scale-plan-v05-2026-10-07-checks.json`): the v04 checks pass, and v05 equals the v04 front with only the connected-cells group and the SVG title/description changed; no connector group or dashed cyan path remains.

Rebuild: `python3 -B poster/poster-scale-plan-v05-2026-10-07-render.py poster/poster-references-v04-2026-10-07.svg OUT`, after the v04 build in the same OUT, then the v05 check script with the same arguments.
