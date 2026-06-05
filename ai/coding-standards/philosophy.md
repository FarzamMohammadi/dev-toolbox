# Coding Philosophy

The language-agnostic principles underneath every standard. Read this **after** `refactor-guide.md` and **before** any `<language>/` file, every session.

Three layers, three jobs:

- **`refactor-guide.md`** — the *mode*: how to run a session collaboratively, when to push back, what earns its place.
- **This file** — the *values*: the durable principles that hold in any language. What to internalize.
- **`<language>/coding-standards.md` + `anti-patterns.md`** — the *patterns*: what those values look like in a specific language's syntax and tooling.

Examples here are concrete (and lean on one language for legibility), but the principle is the point — translate the syntax to your language's equivalent. None of this justifies code that reads badly: when a rule and clarity collide, the application is wrong, not the rule.

---

## Comments

A comment earns its place only when it carries something the code **cannot**: the unspoken *why*, the context behind a decision, a constraint or edge case a reader would otherwise trip over. It never narrates the *what* — the code already says that.

Earns its keep:

- A **load-bearing why** the code can't express — a constraint, an invariant, "we tried X and it broke because Y."
- A **non-obvious effect** that would surprise the next reader.
- A **pointer** to where the deeper context lives.

Doesn't:

- Restates what the line plainly does.
- Explains something meaningful only to "us, right now, in this conversation."
- Speculates about future requirements ("kept this way so we can add siblings later").
- Names the ticket or PR that introduced the code.

```text
# Bad — narrates the what
i += 1  # increment the retry counter

# Good — the why the code can't say
# Vendor's gateway 503s for ~1s right after a deploy; a single immediate
# retry clears it without surfacing a blip to callers.
```

Two rules of thumb:

- **Don't overdo it.** Comment density is not a virtue. A file thick with comments that restate the code is *harder* to read — the signal drowns in narration. Reach for a comment when the code genuinely can't speak; otherwise let it speak. When you do write one, keep it tight.
- **Move the why to where it's executed, not where it's referenced.** If a producer has surprising behavior, document it on the producer, not on every call site. One durable note beats N copies that drift.

When a comment describes a contract ("everything below does X"), prefer to **make it true by construction** — a base type, a wrapper, a decorator — so the convention enforces itself and the comment becomes redundant. (See `refactor-guide.md` → "Encode contracts in code, not comments.")

---

## Idiom Over Transliteration

Write the form a fluent reader of *the target language* expects — not the one transliterated from the language you came from. The same idea has a different natural shape in each language; reach for the local one.

- A namespace of stateless helpers is a **module** of functions in Python or Go — not a class of `static` methods carried over from C#/Java.
- "A value with a little behavior" is a **record / dataclass / struct** — not a class of `classmethod`s aping a static holder.
- "Maybe-absent" is the language's **optional / union** (`T | None`, `Option<T>`, `Result<T, E>`) — not a sentinel object or a null-object pattern imported from elsewhere.

The test: would someone who only ever wrote *this* language recognize it as natural? If they'd ask "why is this shaped like Java?", the construct is a transliteration. Pick the idiom that disappears.

This is not "never learn from other ecosystems" — good ideas travel. It's "express the idea in the host language's grammar," so the reader spends attention on the logic, not on decoding a foreign accent.

---

## Separate Retrieval From Policy

Reading a value and deciding what to do when it's missing are **two jobs**. Keep them apart:

- The **boundary** (a settings/config module) retrieves the raw value and surfaces *absence* — returns "not set," warns, flips a flag. It holds no defaults and no domain logic.
- The **owner** of the concern applies the default and the rules. It knows what "missing" should mean *here*, what a blank value implies, what the fallback is.

A config reader that also bakes in defaults braids together "where the value comes from" with "what we do without one" — two things that change for different reasons. Split them and each side stays obvious: the boundary is a thin retrieval surface; the policy lives where the concern is actually understood. This is `Parse, don't validate` applied to configuration — parse the environment at the edge, decide policy in the interior.

---

## Side Effects Resolve Once

A read that *does something* — warns on absence, emits a metric, logs a fallback — should resolve **once**, at a boundary (startup, construction), not re-run on every call. Re-reading a value is cheap and harmless; re-warning is per-call noise that trains operators to ignore the signal.

Separate "what is the value" (repeatable, side-effect-free) from "announce the state of it" (once). Resolve the configuration when the component is built; reuse the resolved result for each request. The warning fires at startup, where a human sees it — not buried in every log line for the lifetime of the process.

---

## Philosophical Foundations

The mental models behind the standards. Internalize them — they guide the decisions the rules don't cover.

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
- **Explicit over implicit** (Zen of Python) — Be obvious. No magic, no clever indirection where a plain construct works. If a reader has to guess, the code is unclear.
- **Errors should never pass silently** (Zen of Python) — Catch what you can handle; let the rest bubble. Swallowing an error you can't handle is a betrayal of the next person to debug it.
