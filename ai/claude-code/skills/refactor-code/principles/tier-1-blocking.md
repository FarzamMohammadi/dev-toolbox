# Tier 1: Blocking Principles

These issues **must be fixed**. Review is blocked until resolved.

---

## 3.1 Intent-Revealing Names

Names should make code self-documenting.

**Violation signals:**
- Variable named `data`, `temp`, `result`, `info`, `item`
- Function named `process()`, `handle()`, `do()`, `run()` without specifics
- Need to read implementation to understand purpose

**Fix:** Ask "what specifically?" and put that in the name.

**See:** [examples/naming.md](../examples/naming.md)

---

## 3.9 Semantic Specificity (NEW)

Function/method names must specify WHAT they operate on.

**Violation signals:**
- `validate()` - validate what?
- `process()` - process what?
- `check()` - check what?
- `get()` - get what?
- `update()` - update what?

**Fix:** `validate_user_credentials()`, `process_payment_request()`, `check_inventory_levels()`

**Example:**
```python
# Bad
input_guard.validate(request)

# Good
input_guard.validate_request_schema(request)
# Or
input_guard.detect_suspicious_patterns(request)
```

---

## 3.5 No Misleading Names

Names must match behavior exactly.

**Violation signals:**
- `getX()` that modifies state (should be `fetchX()` or `retrieveAndUpdateX()`)
- `isValid()` that returns an error message (should be `getValidationError()`)
- Plural name for single item or vice versa
- `calculate()` that also saves (should be `calculateAndSave()` or split)

**Fix:** Rename to match actual behavior.

---

## 1.1 Single Responsibility Principle

Each class/module has exactly one reason to change.

**Violation signals:**
- Class name contains "And" or "Manager" with multiple concerns
- File > 500 lines
- Module imports from 5+ unrelated domains
- Class methods touch unrelated data

**Fix:** Split by responsibility into focused classes.

---

## 1.7 Separation of Concerns

Data access, business logic, and presentation must be separated.

**Violation signals:**
- SQL queries in controller/view code
- HTML generation in business logic
- API calls mixed with data transformation

**Fix:** Extract into layers - repository for data, service for logic, view for presentation.

---

## 5.1 Specific Exceptions

Catch specific exception types, not generic `Exception`.

**Violation signals:**
- `except Exception:`
- `except:` (bare except)
- Catching broad exception when specific is available

**Fix:** Catch the specific exception type you're handling.

```python
# Bad
try:
    process()
except Exception:
    log("error")

# Good
try:
    process()
except ValidationError as e:
    return {"error": str(e)}
except DatabaseError:
    raise ServiceUnavailable()
```

---

## 5.2 Never Catch and Ignore

Silent `except: pass` hides bugs.

**Violation signals:**
- `except: pass`
- `except Exception: pass`
- Empty except blocks
- Catch with only a `continue`

**Fix:** Always log, re-raise, or handle meaningfully.

```python
# Bad
try:
    send_email()
except:
    pass

# Good
try:
    send_email()
except EmailError as e:
    logger.warning(f"Failed to send: {e}")
    queue_for_retry()
```

---

## 2.9 Fail Fast

Validate inputs at the start, not after processing.

**Violation signals:**
- Validation after computation
- Error check at end of function
- Processing null/invalid data then checking

**Fix:** Guard clauses at function start.

```python
# Bad
def process_order(order):
    items = prepare_items(order)
    totals = calculate(items)
    if not order:  # Too late!
        raise ValueError("Order required")

# Good
def process_order(order):
    if not order:
        raise ValueError("Order required")
    if not order.items:
        raise ValueError("Order must have items")
    # Now proceed safely
```
