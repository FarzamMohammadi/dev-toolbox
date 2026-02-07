#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass=0
fail=0
warn=0

check() {
  local name="$1" cmd="$2" min_ver="${3:-}" install_hint="${4:-}"
  if command -v "$cmd" &>/dev/null; then
    local ver
    ver=$("$cmd" --version 2>&1 | head -1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1 || echo "unknown")
    printf "${GREEN}[OK]${NC}  %-18s %s\n" "$name" "v$ver"
    ((pass++)) || true || true
  else
    printf "${RED}[MISSING]${NC}  %-14s %s\n" "$name" "$install_hint"
    ((fail++))  || true
  fi
}

echo ""
echo "=== Demo Generator - Dependency Check ==="
echo ""

echo "-- Core Tools --"
check "Node.js"   "node"    "18.0.0"  "brew install node"
check "npm"       "npm"     ""        "(comes with Node.js)"
check "Python 3"  "python3" "3.10.0"  "brew install python3"
check "uv"        "uv"      ""        "curl -LsSf https://astral.sh/uv/install.sh | sh"
check "ffmpeg"    "ffmpeg"  ""        "brew install ffmpeg"

echo ""
echo "-- Python Packages (managed by uv) --"
if command -v uv &>/dev/null; then
  printf "${GREEN}[OK]${NC}  %-18s %s\n" "uv sync" "run 'uv sync' to install Python deps"
  ((pass++)) || true
else
  printf "${YELLOW}[INFO]${NC}  %-12s %s\n" "Python deps" "install uv first, then run 'uv sync'"
  ((warn++)) || true
fi

echo ""
echo "-- Optional (manual recording fallback & assembly) --"

if command -v obs &>/dev/null || [ -d "/Applications/OBS.app" ]; then
  printf "${GREEN}[OK]${NC}  %-18s %s\n" "OBS Studio" "found"
  ((pass++)) || true
else
  printf "${YELLOW}[OPTIONAL]${NC}  %-12s %s\n" "OBS Studio" "https://obsproject.com (fallback screen recorder)"
  ((warn++)) || true
fi

if [ -f "/System/Applications/QuickTime Player.app/Contents/MacOS/QuickTime Player" ]; then
  printf "${GREEN}[OK]${NC}  %-18s %s\n" "QuickTime Player" "found (fallback screen recorder)"
  ((pass++)) || true
else
  printf "${YELLOW}[OPTIONAL]${NC}  %-12s %s\n" "Screen Recorder" "QuickTime (built-in) — only needed if automated recording fails"
  ((warn++)) || true
fi

echo ""
echo "-------------------------------------------"
printf "Results: ${GREEN}%d passed${NC}" "$pass"
[ "$fail" -gt 0 ] && printf ", ${RED}%d missing${NC}" "$fail"
[ "$warn" -gt 0 ] && printf ", ${YELLOW}%d optional${NC}" "$warn"
echo ""

if [ "$fail" -gt 0 ]; then
  echo ""
  echo "Install missing dependencies, then re-run: bash setup/check-dependencies.sh"
  echo "For Python packages: uv sync"
  exit 1
else
  echo "All required dependencies are installed!"
fi
