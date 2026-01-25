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
