# Panel 3 v05 — native artwork and provenance

Date: 3 October 2026. Authority: selected master v03 / D-072.

## Executed native call

Tool: built-in `image_gen.imagegen`. One new generation call; no CLI/API fallback or model change.

The existing sheet was inspected before use. Its role was a **style reference**, not an edit target.

Reference: `panel-03-production-v02-2026-10-03-generated-art.png`.
Arguments: `referenced_image_paths` contains that local file; `transparent_background: true`.

Exact executed prompt:

> Use case: illustration-story. Asset type: text-free transparent decorative drawing sheet for an assessed student marketing-plan infographic. Input image is a STYLE REFERENCE ONLY: use its navy fineliner and flat cyan/yellow marker language, do not reproduce its app/car sheet, dark display background or any existing objects. Primary request: draw exactly THREE small isolated pictogram scenes in one landscape row, with generous transparent gutters. Left scene: simple generic driver training, one instructor and one trainee beside a small plain steering wheel and an open blank manual, composed from a few imperfect pen lines; no uniforms, badges, country indicators or actual identified people. Centre scene: operational standards, a simple clipboard with three clear checkmarks and plain horizontal strokes, slight yellow marker highlight, no words or digits. Right scene: customer-service procedures, a simple friendly generic headset-wearing support person with a small blank trip ticket and a tiny empty speech bubble; no app UI or text. These are corporate approach illustrations, not evidence of a Copenhagen training class or service result. Style/medium: genuinely student-drawn 0.3 mm navy pen with slight natural wobble, light flat translucent marker strokes with visible direction and unfilled gaps, minimal features, simple outlines that a person could redraw. Palette: navy ink, restrained pale cyan and yellow, warm white highlights; preserve true alpha transparency. Each scene a compact pictogram with no large backdrop or surrounding frame. No text, letters, numbers, logos, watermarks, stars, rating scores, flags, gradients, dark fog, glow, drop shadows, glossy render, 3D, dense anime shading or photoreal faces. Do not draw connectors; exact labels and hand-drawn arrows will be added by a controlled layout tool. Keep each of the three pictograms safely isolated, fully inside the image, with clear gutters and generous outer margins.

Original returned file:
`/Users/KHOILQ/.codex/generated_images/01a10052-be76-7750-8e04-af9a43fd23fe/exec-67e6a9c2-67da-4aa2-a0f1-a4d4d2571acc.png`.

Preserved byte-for-byte in [project artwork](panel-03-production-v05-2026-10-03-generated-art.png). Size: **1942 × 809 px**, RGBA, alpha extrema **0–255**. SHA-256: `8f102d041e020e7861c4f5d59eb0fc24d10b98b6f1bc369294ec98308330c122`.

The returned sheet was inspected: generic training, standards checklist and support-procedure scenes; no observed letters, digits, logos or rating symbols. Checkmarks are symbolic procedure marks rather than performance data. The parent also inspected and accepted this sheet for composition; student acceptance of the completed section remains separate.

## Composition use

[Render source](panel-03-production-v05-2026-10-03-render.py) embeds the complete unchanged sheet and displays each illustration through an explicit source-coordinate clip rectangle. Reading alpha bounds informed viewport selection; no raster pixels were painted, edited or removed.

The existing app/EV, benefit icons and neutral rival artwork are reused unchanged from v02 and scaled down in SVG. The official panel-1 logo remains unchanged. Loose pen frames, connectors and a modest EV/noise cue are layout-native SVG extensions.

All words use explicit Marker Felt Thin / Noteworthy Light glyph outlines. The selected positioning sentence is preserved as four exact labelled segments; all labels and the bounded EV caption come from master v03. Sources/citations remain internal.

See [manifest](panel-03-production-v05-2026-10-03-text-manifest.json), [fidelity checks](panel-03-production-v05-2026-10-03-checks.json) and [production review](../reviews/panel-03-about-inspired-production-review-2026-10-03.md).

