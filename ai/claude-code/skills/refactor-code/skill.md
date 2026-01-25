---
name: refactor-code
description: Review git diffs against refactoring philosophies and principles. Use when user wants code review, refactoring suggestions, or mentions reviewing changes.
allowed-tools: Read, Bash, Grep, Glob
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

**The Golden Rule:**
> If you're about to suggest a comment that explains WHAT code does → STOP.
> Suggest renaming or restructuring instead.
> Comments explain WHY (business context), never WHAT.

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

## Review Process (Layered - Follow In Order)

**CRITICAL: Complete each layer before proceeding to the next.**

### Layer 1: Philosophy Check (REQUIRED FIRST)

For each changed file, check:

- [ ] **Code as Communication**: Is there code that needs a comment to explain WHAT it does?
  - If YES → Flag for rename/restructure (NOT comment)
  - Check: vague function names like `validate()`, `process()`, `handle()`
  - Check: complex conditions that need inline explanation
  - Check: variables named `data`, `temp`, `result`, `info`

- [ ] **Reducing Cognitive Load**: Can a reader understand intent at their desired level?
  - If NO → Flag for extraction into well-named functions
  - Check: functions mixing high-level and low-level operations
  - Check: functions over 30 lines with multiple responsibilities

- [ ] **Philosophy violations documented**

⚠️ **GATE**: Do not proceed to Layer 2 until Layer 1 is complete.

---

### Layer 2: Tier 1 Principles (Blocking)

Issues that **must be fixed**. See [principles/tier-1-blocking.md](principles/tier-1-blocking.md).

- [ ] **3.1 Intent-revealing names**: Names eliminate need for explanation
- [ ] **3.9 Semantic specificity**: `validate()` → `validate_user_input()`
- [ ] **3.5 No misleading names**: Behavior matches name exactly
- [ ] **1.1 Single Responsibility**: One reason to change per class
- [ ] **1.7 Separation of Concerns**: Data, logic, presentation separated
- [ ] **5.1 Specific exceptions**: No generic `except Exception:`
- [ ] **5.2 No silent failures**: No `except: pass`
- [ ] **2.9 Fail fast**: Validate at start, not after processing

⚠️ **CHECKPOINT**: Review each finding against Layer 1.
Does any suggestion conflict with a Philosophy? If YES → Revise to align.

- [ ] **All Tier 1 issues documented**

---

### Layer 3: Tier 2 Principles (Important)

Issues that **should be fixed**. See [principles/tier-2-important.md](principles/tier-2-important.md).

- [ ] **Naming**: Abbreviations, searchability, domain consistency, boolean naming
- [ ] **Structure**: Cohesion, coupling, dependency injection, abstraction levels
- [ ] **Functions**: Do one thing, length < 30 lines, max 4 params, nesting < 3 levels
- [ ] **Errors**: Context in messages, user vs system errors, fail safely
- [ ] **Code quality**: DRY, KISS, primitive obsession, magic numbers
- [ ] **Types**: Type hints, null safety, defensive at boundaries
- [ ] **Comments**: Explain why (not what), no outdated comments

⚠️ **CHECKPOINT**: Review each finding against Layer 1.
Does any suggestion conflict with a Philosophy? If YES → Revise to align.

- [ ] **All Tier 2 issues documented**

---

### Layer 4: Tier 3 Principles (Suggestions)

Nice-to-have improvements. See [principles/tier-3-suggestions.md](principles/tier-3-suggestions.md).

- [ ] **Style**: Noise words, composition over inheritance, feature envy
- [ ] **Code cleanup**: YAGNI, speculative generality, dead code
- [ ] **Interface design**: SOLID principles, Law of Demeter
- [ ] **Performance**: Only if profiled bottlenecks exist

⚠️ **CHECKPOINT**: Review each finding against Layer 1.
Does any suggestion conflict with a Philosophy? If YES → Revise to align.

- [ ] **All Tier 3 issues documented**

---

### Layer 5: Final Validation

Before generating report:

- [ ] Re-read ALL suggestions from Layers 2-4
- [ ] Verify NONE suggest comments for things that should be renames
- [ ] Verify all suggestions align with both Philosophies
- [ ] Remove any suggestions that slipped through checkpoints

⚠️ **FINAL CHECK**: If any suggestion says "add comment to explain [what code does]":
→ REPLACE with suggestion to rename/restructure
→ See [decision-logic/naming-vs-comments.md](decision-logic/naming-vs-comments.md)

- [ ] **Report ready to generate**

---

## Quick Reference: Common Patterns

### Naming → Comment Decision

```
Need to explain code?
├── Explaining WHAT → RENAME (Philosophy 1 applies)
└── Explaining WHY (business context) → Comment OK
```

See [decision-logic/naming-vs-comments.md](decision-logic/naming-vs-comments.md) for full decision tree.

### Philosophy Enforcement

```
For each suggestion:
├── Aligns with Philosophies? → Keep
└── Conflicts with Philosophy? → REVISE or REJECT
```

See [decision-logic/philosophy-enforcement.md](decision-logic/philosophy-enforcement.md) for details.

### Tier Quick Summary

| Tier | Enforcement | Focus |
|------|-------------|-------|
| 1 | Must fix | Names, SRP, error handling |
| 2 | Should fix | Structure, functions, types |
| 3 | Nice to have | Style, cleanup, performance |

---

## Reporting Format

Use this format for each issue found:

```markdown
## [filename]

### Layer [N]: [Issue Name] (Tier [T])
**Line [N]:** [Description of the issue]
**Philosophy alignment:** ✓ Compliant / ⚠️ Revised from [original suggestion]

**Current:**
```[language]
[code snippet]
```

**Suggested:**
```[language]
[improved code]
```

**Rationale:** [Brief explanation linking to philosophy or principle]
```

### Report Structure

```markdown
# Refactoring Review: [git diff command]

## Summary
- Layer 1 (Philosophy): [N] findings
- Layer 2 (Tier 1 - Blocking): [N] findings
- Layer 3 (Tier 2 - Important): [N] findings
- Layer 4 (Tier 3 - Suggestions): [N] findings

## Findings by File

### [filename1]
[Issues...]

### [filename2]
[Issues...]

## Philosophy Alignment Check
✓ All suggestions verified against Philosophies
✓ No comments suggested for WHAT explanations
✓ All naming follows semantic specificity
```

---

## Reference Materials

- [principles/index.md](principles/index.md) - Full principle classification
- [principles/tier-1-blocking.md](principles/tier-1-blocking.md) - Must-fix issues
- [principles/tier-2-important.md](principles/tier-2-important.md) - Should-fix issues
- [principles/tier-3-suggestions.md](principles/tier-3-suggestions.md) - Nice-to-have
- [decision-logic/philosophy-enforcement.md](decision-logic/philosophy-enforcement.md) - Override rules
- [decision-logic/naming-vs-comments.md](decision-logic/naming-vs-comments.md) - Common conflict resolution
- [examples/naming.md](examples/naming.md) - Naming examples
- [examples/structure.md](examples/structure.md) - Structure examples
- [examples/functions.md](examples/functions.md) - Function design examples
