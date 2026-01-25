# Example Skills

Reference examples for learning skill patterns and techniques.

---

## Local Examples

Skills in this repository demonstrating different patterns:

| Skill | Complexity | Pattern | Key Techniques |
|-------|------------|---------|----------------|
| [commit](../../commit/skill.md) | Medium | Git Operations | User approval gate, HEREDOC, multi-phase workflow |
| [handoff](../../handoff/skill.md) | Simple | Session Memory | Idempotent setup, memory files, starter prompts |
| [jira](../../jira/skill.md) | Complex | API Integration | Data caching, env vars, JQL queries, multiple operations |
| [glab-mr-manager](../../glab-mr-manager/skill.md) | Complex | Multi-Operation | Full lifecycle management, CLI wrapper, 15+ operations |

---

## By Complexity

### Simple Skills
- **[handoff](../../handoff/skill.md)** - Session context preservation
  - Single primary operation
  - Idempotent file setup
  - Memory file patterns

### Medium Skills
- **[commit](../../commit/skill.md)** - Git commit creation
  - Multi-phase workflow (Gather → Analyze → Present → Gate → Execute)
  - User approval gate
  - HEREDOC for multi-line messages

### Complex Skills
- **[jira](../../jira/skill.md)** - Jira REST API integration
  - 7+ operations (get, search, create, update, comment, transition)
  - Data caching to files
  - Environment variable authentication
  - Error handling table

- **[glab-mr-manager](../../glab-mr-manager/skill.md)** - GitLab MR lifecycle
  - 15+ operations covering full MR lifecycle
  - CLI wrapper pattern
  - Direct API access for advanced operations
  - Comprehensive documentation

---

## External Examples

### Anthropic Skills Repository

Production-quality examples from Anthropic:
https://github.com/anthropics/skills

| Skill | Description | Notable Features |
|-------|-------------|------------------|
| **pdf** | PDF processing | Scripts directory, reference files, forms handling |
| **mcp-builder** | MCP server creation | Multi-phase workflow, evaluation guide |
| **skill-creator** | Meta-skill for creating skills | Progressive disclosure, bundling patterns |
| **webapp-testing** | Playwright testing | Helper scripts, decision tree |
| **docx/xlsx/pptx** | Office document handling | Complex file manipulation |

### Skill Structure Examples

**Simple (single file):**
```
skill-name/
└── SKILL.md
```

**With references:**
```
pdf/
├── SKILL.md
├── forms.md
├── reference.md
└── LICENSE.txt
```

**With scripts:**
```
webapp-testing/
├── SKILL.md
├── scripts/
│   └── with_server.py
└── examples/
    └── *.py
```

**Full structure:**
```
mcp-builder/
├── SKILL.md
├── reference/
│   ├── spec.md
│   └── best-practices.md
├── scripts/
│   └── validate.py
└── LICENSE.txt
```

---

## Annotated Examples

Detailed breakdowns of selected skills:

- [pdf-skill.md](annotated/pdf-skill.md) - Complex skill with scripts and references
- [skill-creator.md](annotated/skill-creator.md) - Meta-skill showing progressive disclosure

---

## Learning Path

### Beginner
1. Read [handoff](../../handoff/skill.md) - simplest pattern
2. Understand idempotent setup
3. Try creating a simple skill from [templates/simple.md](../templates/simple.md)

### Intermediate
1. Read [commit](../../commit/skill.md) - approval gate pattern
2. Read [jira](../../jira/skill.md) - API integration pattern
3. Try creating an API skill from [templates/api-based.md](../templates/api-based.md)

### Advanced
1. Read [glab-mr-manager](../../glab-mr-manager/skill.md) - full lifecycle
2. Study Anthropic's [pdf](https://github.com/anthropics/skills/tree/main/skills/pdf) - scripts + references
3. Create a multi-operation skill with custom scripts

---

## Key Takeaways from Examples

### From `commit/`
- Always use approval gates for destructive operations
- Present plan before execution
- HEREDOC for multi-line content

### From `handoff/`
- `[ -f file ] ||` pattern for idempotent setup
- Append-only updates to memory files
- Generate starter prompts for next session

### From `jira/`
- Source shell profile before using env vars
- Save API responses to files, then parse
- Include error handling table
- Keep output concise with URLs

### From `glab-mr-manager/`
- Organize operations by lifecycle stage
- Include quick reference section
- Provide escape hatch for advanced API access
- Consider README.md for complex skills
