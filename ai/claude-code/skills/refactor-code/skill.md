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

## Review Process (File-Based Multi-Pass)

**Uses per-file notes as external memory to prevent context overflow.**

### Phase 1: Comprehensive Understanding

1. Run the git diff command provided
2. List ALL changed files
3. Read each file to understand changes holistically
4. Identify cross-file dependencies

### Phase 2: Per-File Analysis

**For EACH changed file**, create a notes file and analyze layer-by-layer:

```
{filename}.refactor-notes.md  ← Created in SAME directory as source file
```

**Process for each file:**

1. **Create notes file** using [templates/refactor-notes-template.md](templates/refactor-notes-template.md)
2. **Layer 1 → Write to notes**: Philosophy checks (Code as Communication, Cognitive Load, Code Block Extraction)
3. **Layer 2 → Write to notes**: Tier 1 Principles (blocking issues)
4. **Layer 3 → Write to notes**: Tier 2 Principles (important issues)
5. **Layer 4 → Write to notes**: Tier 3 Principles (suggestions)
6. **Layer 5 → Write to notes**: Philosophy alignment check, compile "Changes to Apply"
7. **Move to next file** (don't apply changes yet!)

See [Per-File Layer Details](#per-file-layer-details) below.

### Phase 3: Apply Changes

**For EACH notes file:**

1. Read `{filename}.refactor-notes.md`
2. Apply each item in "Changes to Apply" checklist
3. Mark items complete as applied
4. Verify changes match documented intent

### Phase 4: Cleanup

1. **Delete ALL `.refactor-notes.md` files** created during review
2. Generate final summary report

---

## Per-File Layer Details

### Layer 1: Philosophy Check (WRITE TO NOTES)

Check and write findings to notes file:

**Code as Communication:**
- [ ] Vague function names (`validate()`, `process()`, `handle()`) → rename
- [ ] Comments explaining WHAT → extract to named function
- [ ] Vague variables (`data`, `temp`, `result`, `info`) → rename

**Reducing Cognitive Load:**
- [ ] Functions mixing abstraction levels → extract helpers
- [ ] Functions > 30 lines with multiple responsibilities → split

**Code Block Extraction:**
- [ ] If blocks, for/while loops, try/except → can describe in a phrase?
  - YES → extract to function with that name
  - With comment: DELETE comment after extraction
  - Without comment: still extract if logical unit
- See [decision-logic/code-block-extraction.md](decision-logic/code-block-extraction.md)

### Layer 2: Tier 1 Principles (WRITE TO NOTES)

See [principles/tier-1-blocking.md](principles/tier-1-blocking.md).

- [ ] **3.1 Intent-revealing names**
- [ ] **3.9 Semantic specificity**: `validate()` → `validate_user_input()`
- [ ] **3.5 No misleading names**
- [ ] **1.1 Single Responsibility**
- [ ] **1.7 Separation of Concerns**
- [ ] **5.1 Specific exceptions** (no `except Exception:`)
- [ ] **5.2 No silent failures** (no `except: pass`)
- [ ] **2.9 Fail fast**

⚠️ **Write checkpoint to notes**: Do findings conflict with Layer 1? Revise.

### Layer 3: Tier 2 Principles (WRITE TO NOTES)

See [principles/tier-2-important.md](principles/tier-2-important.md).

- [ ] **Naming**: Abbreviations, searchability, domain consistency, boolean naming
- [ ] **Structure**: Cohesion, coupling, dependency injection, abstraction levels
- [ ] **Functions**: Length < 30, max 4 params, nesting < 3 levels
- [ ] **Errors**: Context in messages, fail safely
- [ ] **Code quality**: DRY, KISS, magic numbers
- [ ] **Types**: Type hints, null safety

⚠️ **Write checkpoint to notes**: Do findings conflict with Layer 1? Revise.

### Layer 4: Tier 3 Principles (WRITE TO NOTES)

See [principles/tier-3-suggestions.md](principles/tier-3-suggestions.md).

- [ ] **Style**: Noise words, composition over inheritance
- [ ] **Code cleanup**: YAGNI, dead code
- [ ] **Interface design**: SOLID, Law of Demeter
- [ ] **Performance**: Only if profiled

⚠️ **Write checkpoint to notes**: Do findings conflict with Layer 1? Revise.

### Layer 5: Final Validation (WRITE TO NOTES)

- [ ] Re-read ALL layer findings in notes
- [ ] Verify NONE suggest comments for WHAT explanations
- [ ] Compile "Changes to Apply" checklist with specific line numbers

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
