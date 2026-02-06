---
name: review-pr
description: Deep-review all changes in a branch for bugs, race conditions, security issues, gaps, and inconsistencies. Use when user wants to scrutinize a PR or branch diff.
allowed-tools: Bash, Read, Grep, Glob
argument-hint: <branch-name>
context: fork
---

# PR Review

Scrutinize every change introduced in a branch. Read the actual files — not just diffs — to understand the full context each change lives in.

## Step 1: Gather

```bash
git log --oneline main..<branch>
git diff --stat main...<branch>
```

For each changed file, read the **full file** on the branch (`git show <branch>:<path>`). Diffs alone hide surrounding context that reveals bugs.

## Step 2: Analyze

Review every file against these principles. Think like an adversary trying to break the code, and a maintainer who has to live with it.

### Concurrency & Shared State
- Mutable state on singletons or module-level variables shared across requests
- TOCTOU races (check-then-act without atomicity)
- Data structures that lose entries under concurrent writes (e.g., dict keyed by name when duplicates are possible)

### Security
- Unvalidated redirects, unescaped user input, injection vectors
- Auth checks that reference fields/roles that don't exist on the model
- Tokens or secrets logged, leaked in URLs, or stored insecurely
- Missing size/rate limits on endpoints accepting raw input

### Error Handling & Resilience
- Swallowed exceptions that silently lose data with no alerting
- Streams or generators that can't emit a terminal event on failure
- Missing input validation that turns 400s into 500s
- No timeouts on external calls — can a hang propagate indefinitely?
- Asymmetric error handling between parallel code paths (one raises, the other swallows)

### Consistency & Correctness
- Naming drift across modules (singular vs plural, different defaults for the same concept)
- Scope or config values that don't match between producer and consumer
- Suppression logic that's too broad (e.g., a flag set once that blocks all subsequent output)
- Attribute access via `hasattr`/`getattr` that silently degrades when the attribute is simply missing from the model

### Resource Management
- Connections, clients, or registries instantiated per-call instead of reused
- No cleanup on client disconnect (generators that keep running)
- Missing heartbeats/keep-alives on long-lived connections

### Configuration & DX
- Feature flags or env vars required at runtime but absent from `.env.sample` or docker-compose
- Port mappings that disagree with CORS config
- Build artifacts committed despite `.gitignore` (tracked before the ignore rule was added)

### Dependencies & Packaging
- Unused production dependencies (installed but never imported)
- Dev-only packages listed as production dependencies
- Peer dependency ranges that exclude current major versions

### Test Coverage
- New modules with zero test files
- Critical paths (coordination methods, streaming loops, DB writes) with no coverage
- Error paths wrapped in try/except but never tested
- Placeholder tests that contain only `pass`

## Step 3: Output

Write findings to `<TICKET-OR-BRANCH>-REVIEW-FINDINGS.md` at the repo root.

### Tone
Write as open-ended review comments — not assertions. Ask questions:
- "Could this happen if two requests arrive simultaneously?"
- "Is this intentional, or would this bypass the role check?"
- "Worth checking whether this silently drops data when the DB is down"

### Format
Organize by severity: **Critical > High > Medium > Low**, then a **Test Coverage Gaps** table. Each finding gets a short title, `file:line` reference, and open-ended description.

### Rules
- Every `file:line` reference must be verified against the actual code — re-read before citing
- Organize by severity: Critical > High > Medium > Low
- Include a test coverage section even if the rest is clean
- If nothing is found, say so — don't invent issues
