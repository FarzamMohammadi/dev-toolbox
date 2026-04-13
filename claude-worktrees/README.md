# Claude Worktrees

Find and resume Claude Code worktree sessions that don't show up in `claude --resume`. Interactive TUI with arrow-key navigation — pure Python, zero dependencies.

## Quick Start

```bash
# Make executable
chmod +x claude-worktrees.py

# Browse all worktree sessions
./claude-worktrees.py

# Filter by repo or branch name
./claude-worktrees.py the-engineer
```

## Controls

- **↑/↓** or **j/k** — navigate
- **Page Up/Down** — jump
- **Enter** — resume selected session
- **q/Esc** — quit
