# API-Based Skill Template

Copy this template for skills that integrate with external REST APIs.

**Pattern reference:** [patterns/api-integration.md](../patterns/api-integration.md)

---

```yaml
---
name: [service-name]
description: Manage [service] resources via REST API. Use when user mentions [service], [keywords], or wants to [actions].
allowed-tools: Bash, Read, Write
argument-hint: [operation] [resource-id] [--flags]
---
```

```markdown
# [Service Name] Integration

Interact with [Service] via REST API.

## Pre-Flight Check

Verify credentials are configured:

\`\`\`bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null
echo "[SERVICE]_URL: ${[SERVICE]_URL:-(not set)}"
echo "[SERVICE]_TOKEN: ${[SERVICE]_TOKEN:+set}"
\`\`\`

**If not set**, add to your shell profile (`~/.zshrc` or `~/.bashrc`):

\`\`\`bash
export [SERVICE]_URL="https://api.[service].com"
export [SERVICE]_TOKEN="your-api-token"
\`\`\`

Then reload: `source ~/.zshrc`

## First-Time Setup

Create data cache directory:

\`\`\`bash
mkdir -p .claude/skills/[service]/data && \
  echo '*' > .claude/skills/[service]/data/.gitignore
\`\`\`

---

## Operations

### Get [Resource]

Fetch a single resource by ID.

\`\`\`bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; \
curl -s -H "Authorization: Bearer $[SERVICE]_TOKEN" \
  "$[SERVICE]_URL/api/[resources]/$RESOURCE_ID" \
  > .claude/skills/[service]/data/[resource].json
\`\`\`

Parse and display:

\`\`\`bash
jq '{
  id: .id,
  name: .name,
  status: .status,
  created: .created_at
}' .claude/skills/[service]/data/[resource].json
\`\`\`

**Output:**
| Field | Value |
|-------|-------|
| ID | [id] |
| Name | [name] |
| Status | [status] |
| URL | [link to resource] |

---

### List [Resources]

List resources with optional filters.

\`\`\`bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; \
curl -s -H "Authorization: Bearer $[SERVICE]_TOKEN" \
  "$[SERVICE]_URL/api/[resources]?status=active&limit=20" \
  > .claude/skills/[service]/data/[resources]-list.json
\`\`\`

Parse and display:

\`\`\`bash
jq '.items[] | {id: .id, name: .name, status: .status}' \
  .claude/skills/[service]/data/[resources]-list.json
\`\`\`

---

### Create [Resource]

Create a new resource.

\`\`\`bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; \
curl -s -X POST \
  -H "Authorization: Bearer $[SERVICE]_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$(cat <<'EOF'
{
  "name": "[resource-name]",
  "description": "[description]",
  "[field]": "[value]"
}
EOF
)" \
  "$[SERVICE]_URL/api/[resources]" \
  > .claude/skills/[service]/data/created-[resource].json
\`\`\`

---

### Update [Resource]

Update an existing resource.

\`\`\`bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; \
curl -s -X PUT \
  -H "Authorization: Bearer $[SERVICE]_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$(cat <<'EOF'
{
  "[field]": "[new-value]"
}
EOF
)" \
  "$[SERVICE]_URL/api/[resources]/$RESOURCE_ID" \
  > .claude/skills/[service]/data/updated-[resource].json
\`\`\`

---

### Delete [Resource]

Delete a resource by ID.

\`\`\`bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; \
curl -s -X DELETE \
  -H "Authorization: Bearer $[SERVICE]_TOKEN" \
  "$[SERVICE]_URL/api/[resources]/$RESOURCE_ID"
\`\`\`

---

## Output Guidelines

- Keep output concise
- Include URLs/links for user to open in browser
- Use tables for structured data
- Show status clearly (state, progress, etc.)

## Error Handling

| HTTP Code | Meaning | Resolution |
|-----------|---------|------------|
| 401 | Unauthorized | Check/regenerate API token |
| 403 | Forbidden | Verify user permissions |
| 404 | Not Found | Verify resource ID exists |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Retry later, check service status |

## Usage Examples

\`\`\`
/[service] get [id]
/[service] list --status=active
/[service] create --name="Name" --description="Desc"
/[service] update [id] --field=value
/[service] delete [id]
\`\`\`
```

---

## Customization Notes

### Authentication Types

Replace the `-H "Authorization: Bearer $TOKEN"` with your service's auth:

```bash
# Bearer token
-H "Authorization: Bearer $[SERVICE]_TOKEN"

# Basic auth
-u "$[SERVICE]_USER:$[SERVICE]_TOKEN"

# API key header
-H "X-API-Key: $[SERVICE]_API_KEY"

# Custom header
-H "[Service]-Auth: $[SERVICE]_TOKEN"
```

### Data Caching

Always save responses to files:

```bash
# Save to file (reliable)
curl ... > .claude/skills/[service]/data/response.json

# Then parse
jq '.field' .claude/skills/[service]/data/response.json
```

**Why:** Piping directly can truncate large responses.

### Multiple Environment Variables

For services needing multiple credentials:

```bash
echo "[SERVICE]_URL: ${[SERVICE]_URL:-(not set)}"
echo "[SERVICE]_USER: ${[SERVICE]_USER:-(not set)}"
echo "[SERVICE]_TOKEN: ${[SERVICE]_TOKEN:+set}"
echo "[SERVICE]_PROJECT: ${[SERVICE]_PROJECT:-(not set)}"
```

### Adding More Operations

For skills with many operations (10+), consider:

1. Grouping operations by type (Read/Write/Admin)
2. Creating a separate README.md for quick reference
3. Splitting into sections if approaching 500 lines
