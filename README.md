# Airfoil Sales Deck

Project for keeping the Airfoil sales deck synchronized between Figma slide designs and the Webflow Reveal-style slide deck.

All deck work runs through the Claude Code skill in [`.claude/skills/sync-figma-webflow-slide-decks/`](.claude/skills/sync-figma-webflow-slide-decks/SKILL.md), which drives the Figma and Webflow MCP connectors.

## Requirements

Sessions in this project need two MCP connectors:

- **Figma** — design source of truth: reads frame metadata, detects changes, exports 2x PNG slides.
- **Webflow** — deck target: uploads/optimizes assets, edits the deck component tree, syncs navigation, publishes to staging or production.

Both are available as claude.ai connectors or MCP servers configured for Claude Code. Without them the skill cannot run.

## Layout

```text
.claude/skills/sync-figma-webflow-slide-decks/
├── SKILL.md                         # the skill: sync workflow end to end
├── references/
│   ├── deck-contract.md             # group boundaries, navigation invariant, component props
│   ├── manifest.md                  # manifest shape, rules, validation
│   └── mcp-reliability.md           # auth, retries, publishing, rate-limit handling
└── scripts/
    └── validate_deck_manifest.py    # manifest consistency validator
manifests/
└── deck-manifest.example.json       # template for a per-deck manifest
```

## Usage

Ask Claude Code to sync deck changes, e.g.:

> Replace the Project A slides with the updated frames in <figma link> and publish to staging.

The skill handles change detection, 2x export, WebP optimization, deck-tree edits, navigation sync, verification, and publishing. Production publishes only happen when explicitly requested.

## Manifests

Recurring decks keep a manifest in `manifests/` (copy the example to e.g. `manifests/deck-manifest.json`). Validate with:

```bash
python3 .claude/skills/sync-figma-webflow-slide-decks/scripts/validate_deck_manifest.py manifests/deck-manifest.json
python3 .claude/skills/sync-figma-webflow-slide-decks/scripts/validate_deck_manifest.py manifests/deck-manifest.json --emit-navigation
```

Validation is a consistency check only — the skill always re-reads live Webflow state before writing.
