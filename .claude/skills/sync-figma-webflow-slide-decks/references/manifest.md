# Deck manifest

Use a manifest for recurring decks or any change that adds, removes, or reorders top-level groups. Store the manifest with the user's project when possible; do not require this skill's repository.

## Shape

```json
{
  "figma": {
    "file_key": "<current-file-key>",
    "container_node_id": "<page-or-strip-node-id>",
    "version": "<optional-file-version>"
  },
  "webflow": {
    "site_id": "<current-site-id>",
    "page_id": "<internal-slide-page-id>",
    "deck_component_id": "<current-deck-component-id>"
  },
  "groups": [
    {
      "key": "cover",
      "kind": "cover",
      "include_in_navigation": false
    },
    {
      "key": "project-a",
      "kind": "content",
      "label": "Project A",
      "description": "Short factual product description",
      "include_in_navigation": true,
      "href": "#/2/1",
      "figma_node_ids": ["<frame-node-id>"],
      "render_hashes": ["<export-hash>"],
      "webflow_component_id": "<optional-shared-group-component-id>",
      "webflow_element_id": "<group-instance-or-section-id>",
      "webflow_asset_ids": ["<asset-id>"]
    },
    {
      "key": "end",
      "kind": "end",
      "include_in_navigation": false
    }
  ]
}
```

## Rules

- Refresh site, page, component, element, and asset IDs from current MCP reads before trusting them.
- Keep group keys unique and stable across runs.
- Preserve Figma node order within each group.
- Calculate `href` from the group's actual one-based position in `groups`, including cover and end groups.
- Require label, description, and href for every navigable group.
- Keep cover and end groups out of navigation.
- Reusing the same `webflow_component_id` is valid only for identical complete groups.
- Update render hashes after verifying the final 2x exports.

## Validation

Resolve the validator relative to the installed skill folder:

```bash
python3 <skill-folder>/scripts/validate_deck_manifest.py path/to/deck-manifest.json
python3 <skill-folder>/scripts/validate_deck_manifest.py path/to/deck-manifest.json --emit-navigation
```

The validator checks required identifiers, group kinds and ordering, unique keys, navigation fields, and every `#/N/1` destination. `--emit-navigation` prints the ordered cover/dropdown data derived from the manifest.

Treat validation as a consistency check, not proof that the external Webflow state still matches. Re-read Webflow after validation and before writing.
