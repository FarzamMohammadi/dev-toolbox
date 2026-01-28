---
name: rpi-implement
description: Executes plan documents methodically with phase-by-phase verification. Use when implementing from an existing plan in thoughts/shared/plans/.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [plan-path | ticket-id]
---

# RPI Implement

Executes implementation plans methodically with phase-by-phase verification. Follows plans exactly without improvisation. Stops and asks when reality doesn't match the plan.

## Purpose

This skill ensures implementation:
- Follows the plan exactly (no improvisation)
- Verifies each phase before proceeding
- Stops when encountering unexpected state
- Completes with full verification

## Related Skills

This skill is part of the **RPI Workflow**:

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | `/rpi-research` | Architecture-first codebase research |
| 2 | `/rpi-plan` | Self-contained implementation plan |
| 3 | `/rpi-implement` | Methodical execution with verification |

**Current:** `/rpi-implement`

```
Research ──► Plan ──► Implement
   ◄─────────┴────────┘
      (if issues found)
```

---

## Pre-Flight Check

Verify before proceeding:

- Plan document exists in `thoughts/shared/plans/`
- Plan has Implementation Phases with code snippets
- Git working tree is clean (`git status` shows no uncommitted changes)

**If dirty working tree**, ask user to commit or stash first.

---

## Core Principle: No Improvisation

**CRITICAL**: This skill executes plans, it does not create or modify them.

| Situation | Correct Response |
|-----------|------------------|
| Plan says X but code shows Y | STOP and ask user |
| Plan is missing a step | STOP and ask user |
| Better approach discovered | STOP and ask user |
| Verification fails | STOP and ask user |

**Never:**
- Add steps not in the plan
- Skip steps in the plan
- Modify code differently than specified
- Assume plan errors are acceptable

---

## Process Overview

```
Phase 1: Pre-flight Check
    ↓
[GATE] Confirm Start
    ↓
Phase Loop:
    ├── Verify Pre-conditions
    ├── Execute Changes
    ├── Run Verification
    └── [GATE] Phase Checkpoint
    ↓
Final Verification
    ↓
Summary Report
```

---

## Phase 1: Pre-flight Check

### Locate Plan Document

If argument provided:
```
1. Check if [argument] is a file path
2. Check if it's a ticket ID (search thoughts/shared/plans/ for matching files)
3. If neither found, ask user for clarification
```

If no argument:
```
1. List recent plan documents in thoughts/shared/plans/
2. Ask user which one to execute
```

### Validate Plan Document

Confirm the plan contains:

| Required Section | Purpose |
|------------------|---------|
| Implementation Phases | What to execute |
| Code snippets (current/new) | Exact changes to make |
| Verification Commands | How to verify each phase |
| Excluded Components | What NOT to touch |

If any section is missing:
```
The plan document is missing: [sections]

A valid plan requires all sections. Options:
1. Re-run /rpi-plan to create a complete plan
2. Locate the correct plan document
```

**DO NOT PROCEED** with incomplete plans.

### Verify Plan Currency

Check that the plan's "current code" matches actual files:

```bash
# For each modification point in the plan
Read [file_path]
# Compare lines [X]-[Y] with plan's "Current code" section
```

If mismatch detected:
```
Plan Mismatch Detected

**File**: [file.py]
**Plan expects** (lines [X]-[Y]):
```
[code from plan]
```

**Actual code**:
```
[code from file]
```

The code has changed since the plan was created.

Options:
1. Update the plan to reflect current code
2. Re-run /rpi-plan with current state
3. Proceed anyway (NOT RECOMMENDED)
```

**DO NOT PROCEED** if plan doesn't match reality without user decision.

---

## GATE: Confirm Start

### Present Plan Summary

```markdown
## Ready to Implement

**Plan**: [path/to/plan.md]
**Task**: [task description]
**Created**: [plan date]

### Implementation Summary

| Phase | Description | Files |
|-------|-------------|-------|
| 1 | [Phase 1 name] | [files] |
| 2 | [Phase 2 name] | [files] |
| ... | ... | ... |

### Files to Modify
- [file1.py]
- [file2.py]

### Files Explicitly Excluded (will NOT touch)
- [excluded1.py] - [reason]
- [excluded2.py] - [reason]

### Pre-flight Status
- [x] Plan document found and valid
- [x] Current code matches plan expectations
- [x] All verification commands identified

### Checkpoint Mode

How should I handle phase transitions?
- **Per-phase confirmation** (default): Stop after each phase for approval
- **Batch mode**: Execute all phases, only stop on errors

**Ready to begin implementation?**
```

**DO NOT PROCEED** until user confirms.

---

## Phase Execution Loop

For each phase in the plan:

### Step 1: Announce Phase

```markdown
## Starting Phase [N]: [Phase Name]

**Goal**: [from plan]

**Pre-conditions to verify**:
- [condition 1]
- [condition 2]
```

### Step 2: Verify Pre-conditions

Check each pre-condition listed in the plan:

```markdown
### Pre-condition Check

| Condition | Status |
|-----------|--------|
| [condition 1] | [PASS/FAIL] |
| [condition 2] | [PASS/FAIL] |
```

If any pre-condition fails:
```
Pre-condition Failed

**Condition**: [what was expected]
**Actual state**: [what was found]

Cannot proceed with Phase [N]. Options:
1. Fix the pre-condition manually
2. Skip this phase (if appropriate)
3. Abort implementation
```

**DO NOT PROCEED** if pre-conditions fail.

### Step 3: Execute Changes

For each file modification in the phase:

1. **Read current state** to confirm it matches plan
2. **Apply the exact change** specified in plan
3. **Verify the change** was applied correctly

```markdown
### Applying Changes

**File**: [file.py]

Replacing lines [X]-[Y]:
```[language]
[old code]
```

With:
```[language]
[new code]
```

[Execute Edit tool]

Change applied. Verifying...
```

### Step 4: Run Phase Verification

Execute the verification commands from the plan:

```bash
# From plan's verification section
[verification command]
```

Report results:
```markdown
### Phase [N] Verification

**Command**: `[verification command]`
**Result**: [PASS/FAIL]
**Output**:
```
[command output]
```
```

### Step 5: GATE - Phase Checkpoint

**STOP** after each phase and report:

```markdown
## Phase [N] Complete

### Changes Applied
| File | Lines | Change |
|------|-------|--------|
| [file.py] | [X]-[Y] | [description] |

### Verification Result
- [x] Syntax check: PASS
- [x] Tests: PASS

### Next Phase
Phase [N+1]: [name]

**Continue to next phase?**
```

**DO NOT PROCEED** to next phase without user confirmation.

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Plan not found | Wrong path | Verify path, check `thoughts/shared/plans/` |
| Code mismatch | Code changed since plan | STOP, show diff, ask user to update plan or proceed |
| Verification failed | Test failure or syntax error | STOP, show error, ask user: fix/rollback/abort |
| Pre-condition failed | Dependency not met | STOP, report which condition, await user fix |
| Excluded file modified | Accidental change | Rollback with `git checkout -- [file]` |

**NEVER** guess or improvise. Always stop and ask.

### Rollback Commands

```bash
# Single phase
git checkout -- [files from that phase]

# All changes
git checkout -- [all modified files]

# Check what changed
git diff
```

---

## Final Verification

After all phases complete:

### Run All Verification Commands

Execute every verification command from the plan:

```markdown
## Final Verification

### Syntax/Lint
```bash
[lint command from plan]
```
Result: [PASS/FAIL]

### Unit Tests
```bash
[test command from plan]
```
Result: [PASS/FAIL]

### Integration Check
```bash
[integration command from plan]
```
Result: [PASS/FAIL]
```

### Verify Exclusions Were Respected

Confirm excluded files were NOT modified:

```bash
git diff [excluded_file1.py]  # Should show no changes
git diff [excluded_file2.py]  # Should show no changes
```

```markdown
### Exclusion Verification

| Excluded File | Status |
|---------------|--------|
| [excluded1.py] | NOT MODIFIED (correct) |
| [excluded2.py] | NOT MODIFIED (correct) |
```

---

## Summary Report

```markdown
## Implementation Complete

**Plan executed**: [path/to/plan.md]
**Task**: [description]

### Phases Completed

| Phase | Status | Notes |
|-------|--------|-------|
| 1: [name] | COMPLETE | - |
| 2: [name] | COMPLETE | - |
| ... | ... | ... |

### Files Modified

| File | Changes |
|------|---------|
| [file1.py] | [summary of changes] |
| [file2.py] | [summary of changes] |

### Files NOT Modified (as planned)

| File | Reason |
|------|--------|
| [excluded1.py] | SUB_AGENT - changes in orchestrator |
| [excluded2.py] | DEAD_CODE - not called |

### Verification Summary

| Check | Result |
|-------|--------|
| Syntax/Lint | PASS |
| Unit Tests | PASS |
| Integration | PASS |
| Exclusions Respected | PASS |

### Next Steps

1. Review the changes: `git diff`
2. Commit when ready: `/commit` or manual commit
3. Run full test suite if not already done
```

---

## Anti-Pattern Prevention

| Anti-Pattern | How This Skill Prevents It |
|--------------|---------------------------|
| "I'll just fix this while I'm here" | No improvisation rule - stop and ask |
| "The plan is slightly wrong, I'll adapt" | Mismatch detection - stop and ask |
| "Skip verification, looks fine" | Mandatory verification gates |
| "I know better than the plan" | Plan is authoritative - stop and ask |
| "Modified excluded file by accident" | Exclusion verification in final check |

---

## Output Verification Checklist

Before completing, verify:

- [ ] All phases executed in order
- [ ] Each phase verification passed
- [ ] All exclusions were respected
- [ ] Final verification commands all passed
- [ ] Summary report generated
- [ ] Git diff available for review

---

## Usage Examples

```
/rpi-implement thoughts/shared/plans/2024-01-15-VE-1234-feature.md
/rpi-implement VE-1234
/rpi-implement
```
