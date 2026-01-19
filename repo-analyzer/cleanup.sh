#!/bin/bash
# =============================================================================
# Repo Analyzer - Cleanup Script
# =============================================================================
# Removes all dependencies installed by setup.sh.
# Offers interactive prompts before removing each component.
#
# Usage: ./cleanup.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║                Repo Analyzer - Cleanup                      ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# =============================================================================
# Confirmation
# =============================================================================

echo -e "${YELLOW}[WARN]${NC} This will remove installed dependencies."
echo ""
echo "Components that may be removed:"
echo "  - Python virtual environment (.venv)"
echo "  - Output directory (output/)"
echo "  - Homebrew packages: scc, graphviz, gource, ffmpeg, uv"
echo ""

read -p "Continue with cleanup? [y/N] " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Cleanup cancelled."
    exit 0
fi

echo ""

# Track what was removed
REMOVED=()
SKIPPED=()

# =============================================================================
# Remove Python Virtual Environment
# =============================================================================

echo -e "${BOLD}Python Virtual Environment${NC}"
echo ""

VENV_DIR="$SCRIPT_DIR/.venv"

if [ -d "$VENV_DIR" ]; then
    read -p "Remove Python virtual environment (.venv)? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -n "  Removing .venv... "
        rm -rf "$VENV_DIR"
        echo -e "${GREEN}done${NC}"
        REMOVED+=(".venv")
    else
        echo -e "  ${YELLOW}Skipped${NC}"
        SKIPPED+=(".venv")
    fi
else
    echo -e "${GREEN}[OK]${NC} .venv not present (already clean)"
fi

# =============================================================================
# Remove Output Directory
# =============================================================================

echo ""
echo -e "${BOLD}Output Directory${NC}"
echo ""

OUTPUT_DIR="$SCRIPT_DIR/output"

if [ -d "$OUTPUT_DIR" ]; then
    read -p "Remove output directory? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -n "  Removing output/... "
        rm -rf "$OUTPUT_DIR"
        echo -e "${GREEN}done${NC}"
        REMOVED+=("output/")
    else
        echo -e "  ${YELLOW}Skipped${NC}"
        SKIPPED+=("output/")
    fi
else
    echo -e "${GREEN}[OK]${NC} output/ not present (already clean)"
fi

# =============================================================================
# Uninstall Homebrew Packages
# =============================================================================

echo ""
echo -e "${BOLD}Homebrew Packages${NC}"
echo ""

BREW_AVAILABLE=false
if command -v brew &> /dev/null; then
    BREW_AVAILABLE=true
fi

if [ "$BREW_AVAILABLE" = false ]; then
    echo -e "${YELLOW}[WARN]${NC} Homebrew not found - skipping package removal"
else
    # Packages installed by setup.sh
    BREW_PACKAGES=("scc" "graphviz" "gource" "ffmpeg" "uv")

    echo "The following packages were installed by setup.sh."
    echo "You may want to keep some if used by other tools."
    echo ""

    for pkg in "${BREW_PACKAGES[@]}"; do
        if brew list "$pkg" &> /dev/null; then
            read -p "Uninstall $pkg? [y/N] " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo -n "  Uninstalling $pkg... "
                if brew uninstall "$pkg" -q 2>/dev/null; then
                    echo -e "${GREEN}done${NC}"
                    REMOVED+=("$pkg")
                else
                    echo -e "${YELLOW}failed${NC}"
                fi
            else
                echo -e "  ${YELLOW}Skipped${NC}"
                SKIPPED+=("$pkg")
            fi
        else
            echo -e "${GREEN}[OK]${NC} $pkg not installed (already clean)"
        fi
    done
fi

# =============================================================================
# Summary
# =============================================================================

echo ""
echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║                   Cleanup Complete                          ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ ${#REMOVED[@]} -gt 0 ]; then
    echo -e "${GREEN}Removed:${NC}"
    for item in "${REMOVED[@]}"; do
        echo "  - $item"
    done
    echo ""
fi

if [ ${#SKIPPED[@]} -gt 0 ]; then
    echo -e "${YELLOW}Skipped:${NC}"
    for item in "${SKIPPED[@]}"; do
        echo "  - $item"
    done
    echo ""
fi

if [ ${#REMOVED[@]} -eq 0 ] && [ ${#SKIPPED[@]} -eq 0 ]; then
    echo "Nothing to clean up - environment was already clean."
    echo ""
fi

echo "To reinstall, run: ./setup.sh"
echo ""
