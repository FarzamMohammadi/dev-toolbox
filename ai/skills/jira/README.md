# Jira Skill

Lightweight Jira ticket management for Claude Code using curl + jq.

## Setup

### 1. Get API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Name it (e.g., "Claude Code")
4. Copy the token

### 2. Set Environment Variables

Add to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.):

```bash
export JIRA_URL="https://your-company.atlassian.net"
export JIRA_USER="your-email@company.com"
export JIRA_TOKEN="your-api-token"
```

Then reload: `source ~/.zshrc`

### 3. Verify Setup

```bash
# Test connection
curl -s -u "$JIRA_USER:$JIRA_TOKEN" "$JIRA_URL/rest/api/2/myself" | jq .displayName
```

## Usage

Ask Claude to use the Jira skill:

- "Use the Jira skill to list my open tickets"
- "Create a Jira bug in PROJECT: description here"
- "Get details for PROJ-123"
- "Add a comment to PROJ-123"
- "Move PROJ-123 to In Progress"

## Operations

| Operation | Description |
|-----------|-------------|
| Create | Create new tickets with project, type, summary, description |
| Get | Fetch full ticket details by key |
| Search | Query tickets using JQL |
| My Tickets | List tickets assigned to current user |
| Update | Modify ticket fields (summary, description, assignee, etc.) |
| Comment | Add comments to tickets |
| Transition | Change ticket status (To Do → In Progress → Done) |

## Dependencies

- `curl` - HTTP requests (standard on macOS/Linux)
- `jq` - JSON parsing (install: `brew install jq` or `apt install jq`)
- `base64` - Auth encoding (standard utility)

## Files

- `skill.md` - Claude instructions (read this when using the skill)
- `examples.md` - Common workflows and JQL patterns

## Troubleshooting

**401 Unauthorized**: Check JIRA_USER (must be email) and JIRA_TOKEN

**403 Forbidden**: User lacks permission for that project/action

**404 Not Found**: Check JIRA_URL or ticket key

**Connection refused**: Verify JIRA_URL is correct (include https://)
