---
name: gws
description: Unified interface for Google Workspace via the gws CLI. Send Gmail, create/read/append Google Docs and Sheets, upload and share Google Drive files, and convert markdown to formatted Docs. Use when the user mentions Gmail, Google Docs, Google Sheets, Google Drive, or Google Workspace tasks.
---

# Google Workspace Skill

A router skill for Google Workspace operations via the official `gws` CLI (github.com/googleworkspace/cli). Dispatches to focused sub-files in this directory based on what the user asks.

## Pre-Flight Check

Run this single check before any operation:

```bash
command -v gws &>/dev/null && gws auth whoami 2>&1 | head -1 || echo "gws missing or not authed — see setup.md"
```

If `gws` is missing or not authenticated, stop and read [setup.md](setup.md) to walk the user through install + auth. Do not proceed to operations until pre-flight passes.

## Intent Routing

Match the user's request to the relevant sub-file and read it before acting:

| User intent | Sub-file |
|-------------|----------|
| Send / draft / read / reply to email | [gmail.md](gmail.md) |
| Create / append / read Google Docs (incl. markdown → Doc) | [docs.md](docs.md) |
| Create / append / read Google Sheets | [sheets.md](sheets.md) |
| Upload / share / get-link for Drive files | [drive.md](drive.md) |
| Install issues, auth errors, scope problems | [setup.md](setup.md) |

For cross-service workflows (e.g. "save this md as a doc and share with X"), read both relevant sub-files (`docs.md` + `drive.md`).

## Common Rules

1. Always confirm before write commands (send, create, share, upload). Show the user what's about to happen and wait for go-ahead.
2. Always return the resulting URL or ID so the user can open or reference the artifact.
3. Use `--format json` when chaining commands or parsing output. Default human format is fine for one-shot reads.
4. Quote sheet ranges containing `!` with double quotes to avoid zsh history expansion: `--range "Sheet1!A1"`.
5. Never paste auth tokens or service-account JSON contents into chat. Reference them via env vars or file paths only.

## Cross-Service Workflows

| Workflow | Sub-files to read |
|----------|-------------------|
| Save markdown as a formatted Doc and share with someone | docs.md → drive.md |
| Email a Drive link to someone | drive.md → gmail.md |
| Generate a Sheet from data and email the link | sheets.md → gmail.md |
| Upload an attachment and reference it in an email | drive.md → gmail.md |

## Output Style

- Lead with the result (URL or ID) so the user can act immediately.
- Then a short summary of what was done.
- Skip raw JSON unless the user asked for it.
