# gws

Unified Claude Code skill for Google Workspace via the official `gws` CLI ([github.com/googleworkspace/cli](https://github.com/googleworkspace/cli)).

Send Gmail, create and update Google Docs and Sheets, upload and share Google Drive files, and convert markdown to formatted Docs, all from a single `/gws` invocation.

## Install

```bash
brew install googleworkspace-cli       # macOS
# or
npm install -g @googleworkspace/cli    # cross-platform
```

## Authenticate

```bash
gws auth setup     # one-time: creates a Cloud project, enables APIs
gws auth login     # browser OAuth
gws auth whoami    # verify
```

Full troubleshooting in [setup.md](setup.md).

## Examples

```
/gws send an email to alice@example.com saying the report is ready
/gws save this markdown as a google doc and share with bob@example.com
/gws make a sheet titled "Q1 Budget" with rows: Item,Cost
/gws upload ~/Downloads/report.pdf and give me a shareable link
```

## Structure

| File | Purpose |
|------|---------|
| [skill.md](skill.md) | Router: pre-flight check + intent → sub-file dispatch |
| [setup.md](setup.md) | Install + auth walkthrough + troubleshooting |
| [gmail.md](gmail.md) | Send, read, reply, forward |
| [docs.md](docs.md) | Create, append, markdown → formatted Doc |
| [sheets.md](sheets.md) | Create, append rows, read ranges |
| [drive.md](drive.md) | Upload, share, get link |

The router reads only `skill.md` on activation; sub-files load on demand.
