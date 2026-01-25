# Naming Examples

Good and bad examples for naming principles.

---

## 3.1 Intent-Revealing Names

### Bad - Vague names require reading implementation
```python
def get(id, flag):
    ...

d = fetch()
for i in d:
    t += i.p * i.q
```

### Good - Names tell the story
```python
def get_customer_by_id_or_create_new(customer_id, create_if_missing):
    ...

order_items = fetch_order_items()
for item in order_items:
    total += item.price * item.quantity
```

---

## 3.9 Semantic Specificity

### Bad - Generic verbs without context
```python
class InputGuard:
    def validate(self, input):  # Validate what? How?
        ...

    def process(self, data):  # Process how?
        ...

    def check(self, value):  # Check for what?
        ...

    def handle(self, request):  # Handle how?
        ...
```

### Good - Specific verbs with clear scope
```python
class InputGuard:
    def validate_request_schema(self, request: Request) -> ValidationResult:
        ...

    def sanitize_user_input(self, raw_input: str) -> str:
        ...

    def check_rate_limit_exceeded(self, client_id: str) -> bool:
        ...

    def detect_and_log_suspicious_patterns(self, request: Request) -> None:
        ...
```

### The `input_guard.validate()` Case

**Original (too vague):**
```python
input_guard.validate(
    input_text=message.input or "",
```

**Wrong fix (comment instead of name):**
```python
# Validate and log any suspicious patterns (detection-only, does not block)
input_guard.validate(
    input_text=message.input or "",
```

**Correct fix (semantic specificity):**
```python
input_guard.detect_and_log_suspicious_patterns(
    input_text=message.input or "",
```

---

## 3.5 No Misleading Names

### Bad - Name doesn't match behavior
```python
def get_accounts():  # Returns single account!
    return db.find_one(...)

def is_valid():  # Returns error message, not bool!
    return "Invalid: missing field"

def calculate_total():  # Also saves to database!
    total = sum(items)
    db.save(total)
    return total

users = get_user()  # Plural name, singular value
```

### Good - Name matches behavior exactly
```python
def get_account():
    return db.find_one(...)

def get_validation_error() -> Optional[str]:
    return "Invalid: missing field"

def calculate_and_save_total():
    total = sum(items)
    db.save(total)
    return total

user = get_user()
```

---

## 3.6 Boolean Names

### Bad - Ambiguous
```python
active = check_status()
permission = verify_access()
ready = status()
```

### Good - Clear boolean intent
```python
is_active = check_status()
has_permission = verify_access()
is_ready = check_ready_status()
```

---

## Comments vs Names

### When you're tempted to add a comment, rename instead

**Bad - Comment explains what:**
```python
# Check if user can access premium features
if user.age >= 18 and user.tier == 'premium' and not user.overdue:
    grant_access()
```

**Good - Name explains what:**
```python
if user.is_eligible_for_premium_access():
    grant_access()
```

---

**Bad - Comment explains variable:**
```python
user_id = "user-123"
# Conversation owned by authenticated user
await storage.save_conversation(..., user_id=user_id)
```

**Good - Name communicates intent:**
```python
conversation_owner_id = "user-123"
await storage.save_conversation(..., user_id=conversation_owner_id)
```

---

**When comments ARE appropriate (explaining WHY):**
```python
# 30s timeout required by payment gateway SLA
PAYMENT_TIMEOUT_SECONDS = 30

# Skip validation for legacy accounts migrated before 2020 (JIRA-4521)
if account.created_before(datetime(2020, 1, 1)):
    skip_validation = True
```

These comments explain business context (WHY), not what the code does.
