# Research Document Template

Use this template when generating the final research document.

---

```markdown
# Research: [TICKET-ID] [Brief Description]

**Date**: [YYYY-MM-DD]
**Status**: Complete
**Researcher**: Claude (via /rpi-research)
**Next Step**: `/rpi-plan [path-to-this-document]`

---

## Summary

[One paragraph describing what was investigated and key findings. Include the primary modification points identified.]

---

## Task Context

**Goal**: [What change/feature is being investigated]
**Scope**: [Codebase area(s) involved]
**Constraints**: [Any limitations or requirements noted]

---

## Architecture Overview

### System Flow

```
[Request Source]
    ↓
[ENTRY_POINT: filename.py:function()]
    ↓
[ORCHESTRATOR: coordinator.py:main_flow()]
    ├── [SUB_AGENT: agent_a.py:process_a()]
    ├── [SUB_AGENT: agent_b.py:process_b()]
    └── [UTILITY: helpers.py:format_output()]
```

### Component Relationships

| Component | Type | Responsibility | Dependencies |
|-----------|------|----------------|--------------|
| [filename.py] | [ENTRY_POINT] | [What it does] | [What it depends on] |
| [coordinator.py] | [ORCHESTRATOR] | [What it does] | [What it depends on] |
| [agent_a.py] | [SUB_AGENT] | [What it does] | [What it depends on] |

---

## Findings

### Categorized Results

| File:Line | Category | Function/Class | Purpose | Relevant? |
|-----------|----------|----------------|---------|-----------|
| [path.py:45] | [ENTRY_POINT] | [function_name()] | [Description] | Yes |
| [path.py:120] | [ORCHESTRATOR] | [class.method()] | [Description] | Yes |
| [other.py:30] | [SUB_AGENT] | [function()] | [Description] | No - see Exclusions |

### Detailed Analysis

#### [Primary File: filename.py]

**Purpose**: [One-line description]
**Category**: [ENTRY_POINT/ORCHESTRATOR/etc.]
**Key for task because**: [Why this file matters]

**Relevant Code**:

```
Lines 45-67: function_name()
- Current behavior: [What it does now]
- Calls: [What it invokes]
- Called by: [What invokes it]
```

```
Lines 100-115: other_function()
- Current behavior: [What it does now]
- Note: [Any relevant observations]
```

#### [Secondary File: other.py]

**Purpose**: [One-line description]
**Category**: [Category]
**Key for task because**: [Why this file matters]

**Relevant Code**:

```
Lines 20-35: helper_function()
- Current behavior: [What it does now]
```

---

## Recommended Modification Points

### Primary Changes

| File:Line | Function | Change Type | Rationale |
|-----------|----------|-------------|-----------|
| [path.py:45] | [function()] | [Add/Modify/Remove] | [Why here] |
| [path.py:120] | [method()] | [Add/Modify/Remove] | [Why here] |

### Secondary Changes (if needed)

| File:Line | Function | Change Type | Rationale |
|-----------|----------|-------------|-----------|
| [helper.py:30] | [util()] | [Add/Modify/Remove] | [Why here] |

---

## Exclusions

**These items were found but explicitly excluded from scope:**

| File | Reason for Exclusion |
|------|---------------------|
| [sub_agent.py] | SUB_AGENT: Changes should go in ORCHESTRATOR instead |
| [legacy.py] | DEAD_CODE: Function not called anywhere (verified via grep) |
| [unrelated.py] | OUT_OF_SCOPE: Different feature area |
| [config_old.py] | DEPRECATED: Replaced by new_config.py |

---

## Verification Commands

Commands used to verify findings:

```bash
# Verify function is called
grep -r "function_name(" --include="*.py" .

# Trace call hierarchy
grep -r "orchestrator.process" --include="*.py" .

# Check for dead code
grep -r "old_function" --include="*.py" .  # No results = dead code
```

---

## Open Questions

[List any unresolved questions that should be addressed during planning]

1. [Question about unclear behavior or requirement]
2. [Question about edge case handling]

---

## Dependencies & Impact

### Files That May Be Affected

| File | Relationship | Impact Level |
|------|-------------|--------------|
| [file.py] | Direct modification | High |
| [test_file.py] | Test coverage | Medium |
| [dependent.py] | Imports from modified file | Low - verify after changes |

### External Dependencies

- [Library/Service name]: [How it's used]

---

## Test Coverage

| Component | Test File | Coverage Status |
|-----------|-----------|-----------------|
| [filename.py] | [test_filename.py] | [Covered/Partial/None] |
| [other.py] | [test_other.py] | [Covered/Partial/None] |

---

## Next Steps

1. Review this research document
2. Run `/rpi-plan [path-to-this-document]` to create implementation plan
3. Address any open questions before planning

---

## Metadata

- Research completed: [timestamp]
- Files analyzed: [count]
- Modification points identified: [count]
- Items excluded: [count]
```
