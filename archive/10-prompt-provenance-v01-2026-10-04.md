# Section 10 native artwork prompt and provenance

Date: 4 October 2026. Status: delegated candidate for parent selection, not group approval.

## Executed prompt

Use case: infographic-diagram.
Asset type: one transparent sprite sheet of four small decorative drawings for a student marketing-plan panel about business goals and controlled Copenhagen growth.
Input images are style references only: use the thin imperfect navy pen contours, visible flat cyan/yellow marker strokes and simple hand-drawn character of the supplied poster sections. Do not copy their lettering, composition or logo.
Primary request: make four clearly separated little illustrations in a 2 by 2 grid, each isolated with generous transparent margin so it can be placed individually:
top left, a small cyan taxi on a short stable ground stroke beside a simple blank clipboard and two tiny checkpoint flags, suggesting a stable local operation with stage gates;
top right, a small phone with blank screen, magnifying glass and two empty speech bubbles, suggesting search/social awareness;
bottom left, a small cyan electric taxi with a yellow lightning symbol and a rider entering beside a simple charging plug, suggesting app-booked electric mobility;
bottom right, a small rider and cyan taxi with one short curved return arrow, suggesting repeat trips rather than indefinite expansion.
Style/medium: thin slightly uneven navy fineliner outlines, sparse flat streaky marker colouring, hand-drawn student sketch. Compact friendly pictograms, few details, no gloss, no 3D shading.
Colour palette: navy #173a47, cyan #26c6cf, yellow #ffd400, very pale warm highlights.
Background: genuinely transparent alpha, not a paper sheet or checkerboard.
Constraints: no words, letters, digits, logos or badges; every phone and clipboard completely blank. No bars, graphs, monetary symbols, performance scores, emission plumes, tailpipe icons, lifecycle claims, maps or expansion destinations. No connecting lines between the four sprites. Entire outlines remain inside each cell, generous space between cells. These are conceptual planning illustrations, not observed results.

## Actual native generation

Built-in `image_gen.imagegen`; one call with `transparent_background=true`. The two supplied local PNGs were viewed first and used solely as style references:

- `poster/08-candidate-v01-2026-10-04-small.png`
- `poster/03-logo-candidate.png`

Original native output: `/Users/KHOILQ/.codex/generated_images/01a10052-be76-7750-8e04-af9a43fd23fe/exec-8fe94f34-9d43-4360-a4c5-b9e11ad9023f.png`.

Workspace original: [generated art](10-candidate-v01-2026-10-04-generated-art.png). It is copied byte unchanged and retained as RGBA, 1536 × 1024, alpha range 0–254. The source was inspected: four conceptual scenes, no observed lettering, logo, digits, scores or result charts. The modest halo/background alpha in the raw transparent sheet appears as pale marker texture on the warm-paper section.

## Controlled assembly

Four half-width/half-height SVG source viewports isolate the sprites with explicit source-coordinate clips. The entire unchanged PNG is embedded self-contained for each placement. Python reads metadata and arranges SVG; it does not repaint or edit raster pixels.

All 18 text objects come from [controlled copy](10-copy-v01-2026-10-04.md). CoreText resolves local MarkerFelt-Thin and Noteworthy-Light explicitly, writes glyph outlines, and rejects ordinary font fallback. Slightly uneven frames, rules, marker ribbons and linking arrows are layout-native pen paths. The four rows are goal–objective–action relationships, not a time sequence or measured growth curve. No logo is needed in this alignment panel.

The [manifest](10-candidate-v01-2026-10-04-manifest.json) records exact copy, glyph files, artwork hash, source/target crops, objective mapping and boundaries. Reproduce with `python3 -B poster/10-candidate-v01-2026-10-04-render.py`, then `python3 -B poster/10-candidate-v01-2026-10-04-check.py`. Existing macOS fonts and `/opt/homebrew/bin/rsvg-convert` are used. No dependencies/caches were created in iCloud.

Current work is confined to new `poster/10-*` files. No other panel, historical production, shared asset or project-level control was edited.

