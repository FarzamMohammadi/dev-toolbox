# Skills

Claude Code skills for extending agent capabilities with specialized workflows.

## RRPIR Workflow

**Requirements → Research → Plan → Implement → Review**

A structured development workflow that adds Requirements Gathering before and Review after the
standard RPI cycle. Each phase has a dedicated skill, and together they form a complete pipeline
from "what are we building?" to "is it ready to ship?"

| Phase | Skill | Purpose |
|-------|-------|---------|
| **R** — Requirements | [`rrpir/requirements-gathering/`](rrpir/requirements-gathering/) | Extract intent, constraints, edge cases through sequential questioning |
| **R** — Research | [`rrpir/research/`](rrpir/research/) | Investigate codebases with facts-before-opinions discipline |
| **P** — Plan | [`rrpir/create-plan/`](rrpir/create-plan/) | Design decisions + tasks, stakes-calibrated, stress-tested by expert panel |
| **I** — Implement | *(use Claude Code directly, then `/commit`)* | Execute the plan, commit with `/commit` |
| **R** — Review | [`rrpir/review/`](rrpir/review/) | Automated checks, coverage analysis, bug verification, manual testing prep |

**Supporting skills used within RRPIR:**

| Skill | Used by | Purpose |
|-------|---------|---------|
| [`expert-panel-review/`](expert-panel-review/) | `/create-plan` | Multi-perspective critique from independent panelists |
| [`review-pr/`](review-pr/) | `/review` | Bug hunting in branch diffs — races, logic errors, security holes |
| [`commit/`](commit/) | Implement phase | Git commits with smart grouping and clear descriptions |

Artifacts are stored in `.claude/temp/<skill_name>/` — project-local, grouped per skill,
gitignore-friendly.

## Other Skills

| Path | Purpose |
|------|---------|
| `excalidraw/` | Generate `.excalidraw` JSON diagrams from prompts |
| `finalize-changes/` | Holistic review of completed work to elevate quality |
| `glab-mr-manager/` | GitLab MR lifecycle management |
| `gws/` | Google Workspace operations — Gmail, Docs, Sheets, Drive via gws CLI |
| `handoff/` | Session context handoff for continuity |
| `improve-skill/` | Reflect on a skill's performance and iterate on improvements |
| `jira-ticket-manager/` | Jira ticket management via REST API |
| `literary-editor/` | Transform drafts into polished English |
| `modularize-document/` | Transform monolithic markdown into modular index + detail files |
| `n8n-manager/` | Manage n8n workflows via REST API — list, fetch, update, activate, debug |
| `refactor-code/` | Review git diffs against refactoring principles |
| `repo-docs-overhaul/` | Overhaul repo documentation for clarity, navigability, and OSS-readiness |
| `summarize/` | Distill files, URLs, and videos into thorough value-preserving summaries |
| `system-layer-extraction/` | Deep architectural investigation — extract and map every system in a codebase |
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
