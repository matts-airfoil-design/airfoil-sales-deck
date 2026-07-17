# MCP reliability

Read this reference when a task involves authentication, asset processing, element movement, publishing, rate limits, or server errors on the Figma or Webflow MCP servers.

## Authentication

- On any Figma or Webflow auth failure, identify the authenticated account first (`whoami` on Figma; site listing on Webflow) before concluding access is missing.
- If the Figma file is unreachable, request access for the authenticated account or ask the user for a 2x PNG export. Never silently substitute another source or a cached render.
- Do not retry an auth failure verbatim; the credential or grant must change first.

## Asset processing

- Webflow WebP optimization is asynchronous. Poll the processing task to a terminal state; never assume success from task creation.
- Accept the optimized WebP only when processing reports success and the byte size is smaller than the source PNG. Otherwise fall back to local conversion as described in the skill.
- After a failed upload or optimization, list assets before re-uploading — the asset may exist despite the error. Delete only newly created, unreferenced assets.
- Verify uploaded asset dimensions match the verified 2x export before referencing the asset from any element.

## Element movement

- Re-read the component tree immediately before any structural write; external state may have changed since the last read.
- After any failed or interrupted write, re-read the tree before retrying. Never assume an error means no mutation occurred — partial writes are common.
- If moving a component instance fails, use the replacement strategy from the deck contract: create new instances in final order, populate and verify them, then remove the old ones.
- Verify every mutation by reading back the saved value; link properties in particular may be accepted but stored incorrectly.

## Publishing

- Publishing is site-wide. Inspect the full unpublished scope before publishing so unrelated changes are not shipped unknowingly.
- Target staging (`*.webflow.io`) and production (custom domain) explicitly and separately. Use the custom-domain ID, not the hostname, where the API requires it.
- Confirm success from the publish timestamp and an HTTP request to the published URL, not from the API call returning without error.

## Rate limits and server errors

- On HTTP 429, honor `Retry-After` when present; otherwise back off exponentially (2s, 4s, 8s, 16s) with a maximum of 4 retries.
- Retry 5xx responses with the same backoff. Treat 4xx (other than 429) as a request problem: re-read state and fix the request instead of retrying.
- Rate-limit budgets are per server. Batch reads where the API allows it and avoid re-fetching unchanged design context.
- After exhausting retries, report the failing operation, the last error, and the verified current state — do not guess at what was applied.
