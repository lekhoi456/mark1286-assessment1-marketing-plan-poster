# Panel 1 production v14: hand-drawn Green SM lockup

Date: 3 October 2026. Authority: the student's explicit hand-drawn Green SM request, relayed by the controller. Baseline: D-068 accepted production v13. This is a logo-only revision; every other selected object and ordinary display string remains unchanged.

[Full PNG](panel-01-production-v14-2026-10-03.png), 2400 × 1680. [Header crop](panel-01-production-v14-2026-10-03-header-crop.png), 2235 × 248. [Small logo proof](panel-01-production-v14-2026-10-03-logo-proof.png), 920 × 276. [Editable self-contained SVG](panel-01-production-v14-2026-10-03.svg).

## Exact selected display copy

Print **1. Meet** with the shared hand-drawn Green SM mark and GREEN SM wordmark. The Vingroup emblem, calendar, country details and full middle-door VinFast identity retain their existing treatment.

<!-- display-copy:start -->
## Company/Business Introduction
<!-- budget: 110 -->

**1. Meet Green SM**

**Vingroup-backed**

**Founded March 2023**

Vietnam · Laos · Indonesia · Philippines · India · Kazakhstan · Denmark · Netherlands<sup>pilot</sup>

**14/04/2023**

**30/07/2026**

**Green SM Car: app-booked electric taxi rides in Copenhagen**

**Owned fleet · Employed drivers**
<!-- display-copy:end -->

## Asset, preservation and internal sources

The single actual Green SM lockup is replaced with [the shared PNG](green-sm-hand-drawn-logo-v01-2026-10-03.png), copied byte unchanged into [this package](panel-01-production-v14-2026-10-03-green-sm-logo.png) and embedded in the SVG. SHA256: `36a99749e3cc9585573fedda5fb1dbcf6a76483872cadc2d0f6651ec95430db9`. The complete PNG is 2171 × 724 with transparent alpha. A viewport over its non-transparent bounds, `18 72 2125 572`, omits only empty padding; the complete asset bytes, colours and alpha remain unchanged. The original placement box, x=355, y=49, width=433.5, height=117.3, is retained, with proportional centred fitting.

This is the selected hand-drawn reinterpretation, rather than the original clean PDF paths. The prior authentic-logo extraction/source record is retained as history in the [manifest](panel-01-production-v14-2026-10-03-manifest.json). All factual source records, evidence/date/pilot qualifications, sixteen ordinary text records, eight flags and their details, raw car artwork, full hand-drawn VinFast identity, Vingroup emblem and calendar remain identical to v13. No visible citation or new wording is added. No new image generation or raster repainting was needed.

## Reproduction and focused checks

Run from the workspace:

```sh
python3 -B 07_drafts/design/panel-01-production-v14-2026-10-03-compose.py
/opt/homebrew/bin/rsvg-convert -w 2400 -h 1680 -o 07_drafts/design/panel-01-production-v14-2026-10-03.png 07_drafts/design/panel-01-production-v14-2026-10-03.svg
/opt/homebrew/bin/rsvg-convert -o 07_drafts/design/panel-01-production-v14-2026-10-03-header-crop.png 07_drafts/design/panel-01-production-v14-2026-10-03-header-crop.svg
/opt/homebrew/bin/rsvg-convert -o 07_drafts/design/panel-01-production-v14-2026-10-03-logo-proof.png 07_drafts/design/panel-01-production-v14-2026-10-03-logo-proof.svg
```

[Focused checks](panel-01-production-v14-2026-10-03-checks.json): 18 passed, zero failed. All non-logo SVG objects match v13, apart from intentional non-visual description metadata. The full-PNG difference is confined to the logo region: 48,788 changed pixels, bounds x=532, y=74, width=651, height=175. The original embedded asset hash and transparent alpha are retained. Actual full PNG and close proof were inspected: GREEN SM remains legible, texture is visible, and no overlap or clipping was observed.

[Focused report](../reviews/panel-01-handdrawn-green-sm-logo-revision-2026-10-03.md). Confidence: high for exact preservation and inspected screen placement. Student feedback on this new logo treatment and physical A0 proof remain pending. Historical versions and shared controls are untouched; the dedicated agent remains available.
