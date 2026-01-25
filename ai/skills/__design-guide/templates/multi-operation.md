# Multi-Operation Skill Template

Copy this template for skills with multiple subcommands or operations (like CLI wrappers).

**Pattern reference:** [patterns/api-integration.md](../patterns/api-integration.md)
**Example:** `glab-mr-manager/skill.md`

---

```yaml
---
name: [tool-name]
description: Manage [tool/service] [resources]. [Operations: list, create, update, delete]. Use when user mentions [tool], [keywords].
allowed-tools: Bash, Read, Write
argument-hint: [operation] [args] [--flags]
---
```

```markdown
# [Tool Name] Manager

Full lifecycle management for [resources] via [tool/CLI].

## Pre-Flight Check

Verify [tool] is installed and authenticated:

\`\`\`bash
# Check installation
command -v [tool] >/dev/null && echo "[tool] installed" || echo "[tool] not found"

# Check authentication
[tool] auth status
\`\`\`

**If not installed:**
\`\`\`bash
# macOS
brew install [tool]

# Or download from [url]
\`\`\`

**If not authenticated:**
\`\`\`bash
[tool] auth login
\`\`\`

## First-Time Setup

Create data cache (optional, for API responses):

\`\`\`bash
mkdir -p .claude/skills/[tool]/data && \
  echo '*' > .claude/skills/[tool]/data/.gitignore
\`\`\`

---

## Create Operations

### Create [Resource]

Create a new [resource] with options.

\`\`\`bash
[tool] [resource] create \
  --title "[title]" \
  --description "[description]" \
  --[option]="[value]"
\`\`\`

**Common flags:**
| Flag | Purpose |
|------|---------|
| `--title` | [Resource] title |
| `--description` | Detailed description |
| `--draft` | Create as draft |
| `--[option]` | [Description] |

---

## Read Operations

### List [Resources]

List [resources] with filters.

\`\`\`bash
[tool] [resource] list \
  --state=open \
  --author=@me \
  --limit=20
\`\`\`

**Filter options:**
| Filter | Values | Description |
|--------|--------|-------------|
| `--state` | open, closed, all | Filter by state |
| `--author` | username, @me | Filter by author |
| `--assignee` | username, @me | Filter by assignee |
| `--limit` | number | Max results |

---

### View [Resource]

View details of a specific [resource].

\`\`\`bash
[tool] [resource] view [ID]
\`\`\`

For detailed output:
\`\`\`bash
[tool] [resource] view [ID] --comments
\`\`\`

---

### View [Resource] Diff/Changes

View changes or diff for a [resource].

\`\`\`bash
[tool] [resource] diff [ID]
\`\`\`

---

## Update Operations

### Update [Resource] Metadata

Update title, description, or other metadata.

\`\`\`bash
[tool] [resource] update [ID] \
  --title "[new title]" \
  --description "[new description]"
\`\`\`

---

### Add [Related Item]

Add reviewers, labels, assignees, etc.

\`\`\`bash
# Add single
[tool] [resource] update [ID] --add-[item]="[value]"

# Add multiple
[tool] [resource] update [ID] --add-[item]="[value1]" --add-[item]="[value2]"
\`\`\`

---

### Add Comment

Add a comment to a [resource].

\`\`\`bash
[tool] [resource] comment [ID] --message "[comment text]"
\`\`\`

For multi-line comments, use HEREDOC:
\`\`\`bash
[tool] [resource] comment [ID] --message "$(cat <<'EOF'
## Comment Title

Comment body with **markdown** support.

- Point 1
- Point 2
EOF
)"
\`\`\`

---

## Workflow Operations

### Approve [Resource]

Approve a [resource] (if applicable).

\`\`\`bash
[tool] [resource] approve [ID]
\`\`\`

---

### Merge/Complete [Resource]

Merge or complete a [resource].

\`\`\`bash
[tool] [resource] merge [ID]
\`\`\`

**Merge options:**
| Flag | Purpose |
|------|---------|
| `--squash` | Squash commits |
| `--rebase` | Rebase before merge |
| `--delete-branch` | Delete source branch |
| `--when-pipeline-succeeds` | Wait for CI |

---

### Close [Resource]

Close without merging/completing.

\`\`\`bash
[tool] [resource] close [ID]
\`\`\`

---

### Reopen [Resource]

Reopen a closed [resource].

\`\`\`bash
[tool] [resource] reopen [ID]
\`\`\`

---

## Advanced Operations

### Direct API Access

For operations not covered by CLI:

\`\`\`bash
[tool] api [METHOD] [endpoint] --field [key]=[value]
\`\`\`

Example:
\`\`\`bash
[tool] api GET /projects/:id/[resources]
[tool] api POST /projects/:id/[resources] --field title="New"
\`\`\`

---

## Output Guidelines

- **Be concise** - Show essential info, not full API responses
- **Include URLs** - Users often want to open in browser
- **Show state clearly** - Status, progress, approval state
- **Use tables** for structured data

Example output:
\`\`\`
[Resource] #123: [Title]
Status: [state] | Author: [user] | Created: [date]
URL: [link]

[Brief description or summary]
\`\`\`

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "not found" | Invalid ID | Verify [resource] ID exists |
| "permission denied" | Insufficient access | Check user permissions |
| "not authenticated" | Auth expired | Run `[tool] auth login` |
| "conflict" | State conflict | Check current state, refresh |

---

## Quick Reference

| Operation | Command |
|-----------|---------|
| List | `[tool] [resource] list` |
| View | `[tool] [resource] view [ID]` |
| Create | `[tool] [resource] create --title "..."` |
| Update | `[tool] [resource] update [ID] --[field]="..."` |
| Comment | `[tool] [resource] comment [ID] --message "..."` |
| Approve | `[tool] [resource] approve [ID]` |
| Merge | `[tool] [resource] merge [ID]` |
| Close | `[tool] [resource] close [ID]` |
```

---

## Customization Notes

### Organizing Operations

Group by lifecycle stage:
1. **Create** - New resource creation
2. **Read** - List, view, search
3. **Update** - Modify metadata, add related items
4. **Workflow** - State transitions (approve, merge, close)
5. **Advanced** - API access, bulk operations

### When to Add README.md

Add separate user documentation when:
- 10+ operations
- Complex setup with multiple options
- Users need quick reference card
- External links or detailed examples helpful

### Handling Long Skills

If approaching 500 lines:
1. Move detailed examples to separate files
2. Create `references/` directory for advanced docs
3. Keep SKILL.md as overview with links
