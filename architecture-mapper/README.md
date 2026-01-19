# Architecture Mapper

Tools for understanding, analyzing, and documenting project architecture.

> **Philosophy:** Understanding comes from patterns, not pixels. See [philosophy.md](./philosophy.md) for the full manifesto.

## Quick Start

```bash
# Run full analysis (auto-installs dependencies if needed)
./run-all.sh /path/to/repo

# When done, clean up installed dependencies
./cleanup.sh
```

That's it. Two commands.

## What It Does

`run-all.sh` runs analysis in four phases:

**Phase 1: Core Statistics** (always runs)
- Code statistics: lines, complexity, language breakdown
- Directory structure mapping
- Git history: hotspots, churn, ownership

**Phase 2: Language-Specific** (if detected)
- Python: module dependencies, call graphs, pattern detection
- More languages coming soon

**Phase 3: LLM-Powered** (requires [Claude Code](https://claude.com/claude-code))
- Auto-generates architecture.md from codebase analysis

**Phase 4: Visualization** (if gource installed)
- Interactive git history visualization (navigate with keyboard/mouse: arrows, +/-, Space to pause)

Missing dependencies are skipped with a warning, not failures.

## Output

Results are saved to `./output/`:

```
output/
├── code-stats.json           # SLOC, complexity metrics
├── code-stats.html           # Visual report (open in browser)
├── structure.txt             # Directory tree
├── structure.json            # Structured directory data
├── git-analysis/
│   ├── revisions.csv         # Most changed files (hotspots)
│   ├── churn.csv             # Lines added/removed per file
│   └── ownership.csv         # Primary authors per file
├── python/                   # (if Python detected)
│   ├── dependencies.svg      # Module dependency graph
│   ├── imports.txt           # Import analysis
│   └── patterns.json         # Detected design patterns
├── repo-evolution/           # (if GOURCE_LIVE_PREVIEW=false)
│   └── history.mp4           # Exported git history video
└── architecture.md           # LLM-generated documentation
```

## Configuration

All settings are in `config.sh` at the root. Edit once, applies to all tools:

```bash
# General
PROJECT_NAME=""                     # Leave empty to auto-detect from repo name
MAX_DEPTH=4                         # Directory tree depth
EXCLUDE_DIRS=".git node_modules .venv ..."  # Directories to skip

# Git Visualization
GOURCE_RESOLUTION="800x600"
GOURCE_SECONDS_PER_DAY="0.5"        # Lower = faster animation
GOURCE_VIDEO_DURATION=60            # Seconds (-1 for full history)
GOURCE_LIVE_PREVIEW="true"          # Interactive window (false = export video)

# Git Statistics
CODE_MAAT_JAR=""                    # Optional path to code-maat.jar

# Python Analysis
PYTHON_SRC_DIRS="src lib app ."     # Search order for source
PYTHON_MAX_FILES=100                # Max files for call graph

# LLM Documentation
LLM_CONTEXT_DEPTH=3                 # Tree depth for context
LLM_FILE_LIMIT=100                  # Lines per config file
```

See `config.sh` for all options with descriptions.

## How It Works

```
architecture-mapper/
├── config.sh                 # Single config file for all tools
├── run-all.sh                # Orchestrator - runs everything
├── setup.sh                  # Installs dependencies (auto-called if needed)
├── cleanup.sh                # Removes .venv, output/, optionally brew packages
├── README.md
├── philosophy.md
└── resources/
    ├── tools/
    │   ├── analyzers/        # Code analysis tools
    │   ├── visualizers/      # Output generators (gource)
    │   └── llm-tools/        # LLM-powered analysis
    └── templates/            # Documentation templates
```

**Key design:**
- `config.sh` configures all tools from one place
- `run-all.sh` sources config and passes settings to each tool
- `run-all.sh` auto-runs `setup.sh` if dependencies are missing
- Each tool can also run independently (uses defaults if no config exported)
- Tools accept standard arguments: `$1=target_repo`, `$2=output_dir`
- Missing tools are skipped gracefully (warn, don't fail)

## Dependencies

Installed automatically by `setup.sh` (or when you run `run-all.sh`):

| Tool | Purpose |
|------|---------|
| scc | Code statistics and complexity |
| graphviz | Graph rendering |
| gource + ffmpeg | Git history visualization |
| pydeps, pyan3 | Python analysis (installed in .venv) |

Optional: [Claude Code](https://claude.com/claude-code) for LLM-powered documentation.

## Adding New Tools

1. Create `resources/tools/analyzers/<category>/<tool>/run.sh` or `resources/tools/visualizers/<tool>/run.sh`
2. Accept `$1=target_repo`, `$2=output_dir`
3. Add to appropriate phase in `run-all.sh`
4. Add dependencies to `setup.sh` and `cleanup.sh`

## Resources

- [Your Code as a Crime Scene](https://pragprog.com/titles/atcrime2/your-code-as-a-crime-scene-second-edition/) - Adam Tornhill (hotspots methodology)
- [scc](https://github.com/boyter/scc) - Code counter with complexity
- [gource](https://gource.io/) - Git visualization
