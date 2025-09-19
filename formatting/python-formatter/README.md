# Python Code Formatter

Standalone Python formatter: removes unused imports, sorts imports, formats code, checks for issues.

## Setup
```bash
cd python-formatter
python -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
```

## Usage
```bash
python formatter.py .                    # Format current directory
python formatter.py ./project-dir       # Format external project
python formatter.py file.py             # Format single file
python formatter.py . --check           # Check only (no changes)
python formatter.py . --verbose         # Show details
```

## What It Does
- Removes unused imports (except `__init__.py`)
- Sorts imports (Google style: stdlib → third-party → local)
- Formats to 88 char line length
- Finds common issues (F401, F541, E721)

## Dependencies
- `click` - CLI framework
- `colorama` - Colored output
- `rich` - Progress bars (optional)

Core formatting uses only Python standard library.