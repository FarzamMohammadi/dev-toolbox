#!/bin/bash
# =============================================================================
# Git Visualizer Configuration
# =============================================================================
# Edit these values to customize for your project

# Project name (used in titles and headers)
PROJECT_NAME="AI Knowledge Service"

# Gource configuration
GOURCE_TITLE="${PROJECT_NAME} Evolution"
# Window resolution (use small fixed size to avoid Retina scaling issues)
GOURCE_RESOLUTION="960x720"
GOURCE_SECONDS_PER_DAY="0.5"

# Output video duration (in seconds, -1 for auto)
GOURCE_VIDEO_DURATION=60

# Whether to show live gource preview instead of generating video
# Set to "true" for live preview, "false" for video generation
GOURCE_LIVE_PREVIEW="false"
