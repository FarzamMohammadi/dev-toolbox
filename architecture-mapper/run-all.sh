#!/bin/bash
# =============================================================================
# Architecture Mapper - Full Analysis Suite
# =============================================================================
# Runs all available analyzers on a target repository and generates
# comprehensive architecture documentation.
#
# Usage: ./run-all.sh [target_repo] [output_dir]
#
# Arguments:
#   target_repo  - Path to repository to analyze (default: current directory)
#   output_dir   - Where to save results (default: ./output)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# =============================================================================
# Load Configuration
# =============================================================================

# Source config.sh if present (provides defaults for all tools)
if [ -f "$SCRIPT_DIR/config.sh" ]; then
    source "$SCRIPT_DIR/config.sh"
fi

# Set defaults for any unset variables
PROJECT_NAME="${PROJECT_NAME:-}"
MAX_DEPTH="${MAX_DEPTH:-4}"
EXCLUDE_DIRS="${EXCLUDE_DIRS:-.git node_modules .venv venv __pycache__ dist build .next .cache coverage}"
GOURCE_RESOLUTION="${GOURCE_RESOLUTION:-800x600}"
GOURCE_SECONDS_PER_DAY="${GOURCE_SECONDS_PER_DAY:-0.5}"
GOURCE_VIDEO_DURATION="${GOURCE_VIDEO_DURATION:-60}"
GOURCE_LIVE_PREVIEW="${GOURCE_LIVE_PREVIEW:-false}"
CODE_MAAT_JAR="${CODE_MAAT_JAR:-}"
PYTHON_SRC_DIRS="${PYTHON_SRC_DIRS:-src lib app .}"
PYTHON_MAX_FILES="${PYTHON_MAX_FILES:-100}"
LLM_CONTEXT_DEPTH="${LLM_CONTEXT_DEPTH:-3}"
LLM_FILE_LIMIT="${LLM_FILE_LIMIT:-100}"

# Export for child scripts
export PROJECT_NAME MAX_DEPTH EXCLUDE_DIRS
export GOURCE_RESOLUTION GOURCE_SECONDS_PER_DAY GOURCE_VIDEO_DURATION GOURCE_LIVE_PREVIEW
export CODE_MAAT_JAR
export PYTHON_SRC_DIRS PYTHON_MAX_FILES
export LLM_CONTEXT_DEPTH LLM_FILE_LIMIT

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# =============================================================================
# Arguments
# =============================================================================

TARGET_REPO="${1:-.}"
OUTPUT_DIR="${2:-$SCRIPT_DIR/output}"

# Resolve to absolute paths
if [ -d "$TARGET_REPO" ]; then
    TARGET_REPO="$(cd "$TARGET_REPO" && pwd)"
else
    echo -e "${RED}[ERROR]${NC} Target repository not found: $TARGET_REPO"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"

echo ""
echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║          Architecture Mapper - Full Analysis Suite         ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Target:${NC} $TARGET_REPO"
echo -e "${BLUE}Output:${NC} $OUTPUT_DIR"
echo ""

# =============================================================================
# Auto-Setup (run setup.sh if needed)
# =============================================================================

# Check if venv exists and key tools available
NEEDS_SETUP=false

if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    NEEDS_SETUP=true
fi

if ! command -v scc &> /dev/null; then
    NEEDS_SETUP=true
fi

if [ "$NEEDS_SETUP" = true ]; then
    echo -e "${YELLOW}[SETUP]${NC} Dependencies missing - running setup..."
    echo ""
    if [ -f "$SCRIPT_DIR/setup.sh" ]; then
        bash "$SCRIPT_DIR/setup.sh"
        echo ""
    else
        echo -e "${RED}[ERROR]${NC} setup.sh not found"
        exit 1
    fi
fi

# =============================================================================
# Helper Functions
# =============================================================================

run_analyzer() {
    local name="$1"
    local script="$2"

    if [ -f "$script" ]; then
        echo ""
        echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BLUE}▶ Running:${NC} $name"
        echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

        if bash "$script" "$TARGET_REPO" "$OUTPUT_DIR"; then
            echo -e "${GREEN}✓${NC} $name completed"
        else
            echo -e "${YELLOW}⚠${NC} $name had warnings or errors"
        fi
    else
        echo -e "${YELLOW}[SKIP]${NC} $name - script not found: $script"
    fi
}

# =============================================================================
# Phase 1: Core Statistics (Language-Agnostic)
# =============================================================================

echo ""
echo -e "${BOLD}Phase 1: Core Statistics${NC}"
echo ""

# Code statistics
run_analyzer "Code Statistics (scc)" "$SCRIPT_DIR/resources/tools/analyzers/common/code-stats/run.sh"

# Directory structure
run_analyzer "Directory Structure" "$SCRIPT_DIR/resources/tools/analyzers/common/structure/run.sh"

# Git analysis
run_analyzer "Git Statistics" "$SCRIPT_DIR/resources/tools/analyzers/common/git-stats/run.sh"

# =============================================================================
# Phase 2: Language-Specific Analysis
# =============================================================================

echo ""
echo -e "${BOLD}Phase 2: Language-Specific Analysis${NC}"
echo ""

# Detect Python
PYTHON_FILES=$(find "$TARGET_REPO" -name "*.py" \
    -not -path "*/.git/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/.venv/*" \
    -not -path "*/venv/*" \
    2>/dev/null | head -5)

if [ -n "$PYTHON_FILES" ]; then
    echo -e "${GREEN}[OK]${NC} Python detected"

    # Python dependencies
    run_analyzer "Python Dependencies (pydeps)" "$SCRIPT_DIR/resources/tools/analyzers/python/dependencies/run.sh"

    # Python call graph
    run_analyzer "Python Call Graph (pyan)" "$SCRIPT_DIR/resources/tools/analyzers/python/call-graph/run.sh"

    # Python AST patterns
    if [ -f "$SCRIPT_DIR/resources/tools/analyzers/python/ast-patterns/analyze.py" ]; then
        echo ""
        echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BLUE}▶ Running:${NC} Python AST Pattern Analysis"
        echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

        # Use venv python if available, otherwise system python3
        PYTHON_CMD="python3"
        if [ -f "$SCRIPT_DIR/.venv/bin/python" ]; then
            PYTHON_CMD="$SCRIPT_DIR/.venv/bin/python"
        fi

        if $PYTHON_CMD "$SCRIPT_DIR/resources/tools/analyzers/python/ast-patterns/analyze.py" "$TARGET_REPO" "$OUTPUT_DIR"; then
            echo -e "${GREEN}✓${NC} Python AST analysis completed"
        else
            echo -e "${YELLOW}⚠${NC} Python AST analysis had errors"
        fi
    fi
else
    echo -e "${YELLOW}[SKIP]${NC} Python analysis - no Python files detected"
fi

# Detect JavaScript/TypeScript (placeholder for future)
JS_FILES=$(find "$TARGET_REPO" -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" \
    -not -path "*/.git/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/dist/*" \
    -not -path "*/build/*" \
    2>/dev/null | head -5)

if [ -n "$JS_FILES" ]; then
    echo -e "${YELLOW}[NOTE]${NC} JavaScript/TypeScript detected - language-specific analysis coming soon"
fi

# Detect Go (placeholder for future)
GO_FILES=$(find "$TARGET_REPO" -name "*.go" \
    -not -path "*/.git/*" \
    2>/dev/null | head -5)

if [ -n "$GO_FILES" ]; then
    echo -e "${YELLOW}[NOTE]${NC} Go detected - language-specific analysis coming soon"
fi

# =============================================================================
# Phase 3: LLM-Powered Analysis (Optional)
# =============================================================================

echo ""
echo -e "${BOLD}Phase 3: LLM-Powered Analysis${NC}"
echo ""

if command -v claude &> /dev/null; then
    run_analyzer "LLM Architecture Doc" "$SCRIPT_DIR/resources/tools/llm-tools/architecture-doc/run.sh"
else
    echo -e "${YELLOW}[SKIP]${NC} LLM analysis - Claude CLI not found"
    echo "       Install Claude CLI for auto-generated architecture documentation"
fi

# =============================================================================
# Phase 4: Visualization
# =============================================================================

echo ""
echo -e "${BOLD}Phase 4: Visualization${NC}"
echo ""

if command -v gource &> /dev/null; then
    run_analyzer "Git Visualization (gource)" "$SCRIPT_DIR/resources/tools/visualizers/git-visualizer/run.sh"
else
    echo -e "${YELLOW}[SKIP]${NC} Git visualization - gource not installed"
    echo "       Install with: brew install gource ffmpeg"
fi

# =============================================================================
# Summary
# =============================================================================

echo ""
echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║                    Analysis Complete                        ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}Output Directory:${NC} $OUTPUT_DIR"
echo ""

# List generated files
if [ -d "$OUTPUT_DIR" ]; then
    echo "Generated files:"
    echo ""

    # Core files
    for f in code-stats.json code-stats.html structure.txt structure.json architecture.md; do
        if [ -f "$OUTPUT_DIR/$f" ]; then
            size=$(du -h "$OUTPUT_DIR/$f" 2>/dev/null | cut -f1)
            printf "  ${GREEN}✓${NC} %-30s %s\n" "$f" "$size"
        fi
    done

    # Git analysis
    if [ -d "$OUTPUT_DIR/git-analysis" ]; then
        echo ""
        echo "  git-analysis/"
        for f in "$OUTPUT_DIR/git-analysis"/*; do
            if [ -f "$f" ]; then
                fname=$(basename "$f")
                size=$(du -h "$f" 2>/dev/null | cut -f1)
                printf "    ${GREEN}✓${NC} %-28s %s\n" "$fname" "$size"
            fi
        done
    fi

    # Python analysis
    if [ -d "$OUTPUT_DIR/python" ]; then
        echo ""
        echo "  python/"
        for f in "$OUTPUT_DIR/python"/*; do
            if [ -f "$f" ]; then
                fname=$(basename "$f")
                size=$(du -h "$f" 2>/dev/null | cut -f1)
                printf "    ${GREEN}✓${NC} %-28s %s\n" "$fname" "$size"
            fi
        done
    fi

    # Gource visualization
    if [ -d "$OUTPUT_DIR/repo-evolution" ]; then
        echo ""
        echo "  repo-evolution/"
        for f in "$OUTPUT_DIR/repo-evolution"/*; do
            if [ -f "$f" ]; then
                fname=$(basename "$f")
                size=$(du -h "$f" 2>/dev/null | cut -f1)
                printf "    ${GREEN}✓${NC} %-28s %s\n" "$fname" "$size"
            fi
        done
    fi
fi

echo ""
echo -e "${GREEN}Done!${NC} Review the output files to understand the codebase architecture."
echo ""

# Quick tips
echo -e "${BOLD}Quick Start:${NC}"
echo "  - Open code-stats.html in a browser for visual code statistics"
echo "  - Check git-analysis/revisions.csv for hotspots (most changed files)"
echo "  - Review architecture.md for AI-generated documentation (if generated)"
echo "  - Watch repo-evolution/history.mp4 for animated git history visualization"
echo ""
