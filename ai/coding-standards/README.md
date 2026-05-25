# Coding Standards

Centralized, language-specific coding standards referenced from any repository.

## How to Use

From any project, point your agent at the relevant language folder:

```
Refactor the files I changed based on:
  ~/Documents/Repos/dev-toolbox/ai/coding-standards/typescript/coding-standards.md
  ~/Documents/Repos/dev-toolbox/ai/coding-standards/typescript/anti-patterns.md
```

Or reference the whole language folder:

```
Follow the conventions in ~/Documents/Repos/dev-toolbox/ai/coding-standards/python/
```

## The Two-Step Rule

These standards are the *target*. The codebase's existing patterns are the *starting point*. Before applying:

1. **Learn the patterns already in place.** Read enough of the repo to understand its conventions. Some of them will be deliberate and worth preserving — even when they differ from these standards.
2. **Propagate the good. Replace the bad.** Deliberate conventions that aid readability, maintainability, and evolution stay. Accidental cruft or harmful patterns get replaced with what's here. Never propagate garbage just because it exists; never overwrite deliberate choices just because the standard says otherwise. Judgment first.

If a project's convention deliberately deviates from these standards, that's a decision worth surfacing — but not silently overriding.

## Structure

```
coding-standards/
  <language>/
    coding-standards.md  ← positive rules: how to write code well
    anti-patterns.md     ← negative rules: what looks productive but hurts
```

Each language has its own folder. Anti-patterns are largely language-agnostic (YAGNI, cargo-culting, silent decisions) but each file appends a language-specific section.

## Supported Languages

- `typescript/` — TypeScript, including Zod, Node.js async discipline, and strict compiler usage.
- `python/` — Python, including type hints (no `Any`), pydantic/dataclasses, asyncio, and ruff.

## Philosophy

These standards are strong defaults, not absolute laws. Apply with judgment, never mechanically. The philosophical foundations at the bottom of each `coding-standards.md` are what to internalize — the rules above them are how those foundations look in practice for that language.

When a rule and clarity collide, the application is wrong, not the rule. Find what an experienced engineer would naturally write that still honors the intent.
