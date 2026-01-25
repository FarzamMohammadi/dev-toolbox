# Philosophy Enforcement Rules

Philosophies are the user's core coding beliefs. They **always override** principles.

## The Hierarchy

```
PHILOSOPHIES (Non-negotiable)
    │
    ▼
PRINCIPLES (Secondary - must defer to philosophies)
```

## Checkpoint Decision Tree

Use this after EVERY layer to validate suggestions:

```
For each refactoring suggestion:
│
├── Does it align with ALL philosophies?
│   │
│   ├── YES → Keep the suggestion
│   │
│   └── NO → Which philosophy does it violate?
│       │
│       ├── Code as Communication?
│       │   └── REVISE: Suggest rename/restructure instead of comment
│       │
│       └── Reducing Cognitive Load?
│           └── REVISE: Suggest extraction to named function
│
└── After revision, re-check against philosophies
```

## Common Violations to Catch

| Suggestion | Violates | Correct Alternative |
|------------|----------|---------------------|
| "Add comment to explain what code does" | Code as Communication | Rename function/variable to be self-explanatory |
| "Add comment explaining the condition" | Code as Communication | Extract condition to well-named function |
| "Document this complex logic" | Reducing Cognitive Load | Extract to named functions with clear hierarchy |
| "Add inline explanation" | Code as Communication | Improve naming or extract |

## The Golden Rule

> If you're about to suggest a comment that explains WHAT code does, STOP.
> Suggest renaming or restructuring instead.
> Comments only explain WHY (business context), never WHAT.

## Example: `input_guard.validate()` Case

**Wrong approach (violates philosophy):**
```python
# Validate and log any suspicious patterns (detection-only, does not block)
input_guard.validate(request)
```

**Correct approach (follows philosophy):**
```python
input_guard.detect_and_log_suspicious_patterns(request)
```

The function name communicates the intent. No comment needed.
