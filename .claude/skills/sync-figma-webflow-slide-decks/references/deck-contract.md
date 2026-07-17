# Deck contract

Read this reference whenever a task changes slide-group boundaries, ordering, reuse, navigation, or descriptions.

## Structural model

A typical deck contains:

```text
deck_content
├── toolbar
│   └── deck_dropdown-menu-content
├── cover deck_group
│   └── deck_slide
│       └── cover overlay navigation
├── content deck_group
│   ├── deck_slide
│   │   └── deck_slide-image
│   └── deck_slide
│       └── deck_slide-image
├── additional deck_group or component instances
└── end-screen deck_group
```

A `deck_group` is one horizontal Reveal destination. Its nested `deck_slide` elements are vertical slides within that destination.

Inspect the actual site before assuming these names. Preserve equivalent existing classes and element types when a deck uses different naming.

## Group boundaries and components

- Keep each independently navigable body of work as a separate top-level group.
- Do not merge groups because they share a company, subject, or visual style.
- Create a reusable component only when every slide, order, asset, overlay, and behavior in the complete group is identical across decks.
- Insert component instances rather than duplicate markup once an identical group is componentized.
- Re-read every destination deck after component creation to verify that the intended instances exist and old duplicate markup is gone.

## Navigation invariant

Treat the top-level group sequence as the source of truth.

For each group at one-based horizontal position `N`:

```text
destination = #/N/1
```

The cover usually occupies position 1, so the first navigable content group normally points to `#/2/1`. Cover and end-screen groups usually remain absent from navigation.

Maintain two ordered navigation projections:

1. Cover overlay: `deck_link` instances with Text and Link properties.
2. Dropdown menu: `deck_dropdown-link` instances with Text, Link, and Description properties.

After a group addition, deletion, or move, recalculate every destination at and after the changed position. Matching labels without matching order and destinations is invalid.

## Webflow component properties

Set string properties with the tool's explicit string wrapper. Set URL link properties using this shape:

```json
{
  "prop_id": "<link-property-id>",
  "type": "link",
  "link_mode": "url",
  "link_to": "#/4/1"
}
```

A nested `link_value` object may be accepted but lose its URL target. Always read the saved property after mutation.

## Description policy

When a new company or project enters the navigation:

1. Search the web for its current offering.
2. Prefer the official site, official documentation, or an official announcement.
3. Write one short, neutral description of the actual product or service.
4. Avoid marketing superlatives, unsupported claims, and wording inferred only from the deck.
5. Preserve existing descriptions for unaffected groups.

## Reordering fallbacks

Prefer a direct element move when the MCP supports the source and anchor relationship. If component-instance movement fails:

1. Read and retain every existing label, link, and description.
2. Create replacement navigation instances in final order.
3. Populate them with explicit typed property values.
4. Verify all new instances.
5. Remove the superseded instances.

For an adjacent undo involving identical navigation components, swap their complete property sets instead of moving the elements.
