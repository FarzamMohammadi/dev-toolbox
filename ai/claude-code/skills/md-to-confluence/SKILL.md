---
name: md-to-confluence
description: Upload a Markdown (.md) file to a Confluence Cloud page with tables, headings, formatting, and mermaid diagrams all rendering correctly — no copy-paste, no wording changes. Use this whenever someone wants to publish, push, sync, or upload a markdown doc, spec, design, or README to Confluence, or complains that pasting markdown into Confluence breaks the tables or diagrams. Also trigger on "put this doc on Confluence", "get this on the wiki", "publish this to Confluence", or updating an existing Confluence page from a markdown source.
---

# Markdown → Confluence

Confluence Cloud does **not** store Markdown. Pasting `.md` source into the editor leaves tables as literal `| ... |` text and mermaid blocks as dead code fences. This skill converts the file to Confluence **storage format** (their XHTML dialect) and pushes it over the REST API, so tables, headings, lists, inline code, and diagrams all render — and **not a word of the content changes**.

Two bundled scripts do the work:
- `scripts/convert.py` — Markdown → storage-format XHTML. Pulls out mermaid blocks, adds an auto table-of-contents.
- `scripts/publish.py` — creates or updates the page, then renders each mermaid diagram to a retina PNG and uploads it as an attachment.

## What you need from the user

Ask for these before doing anything. Never hardcode them into the scripts — the scripts read credentials from environment variables so nothing sensitive is written to disk.

1. **The markdown file** — its path.
2. **Confluence site** — the subdomain, e.g. `yourcompany.atlassian.net` (no `https://`, no `/wiki`).
3. **Atlassian email** — the account the API token belongs to.
4. **API token** — the user creates one at https://id.atlassian.com/manage-profile/security/api-tokens ("Create API token", ~30 seconds). Atlassian Cloud authenticates as Basic `email:token`; a plain token alone will 401.
5. **Target**, one of:
   - **Update an existing page** — the page ID. It's the number in the page URL: `.../pages/<PAGE_ID>/Some+Title`.
   - **Create a new page** — the **space key** (the short code in `.../spaces/<KEY>/...`) and a title, plus an optional parent page ID to nest it under.

If the user hands you a Confluence page URL, parse the site, space key, and page ID out of it rather than asking again.

Handle the token carefully: prefer having the user paste it into a file you `chmod 600`, or accept it in chat but delete any file you write it to when you're done. Do not echo it back.

## Dependencies

- **Python 3** with the `markdown` library:
  `python3 -m pip install --user --break-system-packages markdown`
- **npx + mermaid-cli** — only needed if the file contains ```mermaid``` blocks. `publish.py` invokes `npx -y -p @mermaid-js/mermaid-cli mmdc`, which downloads on first use. It renders headlessly via Chromium; the script already passes `--no-sandbox`.

Check these first and install what's missing before running.

## Steps

1. **Gather the inputs above.** Confirm the target (update vs create) explicitly — updating overwrites a page's body.
2. **Export credentials** into the environment for the shell session (don't pass them as flags):
   ```bash
   export CONF_SITE="yourcompany.atlassian.net"
   export CONF_EMAIL="you@yourcompany.com"
   export CONF_TOKEN="<api-token>"
   ```
3. **Convert:**
   ```bash
   python3 scripts/convert.py path/to/doc.md storage.html mmd/
   ```
   It prints how many tables and mermaid blocks it found — sanity-check that against the source.
4. **Publish** — update:
   ```bash
   python3 scripts/publish.py --html storage.html --mmd-dir mmd/ --update <PAGE_ID>
   ```
   or create:
   ```bash
   python3 scripts/publish.py --html storage.html --mmd-dir mmd/ \
     --create "Doc Title" --space <SPACEKEY> [--parent <PARENT_ID>]
   ```
   It prints the live page URL. Give that to the user and ask them to confirm the diagrams render (not broken-image icons).

## Verifying it worked

To confirm the diagram attachments bound to their image macros rather than trusting the exit code, fetch the page body and its attachments:
```bash
curl -s -u "$CONF_EMAIL:$CONF_TOKEN" \
  "https://$CONF_SITE/wiki/rest/api/content/<PAGE_ID>?expand=body.storage" \
  | python3 -c "import sys,json;b=json.load(sys.stdin)['body']['storage']['value'];print('tables',b.count('<table>'),'images',b.count('ri:attachment'))"
```

## Gotchas

- **Two mermaid mistakes are auto-fixed at convert time** (on sequence-diagram message lines only, where they'd otherwise be fatal): a `<br/>` on a message-arrow line (`A-->>B: text<br/>more`) — valid only inside a `Note` — is collapsed to a space, and a `;` inside a message (which mermaid reads as a statement terminator, silently truncating the text) becomes a comma. `convert.py` prints `mermaid_autofixes=N` when it touches anything; both fixes are cosmetic and lose no words. Flowchart node/edge labels are left alone, where `<br/>` is legal. If a diagram still fails on some *other* mermaid syntax, fix the source `.md` and re-run.
- **A diagram error never leaves a half-published page.** `publish.py` renders every diagram to PNG *before* it creates or updates the page, so a bad diagram aborts with nothing changed — you won't get a version bump pointing at attachments that never rendered. (Before this, the body was pushed first and a later render failure stranded the page mid-update.)
- **Re-running is safe.** Attachments upload with `PUT` (upsert by filename), so publishing again replaces each diagram instead of stacking duplicates. Updates bump the page version automatically.
- **What survives the conversion:** headings, bold/italic, inline code, ordered/unordered lists, tables, horizontal rules, links, and mermaid (as images). Fenced non-mermaid code blocks come through as `<pre>` text — fine, but not syntax-highlighted. If the user needs highlighted code macros, that's a follow-up, not default behavior.
- **Diagrams are images, not editable in Confluence.** The markdown file stays the source of truth: to change a diagram, edit the `.md` and re-run. That's the intended model — don't try to split the source across two places.
- **First-run auth failures are almost always** a missing `/wiki` assumption (the scripts add it — don't put it in `CONF_SITE`) or using a password instead of an API token.
