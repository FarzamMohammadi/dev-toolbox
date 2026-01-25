# Session Memory Pattern

For skills that capture and preserve session context, learnings, and decisions.

**Local example:** `handoff/skill.md`

---

## Pattern Overview

```
┌─────────────────┐
│  First-Time     │ → Create memory file structure (idempotent)
│  Setup          │
├─────────────────┤
│  Gather         │ → Collect session intelligence
│  Intelligence   │   (conversation history, decisions, learnings)
├─────────────────┤
│  Update         │ → Append to memory files
│  Memory         │
├─────────────────┤
│  Generate       │ → Create starter prompt for next session
│  Output         │
└─────────────────┘
```

---

## Structure Template

```yaml
---
name: session-skill
description: [Capture/preserve] session context for [purpose]. Use when user wants to [action].
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash
argument-hint: [optional-notes]
---
```

```markdown
# Session [Skill Name]

## First-Time Setup

Create memory structure (safe to run multiple times):

\`\`\`bash
mkdir -p ai/memory && \
  [ -f ai/memory/session-history.md ] || printf '# Session History\n\nChronological record of sessions.\n\n---\n' > ai/memory/session-history.md && \
  [ -f ai/memory/learnings.md ] || printf '# Learnings\n\nAccumulated knowledge about this project.\n\n---\n' > ai/memory/learnings.md && \
  [ -f ai/memory/decisions.md ] || printf '# Decisions\n\nArchitectural and design decisions.\n\n---\n' > ai/memory/decisions.md
\`\`\`

## Step 1: Gather Session Intelligence

Review the conversation to identify:

### Session Summary
- **Goal**: What was the user trying to accomplish?
- **State**: In progress / blocked / completed
- **Work Done**: Key actions taken
- **Blockers**: Any issues encountered

### Learnings
- Codebase patterns discovered
- User preferences observed
- Technical constraints identified

### Decisions Made
- Architectural choices
- Design decisions
- Trade-offs accepted

## Step 2: Update Memory Files

### Session History
Append to `ai/memory/session-history.md`:

\`\`\`markdown
## [DATE] - [Brief Title]

**Goal:** [what user was trying to accomplish]
**State:** [in progress / blocked / completed]

**Work Done:**
- [bullet list of completed items]

**Next Step:** [immediate next action]

---
\`\`\`

### Learnings
Append to `ai/memory/learnings.md`:

\`\`\`markdown
## [Category] - [DATE]

[Learning content]

---
\`\`\`

### Decisions
Append to `ai/memory/decisions.md`:

\`\`\`markdown
## [Decision Title] - [DATE]

**Context:** [Why this decision was needed]
**Decision:** [What was decided]
**Rationale:** [Why this choice]
**Alternatives Considered:** [Other options]

---
\`\`\`

## Step 3: Generate Output

### Starter Prompt for Next Session

\`\`\`markdown
## Context

[Brief summary of where things stand]

## Recent Work

- [Key item 1]
- [Key item 2]

## Immediate Next Steps

1. [Next action]
2. [Following action]

## Reference

- Session history: ai/memory/session-history.md
- Learnings: ai/memory/learnings.md
- Decisions: ai/memory/decisions.md
\`\`\`
```

---

## Key Techniques

### 1. Idempotent Setup

**Critical:** Setup must be safe to run multiple times.

```bash
# Pattern: [ -f file ] || create_file
mkdir -p ai/memory && \
  [ -f ai/memory/history.md ] || printf 'initial content' > ai/memory/history.md
```

**Why:** Users might run the skill on existing projects. Never overwrite their data.

### 2. Append-Only Updates

Memory files should grow over time, not be overwritten:

```markdown
## Step 2: Update Session History

**Append** to the end of `ai/memory/session-history.md`:
[new content]

Do not overwrite existing entries.
```

### 3. Date Stamping

Include dates for chronological tracking:

```markdown
## 2025-01-15 - Authentication Implementation

**Goal:** Add JWT authentication
...
```

### 4. Structured Categories

Organize learnings and decisions by category:

```markdown
# Learnings

## Architecture - 2025-01-15
[learning about architecture]

## Testing - 2025-01-14
[learning about testing approach]

## Performance - 2025-01-13
[learning about performance patterns]
```

---

## Real-World Example: Handoff Pattern

From `handoff/skill.md`:

```markdown
## Step 1: Gather Session Intelligence

Review the conversation to identify:

1. **Session Summary**
   - Main goal the user was working toward
   - Current state (in progress / blocked / completed)
   - Key files modified or discussed
   - Immediate next steps

2. **Learnings About This Codebase**
   - Code patterns unique to this project
   - User preferences (formatting, naming, etc.)
   - Technical constraints discovered

3. **Decisions Made**
   - Architectural choices discussed
   - Design decisions agreed upon
   - Trade-offs accepted

## Step 2: Write to Memory Files

### Session History Entry

Append to `ai/memory/session-history.md`:

\`\`\`markdown
## [DATE] - [Brief descriptive title]

**Goal:** [Main objective]
**State:** [in progress / blocked / completed]

**Work Done:**
- [Completed item 1]
- [Completed item 2]

**Next Step:** [Immediate next action]

**Key Files:**
- [file1.ts] - [what changed]
- [file2.ts] - [what changed]

---
\`\`\`
```

---

## Memory File Structure

### Recommended Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `session-history.md` | Chronological work log | Every session |
| `learnings.md` | Accumulated knowledge | When discoveries made |
| `decisions.md` | Architectural decisions | When decisions made |

### Optional Additional Files

| File | Purpose |
|------|---------|
| `preferences.md` | User preferences (style, tools) |
| `blockers.md` | Known issues and workarounds |
| `references.md` | External docs, links, resources |

### File Location Options

```
# Option 1: Project-scoped (recommended)
ai/memory/
├── session-history.md
├── learnings.md
└── decisions.md

# Option 2: Hidden directory
.claude/memory/
├── session-history.md
└── ...

# Option 3: Docs integration
docs/ai/
├── session-history.md
└── ...
```

---

## Starter Prompt Generation

The skill should generate a prompt for the next session:

```markdown
## Starter Prompt

Copy this to start the next session:

---

## Context

I'm continuing work on [project]. Previous session on [date] focused on [topic].

## Current State

[Brief summary]

## Next Steps

1. [Immediate next action]
2. [Following action]

## References

Read these for context:
- ai/memory/session-history.md (recent: last 3 entries)
- ai/memory/decisions.md (if architectural questions arise)

---
```

---

## Checklist for Memory Skills

- [ ] `disable-model-invocation: true` (requires user context)
- [ ] First-time setup is idempotent (`[ -f file ] ||` pattern)
- [ ] Memory files are appended, not overwritten
- [ ] Entries include dates for chronological tracking
- [ ] Clear categories for different types of information
- [ ] Starter prompt generated for next session
- [ ] File structure documented for user reference
- [ ] Works when copied to fresh project
