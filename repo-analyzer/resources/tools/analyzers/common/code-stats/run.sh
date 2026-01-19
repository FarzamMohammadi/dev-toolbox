#!/bin/bash
# =============================================================================
# Code Statistics Analyzer
# =============================================================================
# Uses scc (Sloc, Cloc and Code) for fast, accurate code statistics
# including lines of code, complexity, and COCOMO estimates.
#
# Requirements: scc (brew install scc)
# Usage: ./run.sh <target_repo> <output_dir>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

echo ""
echo -e "${BOLD}Code Statistics Analyzer${NC}"
echo "========================"
echo ""
echo "Target: $TARGET_REPO"
echo "Output: $OUTPUT_DIR"
echo ""

# =============================================================================
# Check for scc
# =============================================================================

if ! command -v scc &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} scc is not installed"
    echo ""
    echo "Install with:"
    echo "  brew install scc"
    echo ""
    echo "Or visit: https://github.com/boyter/scc"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} scc found: $(scc --version 2>&1 | head -1)"
echo ""

# =============================================================================
# Run Analysis
# =============================================================================

echo "Analyzing code statistics..."
echo ""

# JSON output for programmatic use
echo -n "  Generating JSON... "
scc "$TARGET_REPO" --format json > "$OUTPUT_DIR/code-stats.json" 2>/dev/null
echo -e "${GREEN}done${NC}"

# HTML output for visual report
echo -n "  Generating HTML... "
scc "$TARGET_REPO" --format html > "$OUTPUT_DIR/code-stats.html" 2>/dev/null
echo -e "${GREEN}done${NC}"

# Also generate a summary to stdout
echo ""
echo -e "${BOLD}Summary:${NC}"
echo ""
scc "$TARGET_REPO" --no-cocomo 2>/dev/null

# =============================================================================
# Summary
# =============================================================================

echo ""
echo -e "${GREEN}[OK]${NC} Code statistics generated:"
echo "  - $OUTPUT_DIR/code-stats.json"
echo "  - $OUTPUT_DIR/code-stats.html"
echo ""
