# ai/

Context-engineered AI assets for Claude-based workflows. Organized by type — drop in what you need.

---

## Directory Structure

```
ai/
├── toolkits/               # Multi-agent orchestrated systems
│   ├── writing/            # Blog, book, and docs writing pipeline
│   ├── research/           # Multi-agent research with source evaluation
│   └── research-doc-refiner/  # Refine research output into polished docs
│
├── personas/               # Reusable AI personas
│   ├── roles/              # Identity personas (session-long)
│   ├── tasks/              # Task personas (short-lived)
│   └── philosophies.md     # Shared foundations all personas inherit from
│
├── claude-code/            # Claude Code specific assets
│   └── skills/             # Skills for extending Claude Code workflows
│
├── context-engineering/    # Versioned standalone prompts
│   └── prompts/
│       ├── leetcode-tutor/ # Algorithm tutoring (v1–v4)
│       ├── plan-starter/   # Role-specific planning kickstarters
│       └── rpi/            # Researcher / Planner / Implementer prompts
│
└── workflow-optimization-plan/  # Internal planning docs and session memory
```

---

## What Goes Where

| Folder | What it's for | Example |
|--------|---------------|---------|
| `toolkits/` | Complex systems with multiple agents, templates, and commands | Writing pipeline (10+ agents) |
| `personas/` | Reusable Claude identity and task personas | Backend engineer role, PR reviewer task |
| `claude-code/skills/` | Claude Code skills for specialized workflows | Commit, review-pr, wrap-session |
| `context-engineering/` | Standalone versioned prompts | LeetCode tutor v1–v4 |

---

## Quick Access

### Toolkits

| Toolkit | Purpose | Entry Point |
|---------|---------|-------------|
| [writing](toolkits/writing/) | Blog, book, docs creation pipeline | `toolkits/writing/readme.md` |
| [research](toolkits/research/) | Multi-agent research and synthesis | `toolkits/research/README.md` |
| [research-doc-refiner](toolkits/research-doc-refiner/) | Refine research into polished documents | `toolkits/research-doc-refiner/README.md` |

### Personas

| Type | Contents |
|------|---------|
| [roles/](personas/roles/) | backend-engineer, frontend-engineer, technical-architect, designer, product-manager, devops-engineer, business-strategist |
| [tasks/](personas/tasks/) | pr-reviewer, code-scrutinizer |

### Skills

See [`claude-code/skills/README.md`](claude-code/skills/README.md) for the full directory and deployment instructions.

### Prompts

| Prompt | Purpose |
|--------|---------|
| [leetcode-tutor](context-engineering/prompts/leetcode-tutor/) | Algorithm problem tutoring (v1–v4) |
| [plan-starter](context-engineering/prompts/plan-starter/) | Planning kickstarters for specific roles |
| [rpi](context-engineering/prompts/rpi/) | Researcher / Planner / Implementer orchestration |
