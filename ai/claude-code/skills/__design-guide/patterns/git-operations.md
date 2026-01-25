# Git Operations Pattern

For skills that perform git commands (commit, branch, push, merge, etc.)

**Local example:** `commit/skill.md`

---

## Pattern Overview

```
┌─────────────────┐
│  Pre-Flight     │ → Verify git repo, check status
├─────────────────┤
│  Gather         │ → Collect changes (diff, status, log)
├─────────────────┤
│  Analyze        │ → Group changes, determine approach
├─────────────────┤
│  Present        │ → Show plan to user
├─────────────────┤
│  Gate           │ → Wait for user approval
├─────────────────┤
│  Execute        │ → Perform git operations
└─────────────────┘
```

---

## Structure Template

```yaml
---
name: git-operation
description: [Operation] for git repositories. Use when user wants to [action].
disable-model-invocation: true
allowed-tools: Read, Bash
argument-hint: [--flag] [args]
---
```

**Key:** Always include `disable-model-invocation: true` for git operations that modify state.

```markdown
# Git [Operation]

## Pre-Flight Check

Verify we're in a git repository:

\`\`\`bash
git rev-parse --is-inside-work-tree
\`\`\`

If not a git repo, inform user and stop.

## Step 1: Gather Changes

Collect information about current state:

\`\`\`bash
# Staged changes
git diff --cached --stat

# Unstaged changes
git diff --stat

# Untracked files
git status --porcelain | grep '^??'

# Recent commits for style reference
git log --oneline -5
\`\`\`

## Step 2: Analyze

[Instructions for analyzing gathered information]

## Step 3: Present Plan

Show the user what will happen:

\`\`\`
Proposed [operation]:

1. [First action]
2. [Second action]
3. [Third action]

Affected files:
- path/to/file1.ts
- path/to/file2.ts
\`\`\`

## Step 4: User Approval

**Ask the user to confirm before proceeding:**

> Ready to [operation]. Proceed? (Y/n/edit)

- **Y** → Execute the plan
- **n** → Abort
- **edit** → Let user modify the plan

## Step 5: Execute

Only after approval:

\`\`\`bash
git [command]
\`\`\`

## Output Format

After completion:

\`\`\`
✓ [Operation] complete

[Summary of what was done]
- [detail 1]
- [detail 2]

[Hash/reference if applicable]
\`\`\`
```

---

## Key Techniques

### 1. User Approval Gate

**Critical:** Never execute git operations that modify state without explicit user approval.

```markdown
## Step 4: User Approval

Present the plan and wait for confirmation:

> Ready to commit. Proceed? (Y/n/edit)

**Only proceed after explicit "Y" or "yes" response.**
```

### 2. HEREDOC for Multi-Line Messages

Use HEREDOC for commit messages with body:

```bash
git commit -m "$(cat <<'EOF'
feat(auth): implement JWT authentication

- Add login endpoint
- Add token validation middleware
- Add refresh token support

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Why:** Preserves formatting, handles special characters, multi-line support.

### 3. Atomic Operations

Group related operations with `&&`:

```bash
git add file1.ts file2.ts && \
git commit -m "message" && \
git push origin branch
```

**Why:** If any step fails, subsequent steps don't execute.

### 4. Safe Status Checks

Check state before modifying:

```bash
# Check for uncommitted changes
git status --porcelain

# Check if branch exists
git rev-parse --verify branch-name

# Check if remote exists
git remote get-url origin
```

---

## Real-World Example: Commit Pattern

From `commit/skill.md`:

```markdown
## Step 1: Gather Git State

\`\`\`bash
# Get all changes
git status --porcelain

# Get staged diff
git diff --cached

# Get unstaged diff
git diff

# Get recent commit messages for style
git log --oneline -10
\`\`\`

## Step 2: Analyze Changes

Group changes by:
1. **Feature** - Related functionality
2. **File type** - Tests separate from implementation
3. **Scope** - Module or component affected

## Step 3: Present Commit Plan

\`\`\`
Proposed commits:

1. feat(auth): add login endpoint
   Files: src/auth/login.ts, src/auth/types.ts

2. test(auth): add login tests
   Files: tests/auth/login.test.ts

Proceed? (Y/n/edit)
\`\`\`

## Step 4: Execute

For each approved commit:
\`\`\`bash
git add [files] && \
git commit -m "$(cat <<'EOF'
[type]([scope]): [description]

[body if needed]

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
\`\`\`
```

---

## Common Git Operations

### Commit with Co-Author

```bash
git commit -m "$(cat <<'EOF'
type(scope): description

Body text here.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Interactive Staging (Avoid)

**Don't use `-i` flags** - they require interactive input:

```bash
# Wrong - requires interactive input
git add -i
git rebase -i

# Right - specify files directly
git add file1.ts file2.ts
```

### Branch Operations

```bash
# Create and switch
git checkout -b feature/new-feature

# Push with upstream
git push -u origin feature/new-feature
```

### Stash Operations

```bash
# Stash with message
git stash push -m "WIP: description"

# List stashes
git stash list

# Apply specific stash
git stash apply stash@{0}
```

---

## Safety Guidelines

### Never Without Approval

- `git commit` (any flags)
- `git push` (any flags)
- `git reset` (especially `--hard`)
- `git rebase`
- `git merge`
- `git branch -d/-D`
- `git stash drop/clear`

### Safe to Run Anytime

- `git status`
- `git diff` (read-only)
- `git log`
- `git branch` (list only)
- `git remote -v`
- `git rev-parse`

### Dangerous - Extra Caution

- `git push --force` → Warn user explicitly
- `git reset --hard` → Warn about data loss
- `git clean -fd` → Warn about untracked file deletion

---

## Checklist for Git Skills

- [ ] `disable-model-invocation: true` in frontmatter
- [ ] Pre-flight check verifies git repo
- [ ] State gathered before any modifications
- [ ] Plan presented to user before execution
- [ ] Explicit approval gate (Y/n/edit pattern)
- [ ] HEREDOC used for multi-line commit messages
- [ ] Co-Author-By included in commits
- [ ] No interactive flags (`-i`)
- [ ] Dangerous operations have extra warnings
