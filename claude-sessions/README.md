# Claude Sessions

Browse and resume all Claude Code sessions with live usage stats — including worktree sessions hidden from `claude --resume`. Pure Python, zero dependencies.

## Quick Start

```bash
# Browse all sessions
python3 claude-sessions.py

# Filter by repo or branch name
python3 claude-sessions.py the-engineer

# Only show worktree sessions
python3 claude-sessions.py --worktrees-only
```

## Controls

- **↑/↓** or **j/k** — navigate
- **Page Up/Down** — jump
- **Enter** — resume selected session
- **q/Esc** — quit

## What You See

Each session shows a label and date. The footer shows the selected session's usage stats:

```
 claude --resume 94d3cf61-672b-41a0-bf59-c6fdea8fe9db
 opus-4-6 · 8min · 50 msgs · 14.5k in / 3.7k out · Read:14 Grep:3
```

Stats are parsed once on first selection and cached. Worktree sessions are marked with `W`.
