---
name: refactor-code
description: Review git diffs against comprehensive refactoring principles. Use when user wants code review, refactoring suggestions, or mentions reviewing changes.
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [git-diff-command]
context: fork
---

# Ultimate Code Refactoring Agent

Reviews changed files in a git diff and applies comprehensive refactoring principles to produce maintainable, evolvable, and intuitive code.

## Usage

```
Review commits: /refactor-code git diff main...HEAD
Review last commit: /refactor-code git diff HEAD~1
Review specific range: /refactor-code git diff abc123..def456
Review staged changes: /refactor-code git diff --cached
```

## Philosophy

Philosophies are higher-priority guiding beliefs that inform all the principles below.

### Code as Communication

**Code should communicate as effectively, clearly, and comprehensively as possible to decrease mental load and make the codebase intuitive to follow, understand, maintain, and modify.**

Key tenets:
- **Names over comments**: Use descriptive variable, function, and class names that eliminate the need for explanatory comments
- **Self-documenting code**: The code itself should tell the story; comments should only explain "why" for non-obvious decisions
- **Concise yet complete**: Names should be descriptive enough to convey meaning without being verbose
- **Extract for clarity**: Complex conditions and logic blocks should be extracted into well-named functions that describe their purpose—readers understand intent from the function name without needing to examine implementation

**Before (comment explains intent):**
```python
user_id = "user-123"
# Conversation owned by authenticated user
await storage.save_conversation(..., user_id=user_id)

headers = {...}  # Headers for the owner
```

**After (names communicate intent):**
```python
conversation_owner_id = "user-123"
await storage.save_conversation(..., user_id=conversation_owner_id)

owner_headers = {...}
```

**Before (reader must parse the condition):**
```python
if user.age >= 18 and user.subscription_tier == 'premium' and not user.has_overdue_balance:
    grant_access()
```

**After (function name communicates intent):**
```python
if is_eligible_for_premium_access(user):
    grant_access()
```

### Reducing Cognitive Load

**Structure code to minimize the mental effort required to understand it. Enable readers to grasp intent at their desired level of abstraction.**

Key tenets:
- **Hierarchical abstraction**: Organize code in layers—high-level orchestration functions call well-named lower-level functions. Readers can understand the "what" without diving into the "how"
- **Progressive disclosure**: Complex details should be hidden until needed. Main functions read like an outline; implementation details live in helper functions
- **Chunking**: Group related operations together. Unrelated logic in the same function forces readers to track multiple mental threads
- **Intuitive structure**: File names, directory structure, and component organization should match the mental model of the domain
- **Consistent patterns**: Use the same patterns for similar operations. Inconsistency forces readers to re-learn for each instance

**Before (all details at one level - high cognitive load):**
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

**After (hierarchical - read at your level of interest):**
```python
def process_order(order):
    validate_order(order)
    order.total = calculate_order_total(order)
    finalize_order(order)
    notify_customer(order)
```

---

## Process

1. Run the specified `git diff` command
2. For each changed file, read and review the full file context
3. Apply all principles below, checking for violations
4. Report issues found with `file:line` references
5. Suggest specific refactoring for each violation

---

## Principles

### 1. Structural / Architectural

#### 1.1 Single Responsibility Principle
Each class/module should have only one reason to change. When something has multiple responsibilities, changes in one area risk breaking others.

**Bad:**
```python
class UserManager:
    def authenticate(self, username, password): ...
    def send_email(self, user, message): ...
    def generate_report(self, user): ...
    def backup_database(self): ...
```

**Good:**
```python
class Authenticator:
    def authenticate(self, username, password): ...

class EmailService:
    def send(self, recipient, message): ...

class ReportGenerator:
    def generate(self, user): ...
```

#### 1.2 High Cohesion
Keep related functionality together in the same module. Unrelated functionality should be separated into different modules.

**Bad:**
```python
# utils.py - grab bag of unrelated functions
def parse_date(s): ...
def send_email(to, body): ...
def calculate_tax(amount): ...
def resize_image(img): ...
```

**Good:**
```python
# date_utils.py
def parse_date(s): ...
def format_date(d): ...

# email_service.py
def send_email(to, body): ...
def validate_email(addr): ...
```

#### 1.3 Low Coupling
Minimize dependencies between modules so changes in one don't ripple through others.

**Bad:**
```python
class OrderProcessor:
    def process(self, order):
        db = MySQLDatabase("localhost", "root", "pass")
        emailer = SmtpEmailer("smtp.gmail.com", 587)
        logger = FileLogger("/var/log/orders.log")
```

**Good:**
```python
class OrderProcessor:
    def __init__(self, db, emailer, logger):
        self.db = db
        self.emailer = emailer
        self.logger = logger
```

#### 1.4 Composition Over Inheritance
Favor composing objects over inheritance hierarchies. Inheritance creates tight coupling and fragile base class problems.

**Bad:**
```python
class Animal:
    def move(self): ...

class Bird(Animal):
    def move(self): print("fly")

class Penguin(Bird):  # Penguins can't fly!
    def move(self): print("walk")  # Violates expectations
```

**Good:**
```python
class Animal:
    def __init__(self, movement_strategy):
        self.movement = movement_strategy

penguin = Animal(WalkingMovement())
eagle = Animal(FlyingMovement())
```

#### 1.5 Dependency Injection
Pass dependencies into components rather than having them create dependencies internally. Makes testing and swapping implementations trivial.

**Bad:**
```python
class ReportGenerator:
    def generate(self):
        db = PostgresDatabase()  # Hard-coded dependency
        data = db.query("SELECT * FROM sales")
```

**Good:**
```python
class ReportGenerator:
    def __init__(self, database):
        self.db = database

    def generate(self):
        data = self.db.query("SELECT * FROM sales")
```

#### 1.6 Single Level of Abstraction
Functions should operate at one consistent abstraction level. Don't mix high-level business logic with low-level implementation details.

**Bad:**
```python
def process_order(order):
    # High-level
    validate_order(order)
    # Low-level mixed in
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders VALUES (?, ?)", (order.id, order.total))
    conn.commit()
    # High-level again
    send_confirmation(order)
```

**Good:**
```python
def process_order(order):
    validate_order(order)
    save_order(order)
    send_confirmation(order)
```

#### 1.7 Separation of Concerns
Partition code into distinct sections each addressing a separate concern (data access, business logic, presentation).

**Bad:**
```python
def display_user_report(user_id):
    conn = psycopg2.connect(...)
    user = conn.execute("SELECT * FROM users WHERE id = ?", user_id)
    html = f"<h1>{user.name}</h1><p>Sales: ${user.sales}</p>"
    return html
```

**Good:**
```python
# repository.py
def get_user(user_id): ...

# service.py
def calculate_user_stats(user): ...

# view.py
def render_user_report(user, stats): ...
```

#### 1.8 Feature Envy
When a method uses many methods/data from another class, it probably belongs in that class instead.

**Bad:**
```python
class Order:
    def __init__(self):
        self.items = []

class PriceCalculator:
    def calculate(self, order):
        total = 0
        for item in order.items:  # Envies Order's data
            total += item.price * item.quantity
        if order.customer.is_premium:
            total *= 0.9
        return total
```

**Good:**
```python
class Order:
    def calculate_total(self):
        subtotal = sum(item.price * item.quantity for item in self.items)
        return self.customer.apply_discount(subtotal)
```

#### 1.9 Large Class / God Object
Classes doing too much should be split. If you can't describe a class's purpose in one sentence, it's too big.

**Bad:**
```python
class Application:
    def handle_login(self): ...
    def handle_logout(self): ...
    def process_payment(self): ...
    def generate_invoice(self): ...
    def send_notification(self): ...
    def backup_data(self): ...
    def generate_report(self): ...
    # 50+ more methods...
```

**Good:**
Split into `AuthController`, `PaymentService`, `InvoiceGenerator`, `NotificationService`, etc.

#### 1.10 Circular Dependencies
Modules that depend on each other in cycles create tight coupling and make code impossible to understand or test in isolation.

**Bad:**
```python
# order.py
from customer import Customer
class Order: ...

# customer.py
from order import Order  # Circular!
class Customer: ...
```

**Good:**
Extract shared abstractions or use dependency injection to break the cycle.

#### 1.11 Layered Architecture
Organize code into horizontal layers where each layer depends only on layers below it. Cross-layer dependencies create brittleness.

**Bad:** Controller directly accesses database, bypassing service layer.

**Good:**
```
Controller → Service → Repository → Database
     ↓           ↓           ↓
   (HTTP)    (Business)   (Data)
```

#### 1.12 Package by Feature, Not Layer
Group code by feature/domain rather than by technical layer. Keeps related code together and reduces coupling between features.

**Bad:**
```
controllers/
    user_controller.py
    order_controller.py
services/
    user_service.py
    order_service.py
```

**Good:**
```
users/
    controller.py
    service.py
    repository.py
orders/
    controller.py
    service.py
    repository.py
```

---

### 2. Function / Method Design

#### 2.1 Do One Thing
Functions should do a single task well. If you describe it with "and," it should be split.

**Bad:**
```python
def save_user_and_send_welcome_email(user):
    db.save(user)
    email.send(user.email, "Welcome!")
```

**Good:**
```python
def save_user(user):
    db.save(user)

def send_welcome_email(user):
    email.send(user.email, "Welcome!")
```

#### 2.2 Function Length
Keep functions under 20-30 lines. Longer functions are harder to understand, test, and modify.

#### 2.3 Long Parameter List
Functions with 4+ parameters indicate the function is doing too much. Group related parameters into objects.

**Bad:**
```python
def create_user(name, email, street, city, state, zip, phone, fax):
```

**Good:**
```python
def create_user(name, email, address, contact_info):
```

#### 2.4 Flag Parameters
Boolean parameters that change function behavior should be replaced with separate functions or polymorphism.

**Bad:**
```python
def get_users(include_deleted=False):
    if include_deleted:
        return db.query("SELECT * FROM users")
    return db.query("SELECT * FROM users WHERE deleted = false")
```

**Good:**
```python
def get_active_users():
    return db.query("SELECT * FROM users WHERE deleted = false")

def get_all_users():
    return db.query("SELECT * FROM users")
```

#### 2.5 Deep Nesting
More than 2-3 levels of nesting makes code hard to follow. Use early returns (guard clauses) to flatten logic.

**Bad:**
```python
def process(data):
    if data:
        if data.is_valid:
            if data.has_permission:
                if not data.is_expired:
                    return do_work(data)
    return None
```

**Good:**
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

#### 2.6 Early Return Pattern
Return or throw from functions early if preconditions fail. Execute main logic only after all guards pass.

#### 2.7 No Side Effects
Functions should be predictable. If a function modifies state, files, or globals, it should be obvious from the name.

**Bad:**
```python
def get_user(id):
    user = db.find(id)
    user.last_accessed = now()  # Hidden side effect!
    db.save(user)
    return user
```

**Good:**
```python
def get_user(id):
    return db.find(id)

def record_user_access(user):
    user.last_accessed = now()
    db.save(user)
```

#### 2.8 Output Parameters
Don't use mutable reference parameters for output. Return values instead.

**Bad:**
```python
def calculate(data, result):
    result['total'] = sum(data)
    result['average'] = result['total'] / len(data)
```

**Good:**
```python
def calculate(data):
    total = sum(data)
    return {'total': total, 'average': total / len(data)}
```

#### 2.9 Fail Fast
Validate inputs and preconditions at the start. Errors discovered early prevent cascading failures.

**Bad:**
```python
def process_order(order):
    items = prepare_items(order)
    totals = calculate_totals(items)
    if not order:  # Too late!
        raise ValueError("Order required")
```

**Good:**
```python
def process_order(order):
    if not order:
        raise ValueError("Order required")
    if not order.items:
        raise ValueError("Order must have items")
    # Now proceed with valid data
```

---

### 3. Naming & Readability

#### 3.1 Reveal Intent Through Names
Names should make code self-documenting.

**Bad:**
```python
def get(id, flag):
    ...
```

**Good:**
```python
def get_customer_by_id_or_create_new(customer_id, create_if_missing):
    ...
```

#### 3.2 Avoid Abbreviations
Spell out names fully unless universally understood.

**Bad:** `usr`, `cfg`, `btn`, `mgr`, `impl`

**Good:** `user`, `config`, `button`, `manager`, `implementation`

#### 3.3 Searchable Names
Avoid single-letter or ambiguous names.

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

#### 3.4 Domain Language Consistency
Use terms from the problem domain consistently. If the business calls it "customer," don't call it "user," "client," and "buyer" in different places.

#### 3.5 Misleading Names
Names should match behavior. `accounts` should be a collection. `is_ready` should return boolean.

**Bad:**
```python
def get_accounts():  # Returns single account
    return db.find_one(...)

def is_valid():  # Returns error message string
    return "Invalid: missing field"
```

#### 3.6 Boolean Names
Prefix with `is_`, `has_`, `can_`, `should_`. Names should clearly indicate boolean nature.

**Bad:** `active`, `permission`, `ready`

**Good:** `is_active`, `has_permission`, `is_ready`

#### 3.7 Class Names Are Nouns, Methods Are Verbs
Classes represent things (`Customer`, `Order`). Methods describe actions (`calculate()`, `validate()`).

**Bad:**
```python
class ProcessOrder:  # Verb as class name
    def data(self):  # Noun as method name
```

**Good:**
```python
class OrderProcessor:
    def process(self):
```

#### 3.8 Noise Words
Remove redundant words that add no information.

**Bad:** `UserObject`, `CustomerData`, `AccountInfo`, `OrderDetails`

**Good:** `User`, `Customer`, `Account`, `Order`

---

### 4. Code Duplication & Simplification

#### 4.1 DRY - Don't Repeat Yourself
Every piece of logic should exist in exactly one place. Duplicated code multiplies bugs and maintenance cost.

**Bad:**
```python
def get_active_users():
    return [u for u in users if u.status == 'active' and not u.deleted]

def count_active_users():
    return len([u for u in users if u.status == 'active' and not u.deleted])
```

**Good:**
```python
def get_active_users():
    return [u for u in users if u.status == 'active' and not u.deleted]

def count_active_users():
    return len(get_active_users())
```

#### 4.2 KISS - Keep It Simple
Choose the simplest solution that solves the problem. Complexity is the enemy of maintainability.

**Bad:**
```python
def is_even(n):
    return n & 1 == 0 if isinstance(n, int) else None
```

**Good:**
```python
def is_even(n):
    return n % 2 == 0
```

#### 4.3 YAGNI - You Aren't Gonna Need It
Don't build features "just in case." Speculative features add complexity without immediate value.

**Bad:**
```python
class User:
    def __init__(self):
        self.name = ""
        self.email = ""
        self.fax = ""  # Nobody uses fax anymore
        self.pager = ""  # Just in case
        self.telex = ""  # Future-proofing!
```

#### 4.4 Speculative Generality
Remove overly complex code built for hypothetical future use that isn't needed now.

**Bad:** Creating abstract factory patterns for a system that will only ever have one implementation.

#### 4.5 Dead Code
Unreachable or unused code should be deleted, not commented out. Version control preserves history.

**Bad:**
```python
def process():
    do_work()
    # Old implementation - keeping just in case
    # old_do_work()
    # more_old_stuff()
```

**Good:**
```python
def process():
    do_work()
```

#### 4.6 Primitive Obsession
Using primitives (strings, ints) instead of domain objects. Create value objects with validation and business logic.

**Bad:**
```python
def send_email(to: str):  # Any string allowed
    ...

send_email("not-an-email")  # No validation
```

**Good:**
```python
class EmailAddress:
    def __init__(self, value):
        if "@" not in value:
            raise ValueError("Invalid email")
        self.value = value

def send_email(to: EmailAddress):
    ...
```

#### 4.7 Magic Numbers / Strings
Extract literals into named constants.

**Bad:**
```python
if retries > 3:
    sleep(86400)
```

**Good:**
```python
MAX_RETRIES = 3
SECONDS_PER_DAY = 86400

if retries > MAX_RETRIES:
    sleep(SECONDS_PER_DAY)
```

---

### 5. Error Handling

#### 5.1 Specific Exceptions
Catch specific exception types rather than generic `Exception`. Allows precise handling and prevents masking unexpected errors.

**Bad:**
```python
try:
    process()
except Exception:
    log("Something went wrong")
```

**Good:**
```python
try:
    process()
except ValidationError as e:
    return {"error": str(e)}
except DatabaseError:
    raise ServiceUnavailable()
```

#### 5.2 Never Catch and Ignore
Silent `except: pass` hides bugs. Always log, re-raise, or handle meaningfully.

**Bad:**
```python
try:
    send_email()
except:
    pass  # Email silently fails forever
```

**Good:**
```python
try:
    send_email()
except EmailError as e:
    logger.warning(f"Failed to send email: {e}")
    queue_for_retry()
```

#### 5.3 Context in Errors
Include relevant data in error messages.

**Bad:** `raise ValueError("Invalid input")`

**Good:** `raise ValueError(f"Invalid order ID: {order_id}. Expected format: ORD-XXXX")`

#### 5.4 Distinguish User vs System Errors
Handle user input validation separately from system failures. Different audiences need different messages.

**Bad:** Showing stack traces to end users.

**Good:** User-friendly messages for validation errors, detailed logs for system errors.

#### 5.5 Fail Safely
If an operation fails partially, don't leave the system in an inconsistent state. Use transactions or atomic operations.

**Bad:**
```python
def transfer(from_acct, to_acct, amount):
    from_acct.balance -= amount
    # If this fails, money disappears!
    to_acct.balance += amount
```

**Good:**
```python
def transfer(from_acct, to_acct, amount):
    with db.transaction():
        from_acct.balance -= amount
        to_acct.balance += amount
```

---

### 6. Comments & Documentation

#### 6.1 No Redundant Comments
Remove comments that repeat what code already says.

**Bad:**
```python
# Increment counter by one
counter += 1

# Loop through all users
for user in users:
```

**Good:**
```python
counter += 1

for user in users:
```

#### 6.2 Comments Explain Why, Not What
Good code is self-explanatory about "what." Comments should explain non-obvious "why" decisions or workarounds.

**Bad:**
```python
# Set timeout to 30
timeout = 30
```

**Good:**
```python
# 30s timeout required by payment gateway SLA
timeout = 30
```

#### 6.3 Outdated Comments
Comments that don't match the code are worse than no comments. They actively mislead.

**Bad:**
```python
# Returns user's full name
def get_user_email(user):
    return user.email
```

#### 6.4 TODO/FIXME Hygiene
TODOs without tickets or owners accumulate forever. Either fix them, create a ticket, or delete them.

**Bad:**
```python
# TODO: fix this later
# FIXME: doesn't work sometimes
# HACK: temporary workaround (added 3 years ago)
```

**Good:**
```python
# TODO(JIRA-1234): Migrate to new API before Q2 deprecation
```

---

### 7. Testing & Testability

#### 7.1 Testable Design
Design code with testing in mind. Avoid hard-coded dependencies, global state, and tight coupling that makes testing difficult.

**Bad:**
```python
def get_weather():
    return requests.get("https://api.weather.com/today").json()
```

**Good:**
```python
def get_weather(http_client):
    return http_client.get("https://api.weather.com/today").json()
```

#### 7.2 Test Behavior, Not Implementation
Test what code does, not how. Tests relying on implementation details break when refactoring.

**Bad:**
```python
def test_sort():
    sorter = Sorter()
    assert sorter._use_quicksort == True  # Testing private implementation
```

**Good:**
```python
def test_sort():
    assert sort([3, 1, 2]) == [1, 2, 3]  # Testing behavior
```

#### 7.3 Independent Tests
Tests shouldn't depend on execution order or shared state. Each test should run in isolation.

**Bad:**
```python
def test_create_user():
    create_user("alice")  # Creates state

def test_get_user():
    user = get_user("alice")  # Depends on previous test!
```

#### 7.4 Test Edge Cases
Don't test only the happy path. Include boundaries, empty inputs, null values, and error conditions.

---

### 8. Type Safety & Contracts

#### 8.1 Type Hints / Static Typing
Use type hints. They serve as documentation, catch errors at compile time, and enable better IDE support.

**Bad:**
```python
def process(data):
    return data.value * data.quantity
```

**Good:**
```python
def process(data: OrderItem) -> Decimal:
    return data.value * data.quantity
```

#### 8.2 Null Safety
Handle null/None explicitly. Use Optional types, null object pattern, or fail-fast validation.

**Bad:**
```python
def greet(user):
    return f"Hello, {user.name}"  # Crashes if user is None
```

**Good:**
```python
def greet(user: Optional[User]) -> str:
    if user is None:
        return "Hello, Guest"
    return f"Hello, {user.name}"
```

#### 8.3 Defensive Programming at Boundaries
Validate inputs at system boundaries (user input, external APIs). Trust internal code.

---

### 9. Immutability & State

#### 9.1 Immutability Where Possible
Prefer immutable objects and data structures. Reduces bugs from unexpected state changes and improves thread safety.

**Bad:**
```python
def add_discount(order):
    order.total *= 0.9  # Mutates input
    return order
```

**Good:**
```python
def add_discount(order):
    return Order(
        items=order.items,
        total=order.total * 0.9
    )
```

#### 9.2 Global State
Mutable global variables or singletons create hidden dependencies and make testing impossible. Use dependency injection instead.

**Bad:**
```python
config = {}  # Global mutable state

def get_setting(key):
    return config[key]
```

**Good:**
```python
class Settings:
    def __init__(self, config: dict):
        self._config = config.copy()  # Immutable copy
```

#### 9.3 Temporal Coupling
When methods must be called in a specific order, make this explicit in the API design or combine them.

**Bad:**
```python
processor.init()
processor.load()
processor.validate()  # Must call in this order!
processor.run()
```

**Good:**
```python
processor.run()  # Handles init, load, validate internally
# Or use builder pattern that enforces order
```

---

### 10. Interface Design

#### 10.1 Open/Closed Principle
Code should be open for extension but closed for modification. Add behavior through extension, not by changing existing code.

**Bad:**
```python
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14 * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height
    # Must modify this function for every new shape!
```

**Good:**
```python
class Shape(ABC):
    @abstractmethod
    def area(self): pass

class Circle(Shape):
    def area(self):
        return 3.14 * self.radius ** 2
```

#### 10.2 Liskov Substitution Principle
Derived classes must be substitutable for their base classes. Subclasses should extend, not modify, expected behavior.

**Bad:**
```python
class Bird:
    def fly(self): ...

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError()  # Violates LSP!
```

#### 10.3 Interface Segregation
Clients shouldn't depend on interfaces they don't use. Create specific, focused interfaces rather than monolithic ones.

**Bad:**
```python
class Worker(ABC):
    @abstractmethod
    def work(self): ...
    @abstractmethod
    def eat(self): ...
    @abstractmethod
    def sleep(self): ...

class Robot(Worker):
    def eat(self): pass  # Robots don't eat!
    def sleep(self): pass  # Robots don't sleep!
```

**Good:**
```python
class Workable(ABC):
    @abstractmethod
    def work(self): ...

class Feedable(ABC):
    @abstractmethod
    def eat(self): ...
```

#### 10.4 Dependency Inversion
High-level modules shouldn't depend on low-level modules. Both should depend on abstractions.

**Bad:**
```python
class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()  # Depends on concrete class
```

**Good:**
```python
class OrderService:
    def __init__(self, db: Database):  # Depends on abstraction
        self.db = db
```

#### 10.5 Law of Demeter
Only talk to your immediate friends. Don't chain through objects.

**Bad:**
```python
user.get_address().get_city().get_zipcode()
```

**Good:**
```python
user.get_zipcode()  # User handles the traversal internally
```

---

### 11. Performance & Optimization

#### 11.1 Premature Optimization
Write clear, simple code first. Optimize only where profiling shows actual bottlenecks.

**Bad:** Micro-optimizing code that runs once at startup.

**Good:** Profile first, then optimize the 5% of code that takes 95% of time.

#### 11.2 N+1 Queries
Detect database queries in loops. Batch them or use eager loading instead.

**Bad:**
```python
for user in users:
    orders = db.query(f"SELECT * FROM orders WHERE user_id = {user.id}")
```

**Good:**
```python
user_ids = [u.id for u in users]
orders = db.query(f"SELECT * FROM orders WHERE user_id IN ({user_ids})")
```

#### 11.3 Unnecessary Computation
Don't compute values that are never used. Apply lazy evaluation or remove dead calculations.

**Bad:**
```python
def get_report(include_stats=False):
    data = fetch_data()
    stats = expensive_stats_calculation(data)  # Always computed
    if include_stats:
        return {"data": data, "stats": stats}
    return {"data": data}
```

**Good:**
```python
def get_report(include_stats=False):
    data = fetch_data()
    result = {"data": data}
    if include_stats:
        result["stats"] = expensive_stats_calculation(data)
    return result
```

---

### 12. Modern Practices

#### 12.1 Incremental Refactoring
Refactor continuously in small increments alongside feature work. Avoid large risky rewrites.

#### 12.2 Automated Formatting
Use formatters (Black, Prettier, gofmt) to eliminate style debates and ensure consistency without manual effort.

#### 12.3 Configuration Over Hardcoding
Use environment variables or config files, not hardcoded values. Enables deployment across environments.

**Bad:**
```python
API_URL = "https://api.production.com"
```

**Good:**
```python
API_URL = os.environ.get("API_URL")
```

#### 12.4 Backward Compatibility Awareness
Breaking changes require migration paths. Be intentional about API changes.

---

## Reporting Format

When reporting issues, use this format:

```
## [filename]

### [Principle Name] (Category)
**Line [N]:** [Description of the issue]

**Current:**
[code snippet]

**Suggested:**
[improved code snippet]
```
