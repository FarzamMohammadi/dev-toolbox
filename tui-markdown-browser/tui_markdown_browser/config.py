"""Configuration constants for tui-markdown-browser."""

# TOC width presets (percentages, 0 = hidden)
TOC_WIDTHS: list[int] = [0, 15, 25, 35, 50]

# Directories and files to hide in the file tree
FILTERED_NAMES: set[str] = {
    "node_modules",
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    "*.egg-info",
}

# Welcome message shown on startup
WELCOME_MESSAGE = """\
# tui-markdown-browser

**Keyboard (files)**
- `↑` `↓` move up/down
- `←` go back (parent)
- `→` enter directory
- `Enter` preview file

**Mouse (preview)**
- Scroll to read
- Click TOC to jump

**Shortcuts**
- `q` quit
- `r` reload
- `t` toggle TOC
- `w` TOC width
"""
