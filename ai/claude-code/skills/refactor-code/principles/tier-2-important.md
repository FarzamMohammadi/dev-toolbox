# Tier 2: Important Principles

These issues **should be fixed**. Prominently flagged in review.

---

## Naming & Readability

### 3.2 Avoid Abbreviations
Spell out names unless universally understood.

**Bad:** `usr`, `cfg`, `btn`, `mgr`, `impl`, `ctx`
**Good:** `user`, `config`, `button`, `manager`, `implementation`, `context`

**Exception:** Universal abbreviations like `id`, `url`, `html`, `json`

### 3.3 Searchable Names
No single-letter or ambiguous names.

**Bad:**
```python
for i in d:
    t += i.p * i.q
```

**Good:**
```python
for item in order_items:
    total += item.price * item.quantity
```

**Exception:** Loop counters `i`, `j`, `k` in simple loops

### 3.4 Domain Consistency
Use one term per concept. If business says "customer," don't also use "user," "client," "buyer."

### 3.6 Boolean Naming
Prefix with `is_`, `has_`, `can_`, `should_`.

**Bad:** `active`, `permission`, `ready`
**Good:** `is_active`, `has_permission`, `is_ready`

### 3.7 Class/Method Naming
Classes = nouns (`Customer`, `Order`), Methods = verbs (`calculate()`, `validate()`)

---

## Structure

### 1.2 High Cohesion
Related functionality stays together.

**Bad:** `utils.py` with `parse_date()`, `send_email()`, `calculate_tax()`, `resize_image()`
**Good:** `date_utils.py`, `email_service.py`, `tax_calculator.py`

### 1.3 Low Coupling
Minimize dependencies between modules.

**Bad:**
```python
class OrderProcessor:
    def process(self):
        db = MySQLDatabase("localhost", "root", "pass")  # Hard-coded
```

**Good:**
```python
class OrderProcessor:
    def __init__(self, db):
        self.db = db  # Injected
```

### 1.5 Dependency Injection
Pass dependencies in, don't create internally.

### 1.6 Single Level of Abstraction
Don't mix high-level logic with low-level details.

**Bad:**
```python
def process_order(order):
    validate_order(order)  # High-level
    conn = sqlite3.connect('orders.db')  # Low-level!
    cursor = conn.cursor()
    cursor.execute("INSERT...")
    send_confirmation(order)  # High-level again
```

**Good:**
```python
def process_order(order):
    validate_order(order)
    save_order(order)  # Hides DB details
    send_confirmation(order)
```

### 1.9 Large Class / God Object
If you can't describe a class in one sentence, split it.

### 1.10 Circular Dependencies
Module A imports B, B imports A = problem. Break cycles with abstraction or restructuring.

---

## Function Design

### 2.1 Do One Thing
If description uses "and," split the function.

**Bad:** `save_user_and_send_welcome_email()`
**Good:** `save_user()` + `send_welcome_email()`

### 2.2 Function Length
Under 30 lines preferred. If longer, look for extraction opportunities.

### 2.3 Long Parameter List
More than 4 parameters = group into objects.

**Bad:** `create_user(name, email, street, city, state, zip, phone)`
**Good:** `create_user(name, email, address, contact_info)`

### 2.5 Deep Nesting
More than 3 levels = use early returns.

**Bad:**
```python
if data:
    if data.is_valid:
        if data.has_permission:
            if not data.is_expired:
                do_work(data)
```

**Good:**
```python
if not data:
    return None
if not data.is_valid:
    return None
if not data.has_permission:
    return None
if data.is_expired:
    return None
do_work(data)
```

### 2.6 Early Return Pattern
Guard clauses at the top, main logic at the bottom.

### 2.7 No Side Effects
If a function modifies state, make it obvious in the name.

**Bad:** `get_user()` that also updates `last_accessed`
**Good:** `get_user()` pure, `record_user_access()` separate

---

## Error Handling

### 5.3 Context in Errors
Include relevant data.

**Bad:** `raise ValueError("Invalid input")`
**Good:** `raise ValueError(f"Invalid order ID: {order_id}. Expected format: ORD-XXXX")`

### 5.4 User vs System Errors
User errors = friendly message. System errors = detailed log.

### 5.5 Fail Safely
Use transactions for operations that can fail partway.

---

## Code Quality

### 4.1 DRY
Same logic in two places = extract.

### 4.2 KISS
Simplest solution that works. No clever tricks.

### 4.6 Primitive Obsession
Create value objects instead of raw strings/ints.

**Bad:** `def send_email(to: str)` - any string accepted
**Good:** `def send_email(to: EmailAddress)` - validated type

### 4.7 Magic Numbers
Extract to named constants.

**Bad:** `if retries > 3: sleep(86400)`
**Good:** `if retries > MAX_RETRIES: sleep(SECONDS_PER_DAY)`

---

## Type Safety

### 8.1 Type Hints
Use type annotations for clarity and tooling.

### 8.2 Null Safety
Handle `None` explicitly with `Optional` types.

### 8.3 Defensive at Boundaries
Validate inputs from external sources (user input, APIs).

---

## Comments

### 6.2 Comments Explain Why
Comments explain business context, never what code does.

**Bad:** `# Increment counter` before `counter += 1`
**Good:** `# 30s timeout required by payment gateway SLA`

### 6.3 Outdated Comments
Comments that don't match code are worse than no comments.

---

## State

### 9.2 Global State
Avoid mutable global variables. Use dependency injection.
