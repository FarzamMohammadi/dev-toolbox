#!/bin/bash
# =============================================================================
# Directory Structure Analyzer
# =============================================================================
# Analyzes and documents project directory structure:
# - Tree generation with depth control
# - File type distribution
# - Entry point detection
# - JSON output for programmatic use
#
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
# Arguments & Configuration
# =============================================================================

TARGET_REPO="${1:-.}"
OUTPUT_DIR="${2:-./output}"

# Use env var from orchestrator, then arg, then default
MAX_DEPTH="${MAX_DEPTH:-${3:-4}}"
EXCLUDE_DIRS="${EXCLUDE_DIRS:-.git node_modules .venv venv __pycache__ dist build .next .cache coverage}"

# Resolve to absolute paths
TARGET_REPO="$(cd "$TARGET_REPO" && pwd)"
mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"

echo ""
echo -e "${BOLD}Directory Structure Analyzer${NC}"
echo "============================="
echo ""
echo "Target: $TARGET_REPO"
echo "Output: $OUTPUT_DIR"
echo "Max Depth: $MAX_DEPTH"
echo ""

# =============================================================================
# Generate Tree
# =============================================================================

echo "Generating directory tree..."

# Convert EXCLUDE_DIRS to tree -I pattern (space-separated to pipe-separated)
TREE_EXCLUDE=$(echo "$EXCLUDE_DIRS" | tr ' ' '|')

# Use tree if available, otherwise use find
if command -v tree &> /dev/null; then
    tree "$TARGET_REPO" -L "$MAX_DEPTH" \
        -I "$TREE_EXCLUDE" \
        --dirsfirst \
        > "$OUTPUT_DIR/structure.txt" 2>/dev/null
    echo -e "${GREEN}[OK]${NC} Tree generated using 'tree' command"
else
    # Fallback to find
    echo "# Directory Structure" > "$OUTPUT_DIR/structure.txt"
    echo "# Generated: $(date)" >> "$OUTPUT_DIR/structure.txt"
    echo "" >> "$OUTPUT_DIR/structure.txt"

    find "$TARGET_REPO" -maxdepth "$MAX_DEPTH" \
        -not -path '*/.git/*' \
        -not -path '*/node_modules/*' \
        -not -path '*/__pycache__/*' \
        -not -path '*/.venv/*' \
        -not -path '*/venv/*' \
        -not -path '*/dist/*' \
        -not -path '*/build/*' \
        -not -path '*/.next/*' \
        -not -name '*.pyc' \
        -print | \
        sed "s|$TARGET_REPO/||" | \
        sort >> "$OUTPUT_DIR/structure.txt"

    echo -e "${YELLOW}[OK]${NC} Tree generated using 'find' (install 'tree' for better output)"
fi

echo ""

# =============================================================================
# File Type Distribution
# =============================================================================

echo "Analyzing file types..."

# Count files by extension
cd "$TARGET_REPO"

echo '{' > "$OUTPUT_DIR/structure.json"
echo '  "generated": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",' >> "$OUTPUT_DIR/structure.json"
echo '  "target": "'$TARGET_REPO'",' >> "$OUTPUT_DIR/structure.json"

# File type counts
echo '  "file_types": {' >> "$OUTPUT_DIR/structure.json"

find . -type f \
    -not -path '*/.git/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/__pycache__/*' \
    -not -path '*/.venv/*' \
    -not -path '*/venv/*' \
    2>/dev/null | \
    sed 's/.*\.//' | \
    grep -v '/' | \
    sort | \
    uniq -c | \
    sort -rn | \
    head -20 | \
    awk 'BEGIN{first=1} {
        if (!first) printf ",\n"
        first=0
        gsub(/"/, "\\\"", $2)
        printf "    \"%s\": %d", $2, $1
    } END{print ""}' >> "$OUTPUT_DIR/structure.json"

echo '  },' >> "$OUTPUT_DIR/structure.json"

# =============================================================================
# Entry Points Detection
# =============================================================================

echo "Detecting entry points..."

echo '  "entry_points": [' >> "$OUTPUT_DIR/structure.json"

FIRST_ENTRY=true

# Common entry point patterns
ENTRY_PATTERNS=(
    "main.py"
    "app.py"
    "__main__.py"
    "index.js"
    "index.ts"
    "main.js"
    "main.ts"
    "server.js"
    "server.ts"
    "index.html"
    "main.go"
    "main.rs"
    "Program.cs"
    "Main.java"
    "Makefile"
    "setup.py"
    "pyproject.toml"
    "package.json"
    "Cargo.toml"
    "go.mod"
)

for pattern in "${ENTRY_PATTERNS[@]}"; do
    found=$(find . -name "$pattern" -not -path '*/.git/*' -not -path '*/node_modules/*' 2>/dev/null | head -5)
    if [ -n "$found" ]; then
        while IFS= read -r file; do
            if [ "$FIRST_ENTRY" = true ]; then
                FIRST_ENTRY=false
            else
                echo ',' >> "$OUTPUT_DIR/structure.json"
            fi
            # Clean up path
            clean_path=$(echo "$file" | sed 's|^\./||')
            printf '    "%s"' "$clean_path" >> "$OUTPUT_DIR/structure.json"
        done <<< "$found"
    fi
done

echo '' >> "$OUTPUT_DIR/structure.json"
echo '  ],' >> "$OUTPUT_DIR/structure.json"

# =============================================================================
# Directory Summary
# =============================================================================

echo "Generating directory summary..."

echo '  "directories": [' >> "$OUTPUT_DIR/structure.json"

# List top-level directories with file counts
find . -maxdepth 1 -type d \
    -not -name '.' \
    -not -name '.git' \
    -not -name 'node_modules' \
    -not -name '__pycache__' \
    -not -name '.venv' \
    -not -name 'venv' \
    2>/dev/null | \
sort | \
{
    first=true
    while IFS= read -r dir; do
        dir_name=$(basename "$dir")
        file_count=$(find "$dir" -type f 2>/dev/null | wc -l | tr -d ' ')

        if [ "$first" = true ]; then
            first=false
        else
            echo ',' >> "$OUTPUT_DIR/structure.json"
        fi
        printf '    {"name": "%s", "file_count": %d}' "$dir_name" "$file_count" >> "$OUTPUT_DIR/structure.json"
    done
}

echo '' >> "$OUTPUT_DIR/structure.json"
echo '  ]' >> "$OUTPUT_DIR/structure.json"
echo '}' >> "$OUTPUT_DIR/structure.json"

echo -e "${GREEN}[OK]${NC} Structure analysis complete"

# =============================================================================
# Summary Output
# =============================================================================

echo ""
echo -e "${BOLD}Directory Summary:${NC}"
echo ""

# Show top directories
find "$TARGET_REPO" -maxdepth 1 -type d \
    -not -name '.' \
    -not -name '.git' \
    -not -name 'node_modules' \
    -not -name '__pycache__' \
    2>/dev/null | \
while IFS= read -r dir; do
    dir_name=$(basename "$dir")
    file_count=$(find "$dir" -type f 2>/dev/null | wc -l | tr -d ' ')
    printf "  %-30s %5d files\n" "$dir_name/" "$file_count"
done | sort -t: -k2 -rn | head -15

echo ""
echo -e "${GREEN}[OK]${NC} Structure analysis complete:"
echo "  - $OUTPUT_DIR/structure.txt (tree view)"
echo "  - $OUTPUT_DIR/structure.json (structured data)"
echo ""
