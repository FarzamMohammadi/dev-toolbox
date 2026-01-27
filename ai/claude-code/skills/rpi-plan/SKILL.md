---
name: rpi-plan
description: Transforms research documents into self-contained implementation plans with explicit scope boundaries and excluded components. Use when creating an implementation plan from completed research.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Write
argument-hint: [research-path]
---

# RPI Plan

Transforms research documents into self-contained implementation plans that can be executed without additional context. Plans include explicit scope boundaries, excluded components with reasons, and verification commands.

## Purpose

This skill ensures implementation plans:
- Are self-contained (don't require re-reading the codebase)
- Have explicit scope boundaries (what we're NOT doing)
- List excluded components with clear reasons
- Include verification commands for each phase
- Can be executed by `/rpi-implement` without ambiguity

## Related Skills

This skill is part of the **RPI Workflow** (Research -> Plan -> Implement):
- **Previous:** `/rpi-research` — Creates research document
- **Current:** `/rpi-plan` — Creates implementation plan from research
- **Next:** `/rpi-implement` — Executes the plan

---

## Process Overview

```
Phase 1: Pre-flight Check
    ↓
[GATE] Research Selection
    ↓
Phase 2: Gather Context
    ↓
[GATE] Architecture Validation
    ↓
Phase 3: Draft Plan
    ↓
[GATE] Plan Approval
    ↓
Phase 4: Write Document
```

---

## Phase 1: Pre-flight Check

### Locate Research Document

If argument provided:
```
1. Check if [argument] is a file path
2. Check if it's a ticket ID (search thoughts/shared/research/ for matching files)
3. If neither found, ask user for clarification
```

If no argument:
```
1. List recent research documents in thoughts/shared/research/
2. Ask user which one to use
```

### Validate Research Document

Confirm the research document contains:

| Required Section | Purpose |
|------------------|---------|
| Architecture Overview | Understanding of system flow |
| Categorized Findings | Entry points, orchestrators, sub-agents identified |
| Modification Points | Where changes should go |
| Exclusions | What was found but excluded |

If any section is missing:
```
The research document is missing: [sections]

This information is required to create a reliable plan. Options:
1. Re-run /rpi-research to complete the research
2. Provide the missing information now
```

**DO NOT PROCEED** with incomplete research.

---

## GATE: Research Selection

### Present Research Summary

```markdown
## Research Document Found

**File**: [path/to/research.md]
**Date**: [creation date]
**Task**: [task description from research]

### Key Findings Summary

- **Entry Points**: [list]
- **Modification Points**: [count] identified
- **Exclusions**: [count] items excluded

### Architecture from Research

[Brief architecture summary]

**Is this the correct research to base the plan on?**
```

**DO NOT PROCEED** until user confirms research selection.

---

## Phase 2: Gather Context

### Extract from Research

From the research document, extract:

1. **Modification Points** (with exact file:line references)
2. **Architecture Relationships** (what calls what)
3. **Exclusions** (and their reasons)
4. **Open Questions** (to address in plan)
5. **Test Coverage** (existing tests to update)

### Verify Current State

For each modification point:

```bash
# Read the current state of the file
Read [file_path]

# Verify the line numbers still match
# (code may have changed since research)
```

If code has changed since research:
```
The code at [file:line] has changed since research was conducted.

Research expected: [expected code]
Current code: [actual code]

Options:
1. Update plan to reflect current code
2. Re-run /rpi-research with fresh codebase state
```

**DO NOT PROCEED** if significant drift detected without user decision.

---

## GATE: Architecture Validation

### Confirm Understanding

Present the architecture understanding extracted from research:

```markdown
## Architecture Confirmation

Based on the research document, I understand the architecture as:

### Flow
[Request] -> [Entry Point] -> [Orchestrator] -> [Sub-agents]

### Modification Strategy

Changes will be made to:
| Component | Type | Why Here |
|-----------|------|----------|
| [file.py] | ENTRY_POINT | [Reason from research] |
| [coord.py] | ORCHESTRATOR | [Reason from research] |

Changes will NOT be made to:
| Component | Type | Why Excluded |
|-----------|------|--------------|
| [sub.py] | SUB_AGENT | Changes belong in orchestrator per research |
| [old.py] | DEAD_CODE | Not called anywhere |

**Is this modification strategy correct?**
```

**DO NOT PROCEED** until user confirms the strategy.

---

## Phase 3: Draft Plan

### Required Sections

The plan MUST include ALL of the following:

#### 1. What We're NOT Doing

This section is **MANDATORY**. It prevents scope creep and makes boundaries explicit.

```markdown
## What We're NOT Doing

| Excluded Item | Reason | Where It Would Go Instead |
|---------------|--------|---------------------------|
| [Feature X] | Out of scope for this ticket | Future ticket PROJ-456 |
| [Refactoring Y] | Would expand scope beyond task | Could be separate PR |
| [Fix Z] | Unrelated bug found during research | Create separate issue |
```

#### 2. Excluded Components

This section is **MANDATORY**. It documents findings that won't be modified.

```markdown
## Excluded Components

**These files/functions were found in research but are explicitly NOT being modified:**

| Component | Category | Why Excluded |
|-----------|----------|--------------|
| [sub_agent.py:process()] | SUB_AGENT | Per architecture, changes go in orchestrator |
| [legacy_handler.py] | DEAD_CODE | Function not called; modifying would have no effect |
| [config_v1.py] | DEPRECATED | Replaced by config_v2.py; not used |
| [unrelated.py:helper()] | OUT_OF_SCOPE | Different feature area |
```

#### 3. Implementation Phases

Each phase MUST include:

```markdown
### Phase [N]: [Phase Name]

**Goal**: [What this phase accomplishes]

**Pre-conditions**:
- [What must be true before starting]

**Files to Modify**:

#### [filename.py]

**Current code** (lines [X]-[Y]):
```[language]
[exact current code from research/verification]
```

**New code**:
```[language]
[exact code to write, not pseudocode]
```

**Rationale**: [Why this change]

**Verification**:
```bash
[command to verify this phase worked]
```

**Post-conditions**:
- [What should be true after this phase]
```

#### 4. Verification Commands

```markdown
## Verification Commands

Run these commands to verify the implementation is correct:

### Syntax/Lint Check
```bash
[linting command]
```

### Unit Tests
```bash
[test command for affected files]
```

### Integration Check
```bash
[command to verify integration]
```

### Smoke Test
```bash
[manual or automated smoke test]
```
```

#### 5. Rollback Plan

```markdown
## Rollback Plan

If implementation fails:

1. **Git reset**: `git checkout -- [files]`
2. **Specific rollback steps if needed**
```

---

## GATE: Plan Approval

### Present Full Plan

Present the complete plan for review:

```markdown
## Implementation Plan Ready for Review

### Summary
- **Phases**: [count]
- **Files to modify**: [list]
- **Files explicitly excluded**: [count]
- **Estimated changes**: [description]

### Scope Boundaries

**IN SCOPE**:
- [list of what will be done]

**OUT OF SCOPE**:
- [list of what won't be done]

### Full Plan

[Include complete plan here]

---

**Review checklist:**
- [ ] Modification points match research findings
- [ ] Excluded components are clearly documented
- [ ] Each phase has verification commands
- [ ] Code snippets are exact (not pseudocode)
- [ ] Rollback plan is viable

**Approve this plan to proceed with writing?**
```

**DO NOT PROCEED** until user approves the plan.

---

## Phase 4: Write Document

### Output Location

```
thoughts/shared/plans/YYYY-MM-DD-[TICKET]-description.md
```

### Document Structure

Use the template at [references/document-template.md](references/document-template.md).

### Link Back to Research

Include reference to source research:
```markdown
**Based on research**: [path/to/research/document.md]
```

---

## Self-Contained Plan Requirements

A plan is "self-contained" if someone can execute it WITHOUT:
- Re-reading the original codebase
- Re-running the research
- Asking clarifying questions

### Checklist

| Requirement | How to Satisfy |
|-------------|----------------|
| Exact file paths | Full paths, not relative |
| Exact line numbers | From verification step |
| Exact current code | Copied from files, not paraphrased |
| Exact new code | Complete code, not pseudocode |
| Verification commands | Runnable as-is |
| Clear exclusions | With reasons |

### Bad vs Good Examples

**BAD (not self-contained):**
```markdown
### Phase 1
- Update the handler to include the new feature
- Modify the relevant config
```

**GOOD (self-contained):**
```markdown
### Phase 1: Add Feature Flag Check

**File**: src/api/handler.py

**Current code** (lines 45-52):
```python
def process_request(request):
    validated = validate(request)
    return orchestrator.handle(validated)
```

**New code**:
```python
def process_request(request):
    validated = validate(request)
    if feature_flags.is_enabled('new_feature'):
        return orchestrator.handle_v2(validated)
    return orchestrator.handle(validated)
```

**Verification**:
```bash
python -m pytest tests/test_handler.py -v
```
```

---

## Anti-Pattern Prevention

| Anti-Pattern | How This Skill Prevents It |
|--------------|---------------------------|
| "Plan requires re-reading code" | Exact code snippets required |
| "Scope creep during implementation" | "What We're NOT Doing" section |
| "Accidentally modify excluded component" | "Excluded Components" section with reasons |
| "Plan says 'update X' without details" | Phase template requires exact code |
| "No way to verify phase worked" | Verification commands required per phase |

---

## Error Recovery

### If Research Is Stale

```
Research was conducted [N] days ago. Codebase may have changed.

Options:
1. Verify key modification points are still accurate (I'll check)
2. Re-run /rpi-research for fresh analysis
```

### If Plan Is Too Large

```
This plan has [N] phases and modifies [M] files.

Recommendation: Split into smaller plans:
1. [Subset 1 description]
2. [Subset 2 description]

Which subset should I plan first?
```

### If User Rejects Plan

```
Understood. What aspects need revision?

1. Scope too large/small?
2. Wrong modification points?
3. Missing exclusions?
4. Different phase ordering?
```

Update plan and re-present for approval.

---

## Output Verification Checklist

Before completing, verify:

- [ ] "What We're NOT Doing" section is populated
- [ ] "Excluded Components" lists all items from research exclusions
- [ ] Each phase has pre-conditions, code snippets, and verification
- [ ] Code snippets are exact (verified against current files)
- [ ] Verification commands are runnable
- [ ] Plan links back to research document
- [ ] Plan is written to `thoughts/shared/plans/`
- [ ] Next step pointer to `/rpi-implement` is included
