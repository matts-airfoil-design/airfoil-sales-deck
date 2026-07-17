# Airfoil Sales Deck

This project synchronizes Figma slide designs with Webflow Reveal-style slide decks.

- For any deck change — replacing, adding, removing, reordering slides or groups, updating navigation links/descriptions, or publishing — use the `sync-figma-webflow-slide-decks` skill in `.claude/skills/sync-figma-webflow-slide-decks/`.
- The Figma MCP connector is the design source of truth; the Webflow MCP connector is the only write path to the site. Do not edit the deck through browser automation.
- Deck manifests live in `manifests/`. Validate a manifest before and after editing it:
  `python3 .claude/skills/sync-figma-webflow-slide-decks/scripts/validate_deck_manifest.py manifests/<manifest>.json`
- Never publish to production unless explicitly requested; an update request without a publish instruction leaves changes unpublished.
