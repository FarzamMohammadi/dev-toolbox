---
name: finalize-changes
description: Holistic review of completed work to elevate quality from good to excellent. Use after implementation is done to catch what was missed.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [file or directory paths]
---

# Finalize Changes

You finished the work. Now finish it *properly*.

This is the craftsman's final pass—the review you do after everything works, tests pass, and you think you're done. The gap between "works" and "excellent" lives in the details this pass catches.

## Core Principle: Fresh Eyes on Familiar Work

You built it, so you're blind to it. Fight that blindness:

- **Read as a stranger** — someone seeing this for the first time tomorrow
- **Question every choice** — "is this the best way, or just the first way that worked?"
- **Hunt for what's absent** — missing tests, unhandled edges, unclear names are harder to spot than broken code

## Step 1: Gather Scope

Identify all files changed in this session:

- If paths provided as arguments, use those
- Otherwise, use `git diff --name-only` against the base branch or recent commits
- **Read every changed file completely** — no skimming

## Step 2: Deep Review

Analyze each dimension. **Skip dimensions that don't apply.**

| Dimension | What to look for |
|-----------|-----------------|
| **Correctness** | Edge cases, off-by-ones, null paths, race conditions, error propagation |
| **Naming** | Does every name reveal intent? Would a stranger understand without context? |
| **Structure** | Right abstractions? Functions doing one thing? Clear data flow? |
| **Consistency** | Does new code match existing patterns, conventions, style? |
| **Simplicity** | Over-engineering? Unnecessary abstractions? Could anything be removed? |
| **Completeness** | Missing tests? Missing error handling? Gaps in coverage? |
| **Edge cases** | Empty inputs, boundaries, concurrent access, failure modes |
| **Documentation** | Do comments explain *why*, not *what*? Any stale comments left behind? |

**The test for each finding**: "Would I be embarrassed if a senior engineer reviewed this?"

## Step 3: Report

Present findings **before** making changes:

```
## Refinement Review

**Scope**: [N files reviewed]

### Findings
1. **[Dimension]** `file:line` — [specific issue] → [specific fix]
2. **[Dimension]** `file:line` — [specific issue] → [specific fix]
...

### Assessment
[One sentence: how close to done, what's the biggest gap]
```

**Rules for findings:**
- **Specific, not vague** — file, line, exact problem
- Each finding must have a **concrete fix**, not a suggestion to "consider"
- Order by **impact** — biggest improvements first
- If nothing meaningful found, say so — don't invent issues

## Step 4: Apply

After presenting findings and getting confirmation, apply the fixes:
- Make each edit
- Briefly confirm what changed

## Rules

- **No cosmetic-only changes** — reformatting or reordering imports don't count
- **No scope creep** — review what was built, don't redesign it
- **Substance over volume** — 3 real findings beat 10 nitpicks
- **Be honest** — if the work is solid, say "this is solid" and move on
