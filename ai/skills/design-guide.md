# Skill Design Guide

A practical guide for creating portable, self-contained Claude Code skills.

---

## Quick Reference

```yaml
---
name: my-skill                          # Becomes /my-skill command
description: What it does and when      # Triggers auto-discovery
disable-model-invocation: true          # Manual only (for side effects)
user-invocable: true                    # Show in / menu (default: true)
allowed-tools: Read, Write, Edit, Bash  # Restrict tool access
argument-hint: [file] [options]         # Shown in autocomplete
---
```

---

## File Structure

```
ai/skills/
├── design-guide.md           # This guide
├── my-skill/
│   ├── skill.md              # Main skill file (required)
│   └── README.md             # Optional: user docs
└── another-skill/
    └── skill.md
```

**To deploy:** Copy `ai/skills/my-skill/skill.md` → `.claude/skills/my-skill/SKILL.md`

---

## Anatomy of a Self-Contained Skill

### 1. YAML Frontmatter

```yaml
---
name: deploy
description: Deploy to production environment
disable-model-invocation: true
argument-hint: [environment]
allowed-tools: Bash, Read
---
```

| Field | Purpose | When to Use |
|-------|---------|-------------|
| `name` | Command name (`/name`) | Always required |
| `description` | Triggers auto-discovery | Always include - be specific |
| `disable-model-invocation` | Prevents auto-invocation | Side effects (deploy, commit, delete) |
| `user-invocable` | Hides from `/` menu | Background knowledge skills |
| `allowed-tools` | Restricts tool access | Read-only skills, safety |
| `argument-hint` | Autocomplete hint | When skill takes arguments |

### 2. First-Time Setup Section

Embed setup commands so the skill works when copied to a new project:

```markdown
## First-Time Setup

Before first use, create required directories:

\`\`\`bash
mkdir -p path/to/data && \
  [ -f path/to/file.md ] || printf '# Header\n\nContent\n' > path/to/file.md
\`\`\`

Run this once per project.
```

**Pattern:** Use `[ -f file ] || create` to avoid overwriting existing files.

### 3. Instructions Body

Write clear, actionable steps. Use markdown structure:

```markdown
## Step 1: Do This First

Instructions...

## Step 2: Then Do This

More instructions...

## Output Format

What the skill should output when complete.
```

---

## Principles of Effective Skills

What separates a good skill from a great one.

### 1. Context Awareness

Know what information the skill needs:

| Skill Needs | Design Choice |
|-------------|---------------|
| What user just said | Inline skill (default) |
| Full conversation history | Inline skill |
| Only the task, nothing else | `context: fork` |

**The handoff skill works because** it runs inline and can see everything discussed.

### 2. Gather → Process → Output Pattern

Structure every skill in three phases:

```markdown
## Step 1: Gather [Information Type]
What to collect, where to find it, what questions to answer.

## Step 2: Process / Transform
What to do with the gathered information.

## Step 3: Output
Exactly what to produce and in what format.
```

**Why it works:** Claude knows when it's done with each phase. No ambiguity.

### 3. Explicit Output Templates

Don't say "summarize" - show the exact format:

```markdown
## Output Format

**`ai/memory/session-history.md`**
\`\`\`markdown
## [DATE] - Session Summary

**Goal:** [what user was trying to accomplish]
**State:** [in progress / blocked / completed]
**Work Done:** [bullet list]
**Next Step:** [immediate next action]
\`\`\`
```

**Why it works:** Claude fills in the brackets. Consistent output every time.

### 4. Precise Descriptions

Vague descriptions = unreliable auto-invocation.

| Bad | Good |
|-----|------|
| "Helps with code" | "Review code for security vulnerabilities and performance issues" |
| "Manages tasks" | "Create, search, update Jira tickets via REST API" |
| "Context helper" | "Prepare context handoff for next chat session" |

**Rule:** Include the *what* and *when* in the description.

### 5. Minimum Viable Tools

Only allow tools the skill actually needs:

| Skill Type | Tools |
|------------|-------|
| Read-only research | `Read, Grep, Glob` |
| File modification | `Read, Write, Edit` |
| External API | `Bash, Read, Write` |
| Full capability | Omit `allowed-tools` (inherits all) |

**Why it matters:** Prevents accidents, makes intent clear.

### 6. Idempotent Setup

Setup should be safe to run multiple times:

```bash
# Good: Only creates if missing
mkdir -p ai/memory && \
  [ -f ai/memory/file.md ] || printf 'content' > ai/memory/file.md

# Bad: Overwrites existing data
mkdir -p ai/memory && printf 'content' > ai/memory/file.md
```

### 7. Single Responsibility

One skill = one job. If you're writing "and" in the description, consider splitting.

| Instead of | Split into |
|------------|------------|
| "Review code and deploy" | `/review` + `/deploy` |
| "Search and update tickets" | `/jira search` + `/jira update` (or one skill with subcommands) |

### 8. Fail Gracefully

Include error handling guidance:

```markdown
## Error Handling

If environment variables are missing:
\`\`\`bash
echo "JIRA_URL: ${JIRA_URL:-(not set)}"
\`\`\`

**If missing**, guide user to add them to `~/.zshrc`.
```

---

## Skill vs Agent Decision

| Need | Use |
|------|-----|
| Needs conversation history | **Skill** (inline) |
| Output is for user to see/copy | **Skill** (inline) |
| Manual-only with side effects | **Skill** (`disable-model-invocation: true`) |
| Produces verbose output to isolate | **Agent** or **Skill** (`context: fork`) |
| Parallel execution needed | **Agent** |
| Specialized domain expertise | **Agent** (custom system prompt) |

**Rule of thumb:** If it needs to know what you discussed, use a Skill.

---

## Common Patterns

### Pattern 1: Manual-Only with Side Effects

```yaml
---
name: deploy
description: Deploy to production
disable-model-invocation: true
allowed-tools: Bash, Read
---
```

Use for: deployments, commits, deletions, sending messages.

### Pattern 2: Read-Only Research

```yaml
---
name: explore-auth
description: Research authentication patterns in codebase
allowed-tools: Read, Grep, Glob
context: fork
agent: Explore
---
```

Use for: codebase exploration, documentation lookup.

### Pattern 3: Background Knowledge

```yaml
---
name: coding-standards
description: Our team's coding conventions
user-invocable: false
---
```

Use for: conventions, standards, reference material Claude auto-loads.

### Pattern 4: Data Caching

```yaml
---
name: jira
description: Manage Jira tickets
allowed-tools: Bash, Read, Write
---

## Data Storage

API responses saved to `.claude/skills/jira/tickets/` for reliable parsing.

**Setup:**
\`\`\`bash
mkdir -p .claude/skills/jira/tickets && echo '*' > .claude/skills/jira/tickets/.gitignore
\`\`\`
```

Use for: API integrations where responses are large/truncated.

---

## Frontmatter Quick Combos

| Use Case | Frontmatter |
|----------|-------------|
| General utility | `name`, `description`, `allowed-tools` |
| Dangerous action | + `disable-model-invocation: true` |
| Background knowledge | + `user-invocable: false` |
| Research/exploration | + `context: fork`, `agent: Explore` |
| Cheap model for simple task | + `model: haiku` |

---

## Checklist: Before Shipping a Skill

- [ ] YAML frontmatter has `name` and `description`
- [ ] `disable-model-invocation: true` if it has side effects
- [ ] First-time setup section if it creates files/directories
- [ ] Setup uses `[ -f file ] ||` pattern to not overwrite
- [ ] Instructions are clear, step-by-step
- [ ] Output format is defined
- [ ] `allowed-tools` restricts to minimum needed
- [ ] No secrets/credentials in file (use env vars)
- [ ] Works when copied to fresh project

---

## Anti-Patterns to Avoid

### 1. Agent When You Need Context

**Wrong:** Creating an agent for something that needs conversation history.
```yaml
# This agent won't know what you discussed
name: summarize-session
description: Summarize what we talked about
```

**Right:** Use an inline skill - it sees the full conversation.

### 2. Vague Instructions

**Wrong:**
```markdown
Analyze the code and provide feedback.
```

**Right:**
```markdown
## Step 1: Identify Issues
Check for:
- [ ] Hardcoded credentials
- [ ] SQL injection vulnerabilities
- [ ] Missing input validation

## Step 2: Output
For each issue found:
| File:Line | Severity | Issue | Fix |
```

### 3. Missing Output Format

**Wrong:** "Generate a summary and save it."

**Right:** Show the exact template with `[placeholders]` Claude fills in.

### 4. Over-Permissive Tools

**Wrong:** Omitting `allowed-tools` for a read-only skill.

**Right:** `allowed-tools: Read, Grep, Glob` - explicit minimum.

### 5. Hardcoded Secrets

**Wrong:**
```markdown
Use API token: sk-abc123...
```

**Right:**
```markdown
## Pre-Flight Check
\`\`\`bash
echo "API_TOKEN: ${API_TOKEN:+set}"
\`\`\`
If not set, guide user to add to `~/.zshrc`.
```

### 6. No Setup Section

**Wrong:** Assuming directories exist.

**Right:** First-time setup that creates everything needed.

### 7. Auto-Invoke for Dangerous Actions

**Wrong:**
```yaml
name: deploy
description: Deploy to production  # Claude might auto-invoke!
```

**Right:**
```yaml
name: deploy
description: Deploy to production
disable-model-invocation: true  # Manual only
```

---

## References

- [Skills Documentation](https://code.claude.com/docs/en/skills)
- [Agent Skills Standard](https://agentskills.io)
- [tools-analysis.md](../claude-code/tools-analysis.md) - Full comparison of skills vs commands vs agents
