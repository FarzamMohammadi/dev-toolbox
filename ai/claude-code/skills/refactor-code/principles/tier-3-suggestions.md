# Tier 3: Suggestions

Nice-to-have improvements. Mention but don't emphasize.

---

## Naming

### 3.8 No Noise Words
Remove redundant suffixes that add no information.

**Verbose:** `UserObject`, `CustomerData`, `AccountInfo`, `OrderDetails`
**Clean:** `User`, `Customer`, `Account`, `Order`

---

## Structure

### 1.4 Composition Over Inheritance
Favor composing objects over deep inheritance hierarchies.

### 1.8 Feature Envy
When a method uses mostly another class's data, consider moving it there.

### 1.11 Layered Architecture
Higher layers depend on lower layers only: Controller → Service → Repository

### 1.12 Package by Feature
Group code by domain/feature, not by technical layer.

**Layer-based:**
```
controllers/user_controller.py
services/user_service.py
```

**Feature-based (preferred):**
```
users/controller.py
users/service.py
```

---

## Function Design

### 2.4 Flag Parameters
Boolean flags change behavior = consider separate functions.

**With flag:** `get_users(include_deleted=False)`
**Separate:** `get_active_users()` and `get_all_users()`

### 2.8 Output Parameters
Return values instead of mutating passed-in parameters.

---

## Code Simplification

### 4.3 YAGNI
Don't build features "just in case." Build when needed.

### 4.4 Speculative Generality
Remove complex abstractions built for hypothetical future use.

### 4.5 Dead Code
Delete unreachable/unused code. Version control has history.

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

---

## Comments

### 6.1 No Redundant Comments
Don't repeat what code already says.

**Redundant:** `# Loop through users` before `for user in users:`
**Useful:** (none needed - code is clear)

### 6.4 TODO Hygiene
TODOs without tickets accumulate forever.

**Bad:** `# TODO: fix this later`
**Good:** `# TODO(JIRA-1234): Migrate to new API before Q2`

---

## Interface Design

### 10.1 Open/Closed Principle
Open for extension, closed for modification.

### 10.2 Liskov Substitution
Derived classes must be substitutable for base classes.

### 10.3 Interface Segregation
Don't force clients to depend on methods they don't use.

### 10.4 Dependency Inversion
Depend on abstractions, not concrete implementations.

### 10.5 Law of Demeter
Only talk to immediate friends. Avoid `a.b.c.d()` chains.

**Bad:** `user.get_address().get_city().get_zipcode()`
**Good:** `user.get_zipcode()`

---

## Immutability

### 9.1 Prefer Immutable
When possible, create new objects instead of mutating.

### 9.3 Temporal Coupling
When methods must be called in order, make it explicit or combine them.

---

## Performance

### 11.1 Premature Optimization
Profile first. Optimize only proven bottlenecks.

### 11.2 N+1 Queries
Detect database queries in loops. Batch them.

### 11.3 Unnecessary Computation
Don't compute values that are never used.
