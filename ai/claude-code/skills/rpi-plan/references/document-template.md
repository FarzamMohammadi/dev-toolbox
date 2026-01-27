# Plan Document Template

Use this template when generating the final plan document.

---

```markdown
# Implementation Plan: [TICKET-ID] [Brief Description]

**Date**: [YYYY-MM-DD]
**Status**: Ready for Implementation
**Based on research**: [path/to/research/document.md]
**Execute with**: `/rpi-implement [path-to-this-plan]`

---

## Summary

[One paragraph describing what will be implemented and the approach.]

---

## Scope

### In Scope

- [Specific deliverable 1]
- [Specific deliverable 2]
- [Specific deliverable 3]

### What We're NOT Doing

| Excluded Item | Reason | Future Reference |
|---------------|--------|------------------|
| [Feature/change X] | [Why excluded] | [Ticket/note for future] |
| [Refactoring Y] | [Why excluded] | [Ticket/note for future] |
| [Related issue Z] | [Why excluded] | [Ticket/note for future] |

---

## Excluded Components

**These files/functions were identified in research but are explicitly NOT being modified:**

| Component | Category | Reason for Exclusion |
|-----------|----------|---------------------|
| [file.py:function()] | SUB_AGENT | Changes belong in orchestrator per architecture |
| [legacy.py] | DEAD_CODE | Not called anywhere; modification would have no effect |
| [old_config.py] | DEPRECATED | Replaced by new_config.py |
| [unrelated.py] | OUT_OF_SCOPE | Different feature area, not part of this task |

---

## Architecture Reference

### Relevant System Flow

```
[Request/Trigger]
    ↓
[ENTRY_POINT: path/file.py:function()]  <- MODIFY
    ↓
[ORCHESTRATOR: path/coord.py:process()]  <- MODIFY
    ├── [SUB_AGENT: agents/a.py] <- DO NOT MODIFY
    └── [SUB_AGENT: agents/b.py] <- DO NOT MODIFY
```

### Key Files

| File | Role | Action |
|------|------|--------|
| [path/entry.py] | Entry point | Modify |
| [path/coord.py] | Orchestrator | Modify |
| [agents/sub.py] | Sub-agent | NO CHANGE (excluded) |

---

## Implementation Phases

### Phase 1: [Phase Name]

**Goal**: [What this phase accomplishes]

**Pre-conditions**:
- [Condition that must be true]
- [Another condition]

#### File: [path/to/file.py]

**Current code** (lines [X]-[Y]):
```python
[exact current code copied from file]
```

**New code**:
```python
[exact replacement code]
```

**Rationale**: [Why this change is being made]

---

**Verification**:
```bash
# Syntax check
python -m py_compile path/to/file.py

# Run relevant tests
python -m pytest tests/test_file.py -v
```

**Post-conditions**:
- [What should now be true]

---

### Phase 2: [Phase Name]

**Goal**: [What this phase accomplishes]

**Pre-conditions**:
- Phase 1 completed successfully
- [Other conditions]

#### File: [path/to/other_file.py]

**Current code** (lines [X]-[Y]):
```python
[exact current code]
```

**New code**:
```python
[exact replacement code]
```

**Rationale**: [Why this change is being made]

---

#### File: [path/to/second_file.py] (if multiple files in phase)

**Current code** (lines [X]-[Y]):
```python
[exact current code]
```

**New code**:
```python
[exact replacement code]
```

---

**Verification**:
```bash
# Phase 2 specific verification
[verification command]
```

**Post-conditions**:
- [What should now be true]

---

### Phase 3: [Phase Name]

[Continue pattern for additional phases]

---

## Verification Commands

### After All Phases Complete

#### Syntax/Lint Check
```bash
[linting command for all modified files]
```

#### Unit Tests
```bash
[test command covering modified code]
```

#### Integration Tests
```bash
[integration test command]
```

#### Manual Smoke Test

1. [Step 1 to manually verify]
2. [Step 2 to manually verify]
3. [Expected result]

---

## Rollback Plan

If implementation fails at any phase:

### Quick Rollback
```bash
# Discard all changes
git checkout -- [list of modified files]
```

### Partial Rollback (if some phases succeeded)

**If Phase 1 fails:**
```bash
git checkout -- [phase 1 files]
```

**If Phase 2 fails (after Phase 1 succeeded):**
```bash
git checkout -- [phase 2 files]
# Phase 1 changes remain; consider whether to keep or revert
```

---

## Dependencies

### Libraries/Packages

| Dependency | Version | Required For |
|------------|---------|--------------|
| [package] | [version] | [What it's used for] |

### External Services

| Service | Required For | Fallback |
|---------|--------------|----------|
| [service] | [Purpose] | [What happens if unavailable] |

---

## Test Updates Required

| Test File | Modification Needed |
|-----------|---------------------|
| [test_file.py] | [Add test for new behavior] |
| [test_integration.py] | [Update expected output] |

---

## Notes for Implementer

- [Any important notes or gotchas]
- [Things to watch out for]
- [Assumptions made in this plan]

---

## Metadata

- Plan created: [timestamp]
- Phases: [count]
- Files to modify: [count]
- Files excluded: [count]
- Research source: [path]
```
