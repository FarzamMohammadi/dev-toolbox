#!/bin/bash
# =============================================================================
# Git Visualizer
# =============================================================================
# Generates animated repository history visualization using gource.
#
# Usage: ./run.sh <target_repo> <output_dir>
#
# Arguments:
#   target_repo  - Path to git repository to visualize (default: current directory)
#   output_dir   - Where to save video (default: ./output)
#
# Configuration: ./config.sh (optional - defaults used if not present)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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
OUTPUT_DIR="${2:-./output}"

# Resolve to absolute paths
if [ -d "$TARGET_REPO" ]; then
    TARGET_REPO="$(cd "$TARGET_REPO" && pwd)"
else
    echo -e "${RED}[ERROR]${NC} Target repository not found: $TARGET_REPO"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"

# Create gource output subdirectory
GOURCE_OUTPUT_DIR="$OUTPUT_DIR/repo-evolution"
mkdir -p "$GOURCE_OUTPUT_DIR"

# Detect if running interactively or from orchestrator
INTERACTIVE=true
if [ ! -t 0 ]; then
    INTERACTIVE=false
fi

echo ""
echo -e "${BOLD}Git Visualizer${NC}"
echo "==============="
echo ""
echo "Target: $TARGET_REPO"
echo "Output: $GOURCE_OUTPUT_DIR"
echo ""

# =============================================================================
# Load Configuration
# =============================================================================

# Use environment variables if set (from orchestrator), otherwise use defaults
# PROJECT_NAME empty means auto-detect from repo
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="$(basename "$TARGET_REPO")"
fi
GOURCE_TITLE="${PROJECT_NAME} Evolution (Interactive) - DON'T CLOSE WINDOW - VIDEO IS GENERATING"
GOURCE_RESOLUTION="${GOURCE_RESOLUTION:-960x720}"
GOURCE_SECONDS_PER_DAY="${GOURCE_SECONDS_PER_DAY:-0.5}"
GOURCE_VIDEO_DURATION="${GOURCE_VIDEO_DURATION:-60}"
GOURCE_LIVE_PREVIEW="${GOURCE_LIVE_PREVIEW:-false}"

echo -e "${BLUE}[INFO]${NC} Project: $PROJECT_NAME"

# =============================================================================
# Check Required Tools
# =============================================================================

echo ""
echo "Checking required tools..."

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
# Handle Missing Tools
# =============================================================================

MISSING_TOOLS=()
if [ "$GOURCE_OK" = false ]; then
    MISSING_TOOLS+=("gource")
fi
if [ "$FFMPEG_OK" = false ]; then
    MISSING_TOOLS+=("ffmpeg")
fi

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    if [ "$INTERACTIVE" = true ] && command -v brew &> /dev/null; then
        echo ""
        echo "Missing tools: ${MISSING_TOOLS[*]}"
        read -p "Install via Homebrew? [y/N] " -n 1 -r
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

            # Re-check
            command -v gource &> /dev/null && GOURCE_OK=true
            command -v ffmpeg &> /dev/null && FFMPEG_OK=true
        fi
    else
        # Non-interactive mode: skip gracefully
        echo ""
        echo -e "${YELLOW}[SKIP]${NC} Missing tools: ${MISSING_TOOLS[*]}"
        echo "       Install with: brew install gource ffmpeg"
        echo "       Or run setup.sh to install all dependencies"
        exit 0
    fi
fi

# =============================================================================
# Validate Requirements
# =============================================================================

if [ "$GOURCE_OK" = false ]; then
    echo ""
    echo -e "${YELLOW}[SKIP]${NC} Gource not installed - cannot generate visualization"
    exit 0
fi

if [ ! -d "$TARGET_REPO/.git" ]; then
    echo ""
    echo -e "${YELLOW}[SKIP]${NC} Not a git repository: $TARGET_REPO"
    exit 0
fi

# =============================================================================
# Generate Visualization
# =============================================================================

echo ""
echo -e "${BOLD}Generating repository visualization...${NC}"
echo ""

cd "$TARGET_REPO"

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
        "$TARGET_REPO"
else
    # Check for ffmpeg
    if [ "$FFMPEG_OK" = false ]; then
        echo -e "${YELLOW}[SKIP]${NC} FFmpeg not installed (required for video export)"
        echo "       Install with: brew install ffmpeg"
        exit 0
    fi

    OUTPUT_FILE="$GOURCE_OUTPUT_DIR/history.mp4"

    # In interactive mode, warn about window
    if [ "$INTERACTIVE" = true ]; then
        echo -e "${YELLOW}NOTE:${NC} An interactive window will open to render the video."
        echo "      Navigate while recording: Space (pause), +/- (speed), arrows (pan), mouse (drag/zoom)"
        echo "      Do not close it early - it will close automatically when complete."
        echo ""
        echo "      If the video doesn't capture full git history, edit config.sh:"
        echo "        GOURCE_VIDEO_DURATION=120   # Increase duration (seconds)"
        echo "        GOURCE_SECONDS_PER_DAY=0.3  # Speed up animation (lower = faster)"
        echo ""
        read -n 1 -p "Press Enter to continue, or any other key to skip: " key
        echo ""
        if [ -n "$key" ]; then
            echo -e "${YELLOW}[SKIP]${NC} Generation cancelled by user"
            exit 0
        fi
    else
        echo "Generating video (a window will open temporarily)..."
    fi

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
        --output-framerate 30 \
        --output-ppm-stream - \
        "$TARGET_REPO" \
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
echo -e "${GREEN}[OK]${NC} Git visualization complete"

if [ -d "$GOURCE_OUTPUT_DIR" ] && [ "$(ls -A "$GOURCE_OUTPUT_DIR" 2>/dev/null)" ]; then
    echo ""
    echo "Generated files:"
    ls "$GOURCE_OUTPUT_DIR"/* 2>/dev/null | while read f; do
        size=$(du -h "$f" | cut -f1)
        echo "  - $(basename "$f") ($size)"
    done
fi

echo ""
