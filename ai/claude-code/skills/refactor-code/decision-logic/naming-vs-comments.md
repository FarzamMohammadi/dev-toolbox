# Decision Tree: Naming vs Comments

The most common conflict. Use this to decide correctly every time.

## The Core Question

```
Does this code need explanation?
│
├── NO → No action needed
│
└── YES → What am I explaining?
    │
    ├── WHAT the code does (behavior, logic, purpose)
    │   │
    │   └── ❌ DO NOT ADD A COMMENT
    │       │
    │       └── Instead, choose one:
    │           ├── Rename variable to reveal intent
    │           ├── Rename function to describe what it does
    │           ├── Extract logic to well-named function
    │           └── Restructure for clarity
    │
    └── WHY the code does something (business context, constraints)
        │
        └── ✅ COMMENT IS APPROPRIATE
            │
            Examples of valid "why" comments:
            ├── "30s timeout required by payment gateway SLA"
            ├── "Skip validation for legacy migrated accounts (JIRA-1234)"
            ├── "Order matters: auth must complete before rate limiting"
            └── "Using deprecated API until v3 migration (Q2 deadline)"
```

## Quick Test

Ask yourself: **"Could this explanation become part of a name?"**

- If YES → It's explaining WHAT → Don't comment, rename instead
- If NO → It's explaining WHY → Comment is OK

## Examples

### Explaining WHAT → Rename

**Bad (comment explains what):**
```python
# Check if user can access premium features
if user.age >= 18 and user.tier == 'premium' and not user.overdue:
    grant_access()
```

**Good (name explains what):**
```python
if user.is_eligible_for_premium_access():
    grant_access()
```

---

**Bad (comment explains what):**
```python
# Validate input and log suspicious patterns
input_guard.validate(request)
```

**Good (name explains what):**
```python
input_guard.validate_and_log_suspicious_patterns(request)
# Or better, if it's detection-only:
input_guard.detect_suspicious_patterns(request)
```

---

**Bad (comment explains what):**
```python
data = process(items)  # Calculate totals and apply discounts
```

**Good (name explains what):**
```python
totals_with_discounts = calculate_totals_with_discounts(items)
```

### Explaining WHY → Comment OK

**Good (comment explains why):**
```python
# Payment gateway requires exactly 30s timeout per their SLA
PAYMENT_TIMEOUT = 30
```

**Good (comment explains why):**
```python
# Legacy accounts migrated before 2020 bypass email verification (JIRA-4521)
if account.migration_date < datetime(2020, 1, 1):
    skip_email_verification = True
```

**Good (comment explains why):**
```python
# Rate limiting must happen AFTER auth to track per-user limits
authenticate(request)
apply_rate_limit(request)
```

## Anti-Pattern Checklist

Before suggesting a comment, verify it's NOT one of these:

| Anti-Pattern | Why It's Wrong | Do This Instead |
|--------------|----------------|-----------------|
| "This function validates X" | Explaining WHAT | Rename function to include "validate_X" |
| "Loop through items and..." | Explaining WHAT | Extract to `process_items()` or similar |
| "Check if condition is met" | Explaining WHAT | Extract condition to `is_condition_met()` |
| "Handle the error case" | Explaining WHAT | Rename function or extract error handling |
| "Convert X to Y format" | Explaining WHAT | Rename to `convert_X_to_Y()` |

## The `input_guard.validate()` Case Study

This is the exact case that prompted the skill restructure.

**Original code:**
```python
input_guard.validate(
    input_text=message.input or "",
```

**Wrong suggestion (added comment):**
```python
# Validate and log any suspicious patterns (detection-only, does not block)
input_guard.validate(
    input_text=message.input or "",
```

**Why it's wrong:**
- The comment explains WHAT the function does
- This is exactly what Philosophy 1 (Code as Communication) forbids
- The function name should communicate this, not a comment

**Correct suggestion:**
```python
input_guard.detect_and_log_suspicious_patterns(
    input_text=message.input or "",
```

Or if `validate` must stay, add semantic specificity:
```python
input_guard.validate_input_for_suspicious_patterns(
    input_text=message.input or "",
```
