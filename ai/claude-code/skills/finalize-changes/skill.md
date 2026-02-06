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

You know this code — you built it. Use that knowledge. Don't scan; *think*.

### Hindsight

1. **You have full context now.** Research, plan, implementation — use hindsight. What would you do differently if starting over?
2. **Challenge the first solution.** The first thing that worked isn't always the best. Was there a simpler, clearer, or more robust way?

### Absence Over Presence

3. **Hunt for what's missing.** Gaps are harder to see than bugs — missing tests, unhandled paths, undocumented assumptions.
4. **Broken code is obvious. Incomplete code ships quietly.** Look for the quiet gaps.

### Intent

5. **Everything should reveal its purpose to a stranger.** Every name, function, and structure. If it needs explanation, it needs rewriting.
6. **Code communicates.** Does this code say what it means?

### Honesty

7. **You know where you cut corners.** Go back to those spots first.
8. **Don't manufacture findings.** If it's solid, say "this is solid."

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
