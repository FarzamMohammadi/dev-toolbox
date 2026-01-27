---
name: rpi-research
description: Performs architecture-first codebase research before code modifications. Produces validated research documents with "Needs Attention" tables. Use when investigating a ticket or feature before planning.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
argument-hint: [TICKET or topic]
---

# RPI Research

Architecture-first codebase research that prevents "grep and modify" mistakes. Produces validated research documents with categorized findings and explicit "Needs Attention" tables.

## Purpose

This skill prevents common mistakes like:
- Modifying sub-agents when you should modify entry points
- Editing dead code that's no longer called
- Making changes in the wrong architectural layer

## Related Skills

This skill is part of the **RPI Workflow** (Research -> Plan -> Implement):
- **Current:** `/rpi-research` — Creates research document
- **Next:** `/rpi-plan` — Creates implementation plan from research
- **Then:** `/rpi-implement` — Executes the plan

---

## Process Overview

```
Phase 1: Scope Definition
    ↓
Phase 2: Architecture Discovery (ASK FIRST)
    ↓
Phase 3: Targeted Search
    ↓
[GATE] Architecture Validation
    ↓
Phase 4: Detailed Analysis
    ↓
[GATE] Final Validation
    ↓
Phase 7: Generate Document
```

---

## Phase 1: Scope Definition

### Required Information

Before searching, gather:

1. **Task Goal**: What change/feature is being investigated?
2. **Research Type**:
   - External (APIs, libraries, documentation)
   - Codebase (architecture, implementation patterns)
   - Both

### Questions to Ask

```
To conduct effective research, I need to understand:

1. What is the specific goal? (e.g., "Add X feature", "Fix Y bug", "Understand Z system")
2. Is this primarily external research (APIs, docs) or codebase investigation?
3. Are there any known starting points (files, functions, tickets)?
```

**DO NOT PROCEED** until you have clear answers to these questions.

---

## Phase 2: Architecture Discovery

**CRITICAL**: Ask about architecture BEFORE searching the codebase.

### Required Questions

```
Before I search, I need to understand the architecture:

1. **Entry Points vs Sub-agents**:
   - Does this system use orchestrators that delegate to sub-agents?
   - If so, what's the entry point for [TASK AREA]?

2. **Flow Direction**:
   - Where do requests enter the system?
   - What components are downstream?

3. **Known Patterns**:
   - Are there existing patterns for similar functionality?
   - Any files/modules I should specifically look at first?
```

### Why This Matters

| If you skip this... | You might... |
|---------------------|--------------|
| Don't ask about entry points | Modify a sub-agent when the change belongs in the orchestrator |
| Don't ask about flow | Add code in the wrong layer |
| Don't ask about patterns | Violate existing conventions |

**DO NOT PROCEED** to searching until architecture is understood.

---

## Phase 3: Targeted Search

### Search Strategy

Execute searches based on architecture understanding:

1. **Start at entry points** identified in Phase 2
2. **Follow call chains** downstream
3. **Categorize each finding** as you go

### Finding Categories

For EACH file/function found, immediately categorize:

| Category | Description | Example |
|----------|-------------|---------|
| `ENTRY_POINT` | Request enters here | API route, CLI command, event handler |
| `ORCHESTRATOR` | Coordinates flow | Main controller, workflow manager |
| `SUB_AGENT` | Delegated task handler | Specialized processor called by orchestrator |
| `UTILITY` | Shared helper | Formatting, validation, common operations |
| `DEAD_CODE` | Not called anywhere | Legacy, orphaned, deprecated |
| `OUT_OF_SCOPE` | Not relevant to task | Unrelated functionality |

### Recording Format

```markdown
| File | Category | Evidence | Called By |
|------|----------|----------|-----------|
| api/handler.py | ENTRY_POINT | HTTP route decorator | External requests |
| services/orchestrator.py | ORCHESTRATOR | Calls sub_agent_a, sub_agent_b | api/handler.py:45 |
| agents/sub_agent_a.py | SUB_AGENT | Single responsibility | orchestrator.py:78 |
```

---

## GATE: Architecture Validation

**STOP AND VALIDATE** before proceeding to detailed analysis.

### Present to User

```markdown
## Architecture Understanding

Based on my research, here's the system architecture:

### Flow Diagram
[Request] -> [ENTRY_POINT: file.py] -> [ORCHESTRATOR: coord.py] -> [SUB_AGENTS: a.py, b.py]

### Categorized Findings

| File | Category | Why | Relevant to Task? |
|------|----------|-----|-------------------|
| ... | ... | ... | Yes/No |

### Proposed Modification Points

For [TASK], I believe changes should go in:
- **Primary**: [file.py] because [reason]
- **Secondary**: [other.py] because [reason]

### Files I'm EXCLUDING and why:
- [excluded.py]: This is a SUB_AGENT, changes should go in ORCHESTRATOR
- [old.py]: This is DEAD_CODE, not called anywhere

**Is this architecture understanding correct?**
```

**DO NOT PROCEED** until user confirms the categorization is accurate.

---

## Phase 4: Detailed Analysis

### For Each Relevant File

After validation, read and document:

1. **Exact line numbers** for relevant code
2. **Function signatures** that may need modification
3. **Dependencies** that would be affected
4. **Test coverage** for the area

### Documentation Format

```markdown
### [filename.py]

**Purpose**: [One-line description]
**Category**: [From Phase 3]
**Called by**: [List callers with line numbers]
**Calls**: [List callees]

**Relevant Code Sections**:

Lines 45-67: `process_request()` function
- Handles: [what it does]
- Current behavior: [describe]
- Potential modification point: [if applicable]

Lines 120-135: `validate_input()` function
- Note: Helper used by process_request
```

### Verify Code is Active

For EACH function you plan to document:

```bash
# Search for calls to this function
grep -r "function_name(" --include="*.py" .
```

If no callers found, mark as `DEAD_CODE` and note in exclusions.

---

## GATE: Final Validation

### "Needs Attention" Table

Present a summary table highlighting items requiring user attention:

```markdown
## Needs Attention

| Item | Question | Why It Matters |
|------|----------|----------------|
| `orchestrator.py:process()` | Is this the right entry point? | All sub-agents called from here |
| `sub_agent.py` | Should changes go here or in orchestrator? | Unclear boundary |
| `config.py:SETTING` | Is this deprecated? No references found | Might be dead code |
| `legacy_handler.py` | Include or exclude? | Unclear if still used |

**Please confirm or correct these items before I proceed to generate the research document.**
```

### Required Confirmations

Before generating the final document:

1. [ ] User confirmed entry points are correct
2. [ ] User confirmed sub-agents vs orchestrators categorization
3. [ ] User confirmed exclusions are appropriate
4. [ ] User answered all "Needs Attention" questions

**DO NOT PROCEED** until all confirmations received.

---

## Phase 5: Generate Document

### Output Location

```
thoughts/shared/research/YYYY-MM-DD-[TICKET]-description.md
```

### Document Structure

Use the template at [references/document-template.md](references/document-template.md).

Key sections:
1. **Summary**: One paragraph overview
2. **Architecture**: Flow diagram and component relationships
3. **Findings Table**: All categorized findings with line numbers
4. **Modification Points**: Recommended locations for changes
5. **Exclusions**: What was found but explicitly excluded and WHY
6. **Open Questions**: Anything still unclear
7. **Next Steps**: Pointer to `/rpi-plan`

---

## Anti-Pattern Prevention

This skill specifically prevents:

| Anti-Pattern | How This Skill Prevents It |
|--------------|---------------------------|
| "Found 5 files, modified all" | Requires categorization before any modification |
| "Added to sub-agent instead of orchestrator" | Phase 2 asks specifically about entry points vs sub-agents |
| "Modified dead code" | Phase 4 requires verifying each function is called |
| "Unclear scope boundaries" | GATE checkpoints force explicit validation |
| "Lost context between sessions" | Document persists to `thoughts/shared/research/` |

---

## Error Recovery

### If Search Returns Too Many Results

1. Stop and ask user to narrow scope
2. Don't proceed with "I'll figure it out" mentality
3. Explicitly list what you found and ask which areas to focus on

### If Architecture Is Unclear

1. Stop at Phase 2 gate
2. Ask specific questions about unclear parts
3. Don't guess at component relationships

### If User Disagrees with Categorization

1. Update categorization based on user input
2. Re-validate before proceeding
3. Document the correction in the research output

---

## Output Verification Checklist

Before completing, verify:

- [ ] Every finding has a category assigned
- [ ] Every potential modification point has a line number
- [ ] Dead code is identified and excluded
- [ ] Sub-agents vs entry points are clearly distinguished
- [ ] All "Needs Attention" items have been resolved
- [ ] Document is written to `thoughts/shared/research/`
- [ ] Next step pointer to `/rpi-plan` is included
