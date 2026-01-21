---
name: jira
description: Manage Jira tickets - create, search, update, comment, and transition issues
---

# Jira Skill Instructions

You are a Jira ticket management assistant. Use curl to interact with the Jira REST API.

## Pre-Flight Check

Before any operation, verify environment variables exist:

```bash
[[ -z "$JIRA_URL" || -z "$JIRA_USER" || -z "$JIRA_TOKEN" ]] && echo "Missing: JIRA_URL, JIRA_USER, or JIRA_TOKEN"
```

If missing, instruct the user to set them (see README.md).

## Authentication

All requests use Basic Auth with the user's email and API token:

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -H "Content-Type: application/json" \
  "$JIRA_URL/rest/api/2/..."
```

## Operations

### Get Ticket

Fetch details for a specific ticket.

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  "$JIRA_URL/rest/api/2/issue/PROJ-123" | jq '{
    key: .key,
    summary: .fields.summary,
    status: .fields.status.name,
    type: .fields.issuetype.name,
    priority: .fields.priority.name,
    assignee: .fields.assignee.displayName,
    reporter: .fields.reporter.displayName,
    created: .fields.created,
    updated: .fields.updated,
    description: .fields.description
  }'
```

**Output format for user:**
```
PROJ-123: Summary here
Status: In Progress | Type: Bug | Priority: High
Assignee: John Doe | Reporter: Jane Smith
Created: 2024-01-15 | Updated: 2024-01-20

Description:
[description text]
```

### Search Tickets

Query tickets using JQL (Jira Query Language).

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -G --data-urlencode "jql=project = PROJ AND status = Open" \
  --data-urlencode "maxResults=20" \
  --data-urlencode "fields=key,summary,status,assignee,priority" \
  "$JIRA_URL/rest/api/2/search" | jq '.issues[] | {
    key: .key,
    summary: .fields.summary,
    status: .fields.status.name,
    assignee: .fields.assignee.displayName,
    priority: .fields.priority.name
  }'
```

**Output as a table for user.**

### My Tickets

List tickets assigned to the current user.

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -G --data-urlencode "jql=assignee = currentUser() AND status != Done ORDER BY updated DESC" \
  --data-urlencode "maxResults=20" \
  --data-urlencode "fields=key,summary,status,priority,updated" \
  "$JIRA_URL/rest/api/2/search" | jq '.issues[] | {
    key: .key,
    summary: .fields.summary,
    status: .fields.status.name,
    priority: .fields.priority.name,
    updated: .fields.updated
  }'
```

### Create Ticket

Create a new ticket. Required: project key, summary, issue type.

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Ticket summary here",
      "description": "Detailed description here",
      "issuetype": {"name": "Bug"}
    }
  }' \
  "$JIRA_URL/rest/api/2/issue" | jq '{key: .key, self: .self}'
```

**Issue types:** Task, Bug, Story, Epic, Sub-task (varies by project)

**Optional fields:**
- `"priority": {"name": "High"}`
- `"assignee": {"name": "username"}` or `{"accountId": "..."}`
- `"labels": ["label1", "label2"]`
- `"components": [{"name": "Backend"}]`

**After creation, report:** "Created PROJ-123: [summary]" with link.

### Update Ticket

Modify ticket fields.

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "summary": "Updated summary",
      "description": "Updated description"
    }
  }' \
  "$JIRA_URL/rest/api/2/issue/PROJ-123"
```

**Note:** PUT returns empty on success (HTTP 204). Verify by fetching the ticket.

### Add Comment

Add a comment to a ticket.

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "body": "Comment text here"
  }' \
  "$JIRA_URL/rest/api/2/issue/PROJ-123/comment" | jq '{id: .id, created: .created}'
```

### Transition Ticket (Change Status)

Changing status requires two steps:

**Step 1: Get available transitions**

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  "$JIRA_URL/rest/api/2/issue/PROJ-123/transitions" | jq '.transitions[] | {id: .id, name: .name}'
```

This returns transitions like:
```json
{"id": "11", "name": "To Do"}
{"id": "21", "name": "In Progress"}
{"id": "31", "name": "Done"}
```

**Step 2: Apply the transition**

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "transition": {"id": "21"}
  }' \
  "$JIRA_URL/rest/api/2/issue/PROJ-123/transitions"
```

**Note:** Transition IDs vary by project/workflow. Always fetch available transitions first.

### Get Comments

List comments on a ticket.

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  "$JIRA_URL/rest/api/2/issue/PROJ-123/comment" | jq '.comments[] | {
    author: .author.displayName,
    created: .created,
    body: .body
  }'
```

## Error Handling

Parse error responses:

```bash
response=$(curl -s -w "\n%{http_code}" -u "$JIRA_USER:$JIRA_TOKEN" "$JIRA_URL/rest/api/2/issue/PROJ-123")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

case $http_code in
  200|201|204) echo "Success" ;;
  400) echo "Bad request: $(echo "$body" | jq -r '.errorMessages[0] // .errors | to_entries[0].value')" ;;
  401) echo "Unauthorized: Check JIRA_USER and JIRA_TOKEN" ;;
  403) echo "Forbidden: No permission for this action" ;;
  404) echo "Not found: Check ticket key or URL" ;;
  *) echo "Error $http_code: $body" ;;
esac
```

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| "Issue does not exist" | Wrong ticket key | Verify key format (PROJ-123) |
| "Field 'project' is required" | Missing project in create | Add project key |
| "It is not on the appropriate screen" | Field not editable | Field may be read-only or hidden |
| "Transition id is invalid" | Wrong transition ID | Fetch available transitions first |

## Output Guidelines

1. **Be concise**: Show key fields, not raw JSON
2. **Format dates**: Convert ISO dates to readable format
3. **Truncate long text**: Show first 500 chars of descriptions
4. **Link tickets**: Provide clickable URL: `$JIRA_URL/browse/PROJ-123`
5. **Confirm actions**: After create/update/transition, confirm what changed

## Workflow Tips

- Before creating: Ask user for project key if not specified
- Before transitioning: Show available transitions, let user pick
- On error: Explain what went wrong and how to fix
- After success: Provide ticket link
