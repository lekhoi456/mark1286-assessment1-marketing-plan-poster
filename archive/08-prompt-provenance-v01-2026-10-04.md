# Section 8 decorative art prompt and provenance

Session date: 4 October 2026. Scope: a small neutral tracking illustration for the header of **8. Success Dashboard**. This is a delegated candidate, not group approval.

## Executed native prompt

Use case: illustration-story. Asset type: a small decorative header sketch for a student hand-drawn marketing success dashboard. Create one sparse wide horizontal illustration on warm cream paper (#fffdf5): a small blank clipboard with an entirely empty sheet, a modest navy pen, a magnifying glass and a simple analogue clock. Arrange objects in a shallow 3:1 horizontal cluster with ample clear margin. Thin slightly uneven navy fineliner contours, flat streaky cyan and yellow marker strokes, coloured-pencil texture, very few details. Match student hand-drawn infographic style, not glossy/cartoon 3D or clean vector. The clipboard and paper must be blank: NO lettering, NO words, NO numbers, NO logos, NO digits on the clock, NO ticked checkboxes, NO metric charts/bars, NO invented readings or results, NO watermark. This art is a neutral tracking cue; all exact dashboard text and targets will be added independently in controlled layout. No whole poster, car, people or extra objects. Wide composition; cream paper background.

## Actual result and controlled assembly

Tool: built-in `image_gen.imagegen`; one new generation without reference arguments. `transparent_background=false`. Native result: `/Users/KHOILQ/.codex/generated_images/01a10028-2e2f-7a92-8df7-45fa2e0976f8/exec-d2a8afe3-ff7c-491b-b6aa-f7678406ce74.png`. Original result remains in place. [Workspace artwork](08-candidate-v01-2026-10-04-generated-art.png) is copied byte unchanged and embedded in the self-contained SVG.

The raw artwork was visually inspected. It contains a blank clipboard, pen, magnifying glass and unnumbered clock; no poster lettering, logo, KPI values, table cells or claimed achievement. Placement: x=1450, y=68, width=645, height=215, above the metric zones. It is decorative, not a measured time or performance display. Raw image hash and placement are recorded in [the manifest](08-candidate-v01-2026-10-04-manifest.json).

All final lettering and numbers use controlled CoreText glyph paths from local MarkerFelt and Noteworthy files. Exact fields come from the eleven-row selected baseline, with tool and rhythm beside each metric. Four objective zones, separate spend control, counting rules, gates and M12 review are composed in editable SVG. The right-arrow symbol uses a small controlled pen-shaped vector so no alternate ordinary font is introduced. No model lettering, source-file repainting, generic brand mark or visible citation is used.

## Reproduction

From the workspace, run `python3 -B poster/08-candidate-v01-2026-10-04-render.py`. The renderer reads the local copy and generated art, uses its section-specific layout helper and Swift glyph source, then exports the SVG, full PNG, small PNG and manifest. It requires the existing macOS CoreText fonts and `/opt/homebrew/bin/rsvg-convert`, without installing dependencies or creating caches in iCloud. Re-run `python3 -B poster/08-candidate-v01-2026-10-04-check.py` after any composition change. Internal source/provenance additions are documented in the focused review; the shared source apparatus is not edited.

No other panel, historical asset, README, HANDOFF or project control is changed.
