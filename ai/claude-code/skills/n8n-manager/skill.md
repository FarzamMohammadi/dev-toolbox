---
name: n8n-manager
description: Manage n8n workflows via REST API — list, fetch, update, activate, and debug executions. Use when user mentions n8n, workflows, automations, or workflow executions.
allowed-tools: Bash, Read, Write
argument-hint: [operation] [workflow-id] [--flags]
---

# n8n Workflow Manager

Interact with n8n via its public REST API. All requests use `curl` with the `X-N8N-API-KEY` header.

## Pre-Flight Check

Verify environment variables are set (source the shell profile first):

```bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; echo "N8N_URL: ${N8N_URL:-(not set)}"; echo "N8N_API_KEY: ${N8N_API_KEY:+set}"
```

**If variables are missing**, guide the user to add them to `~/.zshrc`:

```bash
printf '\nexport N8N_URL="https://n8n.example.com"\nexport N8N_API_KEY="your-api-key"\n' >> ~/.zshrc && source ~/.zshrc
```

Do NOT ask users to paste credentials directly—the key should stay in their shell profile.

## First-Time Setup

Create data cache directory:

```bash
mkdir -p .claude/skills/n8n-manager/data && echo '*' > .claude/skills/n8n-manager/data/.gitignore
```

**Files stored:**
- `workflow-{id}.json` — Full workflow JSON
- `workflows-list.json` — Most recent list result
- `executions-list.json` — Most recent executions list
- `execution-{id}.json` — Individual execution data

Users can delete the `data/` folder anytime to clear cached data.

## Command Pattern

Every command must source the shell profile first:

```bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; <curl command>
```

All examples below omit this prefix for brevity—**always include it**.

## Operations

### List Workflows

**Step 1: Fetch and save**
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_URL/api/v1/workflows?limit=100" \
  -o .claude/skills/n8n-manager/data/workflows-list.json
```

**Optional query params:** `active=true|false`, `tags=tag1,tag2`, `name=search-term`, `limit=N` (max 250)

**Step 2: Parse**
```bash
jq '.data[] | {id: .id, name: .name, active: .active, updatedAt: .updatedAt[0:10], tags: [.tags[]?.name]}' \
  .claude/skills/n8n-manager/data/workflows-list.json
```

Output as a table with columns: ID, Name, Active, Updated, Tags.

### Get Workflow

Fetch a full workflow by ID and save to cache for inspection or round-trip editing.

**Step 1: Fetch and save**
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_URL/api/v1/workflows/WORKFLOW_ID" \
  -o .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID.json
```

**Step 2: Parse summary**
```bash
jq '{
  id: .id,
  name: .name,
  active: .active,
  createdAt: .createdAt[0:10],
  updatedAt: .updatedAt[0:10],
  nodeCount: (.nodes | length),
  nodeTypes: [.nodes[].type] | unique,
  tags: [.tags[]?.name]
}' .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID.json
```

**Output format:**
```
Workflow WORKFLOW_ID: Name Here
Active: true | Nodes: 12 | Updated: 2024-06-15
Tags: production, athena
Node types: n8n-nodes-base.webhook, n8n-nodes-base.httpRequest, ...

Full JSON saved to .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID.json
```

To inspect individual nodes, read the cached JSON file directly.

### Update Workflow

Push a modified workflow JSON back to n8n. The JSON file must contain the full workflow body (`name`, `nodes`, `connections`, `settings`).

**Step 1: Update**
```bash
curl -s -X PUT \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @.claude/skills/n8n-manager/data/workflow-WORKFLOW_ID.json \
  "$N8N_URL/api/v1/workflows/WORKFLOW_ID" \
  -o .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID-updated.json
```

**Step 2: Verify**
```bash
jq '{id: .id, name: .name, active: .active, updatedAt: .updatedAt}' \
  .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID-updated.json
```

If the workflow is published, the updated version is automatically re-published.

### Activate Workflow

```bash
curl -s -X POST \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_URL/api/v1/workflows/WORKFLOW_ID/activate" \
  | jq '{id: .id, name: .name, active: .active}'
```

### Deactivate Workflow

```bash
curl -s -X POST \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_URL/api/v1/workflows/WORKFLOW_ID/deactivate" \
  | jq '{id: .id, name: .name, active: .active}'
```

### List Executions

**Step 1: Fetch and save**
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_URL/api/v1/executions?limit=20" \
  -o .claude/skills/n8n-manager/data/executions-list.json
```

**Optional query params:** `workflowId=ID`, `status=success|error|running|waiting|canceled`, `limit=N` (max 250), `includeData=true`

**Step 2: Parse**
```bash
jq '.data[] | {id: .id, workflowId: .workflowId, status: .status, mode: .mode, startedAt: .startedAt[0:19], stoppedAt: .stoppedAt[0:19]}' \
  .claude/skills/n8n-manager/data/executions-list.json
```

Output as a table with columns: ID, Workflow, Status, Mode, Started, Stopped.

### Get Execution

**Step 1: Fetch and save**
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_URL/api/v1/executions/EXECUTION_ID?includeData=true" \
  -o .claude/skills/n8n-manager/data/execution-EXECUTION_ID.json
```

**Step 2: Parse summary**
```bash
jq '{
  id: .id,
  workflowId: .workflowId,
  status: .status,
  mode: .mode,
  finished: .finished,
  startedAt: .startedAt,
  stoppedAt: .stoppedAt
}' .claude/skills/n8n-manager/data/execution-EXECUTION_ID.json
```

To inspect full execution data (node inputs/outputs), read the cached JSON file directly.

### List Tags

```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_URL/api/v1/tags?limit=100" \
  | jq '.data[] | {id: .id, name: .name}'
```

## Error Handling

Check responses for error fields. Common issues:

| HTTP Code | Meaning | Resolution |
|-----------|---------|------------|
| 401 | Unauthorized | Check `N8N_API_KEY` is valid |
| 403 | Forbidden | API key lacks permission for this operation |
| 404 | Not Found | Verify workflow/execution ID exists |
| 400 | Bad Request | Check JSON body — `name`, `nodes`, `connections`, `settings` are required for updates |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Retry later, check n8n instance health |

## Output Guidelines

1. **Be concise**: Show key fields, not raw JSON
2. **Format dates**: Use `[0:10]` slice for YYYY-MM-DD or `[0:19]` for datetime
3. **Link workflows**: `$N8N_URL/workflow/WORKFLOW_ID`
4. **Show node counts**: Summarize workflow complexity
5. **Cache files**: Always mention where the full JSON is saved so users can inspect it
