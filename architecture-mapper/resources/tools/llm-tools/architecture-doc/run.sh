#!/bin/bash
# =============================================================================
# LLM Architecture Documentation Generator
# =============================================================================
# Uses Claude CLI to generate architecture.md from codebase analysis.
#
# Requirements: Claude CLI (claude command available)
# Usage: ./run.sh <target_repo> <output_dir>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAPPER_ROOT="$(dirname "$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")")"

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
echo -e "${BOLD}LLM Architecture Documentation Generator${NC}"
echo "=========================================="
echo ""
echo "Target: $TARGET_REPO"
echo "Output: $OUTPUT_DIR"
echo ""

# =============================================================================
# Check for Claude CLI
# =============================================================================

if ! command -v claude &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Claude CLI is not installed or not in PATH"
    echo ""
    echo "Install Claude CLI and ensure 'claude' command is available"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Claude CLI found"
echo ""

# =============================================================================
# Collect Context
# =============================================================================

# Use env vars from orchestrator or defaults
LLM_CONTEXT_DEPTH="${LLM_CONTEXT_DEPTH:-3}"
LLM_FILE_LIMIT="${LLM_FILE_LIMIT:-100}"

echo "Collecting codebase context..."

CONTEXT_FILE=$(mktemp)

{
    echo "# Codebase Analysis Context"
    echo ""
    echo "## Target Repository"
    echo "Path: $TARGET_REPO"
    echo ""

    # Directory structure
    echo "## Directory Structure"
    echo '```'
    if command -v tree &> /dev/null; then
        tree "$TARGET_REPO" -L "$LLM_CONTEXT_DEPTH" \
            -I 'node_modules|.git|__pycache__|*.pyc|.venv|venv|.env|dist|build|.next|.cache|coverage' \
            --dirsfirst 2>/dev/null | head -"$LLM_FILE_LIMIT"
    else
        find "$TARGET_REPO" -maxdepth "$LLM_CONTEXT_DEPTH" \
            -not -path '*/.git/*' \
            -not -path '*/node_modules/*' \
            -not -path '*/__pycache__/*' \
            2>/dev/null | head -"$LLM_FILE_LIMIT"
    fi
    echo '```'
    echo ""

    # README if exists
    if [ -f "$TARGET_REPO/README.md" ]; then
        echo "## README.md"
        echo '```markdown'
        head -"$LLM_FILE_LIMIT" "$TARGET_REPO/README.md"
        echo '```'
        echo ""
    fi

    # Package info (Python)
    if [ -f "$TARGET_REPO/pyproject.toml" ]; then
        echo "## pyproject.toml"
        echo '```toml'
        head -50 "$TARGET_REPO/pyproject.toml"
        echo '```'
        echo ""
    elif [ -f "$TARGET_REPO/setup.py" ]; then
        echo "## setup.py"
        echo '```python'
        head -50 "$TARGET_REPO/setup.py"
        echo '```'
        echo ""
    fi

    # Package info (Node.js)
    if [ -f "$TARGET_REPO/package.json" ]; then
        echo "## package.json"
        echo '```json'
        head -50 "$TARGET_REPO/package.json"
        echo '```'
        echo ""
    fi

    # Go modules
    if [ -f "$TARGET_REPO/go.mod" ]; then
        echo "## go.mod"
        echo '```'
        cat "$TARGET_REPO/go.mod"
        echo '```'
        echo ""
    fi

    # Rust cargo
    if [ -f "$TARGET_REPO/Cargo.toml" ]; then
        echo "## Cargo.toml"
        echo '```toml'
        head -50 "$TARGET_REPO/Cargo.toml"
        echo '```'
        echo ""
    fi

    # Entry points
    echo "## Detected Entry Points"
    for pattern in "main.py" "app.py" "__main__.py" "index.js" "index.ts" "main.go" "main.rs"; do
        found=$(find "$TARGET_REPO" -name "$pattern" \
            -not -path '*/.git/*' \
            -not -path '*/node_modules/*' \
            2>/dev/null | head -3)
        if [ -n "$found" ]; then
            echo "- $pattern found:"
            echo "$found" | while read f; do
                echo "  - ${f#$TARGET_REPO/}"
            done
        fi
    done
    echo ""

    # Include code stats if available
    if [ -f "$OUTPUT_DIR/code-stats.json" ]; then
        echo "## Code Statistics (from scc)"
        echo '```json'
        head -100 "$OUTPUT_DIR/code-stats.json"
        echo '```'
        echo ""
    fi

    # Include hotspots if available
    if [ -f "$OUTPUT_DIR/git-analysis/revisions.csv" ]; then
        echo "## Top Changed Files (Git Hotspots)"
        echo '```csv'
        head -25 "$OUTPUT_DIR/git-analysis/revisions.csv"
        echo '```'
        echo ""
    fi

    # Include pattern analysis if available
    if [ -f "$OUTPUT_DIR/python/patterns.json" ]; then
        echo "## Detected Patterns (Python AST Analysis)"
        echo '```json'
        head -100 "$OUTPUT_DIR/python/patterns.json"
        echo '```'
        echo ""
    fi

} > "$CONTEXT_FILE"

echo -e "${GREEN}[OK]${NC} Context collected"
echo ""

# =============================================================================
# Generate Architecture Doc with Claude
# =============================================================================

echo "Generating architecture documentation with Claude..."
echo "(This may take a moment)"
echo ""

PROMPT="Based on the codebase analysis context provided, generate a comprehensive architecture.md document.

The document should include:
1. A brief project overview (purpose, key features)
2. Technology stack summary
3. High-level architecture description
4. Directory structure explanation (what each major directory contains)
5. Core components and their responsibilities
6. Data flow (how data moves through the system)
7. Key patterns used (based on detected patterns or inferred from structure)
8. External dependencies summary
9. Entry points and how to run/deploy

Format the output as a proper markdown document that could be placed in the project root.
Focus on being concise but informative - this is meant to help new developers quickly understand the codebase.

If certain information is not available from the context, make reasonable inferences based on common patterns,
or note that the section would need manual input.

IMPORTANT: Output ONLY the markdown document content. Do not include any preamble or explanation."

# Use Claude CLI to generate the doc
# Pass the context file as input and the prompt
cat "$CONTEXT_FILE" | claude --print "$PROMPT" > "$OUTPUT_DIR/architecture.md" 2>/dev/null || {
    echo -e "${YELLOW}[WARN]${NC} Claude CLI failed, trying alternative approach..."

    # Alternative: If claude CLI has different syntax
    claude --print "$PROMPT" < "$CONTEXT_FILE" > "$OUTPUT_DIR/architecture.md" 2>/dev/null || {
        echo -e "${RED}[ERROR]${NC} Failed to generate architecture doc with Claude"
        echo "       You may need to run Claude manually with the context"
        echo "       Context saved to: $CONTEXT_FILE"
        exit 1
    }
}

# Clean up
rm -f "$CONTEXT_FILE"

# =============================================================================
# Summary
# =============================================================================

if [ -f "$OUTPUT_DIR/architecture.md" ]; then
    DOC_LINES=$(wc -l < "$OUTPUT_DIR/architecture.md" | tr -d ' ')
    echo ""
    echo -e "${GREEN}[OK]${NC} Architecture documentation generated:"
    echo "  - $OUTPUT_DIR/architecture.md ($DOC_LINES lines)"
    echo ""
    echo "Review and refine the generated document as needed."
else
    echo -e "${RED}[ERROR]${NC} Failed to generate architecture documentation"
    exit 1
fi

echo ""
