#!/bin/bash
# =============================================================================
# Python Dependencies Analyzer
# =============================================================================
# Generates module dependency graphs for Python projects using pydeps.
#
# Requirements: pydeps (via venv), graphviz
# Usage: ./run.sh <target_repo> <output_dir>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAPPER_ROOT="$(dirname "$(dirname "$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")")")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

# =============================================================================
# Arguments
# =============================================================================

TARGET_REPO="${1:-.}"
OUTPUT_DIR="${2:-./output}"

# Resolve to absolute paths
TARGET_REPO="$(cd "$TARGET_REPO" && pwd)"
mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"

# Create python output subdirectory
PYTHON_OUTPUT_DIR="$OUTPUT_DIR/python"
mkdir -p "$PYTHON_OUTPUT_DIR"

echo ""
echo -e "${BOLD}Python Dependencies Analyzer${NC}"
echo "=============================="
echo ""
echo "Target: $TARGET_REPO"
echo "Output: $PYTHON_OUTPUT_DIR"
echo ""

# =============================================================================
# Activate Virtual Environment (if available)
# =============================================================================

VENV_DIR="$MAPPER_ROOT/.venv"
if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
    echo -e "${GREEN}[OK]${NC} Using venv: $VENV_DIR"
fi

# =============================================================================
# Check Requirements
# =============================================================================

if ! command -v pydeps &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} pydeps is not installed"
    echo ""
    echo "Run setup.sh to install dependencies:"
    echo "  cd $MAPPER_ROOT && ./setup.sh"
    echo ""
    echo "Or install manually with uv:"
    echo "  uv venv $VENV_DIR"
    echo "  uv pip install --python $VENV_DIR/bin/python pydeps"
    echo ""
    exit 1
fi

if ! command -v dot &> /dev/null; then
    echo -e "${YELLOW}[WARN]${NC} graphviz not installed (needed for graph rendering)"
    echo "       Install with: brew install graphviz"
    echo ""
fi

echo -e "${GREEN}[OK]${NC} pydeps found"
echo ""

# =============================================================================
# Find Python Source Directory
# =============================================================================

cd "$TARGET_REPO"

# Use env var from orchestrator or default
PYTHON_SRC_DIRS="${PYTHON_SRC_DIRS:-src lib app .}"

# Convert space-separated string to array
read -ra SRC_DIRS <<< "$PYTHON_SRC_DIRS"
PYTHON_SRC=""

for dir in "${SRC_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        # Check if there are Python files
        py_count=$(find "$dir" -maxdepth 3 -name "*.py" 2>/dev/null | head -20 | wc -l | tr -d ' ')
        if [ "$py_count" -gt 0 ]; then
            PYTHON_SRC="$dir"
            break
        fi
    fi
done

if [ -z "$PYTHON_SRC" ]; then
    echo -e "${YELLOW}[WARN]${NC} No Python source directory found"
    exit 0
fi

echo "Analyzing Python source: $PYTHON_SRC"
echo ""

# =============================================================================
# Find Packages
# =============================================================================

echo "Detecting Python packages..."

# Collect all packages (directories with __init__.py)
PACKAGES=()

# Check if src itself is a package
if [ -f "$PYTHON_SRC/__init__.py" ]; then
    PACKAGES+=("$PYTHON_SRC")
    echo "  Found package: $PYTHON_SRC (root)"
fi

# Find all subpackages
while IFS= read -r init_file; do
    pkg_dir=$(dirname "$init_file")
    # Skip if it's the root we already added
    if [ "$pkg_dir" != "$PYTHON_SRC" ] && [ "$pkg_dir" != "." ]; then
        # Only add top-level packages (direct children of PYTHON_SRC)
        parent_dir=$(dirname "$pkg_dir")
        if [ "$parent_dir" = "$PYTHON_SRC" ] || [ "$parent_dir" = "." ]; then
            PACKAGES+=("$pkg_dir")
            echo "  Found package: $(basename "$pkg_dir")"
        fi
    fi
done < <(find "$PYTHON_SRC" -maxdepth 3 -name "__init__.py" 2>/dev/null)

# If no packages found, look for directories with multiple .py files (namespace packages)
if [ ${#PACKAGES[@]} -eq 0 ]; then
    echo "  No __init__.py found, looking for namespace packages..."
    while IFS= read -r dir; do
        if [ -d "$dir" ] && [ "$dir" != "$PYTHON_SRC" ]; then
            py_count=$(find "$dir" -maxdepth 1 -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
            if [ "$py_count" -gt 1 ]; then
                PACKAGES+=("$dir")
                echo "  Found namespace package: $(basename "$dir")"
            fi
        fi
    done < <(find "$PYTHON_SRC" -maxdepth 1 -type d 2>/dev/null)
fi

echo ""

# =============================================================================
# Generate Dependencies Graph
# =============================================================================

echo "Generating dependency graph..."

# Set PYTHONPATH so pydeps can resolve imports
export PYTHONPATH="$TARGET_REPO:$PYTHON_SRC:${PYTHONPATH:-}"

GRAPH_GENERATED=false

# Strategy 1: If we found packages, try each one
if [ ${#PACKAGES[@]} -gt 0 ]; then
    # Try the first/main package
    MAIN_PKG="${PACKAGES[0]}"
    PKG_NAME=$(basename "$MAIN_PKG")
    echo "  Analyzing package: $PKG_NAME"

    # Try with --only to show only internal dependencies (cleaner graph)
    if pydeps "$MAIN_PKG" \
        --only "$PKG_NAME" \
        --cluster \
        --no-show \
        --reverse \
        -o "$PYTHON_OUTPUT_DIR/dependencies.svg" \
        2>/dev/null; then
        GRAPH_GENERATED=true
        echo -e "  ${GREEN}✓${NC} Generated with internal deps only"
    fi

    # Fallback: try without --only (shows external deps too)
    if [ "$GRAPH_GENERATED" = false ]; then
        echo "  Trying with external dependencies included..."
        if pydeps "$MAIN_PKG" \
            --max-bacon 3 \
            --cluster \
            --no-show \
            -o "$PYTHON_OUTPUT_DIR/dependencies.svg" \
            2>/dev/null; then
            GRAPH_GENERATED=true
            echo -e "  ${GREEN}✓${NC} Generated with clustering"
        fi
    fi

    # Fallback: simpler mode without clustering
    if [ "$GRAPH_GENERATED" = false ]; then
        echo "  Trying simpler mode..."
        if pydeps "$MAIN_PKG" \
            --max-bacon 2 \
            --no-show \
            -o "$PYTHON_OUTPUT_DIR/dependencies.svg" \
            2>/dev/null; then
            GRAPH_GENERATED=true
            echo -e "  ${GREEN}✓${NC} Generated (simple mode)"
        fi
    fi
fi

# Strategy 2: Try analyzing src directory directly with pyproject.toml detection
if [ "$GRAPH_GENERATED" = false ]; then
    # Check if there's a pyproject.toml or setup.py (installable package)
    if [ -f "$TARGET_REPO/pyproject.toml" ] || [ -f "$TARGET_REPO/setup.py" ]; then
        echo "  Detected installable package, trying project root..."

        # Try to find the package name from pyproject.toml
        if [ -f "$TARGET_REPO/pyproject.toml" ]; then
            PKG_NAME=$(grep -E "^name\s*=" "$TARGET_REPO/pyproject.toml" 2>/dev/null | head -1 | sed 's/.*=\s*["'"'"']\([^"'"'"']*\)["'"'"'].*/\1/' | tr '-' '_')
        fi

        if [ -n "$PKG_NAME" ] && [ -d "$PYTHON_SRC/$PKG_NAME" ]; then
            echo "  Found package from pyproject.toml: $PKG_NAME"
            if pydeps "$PYTHON_SRC/$PKG_NAME" \
                --cluster \
                --no-show \
                -o "$PYTHON_OUTPUT_DIR/dependencies.svg" \
                2>/dev/null; then
                GRAPH_GENERATED=true
            fi
        fi
    fi
fi

# Strategy 3: Last resort - analyze the whole source directory
if [ "$GRAPH_GENERATED" = false ]; then
    echo "  Trying full source directory analysis..."
    pydeps "$PYTHON_SRC" \
        --max-bacon 2 \
        --no-show \
        -o "$PYTHON_OUTPUT_DIR/dependencies.svg" \
        2>/dev/null || {
            echo -e "${YELLOW}[WARN]${NC} pydeps could not generate graph"
            echo "       The project structure may not be compatible with pydeps"
            echo "       Check imports.txt for dependency information instead"
        }
fi

# =============================================================================
# Generate Text Dependencies (simpler, always works)
# =============================================================================

echo ""
echo "Extracting import statements..."

# Extract all imports from Python files
{
    echo "# Python Dependencies"
    echo "# Extracted imports from $TARGET_REPO"
    echo "# Generated: $(date)"
    echo ""
    echo "## Standard Library Imports"
    find "$PYTHON_SRC" -name "*.py" -exec grep -h "^import \|^from " {} \; 2>/dev/null | \
        grep -v "^\s*#" | \
        sort -u | \
        grep -E "^(import|from) (os|sys|re|json|typing|collections|functools|itertools|pathlib|datetime|time|logging|subprocess|argparse|unittest|dataclasses|abc|contextlib|copy|io|math|random|string|textwrap|warnings|enum|uuid)" | \
        head -50
    echo ""
    echo "## Third-Party Imports"
    find "$PYTHON_SRC" -name "*.py" -exec grep -h "^import \|^from " {} \; 2>/dev/null | \
        grep -v "^\s*#" | \
        sort -u | \
        grep -vE "^(import|from) (os|sys|re|json|typing|collections|functools|itertools|pathlib|datetime|time|logging|subprocess|argparse|unittest|dataclasses|abc|contextlib|copy|io|math|random|string|textwrap|warnings|enum|uuid|\.)" | \
        head -50
    echo ""
    echo "## Internal Imports (relative)"
    find "$PYTHON_SRC" -name "*.py" -exec grep -h "^from \." {} \; 2>/dev/null | \
        grep -v "^\s*#" | \
        sort -u | \
        head -50
} > "$PYTHON_OUTPUT_DIR/imports.txt"

echo -e "${GREEN}[OK]${NC} Import analysis complete"

# =============================================================================
# Summary
# =============================================================================

echo ""
echo -e "${GREEN}[OK]${NC} Python dependency analysis complete:"

if [ -f "$PYTHON_OUTPUT_DIR/dependencies.svg" ]; then
    echo "  - $PYTHON_OUTPUT_DIR/dependencies.svg (visual graph)"
fi
echo "  - $PYTHON_OUTPUT_DIR/imports.txt (import list)"
echo ""
