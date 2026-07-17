# Airfoil Slide Deck — site architecture notes

Orientation for deck-sync sessions, mapped from live MCP reads on 2026-07-17. Structure here is stable context; **all IDs must still be refreshed from live reads before any write**, per the skill.

## Sites and domains

One Webflow site: **"Airfoil Slide Deck"** (site ID at time of mapping: `69c551e56bb97cdb759254e1`).

- Staging: `airfoil-slide-deck.webflow.io`
- Production: `explore.airfoil.studio` (custom-domain ID at time of mapping: `69e64ae3b3223bdde92ece7d`)

## Page model

Two-layer structure — always edit the internal slide pages, not the wrappers:

| Public wrapper (SEO, iframe embed) | Internal slide page (owns the deck) |
|---|---|
| `/ai` ("AI Deck") | `/slides/ai` ("AI Slides") |
| `/web3` ("Web3 Deck") | `/slides/web3` ("Web3 Slides") |
| `/all` ("All projects Deck") | `/slides/all` ("All Slides") |

Wrappers use the "Deck Page Wrapper" component plus a per-deck "Deck iframes - *" component. Internal pages hold the actual slides through a **"Deck Slides Content"** component per deck: `AI`, `Web3`, `AI & Web3`.

## Component model

- **Slide Groups** (component folder): reusable per-company groups shared across decks — e.g. `Reducto` (2 instances), `Deck End Screen` (3 instances, shared final slide). A group is `deck_group` (horizontal Reveal destination) → `deck_slide` sections (vertical) → `deck_slide-image`, optionally plus a `deck_overlay` block containing a `<video>` DOM element (sources hosted at `cdn.airfoil.engineering`).
- **Utility**: `deck_link` (cover overlay nav) and `deck_dropdown-link` (dropdown nav), 36 instances each at time of mapping.

## Assets

- Folders by deck theme: `AI Projects`, `Web3 Projects`, `AI & Web3 Projects`.
- Slide files are named `<slide-number>-v<version>` (e.g. `3-v2.webp` → replaced by `3-v3`). Keep this convention: upload the new version, never overwrite or delete the previously referenced asset.
- Final format is WebP at 3840×2160 (2x of the 1920×1080 Figma frames), produced by Webflow's native compression (`compress_assets` → poll task). Compression replaces the uploaded PNG in place under the same asset ID.

## Figma source

- File: **Work Samples** (`jbzrH2KS0nMA4K8FwSbYIC`), slides as 1920×1080 frames named per company (e.g. `Reducto`), laid out horizontally on the canvas.
- Export at 2x PNG → verify 3840×2160 before upload.
