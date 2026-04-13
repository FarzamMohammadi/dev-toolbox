#!/usr/bin/env python3
"""Browse and resume all Claude Code sessions with usage stats — including worktree sessions hidden from --resume."""

import curses
import json
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
    filter_pattern, worktrees_only = parse_args()
    sessions = collect_sessions(filter_pattern, worktrees_only)

    if not sessions:
        print("No sessions found.")
        sys.exit(0)

    chosen_index = curses.wrapper(render_session_picker, sessions)

    if chosen_index is not None:
        resume_session(sessions[chosen_index])


# --- Session Discovery ---


def collect_sessions(filter_pattern=None, worktrees_only=False):
    """Scan Claude's project dirs for sessions, sorted newest first."""
    if not CLAUDE_PROJECTS_DIR.is_dir():
        return []

    sessions = []
    for project_dir in CLAUDE_PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue

        is_worktree = "worktree" in project_dir.name
        if worktrees_only and not is_worktree:
            continue

        if filter_pattern and not re.search(filter_pattern, project_dir.name, re.IGNORECASE):
            continue

        if is_worktree:
            label = extract_worktree_label(project_dir.name)
            project_path = resolve_worktree_path(project_dir.name)
        else:
            label = extract_project_label(project_dir.name)
            project_path = decode_project_path(project_dir.name)

        for session_file in project_dir.glob("*.jsonl"):
            mtime = session_file.stat().st_mtime
            title = extract_session_title(session_file)
            if title:
                display_label = f"{label} > {title}" if is_worktree else f"{label} > {title}"
            else:
                display_label = label

            sessions.append({
                "label": display_label,
                "session_id": session_file.stem,
                "date": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M"),
                "timestamp": mtime,
                "project_path": project_path,
                "jsonl_path": str(session_file),
                "is_worktree": is_worktree,
            })

    sessions.sort(key=lambda s: s["timestamp"], reverse=True)
    return sessions


def extract_session_title(jsonl_path):
    """Scan for customTitle in a session file. Fast string check before JSON parse."""
    try:
        with open(jsonl_path) as f:
            for line in f:
                if "customTitle" in line:
                    return json.loads(line).get("customTitle")
    except Exception:
        pass
    return None


def extract_worktree_label(dirname):
    """Turn a worktree project dir name into 'repo > branch'."""
    match = re.search(rf"worktrees-[^-]+-([^-]+-[^-]+)-{ULID_PATTERN}-(.*)", dirname)
    if not match:
        return dirname
    repo, branch = match.group(1), match.group(2)
    return f"{repo} > {branch}".replace("-", " ")


def extract_project_label(dirname):
    """Turn a regular project dir name into a readable label."""
    # e.g. "-Users-farzammohammadi-Documents-Repos-the-engineer" -> "the-engineer"
    # Take the last meaningful segment
    parts = dirname.strip("-").split("-")
    # Find last segment after common path parts
    skip = {"Users", "Documents", "Repos", "home", "farzammohammadi"}
    meaningful = [p for p in parts if p not in skip]
    if meaningful:
        return " ".join(meaningful[-3:])  # last 3 parts for context
    return dirname


def decode_project_path(dirname):
    """Reverse a project dir name back to a filesystem path."""
    # "-Users-foo-Documents-Repos-bar" -> "/Users/foo/Documents/Repos/bar"
    # But "--" encodes "." so: "-Users-foo--bar" -> "/Users/foo/.bar"
    path = dirname.replace("--", "\x00").replace("-", "/").replace("\x00", "/.")
    if not path.startswith("/"):
        path = "/" + path
    return path if os.path.isdir(path) else None


def resolve_worktree_path(dirname):
    """Reverse an encoded worktree project dir name back to its filesystem path."""
    match = re.search(rf"worktrees-(.+)-({ULID_PATTERN}-.+)", dirname)
    if not match:
        return None

    org_and_repo = match.group(1)
    worktree_slug = match.group(2)

    parts = org_and_repo.split("-")
    for i in range(1, len(parts)):
        org = "-".join(parts[:i])
        repo = "-".join(parts[i:])
        for candidate_org in (org, org.lower()):
            path = WORKTREES_BASE_DIR / candidate_org / repo / worktree_slug
            if path.is_dir():
                return str(path)

    return None


# --- Session Stats (lazy loaded) ---


_stats_cache = {}


def get_session_stats(session):
    """Parse the jsonl to extract usage stats. Cached after first read."""
    session_id = session["session_id"]
    if session_id in _stats_cache:
        return _stats_cache[session_id]

    stats = parse_jsonl_stats(session["jsonl_path"])
    _stats_cache[session_id] = stats
    return stats


def parse_jsonl_stats(jsonl_path):
    """Read a session's jsonl and extract title, model, tokens, duration, message counts, and tools."""
    title = None
    model = None
    input_tokens = 0
    output_tokens = 0
    cache_read = 0
    cache_create = 0
    message_count = 0
    tool_counts = {}
    timestamps = []

    try:
        with open(jsonl_path) as f:
            for line in f:
                msg = json.loads(line)
                if not title and "customTitle" in msg:
                    title = msg["customTitle"]

                if "timestamp" in msg:
                    timestamps.append(msg["timestamp"])

                if msg.get("type") != "assistant":
                    continue

                message_count += 1
                raw = msg.get("message", {})
                if not isinstance(raw, dict):
                    continue

                if not model and raw.get("model"):
                    model = raw["model"]

                usage = raw.get("usage", {})
                input_tokens += usage.get("input_tokens", 0)
                output_tokens += usage.get("output_tokens", 0)
                cache_read += usage.get("cache_read_input_tokens", 0)
                cache_create += usage.get("cache_creation_input_tokens", 0)

                for block in raw.get("content", []):
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        name = block.get("name", "?")
                        tool_counts[name] = tool_counts.get(name, 0) + 1
    except Exception:
        return None

    duration = compute_duration(timestamps)
    return {
        "title": title,
        "model": shorten_model_name(model),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read": cache_read,
        "cache_create": cache_create,
        "message_count": message_count,
        "tool_counts": tool_counts,
        "duration": duration,
    }


def compute_duration(timestamps):
    """Return human-readable duration from a list of ISO timestamp strings."""
    if len(timestamps) < 2:
        return "< 1min"
    try:
        times = sorted(datetime.fromisoformat(t.replace("Z", "+00:00")) for t in timestamps)
        delta = times[-1] - times[0]
        minutes = int(delta.total_seconds() / 60)
        if minutes < 1:
            return "< 1min"
        if minutes < 60:
            return f"{minutes}min"
        return f"{minutes // 60}h {minutes % 60}min"
    except Exception:
        return "?"


def shorten_model_name(model):
    if not model:
        return "?"
    short = model.replace("claude-", "")
    short = re.sub(r"-\d{8}$", "", short)
    return short


def format_tokens(n):
    """Format token count: 1234 -> '1.2k', 56789 -> '56.8k', 1234567 -> '1.2M'."""
    if n < 1000:
        return str(n)
    if n < 1_000_000:
        return f"{n / 1000:.1f}k"
    return f"{n / 1_000_000:.1f}M"


def format_stats_line(stats):
    """Build the stats summary string for the footer."""
    if not stats:
        return "  (could not read session data)"

    parts = [stats["model"], stats["duration"], f"{stats['message_count']} msgs"]

    total_in = stats["input_tokens"] + stats["cache_read"] + stats["cache_create"]
    parts.append(f"{format_tokens(total_in)} in / {format_tokens(stats['output_tokens'])} out")

    if stats["tool_counts"]:
        top_tools = sorted(stats["tool_counts"].items(), key=lambda x: -x[1])[:4]
        tools_str = " ".join(f"{name}:{count}" for name, count in top_tools)
        parts.append(tools_str)

    return " " + " · ".join(parts)


# --- Interactive Picker ---


def render_session_picker(stdscr, sessions):
    """Full-screen navigable list. Returns chosen index or None."""
    setup_colors()
    curses.curs_set(0)
    stdscr.nodelay(False)

    cursor = 0
    scroll_offset = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        visible_rows = height - 5

        scroll_offset = keep_cursor_in_view(cursor, scroll_offset, visible_rows)

        draw_header(stdscr, width, len(sessions))
        draw_session_list(stdscr, sessions, cursor, scroll_offset, visible_rows, width)

        # Show "Calculating..." then redraw with real stats
        session = sessions[cursor]
        if session["session_id"] not in _stats_cache:
            draw_footer_loading(stdscr, session, visible_rows, width)
            stdscr.refresh()
            get_session_stats(session)
            stdscr.clear()
            draw_header(stdscr, width, len(sessions))
            draw_session_list(stdscr, sessions, cursor, scroll_offset, visible_rows, width)

        draw_footer(stdscr, session, visible_rows, width)
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
    header = f" {total} sessions (arrow keys navigate, enter resume, q quit)"
    stdscr.attron(curses.A_BOLD)
    stdscr.addnstr(0, 0, header, width - 1)
    stdscr.attroff(curses.A_BOLD)


def draw_session_list(stdscr, sessions, cursor, scroll_offset, visible_rows, width):
    end = min(scroll_offset + visible_rows, len(sessions))
    for i in range(scroll_offset, end):
        row = 2 + (i - scroll_offset)
        session = sessions[i]
        marker = " W " if session["is_worktree"] else "   "
        line = f"{marker}{session['label'][:45]:<45}  {session['date']}"

        if i == cursor:
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addnstr(row, 0, line.ljust(width - 1), width - 1)
            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
        else:
            stdscr.attron(curses.color_pair(1))
            stdscr.addnstr(row, 0, line, width - 1)
            stdscr.attroff(curses.color_pair(1))


def draw_footer_loading(stdscr, session, visible_rows, width):
    footer_start = min(2 + visible_rows, curses.LINES - 3)
    resume_cmd = f" claude --resume {session['session_id']}"
    stdscr.attron(curses.A_DIM)
    stdscr.addnstr(footer_start, 0, resume_cmd, width - 1)
    stdscr.addnstr(footer_start + 1, 0, " Calculating...", width - 1)
    stdscr.attroff(curses.A_DIM)


def draw_footer(stdscr, session, visible_rows, width):
    footer_start = min(2 + visible_rows, curses.LINES - 3)

    resume_cmd = f" claude --resume {session['session_id']}"
    stdscr.attron(curses.A_DIM)
    stdscr.addnstr(footer_start, 0, resume_cmd, width - 1)
    stdscr.attroff(curses.A_DIM)

    stats = get_session_stats(session)
    stats_line = format_stats_line(stats)
    stdscr.attron(curses.A_DIM)
    stdscr.addnstr(footer_start + 1, 0, stats_line, width - 1)
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
    """cd into the project directory and hand off to claude --resume."""
    project_path = session["project_path"]
    session_id = session["session_id"]

    if not project_path:
        print(f"Project directory no longer exists for: {session['label']}")
        print(f"Session ID: {session_id}")
        sys.exit(1)

    os.chdir(project_path)
    os.execvp("claude", ["claude", "--resume", session_id])


# --- CLI ---


def parse_args():
    filter_pattern = None
    worktrees_only = False
    args = sys.argv[1:]

    for arg in args:
        if arg in ("-h", "--help"):
            print("Usage: claude-sessions.py [--worktrees-only] [pattern]")
            print("")
            print("  --worktrees-only    Only show worktree sessions")
            print("  pattern             Filter sessions by name (regex)")
            print("")
            print("Controls:")
            print("  arrow keys / j,k    Navigate")
            print("  enter               Resume selected session")
            print("  page up/down        Jump")
            print("  q / esc             Quit")
            sys.exit(0)
        elif arg == "--worktrees-only":
            worktrees_only = True
        else:
            filter_pattern = arg

    return filter_pattern, worktrees_only


if __name__ == "__main__":
    main()
