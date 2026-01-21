# Jira Skill Examples

## Common Workflows

### Daily Standup: Check My Work

```
"Show me my in-progress tickets"
```

JQL: `assignee = currentUser() AND status = "In Progress"`

### Sprint Review: Find Recent Completions

```
"List tickets I completed this week"
```

JQL: `assignee = currentUser() AND status = Done AND updated >= -7d`

### Bug Triage: Unassigned Bugs

```
"Find unassigned bugs in PROJECT"
```

JQL: `project = PROJECT AND issuetype = Bug AND assignee is EMPTY ORDER BY priority DESC`

### Create Bug from Error

```
"Create a bug in PROJECT: Login fails with 500 error on mobile Safari"
```

Will create:
- Project: PROJECT
- Type: Bug
- Summary: Login fails with 500 error on mobile Safari

### Quick Status Update

```
"Move PROJ-123 to In Progress and add comment: Starting work on this"
```

Two operations:
1. Transition to "In Progress"
2. Add comment

### Handoff Ticket

```
"Assign PROJ-123 to john.doe@company.com"
```

Update assignee field.

## JQL Quick Reference

### By Assignee

| Query | JQL |
|-------|-----|
| My tickets | `assignee = currentUser()` |
| Unassigned | `assignee is EMPTY` |
| Specific user | `assignee = "john.doe"` |

### By Status

| Query | JQL |
|-------|-----|
| Open | `status = Open` |
| In Progress | `status = "In Progress"` |
| Not Done | `status != Done` |
| Done this week | `status = Done AND updated >= -7d` |

### By Type

| Query | JQL |
|-------|-----|
| Bugs only | `issuetype = Bug` |
| Tasks only | `issuetype = Task` |
| Stories only | `issuetype = Story` |

### By Priority

| Query | JQL |
|-------|-----|
| Critical/Blocker | `priority in (Critical, Blocker)` |
| High priority | `priority = High` |
| Not low | `priority != Low` |

### By Time

| Query | JQL |
|-------|-----|
| Created today | `created >= startOfDay()` |
| Created this week | `created >= startOfWeek()` |
| Updated recently | `updated >= -24h` |
| Overdue | `duedate < now()` |

### Combined Examples

**Critical bugs in my project:**
```
project = PROJ AND issuetype = Bug AND priority in (Critical, Blocker)
```

**My open work, ordered by priority:**
```
assignee = currentUser() AND status != Done ORDER BY priority DESC, updated DESC
```

**Stale tickets (no updates in 30 days):**
```
project = PROJ AND status != Done AND updated <= -30d
```

**Recently created by me:**
```
reporter = currentUser() AND created >= -7d
```

## Request Examples

### Creating Tickets

**Simple task:**
```
Create a task in PROJ: Update documentation for new API
```

**Bug with details:**
```
Create a bug in PROJ:
Summary: Payment fails on checkout
Description: Users see error 500 when clicking Pay button. Affects production.
Priority: High
```

**Story with acceptance criteria:**
```
Create a story in PROJ:
Summary: User can export data to CSV
Description:
As a user, I want to export my data to CSV format.

Acceptance Criteria:
- Export button visible on dashboard
- CSV includes all visible columns
- Download starts immediately
```

### Searching

**Natural language to JQL:**
```
"Find all high priority bugs created this week in PROJECT"
→ project = PROJECT AND issuetype = Bug AND priority = High AND created >= startOfWeek()
```

```
"What's blocking the release?"
→ project = PROJECT AND status = "Blocked" OR labels = blocker
```

```
"Show me what John is working on"
→ assignee = "john.doe" AND status = "In Progress"
```

### Bulk Operations

**Get multiple tickets:**
```
"Get details for PROJ-101, PROJ-102, and PROJ-103"
```

JQL: `key in (PROJ-101, PROJ-102, PROJ-103)`

### Transitions

**Common status flows:**
```
To Do → In Progress → In Review → Done
To Do → In Progress → Blocked → In Progress → Done
```

Always fetch available transitions first - they vary by project workflow.

## Output Format Examples

### Ticket Details

```
PROJ-123: Login fails on mobile Safari
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: In Progress    Type: Bug    Priority: High
Assignee: John Doe     Reporter: Jane Smith
Created: Jan 15, 2024  Updated: Jan 20, 2024

Description:
Users report 500 error when logging in via mobile Safari.
Steps to reproduce:
1. Open Safari on iOS
2. Navigate to login page
3. Enter credentials
4. Click Login

Link: https://company.atlassian.net/browse/PROJ-123
```

### Search Results

```
Found 5 tickets:

Key       Status        Priority  Summary
────────  ────────────  ────────  ─────────────────────────────
PROJ-123  In Progress   High      Login fails on mobile Safari
PROJ-124  Open          Medium    Add dark mode support
PROJ-125  In Review     Low       Update copyright year
PROJ-126  Open          High      API rate limiting broken
PROJ-127  Blocked       Critical  Database migration failing
```

### After Creation

```
Created PROJ-128: Payment validation error handling

Type: Bug | Priority: Medium | Status: To Do
Link: https://company.atlassian.net/browse/PROJ-128
```
