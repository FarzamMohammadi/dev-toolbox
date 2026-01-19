#!/bin/bash
# =============================================================================
# Git Visualizer
# =============================================================================
# Generates animated repository history visualization using gource.
# This script handles everything: tool checking, installation prompts, and video generation.
#
# Configuration: ./config.sh
# Note: If video doesn't capture full git history, increase GOURCE_VIDEO_DURATION in config.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}========================================"
echo "Git Visualizer"
echo -e "========================================${NC}"
echo ""

# =============================================================================
# Step 1: Check configuration
# =============================================================================

if [ ! -f "config.sh" ]; then
    echo -e "${RED}[ERROR]${NC} config.sh not found."
    echo "        Create config.sh with your project settings."
    exit 1
fi

source config.sh
echo -e "${GREEN}[OK]${NC} Configuration loaded: $PROJECT_NAME"

# =============================================================================
# Step 2: Check required tools
# =============================================================================

echo ""
echo "Checking required tools..."
echo ""

GOURCE_OK=false
FFMPEG_OK=false

if command -v gource &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} gource is installed"
    GOURCE_OK=true
else
    echo -e "${YELLOW}[MISSING]${NC} gource is not installed"
fi

if command -v ffmpeg &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} ffmpeg is installed"
    FFMPEG_OK=true
else
    echo -e "${YELLOW}[MISSING]${NC} ffmpeg is not installed"
fi

# =============================================================================
# Step 3: Offer to install missing tools via Homebrew
# =============================================================================

MISSING_TOOLS=()
if [ "$GOURCE_OK" = false ]; then
    MISSING_TOOLS+=("gource")
fi
if [ "$FFMPEG_OK" = false ]; then
    MISSING_TOOLS+=("ffmpeg")
fi

if [ ${#MISSING_TOOLS[@]} -gt 0 ] && command -v brew &> /dev/null; then
    echo ""
    echo "-----------------------------------------"
    echo "The following tools are not installed:"
    echo ""
    for tool in "${MISSING_TOOLS[@]}"; do
        case "$tool" in
            gource)
                echo "  - gource (Required)"
                echo "    Creates animated visualization of git repository history"
                ;;
            ffmpeg)
                echo "  - ffmpeg (Required for video export)"
                echo "    Encodes gource output to .mp4 video"
                echo "    Without it: gource shows live preview only, cannot save video"
                ;;
        esac
        echo ""
    done
    read -p "Would you like to install them via Homebrew? [y/N] " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Installing tools..."
        for tool in "${MISSING_TOOLS[@]}"; do
            echo -n "  Installing $tool... "
            if brew install "$tool" -q 2>/dev/null; then
                echo -e "${GREEN}[OK]${NC}"
            else
                echo -e "${YELLOW}[FAILED]${NC}"
            fi
        done

        # Re-check tools after installation
        if command -v gource &> /dev/null; then
            GOURCE_OK=true
        fi
        if command -v ffmpeg &> /dev/null; then
            FFMPEG_OK=true
        fi
    else
        echo "Skipping tool installation."
    fi
elif [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}Note:${NC} Homebrew not found. Install missing tools manually:"
    echo "  brew install gource ffmpeg"
fi

# =============================================================================
# Step 4: Validate we can proceed
# =============================================================================

if [ "$GOURCE_OK" = false ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Gource is required but not installed."
    echo "        Install with: brew install gource"
    exit 1
fi

if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Not a git repository"
    exit 1
fi

# =============================================================================
# Step 5: Generate visualization
# =============================================================================

echo ""
echo -e "${BOLD}Generating repository visualization...${NC}"
echo ""

# Create output directory
OUTPUT_DIR="$SCRIPT_DIR/output/gource"
mkdir -p "$OUTPUT_DIR"

cd "$PROJECT_ROOT"

# Parse resolution
WIDTH=$(echo "$GOURCE_RESOLUTION" | cut -d'x' -f1)
HEIGHT=$(echo "$GOURCE_RESOLUTION" | cut -d'x' -f2)

# Common gource options
GOURCE_OPTS=(
    --title "$GOURCE_TITLE"
    --seconds-per-day "$GOURCE_SECONDS_PER_DAY"
    --auto-skip-seconds 0.5
    --file-idle-time 0
    --max-files 0
    --hide filenames,mouse
    --font-size 18
    --date-format "%Y-%m-%d"
    --background-colour 1a1a2e
    --font-colour 94b4c8
)

if [ "$GOURCE_LIVE_PREVIEW" = "true" ]; then
    echo "Starting live preview..."
    echo "(Close the window to exit)"
    echo ""

    gource "${GOURCE_OPTS[@]}" \
        -${WIDTH}x${HEIGHT} \
        "$PROJECT_ROOT"
else
    # Check for ffmpeg
    if [ "$FFMPEG_OK" = false ]; then
        echo -e "${YELLOW}[SKIP]${NC} FFmpeg not installed (required for video export)"
        echo "       Install with: brew install ffmpeg"
        echo "       Or set GOURCE_LIVE_PREVIEW=true in config.sh for live preview"
        exit 0
    fi

    OUTPUT_FILE="$OUTPUT_DIR/history.mp4"

    # Warn user about the window that will open
    echo -e "${RED}WARNING:${NC} A window will open to render the video."
    echo -e "         ${RED}DO NOT close the window!${NC} It is part of the generation process."
    echo "         (This is a limitation of gource requiring OpenGL for rendering.)"
    echo "         The window will close automatically when complete."
    echo ""
    echo "         Video will be saved to: $OUTPUT_FILE"
    echo ""
    read -n 1 -p "Press Enter to continue, or any other key to skip: " key
    echo ""
    if [ -n "$key" ]; then
        echo ""
        echo -e "${YELLOW}Generation stopped by user.${NC}"
        exit 1
    fi
    echo ""

    echo "Generating video (this may take a while)..."
    echo ""

    # Calculate stop-at-time if duration is specified
    STOP_OPTS=()
    if [ "$GOURCE_VIDEO_DURATION" -gt 0 ] 2>/dev/null; then
        STOP_OPTS=(--stop-at-time "$GOURCE_VIDEO_DURATION")
    fi

    # Generate video using ffmpeg
    gource "${GOURCE_OPTS[@]}" \
        "${STOP_OPTS[@]}" \
        -${WIDTH}x${HEIGHT} \
        --title "DO NOT EXIT OR CLOSE THIS WINDOW - VIDEO GENERATING" \
        --output-framerate 30 \
        --output-ppm-stream - \
        "$PROJECT_ROOT" \
        2>/dev/null | \
    ffmpeg -y \
        -r 30 \
        -f image2pipe \
        -vcodec ppm \
        -i - \
        -vcodec libx264 \
        -preset fast \
        -pix_fmt yuv420p \
        -crf 23 \
        "$OUTPUT_FILE" \
        2>/dev/null

    if [ -f "$OUTPUT_FILE" ]; then
        FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
        echo -e "${GREEN}[OK]${NC} Video generated: $OUTPUT_FILE ($FILE_SIZE)"
    else
        echo -e "${RED}[ERROR]${NC} Failed to generate video"
        exit 1
    fi
fi

# =============================================================================
# Summary
# =============================================================================

echo ""
echo -e "${BOLD}========================================"
echo "Complete!"
echo -e "========================================${NC}"
echo ""
echo "Output location: $SCRIPT_DIR/output/"
echo ""

# Show what was generated
if [ -d "$OUTPUT_DIR" ] && [ "$(ls -A "$OUTPUT_DIR" 2>/dev/null)" ]; then
    echo "Generated files:"
    echo ""
    ls "$OUTPUT_DIR"/* 2>/dev/null | while read f; do
        size=$(du -h "$f" | cut -f1)
        echo "  $(basename "$f") ($size)"
    done
    echo ""
fi

echo -e "${GREEN}Done!${NC}"
echo ""
