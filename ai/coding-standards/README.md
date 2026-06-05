# Coding Standards

Centralized coding standards and refactoring approach, referenced from any repository.

## How to Use

Every session, start by pointing the agent at the refactor guide **first**, then the language standards:

```
Please read:
  ~/Documents/Repos/dev-toolbox/ai/coding-standards/refactor-guide.md
  ~/Documents/Repos/dev-toolbox/ai/coding-standards/philosophy.md
  ~/Documents/Repos/dev-toolbox/ai/coding-standards/python/coding-standards.md
  ~/Documents/Repos/dev-toolbox/ai/coding-standards/python/anti-patterns.md
```

The refactor guide is the **mode** — how to work collaboratively, when to push back, what earns its place. `philosophy.md` is the **values** — the language-agnostic principles to internalize (comments, idiom over transliteration, the philosophical foundations). The language files are the **patterns** — what good code looks like in that language. Without the guide, the standards become a mechanical checklist. With it, they become tools used with judgment.

## The Two-Step Rule

These standards are the *target*. The codebase's existing patterns are the *starting point*. Before applying:

1. **Learn the patterns already in place.** Read enough of the repo to understand its conventions. Some of them will be deliberate and worth preserving — even when they differ from these standards.
2. **Propagate the good. Replace the bad.** Deliberate conventions that aid readability, maintainability, and evolution stay. Accidental cruft or harmful patterns get replaced with what's here. Never propagate garbage just because it exists; never overwrite deliberate choices just because the standard says otherwise. Judgment first.

If a project's convention deliberately deviates from these standards, that's a decision worth surfacing — but not silently overriding.

## Structure

```
coding-standards/
  refactor-guide.md      ← the mode: how to run a session
  philosophy.md          ← the values: language-agnostic principles + foundations
  <language>/
    coding-standards.md  ← positive rules: how to write code well
    anti-patterns.md     ← negative rules: what looks productive but hurts
```

Each language has its own folder. The cross-cutting values (comment philosophy, the philosophical foundations) live once in `philosophy.md`; the language files reference it rather than restating it. Anti-patterns are largely language-agnostic (YAGNI, cargo-culting, silent decisions) but each file appends a language-specific section.

## Supported Languages

- `typescript/` — TypeScript, including Zod, Node.js async discipline, and strict compiler usage.
- `python/` — Python, including type hints (no `Any`), pydantic/dataclasses, asyncio, and ruff.

## Philosophy

These standards are strong defaults, not absolute laws. Apply with judgment, never mechanically. The cross-cutting principles and philosophical foundations in [`philosophy.md`](philosophy.md) are what to internalize — the language rules are how those foundations look in practice for that language.

When a rule and clarity collide, the application is wrong, not the rule. Find what an experienced engineer would naturally write that still honors the intent.
