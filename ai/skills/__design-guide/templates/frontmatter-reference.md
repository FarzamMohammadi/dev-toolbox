# Frontmatter Reference

Complete reference for all YAML frontmatter fields in skill files.

---

## Required Fields (Official Standard)

### `name`

The skill's command identifier. Becomes `/name` in Claude Code.

```yaml
name: pdf-processing
```

**Constraints:**
- 1-64 characters
- Lowercase letters, numbers, hyphens only (`a-z`, `0-9`, `-`)
- Cannot start or end with `-`
- Cannot contain consecutive hyphens (`--`)
- Must match the parent directory name

**Valid examples:**
```yaml
name: code-review
name: data-analysis
name: jira-ticket-manager
```

**Invalid examples:**
```yaml
name: Code-Review        # uppercase not allowed
name: -code-review       # cannot start with hyphen
name: code--review       # consecutive hyphens
name: code_review        # underscores not allowed
```

---

### `description`

What the skill does and when to use it. Critical for auto-discovery.

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Constraints:**
- 1-1024 characters
- Non-empty

**Guidelines:**
- Write in **third person** (critical for discovery)
- Include both **what** it does and **when** to use it
- Include **keywords** that help identify relevant tasks
- Be **specific**, not vague

**Good examples:**
```yaml
# Specific, includes what + when + keywords
description: Create, search, update, and comment on Jira tickets via REST API. Use when user mentions Jira, tickets, issues, or sprint planning.

description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

**Bad examples:**
```yaml
# Too vague
description: Helps with documents

# Wrong person
description: I can help you process files

# Missing "when"
description: Manages Jira tickets
```

---

## Optional Fields (Official Standard)

### `license`

License identifier or file reference.

```yaml
license: Apache-2.0
license: Proprietary. See LICENSE.txt
```

---

### `compatibility`

Environment requirements (1-500 characters if provided).

```yaml
compatibility: Requires git, docker, jq, and internet access
compatibility: Designed for Claude Code
```

---

### `metadata`

Arbitrary key-value pairs for additional properties.

```yaml
metadata:
  author: team-name
  version: "1.0"
  category: development
```

---

### `allowed-tools`

Space-delimited list of pre-approved tools.

```yaml
allowed-tools: Bash Read Write
allowed-tools: Read Grep Glob
```

---

## Claude Code Extensions

These fields are **Claude Code-specific** and may not work in other agents.

### `disable-model-invocation`

Prevents Claude from automatically invoking this skill.

```yaml
disable-model-invocation: true
```

| Value | Behavior |
|-------|----------|
| `true` | Manual-only via `/command` |
| `false` or omitted | Claude can auto-invoke based on description |

**Use when:** Skill has side effects (deploy, commit, delete, send, purchase).

**Example:**
```yaml
name: deploy
description: Deploy to production environment
disable-model-invocation: true  # Dangerous - manual only
```

---

### `user-invocable`

Controls visibility in the `/` command menu.

```yaml
user-invocable: false
```

| Value | Behavior |
|-------|----------|
| `true` or omitted | Appears in `/` menu |
| `false` | Hidden from menu, but Claude can still use it |

**Use when:** Background knowledge or reference material that Claude auto-loads.

**Example:**
```yaml
name: coding-standards
description: Our team's coding conventions and style guide
user-invocable: false  # Background knowledge, not a command
```

---

### `argument-hint`

Shown in autocomplete to guide users.

```yaml
argument-hint: [ticket-key] [--comment]
argument-hint: [file] [--format=json|yaml]
argument-hint: [operation] [args]
```

**Use when:** Skill takes arguments users should know about.

---

### `context`

Controls execution context.

```yaml
context: fork
```

| Value | Behavior |
|-------|----------|
| omitted | Inline execution, sees full conversation |
| `fork` | Isolated context, verbose output won't pollute conversation |

**Use when:** Research tasks, exploration, or operations producing large output.

**Example:**
```yaml
name: explore-codebase
description: Research patterns and architecture
context: fork  # Isolate verbose exploration output
```

---

### `agent`

Delegates execution to a named agent type.

```yaml
agent: Explore
```

**Use when:** Skill should use specialized agent capabilities.

---

### `model`

Overrides the model for this skill.

```yaml
model: haiku
```

**Use when:** Simple tasks where speed/cost matters more than capability.

---

## Quick Combos

Common frontmatter combinations for different use cases:

### General Utility
```yaml
---
name: my-utility
description: Does X when user needs Y
allowed-tools: Read, Write, Edit
---
```

### Dangerous Action (Manual Only)
```yaml
---
name: deploy
description: Deploy to production environment
disable-model-invocation: true
allowed-tools: Bash, Read
---
```

### Background Knowledge
```yaml
---
name: team-conventions
description: Team coding conventions and standards
user-invocable: false
---
```

### Read-Only Research
```yaml
---
name: explore-auth
description: Research authentication patterns
allowed-tools: Read, Grep, Glob
context: fork
agent: Explore
---
```

### API Integration
```yaml
---
name: jira
description: Manage Jira tickets via REST API
allowed-tools: Bash, Read, Write
argument-hint: [operation] [ticket-key]
---
```

### Fast/Cheap Simple Task
```yaml
---
name: quick-format
description: Format code snippet
model: haiku
allowed-tools: Read, Write
---
```

---

## Tool Combinations Reference

| Skill Type | Recommended Tools |
|------------|-------------------|
| Read-only research | `Read, Grep, Glob` |
| File editing | `Read, Write, Edit` |
| External commands | `Bash, Read` |
| API integration | `Bash, Read, Write` |
| Full capability | Omit `allowed-tools` |

---

## Validation

The `name` and `description` fields are validated:
- `name` must meet all constraints (length, characters, no consecutive hyphens)
- `description` must be non-empty and under 1024 characters

Use [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) to validate:

```bash
skills-ref validate ./my-skill
```
