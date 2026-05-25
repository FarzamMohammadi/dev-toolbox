# Python Coding Standards

These standards govern Python code. Every contributor — human or agent — must adhere to them. No exceptions without justification.

A formatter and linter (Ruff, Black, mypy, pyright) automate what they can: formatting, import ordering, lint rules, type checking. Run the project's lint and type-check commands after every change. These standards cover everything tooling cannot enforce — structure, naming intent, function design, type discipline, and the philosophical foundations behind every decision.

> **Apply with judgment, never mechanically.** No rule justifies code that reads badly. When a rule and clarity collide, the application is wrong, not the rule. Find what an experienced engineer would naturally write that still honors the intent.

> **Respect existing patterns first.** Before applying these standards to an existing codebase, read enough of it to learn the patterns already in place. Propagate the *good* patterns that exist — the deliberate ones that aid readability, maintainability, and evolution. Replace the accidental or harmful ones with what's here. Never propagate garbage just because it exists; never overwrite deliberate choices just because the standard says otherwise. Judgment first.

> **Target Python 3.11+.** Standards assume modern Python: PEP 604 union syntax (`str | None`), `match` statements, `Self` type, `tomllib`, `ExceptionGroup`. If your project targets an older version, adapt accordingly — but prefer upgrading the project.

---

## 1. File Structure & Vertical Ordering

**Newspaper order.** A module reads top-to-bottom like a newspaper article: imports, then public API (classes, public functions), then private helpers (prefixed `_`) at the bottom. Caller above callee. High-level above low-level.

Python module layout:

```python
"""One-line module purpose. Optional second paragraph for context."""

from __future__ import annotations  # if needed for forward refs

import std_lib
import third_party
from local_package import thing

# Public API first
def schedule_task(input: CreateTaskInput, queue: PriorityQueue) -> ScheduledTask:
    decision = _decide_priority(input)
    return queue.enqueue(decision, input)

# Private helpers below
def _decide_priority(input: CreateTaskInput) -> Priority:
    ...
```

**Section dividers** (`# ── Name ──────────`) are used sparingly — only when a module has 3+ distinct logical sections. They are navigation landmarks, not documentation.

**File length:** Cohesion matters more than line count. A 400-line file with one cohesive concept is better than 4 fragmented files. 500+ lines is a smell worth examining — probably mixed concerns — but not a rule.

**`__all__` for public API.** Top-level modules define `__all__` to make the public surface explicit. Internal names stay out.

---

## 2. Naming

### Files & Directories

- **Modules:** `snake_case.py`
- **Packages:** `snake_case/`

### Variables & Functions

- **Functions, methods, variables:** `snake_case`
- **Classes:** `PascalCase`
- **Type aliases, `TypeVar`, `NewType`:** `PascalCase`
- **Constants (module-level):** `UPPER_SNAKE_CASE`
- **Enum members:** `UPPER_SNAKE_CASE` (PEP 8) or `PascalCase` for `StrEnum` value-like members — be consistent within the project
- **Private (convention):** `_leading_underscore`
- **Name-mangled (rare, only when needed):** `__double_underscore`
- **Dunder (reserved):** `__init__`, `__enter__`, etc. — never invent your own

### Schema Fields, Config, Database

- **Pydantic model fields:** `snake_case`
- **Config YAML/TOML keys:** `snake_case`
- **Database columns:** `snake_case`

### Rules

- **Full names, no abbreviations.** `communication_adapter` not `comm_adapter`. `requirements_gathering` not `req_gathering`.
- **Acronyms lowercase in snake_case, capitalized in PascalCase as a word.** `LlmAdapter`, `load_http_url`, `parse_json_body` — not `LLMAdapter`, `load_HTTP_url`.
- **Boolean prefixes preferred.** Use `is_`, `has_`, `can_`, `should_`, `was_`, `will_` when the bare word is ambiguous. `is_active`, `has_children`, `should_retry`. Exception: obvious adjectives that can only be boolean — `enabled`, `blocked`, `active`.
- **No vague -ER suffixes.** `TaskManager` (manages how?) and `DataProcessor` (processes into what?) are banned. `ConfigLoader` and `EventHandler` are fine when precise.
- **No `utils`, `helpers`, `misc`, `common`.** These are junk drawers. Move functions to the concept they belong to.
- **Domain language.** Names mirror the business domain (Ubiquitous Language). `TaskEngine`, `PipelineStage`, `TriggerEvent` — not `ItemProcessor`, `StepExecutor`, `IncomingData`.

---

## 3. Function Design

### Length

Ousterhout pragmatic: a function can be a few dozen lines if it does one cohesive thing clearly. Don't split for the sake of splitting — splitting multiplies interfaces and forces readers to bounce between functions. The test: can you name it well? Can you follow it without scrolling? Then it's fine.

### Parameters

2-3 positional parameters is ideal. Beyond that, use keyword-only arguments via `*,`. Keyword arguments are self-documenting, order-independent, and extensible without breaking callers.

```python
# Good — positional for the few, keyword-only for the rest
def schedule_task(
    task: Task,
    queue: PriorityQueue,
    *,
    priority: Priority = Priority.NORMAL,
    deadline: datetime | None = None,
    tags: list[str] | None = None,
) -> ScheduledTask:
    ...
```

### No Mutable Default Arguments

Default arguments are evaluated once at function definition, not per call. Mutable defaults are shared state across every call — a classic source of bugs.

```python
# Bad — `tags` is the *same list* across all calls
def add_task(name: str, tags: list[str] = []) -> Task: ...

# Good — sentinel pattern
def add_task(name: str, tags: list[str] | None = None) -> Task:
    tags = tags if tags is not None else []
    ...
```

### Guard Clauses

Always. Validate and bail at the top. The happy path reads flat at the lowest indentation level. No arrow code (deeply nested conditionals).

```python
def process_task(task: Task, config: Config) -> ProcessResult:
    if not task.is_ready:
        return ProcessResult(skipped=True, reason="not ready")
    if task.attempts >= config.max_retries:
        return ProcessResult(skipped=True, reason="max retries")

    # Happy path — flat, clear, no nesting
    result = execute_pipeline(task, config)
    return ProcessResult(skipped=False, result=result)
```

### Functional Core, Imperative Shell (FCIS)

Strict separation. If a function makes a **decision**, it must be pure — take data in, return data out, no side effects. If a function **performs effects** (I/O, database, network), it should contain minimal logic — just route the decision into the world.

```python
# PURE — decision logic, trivially testable
def decide_next_phase(task: Task, config: PipelineConfig) -> PhaseDecision:
    ...

# SHELL — performs effects, minimal logic
async def advance_task(task_id: TaskId, db: Database, event_bus: EventBus) -> None:
    task = await db.get_task(task_id)
    decision = decide_next_phase(task, await db.get_pipeline_config())
    if decision.next != task.phase:
        await db.update_phase(task_id, decision.next)
        await event_bus.publish("task.phase_changed", {"task_id": task_id, "phase": decision.next})
```

### `match` for State Machines and Dispatch

Use `match` when you're dispatching on the *shape* or *kind* of a value — state transitions, message handlers, AST walks. For simple equality checks an `if`/`elif` chain is fine; `match` earns its weight when patterns destructure or you need exhaustiveness.

```python
def transition(state: State, event: Event) -> State:
    match (state, event):
        case (Pending(), Start()):
            return Running(started_at=event.at)
        case (Running(), Complete(result=r)):
            return Done(result=r)
        case (Running(), Cancel()):
            return Cancelled()
        case (Done() | Cancelled(), _):
            raise InvariantError(f"No transitions from terminal state {type(state).__name__}")
        case _:
            assert_never((state, event))
```

`assert_never` in the wildcard arm makes the state/event table a compile-time contract — adding a new state or event forces every transition table to be updated.

### Context Managers for Resources

Anything that holds a resource — files, sockets, DB connections, locks, temp directories — uses `with` (sync) or `async with` (async). Never call `.close()` manually in code that could raise.

```python
# Good
with open(path) as f:
    data = f.read()

async with db.transaction() as tx:
    await tx.execute(...)

# Bad — leaks on exception
f = open(path)
data = f.read()
f.close()
```

If a class manages a resource, implement `__enter__`/`__exit__` (or `__aenter__`/`__aexit__`) — don't expose `.open()` and `.close()` for callers to remember.

---

## 4. Type System & Schemas

### `Any` Is Banned

Never use `typing.Any`. It silently disables type checking at every point it touches. The escape hatches, in order of preference:

1. **The actual type.** If you know the shape, declare it.
2. **`object`** when you truly accept anything but won't do anything with it beyond passing it through.
3. **A `TypeVar`** when the caller knows the type and you're just passing it through generically.
4. **A `Protocol`** when you need structural typing — the value must have method X but the concrete class doesn't matter.
5. **A precise union** (`str | int | None`) when the value really can be one of a few things.

`# type: ignore` is similarly banned without a written reason on the same line. `# type: ignore[error-code]  # mypy false positive on Self in mixin` is acceptable. Bare `# type: ignore` is not.

### Type Hints Everywhere

Every function gets parameter types and a return type. Every method. No exceptions for `__init__` (return `None`), private helpers, or "simple" functions. Types are contracts and intent — the reader should never have to guess.

```python
# Good
def build_priority_queue(config: SchedulerConfig) -> PriorityQueue:
    ...

# Bad — no types
def build_priority_queue(config):
    ...
```

Run `mypy --strict` or `pyright` in strict mode. Loosening either is a project-wide decision, not a per-file one.

### Protocols for Structural Typing

Use `Protocol` (PEP 544) for interface-like contracts. Duck typing with compiler help — the implementor doesn't need to inherit anything.

```python
from typing import Protocol

class TriggerSource(Protocol):
    async def poll(self) -> list[TriggerEvent]: ...
    async def health_check(self) -> HealthStatus: ...

# Any class with those methods satisfies TriggerSource — no inheritance needed
```

Reserve abstract base classes (`abc.ABC`) for shared *implementation*, not for pure contracts.

### Generics

On Python 3.12+, **PEP 695 generic syntax is the default.** Reach for legacy `TypeVar` only when the project must support 3.11.

```python
# Good — 3.12+ default
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

class Repository[T]:
    def get(self, id: str) -> T | None: ...

# Fallback — pre-3.12 compatibility only
from typing import TypeVar
T = TypeVar("T")
def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

Type-parameter names are `PascalCase` and short for simple cases (`T`, `K`, `V`). Use descriptive names (`TInput`, `TOutput`) when there are multiple parameters.

### Exhaustiveness with `assert_never`

Pair every discriminated union, enum, or `match` with `typing.assert_never` so adding a new variant becomes a *type-check* error everywhere it must be handled. This is the highest-leverage type-system pattern for evolvability — the checker points you at every site that needs updating when the union grows.

```python
from typing import assert_never

def handle_event(event: TaskCreated | TaskUpdated | TaskDeleted) -> None:
    match event:
        case TaskCreated():
            handle_created(event)
        case TaskUpdated():
            handle_updated(event)
        case TaskDeleted():
            handle_deleted(event)
        case _:
            assert_never(event)  # type error if a new variant is added
```

### `@override` for Inheritance Contracts (3.12+)

Mark every method that overrides a base-class method with `@typing.override`. If the parent renames or removes the method, the child errors at type-check time instead of silently decoupling.

```python
from typing import override

class JsonAdapter(Adapter):
    @override
    def serialize(self, value: object) -> bytes: ...
```

Enable the strict-checker setting (`reportImplicitOverride = "error"` in pyright, similar in mypy) so missing `@override` is itself a type error in projects on 3.12+.

### `Self` for Fluent Builders and Factory Methods

Use `typing.Self` (3.11+) for any method that returns "an instance of whatever class this is" — factory classmethods and fluent builders. Subclasses get the correct return type for free.

```python
from typing import Self

@dataclass(frozen=True)
class Task:
    id: TaskId
    priority: Priority

    def with_priority(self, priority: Priority) -> Self:
        return dataclasses.replace(self, priority=priority)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        return cls(...)
```

### `TypeIs` over `TypeGuard` (3.13+)

For runtime narrowing, prefer `typing.TypeIs` over `TypeGuard`. `TypeIs` narrows in *both* branches (positive and negative); `TypeGuard` only narrows the positive branch — which is rarely what you want.

```python
from typing import TypeIs

def is_task(value: object) -> TypeIs[Task]:
    return isinstance(value, Task)
```

### Decorators: `ParamSpec` and `functools.wraps`

Decorators that don't preserve the wrapped signature are bug factories — autocomplete dies, type checkers shrug. Always use `ParamSpec` for generic decorators, and always wrap with `functools.wraps`.

```python
from collections.abc import Callable
from functools import wraps
import logging

def timed[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.monotonic()
        try:
            return fn(*args, **kwargs)
        finally:
            logging.info("Call timed", extra={"fn": fn.__name__, "duration_ms": (time.monotonic() - start) * 1000})
    return wrapper
```

### Branded / Newtypes

Use `NewType` for domain IDs to prevent mixing them up.

```python
from typing import NewType

TaskId = NewType("TaskId", str)
SessionId = NewType("SessionId", str)

def get_task(task_id: TaskId) -> Task: ...

# Compiler catches this:
session = SessionId("abc")
get_task(session)  # type error
```

### Schema-First (Pydantic v2)

For data crossing system boundaries (API requests, config files, external API responses), define a Pydantic v2 model. The model is both validator and type — single source of truth.

```python
from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints

# Reusable constrained types — define once, compose everywhere
PositiveInt = Annotated[int, Field(gt=0)]
TaskName = Annotated[str, StringConstraints(min_length=1, max_length=80)]

class SafetyConfig(BaseModel):
    max_retries: PositiveInt = 3
    cost_limit_usd: Annotated[float, Field(gt=0)] = 5.0
    model_config = {"frozen": True}  # immutable
```

Prefer `Annotated[T, ...]` over keeping constraints on `Field(...)` defaults — the constraint travels with the type, is reusable across models, and replaces scattered `@field_validator` boilerplate.

### Internal Data: dataclass vs attrs vs Pydantic

Picking the right tool for internal types is a frequent source of confusion. The rule:

- **Pydantic** — anything crossing a boundary (parse, validate, serialize). Pays for itself with validation and schema generation.
- **`@dataclass(frozen=True, slots=True)`** — internal immutable values, zero deps preferred, no validation needed. The default for internal types.
- **attrs** — internal values that need validators, converters, or `__slots__` features that dataclasses lack; or projects on Python < 3.10 where dataclass ergonomics are weaker.
- **`TypedDict`** — when you're handed a `dict` shape from an untyped source and only need a typed view, not a class.

Pick one tool for internal data and one for boundary data per project — and stay consistent. Mixing freely creates cognitive overhead with no payoff.

### Immutability by Default

Treat mutability as the exception that requires justification.

- **Frozen dataclasses for internal data.** `@dataclass(frozen=True, slots=True)` — prevents accidental mutation, enables hashing, lighter memory footprint.
- **Frozen Pydantic models for parsed inputs.** `model_config = {"frozen": True}`.
- **Tuples over lists for fixed collections.** When the collection won't grow, tuples are immutable and signal that.
- **`Final` for module constants.** `MAX_RETRIES: Final[int] = 3` tells readers and the type checker this won't be reassigned.
- **Never mutate function parameters.** If a function needs a modified version of its input, create a new object — `dataclasses.replace(obj, field=new_value)` for dataclasses, `model.model_copy(update={...})` for Pydantic.

```python
@dataclass(frozen=True, slots=True)
class TaskSnapshot:
    id: TaskId
    state: TaskState
    phase: Phase

def with_updated_phase(task: TaskSnapshot, phase: Phase) -> TaskSnapshot:
    return dataclasses.replace(task, phase=phase)
```

### Parse, Don't Validate

At system boundaries (user input, config files, API responses, third-party returns), parse raw data into typed values. After the boundary, trust the types — no defensive checks deep in the codebase.

```python
# Boundary — parse raw input into a typed, validated value
def parse_task_input(raw: dict[str, object]) -> CreateTaskInput:
    return CreateTaskInput.model_validate(raw)

# Interior — receives CreateTaskInput, trusts the type, no re-validation
def schedule_task(input: CreateTaskInput, queue: PriorityQueue) -> ScheduledTask:
    return queue.enqueue(input.priority, input)
```

### Strict Type Checker Settings

`pyproject.toml` should enable strict mode for mypy or pyright. For mypy: `strict = true`, `disallow_any_explicit = true`, `disallow_any_generics = true`, `warn_unused_ignores = true`. For pyright: `typeCheckingMode = "strict"`. Loosening any of these is project-wide.

---

## 5. Error Handling

### Exceptions Are Python's Idiom

Python doesn't have native Result/Either types — exceptions are the language's chosen mechanism for both expected and unexpected failures. The discipline lies in:

1. **A clear domain exception hierarchy** that signals to the caller what kind of failure happened.
2. **Catching only what you can meaningfully handle** — never blanket `except Exception:`.
3. **Preserving the cause chain** with `raise X from e`.

### Domain Exception Hierarchy

Every module exports a base exception that all module-specific exceptions inherit from. Callers can catch the base when they want everything from that module; they can catch a specific subclass when they want to handle a particular case.

```python
class TaskEngineError(Exception):
    """Base for all task-engine errors."""
    retryable: bool = False

class TaskNotFoundError(TaskEngineError):
    """Task does not exist."""
    retryable = False  # permanent — retrying won't help

class WorkspaceNotReadyError(TaskEngineError):
    """Workspace is being provisioned."""
    retryable = True  # transient — workspace may become ready
```

The `retryable` attribute drives behavior at the boundary: retryable errors get backoff and retry. Permanent errors get logged, reported, and the task moves to a failed state. No guessing.

### Expected vs Unexpected

Pythonic style throws exceptions for both, but the *type* of exception communicates the difference:

- **Expected failures** (validation, not-found, rate-limited): a domain exception the caller is expected to handle. Documented in the docstring's `Raises:` section.
- **Unexpected failures** (invariant violations, bugs, unreachable states): generic `AssertionError`, `RuntimeError`, or a custom `InvariantError`. The caller should *not* catch these — they signal bugs.

```python
def get_active_session(task: Task) -> Session:
    if task.session_id is None:
        raise InvariantError("Task in active state must have a session")
    return sessions[task.session_id]
```

### Error Messages

Uppercase first letter, no trailing period, active voice, quote string values.

```python
# Good
raise NotFoundError(f'Cannot find task "{task_id}"')
raise ValidationError(f'Expected positive integer, got "{value}"')

# Bad
raise Exception("task not found.")
raise Exception(f"invalid value: {value}")
```

### Where to Catch

Let exceptions bubble unless you can meaningfully handle them (retry, fallback, translate for a different boundary). Never catch just to log and re-raise. Boundary layers (CLI handlers, request handlers, top-level orchestration loops) are the natural catch-all points.

**Never use bare `except:` or `except Exception:` without a specific reason.** Bare except catches `KeyboardInterrupt` and `SystemExit` — almost always wrong. `except Exception:` is acceptable only at the outermost boundary, and only with a comment explaining why.

### Propagation Through Layered Boundaries

Errors travel outward through architectural layers. Each layer translates for its consumer — never swallows, never exposes internals upward.

```python
# Inner boundary — translate, preserve cause via `from`
try:
    return await self.client.fetch(url)
except httpx.HTTPError as e:
    raise AdapterError(f'Fetch failed for "{url}"') from e
```

### Cause Chains with `raise ... from`

Always preserve the original exception with `from`. Never just stringify the message — the traceback, `__cause__` chain, and exception class are all diagnostic information.

```python
# Good — cause chain preserved
try:
    result = phase.execute()
except PhaseError as e:
    raise OrchestratorError(f'Phase "{phase.name}" failed for task "{task_id}"') from e

# Bad — original exception discarded, traceback lost
try:
    result = phase.execute()
except PhaseError as e:
    raise OrchestratorError(f"Phase failed: {e}")
```

Use `raise X from None` only to explicitly suppress the cause when re-raising would expose an irrelevant internal traceback.

### ExceptionGroup (3.11+)

When parallel work fails in multiple places at once (e.g., `asyncio.gather` with `return_exceptions=True` then filtering), use `ExceptionGroup` and `except*` syntax instead of swallowing or arbitrarily picking one exception.

---

## 6. Imports & Dependencies

### Import Order

Automated by the formatter (Ruff's `I` rules, isort). The conventional grouping:

1. Future imports (`from __future__ import annotations`)
2. Standard library
3. Third-party packages
4. Local package (absolute imports)

Blank line between groups. No manual ordering — let the tool handle it.

### No Wildcard Imports

`from module import *` pollutes the namespace and breaks tooling. Always import what you need explicitly.

```python
# Good
from collections.abc import Iterable, Mapping

# Bad
from collections.abc import *
```

The one exception: `from __future__ import annotations` is not a wildcard despite the syntax.

### Absolute Imports Preferred

Use absolute imports (`from package.module import thing`) over relative (`from .module import thing`). Absolute imports survive file moves better and are unambiguous when reading.

Relative imports are tolerable within a tightly-coupled subpackage where the relationship is intentional.

### Explicit Public API via `__init__.py`

A package's `__init__.py` defines its public surface. Internal modules import directly from each other — never through their own package's `__init__.py`.

```python
# Consumer (outside the package):
from task_engine import TaskEngine

# Internal (within the package):
from task_engine.state_machine import StateMachine  # Direct, not through __init__
```

### No Re-Imports That Just Forward

If `package/__init__.py` re-exports `StateMachine` and you do `from package.state_machine import StateMachine` *inside* the package, you've created an import cycle risk. Internal code uses the direct path.

---

## 7. Module Boundaries

A well-bounded module is one where a contributor can load its full context, understand it, modify it, and verify the change without needing to understand anything beyond its contract with the outside world. That is the test of modularity. If working on a module requires reading three other modules to form a mental model, the boundaries are wrong.

### One Concept per Module

A "concept" may include a class + its factory + its validators — as long as they form one cohesive unit that you can name with a single word. The test: can you name the module file after the concept without it feeling forced?

### When to Split

Split when parts of a file change for different reasons (Common Closure Principle). Line count is a smell that triggers this check, not a rule in itself.

### Directory Structure

Hybrid: domain-first at the top level, technical organization within.

```
src/
  core/
    task_engine/         ← domain concept (package)
      __init__.py        ← public API
      state_machine.py   ← internal
      queries.py         ← internal
      errors.py          ← internal
  adapters/              ← architectural layer
  plugins/               ← architectural layer
  schemas/               ← shared pydantic models
```

### Structure Reveals Intent

A new contributor should understand what a directory contains and how its files relate — without opening any of them. Directory grouping and module names are the first layer of documentation.

- **Group by cohesion.** Modules that change together, deploy together, or serve the same command/feature live in the same package.
- **Eliminate redundant prefixes.** When modules move into a named package, drop the prefix that the package already provides. `start_background.py` becomes `background.py` inside `commands/start/`.
- **Flat is fine when names are sufficient.** Not every pair of related modules needs a subpackage.

### Test Location

Tests live in a separate `tests/` directory mirroring `src/`. Fixtures colocate with their test files or live in `conftest.py`.

```
src/core/task_engine/__init__.py
tests/core/task_engine/test_engine.py
tests/core/task_engine/conftest.py
```

---

## 8. Comments & Documentation

### Philosophy

Minimal. A comment earns its place only when the code cannot express the WHY — hidden constraints, non-obvious workarounds, "we tried X and it broke because Y."

### Docstrings

Every exported function, class, and method gets a docstring. One-line for simple cases. Multi-section (Google or NumPy style) when the signature deserves explanation.

```python
def poll(self) -> list[TriggerEvent]:
    """Poll for new trigger events from the external source."""
    ...

def schedule_task(input: CreateTaskInput, queue: PriorityQueue) -> ScheduledTask:
    """Enqueue a task at the priority derived from its input.

    Raises:
        QueueFullError: When the queue is at capacity.
    """
    ...
```

Pick one docstring style (Google, NumPy, or Sphinx) per project and stick with it. Ruff's `D` rules enforce.

Private helpers (`_leading_underscore`) get a docstring only if the why isn't obvious from the name.

### Section Dividers

Navigation landmarks only. Just the section name, no explanation.

```python
# ── Event Declarations ──────────────────────────────────────────────────────
```

### TODOs

Allowed. Must include author and context.

```python
# TODO(farzam): Handle unicode edge case in Korean input
```

---

## 9. Testing

### Framework

Pytest. No `unittest.TestCase` boilerplate — pytest's plain-function style is cleaner and composes better with fixtures.

### Structure

Group related tests in a class (`class TestTaskEngine:`) for context, not for inheritance. Pytest treats classes as namespaces. Maximum 2 levels of grouping (class + nested class) — beyond that the structure isn't helping.

```python
class TestTaskEngine:
    class TestRequestTransition:
        def test_advances_to_next_state_when_transition_is_valid(self): ...
        def test_rejects_transition_when_task_is_blocked(self): ...
```

### Naming

Behavior-as-fact. No "should." Describe what the system does, not what it "should" do.

```python
# Good
def test_rejects_transition_when_task_is_blocked(): ...
def test_emits_task_created_event_with_payload(): ...

# Bad
def test_should_reject_the_transition(): ...
def test_should_emit_an_event(): ...
```

### Fixtures

Use pytest fixtures for setup. Module-level for expensive resources (`scope="module"`). Function-level by default. Put shared fixtures in `conftest.py`.

### Parametrize Over Loops

Use `@pytest.mark.parametrize` for table-driven tests. Each case becomes a separate test in the report — easier to diagnose than a loop that fails on iteration 7.

```python
@pytest.mark.parametrize("input,expected", [
    ("pending", True),
    ("active", True),
    ("blocked", False),
])
def test_can_transition_returns_correct_value_for_state(input, expected):
    assert can_transition(State(input)) == expected
```

### Mocking

Mock only at system boundaries — network, filesystem, time, external services. Pure functions need no mocks (test with data). Never mock internal modules of your own code.

Prefer `unittest.mock` or `pytest-mock`'s `mocker` fixture. For HTTP, prefer `respx` (httpx) or `responses` (requests) — they intercept at the network layer, not by patching internal functions.

### What Not to Test

- Trivial getters, simple delegation, dataclass `__init__`
- Anything the type checker already guarantees
- Third-party library behavior (test your usage, not their internals)

---

## 10. Code Layout & Formatting

### Automated by Tooling

Ruff (formatter + linter) and mypy/pyright handle formatting (88 or 120 char lines — pick one per project), import ordering, lint rules, and type checking. Run `ruff format && ruff check && mypy .` after every change. The standards below cover what tooling cannot automate.

### Visual Principles

- **Blank lines separate concepts.** Two blank lines between top-level functions and classes (PEP 8). One blank line between methods. One blank line between logical groups within a function.
- **Density within related code.** Related declarations stay packed.
- **Guard clauses at top.** Happy path reads flat.
- **Early returns** over nested `else` branches.
- **No arrow code.** If indentation exceeds 3 levels, refactor.
- **f-strings only.** `f"{name}: {value}"` — never `%` or `.format()`.

---

## 11. Single Source of Truth

Define every value once. Derive everywhere else. A constant that appears in two places will eventually disagree — every duplicate is a future bug.

- **Versions and metadata.** Read the version from `pyproject.toml` at runtime via `importlib.metadata.version("your_package")` — no hardcoded `__version__` constant maintained separately.
- **Schemas drive types.** Pydantic models are the runtime source of truth; types come from the model. Never declare a model and a `TypedDict` that mirror each other.
- **Enums for fixed sets.** Use `enum.StrEnum` or `Literal[...]` for fixed sets of values. Never scatter magic strings.
- **No duplicate constants.** If a value (a path, a magic number, a default) needs to appear in two modules, the second occurrence is an import — never a literal repeat.

The test: when you change a value, do you have to remember every other place it lives? If yes, you have duplication. Centralize.

---

## 12. Caching

Memoization is a sharp tool. Used wrong, it leaks memory or holds onto state that should be released.

### Rules

- **Never on instance methods.** `@functools.cache` and `@lru_cache` on a method hold a reference to `self` forever — the instance becomes uncollectable. Use a module-level function, or `cachetools` if you need per-instance caching. Ruff's `B019` enforces this.
- **`@cache` only when the input domain is bounded.** Unbounded `@cache` is unbounded memory growth. For unbounded domains, use `@lru_cache(maxsize=N)` with a deliberate cap.
- **Pure functions only.** Caching a function that does I/O caches a *moment in time* — stale results downstream. If the function has side effects, caching makes the bug worse.

```python
# Bad — leaks every Client instance forever
class Client:
    @lru_cache
    def fetch(self, key: str) -> bytes: ...

# Good — module-level cache, bounded
@lru_cache(maxsize=1024)
def lookup_country_code(alpha2: str) -> CountryCode: ...
```

---

## 13. Logging

### Philosophy

Log at decision points, not I/O points. The question a log answers is **why did the system do what it did** — not what functions were called or what data flowed through.

### Use the Stdlib Logger (or structlog)

`logging.getLogger(__name__)` per module. Configure handlers and formatters once at the application entry point. For structured/JSON logs in production, use `structlog` or a JSON formatter on the stdlib logger.

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Task dispatched", extra={"task_id": task_id, "phase": phase, "priority": priority})
```

### Levels

- **`DEBUG`** — Developer investigating a specific issue. High volume, disabled in production.
- **`INFO`** — Operator watching the system run. Lifecycle events: service started, task dispatched, phase transitioned.
- **`WARNING`** — Something unexpected but non-fatal. A retry that succeeded, a deprecated config key. Deserves attention, not broken yet.
- **`ERROR`** — Something broke and a human needs to know. Failed transitions, unhandled exceptions, invariant violations. Every `ERROR` log must be actionable.
- **`CRITICAL`** — System cannot continue. Reserve for true fatal conditions.

### Rules

- **Structured data, always.** Pass context via `extra=` (stdlib) or as keyword args (structlog). Never bake variable values into the message string for queryability.
- **Log decisions, not actions.** "Chose retry because rate limit resets in 12s" is useful. "Called GitHub API" is noise — the action is visible in tracing; the log captures *reasoning*.
- **One log per decision, not per step.** Don't log entry and exit of every function.
- **`logger.exception()` inside `except` blocks** to capture the traceback automatically.
- **Uniform across layer boundaries.** Logging format stays consistent regardless of which implementation is behind a layer's interface.

---

## 14. Async Discipline

A long-running service cannot tolerate loose async hygiene. `asyncio` is unforgiving — unawaited coroutines warn but don't fail loudly, and lost task references vanish silently.

### Never Drop a Task Reference

`asyncio.create_task()` returns a task that gets garbage-collected if nothing holds a reference — the task simply disappears, sometimes mid-execution. Always store the reference.

```python
# Good — store reference, handle exceptions
self._background_tasks: set[asyncio.Task] = set()
task = asyncio.create_task(self._cleanup())
self._background_tasks.add(task)
task.add_done_callback(self._background_tasks.discard)

# Bad — task may be garbage collected before completion
asyncio.create_task(self._cleanup())
```

In 3.11+, prefer `asyncio.TaskGroup` for structured concurrency — it handles references and exception aggregation automatically.

### Never Block the Event Loop

Inside an `async def`, never call a blocking function (file I/O, `requests.get`, `time.sleep`). Use the async equivalent (`aiofiles`, `httpx`, `asyncio.sleep`) or offload to a thread with `asyncio.to_thread()`.

### Parallel vs Sequential

Default to sequential `await`. Use `asyncio.gather()` (or `TaskGroup` in 3.11+) only when parallelism is intentional, bounded, and the operations are independent. Unbounded parallel calls over a large collection risks resource exhaustion — bound with `asyncio.Semaphore`.

```python
# Good — bounded parallel via TaskGroup
async with asyncio.TaskGroup() as tg:
    results = [tg.create_task(p.health_check()) for p in plugins]

# Good — semaphore caps concurrency over unknown-size collection
sem = asyncio.Semaphore(10)
async def bounded(task: Task) -> Result:
    async with sem:
        return await process_task(task)
results = await asyncio.gather(*(bounded(t) for t in all_tasks))

# Bad — unbounded parallel over potentially huge collection
results = await asyncio.gather(*(process_task(t) for t in all_tasks))
```

### Timeouts: `asyncio.timeout()` over `wait_for()`

On 3.11+, use `asyncio.timeout()` (context manager) — not `asyncio.wait_for()` (legacy). `timeout()` composes with `TaskGroup`, wraps blocks rather than single awaits, and avoids spawning an extra wrapper task.

```python
# Good — modern, composable
async with asyncio.timeout(5):
    result = await fetch(url)

# Legacy — avoid in new code
result = await asyncio.wait_for(fetch(url), timeout=5)
```

### Request-Scoped State: `contextvars.ContextVar`

For per-request / per-task ambient state in async code (request ID, trace ID, current user), use `contextvars.ContextVar`. `threading.local` leaks across `asyncio` tasks; globals are worse. ContextVar is the only correct mechanism.

```python
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar("request_id")

async def handle_request(req: Request) -> Response:
    token = request_id.set(req.id)
    try:
        return await process(req)
    finally:
        request_id.reset(token)  # always reset via the token
```

### Cancellation and Cleanup

Long-running operations must be cancellable. Trust `asyncio.CancelledError` to propagate — don't catch it unless you genuinely need to release a resource, and then re-raise.

```python
# Cleanup with try/finally
try:
    await long_running_operation()
finally:
    await release_resources()

# Re-raise CancelledError after cleanup
try:
    await long_running_operation()
except asyncio.CancelledError:
    await release_resources()
    raise  # never swallow cancellation
```

### `asyncio.run()` Only at the Entry Point

Call `asyncio.run()` once, at the program's `main()`. Don't nest `asyncio.run()` calls or run loops manually inside library code — let the application own the event loop lifecycle.

---

## 15. Observability & Tracing

Logging captures *reasoning*. Tracing captures *structure* — the shape of an operation, its duration, its nesting, and its outcome. Together they make any behavior diagnosable after the fact.

### OpenTelemetry

Use OpenTelemetry (`opentelemetry-api`, `opentelemetry-sdk`) for spans. The instrumentation packages for common libraries (httpx, asyncpg, fastapi) provide automatic spans for I/O — opt in at the entry point.

```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("phase_transition", attributes={"task_id": task_id}):
    result = await run_phase(task, phase)
```

### Trace Correlation

Every log entry carries `trace_id` for correlation with spans. This is the bridge between logging and tracing — filter logs by trace ID to see every log line for a specific operation across all components. OpenTelemetry's logging integration handles this automatically.

### Record Decisions Explicitly

Non-obvious choices (retry vs. fail, plugin selection, safety verdicts) deserve span attributes or events that capture: context, options considered, chosen option, reasoning. Don't bury this in a `INFO` log buried among hundreds of others.

### Structured Events Over Free Text

"What happened" lives in typed span name and attributes. "Why and how" lives in structured event attributes. Free-text messages are for humans scanning logs — structured fields are for querying, dashboards, and automated analysis.

---

## 16. Graceful Degradation

A long-running service must survive any single component failure. A dependency crash, a temporary DB lock, an external API timeout — none of these should take down the system.

### Degrade, Don't Crash

When a dependency fails, reduce capability instead of terminating. A failed trigger source means no new events from that source — not a dead service. A failed external call means the current operation retries or pauses — not a process exit.

### Log the Degradation

Every degradation emits a `WARNING`-level log and a health event. The log captures: what failed, what capability is reduced, and when recovery will be attempted. Silent degradation is invisible degradation — and invisible degradation is a bug.

```python
logger.warning(
    "Plugin health check failed — disabling until recovery",
    extra={
        "plugin_id": plugin_id,
        "capability": "trigger polling",
        "retry_in_ms": backoff.next_attempt_ms,
    },
)
```

### Auto-Recover

When the failed dependency returns, the system resumes full capability without manual intervention. Health checks drive recovery — when a dependency's `health_check()` succeeds again, re-enable it and log the recovery at `INFO` level.

---

## Philosophical Foundations

These are the mental models behind the standards. Internalize them before coding — they guide decisions the rules don't cover.

- **Newspaper metaphor** (Uncle Bob) — A file reads top-to-bottom: headline first, details last. Caller above callee. The reader should never scroll up to understand what they just read.
- **Deep modules** (Ousterhout) — A good module does a lot behind a simple interface. Don't split for the sake of splitting — splitting multiplies interfaces and forces readers to bounce. Pragmatic function length follows from this.
- **Simple over easy** (Hickey) — Easy means familiar. Simple means fewer entanglements. Choose simple — even when it requires learning something new. Avoid complecting (braiding together) separate concerns.
- **Functional Core / Imperative Shell** (Bernhardt) — Decisions are pure functions. Effects are thin wrappers. This makes the hard parts trivially testable and the effectful parts trivially simple.
- **Parse, don't validate** (King) — Transform unstructured input into typed, branded values at the boundary. Once parsed, the type system guarantees correctness — no runtime checks needed downstream.
- **Duplication over wrong abstraction** (Metz) — Three similar functions are better than one premature abstraction. Wait until the pattern is clear. The cost of the wrong abstraction compounds; duplication is cheap to fix later.
- **Semantic compression** (Muratori) — Don't design abstractions upfront. Write the code, see the patterns emerge, then compress. Abstraction is the last step, not the first.
- **Make the change easy, then make the easy change** (Beck) — Refactor first to make the feature trivial to add, then add it. Two small steps beat one complex step.
- **Code as narrative** (Knuth) — Code is read far more than written. Ordering, naming, and structure serve the reader's comprehension, not the writer's convenience.
- **Ubiquitous language** (DDD) — Names mirror the business domain. `TaskEngine`, `PipelineStage`, `TriggerEvent` — not `ItemProcessor`, `StepExecutor`, `IncomingData`.
- **Do one thing well, compose** (Unix) — Small, focused modules with standard interfaces. Composition over inheritance. Pipelines over monoliths.
- **Proximity and chunking** (Gestalt) — Related code stays together. Visual grouping (blank lines, sections) guides the eye. The reader's brain chunks what's close — use that.
- **Explicit is better than implicit** (Zen of Python) — Be obvious. No magic. No clever metaclasses where a plain function works. If a reader has to guess, the code is unclear.
- **Errors should never pass silently** (Zen of Python) — Catch what you can handle, let the rest bubble. Bare `except:` is a betrayal of this principle.
