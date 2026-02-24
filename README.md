# dev-toolbox

Standalone dev tools and AI infrastructure I built for my own workflow. Scripts for daily tasks, multi-agent AI systems, reusable Claude Code skills, and context-engineered prompts — each documented and self-contained.

> **Note:** Items are listed alphabetically within each section.

---

## Dev Tools

Standalone tools, each with its own README covering setup and usage.

| Tool | What it does |
|------|--------------|
| [demo-generator](./demo-generator/README.md) | Build beat-synced animated web demos with Claude, then screen-record into polished demo videos |
| [directory-tree-printer](./directory-tree-printer/README.md) | Print directory structure to terminal and file, respecting .gitignore |
| [docker-cleanser](./docker-cleanser/README.md) | Nuke and reset Docker environment — containers, images, volumes, networks |
| [repo-analyzer](./repo-analyzer/README.md) | Code statistics, git history analysis, dependency graphs, and LLM-generated architecture docs |
| [repo-content-aggregator](./repo-content-aggregator/README.md) | Dump an entire repo into a single text file for LLM ingestion, respecting .gitignore |
| [tui-markdown-browser](./tui-markdown-browser/README.md) | Terminal markdown browser — keyboard navigation, live preview, mouse scroll |

---

## Comparison & Conversion

| Tool | What it does |
|------|--------------|
| [medium-post-converter](./medium-post-converter/README.md) | Markdown → Medium-optimized HTML for copy-paste publishing |
| [spreadsheet-diff](./comparison/spreadsheet-diff/README.md) | Field-level diff for CSV and Excel files — handles 10M+ rows, composite keys, multiple output formats |
| [tsql-sp-to-query](./conversion/tsql-sp-to-query/README.md) | Convert T-SQL stored procedures to inline queries |
| [xlsx-to-json](./conversion/xlsx-to-json/README.md) | Convert Excel files to JSON |

---

## AI

Context-engineered AI assets under [`ai/`](./ai/README.md). Drop-in components for Claude-based workflows, organized by type.

| Category | What it contains |
|----------|-----------------|
| [Claude Code Skills](./ai/claude-code/skills/) | Skills for extending Claude Code workflows — commit management, code review, session handoff, document editing, Jira, GitLab MR, and more |
| [Context Engineering Prompts](./ai/context-engineering/) | Versioned standalone prompts: algorithm tutoring, role-specific planning starters, and multi-agent RPI (researcher / planner / implementer) |
| [Personas](./ai/personas/) | Reusable Claude personas: `roles/` for session-long identities (engineer, architect, designer, PM, etc.), `tasks/` for short-lived jobs (PR review, code scrutiny) |
| [Toolkits](./ai/toolkits/) | Multi-agent orchestrated systems with dedicated agents, philosophy, templates, and slash commands — writing, research, and document refinement pipelines |
