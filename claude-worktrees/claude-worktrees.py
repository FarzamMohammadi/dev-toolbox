#!/usr/bin/env python3
"""claude-worktrees — find and resume Claude Code worktree sessions that don't show up in --resume"""

import curses
import os
import re
import sys
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"


def find_sessions(filter_pat=None):
    if not PROJECTS_DIR.is_dir():
        return []

    sessions = []
    for d in PROJECTS_DIR.iterdir():
        if not d.is_dir() or "worktree" not in d.name:
            continue
        if filter_pat and not re.search(filter_pat, d.name, re.IGNORECASE):
            continue

        # Extract readable label: repo + branch from dir name
        m = re.search(r"worktrees-[^-]+-([^-]+-[^-]+)-[A-Z0-9]{26}-(.*)", d.name)
        label = m.group(1) + " → " + m.group(2) if m else d.name
        label = label.replace("-", " ")

        for jsonl in d.glob("*.jsonl"):
            sid = jsonl.stem
            mtime = jsonl.stat().st_mtime
            date_str = __import__("datetime").datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            sessions.append((label, sid, date_str, mtime))

    sessions.sort(key=lambda x: x[3], reverse=True)
    return sessions


def interactive(stdscr, sessions):
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_WHITE, -1)

    selected = 0
    offset = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        visible = h - 4  # header + footer

        if selected < offset:
            offset = selected
        if selected >= offset + visible:
            offset = selected - visible + 1

        # Header
        header = f" {len(sessions)} worktree sessions (↑↓ navigate · enter resume · q quit)"
        stdscr.attron(curses.A_BOLD)
        stdscr.addnstr(0, 0, header, w - 1)
        stdscr.attroff(curses.A_BOLD)

        # List
        for i in range(offset, min(offset + visible, len(sessions))):
            row = 2 + (i - offset)
            label, sid, date_str, _ = sessions[i]
            line = f" {label[:48]:<48}  {date_str}"

            if i == selected:
                stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                stdscr.addnstr(row, 0, line.ljust(w - 1), w - 1)
                stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.attron(curses.color_pair(1))
                stdscr.addnstr(row, 0, line, w - 1)
                stdscr.attroff(curses.color_pair(1))

        # Footer
        footer_row = min(2 + visible, h - 1)
        sid_line = f" claude --resume {sessions[selected][1]}"
        stdscr.attron(curses.A_DIM)
        stdscr.addnstr(footer_row, 0, sid_line, w - 1)
        stdscr.attroff(curses.A_DIM)

        stdscr.refresh()

        key = stdscr.getch()
        if key == ord("q") or key == 27:  # q or esc
            return None
        elif key == curses.KEY_UP or key == ord("k"):
            selected = max(0, selected - 1)
        elif key == curses.KEY_DOWN or key == ord("j"):
            selected = min(len(sessions) - 1, selected + 1)
        elif key == curses.KEY_PPAGE:  # page up
            selected = max(0, selected - visible)
        elif key == curses.KEY_NPAGE:  # page down
            selected = min(len(sessions) - 1, selected + visible)
        elif key == curses.KEY_HOME:
            selected = 0
        elif key == curses.KEY_END:
            selected = len(sessions) - 1
        elif key in (curses.KEY_ENTER, 10, 13):
            return sessions[selected][1]


def main():
    filter_pat = None
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print("Usage: claude-worktrees [pattern]")
            print("  Navigate with arrow keys, enter to resume, q to quit")
            sys.exit(0)
        filter_pat = sys.argv[1]

    sessions = find_sessions(filter_pat)
    if not sessions:
        print("No worktree sessions found.")
        sys.exit(0)

    chosen = curses.wrapper(interactive, sessions)
    if chosen:
        os.execvp("claude", ["claude", "--resume", chosen])


if __name__ == "__main__":
    main()
