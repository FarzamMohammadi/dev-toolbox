# Architecture Patterns Mandate

> **Purpose:** Define structural patterns for organizing scripts, tools, and automation at scale. One command to run everything, one command to clean up.

---

## Core Principle

**Modular tools, unified orchestration.** Each tool is self-contained and independently runnable. An orchestrator script calls them all in sequence. A cleanup script removes everything. The user remembers two commands, not twenty.

---

## The Orchestrator Pattern

### What It Is

One master script (`run-all.sh`) that:
1. Checks dependencies and auto-installs if needed
2. Calls each tool's `run.sh` in logical phases
3. Skips unavailable tools gracefully (warn, don't fail)
4. Collects all output to a unified directory

### Why It Matters

| Without Orchestrator | With Orchestrator |
|---------------------|-------------------|
| User runs 8 scripts manually | User runs 1 script |
| Forgets which scripts exist | Everything runs automatically |
| Inconsistent output locations | Unified output directory |
| Manual dependency management | Auto-setup on first run |

### Implementation Pattern

```bash
# run-all.sh structure
./run-all.sh [target] [output_dir]

# Internal flow:
# 1. Auto-setup if dependencies missing
# 2. Phase 1: Core tools (always run)
# 3. Phase 2: Conditional tools (if language detected)
# 4. Phase 3: Optional tools (if deps available)
# 5. Summary of generated files
```

---

## The Modular Tool Pattern

### Contract

Every tool's `run.sh` MUST accept:

```bash
./run.sh <target> <output_dir>

# $1 = Target to analyze (default: current directory)
# $2 = Output directory (default: ./output)
```

### Standard Structure

```bash
#!/bin/bash
set -e

# Arguments
TARGET="${1:-.}"
OUTPUT_DIR="${2:-./output}"

# Resolve to absolute paths
TARGET="$(cd "$TARGET" && pwd)"
mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"

# Check dependencies
if ! command -v <tool> &> /dev/null; then
    echo "[ERROR] <tool> not installed"
    exit 1
fi

# Do the work...

# Output to $OUTPUT_DIR/<tool-name>/
```

### Key Rules

1. **Accept standard arguments** - same interface for all tools
2. **Resolve paths** - convert to absolute paths immediately
3. **Check dependencies** - fail fast or skip gracefully
4. **Output consistently** - write to `$OUTPUT_DIR/` or subdirectory
5. **Exit clean** - return 0 on success, non-zero on failure

---

## The Cleanup Pattern

### What It Does

One script (`cleanup.sh`) that removes:
- Generated output directories
- Virtual environments
- Installed packages (with user confirmation)

### Implementation Pattern

```bash
# cleanup.sh structure

# 1. Show what will be removed
# 2. Ask for confirmation
# 3. For each component:
#    - Check if present
#    - Prompt before removing
#    - Track what was removed
# 4. Show summary
```

### Key Rules

1. **Interactive by default** - prompt before destructive actions
2. **Granular control** - user can skip individual components
3. **Informative** - show what was/wasn't removed
4. **Non-destructive default** - require explicit 'y' to proceed

---

## Directory Structure

```
project/
├── run-all.sh              # Orchestrator
├── setup.sh                # Dependency installer
├── cleanup.sh              # Cleanup script
│
├── tools/                  # Individual tools
│   ├── tool-a/
│   │   ├── run.sh          # Standard interface
│   │   └── config.sh       # Optional configuration
│   └── tool-b/
│       └── run.sh
│
└── output/                 # Unified output (generated)
    ├── tool-a/
    └── tool-b/
```

---

## Adding New Tools

### Checklist

1. Create `tools/<name>/run.sh` following the modular pattern
2. Accept `$1=target`, `$2=output_dir`
3. Add to `run-all.sh` using the orchestrator pattern
4. Add any new system dependencies to `setup.sh`
5. Add same dependencies to `cleanup.sh`

### Anti-Patterns

| Bad | Good |
|-----|------|
| Hardcoded paths in tool scripts | Accept paths as arguments |
| Tool outputs to its own directory | Output to shared `$OUTPUT_DIR` |
| Fail if optional dep missing | Skip with warning message |
| Require manual setup first | Auto-setup in orchestrator |

---

## Integration Points

This pattern applies to:
- CLI toolkits with multiple commands
- Analysis suites with multiple analyzers
- Build systems with multiple stages
- Any multi-tool workflow

---

## Verification Checklist

- [ ] User can run full workflow with single command
- [ ] User can clean up everything with single command
- [ ] Each tool works independently when called directly
- [ ] Missing dependencies result in skip, not failure
- [ ] All output goes to unified directory
- [ ] Adding new tools follows documented pattern
