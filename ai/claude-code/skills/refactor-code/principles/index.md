# Refactoring Principles Index

Principles are organized by enforcement tier. **Philosophies always override principles.**

## Override Rule

> Any principle suggestion that conflicts with a Philosophy is automatically invalid.
> Philosophies are the user's core beliefs; principles are supporting guidelines.
> See [philosophy-enforcement.md](../decision-logic/philosophy-enforcement.md) for decision logic.

## Tier System

| Tier | Enforcement | When to Use | Count |
|------|-------------|-------------|-------|
| **1 - Blocking** | Must fix | Issues that significantly harm code quality | 8 |
| **2 - Important** | Should fix | Issues worth addressing in the review | 15 |
| **3 - Suggestions** | Nice to have | Minor improvements, style preferences | ~12 |

## Quick Reference by Category

### Naming & Readability
| ID | Principle | Tier | One-liner |
|----|-----------|------|-----------|
| 3.1 | Intent-revealing names | 1 | Names eliminate need for explanation |
| 3.9 | Semantic specificity | 1 | `validate()` → `validate_user_input()` |
| 3.5 | No misleading names | 1 | Behavior must match name |
| 3.2 | Avoid abbreviations | 2 | Spell out unless universal |
| 3.3 | Searchable names | 2 | No single letters (except loop `i`) |
| 3.4 | Domain consistency | 2 | One term per concept |
| 3.6 | Boolean naming | 2 | `is_`, `has_`, `can_` prefixes |
| 3.7 | Class/method naming | 2 | Nouns for classes, verbs for methods |
| 3.8 | No noise words | 3 | Remove `Info`, `Data`, `Object` suffixes |

### Structural / Architectural
| ID | Principle | Tier | One-liner |
|----|-----------|------|-----------|
| 1.1 | Single Responsibility | 1 | One reason to change per class |
| 1.7 | Separation of Concerns | 1 | Data, logic, presentation separated |
| 1.2 | High Cohesion | 2 | Related functionality together |
| 1.3 | Low Coupling | 2 | Minimize dependencies |
| 1.4 | Composition over Inheritance | 2 | Favor composition |
| 1.5 | Dependency Injection | 2 | Pass dependencies in |
| 1.6 | Single Level of Abstraction | 2 | Don't mix high/low level |
| 1.8 | Feature Envy | 3 | Move method to class it envies |
| 1.9 | Large Class / God Object | 2 | Split if can't describe in one sentence |
| 1.10 | Circular Dependencies | 2 | Break cycles |
| 1.11 | Layered Architecture | 3 | Layers depend only on lower layers |
| 1.12 | Package by Feature | 3 | Group by domain, not layer |

### Function / Method Design
| ID | Principle | Tier | One-liner |
|----|-----------|------|-----------|
| 2.1 | Do One Thing | 2 | Split if description uses "and" |
| 2.2 | Function Length | 2 | Under 30 lines preferred |
| 2.3 | Long Parameter List | 2 | Max 4 params, group into objects |
| 2.4 | Flag Parameters | 3 | Replace boolean flags with separate functions |
| 2.5 | Deep Nesting | 2 | Max 3 levels, use early returns |
| 2.6 | Early Return Pattern | 2 | Guard clauses first |
| 2.7 | No Side Effects | 2 | Name should indicate mutation |
| 2.8 | Output Parameters | 3 | Return values, don't mutate params |
| 2.9 | Fail Fast | 1 | Validate at start |

### Error Handling
| ID | Principle | Tier | One-liner |
|----|-----------|------|-----------|
| 5.1 | Specific Exceptions | 1 | Catch specific types, not `Exception` |
| 5.2 | Never Catch and Ignore | 1 | No `except: pass` |
| 5.3 | Context in Errors | 2 | Include relevant data in messages |
| 5.4 | User vs System Errors | 2 | Different handling for each |
| 5.5 | Fail Safely | 2 | Use transactions for partial failures |

### Code Duplication & Simplification
| ID | Principle | Tier | One-liner |
|----|-----------|------|-----------|
| 4.1 | DRY | 2 | Logic in one place only |
| 4.2 | KISS | 2 | Simplest solution that works |
| 4.3 | YAGNI | 3 | Don't build for "just in case" |
| 4.4 | Speculative Generality | 3 | Remove unused abstractions |
| 4.5 | Dead Code | 3 | Delete, don't comment out |
| 4.6 | Primitive Obsession | 2 | Create value objects |
| 4.7 | Magic Numbers | 2 | Extract to named constants |

### Comments & Documentation
| ID | Principle | Tier | One-liner |
|----|-----------|------|-----------|
| 6.1 | No Redundant Comments | 3 | Don't repeat what code says |
| 6.2 | Comments Explain Why | 2 | Why (business), never what |
| 6.3 | Outdated Comments | 2 | Update or delete stale comments |
| 6.4 | TODO Hygiene | 3 | Link to ticket or delete |

### Type Safety & Contracts
| ID | Principle | Tier | One-liner |
|----|-----------|------|-----------|
| 8.1 | Type Hints | 2 | Use type annotations |
| 8.2 | Null Safety | 2 | Handle None explicitly |
| 8.3 | Defensive at Boundaries | 2 | Validate external inputs |

### Other
| ID | Principle | Tier | One-liner |
|----|-----------|------|-----------|
| 9.1 | Immutability | 3 | Prefer immutable where possible |
| 9.2 | Global State | 2 | Avoid mutable globals |
| 10.1-10.5 | Interface Design (SOLID) | 2-3 | Open/Closed, LSP, ISP, DIP, Demeter |
| 11.1-11.3 | Performance | 3 | Profile first, then optimize |

## Detailed Principles by Tier

- [Tier 1 - Blocking](tier-1-blocking.md) - Must fix before approval
- [Tier 2 - Important](tier-2-important.md) - Should fix, prominently flagged
- [Tier 3 - Suggestions](tier-3-suggestions.md) - Nice to have
