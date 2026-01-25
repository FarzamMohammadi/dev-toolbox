# Function Design Examples

Good and bad examples for function design principles.

---

## 2.1 Do One Thing

### Bad - Function does multiple things
```python
def save_user_and_send_welcome_email(user):
    db.save(user)
    email.send(user.email, "Welcome!")
```

### Good - Each function does one thing
```python
def save_user(user):
    db.save(user)

def send_welcome_email(user):
    email.send(user.email, "Welcome!")

# Caller orchestrates
save_user(user)
send_welcome_email(user)
```

---

## 2.3 Long Parameter List

### Bad - Too many parameters
```python
def create_user(name, email, street, city, state, zip_code, phone, fax):
    ...
```

### Good - Grouped into objects
```python
def create_user(name, email, address: Address, contact: ContactInfo):
    ...

# Or even better
def create_user(user_data: UserCreationRequest):
    ...
```

---

## 2.4 Flag Parameters

### Bad - Boolean flag changes behavior
```python
def get_users(include_deleted=False):
    if include_deleted:
        return db.query("SELECT * FROM users")
    return db.query("SELECT * FROM users WHERE deleted = false")
```

### Good - Separate functions with clear names
```python
def get_active_users():
    return db.query("SELECT * FROM users WHERE deleted = false")

def get_all_users():
    return db.query("SELECT * FROM users")
```

---

## 2.5 Deep Nesting + 2.6 Early Return

### Bad - Deep nesting hard to follow
```python
def process(data):
    if data:
        if data.is_valid:
            if data.has_permission:
                if not data.is_expired:
                    return do_work(data)
    return None
```

### Good - Guard clauses flatten the logic
```python
def process(data):
    if not data:
        return None
    if not data.is_valid:
        return None
    if not data.has_permission:
        return None
    if data.is_expired:
        return None

    return do_work(data)
```

---

## 2.7 No Side Effects

### Bad - Hidden side effect
```python
def get_user(id):
    user = db.find(id)
    user.last_accessed = now()  # Hidden mutation!
    db.save(user)
    return user
```

### Good - Side effects explicit
```python
def get_user(id):
    return db.find(id)

def record_user_access(user):
    user.last_accessed = now()
    db.save(user)

# Caller decides
user = get_user(id)
record_user_access(user)  # Explicit
```

---

## 2.9 Fail Fast

### Bad - Validation too late
```python
def process_order(order):
    items = prepare_items(order)
    totals = calculate_totals(items)

    if not order:  # Too late!
        raise ValueError("Order required")

    return finalize(order, totals)
```

### Good - Validate upfront
```python
def process_order(order):
    if not order:
        raise ValueError("Order required")
    if not order.items:
        raise ValueError("Order must have items")
    if order.total <= 0:
        raise ValueError(f"Invalid total: {order.total}")

    # Now proceed safely
    items = prepare_items(order)
    totals = calculate_totals(items)
    return finalize(order, totals)
```

---

## 5.1 Specific Exceptions

### Bad - Catching too broadly
```python
try:
    process()
except Exception:
    log("Something went wrong")
```

### Good - Specific handling
```python
try:
    process()
except ValidationError as e:
    return {"error": str(e), "code": "VALIDATION_ERROR"}
except DatabaseError:
    logger.error("Database unavailable")
    raise ServiceUnavailable()
except ExternalAPIError as e:
    logger.warning(f"API call failed: {e}")
    return fallback_result()
```

---

## 5.2 Never Catch and Ignore

### Bad - Silent failure
```python
try:
    send_email()
except:
    pass  # Email silently fails forever
```

### Good - Handle meaningfully
```python
try:
    send_email()
except EmailError as e:
    logger.warning(f"Failed to send email: {e}")
    queue_for_retry()
```

---

## 5.3 Context in Errors

### Bad - Vague error
```python
raise ValueError("Invalid input")
```

### Good - Helpful error with context
```python
raise ValueError(
    f"Invalid order ID: {order_id}. "
    f"Expected format: ORD-XXXX. "
    f"Received: {raw_input}"
)
```

---

## 5.5 Fail Safely

### Bad - Partial failure leaves bad state
```python
def transfer(from_acct, to_acct, amount):
    from_acct.balance -= amount
    # If this line fails, money disappears!
    to_acct.balance += amount
```

### Good - Atomic operation
```python
def transfer(from_acct, to_acct, amount):
    with db.transaction():
        from_acct.balance -= amount
        to_acct.balance += amount
        # Both succeed or both fail
```
