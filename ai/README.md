# ai/

Centralized AI tooling, prompts, and resources.

---

## Directory Structure

```
ai/
├── toolkits/           # Complex multi-file orchestrated systems
│   └── writing/        # 10-layer writing pipeline (blogs, books, docs)
│
├── prompts/            # Standalone prompts (simple, single-purpose)
│   └── leetcode-tutor/ # Algorithm tutoring prompt (v1-v4)
│
├── agents/             # Standalone agents (not part of toolkits)
│   └── context-relay-agent.md
│
├── memory/             # Global persistent context
│   ├── learnings.md    # Cross-session learnings
│   ├── decisions.md    # Key decisions made
│   └── session-history.md
│
├── plans/              # Roadmaps, master plans
│   ├── ultimate-directory-master-plan.md
│   └── implementation-phases.md
│
└── handoffs/           # Session continuity
    └── handoff-prompt.md
```

---

## What Goes Where

| Folder | What It's For | Example |
|--------|---------------|---------|
| `toolkits/` | Complex systems with multiple files, agents, templates | Writing toolkit (35+ files) |
| `prompts/` | Simple standalone prompts | LeetCode tutor, interview prep |
| `agents/` | Standalone agents not part of a toolkit | Context relay agent |
| `memory/` | Persistent context across sessions | Learnings, decisions |
| `plans/` | Documentation, roadmaps, master plans | Implementation phases |
| `handoffs/` | Session continuity prompts | Handoff templates |

---

## Quick Access

### Toolkits

| Toolkit | Purpose | Entry Point |
|---------|---------|-------------|
| [writing](toolkits/writing/) | Blog, book, docs creation | `toolkits/writing/readme.md` |

### Prompts

| Prompt | Purpose |
|--------|---------|
| [leetcode-tutor](prompts/leetcode-tutor/) | Algorithm problem tutoring |

---

## Adding New Content

### New Toolkit
```
ai/toolkits/[name]/
├── readme.md           # How to use
├── commands/           # Entry points
├── agents/             # Specialized agents
├── philosophy/         # Rules and mandates
├── templates/          # Document templates
├── skills/             # Reusable capabilities
└── memory/             # Toolkit-specific memory
```

### New Prompt
```
ai/prompts/[name]/
├── v1.md               # Version 1
├── v2.md               # Version 2 (iterate)
└── ...
```

### New Standalone Agent
```
ai/agents/[name]-agent.md
```
