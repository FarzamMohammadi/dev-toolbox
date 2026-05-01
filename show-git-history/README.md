> Inspired by and built on top of [ghui](https://github.com/kitlangton/ghui) by [Kit Langton](https://github.com/kitlangton). Much of the UI architecture, component patterns, and rendering code originates from his work. This project strips the GitHub coupling and repurposes it as an offline-only local git viewer.

# show-git-history

A terminal git history/diff viewer. Browse branches, commits, files, and diffs — fully offline.

## Install

```bash
cd show-git-history
bun install
```

## Usage

```bash
cd /path/to/any/repo
bun run /path/to/show-git-history/src/index.tsx
```

Or install globally:

```bash
cd show-git-history && bun install -g .
show-git-history   # from any repo
```

## Features

| View            | Key | Description                                      |
|-----------------|-----|--------------------------------------------------|
| Branch History  | `1` | Browse branches, select one to see its commits   |
| File History    | `2` | Browse files, select one to see its commit history |
| Branch Review   | `3` | See what the current branch proposes vs main     |

## Keybindings

| Key       | Action                          |
|-----------|---------------------------------|
| `j` / `k` | Navigate up/down               |
| `Enter`   | Drill in / open diff            |
| `Esc`     | Go back / clear filter          |
| `d`       | Open diff view                  |
| `f`       | Toggle file-scoped/full diff    |
| `v`       | Toggle unified/split diff       |
| `w`       | Toggle word wrap                |
| `[` / `]` | Previous/next file in diff      |
| `/`       | Filter current list             |
| `r`       | Refresh                         |
| `T`       | Theme selector                  |
| `y`       | Copy commit info to clipboard   |
| `q`       | Quit                            |

## Configuration

Set via environment variables:

- `GIT_HISTORY_COMMIT_LIMIT` — max commits to load (default: 500)
- `GIT_HISTORY_FILE_HISTORY_LIMIT` — max file history entries (default: 200)
- `GIT_HISTORY_OTLP_ENDPOINT` — OpenTelemetry collector endpoint (optional)
- `GIT_HISTORY_MOTEL_PORT` — Motel dev port, shorthand for `http://127.0.0.1:<port>` (optional)

## Note

This project is still in active development and may have rough edges. Bugs will be ironed out through usage. Contributions are welcome.
