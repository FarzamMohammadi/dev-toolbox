# Claude Code Skill Design Guide

> Authoritative reference for creating portable, self-contained skills.

---

## Sources & Attribution

This guide consolidates guidance from multiple authoritative sources:

| Source | URL | Coverage |
|--------|-----|----------|
| **Agent Skills Specification** | https://agentskills.io/specification | Open standard for skill format |
| **Anthropic Best Practices** | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Official authoring guidance |
| **Anthropic Example Skills** | https://github.com/anthropics/skills | 16 production-quality examples |
| **Custom Skills Guide** | https://support.claude.com/en/articles/12512198 | Claude.ai skill creation |

**Last updated:** January 2025

---

## Quick Start (30 Seconds)

1. Create `skill-name/skill.md` with YAML frontmatter
2. Include `name` and `description` (required)
3. Add `disable-model-invocation: true` if it has side effects
4. Write clear, step-by-step instructions
5. Define explicit output format with `[placeholders]`

```yaml
---
name: my-skill
description: What it does and when to use it
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash
---

# My Skill

## Step 1: Gather
What to collect...

## Step 2: Process
What to do with it...

## Step 3: Output
Exact format:
- [item]
```

---

## File Naming Convention

| Location | Convention | Notes |
|----------|------------|-------|
| Development (this repo) | `skill.md` (lowercase) | Our local convention |
| Deployment | `.claude/skills/name/SKILL.md` | Official spec (uppercase) |

**Deploy command:**
```bash
cp ai/skills/my-skill/skill.md .claude/skills/my-skill/SKILL.md
```

---

## Navigation

| I need to... | Go to |
|--------------|-------|
| Understand the technical spec | [specification.md](specification.md) |
| Learn authoring best practices | [best-practices.md](best-practices.md) |
| Find a pattern for my skill type | [patterns/](patterns/README.md) |
| Start from a template | [templates/](templates/README.md) |
| See real examples | [examples/](examples/README.md) |
| Verify before shipping | [checklist.md](checklist.md) |
| Know what to avoid | [anti-patterns.md](anti-patterns.md) |

---

## Core Principles

### 1. Context Window is Shared
The context window is a public good. Only include information Claude doesn't already have. Challenge each piece: "Does this justify its token cost?"

### 2. Gather → Process → Output
Structure every skill in three phases. Claude knows when it's done with each phase—no ambiguity.

### 3. Explicit Output Templates
Don't say "summarize"—show the exact format with `[placeholders]` Claude fills in.

### 4. Precise Descriptions
Include the *what* and *when*. Vague descriptions = unreliable auto-invocation.

### 5. Minimum Viable Tools
Only allow tools the skill actually needs. Prevents accidents, makes intent clear.

### 6. Idempotent Setup
Setup should be safe to run multiple times. Use `[ -f file ] || create` pattern.

### 7. Single Responsibility
One skill = one job. If you're writing "and" in the description, consider splitting.

---

## Directory Structure

```
ai/skills/
├── __design-guide/           # You are here
│   ├── start-here.md         # This file
│   ├── specification.md      # Technical spec
│   ├── best-practices.md     # Authoring guidance
│   ├── checklist.md          # Pre-shipping verification
│   ├── anti-patterns.md      # What to avoid
│   ├── patterns/             # Pattern library
│   ├── templates/            # Starting templates
│   └── examples/             # Annotated examples
├── commit/
│   └── skill.md              # Git commit skill
├── handoff/
│   └── skill.md              # Session handoff skill
├── jira/
│   ├── skill.md              # Jira API skill
│   └── README.md
└── glab-mr-manager/
    ├── skill.md              # GitLab MR skill
    └── README.md
```

---

## Quick Decision Matrix

### Skill vs Agent

| Need | Use |
|------|-----|
| Needs conversation history | **Skill** (inline) |
| Output for user to see/copy | **Skill** (inline) |
| Manual-only with side effects | **Skill** (`disable-model-invocation: true`) |
| Isolated verbose output | **Skill** (`context: fork`) |
| Parallel execution | **Agent** |
| Specialized domain | **Agent** (custom system prompt) |

### Frontmatter Quick Combos

| Use Case | Frontmatter |
|----------|-------------|
| General utility | `name`, `description`, `allowed-tools` |
| Dangerous action | + `disable-model-invocation: true` |
| Background knowledge | + `user-invocable: false` |
| Research/exploration | + `context: fork`, `agent: Explore` |
| Cheap model for simple task | + `model: haiku` |

---

## Next Steps

1. **New to skills?** Read [specification.md](specification.md) then [best-practices.md](best-practices.md)
2. **Know what you need?** Jump to [patterns/](patterns/README.md) or [templates/](templates/README.md)
3. **Ready to ship?** Run through [checklist.md](checklist.md)
