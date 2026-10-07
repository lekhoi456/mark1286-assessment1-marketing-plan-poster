# Section 6 candidate v02 — art prompt and provenance

Prepared 4 October 2026. V02 reuses the v01 transparent PNG byte-identically; no new image generation or edit was made for this copy-only revision. The exact original generation and edit prompts are reproduced below for traceability. The image model supplied pictograms only. All visible poster words, headings, arrows, cards and layout were added locally in the editable SVG. No Green SM logo is used.

Tool: built-in `image_gen.imagegen`.

References: `poster/01-approved.png`, `poster/02-approved.png` and `poster/03-approved.png` as primary style guides; `poster/04-candidate-v01-2026-10-04.png` as a secondary style reference.

Output: `poster/06-v02-generated-art.png`, 2172 × 724 RGBA PNG; transparent alpha is preserved. It is an exact copy of `poster/06-candidate-v01-2026-10-04-generated-art.png`. The SVG embeds this PNG as one full-width pictogram ribbon above the five text cards. Its viewport trims transparent margins only and includes the full non-transparent art bounds with padding; no pictogram is cropped individually.

Saved-art SHA-256: `38106e757636cf5cda6ede2da93d32eca3d3cee4c689705094d73d0293e64eed`.

## Exact prompt

```text
Use case: standalone pictogram sheet for a proposed Copenhagen taxi sales-process infographic, section 6. Make five separate hand-drawn illustrations in one horizontal row, each centred in its own equal-width cell with generous transparent gutters and no connecting arrows.

The five illustrations, left to right:
1) A magnifying glass beside a plain local information page and a generic blank-screen smartphone, suggesting search and information.
2) A simple person beside a closed envelope with one small check mark, suggesting a consented follow-up.
3) A modest cyan electric taxi in side view beside a blank receipt and one yellow-gold coin, suggesting a completed paid ride; no badge, brand mark or taxi sign.
4) A blank trip-reference slip beside a friendly human support agent wearing a headset; include a separate small plain help card, not a booking card.
5) A simple calendar with a circular return arrow beside a generic blank-screen phone, suggesting a consented repeat reminder.

Style references: use the warm-paper, navy-outline, cyan and yellow-gold hand-marker and pencil style of reference panels 1–3 as the primary style guide. The separate section-4 candidate is only a secondary reference. Friendly student-marketing-poster drawing; loose but clean outlines, lightly hatched flat fills, no visual clutter. Palette: navy #173a47, cyan #26c6cf, yellow-gold #ffd400 and warm ivory #fffdf5 only inside blank paper/card surfaces.

The sheet itself must have genuine transparent alpha, no background, no border, no labels, no panels or frames. Each pictogram must be isolated and fully visible within its own fifth of the canvas. Leave generous clear space around every object. This is illustration only; a local layout tool will add all exact copy and arrows later.

Absolutely no words, letters, numerals, pseudo-text, logos, flags, branded app interface, readable screens, price amounts, watermarks or rendered text. Do not depict current service coverage, live app functions or performance results. Avoid photorealism, 3D, glossy effects, gradients, glow, checkerboards and background shadows.
```

## Exact image-edit prompt used for the saved sheet

The edit used the generated seed sheet plus the four poster references listed above.

```text
Edit and recompose the supplied transparent pictogram sheet for a proposed Copenhagen taxi sales-process infographic. Keep the five concepts and the hand-marker/pencil drawing style, but separate the five picture groups cleanly for later local layout.

Layout is the critical edit: make five equal-width vertical cells across the full wide canvas, with icon centres at 10%, 30%, 50%, 70% and 90% of the canvas width. Keep each complete icon group inside its own cell and no wider than 15% of the full canvas. Leave a wide, fully transparent vertical gutter at every 20% cell boundary. No line, colour, object or shadow may cross a cell boundary. Do not let any group touch or overlap its neighbours. Keep the canvas wide and short, like the supplied sheet.

Keep these five concepts in order:
1) Magnifying glass, plain local information page and blank-screen phone.
2) Person with a closed envelope and one small check mark.
3) Modest cyan electric taxi with blank receipt and one yellow-gold coin.
4) Friendly human support agent with headset, blank trip-reference slip and separate plain help card.
5) Simple calendar with circular return arrow and blank-screen phone.

Use the three accepted poster panels as the primary style reference: warm ivory paper surfaces, dark navy outlines, cyan and yellow-gold marker/pencil strokes, friendly student-made infographic look. The section-4 candidate remains only a secondary style reference. Preserve genuine transparent alpha; do not add background, cells, frames, borders or arrows.

No words, letters, numerals, pseudo-text, logos, flags, app branding, readable UI, service-area depiction, price amount, performance result or watermark. Do not change the concepts into a live product interface. Avoid photorealism, 3D, gradients, glow and background shadows.
```
