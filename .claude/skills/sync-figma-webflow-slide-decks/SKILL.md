---
name: sync-figma-webflow-slide-decks
description: Synchronize Figma slide designs with Webflow Reveal-style slide decks by detecting changed, added, removed, or reordered frames; exporting 2x PNG sources; optimizing and uploading WebP assets; maintaining reusable slide-group components; aligning cover and dropdown navigation; and publishing to staging or production. Use when a request involves replacing slides, adding or removing slides or groups, reusing an identical group across decks, reordering a deck, updating company links or descriptions, or publishing Figma-driven Webflow slide changes.
---

# Sync Figma to Webflow Slide Decks

Treat the deck as synchronized state across Figma frames, Webflow assets, slide groups, reusable components, navigation, and publishing targets.

## Establish the target

1. Confirm the Figma file and node from the supplied link.
2. Discover the Webflow site, page, and deck component at runtime. Never rely on IDs from a previous run or from the repository containing this skill.
3. Confirm the Webflow site by name, site ID, Webflow subdomain, and custom domains before any write.
4. Distinguish public wrapper pages from internal slide pages. Modify the component that actually owns the slides.
5. Determine whether the requested endpoint is unpublished changes, staging, or production.
6. Read [references/deck-contract.md](references/deck-contract.md) before adding, removing, reusing, or reordering slide groups.
7. Read [references/mcp-reliability.md](references/mcp-reliability.md) when authentication, asset processing, element movement, publishing, rate limits, or server errors are involved.

## Inspect Figma and detect changes

1. Use the Figma MCP as the design source of truth. If the user explicitly requests Figma MCP only, do not use browser automation for the source.
2. Prefer a link to the exact changed frame. If the link targets a strip, section, or page, read its metadata and order slide frames by canvas position.
3. Compare the current Figma inventory with the current Webflow group or a saved manifest:
   - compare ordered node IDs for additions, removals, and reordering;
   - compare render hashes for visual changes whose node IDs remain stable;
   - treat file-level versions only as a signal that something changed.
4. Use metadata plus a screenshot or export when full design context is too large.
5. If Figma access fails, identify the authenticated account and request access or a user-exported 2x PNG. Do not silently substitute another source.

For recurring decks, read [references/manifest.md](references/manifest.md) and validate the manifest before and after editing.

## Export and optimize assets

1. Export each changed frame as a true 2x PNG. For a 1920x1080 source frame, verify a 3840x2160 export.
2. Verify dimensions and visually confirm the exported frame before uploading it.
3. Create and upload a new PNG asset in the correct Webflow asset folder.
4. Run Webflow's native WebP optimization and poll the task to completion.
5. Keep the native WebP only when processing succeeds and its byte size is smaller than the PNG.
6. If native optimization fails or produces no reduction:
   - delete only the newly uploaded, unreferenced PNG asset;
   - convert the source locally to WebP;
   - verify dimensions, visual integrity, and a smaller byte size;
   - upload the local WebP.
7. Preserve the previously referenced live asset unless cleanup is explicitly requested.
8. Use concise, descriptive alt text for every inserted or replaced image.

## Update the Webflow deck

1. Re-read the current component tree immediately before writing. External state may have changed since the prior call.
2. For a visual replacement, repoint the exact image element to the new asset.
3. For a new slide within an existing group, create a `deck_slide` containing a `deck_slide-image` and insert it at the intended vertical position.
4. For a new top-level group, create a separate `deck_group`. Do not merge semantically distinct groups.
5. When the exact same complete group appears in multiple decks, create one reusable Webflow component and insert instances in each deck. Do not componentize merely similar groups.
6. Preserve all unrelated slide and group ordering.
7. After any failed or interrupted write, re-read the tree before retrying. Never assume an error means no mutation occurred.

## Synchronize navigation

1. Build the final ordered list of top-level groups after all structural changes.
2. Count the cover as group 1. Derive each navigable destination from its actual horizontal group position as `#/N/1`.
3. Exclude cover and end-screen groups from company navigation unless the existing deck contract says otherwise.
4. Make both navigation surfaces exactly match the final group order:
   - the cover overlay built from `deck_link` instances;
   - `.deck_dropdown-menu-content` built from `deck_dropdown-link` instances.
5. Keep label, href, and dropdown description associated with the same group.
6. When adding a company, research its current offering using primary or official sources and write a short factual description. Do not infer a description from the company name or slide artwork alone.
7. Set Webflow link properties using `type: "link"`, `link_mode: "url"`, and `link_to: "#/N/1"`. Do not use a nested `link_value` object.
8. If moving navigation component instances fails, build replacement instances in final order, populate and verify them, then remove the old instances. For a simple adjacent swap between identical link components, swapping their values is acceptable.

## Verify before publishing

Verify all of the following from fresh Webflow reads:

- site, page, and component identity;
- slide and group counts;
- final top-level group order;
- reusable component instances and absence of duplicates;
- asset IDs, WebP format, dimensions, and alt text;
- cover-link order, labels, and destinations;
- dropdown order, labels, descriptions, and destinations;
- every destination equals the actual group position.

Use `scripts/validate_deck_manifest.py` when a manifest is available. Resolve the script path relative to this skill folder; do not assume the current working directory contains the skill.

## Publish

1. Inspect the complete unpublished site scope because Webflow publishing is site-wide and may include unrelated page changes.
2. Follow any available safe-publish policy. When the target is already explicit, avoid unrelated questions or ceremony.
3. Publish staging to the `*.webflow.io` subdomain only.
4. Publish production to the requested custom domain only, using Webflow's custom-domain ID rather than its hostname when required by the API.
5. Verify the target's publish timestamp and request the published URL over HTTP.
6. Report the target, included changes, timestamp, and verification result.

Do not publish to production by implication. A request to update a deck without a publish instruction leaves the changes unpublished.
