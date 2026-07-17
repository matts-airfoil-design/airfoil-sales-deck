# Airfoil Sales Deck

This project synchronizes Figma slide designs with Webflow Reveal-style slide decks.

- For any deck change — replacing, adding, removing, reordering slides or groups, updating navigation links/descriptions, or publishing — use the `sync-figma-webflow-slide-decks` skill in `.claude/skills/sync-figma-webflow-slide-decks/`.
- The Figma MCP connector is the design source of truth; the Webflow MCP connector is the only write path to the site. Do not edit the deck through browser automation.
- Deck manifests live in `manifests/`. Validate a manifest before and after editing it:
  `python3 .claude/skills/sync-figma-webflow-slide-decks/scripts/validate_deck_manifest.py manifests/<manifest>.json`
- Never publish to production unless explicitly requested; an update request without a publish instruction leaves changes unpublished.
- Read `docs/site-architecture.md` for the site's page/component/asset structure before starting a sync. It is orientation only — refresh all IDs from live MCP reads before writing.

## Remote-environment network notes (Claude Code on the web)

Verified in practice; re-test before assuming they changed:

- Egress **blocks** raw downloads from `figma.com` and `cdn.prod.website-files.com` (curl gets CONNECT 403 from the proxy). The Figma MCP tools themselves work fine.
- Egress **allows** `s3.amazonaws.com`, so Webflow asset bytes are verifiable via each asset's `hostedUrl`.
- Working asset pipeline: get a fresh Figma export URL (`download_assets`, 2x PNG — URLs are short-lived, use immediately), then have Webflow fetch it server-side with `asset_tool > upload_image_by_url`. That tool is Designer-scoped: the user must open the Webflow Designer via the MCP bridge launch link (the tool's error message provides it — share it with the user and ask them to click). Then verify dimensions/bytes from the S3 `hostedUrl`, compress natively, and repoint the element.
- Do not try to route around blocked hosts; if a needed host is blocked, ask the user to either open the Designer bridge or allow the host in the environment's network policy.
