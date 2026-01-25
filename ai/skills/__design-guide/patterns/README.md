# Skill Patterns

Pattern library for common skill types. Choose the pattern that matches your use case.

---

## Pattern Selection Matrix

| Your Skill Needs | Pattern | Local Example |
|------------------|---------|---------------|
| REST API integration | [api-integration.md](api-integration.md) | `jira/`, `glab-mr-manager/` |
| Git/VCS operations | [git-operations.md](git-operations.md) | `commit/` |
| Session context capture | [session-memory.md](session-memory.md) | `handoff/` |

---

## Quick Reference

### API Integration Pattern
For skills that interact with external REST APIs (Jira, GitLab, GitHub, etc.)

**Key characteristics:**
- Pre-flight check for credentials
- Shell profile sourcing for env vars
- Data caching for large responses
- Structured error handling

**Example skills:** `jira/`, `glab-mr-manager/`

### Git Operations Pattern
For skills that perform git commands (commit, branch, merge, etc.)

**Key characteristics:**
- Gather → Analyze → Present → Gate → Execute workflow
- User approval gate before execution
- HEREDOC for multi-line messages
- Pre-flight check for git repo

**Example skill:** `commit/`

### Session Memory Pattern
For skills that capture and preserve session context

**Key characteristics:**
- Idempotent file setup
- Memory file structure (history, learnings, decisions)
- Starter prompt generation
- Append-only updates

**Example skill:** `handoff/`

---

## Choosing a Pattern

```
Do you call external APIs?
├── Yes → api-integration.md
└── No
    ├── Git operations? → git-operations.md
    └── Session/memory? → session-memory.md
```

If none of these fit, start with [templates/simple.md](../templates/simple.md) and customize.
