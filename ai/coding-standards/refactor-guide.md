# Refactor Guide

How to run a refactoring session collaboratively. Language-agnostic. Read this **first**, every session, before any language-specific standards.

The standards files tell you *what good code looks like.* This file tells you *how to get there together* — the mode of working, when to push back, what earns its place, what to cut. Without this, the standards become a checklist you mechanically apply. With this, they become tools you use with judgment.

Examples in this guide are drawn from real sessions and lean Python (because that's where the patterns were observed), but the *principles* apply to any language. When you see Python syntax, translate to your language's equivalent: decorators → attributes/mixins/higher-order functions, `__all__` → `export` blocks / public modifiers, `with` → `try/finally` or RAII, and so on.

---

## The mode: co-owners, not order-taker

The user is the compass; you are the second pair of eyes that catches what they miss and pushes back when they're wrong. Don't optimize for agreement — optimize for the right outcome. If the user proposes something, evaluate it on its merits. If you agree, say so and act. If you disagree, say so and explain why.

**"Don't just accept things, really consider them."** That's the bar. Confirmation by default is worse than honest disagreement, because it teaches the user that your "yes" is meaningless.

When to push back:
- The user's instinct is right *in spirit* but the literal implementation breaks something. (e.g., "no defaults!" — agree on the spirit; propose a test fixture so 120 tests don't become boilerplate.)
- The user proposes a rename that violates a convention they'd want to follow if they remembered it. (e.g., `CaptureContextEvent` is verb-imperative; events are nouns. `ContextCaptureEvent` is right.)
- The user wants to collapse code that has structural meaning. (e.g., three `with suppress` blocks vs one — the three independent blocks ARE the failure-isolation contract.)

When NOT to push back:
- Taste calls inside their own codebase.
- Anything they've already considered and made a deliberate choice on.
- Anything where you have no better answer than theirs.

---

## The fine-comb discipline

Refactor mode is **line-by-line review**, not "skim and fix the obvious." Every line, every comment, every default value, every blank line, every name gets asked: *does this earn its place?*

Cycle for each unit of code:

1. **Read it cold.** Pretend you've never seen this file. What does each line claim? What invariant is implied? What would surprise a reader?
2. **Assess its need.** Could this line be deleted without losing anything? Could it be rewritten more clearly? Is the *why* visible, and is the *what* obvious from the code itself?
3. **Assess its perfection.** Among the choices that work, is this the best one? Is the name precise? Is the abstraction the right size? Is the comment load-bearing or noise?
4. **Consider best practices.** Does this match the language standards? If it deviates, is the deviation deliberate or accidental?
5. **Decide together.** Surface the assessment to the user, propose a change with tradeoffs, let them weigh in. Then act.

This is slow on purpose. The output is code that reads cleanly to a new reader six months later — which is the actual hard part of software, not making the test pass.

**Apply this to the surrounding code, not just the line you came to edit.** If you're refining a function, the rest of the file is fair game for the same scrutiny. The user may stop you ("not now, focus") — that's fine, but err on the side of noticing.

---

## Before touching code: ground in code

Before recommending a refactor, **read what's there.** Not the docstring — the actual code. Then verify your claims with `grep`, `cat`, a one-liner repl, or a focused unit test.

What this catches:
- A "dead constant" that's actually used by an external caller.
- A "missing abstraction" that already exists three files over.
- A library feature you assumed didn't exist (e.g., a response field the SDK already populates) — verify before claiming "we need to hardcode this."

What this avoids:
- Confidently proposing changes based on stale knowledge from training data.
- Fabricated citations to functions/files that don't exist or have moved.
- The "I think the SDK does X" moment that turns out to be wrong.

**After context compaction, re-ground.** Compaction loses state. The first thing you do post-compact is re-read the files you're about to edit. Don't trust the summary — verify against the current code. The user will (rightly) remind you of this if you forget.

---

## Present options, then recommend

When a refactor has more than one reasonable shape, lay out the choices honestly:

```
Option A — minimal change. Pros: safe, small diff. Cons: doesn't fix root cause.
Option B — encode the contract in code. Pros: invariant enforced. Cons: handles one edge case differently.

My recommendation: B. The whole module's reason for existence is X.
But A is the safer call if you'd rather keep the diff small at this stage.
```

Then let the user pick. This isn't ceremony — it's how you stay aligned without surprising them. The user knows the project; you know the patterns; the decision is theirs.

**Don't hide tradeoffs to make a recommendation look cleaner.** If Option B has a real catch, name it. The user is choosing between honest options, not picking from a sales pitch.

---

## What earns its place in code

The bar for every line, comment, and abstraction is the same: **does this earn its keep, or is it noise?**

### Comments

Earn their keep when they encode:
- A **load-bearing WHY** that the code can't say (constraint, invariant, edge case).
- A non-obvious effect that would surprise a future reader.
- A pointer to where the deeper context lives.

Don't earn their keep when they:
- Restate what the code already says.
- Explain a choice that's only meaningful to "us right now in this conversation."
- Speculate about future requirements ("kept this way so we can add siblings later").
- Reference the PR or task that introduced the code ("added for the X flow").

**Move WHY to where it's executed, not where it's referenced.** If a producer has surprising behavior, document it on the producer, not on every call site.

### Abstractions

Three similar lines is better than a premature abstraction. Don't extract a helper "in case we need it again." Extract when the duplication is real, the boundary is obvious, and the name carries weight.

**Watch for "lint-silencer cleverness."** If you reach for an unusual construct just to silence a linter when the obvious form is clearer, you've made the code worse to please a tool. Either keep the obvious form (with a targeted disable-comment if needed), or restructure honestly.

---

## Encode contracts in code, not comments

If a comment says *"every function below does X,"* there's almost always a way to make X true *by construction* — a decorator, a base class, a type. The contract becomes the code; the comment becomes redundant; future-you can't forget it because the convention enforces itself.

**Example:** a comment said *"every function below handles its own try/except and records a failure metric."* The fix: a decorator that *does* the try/except, applied to every relevant function. The decorator name **is** the contract statement. A function missing the decorator visibly doesn't obey the contract.

The same principle applies in any language:
- Python: a decorator.
- TypeScript/JavaScript: a higher-order function or class decorator.
- C#/Java: an attribute/annotation + an aspect/interceptor, or a base class.
- Go: a wrapper function returning a wrapped handler.
- Rust: a macro or a trait with a blanket impl.

The opposite anti-pattern: leaving the comment as a promise the next person has to verify by hand.

---

## Where things live

### Co-locate with the source of truth

If a piece of data is *also declared* somewhere else, derive it from there. Don't make two declarations that can drift.

**Example shape:** an orchestrator declares "region X is primary" by instantiating a fallback chain `FailoverClient(primary_region_client, backup_region_client)`. Some downstream observability layer *also* declares `PRIMARY_REGION = "us-east-1"` so it can attribute metrics. Two declarations, one truth, drift risk. Fix: derive the primary from the actual chain (`failover_client.primaries[0].region`) at the call site and pass it in. Now there's exactly one place that knows.

### Co-locate registries with where they're used

If a `REGION_QUOTAS` dict exists, it should sit next to `build_us_region_config()` / `build_eu_region_config()` in the regions module — not in the rate-limiting module that *consumes* it. Why: when someone adds a new region in the regions module, the quotas registry is staring at them in the same file. Drift becomes near-impossible.

### Public first, helpers near consumers

A reader who opens the file should land on the actual API immediately. Decorators/utilities/constants used only by private functions belong **near their consumers**, not above the public API. Use whatever your language gives you to declare the public surface explicitly (Python `__all__`, JS/TS `export`, C#/Java `public` modifiers, etc.) — convention-level "private by name" (Python underscore-prefix, Java package-private) reinforces but doesn't replace it.

---

## Failure handling

### Visible staleness beats silent staleness

When a registry is missing an entry, the wrong move is to silently default to a plausible value. The right move is to **flip a diagnostic flag and emit a sentinel** so dashboards surface the gap.

**Example shape:** when a currency isn't in the exchange-rate registry, emit `converted_total = 0` *and* flip `conversion_status = "unknown"`. The missing-data state is visible. An operator notices. The registry gets updated. Compare to "default to 1.0": the dashboard shows wrong-but-plausible totals forever and nobody notices.

### Isolated failure boundaries

When N independent operations each need to survive the others' failures, that's N try/catch blocks, not one. Inside a single try/catch, the first failure exits the block — everything after the failure point silently doesn't run. The visual repetition of N blocks has a structural purpose: a sink-A hiccup must not silently kill sink-B.

```python
# Wrong (Python; same shape in any language) — one failure kills the rest
try:
    write_to_sink_a()
    write_to_sink_b()
    write_to_sink_c()
except Exception:
    pass

# Right — each fails in isolation
try: write_to_sink_a()
except Exception: pass
try: write_to_sink_b()
except Exception: pass
try: write_to_sink_c()
except Exception: pass
```

Extra lines, N independent failure boundaries. Worth it.

---

## Iterative refinement

Don't try to land everything at once. Each round: **one small change, run tests, run lint, report, decide.** The user stays in control because every step is reviewable.

**After every edit:**
- Lint the touched files.
- Run the related tests (not the whole suite every time — the targeted file or class is usually enough until the final pass).
- Report concisely: "X passed, Y failed because Z."

**When tests fail:** read the failure carefully before changing code. Often the test is testing the *old* behavior and needs updating to match the new contract — not the code being wrong. Sometimes it's the other way around. Read first.

**Mass renames (sed/perl/IDE refactor):** verify the boundary. A `s/foo(/bar(/g` won't touch `import foo` (no paren), but might touch the new helper's own body (cause: infinite recursion). Read the diff after the regex, every time.

---

## Required vs optional kwargs

**Config that callers must declare:** no defaults. Required positional or keyword-only. The caller stating it explicitly is the whole point.

**Data that may not exist this call:** a "no value" default (`null`/`None`/`undefined`/empty) is fine. "Absence" is meaningful and the function handles it.

Don't conflate the two. A test-fixture wrapper that fills the required kwargs with sensible test defaults honors the spirit of "no defaults in API" without making every test scream with boilerplate.

---

## Things to cut on sight

Patterns that almost always need refining:

- **Class docstrings that enumerate fields.** They go stale the moment a field is added. Either enumerate exhaustively (and accept the maintenance) or don't enumerate at all (and trust the fields to speak).
- **YAGNI-flavored rationale.** "Kept as its own class so siblings can be added later" is designing for hypothetical future. The honest rationale is whatever is true *now*.
- **Context-only comments.** "(paired with X for symmetry)" — useful only in the conversation that produced it. Cut before commit.
- **Speculative future hooks.** Feature flags for non-existent features. Defensive validation for data that comes from your own boundary-validated input. Backwards-compat shims for callers you control.
- **Dense one-liners that "save lines."** Three obvious lines beats one clever line. Compression earns its place only when the compressed form is *also* easier to read. See language anti-patterns → "Compressing for Line Count."
- **Escape-hatch types** (`any` in TypeScript, `Any` in Python, `object` cast in C#, `interface{}` in Go). They disable type checking everywhere they touch. Reach for a real type, generic, structural interface, or precise union instead.

---

## Things to *keep* on sight

Patterns that look excessive but earn their place:

- **A class wrapping one field** — if the wire shape needs to be uniform across consumers.
- **Three near-identical `with suppress` blocks** — if they're independent failure boundaries.
- **A comment naming a load-bearing constraint** — if removing it would let a future reader make a wrong assumption.
- **An empty `__init__` or `pass`-body class** — if it's a marker for type discrimination or registration.

---

## Communicating back

After a non-trivial change, report in two layers:

1. **What changed** — a sentence per concept, not per file.
2. **What this leaves on the table** — anything the user might want to do next, or anything you held back from doing because it needed their call.

Don't summarize the obvious. The user reads the diff. Tell them what they can't see from the diff: the *why*, the *tradeoff*, the *next decision*.

---

## When NOT to follow this guide

This guide is for **substantive refactoring sessions** — multi-step, multi-file, judgment-heavy work. For a one-shot edit ("rename X to Y everywhere"), just do the edit; this guide is overhead.

The dial: the more judgment the task requires, the more this guide matters. The less it requires, the more you should just execute.

---

## Reading order for any session

1. **This file** — `refactor-guide.md`.
2. **The relevant language standards** — `<language>/coding-standards.md` and `<language>/anti-patterns.md`.
3. **The project's own context** — `CLAUDE.md`, `README.md`, recent commits.

Then look at the code.
