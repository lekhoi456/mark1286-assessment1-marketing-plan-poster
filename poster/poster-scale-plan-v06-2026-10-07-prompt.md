# Scaled-plan proof v06 — production brief

7 October 2026. D-165. Base: [proof v05](poster-scale-plan-v05-2026-10-07-prompt.md) (D-164). Status: proof awaiting student review.

**Change.** The cloud line *All targets and pilots are group proposals* is removed at the student's request. The seven remaining cloud lines move down 2 units so the block stays centred in the cloud. Nothing else changes; the back of chart stays `poster-scale-plan-v04-2026-10-07-back.*`.

**Checks** (`poster-scale-plan-v06-2026-10-07-checks.json`): the v05 checks pass, and v06 equals the v05 front with only this line dropped, the cloud baselines shifted and the SVG title/description updated.

Rebuild: `python3 -B poster/poster-scale-plan-v06-2026-10-07-render.py poster/poster-references-v04-2026-10-07.svg OUT`, after the v04 and v05 builds in the same OUT, then the v06 check script with the same arguments.
