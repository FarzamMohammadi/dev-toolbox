---
name: refactor-code
description: Review git diffs against refactoring philosophies and principles. Use when user wants code review, refactoring suggestions, or mentions reviewing changes.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [git-diff-command]
context: fork
---

# Code Refactoring Review

Reviews changed files in a git diff using a layered approach: philosophies first, then principles by tier.

## Usage

```
Review commits: /refactor-code git diff main...HEAD
Review last commit: /refactor-code git diff HEAD~1
Review specific range: /refactor-code git diff abc123..def456
Review staged changes: /refactor-code git diff --cached
```

---

## Philosophies (ALWAYS OVERRIDE PRINCIPLES)

These are the user's core coding beliefs. **Non-negotiable. Always win over principles.**

### Philosophy 1: Code as Communication

**Code should communicate intent through names, not comments.**

---

**Core Focus: NAMING**

| Aspect | Apply This |
|--------|------------|
| Intent-revealing names | Names describe purpose: `validate()` → `validate_user_credentials()` |
| Semantic specificity | Avoid vague names: `data`, `temp`, `result`, `info` → specific meaning |
| Misleading names | Names must match behavior: `getUser()` that modifies state → fix |
| Boolean clarity | Booleans read as yes/no questions: `isValid`, `hasPermission`, `canEdit` |

**Structure Clarity:**
- Comments explaining WHAT → rename or restructure instead
- Comments explain WHY (business context), never WHAT

**Example:**
```python
# Bad - comment explains what
input_guard.validate(request)  # Validates and logs suspicious patterns

# Good - name explains what
input_guard.detect_and_log_suspicious_patterns(request)
```

---

### Philosophy 2: Reducing Cognitive Load

**Structure code so readers understand at their desired abstraction level.**

---

**Core Focus: STRUCTURE**

| Aspect | Apply This |
|--------|------------|
| Hierarchical abstraction | High-level functions call well-named lower-level functions |
| Progressive disclosure | Main functions read like an outline; details in helpers |
| Consistent patterns | Same approach for similar operations |

**Code Block Extraction:**
- Logical blocks (if/for/while/try) that can be described in a phrase → extract to named function
- See [decision-logic/code-block-extraction.md](decision-logic/code-block-extraction.md)

**Example:**
```python
# Bad - all details at one level
def process_order(order):
    if not order.items:
        raise ValueError("Empty order")
    total = 0
    for item in order.items:
        price = item.base_price * (1 - get_discount(item))
        total += price * item.quantity
    db.save(order)
    email.send(order.customer, "Confirmed")

# Good - hierarchical (read at your level)
def process_order(order):
    validate_order(order)
    order.total = calculate_order_total(order)
    finalize_order(order)
    notify_customer(order)
```

---

### Philosophy 3: File names and structure used to communicate the purpose of the file and its contents.

**File names and structure should be used to communicate the purpose of the file and its contents.**

FILL MORE HERE.

---

## MANDATORY REVIEW PROCESS

**STOP. Follow these steps EXACTLY in order. Do not skip steps.**

---

### STEP 1: Run the Git Diff

Run the provided git diff command using Bash:
```bash
{user's git diff command}
```

List all changed files. Write them down.

---

### STEP 2: For EACH Changed File - CREATE NOTES FILE

**MANDATORY: Before analyzing ANY code, create a notes file.**

For the FIRST changed file:
1. Determine the file path (e.g., `src/utils/validator.py`)
2. **USE THE WRITE TOOL NOW** to create:
   ```
   src/utils/validator.py.refactor-notes.md
   ```
3. Write this initial content:
   ```markdown
   # Refactor Notes: validator.py

   ## File Context
   - Path: src/utils/validator.py
   - Analyzing: [brief description]

   ## Layer 1: Philosophy Check

   ### Philosophy 1: Code as Communication
   [Will populate below]

   ### Philosophy 2: Reducing Cognitive Load
   [Will populate below]

   ## Layer 2: Tier 1 Principles
   [Will populate below]

   ## Layer 3: Tier 2 Principles
   [Will populate below]

   ## Layer 4: Tier 3 Principles
   [Will populate below]

   ## Layer 5: Final Validation
   [Will populate below]

   ## Changes to Apply
   [Will compile at end]
   ```

**DO NOT PROCEED** until this notes file exists.

---

### STEP 3: Layer 1 Analysis - PHILOSOPHY CHECK

Read the source file. **Check BOTH philosophies with EQUAL attention.**

---

#### Philosophy 1: Code as Communication
**Reference:** [Philosophy 1 section above](#philosophy-1-code-as-communication)

Check ALL naming aspects:
- Intent-revealing names
- Semantic specificity
- Misleading names
- Boolean clarity

Check ALL structure aspects:
- Self-documenting code (comments explaining WHAT should become names)
- Comments explain WHY not WHAT

**Write findings to notes file under "Philosophy 1".**

---

#### Philosophy 2: Reducing Cognitive Load
**Reference:** [Philosophy 2 section above](#philosophy-2-reducing-cognitive-load)

Check ALL structure aspects:
- Hierarchical abstraction
- Progressive disclosure
- Consistent patterns
- Code block extraction (logical blocks → named functions)

**Write findings to notes file under "Philosophy 2".**

---

**USE THE EDIT TOOL** to update the notes file:

```markdown
## Layer 1: Philosophy Check

### Philosophy 1: Code as Communication
[Record findings from ALL naming and structure clarity aspects]

### Philosophy 2: Reducing Cognitive Load
[Record findings from ALL cognitive load aspects]
```

**DO NOT PROCEED** to Layer 2 until Layer 1 findings are written to the notes file.

---

### STEP 4: Layer 2 Analysis - TIER 1 PRINCIPLES

**Reference:** [principles/tier-1-blocking.md](principles/tier-1-blocking.md) (MUST-FIX issues)

Review ALL Tier 1 categories with equal attention:
- **Naming** (3.1, 3.5, 3.9): Intent-revealing, no misleading, semantic specificity
- **Structure** (1.1, 1.7): Single responsibility, separation of concerns
- **Error handling** (5.1, 5.2, 2.9): Specific exceptions, no silent failures, fail fast

**USE THE EDIT TOOL** to update notes file:

```markdown
## Layer 2: Tier 1 Principles
[Record findings from ALL Tier 1 categories]

**Checkpoint**: Verified against Layer 1 ✓
```

⚠️ **MANDATORY CHECKPOINT**: Do findings conflict with Layer 1 philosophies? If yes, REVISE.

**DO NOT PROCEED** until Layer 2 findings are written to the notes file.

---

### STEP 5: Layer 3 Analysis - TIER 2 PRINCIPLES

**Reference:** [principles/tier-2-important.md](principles/tier-2-important.md) (SHOULD-FIX issues)

Review ALL Tier 2 categories with equal attention:
- **Naming**: Abbreviations, searchability, domain consistency, boolean naming
- **Structure**: Cohesion, coupling, dependency injection, abstraction levels
- **Functions**: Length < 30 lines, max 4 params, nesting < 3 levels
- **Errors**: Context in messages, fail safely
- **Code quality**: DRY, KISS, magic numbers
- **Types**: Type hints, null safety

**USE THE EDIT TOOL** to update notes file:

```markdown
## Layer 3: Tier 2 Principles
[Record findings from ALL Tier 2 categories]

**Checkpoint**: Verified against Layer 1 ✓
```

⚠️ **MANDATORY CHECKPOINT**: Do findings conflict with Layer 1 philosophies? If yes, REVISE.

**DO NOT PROCEED** until Layer 3 findings are written to the notes file.

---

### STEP 6: Layer 4 Analysis - TIER 3 PRINCIPLES

**Reference:** [principles/tier-3-suggestions.md](principles/tier-3-suggestions.md) (NICE-TO-HAVE issues)

Review ALL Tier 3 categories with equal attention:
- **Style**: Noise words, composition over inheritance
- **Code cleanup**: YAGNI, dead code
- **Interface design**: SOLID, Law of Demeter
- **Performance**: Only if profiled

**USE THE EDIT TOOL** to update notes file:

```markdown
## Layer 4: Tier 3 Principles
[Record findings from ALL Tier 3 categories]

**Checkpoint**: Verified against Layer 1 ✓
```

⚠️ **MANDATORY CHECKPOINT**: Do findings conflict with Layer 1 philosophies? If yes, REVISE.

**DO NOT PROCEED** until Layer 4 findings are written to the notes file.

---

### STEP 7: Layer 5 - COMPILE CHANGES TO APPLY

Review all findings in the notes file.

**USE THE EDIT TOOL** to populate "Layer 5" and "Changes to Apply":

```markdown
## Layer 5: Final Validation
- [x] Re-read ALL layer findings above
- [x] Verified NONE suggest comments for WHAT explanations
- [x] All suggestions align with both Philosophies

**Revisions made:**
- Line 42: Originally suggested "add comment" → changed to "rename function"

## Changes to Apply
1. [ ] Line 42: Rename `validate()` → `validate_user_credentials()`
2. [ ] Lines 23-35: Extract to `_validate_email_format()`
3. [ ] Line 55: Change `except Exception` → `except ValueError, KeyError`
4. [ ] Line 89: Add `logger.warning()` to except block
```

---

### STEP 8: REPEAT FOR NEXT FILE

Go back to STEP 2 for the next changed file. Create its notes file and repeat the process.

**DO NOT APPLY ANY CHANGES YET.**

---

### STEP 9: APPLY CHANGES

Only after ALL notes files are complete:

For EACH notes file:
1. Read the "Changes to Apply" section
2. **USE THE EDIT TOOL** to make each change to the source file
3. Mark items complete in the notes file as you go

---

### STEP 10: CLEANUP

**DELETE ALL `.refactor-notes.md` files** using Bash:
```bash
find . -name "*.refactor-notes.md" -delete
```

Generate final summary report

---

## Quick Reference

### Decision Trees

**Naming → Comment:**
```
Need to explain code?
├── Explaining WHAT → RENAME (Philosophy 1)
└── Explaining WHY (business context) → Comment OK
```

**Philosophy Enforcement:**
```
For each suggestion:
├── Aligns with Philosophies? → Keep
└── Conflicts with Philosophy? → REVISE or REJECT
```

### Tier Summary

| Tier | Enforcement | Focus |
|------|-------------|-------|
| 1 | Must fix | Names, SRP, error handling |
| 2 | Should fix | Structure, functions, types |
| 3 | Nice to have | Style, cleanup, performance |

---

## Final Summary Report Format

After all notes files are processed and changes applied:

```markdown
# Refactoring Review: [git diff command]

## Summary
- Files reviewed: [N]
- Total changes applied: [N]
- Layer 1 (Philosophy): [N] findings
- Layer 2 (Tier 1 - Blocking): [N] findings
- Layer 3 (Tier 2 - Important): [N] findings
- Layer 4 (Tier 3 - Suggestions): [N] findings

## Changes Applied by File

### [filename1]
- Line X: [change description]
- Line Y: [change description]

### [filename2]
- Line X: [change description]

## Philosophy Alignment
✓ All suggestions verified against Philosophies
✓ No comments suggested for WHAT explanations
✓ All notes files cleaned up
```

---

## Reference Materials

**Templates:**
- [templates/refactor-notes-template.md](templates/refactor-notes-template.md) - Per-file notes structure

**Principles:**
- [principles/index.md](principles/index.md) - Full principle classification
- [principles/tier-1-blocking.md](principles/tier-1-blocking.md) - Must-fix issues
- [principles/tier-2-important.md](principles/tier-2-important.md) - Should-fix issues
- [principles/tier-3-suggestions.md](principles/tier-3-suggestions.md) - Nice-to-have

**Decision Logic:**
- [decision-logic/philosophy-enforcement.md](decision-logic/philosophy-enforcement.md) - Override rules
- [decision-logic/naming-vs-comments.md](decision-logic/naming-vs-comments.md) - Common conflict resolution
- [decision-logic/code-block-extraction.md](decision-logic/code-block-extraction.md) - Logical blocks → named functions

**Examples:**
- [examples/naming.md](examples/naming.md) - Naming examples
- [examples/structure.md](examples/structure.md) - Structure examples
- [examples/functions.md](examples/functions.md) - Function design examples
