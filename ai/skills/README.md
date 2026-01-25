# Skills

Claude Code skills for extending agent capabilities with specialized workflows.

## Directory

| Path | Purpose |
|------|---------|
| `__design-guide/` | Skill creation reference (start here for authoring) |
| `commit/` | Git commit workflow with smart grouping |
| `handoff/` | Session context handoff for continuity |
| `jira/` | Jira ticket management via REST API |
| `glab-mr-manager/` | GitLab MR lifecycle management |

## Creating Skills

**Start here:** [`__design-guide/start-here.md`](__design-guide/start-here.md)

Quick path:
1. Copy a template from `__design-guide/templates/`
2. Customize frontmatter and instructions
3. Test with `/skill-name`
4. Deploy to `.claude/skills/`

## For AI Agents

When creating or modifying skills, read `__design-guide/start-here.md` first. It provides:
- Specification (official + Claude Code extensions)
- Patterns for common skill types
- Ready-to-use templates
- Pre-shipping checklist

---

**Note:** Keep this README updated when adding, removing, or renaming skills in this directory.
