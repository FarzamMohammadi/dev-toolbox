# Python Anti-Patterns

Things that look productive but hurt the project. If you catch yourself doing any of these, stop and reconsider.

The first section is language-agnostic — these apply to any codebase. The Python-specific section follows.

---

## YAGNI Without Confirmation

Don't add features, abstractions, or infrastructure the user didn't ask for. "We might need this later" is not a reason to build it now. If you see a genuine future need, raise it — then wait for confirmation before acting. The user decides scope, not the agent.

## Gold-Plating

Shipping "working" on time beats shipping "perfect" late. But "working" is not "done" — the project's definition of done is the bar, not personal taste. The tension is real: meet the bar fully, then stop. Don't polish beyond what the checklist demands.

## Assuming Over Asking

When uncertain — ask. When "pretty sure" — still ask. Assumptions compound silently. A wrong assumption that ships is harder to fix than a question that takes 30 seconds. This applies to scope, implementation approach, naming, architecture, and especially edge cases.

## Premature Optimization

Don't optimize before measuring. Write clear, correct code first. Profile when performance is actually a problem — not when you imagine it might be. The bottleneck is almost never where you think it is.

## Cargo Culting

Don't copy patterns without understanding why they exist in this codebase. A pattern that solved a problem in module A may be unnecessary in module B. Every pattern earns its place through the specific problem it solves here — not because it exists elsewhere.

## Scope Creep Without Consent

Expanding task scope without explicit user agreement is a violation of trust. If you discover adjacent work that needs doing, surface it — don't silently include it. The user decides whether to expand scope, defer it, or ignore it.

## Dogmatic Rule Following

These standards are strong defaults, not absolute laws. When a specific case deliberately calls for deviation, deviate — but document why. The test: "Is this deviation intentional and justified, or am I being lazy?" The few invariants that *are* absolute should be called out as such by the project itself (e.g., a top-level architecture doc) — everything else is a default that judgment overrides when warranted.

## Silent Decisions

Making decisions on behalf of the user without communicating them is the fastest way to lose alignment. Every non-trivial decision gets surfaced: what you chose, why, and what alternatives existed. The user is always the compass.

---

## Python-Specific

### Bare `except:` and Broad `except Exception:`

```python
# Bad — catches KeyboardInterrupt, SystemExit, MemoryError. Hides bugs.
try:
    do_thing()
except:
    pass

# Bad — too broad, hides programming errors
try:
    do_thing()
except Exception:
    logger.warning("something broke")
```

Catch the specific exceptions you can handle. `except Exception:` is acceptable only at the outermost boundary, with a comment explaining why, and always with `logger.exception(...)` so the traceback survives.

### Mutable Default Arguments

```python
# Bad — `items` is shared across all calls
def append_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items

# Good
def append_item(item: str, items: list[str] | None = None) -> list[str]:
    items = items if items is not None else []
    items.append(item)
    return items
```

The default is evaluated once, at function definition. Mutating it leaks state across calls — a classic, silent bug.

### Using `Any` to Silence Type Errors

`Any` disables type checking everywhere it touches. Reach for `object`, `TypeVar`, `Protocol`, or a precise union instead. If the value really is unknowable, use `object` and narrow with `isinstance` before use.

`# type: ignore` without an error code or comment is the same anti-pattern. If you must, be specific: `# type: ignore[arg-type]  # mypy false positive on Self in mixin`.

### Defensive Programming Inside the Boundary

Re-validating data five layers deep that was already validated at the boundary. If `parse_task_input` returned a `CreateTaskInput`, downstream code doesn't need to check `if input.title:` again — the model already proved it exists. Defensive checks inside the boundary are a sign the boundary doesn't trust itself. Fix the boundary instead.

### Catching Exceptions for Expected Control Flow

```python
# Bad — using exceptions for flow control
try:
    value = my_dict[key]
except KeyError:
    value = default

# Good — Pythonic, no exception machinery for the happy path
value = my_dict.get(key, default)
```

Exceptions are for *exceptional* cases. When the API provides a non-exceptional path (`dict.get`, `next(iter, default)`, `Optional` returns), use it.

### Mocking Internals in Tests

Mocking another module's functions to test the current one couples tests to internal structure — refactors break tests that should still pass. Mock only at the system boundary (network, filesystem, time, external services). Internal collaboration is tested by calling the real code with real data.

### Dict-as-Struct

Passing `dict[str, object]` around as if it were a structured type. The reader has to guess every key. The type checker can't help. Refactor into a `dataclass`, Pydantic model, or `TypedDict` so the shape is named and checkable.

```python
# Bad
def process(task: dict) -> dict:
    return {"id": task["id"], "result": ...}

# Good
@dataclass(frozen=True)
class Task:
    id: TaskId
    name: str

def process(task: Task) -> ProcessResult: ...
```

### `*args, **kwargs` as Default

Variadic arguments are powerful and almost always wrong. They erase the type signature — readers and tools can't see what's accepted. Use explicit parameters unless you're genuinely writing a passthrough wrapper or a true variadic function (`max`, `print`).

### Monkey-Patching

Reassigning attributes on third-party modules or classes at runtime. It works until two pieces of code patch the same thing, or until the upstream changes, or until you forget you did it. Use composition, subclassing, or dependency injection instead.

### God-Object Classes

A class with 20+ methods doing unrelated things. The Class noun has become a junk drawer. Split by responsibility — small classes that compose beat one class that does everything.

### Using `os.path` Where `pathlib` Works

`pathlib.Path` is composable, typed, and reads like the operations it performs (`path / "subdir" / "file.txt"`). `os.path.join(os.path.dirname(...), ...)` is verbose and stringly-typed. Use `pathlib` for new code.

### Manual Resource Cleanup

```python
# Bad — leaks the file handle on exception
f = open(path)
data = f.read()
f.close()

# Good
with open(path) as f:
    data = f.read()
```

If you find yourself writing `try/finally` to close something, ask whether a context manager already exists (or whether you should write one with `__enter__`/`__exit__` or `@contextmanager`).

### Floating Coroutines

Calling an `async` function without `await` and without `asyncio.create_task` (with a reference held). The coroutine warns at most and never runs — or runs partially and then vanishes. Always `await` or schedule with a held reference.

### Catching `asyncio.CancelledError` and Swallowing It

```python
# Bad — task can never be cancelled
try:
    await long_op()
except asyncio.CancelledError:
    pass

# Good — release resources then re-raise
try:
    await long_op()
except asyncio.CancelledError:
    await release()
    raise
```

`CancelledError` is structured concurrency's mechanism for stopping work. Swallowing it breaks every cancellation path above you.

### Module-Level Side Effects

Running I/O, network calls, or other side effects at module import time. Imports should be free of observable effects — readers expect importing a module to be cheap and idempotent. Put side effects inside functions that the caller invokes explicitly.
