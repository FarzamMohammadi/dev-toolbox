#!/bin/bash
# =============================================================================
# Python Call Graph Analyzer
# =============================================================================
# Generates function call graphs for Python projects using pyan3.
#
# Requirements: pyan3 (via venv), graphviz
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
echo -e "${BOLD}Python Call Graph Analyzer${NC}"
echo "==========================="
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

if ! command -v pyan3 &> /dev/null; then
    # Also check for pyan (older name)
    if ! command -v pyan &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} pyan3 is not installed"
        echo ""
        echo "Run setup.sh to install dependencies:"
        echo "  cd $MAPPER_ROOT && ./setup.sh"
        echo ""
        echo "Or install manually with uv:"
        echo "  uv venv $VENV_DIR"
        echo "  uv pip install --python $VENV_DIR/bin/python pyan3"
        echo ""
        exit 1
    fi
    PYAN_CMD="pyan"
else
    PYAN_CMD="pyan3"
fi

echo -e "${GREEN}[OK]${NC} $PYAN_CMD found"
echo ""

# =============================================================================
# Find Python Files
# =============================================================================

cd "$TARGET_REPO"

# Use env var from orchestrator or default
PYTHON_MAX_FILES="${PYTHON_MAX_FILES:-100}"

# Collect Python files (excluding tests and common non-source directories)
PYTHON_FILES=$(find . -name "*.py" \
    -not -path "*/.git/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/.venv/*" \
    -not -path "*/venv/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/test/*" \
    -not -path "*/tests/*" \
    -not -name "test_*.py" \
    -not -name "*_test.py" \
    -not -name "conftest.py" \
    -not -name "setup.py" \
    2>/dev/null | head -"$PYTHON_MAX_FILES")

FILE_COUNT=$(echo "$PYTHON_FILES" | grep -c "\.py$" || echo "0")

if [ "$FILE_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}[WARN]${NC} No Python source files found"
    exit 0
fi

echo "Found $FILE_COUNT Python files to analyze"
echo ""

# =============================================================================
# Generate Call Graph
# =============================================================================

echo "Generating call graph (this may take a moment)..."

# Create a temporary file list
TEMP_FILE=$(mktemp)
echo "$PYTHON_FILES" > "$TEMP_FILE"

# Generate SVG call graph
# Using --uses to show function calls, --defines to show definitions
# --grouped to organize by module, --annotated for labels
{
    $PYAN_CMD $(cat "$TEMP_FILE" | tr '\n' ' ') \
        --uses --defines \
        --grouped \
        --annotated \
        --svg \
        -o "$PYTHON_OUTPUT_DIR/call-graph.svg" \
        2>/dev/null
} || {
    echo -e "${YELLOW}[WARN]${NC} Full call graph failed, trying simplified version..."

    # Try with fewer options
    $PYAN_CMD $(cat "$TEMP_FILE" | tr '\n' ' ') \
        --uses \
        --svg \
        -o "$PYTHON_OUTPUT_DIR/call-graph.svg" \
        2>/dev/null || {
            echo -e "${YELLOW}[WARN]${NC} Call graph generation failed"
            echo "       The project may have syntax errors or complex imports"
        }
}

# Also generate DOT file for potential further processing
{
    $PYAN_CMD $(cat "$TEMP_FILE" | tr '\n' ' ') \
        --uses --defines \
        --grouped \
        --dot \
        -o "$PYTHON_OUTPUT_DIR/call-graph.dot" \
        2>/dev/null
} || true

# Clean up
rm -f "$TEMP_FILE"

# =============================================================================
# Generate Text Summary
# =============================================================================

echo ""
echo "Generating function summary..."

# Extract function and class definitions
{
    echo "# Python Call Graph Summary"
    echo "# Generated: $(date)"
    echo ""
    echo "## Classes"
    echo ""
    grep -rh "^class " . --include="*.py" \
        --exclude-dir=".git" \
        --exclude-dir="node_modules" \
        --exclude-dir=".venv" \
        --exclude-dir="venv" \
        --exclude-dir="__pycache__" \
        2>/dev/null | \
        sed 's/class //' | \
        sed 's/(.*://' | \
        sort -u | \
        head -50

    echo ""
    echo "## Functions"
    echo ""
    grep -rh "^def \|^    def \|^        def " . --include="*.py" \
        --exclude-dir=".git" \
        --exclude-dir="node_modules" \
        --exclude-dir=".venv" \
        --exclude-dir="venv" \
        --exclude-dir="__pycache__" \
        2>/dev/null | \
        sed 's/def //' | \
        sed 's/(.*://' | \
        sed 's/^[[:space:]]*//' | \
        sort -u | \
        head -100

} > "$PYTHON_OUTPUT_DIR/functions.txt"

echo -e "${GREEN}[OK]${NC} Function summary generated"

# =============================================================================
# Summary
# =============================================================================

echo ""
echo -e "${GREEN}[OK]${NC} Python call graph analysis complete:"

if [ -f "$PYTHON_OUTPUT_DIR/call-graph.svg" ]; then
    echo "  - $PYTHON_OUTPUT_DIR/call-graph.svg (visual graph)"
fi
if [ -f "$PYTHON_OUTPUT_DIR/call-graph.dot" ]; then
    echo "  - $PYTHON_OUTPUT_DIR/call-graph.dot (DOT source)"
fi
echo "  - $PYTHON_OUTPUT_DIR/functions.txt (function list)"
echo ""
