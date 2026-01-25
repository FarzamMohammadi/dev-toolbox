# API Integration Pattern

For skills that interact with external REST APIs (Jira, GitLab, GitHub, Slack, etc.)

**Local examples:** `jira/skill.md`, `glab-mr-manager/skill.md`

---

## Pattern Overview

```
┌─────────────────┐
│  Pre-Flight     │ → Verify credentials, check authentication
├─────────────────┤
│  First-Time     │ → Create cache directories, .gitignore
│  Setup          │
├─────────────────┤
│  Operations     │ → Individual API operations (CRUD)
├─────────────────┤
│  Error          │ → Common issues and resolutions
│  Handling       │
└─────────────────┘
```

---

## Structure Template

```yaml
---
name: api-service
description: Manage [service] resources via REST API. Use when user mentions [service], [keywords].
allowed-tools: Bash, Read, Write
argument-hint: [operation] [args]
---
```

```markdown
# [Service] Integration

## Pre-Flight Check

Before any operation, verify credentials:

\`\`\`bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null
echo "SERVICE_URL: ${SERVICE_URL:-(not set)}"
echo "SERVICE_TOKEN: ${SERVICE_TOKEN:+set}"
\`\`\`

**If missing**, guide user to add to shell profile:
\`\`\`bash
export SERVICE_URL="https://api.service.com"
export SERVICE_TOKEN="your-token"
\`\`\`

## First-Time Setup

Create data cache directory:

\`\`\`bash
mkdir -p .claude/skills/service/data && \
  echo '*' > .claude/skills/service/data/.gitignore
\`\`\`

## Operations

### Get Resource

\`\`\`bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; \
curl -s -H "Authorization: Bearer $SERVICE_TOKEN" \
  "$SERVICE_URL/api/resource/$ID" > .claude/skills/service/data/resource.json
\`\`\`

Parse and present:
\`\`\`bash
jq '{id: .id, name: .name, status: .status}' .claude/skills/service/data/resource.json
\`\`\`

### Create Resource
...

### Update Resource
...

## Output Format

Present results concisely:

| Field | Value |
|-------|-------|
| ID | [resource-id] |
| Name | [resource-name] |
| Status | [status] |
| URL | [link-to-resource] |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| 401 Unauthorized | Invalid/expired token | Regenerate token, update env var |
| 404 Not Found | Resource doesn't exist | Verify ID/key |
| 403 Forbidden | Insufficient permissions | Check user permissions |
```

---

## Key Techniques

### 1. Shell Profile Sourcing

**Always** source shell profile before using env vars:

```bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; <command>
```

**Why:** Claude's bash sessions don't automatically load shell profile.

### 2. Data Caching

Save API responses to files for reliable parsing:

```bash
# Save to file
curl ... > .claude/skills/service/data/response.json

# Parse from file
jq '.field' .claude/skills/service/data/response.json
```

**Why:**
- Avoids truncation in piped output
- Enables complex jq parsing
- User can inspect raw responses
- Subsequent commands can reference same data

### 3. Gitignore for Cache

Always create `.gitignore` in cache directories:

```bash
mkdir -p .claude/skills/service/data && \
  echo '*' > .claude/skills/service/data/.gitignore
```

**Why:** Prevents sensitive API responses from being committed.

### 4. Pre-Flight Credential Check

Check credentials before any operation:

```bash
echo "SERVICE_URL: ${SERVICE_URL:-(not set)}"
echo "SERVICE_TOKEN: ${SERVICE_TOKEN:+set}"
```

Pattern explanation:
- `${VAR:-(not set)}` → Shows "not set" if VAR is empty
- `${VAR:+set}` → Shows "set" if VAR has value (doesn't expose the value)

### 5. HEREDOC for Multi-Line Data

Use HEREDOC for creating/updating with bodies:

```bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; \
curl -s -X POST \
  -H "Authorization: Bearer $SERVICE_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$(cat <<'EOF'
{
  "title": "Resource title",
  "description": "Description here"
}
EOF
)" \
  "$SERVICE_URL/api/resources"
```

---

## Real-World Example: Jira Pattern

From `jira/skill.md`:

```markdown
## Get Ticket

\`\`\`bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; \
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  "$JIRA_URL/rest/api/2/issue/$TICKET_KEY?expand=changelog" \
  > .claude/skills/jira/tickets/$TICKET_KEY.json
\`\`\`

Parse key fields:
\`\`\`bash
jq '{
  key: .key,
  summary: .fields.summary,
  status: .fields.status.name,
  assignee: .fields.assignee.displayName,
  priority: .fields.priority.name
}' .claude/skills/jira/tickets/$TICKET_KEY.json
\`\`\`
```

---

## Multi-Operation Skills

For skills with many operations (like GitLab MR manager), organize by lifecycle:

```markdown
## Create Operations
- Create MR
- Create from issue

## Read Operations
- List MRs
- View MR details
- View diff

## Update Operations
- Update title/description
- Add reviewers
- Add labels

## Workflow Operations
- Approve
- Merge
- Rebase
- Close/Reopen
```

Consider splitting into separate sections or files if > 500 lines.

---

## Common API Patterns

### Pagination

```bash
# Get first page
curl ... "$SERVICE_URL/api/items?page=1&per_page=50"

# Note in skill: "If more results exist, increment page parameter"
```

### Search/Filter

```bash
# With query parameters
curl ... "$SERVICE_URL/api/items?status=open&assignee=me"

# With body (POST search)
curl -X POST -d '{"query": "search term"}' "$SERVICE_URL/api/search"
```

### Authentication Types

```bash
# Bearer token
-H "Authorization: Bearer $TOKEN"

# Basic auth
-u "$USER:$TOKEN"

# API key header
-H "X-API-Key: $API_KEY"
```

---

## Checklist for API Skills

- [ ] Pre-flight check verifies credentials without exposing values
- [ ] Shell profile sourced before every command using env vars
- [ ] Cache directory created with .gitignore
- [ ] Large responses saved to files, not piped directly
- [ ] Error handling table covers common HTTP errors
- [ ] Output format shows essential fields concisely
- [ ] URLs included in output for user to open in browser
