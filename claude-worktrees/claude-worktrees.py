#!/usr/bin/env python3
"""Find and resume Claude Code worktree sessions that don't show up in --resume."""

import curses
import os
import re
import sys
from datetime import datetime
from pathlib import Path

CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"
WORKTREES_BASE_DIR = Path.home() / ".engineer" / "workspaces" / "worktrees"
ULID_PATTERN = r"[A-Z0-9]{26}"


# --- Main Flow ---


def main():
    filter_pattern = parse_args()
    sessions = collect_worktree_sessions(filter_pattern)

    if not sessions:
        print("No worktree sessions found.")
        sys.exit(0)

    chosen_index = curses.wrapper(render_session_picker, sessions)

    if chosen_index is not None:
        resume_session(sessions[chosen_index])


# --- Session Discovery ---


def collect_worktree_sessions(filter_pattern=None):
    """Scan Claude's project dirs for worktree sessions, sorted newest first."""
    if not CLAUDE_PROJECTS_DIR.is_dir():
        return []

    sessions = []
    for project_dir in CLAUDE_PROJECTS_DIR.iterdir():
        if not is_worktree_project(project_dir):
            continue
        if filter_pattern and not re.search(filter_pattern, project_dir.name, re.IGNORECASE):
            continue

        label = extract_label(project_dir.name)
        worktree_path = resolve_worktree_path(project_dir.name)

        for session_file in project_dir.glob("*.jsonl"):
            mtime = session_file.stat().st_mtime
            sessions.append({
                "label": label,
                "session_id": session_file.stem,
                "date": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M"),
                "timestamp": mtime,
                "worktree_path": worktree_path,
            })

    sessions.sort(key=lambda s: s["timestamp"], reverse=True)
    return sessions


def is_worktree_project(path):
    return path.is_dir() and "worktree" in path.name


def extract_label(dirname):
    """Turn a project dir name into a human-readable 'repo > branch' label."""
    match = re.search(rf"worktrees-[^-]+-([^-]+-[^-]+)-{ULID_PATTERN}-(.*)", dirname)
    if not match:
        return dirname
    repo, branch = match.group(1), match.group(2)
    return f"{repo} > {branch}".replace("-", " ")


def resolve_worktree_path(dirname):
    """Reverse the encoded project dir name back to its worktree filesystem path."""
    match = re.search(rf"worktrees-(.+)-({ULID_PATTERN}-.+)", dirname)
    if not match:
        return None

    org_and_repo = match.group(1)
    worktree_slug = match.group(2)

    # Repo names can contain dashes, so try every possible org/repo split
    parts = org_and_repo.split("-")
    for i in range(1, len(parts)):
        org = "-".join(parts[:i])
        repo = "-".join(parts[i:])
        for candidate_org in (org, org.lower()):
            path = WORKTREES_BASE_DIR / candidate_org / repo / worktree_slug
            if path.is_dir():
                return str(path)

    return None


# --- Interactive Picker ---


def render_session_picker(stdscr, sessions):
    """Full-screen navigable list. Returns the chosen session dict or None."""
    setup_colors()
    curses.curs_set(0)

    cursor = 0
    scroll_offset = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        visible_rows = height - 4

        scroll_offset = keep_cursor_in_view(cursor, scroll_offset, visible_rows)

        draw_header(stdscr, width, len(sessions))
        draw_session_list(stdscr, sessions, cursor, scroll_offset, visible_rows, width)
        draw_footer(stdscr, sessions[cursor], visible_rows, width)

        stdscr.refresh()

        cursor, scroll_offset, chosen = handle_input(
            stdscr, cursor, scroll_offset, visible_rows, len(sessions)
        )
        if chosen is not None:
            return chosen if chosen != "quit" else None


def setup_colors():
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)


def keep_cursor_in_view(cursor, scroll_offset, visible_rows):
    if cursor < scroll_offset:
        return cursor
    if cursor >= scroll_offset + visible_rows:
        return cursor - visible_rows + 1
    return scroll_offset


def draw_header(stdscr, width, total):
    header = f" {total} worktree sessions (arrow keys navigate, enter resume, q quit)"
    stdscr.attron(curses.A_BOLD)
    stdscr.addnstr(0, 0, header, width - 1)
    stdscr.attroff(curses.A_BOLD)


def draw_session_list(stdscr, sessions, cursor, scroll_offset, visible_rows, width):
    end = min(scroll_offset + visible_rows, len(sessions))
    for i in range(scroll_offset, end):
        row = 2 + (i - scroll_offset)
        session = sessions[i]
        line = f" {session['label'][:48]:<48}  {session['date']}"

        if i == cursor:
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addnstr(row, 0, line.ljust(width - 1), width - 1)
            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
        else:
            stdscr.attron(curses.color_pair(1))
            stdscr.addnstr(row, 0, line, width - 1)
            stdscr.attroff(curses.color_pair(1))


def draw_footer(stdscr, session, visible_rows, width):
    footer_row = min(2 + visible_rows, curses.LINES - 1)
    resume_cmd = f" claude --resume {session['session_id']}"
    stdscr.attron(curses.A_DIM)
    stdscr.addnstr(footer_row, 0, resume_cmd, width - 1)
    stdscr.attroff(curses.A_DIM)


def handle_input(stdscr, cursor, scroll_offset, visible_rows, total):
    """Returns (cursor, scroll_offset, chosen). chosen is None to keep looping."""
    key = stdscr.getch()

    if key in (ord("q"), 27):
        return cursor, scroll_offset, "quit"
    elif key in (curses.KEY_UP, ord("k")):
        cursor = max(0, cursor - 1)
    elif key in (curses.KEY_DOWN, ord("j")):
        cursor = min(total - 1, cursor + 1)
    elif key == curses.KEY_PPAGE:
        cursor = max(0, cursor - visible_rows)
    elif key == curses.KEY_NPAGE:
        cursor = min(total - 1, cursor + visible_rows)
    elif key == curses.KEY_HOME:
        cursor = 0
    elif key == curses.KEY_END:
        cursor = total - 1
    elif key in (10, 13):
        return cursor, scroll_offset, cursor

    return cursor, scroll_offset, None


# --- Resume ---


def resume_session(session):
    """cd into the worktree directory and hand off to claude --resume."""
    worktree_path = session["worktree_path"]
    session_id = session["session_id"]

    if not worktree_path:
        print(f"Worktree directory no longer exists for: {session['label']}")
        print(f"Session ID: {session_id}")
        sys.exit(1)

    os.chdir(worktree_path)
    os.execvp("claude", ["claude", "--resume", session_id])


# --- CLI ---


def parse_args():
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print("Usage: claude-worktrees.py [pattern]")
            print("  Navigate with arrow keys, enter to resume, q to quit")
            sys.exit(0)
        return sys.argv[1]
    return None


if __name__ == "__main__":
    main()
