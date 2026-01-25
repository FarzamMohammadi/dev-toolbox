# Skill Templates

Ready-to-use templates for creating new skills. Copy the appropriate template and customize.

---

## Template Selection

| Skill Type | Template | Use When |
|------------|----------|----------|
| Basic utility | [simple.md](simple.md) | Single operation, no external dependencies |
| External API | [api-based.md](api-based.md) | REST APIs, needs credentials |
| CLI wrapper | [multi-operation.md](multi-operation.md) | Multiple subcommands/operations |

Also see: [frontmatter-reference.md](frontmatter-reference.md) for complete field documentation.

---

## Quick Start

### 1. Choose a template

```bash
# Simple skill
cp __design-guide/templates/simple.md my-skill/skill.md

# API-based skill
cp __design-guide/templates/api-based.md my-skill/skill.md

# Multi-operation skill
cp __design-guide/templates/multi-operation.md my-skill/skill.md
```

### 2. Customize the template

1. Update YAML frontmatter (`name`, `description`)
2. Fill in `[placeholders]` with your content
3. Remove sections that don't apply
4. Add skill-specific operations

### 3. Test locally

```bash
# Run the skill
/my-skill [args]

# Check auto-invocation (if enabled)
# Ask Claude something that should trigger the skill
```

### 4. Deploy

```bash
cp my-skill/skill.md .claude/skills/my-skill/SKILL.md
```

---

## Template Comparison

| Feature | Simple | API-Based | Multi-Operation |
|---------|--------|-----------|-----------------|
| Complexity | Low | Medium | High |
| External APIs | No | Yes | Optional |
| Data caching | No | Yes | Optional |
| Multiple operations | No | Yes | Yes |
| Setup required | Minimal | Yes | Yes |
| Example skill | - | `jira/` | `glab-mr-manager/` |

---

## When to Create a README

Add a separate `README.md` when:
- Skill has multiple operations users need to reference
- Setup is complex or has multiple options
- External documentation or links are helpful
- Users need quick-reference outside of Claude

```
my-skill/
├── skill.md      # Main skill file
└── README.md     # User documentation (optional)
```

See `jira/README.md` or `glab-mr-manager/README.md` for examples.
