# Code Block Extraction for Readability

Extract logical code blocks into well-named functions to make code read like an outline.

## The Core Principle

> **If you can describe what a code block does in a phrase, it should be a function with that name.**

This applies whether or not there's a comment. Comments are just a *signal* that extraction is needed - their absence doesn't mean the code is fine.

## What Triggers Extraction

| Signal | Action |
|--------|--------|
| Comment + code block | Extract, DELETE the comment (function name replaces it) |
| **Code block with NO comment** | **Still extract if it does a logical unit of work** |
| If block doing one thing | Extract to `_check_X()` or `_handle_X()` |
| For/while loop | Extract to `_process_X()` or `_iterate_X()` |
| Try/except block | Extract to `_safely_do_X()` |
| Multi-line sequence | Extract if it's a cohesive unit of work |

## The Test

Ask yourself: **"Can I describe what this block does in a short phrase?"**

- If YES → That phrase is the function name
- The block becomes the function body
- The parent function becomes more readable

## Goal: Functions Read Like Outlines

**Before (all implementation visible):**
```python
def validate_order(self, order, user_id):
    detected_violations = []
    violation_details = []

    if order.total > MAX_ORDER_AMOUNT:
        detected_violations.append("amount_exceeded")
        violation_details.append(f"Order total exceeds limit ({order.total})")

    for rule_name, checks in _VALIDATION_RULES.items():
        for check in checks:
            if check.fails(order):
                detected_violations.append(rule_name)
                violation_details.append(f"Failed: {rule_name}")
                break

    if detected_violations:
        result = ValidationResult(
            is_valid=False,
            details="; ".join(violation_details),
            failed_rules=tuple(detected_violations),
        )
        logger.bind(
            event="order_validation_failed",
            failed_rules=detected_violations,
            user_id=user_id,
        ).warning("Order validation failed")
        return result

    return ValidationResult(is_valid=True)
```

**After (reads like an outline):**
```python
def validate_order(self, order, user_id):
    detected_violations = []
    violation_details = []

    self._append_violation_if_amount_exceeded(order, detected_violations, violation_details)
    self._check_and_append_rule_violations(order, detected_violations, violation_details)

    if detected_violations:
        return self._create_and_log_validation_result(detected_violations, violation_details, user_id)

    return ValidationResult(is_valid=True)
```

The parent function now tells the story at a high level. Reader can dive into helpers only if they need the details.

---

## Examples

### Example 1: With Comment → Extract and Delete Comment

**Before:**
```python
# Check order amount
if order.total > MAX_ORDER_AMOUNT:
    detected_violations.append("amount_exceeded")
    violation_details.append(f"Order total exceeds limit ({order.total})")
```

**After:**
```python
self._append_violation_if_amount_exceeded(order, detected_violations, violation_details)
```

Comment is gone - function name says it all.

### Example 2: NO Comment, But Still Extract

**Before:**
```python
for rule_name, checks in _VALIDATION_RULES.items():
    for check in checks:
        if check.fails(order):
            detected_violations.append(rule_name)
            violation_details.append(f"Failed: {rule_name}")
            break
```

No comment here, but ask: "What does this block do?" → "Checks and appends rule violations"

**After:**
```python
self._check_and_append_rule_violations(order, detected_violations, violation_details)
```

### Example 3: Complex Block → Extract Regardless

**Before:**
```python
if detected_violations:
    result = ValidationResult(
        is_valid=False,
        details="; ".join(violation_details),
        failed_rules=tuple(detected_violations),
    )
    logger.bind(
        event="order_validation_failed",
        failed_rules=detected_violations,
        user_id=user_id,
    ).warning("Order validation failed")
    return result
```

What does it do? → "Creates and logs validation result"

**After:**
```python
if detected_violations:
    return self._create_and_log_validation_result(detected_violations, violation_details, user_id)
```

---

## Naming the Extracted Function

Convert the description to a function name:

| "What does this block do?" | Function Name |
|----------------------------|---------------|
| "Checks if order amount exceeds limit" | `_check_order_amount_exceeded()` |
| "Appends violation if amount exceeded" | `_append_violation_if_amount_exceeded()` |
| "Checks and appends rule violations" | `_check_and_append_rule_violations()` |
| "Creates and logs validation result" | `_create_and_log_validation_result()` |
| "Validates user credentials" | `_validate_user_credentials()` |
| "Sends notification email" | `_send_notification_email()` |

**Tips:**
- Use underscore prefix `_` for private helpers
- Include the action AND the subject
- Be specific: `_validate_X` not just `_validate`

---

## When NOT to Extract

Keep inline if:
1. **Single simple statement** - no block to extract
2. **Would need 6+ parameters** - extraction adds complexity
3. **Trivially obvious** - `x = x + 1` doesn't need a function
4. **Would be called exactly once and name adds nothing**

**Don't extract this (single assignment):**
```python
input_text = input_text or ""
```

**Don't extract this (trivially obvious):**
```python
count += 1
```

**Consider NOT extracting if passing too many args:**
```python
# If this would require passing 8 parameters, maybe restructure differently
_do_something(a, b, c, d, e, f, g, h)  # Too many - rethink
```

---

## The Hierarchy

```
Main function (reads like outline)
├── _helper_1()  (does one logical thing)
├── _helper_2()  (does one logical thing)
└── _helper_3()  (does one logical thing)
    └── _sub_helper()  (if helper is complex)
```

Reader understands at their desired level:
- **High level**: Read main function only
- **Medium level**: Read main + helper signatures
- **Deep level**: Read helper implementations
