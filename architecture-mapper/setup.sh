#!/bin/bash
# =============================================================================
# Architecture Mapper - Setup Script
# =============================================================================
# Installs all dependencies for the architecture mapper toolset.
# Uses uv for Python dependencies (in a virtual environment).
#
# Usage: ./setup.sh

set -e

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
echo -e "${BOLD}║          Architecture Mapper - Setup                        ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# =============================================================================
# Check for Homebrew (macOS)
# =============================================================================

BREW_AVAILABLE=false
if command -v brew &> /dev/null; then
    BREW_AVAILABLE=true
    echo -e "${GREEN}[OK]${NC} Homebrew found"
else
    echo -e "${YELLOW}[WARN]${NC} Homebrew not found - install system tools manually"
fi

# =============================================================================
# Install System Dependencies (via Homebrew)
# =============================================================================

echo ""
echo -e "${BOLD}System Dependencies${NC}"
echo ""

SYSTEM_TOOLS=("scc" "graphviz" "gource" "ffmpeg")
MISSING_TOOLS=()

for tool in "${SYSTEM_TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo -e "${GREEN}[OK]${NC} $tool installed"
    else
        echo -e "${YELLOW}[MISSING]${NC} $tool"
        MISSING_TOOLS+=("$tool")
    fi
done

if [ ${#MISSING_TOOLS[@]} -gt 0 ] && [ "$BREW_AVAILABLE" = true ]; then
    echo ""
    read -p "Install missing system tools via Homebrew? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for tool in "${MISSING_TOOLS[@]}"; do
            echo -n "  Installing $tool... "
            if brew install "$tool" -q 2>/dev/null; then
                echo -e "${GREEN}done${NC}"
            else
                echo -e "${YELLOW}failed${NC}"
            fi
        done
    fi
fi

# =============================================================================
# Install uv (if not present)
# =============================================================================

echo ""
echo -e "${BOLD}Python Environment (uv)${NC}"
echo ""

if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}[MISSING]${NC} uv not found"

    if [ "$BREW_AVAILABLE" = true ]; then
        read -p "Install uv via Homebrew? [y/N] " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -n "  Installing uv... "
            if brew install uv -q 2>/dev/null; then
                echo -e "${GREEN}done${NC}"
            else
                echo -e "${YELLOW}failed${NC}"
                echo ""
                echo "Install uv manually: https://docs.astral.sh/uv/getting-started/installation/"
                exit 1
            fi
        else
            echo ""
            echo "Install uv manually: https://docs.astral.sh/uv/getting-started/installation/"
            exit 1
        fi
    else
        echo "Install uv: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
else
    echo -e "${GREEN}[OK]${NC} uv found: $(uv --version)"
fi

# =============================================================================
# Create Virtual Environment and Install Python Tools
# =============================================================================

echo ""
echo -e "${BOLD}Creating Python Virtual Environment${NC}"
echo ""

VENV_DIR="$SCRIPT_DIR/.venv"

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -n "  Creating venv... "
    uv venv "$VENV_DIR" 2>/dev/null
    echo -e "${GREEN}done${NC}"
else
    echo -e "${GREEN}[OK]${NC} venv already exists"
fi

# Install Python dependencies
echo ""
echo -e "${BOLD}Installing Python Dependencies${NC}"
echo ""

PYTHON_DEPS=("pydeps" "pyan3")

for dep in "${PYTHON_DEPS[@]}"; do
    echo -n "  Installing $dep... "
    if uv pip install --python "$VENV_DIR/bin/python" "$dep" -q 2>/dev/null; then
        echo -e "${GREEN}done${NC}"
    else
        echo -e "${YELLOW}failed${NC}"
    fi
done

# =============================================================================
# Verify Installation
# =============================================================================

echo ""
echo -e "${BOLD}Verifying Installation${NC}"
echo ""

# Activate venv for verification
source "$VENV_DIR/bin/activate"

if command -v pydeps &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} pydeps available"
else
    echo -e "${YELLOW}[WARN]${NC} pydeps not found in venv"
fi

if command -v pyan3 &> /dev/null || command -v pyan &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} pyan3 available"
else
    echo -e "${YELLOW}[WARN]${NC} pyan3 not found in venv"
fi

deactivate 2>/dev/null || true

# =============================================================================
# Summary
# =============================================================================

echo ""
echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║                    Setup Complete                           ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo "Virtual environment created at: $VENV_DIR"
echo ""
echo "To run the analysis suite:"
echo ""
echo "  ./run-all.sh /path/to/repo"
echo ""
echo "The scripts will automatically use the virtual environment."
echo ""

# Check for optional tools
echo -e "${BOLD}Optional Tools:${NC}"
echo ""

if [ -n "$CODE_MAAT_JAR" ] && [ -f "$CODE_MAAT_JAR" ]; then
    echo -e "${GREEN}[OK]${NC} code-maat jar found at \$CODE_MAAT_JAR"
elif command -v docker &> /dev/null && docker image inspect adamtornhill/code-maat &> /dev/null 2>&1; then
    echo -e "${GREEN}[OK]${NC} code-maat docker image available"
else
    echo -e "${YELLOW}[INFO]${NC} code-maat not configured"
    echo "       For full git analysis, either:"
    echo "       - Set CODE_MAAT_JAR=/path/to/code-maat.jar"
    echo "       - Or: docker pull adamtornhill/code-maat"
fi

if command -v claude &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} Claude CLI available"
else
    echo -e "${YELLOW}[INFO]${NC} Claude CLI not found"
    echo "       LLM-powered documentation will be skipped"
fi

echo ""
