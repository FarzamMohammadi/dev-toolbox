---
name: commit
description: Analyze changes and create clear, descriptive commits with simple sentence messages
disable-model-invocation: true
argument-hint: [--staged | --all]
allowed-tools: Read, Bash
---

# Commit Skill

Analyze code changes, group them into logical commits, and create clear commit messages using simple, descriptive sentences.

---

## Pre-Flight Check

Verify git repository and current state:

```bash
git rev-parse --is-inside-work-tree 2>/dev/null && echo "Git repo: yes" || echo "Git repo: NO"
git status --porcelain | head -1 | grep -q . && echo "Changes: yes" || echo "Changes: NO"
```

**If not a git repository:** Inform user and exit.
**If no changes:** Inform user "Working tree clean. Nothing to commit." and exit.

---

## Phase 1: Gather Changes

### Step 1.1: Assess Current State

```bash
# Overview
git status --short

# Staged changes
git diff --cached --stat

# Unstaged changes
git diff --stat

# Untracked files
git ls-files --others --exclude-standard
```

### Step 1.2: Get Detailed Diffs

```bash
# Staged diff (always needed)
git diff --cached

# Unstaged diff (if --all flag or user wants to include)
git diff
```

### Step 1.3: Check Recent Commit Style

```bash
git log --oneline -10
```

---

## Phase 2: Analyze and Group Changes

### Core Principle

**One commit = one sentence description.** If changes can't be described in a single clear sentence, split them into multiple commits.

### Grouping Priority

| Priority | Criterion | Example |
|----------|-----------|---------|
| 1 | Feature cohesion | All files for user auth feature |
| 2 | Directory scope | All changes in `auth/` module |
| 3 | Logical separation | Config changes separate from code |
| 4 | Dependency order | Interface before implementation |

### Commit Sequence

When splitting into multiple commits, consider the logical order of changes:
- What change enables or defines the others?
- Would a reviewer understand each commit in isolation?
- Does the sequence tell a coherent story?

Order commits so earlier ones provide context for later ones.

### Split Decision

| Can describe in one sentence? | Action |
|-------------------------------|--------|
| Yes | Single commit |
| No - multiple unrelated changes | Split by concern |
| No - too complex | Split by logical phase |

**Examples of good single-sentence commits:**
- "Add OAuth2 authentication to login flow"
- "Update GitLab MR skill to fetch all comments"
- "Refactor design guide into modular directory structure"

**Example of when to split:**
- Updating a skill AND refactoring unrelated code → Two commits

---

## Phase 3: Present Commit Plan

### Commit Message Format

**Simple sentence style:**
- One clear, descriptive sentence
- **Capitalize first letter**
- **Capitalize names and titles** (Claude Code, GitLab, OAuth2, README, etc.)
- Imperative mood ("Add" not "Added")
- No period at end
- Max 72 characters (prefer under 50)
- Comprehensive but concise

**Good examples:**
- `Add fuzzy search to file finder`
- `Update Jira skill to support JQL queries`
- `Create modular skill design guide`
- `Fix null pointer in API response handler`

**Bad examples:**
- `fix bug` (too vague)
- `Updated the thing` (past tense, vague)
- `Add feature, fix bug, update docs` (multiple things - split it)

**Body (optional):**
- Only if subject can't capture full context
- Blank line after subject
- Explain WHY if not obvious
- Reference issues if applicable (`Refs: #123`)

### Output Format

Present plan to user:

```markdown
# Commit Plan

## Summary
- Commits proposed: [N]
- Files: [N]
- Changes: +[N] / -[N] lines

---

## Commit 1 of N

**Message:** `[Single descriptive sentence]`

**Files:**
| File | Change |
|------|--------|
| path/to/file.ts | Modified |

---

**Proceed?** [Y/n/edit]
```

---

## GATE: User Approval

**STOP and wait for explicit user confirmation before executing any commits.**

| Response | Action |
|----------|--------|
| "Y" / "yes" / "proceed" | Execute commits |
| "n" / "no" / "abort" | Cancel, no changes made |
| "edit" | Ask what to modify, re-present plan |
| Specific feedback | Incorporate changes, re-present |

---

## Phase 4: Execute Commits

### For Each Planned Commit

**Step 4.1: Stage files**
```bash
git add path/to/file1.ts path/to/file2.ts
```

**Step 4.2: Create commit**
```bash
git commit -m "Commit message here"
```

For multi-line messages (rare), use HEREDOC:
```bash
git commit -m "$(cat <<'EOF'
Subject line here

Body explaining why if needed.
EOF
)"
```

**Step 4.3: Verify**
```bash
git log -1 --oneline
```

### After All Commits

Report summary:

```markdown
# Commits Created

| # | Hash | Message |
|---|------|---------|
| 1 | abc1234 | Add OAuth2 authentication |
| 2 | def5678 | Update test configuration |

**Ready to push:** `git push`
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "not a git repository" | Not in git repo | Inform user, exit |
| "nothing to commit" | No changes | Inform user, exit gracefully |
| "pre-commit hook failed" | Hook rejected | Show hook output, suggest fixes |
| "merge conflict" | Unresolved conflicts | List files, abort |

---

## Usage

```
/commit              # Analyze all changes, propose commits
/commit --staged     # Only commit currently staged changes
/commit --all        # Include untracked files
```

### Examples

**Single logical change:**
```
$ /commit
# Proposes:
# 1. Add fuzzy search to command palette
```

**Multiple unrelated changes → split:**
```
$ /commit
# Proposes:
# 1. Update commit skill message format
# 2. Refactor skill design guide into modular structure
```
