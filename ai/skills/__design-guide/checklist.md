# Pre-Shipping Checklist

Verify these items before deploying a skill.

---

## Required

- [ ] **YAML frontmatter** has `name` and `description`
- [ ] **`name`** matches directory name
- [ ] **`name`** uses only lowercase letters, numbers, hyphens
- [ ] **`description`** includes WHAT the skill does
- [ ] **`description`** includes WHEN to use it
- [ ] **`description`** written in third person

---

## Safety

- [ ] **`disable-model-invocation: true`** if skill has side effects
  - Deployments, commits, deletions, sending messages
- [ ] **`allowed-tools`** restricts to minimum needed
  - Read-only: `Read, Grep, Glob`
  - File modification: `Read, Write, Edit`
  - External API: `Bash, Read, Write`
- [ ] **No secrets/credentials** in file (use env vars)
- [ ] **Pre-flight check** verifies prerequisites before running

---

## Quality

- [ ] **Instructions are clear**, step-by-step
- [ ] **Output format** is explicitly defined with `[placeholders]`
- [ ] **Error handling** section included
- [ ] **SKILL.md body** under 500 lines
- [ ] **Terminology** is consistent throughout
- [ ] **No time-sensitive information** (or in "old patterns" section)

---

## Portability

- [ ] **First-time setup section** if skill creates files/directories
- [ ] **Setup uses `[ -f file ] ||` pattern** to not overwrite existing
- [ ] **Works when copied** to fresh project
- [ ] **Forward slashes** in all paths (no backslashes)
- [ ] **No hardcoded paths** specific to one machine

---

## Documentation

- [ ] **README.md** for user-facing documentation (if complex skill)
- [ ] **Usage examples** included
- [ ] **Common error resolutions** documented

---

## Testing

- [ ] **Tested manually** via `/command`
- [ ] **Auto-invocation tested** (if enabled) - does description trigger correctly?
- [ ] **Edge cases** considered
- [ ] **Fresh project test** - works when copied to new project

---

## Quick Reference: Common Issues

| Issue | Fix |
|-------|-----|
| Skill doesn't auto-invoke | Make description more specific with keywords |
| Skill invokes unexpectedly | Add `disable-model-invocation: true` |
| Output format varies | Add explicit template with `[placeholders]` |
| Setup overwrites files | Use `[ -f file ] || create` pattern |
| Works locally, fails elsewhere | Remove hardcoded paths, add setup section |
| Too verbose output | Use `context: fork` for isolation |
