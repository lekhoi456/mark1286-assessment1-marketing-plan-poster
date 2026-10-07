# Section 8 v02 art and visual provenance

Session date: 4 October 2026. Controller requested a more visual, compact alternative to v01. Candidate status remains pending parent selection; no group approval is claimed.

## Executed native illustration prompt

Use case: illustration-story. Create a wide 4:1 horizontal sprite strip of FOUR separate simple hand-drawn infographic symbols, evenly spaced in four equal columns on warm cream paper (#fffdf5). From left to right: (1) a small megaphone with three simple sound strokes, (2) a mouse pointer next to one coin, (3) a blank calendar embraced by a curved repeat arrow, (4) a small generic electric taxi silhouette with a protective shield. Each symbol centered in its own equal quarter with clear margins; no overlap between quarters. Thin uneven navy fineliner, flat streaky cyan and yellow marker, pencil hatch, student-drawn appearance, few details, no realistic shading or glossy 3D. NO words, lettering, numbers, digits, logos, brands, checkmarks, charts, gauge readings or claimed results. Calendar blank, coin blank, car unbranded. These are neutral icons for four objective zones; all exact metrics and labels will be added independently through controlled vector layout. No full poster. Wide horizontal composition.

## Actual generated asset and assembly

Tool: built-in `image_gen.imagegen`, one brand-new generation without references, `transparent_background=false`. Original output: `/Users/KHOILQ/.codex/generated_images/01a10028-2e2f-7a92-8df7-45fa2e0976f8/exec-2f85b4d2-8bdd-4d12-b334-f6d462217eed.png`. [Local art](08-v02-art.png) is a byte-unchanged copy, 2172 × 724. Its SHA256 is recorded in [the manifest](08-v02-manifest.json). Original file retained.

The actual strip was inspected: megaphone, pointer/coin, blank calendar/repeat arrow and generic taxi/shield; no letters, digits, brand marks or results. SVG viewports isolate the icons without raster repainting. The calendar's **90 days** is controlled lettering added in the composition, not image-model output. The generic taxi is an objective cue, not an identified fleet model or evidence of performance.

## Charts and exact text

All words/numbers use native MarkerFelt/Noteworthy glyph paths; no ordinary font fallback. Arrow symbols are controlled pen vectors. Exact eleven-measure source fields remain in [copy](08-v02-copy.md) and [the visible encoding map](08-v02-display-map.json).

- Awareness shows a +10 percentage-point delta from M1–2 to M12 without an invented baseline level.
- Search 3% and social 1.5% bars share a zero baseline and scale, with exact 2:1 lengths. They show proposed conversion targets.
- Repeat is a first-paid-trip → full-90-day-window → ≥35% paid-repeat flow, not an achieved-return chart.
- Four unfilled percentage gauges have target markers at 95, 2, 90 and 80, with correct minimum/maximum operators. No observed value or progress fill is supplied. The 0–100% annotation is the chart scale, not an industry benchmark.
- Spend control is a committed-plus-spent → approved-stage-total constraint, with no invented spending amounts.

Tracking tool and review rhythm appear beside each measure, using the global key. Gates/counting/M12 remain controlled text. Sources/evidence remain internal and inherited from v01; no source registry or shared controls changed.

## Reproduction

Run `python3 -B poster/08-v02-render.py`, then `python3 -B poster/08-v02-check.py` after a change. New SVG/PNG, manifest, layout/visual helpers, glyph source, art and encoding map are under `poster/`. The renderer reads the immutable v01 manifest as its baseline and reuses installed macOS fonts and the existing SVG renderer. No dependencies/caches are installed in iCloud. v01 bytes are protected by the recorded history hashes.
