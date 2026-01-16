# TUI Markdown Browser

Terminal markdown browser with live preview. Navigate files with keyboard, scroll preview with mouse.

## Quick Start

```bash
# Create and activate virtual environment
uv venv && source .venv/bin/activate

# Install the tool
uv pip install -e .

# Run
tui-markdown-browser
```

## Usage

```bash
# Browse current directory
tui-markdown-browser

# Browse specific path
tui-markdown-browser /path/to/docs

# Or run as module
python -m tui_markdown_browser /path/to/docs
```

## Controls

### Keyboard (file navigation)

| Key | Action |
|-----|--------|
| `↑` `↓` | Move up/down |
| `←` | Go to parent directory |
| `→` | Enter directory |
| `Enter` | Preview selected file |
| `q` | Quit |
| `r` | Reload file tree |
| `t` | Toggle table of contents |
| `w` | Cycle TOC width |

### Mouse (preview)

- **Scroll** to read content
- **Click** TOC headings to jump
- **Click** links to navigate (markdown files open in preview, URLs open in browser)

## Features

- Live markdown rendering with syntax highlighting
- Table of contents sidebar with adjustable width (0%, 15%, 25%, 35%, 50%)
- Clickable links (internal files + external URLs)
- Clean separation: keyboard for files, mouse for preview
- Hidden files and common noise directories filtered out (node_modules, __pycache__, .git, etc.)

## Requirements

- Python 3.11+
- textual >= 0.40.0

## Development

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run linter
ruff check .

# Run type checker
mypy tui_markdown_browser
```
