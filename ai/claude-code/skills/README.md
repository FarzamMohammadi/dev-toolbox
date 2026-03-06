# Skills

Claude Code skills for extending agent capabilities with specialized workflows.

## Directory

| Path | Purpose |
|------|---------|
| `__design-guide/` | Skill creation reference (start here for authoring) |
| `commit/` | Git commit workflow with smart grouping |
| `finalize-changes/` | Holistic review of completed work to elevate quality |
| `glab-mr-manager/` | GitLab MR lifecycle management |
| `handoff/` | Session context handoff for continuity |
| `improve-skill/` | Reflect on a skill's performance and iterate on improvements |
| `jira-ticket-manager/` | Jira ticket management via REST API |
| `literary-editor/` | Transform drafts into polished English |
| `modularize-document/` | Transform monolithic markdown into modular index + detail files |
| `refactor-code/` | Review git diffs against refactoring principles |
| `review-pr/` | Find bugs in branch changes — races, logic errors, security holes |
| `summarize/` | Distill files, URLs, and videos into thorough value-preserving summaries |
| `work-diary/` | Create work diary entries from session context |
| `wrap-session/` | Capture session context and generate continuation prompt |

## Creating Skills

**Start here:** [`__design-guide/start-here.md`](__design-guide/start-here.md)

Quick path:
1. Copy a template from `__design-guide/templates/`
2. Customize frontmatter and instructions
3. Test with `/skill-name`
4. Deploy to `.claude/skills/`
   > **Note:** Dev uses `skill.md`. Rename to `SKILL.md` when installing for use (official spec).

## For AI Agents

When creating or modifying skills, read `__design-guide/start-here.md` first. It provides:
- Specification (official + Claude Code extensions)
- Patterns for common skill types
- Ready-to-use templates
- Pre-shipping checklist

---

**Note:** Keep this README updated when adding, removing, or renaming skills in this directory.
