#!/bin/bash
# =============================================================================
# Architecture Mapper - Configuration
# =============================================================================
# Single configuration file for all tools.
# Edit this file to customize behavior, then run ./run-all.sh
#
# All settings have sensible defaults - only change what you need.

# =============================================================================
# General Settings
# =============================================================================

# Project name (used in titles, headers, video titles)
PROJECT_NAME=""  # Leave empty to auto-detect from repo name

# Directory tree depth for structure analysis
MAX_DEPTH=4

# =============================================================================
# Exclusions
# =============================================================================

# Directories to exclude from all analysis (space-separated)
EXCLUDE_DIRS=".git node_modules .venv venv __pycache__ dist build .next .cache coverage .pytest_cache"

# =============================================================================
# Git Visualization (gource)
# =============================================================================

# Video resolution (WxH)
GOURCE_RESOLUTION="800x600"

# Animation speed (seconds per day of history - lower = faster)
GOURCE_SECONDS_PER_DAY="0.5"

# Video duration in seconds (-1 for full history)
GOURCE_VIDEO_DURATION=60

# Set to "true" for live preview window instead of video export
GOURCE_LIVE_PREVIEW="true"

# =============================================================================
# Git Statistics
# =============================================================================

# Path to code-maat.jar (optional - uses Docker or simplified analysis if empty)
CODE_MAAT_JAR=""

# =============================================================================
# Python Analysis
# =============================================================================

# Source directories to search (space-separated, in priority order)
PYTHON_SRC_DIRS="src lib app ."

# Maximum Python files to analyze for call graphs
PYTHON_MAX_FILES=100

# =============================================================================
# LLM Documentation
# =============================================================================

# Directory tree depth for context collection
LLM_CONTEXT_DEPTH=3

# Maximum lines to include from config files (README, package.json, etc.)
LLM_FILE_LIMIT=100
