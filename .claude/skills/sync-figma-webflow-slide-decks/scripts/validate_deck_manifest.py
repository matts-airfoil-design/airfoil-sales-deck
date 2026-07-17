#!/usr/bin/env python3
"""Validate a deck manifest against the deck contract.

Checks required identifiers, group kinds and ordering, unique keys,
navigation fields, and every `#/N/1` destination. With --emit-navigation,
prints the ordered cover/dropdown data derived from the manifest.

Validation is a consistency check only; it does not prove that external
Figma or Webflow state still matches. Re-read Webflow after validation
and before writing.

Usage:
    python3 validate_deck_manifest.py path/to/deck-manifest.json
    python3 validate_deck_manifest.py path/to/deck-manifest.json --emit-navigation
"""

import argparse
import json
import sys

VALID_KINDS = {"cover", "content", "end"}

REQUIRED_FIGMA_FIELDS = ["file_key", "container_node_id"]
REQUIRED_WEBFLOW_FIELDS = ["site_id", "page_id", "deck_component_id"]


def _nonempty_str(value):
    return isinstance(value, str) and value.strip() != ""


def validate(manifest):
    errors = []
    warnings = []

    figma = manifest.get("figma")
    if not isinstance(figma, dict):
        errors.append("missing or invalid 'figma' object")
    else:
        for field in REQUIRED_FIGMA_FIELDS:
            if not _nonempty_str(figma.get(field)):
                errors.append(f"figma.{field} is required and must be a non-empty string")

    webflow = manifest.get("webflow")
    if not isinstance(webflow, dict):
        errors.append("missing or invalid 'webflow' object")
    else:
        for field in REQUIRED_WEBFLOW_FIELDS:
            if not _nonempty_str(webflow.get(field)):
                errors.append(f"webflow.{field} is required and must be a non-empty string")

    groups = manifest.get("groups")
    if not isinstance(groups, list) or not groups:
        errors.append("'groups' must be a non-empty list")
        return errors, warnings

    seen_keys = set()
    for position, group in enumerate(groups, start=1):
        label = f"groups[{position - 1}]"
        if not isinstance(group, dict):
            errors.append(f"{label} must be an object")
            continue

        key = group.get("key")
        if not _nonempty_str(key):
            errors.append(f"{label}: 'key' is required and must be a non-empty string")
        elif key in seen_keys:
            errors.append(f"{label}: duplicate group key '{key}'")
        else:
            seen_keys.add(key)
        name = key if _nonempty_str(key) else label

        kind = group.get("kind")
        if kind not in VALID_KINDS:
            errors.append(f"{name}: 'kind' must be one of {sorted(VALID_KINDS)}, got {kind!r}")
            continue

        if kind == "cover" and position != 1:
            errors.append(f"{name}: cover group must be first, found at position {position}")
        if kind == "end" and position != len(groups):
            errors.append(f"{name}: end group must be last, found at position {position}")

        include = group.get("include_in_navigation")
        if not isinstance(include, bool):
            errors.append(f"{name}: 'include_in_navigation' is required and must be a boolean")
            include = False

        if kind in ("cover", "end") and include:
            errors.append(f"{name}: {kind} groups must stay out of navigation")

        if include:
            for field in ("label", "description", "href"):
                if not _nonempty_str(group.get(field)):
                    errors.append(f"{name}: navigable group requires non-empty '{field}'")
            href = group.get("href")
            expected = f"#/{position}/1"
            if _nonempty_str(href) and href != expected:
                errors.append(
                    f"{name}: href {href!r} does not match actual position "
                    f"{position} (expected {expected!r})"
                )

        if kind == "content":
            node_ids = group.get("figma_node_ids")
            if not isinstance(node_ids, list) or not node_ids:
                warnings.append(f"{name}: content group has no 'figma_node_ids'")
            hashes = group.get("render_hashes")
            if isinstance(node_ids, list) and isinstance(hashes, list) and len(hashes) != len(node_ids):
                warnings.append(
                    f"{name}: 'render_hashes' count ({len(hashes)}) does not match "
                    f"'figma_node_ids' count ({len(node_ids)})"
                )

    kinds = [g.get("kind") for g in groups if isinstance(g, dict)]
    if kinds.count("cover") > 1:
        errors.append("more than one cover group")
    if kinds.count("end") > 1:
        errors.append("more than one end group")
    if "content" not in kinds:
        warnings.append("manifest contains no content groups")

    return errors, warnings


def emit_navigation(manifest):
    entries = []
    for position, group in enumerate(manifest.get("groups", []), start=1):
        if isinstance(group, dict) and group.get("include_in_navigation"):
            entries.append(
                {
                    "position": position,
                    "key": group.get("key"),
                    "label": group.get("label"),
                    "href": f"#/{position}/1",
                    "description": group.get("description"),
                }
            )
    print(json.dumps({"cover_links": entries, "dropdown_links": entries}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manifest", help="path to deck-manifest.json")
    parser.add_argument(
        "--emit-navigation",
        action="store_true",
        help="print ordered cover/dropdown navigation derived from the manifest",
    )
    args = parser.parse_args()

    try:
        with open(args.manifest, encoding="utf-8") as handle:
            manifest = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read manifest: {exc}", file=sys.stderr)
        return 1

    errors, warnings = validate(manifest)

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1

    if args.emit_navigation:
        emit_navigation(manifest)

    print(f"OK: {len(manifest.get('groups', []))} group(s), {len(warnings)} warning(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
