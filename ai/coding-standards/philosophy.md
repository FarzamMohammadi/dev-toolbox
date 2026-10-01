# Coding Philosophy

The language-agnostic principles underneath every standard. Read this **after** `refactor-guide.md` and **before** any `<language>/` file, every session.

Three layers, three jobs:

- **`refactor-guide.md`** — the *mode*: how to run a session collaboratively, when to push back, what earns its place.
- **This file** — the *values*: the durable principles that hold in any language. What to internalize.
- **`<language>/coding-standards.md` + `anti-patterns.md`** — the *patterns*: what those values look like in a specific language's syntax and tooling.

Examples here are concrete (and lean on one language for legibility), but the principle is the point — translate the syntax to your language's equivalent. None of this justifies code that reads badly: when a rule and clarity collide, the application is wrong, not the rule.

---

## The First Rule: The Best Code Is No Code

Asked first, of everything: an idea, a feature, a plan, a component, a system, the architecture, a test, a line of code. It comes before every other principle here because it decides whether there is anything for them to apply to. Farzam, 2026-10-01: *"it's applicable to everything from ideas to plans to components, systems, architecture, all the way to code, lines of code."*

Two questions, in this order, from the bottom up:

1. **Is it needed?** What breaks today without it? Is it already done, or already enforced, somewhere else, so that this would be a second copy? If nothing breaks, it is not made: not the feature, the abstraction, the setting, the check, the test, the log line, the document or the step. Nothing is built to be needed later, and nothing is built to be optimized later.
2. **Is this the best way to do it, for the long term?** Weigh the alternatives, doing less among them. Will it go stale? Will it still hold for the next user, the next case, the next contributor? What earns its place is made the general way, with craft and care, the first time, so it is never redone.

Minimal in what exists, thorough in how it is made. The two halves are one rule: the less there is, the more care each piece gets, and the less any mind, a person's or an agent's, has to hold. Every extra piece is overhead carried forever: read, tested, maintained, explained.

Where it is applied, so it is never skipped:

- **Before work starts:** say what the work adds, what breaks without each piece, and what it leaves out.
- **In every plan, brief and design:** name what was left out, and why.
- **In every handoff to an agent:** hand it both questions for whatever the plan does not settle, and ask for what it left out.
- **In every review:** read first for what can go, then for what is wrong.
- **For tests:** a test pins a behaviour something breaks without, that reading the code cannot show, and that no other test already holds.

---

## What Matters Most

These files are long, and not every rule weighs the same. After the first rule above, when time or attention is short, these come first, in this order; each one caught real defects that a skim of the rest missed.

1. **A name says what the thing is and what it is for.** The reader has nothing else in front of them (below).
2. **Nothing is silent.** No plausible default standing in for a missing fact, no branch that "can't happen", no empty result without its reason, no optional argument that skips a check. `anti-patterns.md` → Silent Staleness, Defensive Programming Inside the Boundary, An Optional Argument That Skips a Check.
3. **Things live with what they belong to.** A component's constants, builder and settings sit in its own module; the entry point only wires them together (below).
4. **Code to the contract you have.** Once an interface exists, nothing outside its implementation names the implementation (below).
5. **A required value is required where it is declared.** Not optional in the schema and checked somewhere later.
6. **The file reads top-down as a story.** Newspaper order, blank lines between concepts, and the main line of each function visible through its bookkeeping (`refactor-guide.md` → Separate the signal from the noise).
7. **Comments carry only the why** (below).

---

## Names Carry Purpose

A name is the reader's only context. It says what the thing is and what it is for, so a reader never has to find where it was built to know what it does. A mechanism especially: a semaphore capping runs is `concurrent_runs_limit`, not `runs`; the stack that closes everything is `shutdown_stack`, not `stack`. No cute, pronoun or fragment names that make sense only in the conversation that wrote them (`theirs()`, `telling`, `Talks`). And one name, one meaning: a value that stands for two roles (the operator who gets errors, and one of the users) is two values.

The test: read the name cold, with nothing else on screen. Would you know what it holds or does?

---

## Cohesion: What Belongs Together Lives Together

Everything about one concern lives in one package: its constants, timeouts, settings, defaults, errors, and the code that builds it. The package builds itself through one door, its own opener or factory, and a caller only decides *whether* to use it and calls that door. The caller never knows what is behind it, because nothing the caller does depends on it.

The payoff is that a concern can be understood, changed, swapped or deleted in one place, and every file reads as one subject. The test: to understand or change X, do you open one package? If X's timeout sits in the entry point, its defaults in a shared config module and its builder in a helpers file, the answer is no, and the next change to X will miss one of them.

Centralizing is the same idea from the other side: each fact comes from one place and reaches a component by one route. A value arriving from two places makes a reader stop and ask which one is real.

This is information hiding (Parnas) applied to where code sits, not only to what an interface exposes. The composition root below is its most visible case.

---

## The Entry Point Is a Composition Root

The entry point wires the process together and owns nothing specific. It picks which components run; each component builds itself. A component's constants, timeouts, builders and settings live with that component, so adding, changing or removing one touches one package, and the entry point reads as a table of contents: one line per step, a verb that says what each step is. The test: could you remove a component by deleting its package and one line in the entry point?

---

## Code to the Contract You Have

Once an interface exists (a protocol, a base class, a plugin contract), everything outside its implementation reaches it through the interface: a list of registered entries, looked up by name, never a concrete class or constant scattered through the callers. When the same concrete name appears in many places around an interface that was meant to hide it, the interface is decorative, and the second implementation will cost a rewrite. The variation belongs in data: one entry per implementation, in one list, next to where the implementations are made.

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
- **Invents a justification the code doesn't need, or states cause and effect backwards.** A made-up rationale is worse than no comment — it misleads. For example, `# the email channel is enabled, so it's added here` reverses cause and effect — the channel *becomes* enabled *because* it's added to the list. The honest version states the line's actual effect: `# only channels added here are enabled`. If an effect isn't obvious, say plainly what the line *does* or *enables*; never reverse-engineer a story to make it sound intentional. A wrong comment costs more than a missing one.

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

A config reader that also bakes in defaults braids together "where the value comes from" with "what we do without one" — two things that change for different reasons. Split them and each side stays obvious: the boundary is a thin retrieval surface; the policy lives where the concern is actually understood. This is `Parse, don't validate` applied to configuration — parse the environment at the edge, decide policy in the interior. A value the program cannot run without is the exception: it is required at the boundary, in the schema that declares it, and its absence stops the program there, beside every other missing value, rather than surfacing as "not set" for someone downstream to check.

---

## Side Effects Resolve Once

A read that *does something* — warns on absence, emits a metric, logs a fallback — should resolve **once**, at a boundary (startup, construction), not re-run on every call. Re-reading a value is cheap and harmless; re-warning is per-call noise that trains operators to ignore the signal.

Separate "what is the value" (repeatable, side-effect-free) from "announce the state of it" (once). Resolve the configuration when the component is built; reuse the resolved result for each request. The warning fires at startup, where a human sees it — not buried in every log line for the lifetime of the process.

---

## Built for Humans and Agents Together

The paradigm has shifted: most of the work in a repository is now done by AI coding agents, often several at once, with a human directing and reviewing. Humans remain the first audience — a repo a person cannot follow is broken no matter how well an agent fares in it. But a repo that only a person can work in, because the context lives in someone's head or in a chat, is broken too. **Agent readiness** is the second audience, designed for on purpose wherever it costs little.

What it means in practice:

- **The repo explains itself.** One entry file for agents (`AGENTS.md`), a file that says where things stand right now, a map of what to read for which task. Decisions carry their why. Nothing load-bearing lives only in a conversation. A fresh agent — or a fresh human — orients from the repo alone and never asks for a recap.
- **Work is handed over as a brief, not a chat.** A task for an agent names every document, rule, and definition of done it must satisfy, and carries no secret. If the brief needs a key pasted in, the brief is wrong.
- **Isolation by one command.** Anything two agents would collide on — a database, a port, a cache, an environment file — has a single command that gives a checkout its own private copy, and one that takes it away. When a new shared thing appears, ask: what does a second agent on this collide with, and what one command removes it?
- **Verification by one command.** One command is the definition of green — format, lint, types, boundaries, tests. An agent proves its work the same way a human does, and a supervisor never has to guess whether a report is true.
- **Deliberate conventions are written down.** An agent applying standards must be able to tell a deliberate deviation from accidental cruft (the two-step rule). What is chosen on purpose is named where the agent will find it; what is not named is fair game to fix.
- **Review happens in the code.** An agent's report is an input, never the verdict. Someone — a human or a supervising agent — reads the diff against the brief and runs the checks. Agents drift like any new colleague; the discipline that catches it is the same.

The test: could two agents and a human work on this repo in the same hour, from the repo alone, without stepping on each other or asking anyone what the rules are? Where the answer is no, that is the next thing to fix — with judgment about cost, not as dogma.

---

## Philosophical Foundations

The mental models behind the standards. Internalize them — they guide the decisions the rules don't cover.

- **Newspaper metaphor** (Uncle Bob) — A file reads top-to-bottom: headline first, details last. Caller above callee. The reader should never scroll up to understand what they just read.
- **Deep modules** (Ousterhout) — A good module does a lot behind a simple interface. Don't split for the sake of splitting — splitting multiplies interfaces and forces readers to bounce. Pragmatic function length follows from this.
- **Simple over easy** (Hickey) — Easy means familiar. Simple means fewer entanglements. Choose simple — even when it requires learning something new. Avoid complecting (braiding together) separate concerns.
- **Functional Core / Imperative Shell** (Bernhardt) — Decisions are pure functions. Effects are thin wrappers. This makes the hard parts trivially testable and the effectful parts trivially simple.
- **Parse, don't validate** (King) — Transform unstructured input into typed, branded values at the boundary. Once parsed, the type system guarantees correctness — no runtime checks needed downstream.
- **YAGNI** (Jeffries, Extreme Programming) — You aren't gonna need it: build what is needed now, never what might be. The first rule's first question, at the scale of a feature.
- **Duplication over wrong abstraction** (Metz) — Three similar functions are better than one premature abstraction. Wait until the pattern is clear. The cost of the wrong abstraction compounds; duplication is cheap to fix later.
- **Semantic compression** (Muratori) — Don't design abstractions upfront. Write the code, see the patterns emerge, then compress. Abstraction is the last step, not the first.
- **Make the change easy, then make the easy change** (Beck) — Refactor first to make the feature trivial to add, then add it. Two small steps beat one complex step.
- **Code as narrative** (Knuth) — Code is read far more than written. Ordering, naming, and structure serve the reader's comprehension, not the writer's convenience.
- **Ubiquitous language** (DDD) — Names mirror the business domain. `TaskEngine`, `PipelineStage`, `TriggerEvent` — not `ItemProcessor`, `StepExecutor`, `IncomingData`.
- **Do one thing well, compose** (Unix) — Small, focused modules with standard interfaces. Composition over inheritance. Pipelines over monoliths.
- **Proximity and chunking** (Gestalt) — Related code stays together. Visual grouping (blank lines, sections) guides the eye. The reader's brain chunks what's close — use that.
- **Explicit over implicit** (Zen of Python) — Be obvious. No magic, no clever indirection where a plain construct works. If a reader has to guess, the code is unclear.
- **Errors should never pass silently** (Zen of Python) — Catch what you can handle; let the rest bubble. Swallowing an error you can't handle is a betrayal of the next person to debug it.
