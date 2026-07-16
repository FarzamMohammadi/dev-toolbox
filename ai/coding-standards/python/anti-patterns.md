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

## Compressing for Line Count

Collapsing multiple clear lines into one dense expression because "it's shorter." Fewer lines is not a goal — clarity is. Compression earns its place **only** when the compressed form is *also* easier to read for someone new to the file. If the reader has to mentally unpack stacked idioms (`**` spread + `or {}` fallback + `dict.fromkeys`) on one line to understand what's happening, the verbose form wins.

```python
# Bad — three idioms stacked into one line
merged = {**(maybe or {}), **dict.fromkeys(extras, "default")}

# Good — each line says one thing
merged = dict(maybe or {})
for key in extras:
    merged[key] = "default"
```

Related smells from this same instinct:
- Walrus operators inside comprehension filters (`if (x := lookup(k)) is not None`)
- Nested ternaries (`a if c1 else b if c2 else c`)
- Reaching for a "clever" form to silence a lint rule (e.g. dict-comprehension → `dict.fromkeys` for `C420`) when the obvious form is what a reader would expect — leave the obvious form, add a `# noqa` if needed, or restructure honestly.

A comprehension that stacks multiple `for`/`if` clauses is the same instinct in loop form. It reads worse than a named helper with an explicit, typed loop — and the helper gets a name and a return type the comprehension can't carry:

```python
# Bad — two `for`s and an `if` packed into one comprehension
ids = [item.id for order in orders for item in order.line_items if item.in_stock]

# Good — a named helper, one clause per line, return type stated
def in_stock_item_ids(orders: list[Order]) -> list[ItemId]:
    ids: list[ItemId] = []
    for order in orders:
        for item in order.line_items:
            if item.in_stock:
                ids.append(item.id)
    return ids
```

## Half-Applied Rename

Renaming a symbol but leaving some references on the old name. A rename is finished only when *every* call site, test, and docstring uses the new name. A half-applied rename is worse than none: two names for one thing imply they're *different* things, and the next reader burns time hunting for a distinction that isn't there.

```python
# Bad — the parameter was renamed to `dry_run`, but a caller still passes the old name
def schedule(task: Task, *, dry_run: bool = False) -> None: ...

schedule(task, preview=True)   # ← stale name: silently wrong, or a TypeError at runtime
```

Treat the rename and its propagation as one atomic change — grep for the old name before you call it done. A strict type checker and a full test run catch the references your eyes miss.

## Dogmatic Rule Following

These standards are strong defaults, not absolute laws. When a specific case deliberately calls for deviation, deviate — but document why. The test: "Is this deviation intentional and justified, or am I being lazy?" The few invariants that *are* absolute should be called out as such by the project itself (e.g., a top-level architecture doc) — everything else is a default that judgment overrides when warranted.

## Silent Decisions

Making decisions on behalf of the user without communicating them is the fastest way to lose alignment. Every non-trivial decision gets surfaced: what you chose, why, and what alternatives existed. The user is always the compass.

## Documenting Invariants Instead of Encoding Them

A comment that says *"every function below does X"* is a promise the next person has to verify by hand. If the language has a construct to make X true by construction — a decorator, a base class, a type — use it. The construct's name becomes the contract; the comment becomes redundant; a function missing it visibly doesn't obey the contract.

```python
# Bad — the comment is a promise nothing enforces
# All handlers catch their own exceptions and record a metric on failure.
def handle_signup(event): ...
def handle_login(event): ...
def handle_logout(event): ...

# Good — the decorator is the contract; missing decorator is visibly wrong
@safe_handler(metric="signup_failed")
def handle_signup(event): ...

@safe_handler(metric="login_failed")
def handle_login(event): ...
```

The same pattern: type system over assertion comments, exhaustiveness checking over "remember to update all cases" comments, dataclass over "this dict always has these keys."

## Silent Staleness

When data is missing — an unrecognized currency, an absent feature-flag entry, a config that disappeared — the wrong fix is to *silently* default to a plausible value. The dashboard will show wrong-but-believable numbers forever and nobody will notice the gap.

The right fix: **make the staleness visible.** Emit a sentinel (e.g. `0`, `null`, `"unknown"`) *and* flip a diagnostic flag so operators can filter for the gap and update the registry.

```python
# Bad — operator never notices the new currency isn't registered
def get_exchange_rate(currency: str) -> float:
    return RATES.get(currency, 1.0)  # ← silent default of 1.0 hides the gap

# Good — gap is visible
def get_exchange_rate(currency: str, rates: dict[str, float]) -> float | None:
    return rates.get(currency)  # caller decides what 'None' means

# at the call site:
rate = get_exchange_rate(order.currency, RATES)
if rate is None:
    logger.debug(f"No rate registered for {order.currency!r}")
    quote.conversion_status = "unknown"
    quote.converted_total = 0
```

The principle: a defaulted-to-plausible-value is a bug that compounds over time. A visible-gap is a bug that gets fixed the next time someone looks at the dashboard.

## Pass-through Parameters Without Use

A function that takes parameters *only to forward them* to a downstream callee — without reading them itself — is a structural signal: those parameters belong together as a typed bundle, or the call chain is wrong.

```python
# Bad — process_order receives 3 params it never uses; just forwards to record_audit
def process_order(
    order,
    customer_email,      # ← only used by audit
    customer_tier,       # ← only used by audit
    customer_region,     # ← only used by audit
):
    result = compute_total(order)
    record_audit(
        order, customer_email=customer_email,
        customer_tier=customer_tier, customer_region=customer_region,
    )

# Good — bundle them into a named type at the source; the intermediary
# carries one opaque object instead of three pieces it knows nothing about
@dataclass(frozen=True)
class AuditContext:
    customer_email: str
    customer_tier: str
    customer_region: str

def process_order(order, audit_context):
    result = compute_total(order)
    record_audit(order, audit_context=audit_context)
```

The bundle does three things at once: gives the cohesive concept a *name*, removes the intermediary's apparent dependency on what it doesn't use, and makes the call chain reveal *whose* concern each piece is.

## Tuple Returns Often Hide Multiple Jobs

A function returning a tuple of two unrelated things is often doing two jobs in one. The tuple is the smell; the fix is usually to split the responsibility.

```python
# Bad — build_client does two jobs: fetch the config AND build the client
def build_client(account_id) -> tuple[Client, Config]:
    config = fetch_config(account_id)
    client = Client(endpoint=config.endpoint, timeout=config.timeout)
    return client, config   # ← caller needs both halves

# Good — caller sequences the steps; each function has one job
config = fetch_config(account_id)
client = build_client(config)
metrics = init_metrics(config, account_id)
```

Exception: tuples are fine for *naturally paired* returns (e.g. `divmod(a, b) -> (quotient, remainder)`, an iterator returning `(key, value)`). The anti-pattern is the *unrelated* pair returned because a function was doing two jobs.

## Reimplementing What the SDK Gives You

Before writing a derivation, a registry, or a parsing helper to extract some piece of information, **ground in the SDK first.** Read the type definitions, inspect the object in a REPL, grep the library source. The thing you're about to build may already exist as a first-class field.

Illustrative shape: a service hand-rolls a prefix-matching dict to attribute records to regions (`us-east-1 -> us`, `eu-west-2 -> eu`, etc.). The cloud SDK's response object already carries a `region_partition` field set directly by the API. The whole derivation is dead weight that also has to be maintained as new regions ship.

The fix is mechanical (replace the derived value with the SDK field); the cost of not catching it is years of stale code that drifts with every upstream release.

The general rule: if you're about to write code that maps from one shape to another, ask first whether the upstream already gives you the target shape.

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

When that boundary catch *is* warranted, mark its justification with a `Boundary:` prefix. The marker makes a legitimate broad `except` — the deliberate external-I/O edge that must not crash the caller — visibly different from a lazy catch-all that's hiding bugs. A reader scanning for swallowed errors learns which ones are intentional.

```python
try:
    deliver(payload)
except Exception:
    # Boundary: a malformed payload or a transient sink failure must not abort the
    # batch — log it and move to the next item.
    logger.exception("Delivery failed for item %s", item_id)
    return
```

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

### Terse Loop & Binding Variables

Single- or double-letter loop variables (`o`, `inv`, `e`, or `i` for a domain item) force the reader to re-derive what the variable holds every time it appears. "It's a small scope" is not an excuse — name the iteration variable for the singular of the collection.

```python
# Bad
for o in orders: ...
for inv in invoices: ...
async for e in stream(source): yield e
results = [r for r in fetch()]

# Good
for order in orders: ...
for invoice in invoices: ...
async for event in stream(source): yield event
results = [result for result in fetch()]
```

The only exceptions: a deliberately-unused binding (`_`), and conventional `i`/`j` for a pure numeric `range()` with no domain meaning. See [`coding-standards.md`](coding-standards.md) → **Naming**.

### `*args, **kwargs` as Default

Variadic arguments are powerful and almost always wrong. They erase the type signature — readers and tools can't see what's accepted. Use explicit parameters unless you're genuinely writing a passthrough wrapper or a true variadic function (`max`, `print`).

### Building a kwargs dict to splat into a constructor/call

Assembling arguments in a `dict` and `**`-splatting them — usually to make one argument conditional — throws away type checking. The checker can't validate `**kwargs` against the signature, so a wrong or unsupported key only blows up at runtime. Pass arguments explicitly; gate the optional one.

```python
# Bad — type checking is blind to this; an unsupported key fails only at runtime
client_kwargs = {"base_url": url, "timeout": 30, "retries": 3}
if use_cache:
    client_kwargs["cache"] = cache
client = HttpClient(**client_kwargs)

# Good — explicit call, every arg checked; the conditional value is computed, not the kwarg
cache = build_cache() if use_cache else None
client = HttpClient(base_url=url, timeout=30, retries=3, cache=cache)
```

If a kwarg must be *omitted* (not just empty) on some versions/paths, that's a real case for a small conditional `**({"k": v} if cond else {})` — but reach for it only when omission and "empty value" genuinely differ. Default to the explicit call.

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

### `@lru_cache` / `@cache` on Instance Methods

```python
# Bad — every Client instance is kept alive forever by the cache
class Client:
    @lru_cache
    def fetch(self, key: str) -> bytes: ...
```

The cache holds a reference to `self`, so the instance can never be garbage collected. Move the cached function to module level, or use `cachetools` with a weak-reference strategy if you genuinely need per-instance caching. Ruff's `B019` rule catches this — leave it on.

### Bare `@cache` on Unbounded Input

`@functools.cache` has no size limit. Used on a function whose input domain is unbounded (URLs, user IDs, request payloads), it leaks memory until the process dies. Use `@lru_cache(maxsize=N)` with a deliberate cap whenever the input domain isn't trivially small and bounded.

### `asyncio.wait_for` in New Code

`wait_for` is the pre-3.11 way to add timeouts. Modern code uses `asyncio.timeout()` (context manager) — it composes with `TaskGroup`, wraps blocks rather than single awaits, and avoids the extra wrapper task. Migrating existing `wait_for` calls is low priority; writing new ones is the anti-pattern.

### Methods That Don't Use `self`

If a method never references `self`, it's a free function pretending to be a method. The class membership misleads the reader about OO structure (suggests state coupling that isn't there) and forces tests to instantiate the class for no reason.

```python
# Bad — _normalize_record never touches self; lives on the class anyway
class RecordProcessor:
    def _normalize_record(self, record: dict) -> dict:
        # ... cleans whitespace, lowercases keys, drops nulls ...
        # nothing references self
        return cleaned

# Good — module-level free function in the module where it belongs
def normalize_record(record: dict) -> dict:
    return cleaned
```

Side benefit: free functions are testable without mocking an instance. Tests stop carrying `processor = RecordProcessor()` boilerplate that exists purely to call the method.

The Python-flavored fix when you can't move it (e.g. you want to keep the namespace): `@staticmethod`. But ask first whether it should live on the class at all — usually the answer is no, and a module-level function is cleaner.

### Transliterating Another Language's Idiom

Porting a construct wholesale from the language you came from instead of using Python's natural form. The code works, but it reads as foreign, and a fluent Python reader pays a tax decoding why it's shaped that way.

```python
# Bad — a C#/Java "static class": a class that only ever holds stateless helpers
class StringUtils:
    @staticmethod
    def slugify(value: str) -> str: ...

    @staticmethod
    def truncate(value: str, limit: int) -> str: ...

# Good — in Python the namespace is the module; callers import the functions
# string_utils.py
def slugify(value: str) -> str: ...


def truncate(value: str, limit: int) -> str: ...
```

The same tax shows up as a class of `@classmethod`s standing in for a static holder (use a module, or a frozen `@dataclass` when there is genuinely state), a sentinel object where `T | None` belongs, or hand-written getters/setters where a plain attribute or `@property` is idiomatic. The test: would someone who only ever wrote Python recognize it as natural? See [`../philosophy.md`](../philosophy.md) → **Idiom Over Transliteration**.

### Class Docstrings That Enumerate Fields

```python
# Bad — list goes stale the moment someone adds a field, and they often do silently
class CustomerProfile(BaseModel):
    """Customer profile: name, email, tier, signup_date."""
    name: str
    email: str
    tier: str
    signup_date: datetime
    region: str | None = None       # ← added later, docstring not updated
    locale: str | None = None       # ← same
```

Either enumerate exhaustively (and accept the maintenance) or don't enumerate at all. The fields themselves are self-documenting via their names and types — the docstring should explain *what the class is for*, not duplicate the field list.

```python
# Good — the docstring carries the why; the fields carry the what
class CustomerProfile(BaseModel):
    """A customer's stored profile and preferences."""
    ...
```

This generalizes: any docstring that duplicates information the code already conveys (field lists, method names, simple types) is a maintenance trap. Load-bearing docstrings explain purpose, invariants, and constraints — not field inventories.

### Overriding Without `@override` (3.12+)

In a 3.12+ project, every method that overrides a base-class method should carry `@typing.override`. Missing it means the day someone renames the parent's method, the child silently becomes an unrelated method instead of failing type-check. Enable `reportImplicitOverride = "error"` (pyright) or the mypy equivalent so the *absence* of `@override` is itself a type error.
