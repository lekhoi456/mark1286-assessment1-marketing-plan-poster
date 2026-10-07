# Panel 3 — executed hand-drawn revision prompts

Date: 3 October 2026. Production prefix: `panel-03-production-v02-2026-10-03`.

## Native image generation

Tool: built-in `image_gen.imagegen`; no CLI or direct API generation. The Oura reference was viewed before use. It supplies drawing style only.

Reference: `/var/folders/j7/k3hwp19s0614s73_m5cj2hn80000gn/T/codex-clipboard-18eec81c-4572-4828-868e-e1f10d3009a6.png`.

Arguments: `referenced_image_paths` contains that single reference; `transparent_background: true`.

Exact executed prompt:

> Use case: illustration-story. Asset type: text-free decorative drawing sheet for one assessed marketing-plan poster section. The attached Oura poster is a STYLE REFERENCE ONLY: copy its simple student-drawn fineliner and flat marker language, never any text, figures, product or collage. Create a NEW sheet with a genuinely transparent background, ten isolated drawing islands and generous clear gutters, landscape. Make the CENTRAL island a simple upright blank phone rectangle with a lightly turquoise-markered electric MPV taxi in simple SIDE VIEW overlapping its lower edge. The car should be drawable by a student in a few outlines: imperfect thin navy pen silhouette, simple windows, plain dark circular wheels, no detailed hubs, no perspective rendering, one tiny yellow lightning mark, blank taxi roof sign. The phone has one thin irregular outline, blank pale screen and no glossy bezel, reflections or UI. Central island moderately bigger than others, not an enormous polished hero. At lower left and lower right, two smaller identical neutral grey outlined blank-phone plus plain taxi islands; no brand logos, no rankings and no negative symbols. At upper left place three separate simple redrawable pictograms: service-area outline with yellow location pin, unnumbered analogue clock, fare receipt with three plain pen strokes and a light yellow marker stroke. At upper right place a blank trip-reference ticket and a simple headset. At bottom centre place two tiny side-view cyan fleet cars as one island and a simple neutral driver bust as another island, made of a handful of pen lines with a pale cyan shirt; no anime, game character, dense hair shading or uniform badge. Use ordinary 0.3 mm navy fineliner, intentionally slight wobble, a few doubled pen contours, flat visible translucent marker strokes with little unfilled gaps. Warm white highlights, light cyan/turquoise and light yellow. No digital gradients, shadow ovals, 3D, glossy surfaces, thick cartoon contours, dense coloured-pencil shading, rendered reflections, complex wheels, fake grunge or heavy paper noise. NO WORDS, LETTERS, DIGITS, CURRENCY MARKS, LOGOS, labels, handwriting-like marks, watermark, arrows or chart. All phone screens and signs entirely blank. Exact handwriting-font text and real logo will be added by a layout tool. Keep all drawing islands separated and away from edges, on true alpha transparency.

Original returned file: `/Users/KHOILQ/.codex/generated_images/01a10052-be76-7750-8e04-af9a43fd23fe/exec-4f42ef49-befd-4bcb-83cc-49d2a755ffa3.png`.

Preserved byte-for-byte as [initial generated sheet](panel-03-production-v02-2026-10-03-generated-art-initial.png).

## Targeted native edit

The initial local sheet was viewed before editing. Its small rival-context cars still used cyan, so a second native call requested neutral grey.

Arguments: `referenced_image_paths` contains `panel-03-production-v02-2026-10-03-generated-art-initial.png`; `transparent_background: true`.

Exact executed edit prompt:

> Edit this drawing sheet with ONE targeted change: recolour only the two small taxi cars paired with phones at the bottom left and bottom right from cyan to a very pale neutral GREY marker fill, with a few visible marker strokes and unfilled gaps. Keep their yellow headlamps as small accents. Keep the large central cyan side-view taxi, central phone, other icons, fleet cars and driver exactly as they are. Keep all pen outlines, coordinates, island gutters, thin fineliner/flat-marker style and true transparent background. The two small cars are neutral comparator contexts, so no cyan brand colour or lightning symbols on them. Add no text, numbers, letters or logos. Preserve all blank phone screens and signs. No gradients, glossy shading or new objects.

Original returned file: `/Users/KHOILQ/.codex/generated_images/01a10052-be76-7750-8e04-af9a43fd23fe/exec-e65a175d-f9ff-40aa-a6bb-d9849c53b6b4.png`.

Preserved byte-for-byte as [final generated sheet](panel-03-production-v02-2026-10-03-generated-art.png). Both originals are retained; the layout does not alter their raster bytes.

## Controlled lettering and composition

[Complete SVG](panel-03-production-v02-2026-10-03.svg), [PNG](panel-03-production-v02-2026-10-03.png) and [placement manifest](panel-03-production-v02-2026-10-03-text-manifest.json) retain the exact approved content. The original logo is embedded unchanged. All other visible lettering uses glyph outlines from explicit local Marker Felt Thin and Noteworthy Light files, including the full positioning sentence and citation. No computer-sans fallback or font binary is distributed.

The approved B composition remains: a dominant central Green SM app/electric taxi, smaller neutral Uber and Bolt context, attached Clear terms and Local care pictograms, compact factual operating-model comparison, and labelled Delivery plan. The phone, vehicles and pictograms are conceptual illustrations.

Each isolated drawing has an explicit clip rectangle in source coordinates. Custom focal/receipt clips remove neighbouring drawing fragments without editing the generated image. The footer canvas is 1800 × 1488 px, with clear lettering space above its bottom frame.

Hashes, exact-copy checks and inspection limits are recorded in [focused checks](panel-03-production-v02-2026-10-03-checks.json) and [revision handoff](../reviews/panel-03-hand-drawn-revision-2026-10-03.md).

