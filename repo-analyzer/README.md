# Repo Analyzer

Tools for understanding and documenting project architecture.

> See [philosophy.md](./philosophy.md) for design principles.

## Quick Start

```bash
./run-all.sh /path/to/repo    # Analyze (auto-installs deps)
./cleanup.sh                   # Remove installed dependencies
```

## What It Does

**Phase 1: Core Statistics** (always)
- Code stats: lines, complexity, language breakdown
- Directory structure mapping
- Git history: hotspots, churn, ownership

**Phase 2: Language-Specific** (if detected)
- Python: dependencies, call graphs, pattern detection

**Phase 3: LLM-Powered** (if [Claude Code](https://claude.com/claude-code) installed)
- Auto-generates `architecture.md`

**Phase 4: Visualization** (if gource installed)
- Interactive window records to `repo-evolution/history.mp4`
- Navigate while recording: Space (pause), +/- (speed), arrows (pan), mouse (drag/zoom)
- Don't close early - let it finish

Missing tools are skipped gracefully.

## Output

```
output/
├── code-stats.json/html      # SLOC, complexity
├── structure.txt/json        # Directory tree
├── git-analysis/
│   ├── revisions.csv         # Hotspots (most changed files)
│   ├── churn.csv             # Lines added/removed
│   └── ownership.csv         # Primary authors
├── python/                   # (if detected)
│   ├── dependencies.svg      # Module graph
│   └── patterns.json         # Design patterns
├── repo-evolution/
│   └── history.mp4           # Git history video
└── architecture.md           # LLM-generated docs
```

## Configuration

Edit `config.sh`:

```bash
PROJECT_NAME=""               # Auto-detects from repo
MAX_DEPTH=4                   # Tree depth
EXCLUDE_DIRS=".git node_modules .venv ..."

# Visualization
GOURCE_RESOLUTION="800x600"
GOURCE_SECONDS_PER_DAY="0.5"  # Lower = faster
GOURCE_VIDEO_DURATION=60      # -1 for full history

# Python
PYTHON_SRC_DIRS="src lib app ."
PYTHON_MAX_FILES=100
```

## Project Structure

```
├── config.sh         # All settings
├── run-all.sh        # Main entry point
├── setup.sh          # Dependency installer
├── cleanup.sh        # Uninstaller
└── resources/
    ├── tools/        # analyzers/, visualizers/, llm-tools/
    └── templates/    # Doc templates
```

## Dependencies

Auto-installed by `setup.sh`:

| Tool | Purpose |
|------|---------|
| scc | Code statistics |
| graphviz | Graph rendering |
| gource + ffmpeg | Git visualization |
| pydeps, pyan3 | Python analysis |

## Resources

- [Your Code as a Crime Scene](https://pragprog.com/titles/atcrime2/your-code-as-a-crime-scene-second-edition/) - Hotspots methodology
- [scc](https://github.com/boyter/scc) | [gource](https://gource.io/)
