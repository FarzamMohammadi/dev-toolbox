# Skill Specification

Technical reference for SKILL.md format, covering both the official Agent Skills standard and Claude Code-specific extensions.

---

## Official Standard (agentskills.io)

### Required Fields

| Field | Constraints | Purpose |
|-------|-------------|---------|
| `name` | 1-64 chars, lowercase letters/numbers/hyphens only, must match directory | Command identifier (`/name`) |
| `description` | 1-1024 chars, non-empty | Triggers auto-discovery, describes what + when |

#### `name` Field Rules

- Must be 1-64 characters
- Only lowercase alphanumeric and hyphens (`a-z`, `0-9`, `-`)
- Cannot start or end with `-`
- Cannot contain consecutive hyphens (`--`)
- Must match the parent directory name

```yaml
# Valid
name: pdf-processing
name: code-review
name: data-analysis

# Invalid
name: PDF-Processing    # uppercase not allowed
name: -pdf              # cannot start with hyphen
name: pdf--processing   # consecutive hyphens not allowed
```

#### `description` Field Guidelines

- Must be 1-1024 characters
- Should describe both **what** the skill does and **when** to use it
- Write in **third person** (critical for discovery)
- Include specific keywords that help agents identify relevant tasks

```yaml
# Good - specific, includes what + when
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Bad - vague
description: Helps with PDFs.
```

### Optional Standard Fields

| Field | Constraints | Purpose |
|-------|-------------|---------|
| `license` | Short string | License name or file reference |
| `compatibility` | Max 500 chars | Environment requirements |
| `metadata` | Key-value map | Arbitrary additional properties |
| `allowed-tools` | Space-delimited list | Pre-approved tools (experimental) |

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files...
license: Apache-2.0
compatibility: Requires git, docker, jq
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash Read Write
---
```

---

## Claude Code Extensions

These fields are **Claude Code-specific** and may not work in other agents.

### `disable-model-invocation`

Prevents automatic invocation. Use for skills with side effects.

```yaml
disable-model-invocation: true
```

| Value | Behavior |
|-------|----------|
| `true` | Manual-only via `/command` |
| `false` (default) | Claude can auto-invoke based on description |

**Use when:** deployments, commits, deletions, sending messages, any irreversible action.

### `user-invocable`

Controls visibility in the `/` command menu.

```yaml
user-invocable: false
```

| Value | Behavior |
|-------|----------|
| `true` (default) | Appears in `/` menu |
| `false` | Hidden from menu, but Claude can still use it |

**Use when:** Background knowledge, reference material Claude auto-loads.

### `argument-hint`

Shown in autocomplete to guide users.

```yaml
argument-hint: [ticket-key] [--comment]
```

**Use when:** Skill takes arguments the user should know about.

### `context`

Controls execution context.

```yaml
context: fork
```

| Value | Behavior |
|-------|----------|
| (default) | Inline execution, sees full conversation |
| `fork` | Isolated context, verbose output won't pollute conversation |

**Use when:** Research tasks producing large output, exploration.

### `agent`

Delegates to a named agent type.

```yaml
agent: Explore
```

**Use when:** Skill should use specialized agent capabilities.

### `model`

Overrides the model for this skill.

```yaml
model: haiku
```

**Use when:** Simple tasks where speed/cost matters more than capability.

---

## Complete Field Reference

```yaml
---
# === Required (Official Standard) ===
name: my-skill                          # Command name, becomes /my-skill
description: What it does and when      # Triggers auto-discovery

# === Optional (Official Standard) ===
license: Apache-2.0                     # License identifier
compatibility: Requires python>=3.8    # Environment requirements
metadata:                               # Arbitrary key-value pairs
  author: team-name
  version: "1.0"
allowed-tools: Read Write Bash          # Space-delimited tool list

# === Claude Code Extensions ===
disable-model-invocation: true          # Manual only (for side effects)
user-invocable: true                    # Show in / menu (default: true)
argument-hint: [file] [options]         # Autocomplete hint
context: fork                           # Isolated execution context
agent: Explore                          # Delegate to named agent
model: haiku                            # Override model selection
---
```

---

## Directory Structure

### Development Structure (this repo)

```
ai/skills/
├── __design-guide/         # Documentation
├── skill-name/
│   ├── skill.md            # Main file (lowercase, our convention)
│   └── README.md           # Optional: user documentation
```

### Deployment Structure

```
.claude/skills/
└── skill-name/
    └── SKILL.md            # Uppercase per official spec
```

### Optional Directories (Official Standard)

```
skill-name/
├── SKILL.md              # Required: instructions + metadata
├── scripts/              # Optional: executable code
├── references/           # Optional: documentation loaded as needed
└── assets/               # Optional: templates, images, boilerplate
```

| Directory | Purpose | Context Usage |
|-----------|---------|---------------|
| `scripts/` | Executable code (Python, Bash, JS) | Executed, not loaded into context |
| `references/` | Additional documentation | Loaded on-demand when referenced |
| `assets/` | Templates, images, data files | Used in output, not loaded into context |

---

## Progressive Disclosure

Skills use progressive disclosure to manage context efficiently:

1. **Metadata** (~100 tokens): `name` and `description` loaded at startup for all skills
2. **Instructions** (<5000 tokens recommended): Full SKILL.md body loaded on activation
3. **Resources** (as needed): Files in `scripts/`, `references/`, `assets/` loaded only when required

### Guidelines

- Keep SKILL.md body under **500 lines**
- Move detailed reference material to separate files
- Keep file references **one level deep** from SKILL.md
- Avoid deeply nested reference chains

```markdown
# Good: One level deep
See [reference.md](reference.md) for API details.
See [forms.md](forms.md) for form handling.

# Bad: Nested references
See [advanced.md](advanced.md) → which links to [details.md](details.md)
```

---

## Validation

Use the [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) library to validate skills:

```bash
# Validate a skill directory
skills-ref validate ./my-skill

# Generate <available_skills> XML for prompts
skills-ref to-prompt ./my-skill
```
