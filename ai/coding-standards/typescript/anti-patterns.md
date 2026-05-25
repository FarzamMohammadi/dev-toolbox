# TypeScript Anti-Patterns

Things that look productive but hurt the project. If you catch yourself doing any of these, stop and reconsider.

These are language-agnostic in spirit — they apply to any codebase — but the examples and idioms here speak TypeScript. The Python and other-language versions mirror this list with language-appropriate examples.

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

## TypeScript-Specific

### Escaping the Type System

`any`, `as unknown as Foo`, `@ts-ignore`, `@ts-expect-error` without justification. Each one disables the compiler's ability to help you. If you cannot type something correctly, that's a signal to redesign — not to silence the warning. The only legitimate uses are at unparseable boundaries, and even those should narrow to a real type within one or two lines.

### Defensive Programming Inside the Boundary

Re-validating data five layers deep that was already validated at the boundary. If `parseTaskInput` returned a `CreateTaskInput`, downstream code does not need to check `if (input.title)` again — the type already proves it exists. Defensive checks inside the boundary are a sign the boundary doesn't trust itself. Fix the boundary instead.

### Throwing for Expected Failures

Throwing exceptions for outcomes the caller is supposed to handle — "user not found", "rate limited", "validation failed". These are expected outcomes that should appear in the return type as a Result/discriminated union, not surprise the caller via stack unwinding. Throw only for invariant violations and bugs.

### Mocking Internals in Tests

Mocking another module's functions to test the current one. This couples tests to internal structure — refactors break tests that should still pass. Mock only at the system boundary (network, filesystem, time, external services). Internal collaboration is tested by calling the real code with real data.

### Re-Exporting Through Barrels Internally

A module's own files importing from its `index.ts` create circular-import risks and obscure the actual file dependency graph. Barrels are for *consumers*. Internal files import siblings directly.

### Floating Promises

`doSomethingAsync()` without `await` and without `.catch()`. Silent failure waiting to happen. If it's fire-and-forget on purpose, the `.catch()` is the documentation that it was deliberate.

### Type-Only Drift

Declaring a Zod schema and a TypeScript interface that are *supposed* to match but are maintained independently. They will diverge — guaranteed. Infer the type from the schema (`z.infer<typeof Schema>`) and have one source of truth.

### Unnecessary Abstraction

Wrapping a single library call in a "service" or "client" abstraction that adds no behavior. A `UserService` whose only method is `return db.users.findById(id)` is friction with no payoff. Wait for at least three call sites and a clear policy (logging, retry, transformation) before abstracting.

### Util Junk Drawers

Files named `utils.ts`, `helpers.ts`, `misc.ts`, `common.ts`. These attract unrelated code and become uncategorizable graveyards. Every function belongs to a concept — move it there. If you can't name the concept, the function probably shouldn't exist yet.

### Deep Utility-Type Chains

```typescript
// Smell — the source type is the wrong shape for this use case
type DraftTaskInput = Partial<Omit<Pick<Task, "title" | "repo" | "source" | "phase">, "phase">>;
```

One layer of `Pick`/`Omit`/`Partial` to derive a related shape is fine. Two or more layers means you're modeling a distinct concept poorly — give it a name and define it directly (or derive it from a schema). Chained utility types are a maintenance hazard: the chain says nothing about *what* the type represents, and changing the source type produces inscrutable downstream errors.

### `as` to Silence Type Errors

`as Foo` (and worse, `as unknown as Foo`) lies to the compiler. The runtime value may not match the asserted type. Reach for `satisfies` for literal validation, type predicates / `asserts` for narrowing, or a real parse step at the boundary. `as` is acceptable only when you genuinely know more than the compiler — and that should be rare and commented.
