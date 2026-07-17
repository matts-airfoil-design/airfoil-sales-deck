#!/usr/bin/env python3
"""Validate and derive navigation from a portable slide-deck manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


VALID_KINDS = {"cover", "content", "end"}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_manifest(data: Any) -> tuple[list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    navigation: list[dict[str, Any]] = []

    if not isinstance(data, dict):
        return ["manifest must be a JSON object"], navigation

    figma = data.get("figma")
    if not isinstance(figma, dict):
        errors.append("figma must be an object")
    elif not _nonempty_string(figma.get("file_key")):
        errors.append("figma.file_key must be a non-empty string")

    webflow = data.get("webflow")
    if not isinstance(webflow, dict):
        errors.append("webflow must be an object")
    else:
        for field in ("site_id", "page_id", "deck_component_id"):
            if not _nonempty_string(webflow.get(field)):
                errors.append(f"webflow.{field} must be a non-empty string")

    groups = data.get("groups")
    if not isinstance(groups, list) or not groups:
        errors.append("groups must be a non-empty array")
        return errors, navigation

    seen_keys: set[str] = set()
    end_positions: list[int] = []

    for position, group in enumerate(groups, start=1):
        prefix = f"groups[{position - 1}]"
        if not isinstance(group, dict):
            errors.append(f"{prefix} must be an object")
            continue

        key = group.get("key")
        if not _nonempty_string(key):
            errors.append(f"{prefix}.key must be a non-empty string")
        elif key in seen_keys:
            errors.append(f"{prefix}.key duplicates {key!r}")
        else:
            seen_keys.add(key)

        kind = group.get("kind")
        if kind not in VALID_KINDS:
            errors.append(
                f"{prefix}.kind must be one of {sorted(VALID_KINDS)}"
            )
            continue

        include = group.get("include_in_navigation")
        if not isinstance(include, bool):
            errors.append(f"{prefix}.include_in_navigation must be boolean")
            include = False

        if kind == "cover":
            if position != 1:
                errors.append(f"{prefix}: cover must be the first group")
            if include:
                errors.append(f"{prefix}: cover cannot be in navigation")

        if kind == "end":
            end_positions.append(position)
            if include:
                errors.append(f"{prefix}: end group cannot be in navigation")

        if include:
            expected_href = f"#/{position}/1"
            for field in ("label", "description", "href"):
                if not _nonempty_string(group.get(field)):
                    errors.append(f"{prefix}.{field} must be a non-empty string")
            if _nonempty_string(group.get("href")) and group["href"] != expected_href:
                errors.append(
                    f"{prefix}.href is {group['href']!r}; expected {expected_href!r}"
                )
            navigation.append(
                {
                    "key": key,
                    "group_index": position,
                    "label": group.get("label"),
                    "description": group.get("description"),
                    "href": expected_href,
                }
            )

    if groups and isinstance(groups[0], dict) and groups[0].get("kind") != "cover":
        errors.append("groups[0].kind must be 'cover'")

    if len(end_positions) > 1:
        errors.append("only one end group is allowed")
    elif end_positions and end_positions[0] != len(groups):
        errors.append("end group must be the last group")

    return errors, navigation


def _self_test() -> int:
    valid = {
        "figma": {"file_key": "file-key"},
        "webflow": {
            "site_id": "site-id",
            "page_id": "page-id",
            "deck_component_id": "component-id",
        },
        "groups": [
            {"key": "cover", "kind": "cover", "include_in_navigation": False},
            {
                "key": "project-a",
                "kind": "content",
                "label": "Project A",
                "description": "A factual description",
                "include_in_navigation": True,
                "href": "#/2/1",
            },
            {"key": "end", "kind": "end", "include_in_navigation": False},
        ],
    }
    errors, navigation = validate_manifest(valid)
    assert not errors, errors
    assert navigation == [
        {
            "key": "project-a",
            "group_index": 2,
            "label": "Project A",
            "description": "A factual description",
            "href": "#/2/1",
        }
    ]

    invalid = json.loads(json.dumps(valid))
    invalid["groups"][1]["href"] = "#/3/1"
    errors, _ = validate_manifest(invalid)
    assert any("expected '#/2/1'" in error for error in errors), errors
    print("self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a Figma-to-Webflow slide-deck manifest."
    )
    parser.add_argument("manifest", nargs="?", help="Path to a JSON manifest")
    parser.add_argument(
        "--emit-navigation",
        action="store_true",
        help="Print derived navigation JSON after validation",
    )
    parser.add_argument("--self-test", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.self_test:
        return _self_test()
    if not args.manifest:
        parser.error("manifest is required unless --self-test is used")

    path = Path(args.manifest)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: manifest not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {path}: {exc}", file=sys.stderr)
        return 2

    errors, navigation = validate_manifest(data)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    if args.emit_navigation:
        print(json.dumps(navigation, indent=2, ensure_ascii=False))
    else:
        print(
            f"manifest valid: {len(data['groups'])} groups, "
            f"{len(navigation)} navigation entries"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
