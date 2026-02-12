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
# Appends to ~/.zshrc
printf '\nexport N8N_URL="https://n8n.example.com"\nexport N8N_API_KEY="your-api-key"\n' >> ~/.zshrc && source ~/.zshrc
```

Do NOT ask users to paste credentials directly—the key should stay in their shell profile.

## Data Storage

API responses are saved to `.claude/skills/n8n-manager/data/` for reliable parsing (n8n responses are large and get truncated when piped).

**First-time setup** (creates directory + gitignore):
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

**Be extremely surgical.** n8n workflows are complex JSON structures—modifying the wrong node, connection, or setting can silently break a workflow. Before editing:
1. Identify the **exact** node(s) or field(s) that need to change
2. Edit **only** those fields—do not reformat, reorder, or touch anything else
3. Never regenerate the full workflow JSON from scratch; always modify the fetched copy in-place

Push a modified workflow JSON back to n8n. The JSON file must contain the full workflow body (`name`, `nodes`, `connections`, `settings`).

**Step 0: Snapshot before editing**

Before making any edits, save a copy of the original fetched workflow for later comparison:
```bash
cp .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID.json \
   .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID-before.json
```

Then make your surgical edits to `workflow-WORKFLOW_ID.json`.

**Step 1: Pre-push diff — confirm only intended changes**

Before pushing, diff the original against your modified version to verify nothing unexpected changed:
```bash
diff <(jq --sort-keys . .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID-before.json) \
     <(jq --sort-keys . .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID.json)
```

Review the diff carefully. If **any** unintended changes appear, fix them before proceeding. Do NOT push until the diff shows only the intended modifications.

**Step 2: Push update**
```bash
curl -s -X PUT \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @.claude/skills/n8n-manager/data/workflow-WORKFLOW_ID.json \
  "$N8N_URL/api/v1/workflows/WORKFLOW_ID" \
  -o .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID-updated.json
```

**Step 3: Post-push verification — pull and compare**

Re-fetch the workflow from n8n and diff against the pre-edit snapshot to confirm only intended changes landed:
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_URL/api/v1/workflows/WORKFLOW_ID" \
  -o .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID-verify.json
```
```bash
diff <(jq --sort-keys 'del(.updatedAt, .versionId)' .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID-before.json) \
     <(jq --sort-keys 'del(.updatedAt, .versionId)' .claude/skills/n8n-manager/data/workflow-WORKFLOW_ID-verify.json)
```

Report the diff to the user. The only differences should be the fields you intentionally changed (plus server-managed fields like `updatedAt` and `versionId` which are excluded above). If unexpected changes appear, investigate immediately.

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

## API Reference

The full OpenAPI spec is bundled at `openapi.json` in this skill directory. **Only read it** when:
- The user needs an operation not covered above (credentials, variables, users, data tables, source control, projects)
- You need exact query parameters, request body schemas, or response shapes
- The user asks about an endpoint you're unsure of

Do NOT load the spec for routine workflow/execution/tag operations—use the examples above instead.

## Output Guidelines

1. **Be concise**: Show key fields, not raw JSON
2. **Format dates**: Use `[0:10]` slice for YYYY-MM-DD or `[0:19]` for datetime
3. **Link workflows**: `$N8N_URL/workflow/WORKFLOW_ID`
4. **Show node counts**: Summarize workflow complexity
5. **Cache files**: Always mention where the full JSON is saved so users can inspect it
