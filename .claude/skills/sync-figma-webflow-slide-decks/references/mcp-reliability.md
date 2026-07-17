# MCP reliability and publishing

Read this reference when an MCP call fails, authentication changes, a write is interrupted, asset processing behaves unexpectedly, or a publish is requested.

## Figma reads

- Treat Figma MCP metadata, screenshots, and exports as current-state reads, not a design changelog.
- Do not expect per-node modification timestamps or semantic diffs.
- Use ordered node IDs to detect structural changes and render hashes to detect visual changes within stable nodes.
- Use file-level version or modified metadata only as a cheap signal that some part of the file changed.
- When a large vector node exceeds useful design-context limits, use metadata plus a screenshot or direct export.
- If authorization is wrong, report the authenticated identity and request access or a user-provided export. Do not switch to browser capture when the user required Figma MCP only.

## Webflow authorization and target identity

The Webflow MCP can perform supported asset, element, component, and publishing operations without an open Designer tab. A browser or Designer connection is only necessary for canvas-specific state that the API does not expose.

Authorization can expire or expose a different site after reauthentication. Before every write batch, confirm:

- site name and site ID;
- Webflow subdomain and custom domains;
- page ID and published path;
- component ID and current element tree.

Never modify a similarly named site by assumption.

## Partial writes and retries

A transport or internal error does not prove that Webflow rolled back the operation. Before retrying:

1. Re-read the affected component or asset.
2. Determine whether the write completed fully, partially, or not at all.
3. Remove duplicates or temporary elements left by a partial write.
4. Retry only the missing idempotent operations.

Avoid repeated blind move or create calls.

## Asset processing

Use Webflow's native WebP optimization first when the source is a PNG. Poll the returned task rather than assuming synchronous completion.

If optimization fails or the result is not smaller:

1. Confirm the new PNG is not referenced.
2. Delete that temporary new PNG asset only.
3. Convert the original source locally.
4. Verify the local WebP is visually correct, has the expected dimensions, and is smaller.
5. Upload the WebP and repoint the intended image.

Do not delete the old referenced asset as part of this fallback.

## Component authoring failures

Some Webflow relationships may reject direct insertion, conversion, or movement, especially around nested component definitions and component-instance anchors.

Use these fallbacks in order:

1. Insert through the nearest plain parent and then move relative to a plain section.
2. Create a standalone reusable component and insert instances by component name or current component ID.
3. Rebuild a short ordered list of component instances, verify it, then remove the old list.

If a previously created component is absent, inspect the current saved state before rebuilding it. Never assume an earlier component ID is still valid.

## Publishing

Webflow publishes a site scope, not a single element. Before publishing, inspect all unpublished pages and disclose unrelated changes included in the release.

- Staging: publish the Webflow subdomain only.
- Production: publish only the requested custom domain.
- Use custom-domain IDs when the API rejects hostnames.
- Verify the relevant site or domain timestamp after the request.
- Verify the published URL returns a successful HTTP response.

## Rate limits and server errors

For HTTP 429 or server errors:

1. Check [Webflow Status](https://status.webflow.com/).
2. Compare the incident's affected capability with the failed operation.
3. Attribute the failure to an outage only when they match.
4. Otherwise report the actual MCP/API error and continue with a safe retry or fallback.
