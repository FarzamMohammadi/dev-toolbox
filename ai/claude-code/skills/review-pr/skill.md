---
name: review-pr
description: Find bugs in branch changes — races, logic errors, security holes, contract mismatches. Use when user wants to review a PR or branch.
argument-hint: <branch-name>
context: fork
---

# Find Every Bug

Your only job: find real bugs in this branch. Not style issues, not suggestions, not refactoring ideas. Bugs, races, security holes, logic errors, broken contracts.

## Step 1: Scope

```bash
git log --oneline main..<branch>
git diff --stat main...<branch>
```

Collect the list of changed files. Then use Grep across changed files to locate hot spots — mutable state (`self.`, `dict[`, `: dict`), error handling (`try:`, `except`), boundaries (`request`, `endpoint`, `route`). These are where bugs concentrate. Note them for extra scrutiny.

## Step 2: Read

For each changed file, read the **full file** on the branch (`git show <branch>:<path>`). Diffs hide surrounding context that reveals bugs.

**For large diffs (10+ source files):** Split files into groups by domain/directory. Launch parallel Task agents (subagent_type: Explore) — one per group. Each agent reads its files fully and applies Step 3 below. Fewer files per agent means deeper analysis per file. Collect all agent findings for the final report.

## Step 3: Analyze

Work through every file with these lenses. Each one catches a different class of bug.

### State and data structures
- For every dict/map: can the key have duplicates? If yes, what's silently lost on overwrite?
- For every container that accumulates: does it preserve ordering, uniqueness, and all entries under every access pattern?
- For every variable on `self` or at module/class level: who else reads or writes it? What happens under concurrent requests?
- Trace every mutable object from creation through all mutations to final read. Mentally execute what happens after 1 call, 2 calls, N concurrent calls.

### Boundaries
- Every endpoint: size limits? auth? rate limits? What can a caller send to break it?
- Every external call: timeout? What if it hangs, returns garbage, or never responds?
- Every config/env lookup: what if the value is missing or wrong? Is the fallback correct?
- Every auth check: does the field being checked actually exist on the model?

### Failure paths
- Every try/except: what state is left after partial failure? Does the caller see a useful error?
- Parallel code paths: are they handling errors symmetrically, or does one swallow while the other raises?
- Streaming/event code: if it fails mid-stream, does cleanup still run? Does the protocol get a proper termination event?

### Cross-module contracts
- When A calls B: do names, types, defaults, and semantics agree?
- String constants: consistent across all files? (singular vs plural, casing, prefixes)
- Config set in one place, consumed in another: do values match?
- Features declared but unused, or used but undeclared?

Also: are new code paths tested? Are error paths exercised? Are there placeholder tests?

## Step 4: Report

Write findings to `<BRANCH>-REVIEW-FINDINGS.md` at repo root.

Each finding: severity (Critical / High / Medium / Low), short title, `file:line`, what's wrong.
Then a Test Coverage Gaps section.

Rules:
- Verify every `file:line` by re-reading the actual file before citing
- If nothing found, say so — don't invent issues
