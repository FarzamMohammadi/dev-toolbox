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

**Code should communicate intent through names and structure, not comments.**

Key tenets:
- **Names over comments**: Use descriptive names that eliminate need for explanatory comments
- **Self-documenting code**: Code tells the story; comments only explain "why" (business context)
- **Extract for clarity**: Complex conditions → extract to well-named functions

**The Golden Rules:**
> 1. Comment explaining WHAT → STOP. Rename or restructure instead.
> 2. Logical code block → EXTRACT into a well-named function (with OR without comment).
> 3. If you can describe what a block does in a phrase → that's the function name.
> 4. Comments explain WHY (business context), never WHAT.

**Example - Apply this philosophy:**
```python
# Bad - comment explains what
input_guard.validate(request)  # Validates and logs suspicious patterns

# Good - name explains what
input_guard.detect_and_log_suspicious_patterns(request)
```

### Philosophy 2: Reducing Cognitive Load

**Structure code so readers understand at their desired abstraction level.**

Key tenets:
- **Hierarchical abstraction**: High-level functions call well-named lower-level functions
- **Progressive disclosure**: Main functions read like an outline; details in helpers
- **Consistent patterns**: Same approach for similar operations

**Example - Apply this philosophy:**
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

### STEP 3: Layer 1 Analysis - WRITE TO NOTES FILE

Read the source file. Check for philosophy violations.

**USE THE EDIT TOOL** to update the notes file, replacing `[Will populate below]` under "Layer 1" with actual findings:

```markdown
## Layer 1: Philosophy Check

### Code as Communication
- [ ] Line 42: `validate()` is vague → rename to `validate_user_credentials()`
- [ ] Line 78: comment explains WHAT → extract to `_check_password_strength()`

### Reducing Cognitive Load
- [ ] Lines 50-95: function mixes levels → extract helpers

### Code Block Extraction
- [ ] Lines 23-35: if block → `_validate_email_format()`
```

**Checklist for Layer 1:**
- [ ] Vague function names (`validate()`, `process()`, `handle()`) → rename
- [ ] Comments explaining WHAT → extract to named function
- [ ] Vague variables (`data`, `temp`, `result`, `info`) → rename
- [ ] Functions mixing abstraction levels → extract helpers
- [ ] If blocks, for/while loops, try/except that can be described in a phrase → extract
- See [decision-logic/code-block-extraction.md](decision-logic/code-block-extraction.md)

**DO NOT PROCEED** to Layer 2 until Layer 1 findings are written to the notes file.

---

### STEP 4: Layer 2 Analysis - WRITE TO NOTES FILE

Check Tier 1 principles. See [principles/tier-1-blocking.md](principles/tier-1-blocking.md).

**USE THE EDIT TOOL** to update notes file, replacing `[Will populate below]` under "Layer 2":

```markdown
## Layer 2: Tier 1 Principles
- [ ] Line 55: generic `except Exception:` → catch specific types
- [ ] Line 89: silent failure `except: pass` → add logging

**Checkpoint**: Verified against Layer 1 ✓
```

**Checklist for Layer 2:**
- [ ] **3.1 Intent-revealing names**
- [ ] **3.9 Semantic specificity**: `validate()` → `validate_user_input()`
- [ ] **3.5 No misleading names**
- [ ] **1.1 Single Responsibility**
- [ ] **1.7 Separation of Concerns**
- [ ] **5.1 Specific exceptions** (no `except Exception:`)
- [ ] **5.2 No silent failures** (no `except: pass`)
- [ ] **2.9 Fail fast**

⚠️ **MANDATORY CHECKPOINT**: Do findings conflict with Layer 1 philosophies? If yes, REVISE.

**DO NOT PROCEED** until Layer 2 findings are written to the notes file.

---

### STEP 5: Layer 3 Analysis - WRITE TO NOTES FILE

Check Tier 2 principles. See [principles/tier-2-important.md](principles/tier-2-important.md).

**USE THE EDIT TOOL** to update notes file, replacing `[Will populate below]` under "Layer 3":

```markdown
## Layer 3: Tier 2 Principles
- [ ] Line 12: missing type hints → add `def func(name: str) -> bool:`
- [ ] Lines 40-90: function 50 lines → split into helpers

**Checkpoint**: Verified against Layer 1 ✓
```

**Checklist for Layer 3:**
- [ ] **Naming**: Abbreviations, searchability, domain consistency, boolean naming
- [ ] **Structure**: Cohesion, coupling, dependency injection, abstraction levels
- [ ] **Functions**: Length < 30, max 4 params, nesting < 3 levels
- [ ] **Errors**: Context in messages, fail safely
- [ ] **Code quality**: DRY, KISS, magic numbers
- [ ] **Types**: Type hints, null safety

⚠️ **MANDATORY CHECKPOINT**: Do findings conflict with Layer 1 philosophies? If yes, REVISE.

**DO NOT PROCEED** until Layer 3 findings are written to the notes file.

---

### STEP 6: Layer 4 Analysis - WRITE TO NOTES FILE

Check Tier 3 principles. See [principles/tier-3-suggestions.md](principles/tier-3-suggestions.md).

**USE THE EDIT TOOL** to update notes file, replacing `[Will populate below]` under "Layer 4":

```markdown
## Layer 4: Tier 3 Principles
- [ ] Line 5: dead import `import unused_module`

**Checkpoint**: Verified against Layer 1 ✓
```

**Checklist for Layer 4:**
- [ ] **Style**: Noise words, composition over inheritance
- [ ] **Code cleanup**: YAGNI, dead code
- [ ] **Interface design**: SOLID, Law of Demeter
- [ ] **Performance**: Only if profiled

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
