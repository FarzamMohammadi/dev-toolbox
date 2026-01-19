#!/bin/bash
# =============================================================================
# Git Statistics Analyzer
# =============================================================================
# Analyzes git history to identify:
# - Hotspots: Files that change frequently
# - Temporal coupling: Files that change together
# - Code churn: Lines added/removed over time
# - Ownership: Who knows what code best
#
# Based on Adam Tornhill's "Your Code as a Crime Scene" methodology
#
# Requirements:
#   - code-maat (Java jar or Docker)
#   - OR runs simplified analysis with git commands if code-maat unavailable
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
# Arguments
# =============================================================================

TARGET_REPO="${1:-.}"
OUTPUT_DIR="${2:-./output}"

# Resolve to absolute paths
TARGET_REPO="$(cd "$TARGET_REPO" && pwd)"
mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"

# Create git-analysis subdirectory
GIT_OUTPUT_DIR="$OUTPUT_DIR/git-analysis"
mkdir -p "$GIT_OUTPUT_DIR"

echo ""
echo -e "${BOLD}Git Statistics Analyzer${NC}"
echo "========================"
echo ""
echo "Target: $TARGET_REPO"
echo "Output: $GIT_OUTPUT_DIR"
echo ""

# =============================================================================
# Verify git repository
# =============================================================================

if [ ! -d "$TARGET_REPO/.git" ]; then
    echo -e "${RED}[ERROR]${NC} Not a git repository: $TARGET_REPO"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Git repository found"
echo ""

# =============================================================================
# Check for code-maat
# =============================================================================

CODE_MAAT_CMD=""

# Check for code-maat jar
if [ -n "$CODE_MAAT_JAR" ] && [ -f "$CODE_MAAT_JAR" ]; then
    CODE_MAAT_CMD="java -jar $CODE_MAAT_JAR"
    echo -e "${GREEN}[OK]${NC} code-maat jar found: $CODE_MAAT_JAR"
# Check for docker
elif command -v docker &> /dev/null && docker image inspect adamtornhill/code-maat &> /dev/null; then
    CODE_MAAT_CMD="docker run --rm -v $TARGET_REPO:/data -v $GIT_OUTPUT_DIR:/output adamtornhill/code-maat"
    echo -e "${GREEN}[OK]${NC} code-maat docker image found"
else
    echo -e "${YELLOW}[WARN]${NC} code-maat not found - running simplified analysis"
    echo ""
    echo "For full analysis, install code-maat:"
    echo "  Option 1: Set CODE_MAAT_JAR environment variable to jar path"
    echo "  Option 2: docker pull adamtornhill/code-maat"
    echo ""
fi

# =============================================================================
# Generate git log
# =============================================================================

echo "Generating git log..."
cd "$TARGET_REPO"

# Generate git log in code-maat format
git log --all --numstat --date=short \
    --pretty=format:'--%h--%ad--%aN' \
    --no-renames \
    > "$GIT_OUTPUT_DIR/gitlog.log" 2>/dev/null

COMMIT_COUNT=$(grep -c "^--" "$GIT_OUTPUT_DIR/gitlog.log" || echo "0")
echo -e "${GREEN}[OK]${NC} Git log generated ($COMMIT_COUNT commits)"
echo ""

# =============================================================================
# Run Analysis
# =============================================================================

if [ -n "$CODE_MAAT_CMD" ]; then
    echo "Running code-maat analysis..."
    echo ""

    # File revision frequency
    echo -n "  Analyzing revisions... "
    $CODE_MAAT_CMD -l "$GIT_OUTPUT_DIR/gitlog.log" -c git2 -a revisions \
        > "$GIT_OUTPUT_DIR/revisions.csv" 2>/dev/null
    echo -e "${GREEN}done${NC}"

    # Temporal coupling (files that change together)
    echo -n "  Analyzing coupling... "
    $CODE_MAAT_CMD -l "$GIT_OUTPUT_DIR/gitlog.log" -c git2 -a coupling \
        > "$GIT_OUTPUT_DIR/coupling.csv" 2>/dev/null
    echo -e "${GREEN}done${NC}"

    # Absolute churn (lines added/removed)
    echo -n "  Analyzing churn... "
    $CODE_MAAT_CMD -l "$GIT_OUTPUT_DIR/gitlog.log" -c git2 -a abs-churn \
        > "$GIT_OUTPUT_DIR/churn.csv" 2>/dev/null
    echo -e "${GREEN}done${NC}"

    # Entity ownership (primary authors)
    echo -n "  Analyzing ownership... "
    $CODE_MAAT_CMD -l "$GIT_OUTPUT_DIR/gitlog.log" -c git2 -a entity-ownership \
        > "$GIT_OUTPUT_DIR/ownership.csv" 2>/dev/null
    echo -e "${GREEN}done${NC}"

else
    # Simplified analysis using git commands
    echo "Running simplified git analysis..."
    echo ""

    # File revision frequency (most changed files)
    echo -n "  Analyzing revisions... "
    { echo "entity,n-revs"; git log --all --name-only --pretty=format: | \
        grep -v "^$" | \
        sort | \
        uniq -c | \
        sort -rn | \
        head -100 | \
        awk '{print $2","$1}'; } \
        > "$GIT_OUTPUT_DIR/revisions.csv"
    echo -e "${GREEN}done${NC}"

    # Churn analysis (lines changed per file)
    echo -n "  Analyzing churn... "
    { echo "entity,added,deleted"; git log --all --numstat --pretty=format: | \
        grep -v "^$" | \
        awk '{adds[$3]+=$1; dels[$3]+=$2} END {for (f in adds) print f","adds[f]","dels[f]}' | \
        sort -t',' -k2 -rn | \
        head -100; } \
        > "$GIT_OUTPUT_DIR/churn.csv"
    echo -e "${GREEN}done${NC}"

    # Author analysis (who changed what most)
    echo -n "  Analyzing ownership... "
    { echo "author,entity,commits"; git log --all --name-only --pretty=format:'%aN' | \
        awk '/^[^[:space:]]/ {author=$0; next} /^[[:space:]]*$/ {next} {print author","$0}' | \
        sort | \
        uniq -c | \
        sort -rn | \
        awk '{split($0, a, " "); author=a[2]; for(i=3;i<=NF;i++) author=author" "a[i]; print author}' | \
        head -200; } \
        > "$GIT_OUTPUT_DIR/ownership.csv"
    echo -e "${GREEN}done${NC}"

    # Note: Coupling analysis requires code-maat
    echo ""
    echo -e "${YELLOW}[NOTE]${NC} Temporal coupling analysis requires code-maat"
fi

# =============================================================================
# Generate Hotspots Report
# =============================================================================

echo ""
echo -e "${BOLD}Top 20 Most Changed Files (Potential Hotspots):${NC}"
echo ""

if [ -f "$GIT_OUTPUT_DIR/revisions.csv" ]; then
    tail -n +2 "$GIT_OUTPUT_DIR/revisions.csv" | head -20 | \
        awk -F',' '{printf "  %3d changes: %s\n", $2, $1}'
fi

# =============================================================================
# Summary
# =============================================================================

echo ""
echo -e "${GREEN}[OK]${NC} Git analysis complete:"
echo "  - $GIT_OUTPUT_DIR/gitlog.log (raw git log)"
echo "  - $GIT_OUTPUT_DIR/revisions.csv (change frequency)"
echo "  - $GIT_OUTPUT_DIR/churn.csv (lines added/removed)"
echo "  - $GIT_OUTPUT_DIR/ownership.csv (author analysis)"
if [ -n "$CODE_MAAT_CMD" ]; then
    echo "  - $GIT_OUTPUT_DIR/coupling.csv (temporal coupling)"
fi
echo ""
