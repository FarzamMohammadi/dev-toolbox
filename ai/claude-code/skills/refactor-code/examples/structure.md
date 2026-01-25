# Structure Examples

Good and bad examples for structural principles.

---

## 1.1 Single Responsibility Principle

### Bad - Multiple reasons to change
```python
class UserManager:
    def authenticate(self, username, password): ...
    def send_email(self, user, message): ...
    def generate_report(self, user): ...
    def backup_database(self): ...
```

### Good - Each class has one job
```python
class Authenticator:
    def authenticate(self, username, password): ...

class EmailService:
    def send(self, recipient, message): ...

class ReportGenerator:
    def generate(self, user): ...

class DatabaseBackup:
    def backup(self): ...
```

---

## 1.2 High Cohesion

### Bad - Unrelated functions in one file
```python
# utils.py - grab bag of unrelated functions
def parse_date(s): ...
def send_email(to, body): ...
def calculate_tax(amount): ...
def resize_image(img): ...
```

### Good - Related functions grouped
```python
# date_utils.py
def parse_date(s): ...
def format_date(d): ...

# email_service.py
def send_email(to, body): ...
def validate_email(addr): ...

# tax_calculator.py
def calculate_tax(amount): ...
def get_tax_rate(region): ...
```

---

## 1.3 Low Coupling + 1.5 Dependency Injection

### Bad - Hard-coded dependencies
```python
class OrderProcessor:
    def process(self, order):
        db = MySQLDatabase("localhost", "root", "pass")
        emailer = SmtpEmailer("smtp.gmail.com", 587)
        logger = FileLogger("/var/log/orders.log")
        # ...
```

### Good - Dependencies injected
```python
class OrderProcessor:
    def __init__(self, db, emailer, logger):
        self.db = db
        self.emailer = emailer
        self.logger = logger

    def process(self, order):
        # Uses injected dependencies
        # Easy to test with mocks
```

---

## 1.6 Single Level of Abstraction

### Bad - Mixed abstraction levels
```python
def process_order(order):
    validate_order(order)  # High-level

    # Low-level database code mixed in
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders VALUES (?, ?)", (order.id, order.total))
    conn.commit()

    send_confirmation(order)  # High-level again
```

### Good - Consistent abstraction
```python
def process_order(order):
    validate_order(order)
    save_order(order)  # Implementation hidden
    send_confirmation(order)

def save_order(order):
    # Low-level details isolated here
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders VALUES (?, ?)", (order.id, order.total))
    conn.commit()
```

---

## 1.7 Separation of Concerns

### Bad - Data, logic, and presentation mixed
```python
def display_user_report(user_id):
    # Data access
    conn = psycopg2.connect(...)
    user = conn.execute("SELECT * FROM users WHERE id = ?", user_id)

    # Business logic
    stats = calculate_stats(user)

    # Presentation
    html = f"<h1>{user.name}</h1><p>Sales: ${stats.sales}</p>"
    return html
```

### Good - Separated concerns
```python
# repository.py (data access)
def get_user(user_id):
    conn = psycopg2.connect(...)
    return conn.execute("SELECT * FROM users WHERE id = ?", user_id)

# service.py (business logic)
def calculate_user_stats(user):
    return Stats(sales=sum(user.orders), ...)

# view.py (presentation)
def render_user_report(user, stats):
    return f"<h1>{user.name}</h1><p>Sales: ${stats.sales}</p>"

# Orchestration
def display_user_report(user_id):
    user = get_user(user_id)
    stats = calculate_user_stats(user)
    return render_user_report(user, stats)
```

---

## Reducing Cognitive Load - Hierarchical Abstraction

### Bad - All details at one level
```python
def process_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.customer.balance < 0:
        raise ValueError("Customer has negative balance")

    total = 0
    for item in order.items:
        price = item.base_price
        if item.discount_code:
            discount = db.query(f"SELECT rate FROM discounts WHERE code = '{item.discount_code}'")
            if discount:
                price *= (1 - discount.rate)
        total += price * item.quantity

    order.total = total
    order.status = 'processed'
    db.save(order)
    email_service.send(order.customer.email, f"Order {order.id} confirmed")
```

### Good - Hierarchical (read at your level of interest)
```python
def process_order(order):
    validate_order(order)
    order.total = calculate_order_total(order)
    finalize_order(order)
    notify_customer(order)

# Details hidden in helper functions
def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.customer.balance < 0:
        raise ValueError("Customer has negative balance")

def calculate_order_total(order):
    return sum(calculate_item_price(item) for item in order.items)

def calculate_item_price(item):
    price = item.base_price
    discount = get_discount_rate(item.discount_code)
    return price * (1 - discount) * item.quantity
```

Reader can understand the high-level flow from `process_order()` without reading implementation details.

---

## Logical Code Blocks → Extract to Named Functions

Extract code blocks into well-named functions for readability - **whether or not there's a comment**.

Comments are just a signal. If you can describe what a block does in a phrase, it should be a function with that name.

### Bad - Comment explains what the code does
```python
def validate_order(self, order, user_id, session_id):
    detected_violations = []
    violation_details = []

    # Check order amount
    if order.total > MAX_ORDER_AMOUNT:
        detected_violations.append("amount_exceeded")
        violation_details.append(f"Order total exceeds limit ({order.total} > {MAX_ORDER_AMOUNT})")

    # Check each validation rule
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

        # Structured logging for monitoring
        logger.bind(
            event="order_validation_failed",
            failed_rules=detected_violations,
            user_id=user_id,
        ).warning(f"Order validation failed")

        return result

    return ValidationResult(is_valid=True)
```

### Good - Comments replaced with well-named functions
```python
def validate_order(self, order, user_id, session_id):
    detected_violations = []
    violation_details = []

    self._append_violation_if_amount_exceeded(order, detected_violations, violation_details)
    self._check_and_append_rule_violations(order, detected_violations, violation_details)

    if detected_violations:
        return self._create_and_log_validation_result(
            detected_violations, violation_details, user_id, session_id, order.total
        )

    return ValidationResult(is_valid=True)

def _append_violation_if_amount_exceeded(self, order, detected_violations, violation_details):
    if order.total > MAX_ORDER_AMOUNT:
        detected_violations.append("amount_exceeded")
        violation_details.append(f"Order total exceeds limit ({order.total} > {MAX_ORDER_AMOUNT})")

def _check_and_append_rule_violations(self, order, detected_violations, violation_details):
    for rule_name, checks in _VALIDATION_RULES.items():
        for check in checks:
            if check.fails(order):
                detected_violations.append(rule_name)
                violation_details.append(f"Failed: {rule_name}")
                break

def _create_and_log_validation_result(self, detected_violations, violation_details, user_id, session_id, order_total):
    result = ValidationResult(
        is_valid=False,
        details="; ".join(violation_details),
        failed_rules=tuple(detected_violations),
    )

    logger.bind(
        event="order_validation_failed",
        failed_rules=detected_violations,
        user_id=user_id,
    ).warning(f"Order validation failed")

    return result
```

**Why this is better:**
1. Main function reads like an outline - easy to understand at a glance
2. No comments needed - function names communicate intent
3. Each extracted function has a single responsibility
4. Reader can dive into details only when needed

---

### Example: Extraction WITHOUT Comments

The code below has NO comments, but still needs extraction:

**Bad - No comments, but blocks should still be extracted:**
```python
def process_user_data(user, settings):
    if not user.email or "@" not in user.email:
        raise ValueError(f"Invalid email: {user.email}")
    if user.age < 0 or user.age > 150:
        raise ValueError(f"Invalid age: {user.age}")

    normalized_name = user.name.strip().title()
    normalized_email = user.email.lower().strip()

    if settings.notify_on_signup:
        email_client.send(
            to=normalized_email,
            subject="Welcome!",
            body=f"Hello {normalized_name}, welcome to our platform."
        )

    return User(name=normalized_name, email=normalized_email, age=user.age)
```

**Good - Extract logical blocks even without comments:**
```python
def process_user_data(user, settings):
    _validate_user_fields(user)
    normalized = _normalize_user_data(user)
    _send_welcome_email_if_enabled(normalized, settings)
    return normalized

def _validate_user_fields(user):
    if not user.email or "@" not in user.email:
        raise ValueError(f"Invalid email: {user.email}")
    if user.age < 0 or user.age > 150:
        raise ValueError(f"Invalid age: {user.age}")

def _normalize_user_data(user):
    return User(
        name=user.name.strip().title(),
        email=user.email.lower().strip(),
        age=user.age
    )

def _send_welcome_email_if_enabled(user, settings):
    if settings.notify_on_signup:
        email_client.send(
            to=user.email,
            subject="Welcome!",
            body=f"Hello {user.name}, welcome to our platform."
        )
```

**Key insight:** No comments were present in the original, but we could still ask "what does this block do?" and extract accordingly:
- Validation block → `_validate_user_fields()`
- Normalization block → `_normalize_user_data()`
- Email block → `_send_welcome_email_if_enabled()`
