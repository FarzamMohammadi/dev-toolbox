---
name: create-pr-description
description: >-
  Author a comprehensive, reviewer-ready pull request or GitLab merge request description from the
  current branch's changes and the working session's context, saved to an isolated temp file. Use
  this whenever someone is wrapping up a piece of work and needs the writeup — phrasings like "write
  the PR description", "draft the PR/MR", "create a pull request description", "describe these changes
  for review", or finishing a branch before opening a merge request. The skill's edge is that it
  carries the reasoning the diff can't show — why this approach, the root cause behind a bug, the
  decisions and rejected alternatives, scope and follow-ups, related tickets, and how this PR fits a
  multi-PR effort.
allowed-tools: Read, Bash, Write, Edit, AskUserQuestion
argument-hint: "[optional: base branch, ticket, or framing notes]"
---

# Create PR Description

You are turning a finished (or near-finished) branch into the description a reviewer reads first.
This works for a GitHub PR or a GitLab MR — "PR" below means either.

## The one idea that matters

A diff already shows **what** changed, line by line. Nobody needs you to narrate it back. Your value
is everything the diff *can't* carry: **why** this approach and not the obvious alternative, the root
cause behind a bug, the decision that was made in conversation and left no trace in the code, what's
deliberately out of scope, which ticket this serves, how this PR connects to its siblings. Spend your
words there.

## Structure is emergent — do not impose a template

There is no fixed skeleton. The right shape comes from *this* change and *this* session. If the work
was a bug, "context behind the bug → its cause → the fix" is often the natural grouping — because
that's the story this change tells. A refactor, a migration, a new feature, a config tweak, a
dependency bump each want a different shape, and a one-line fix wants one sentence with no headings at
all.

So the actual skill is a way of thinking, run every time:

1. **What are the critical details a reviewer must walk away with?** (Not all details — the load-bearing ones.)
2. **How do these details group?** What's the through-line that makes them make sense together?
3. **How do I deliver that concisely *and* effectively** — short enough to read, complete enough to approve?

Let the answers pick the sections. Calibrate depth to stakes: a typo fix gets a sentence; a risky
migration earns scope, rollout, and risk. Empty section headers on a small PR are noise; stripping a
complex one to one line hides the very context you exist to surface. Use judgment, not a checklist.

## Phase 1 — Gather

Completeness is the whole game here. A change you never loaded into context is one you can't
describe — and worse, one a reviewer will assume was covered when it wasn't. Do not sample, do not
describe only the latest commit, do not trust `--stat` (it shows line counts, not content). Work
through these steps until every change is accounted for.

**1. Pin the base branch correctly.** The base (what this merges into) defines the whole change set;
get it wrong and you either miss commits or describe unrelated ones. Detect, fall back, and *confirm
with the user if there's any doubt* — a wrong base is the single biggest way to silently miss or
over-include work. A stale local base also distorts the diff, so fetch when you can.

```bash
git fetch --quiet 2>/dev/null   # refresh the base so the comparison isn't stale (skip if offline)
base=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
echo "detected base: ${base:-<none — try main / master / develop, or ASK the user>}"
```

**2. Establish the complete change set — and make it an explicit list.** Capture both what's
committed *and* what isn't, because they fail differently:

```bash
git log --oneline   "${base:-main}"..HEAD     # every commit on the branch — the narrative (not just HEAD)
git diff --name-status "${base:-main}"...HEAD  # every committed file, with A/M/D/R status
git status --short                             # staged, unstaged, AND untracked (?? ) work
```

- The committed list (`name-status`) is your **coverage target**: the count of files you must read.
- `git status` catches work that is *not in any commit* and would therefore be **left out of the PR
  entirely**. If anything shows up there, surface it and ask whether it belongs in this PR before
  proceeding — silently ignoring it is how half-finished work ships or gets forgotten. The user just
  "finishing" often means uncommitted changes still sit in the tree.

**3. Read every changed file's actual diff — all of it.** Not the stat, not a sample, not just the
files that look interesting:

```bash
git diff "${base:-main}"...HEAD                 # the full committed diff; page through large output
git diff "${base:-main}"...HEAD -- <path>       # or go file-by-file using the name-status list as a checklist
```

For a large branch, walk the `name-status` list and read each file's diff in turn, ticking it off, so
none is skipped. Account for the awkward shapes the eye glosses over: **deletions and renames** (real
changes even with little content), **binary files** (`git diff` only says "Binary files differ" — note
them), and **generated/vendored/lockfiles** (read enough to confirm they're mechanical, then say so
rather than narrating them). Ground every claim you make in a hunk you actually saw — an unverified
rationale is worse than silence.

**4. Reconcile before you write.** Cross-check your understanding against the `name-status` list: every
file is either reflected in what you'll write or a conscious "not worth mentioning" (e.g. a lockfile).
If you can't say what a file's change was *for*, you haven't finished gathering — go back and read it.

**5. Mine the session — this is the skill's superpower.** The conversation you're in usually holds the
parts that never reach the code: why an approach was chosen over another, the actual root cause of a
bug (vs. its symptom), a deliberate scoping call, the ticket IDs, the fact that a sibling PR carries
the other half. Harvest all of it. If a reason was real in the session and won't survive in the diff,
it belongs in the description.

**6. Collect the connective tissue:** related ticket(s), and any sibling PRs (e.g. a
backend/frontend/infra split sharing one ticket).

## Phase 2 — Compose

Write the description the change earned. Lead with what a reviewer needs first. Draw from this menu
only where it applies — these are candidates, not required sections:

- The problem or motivation (what prompted this)
- For a bug: the **root cause** and the context behind it — why it happened, not just where
- What changed, at the level of intent — high-level, never a line-by-line tour
- Why this approach: the decision, and the alternatives considered and rejected
- Scope: what's deliberately *not* here, and the follow-up that picks it up
- Operational reality: config, migrations, feature flags, deploy ordering, rollback
- Testing: what was run, or how a reviewer can verify
- Related tickets and links

**Multi-PR coordination.** When the work spans more than one PR (split by repo, by layer, or just by
size), open with a short block at the very top so whoever lands on any one PR sees the whole effort
and where to start. Hypothetical:

```markdown
**Part of a 2-PR change — start review here (backend).**
- Backend (this PR): <link>
- Frontend (retry UX + toast): <link>
- Ticket: PAY-1234
```

**Voice and economy.** First person singular — "I", not "we" (one author did this; reserve "we"
only for the genuine team/org). Formal, plain prose. Cut every line that just restates the diff or
pads a section to look thorough. Brevity is a feature; it's what gets the PR actually read.

### A worked hypothetical (illustrative shape, not a mandate)

This shape emerged because the work was a bug split across two PRs. Yours will differ.

```markdown
**Part of a 2-PR change — start review here (backend).**
- Backend (this PR): <link>   ·   Frontend (retry UX): <link>   ·   Ticket: PAY-1234

## Issue
Customers were occasionally charged twice when the checkout request timed out and the client retried.

## Root cause
The idempotency key was generated per HTTP attempt instead of per checkout session, so a retry
produced a fresh key and the gateway treated it as a new charge. The timeout was the trigger; the
key's scope was the actual bug.

## Fix
I moved idempotency-key generation up to the checkout session and persisted it, so every retry of the
same checkout reuses the key. Scoped to the payment service — client retry behavior is unchanged and
handled in the frontend PR.

## Scope
Out of scope: the retry-budget rework (PAY-1240). This PR stops the double charge; that one tunes how
aggressively clients retry.

## Testing
Added a regression test that replays a timed-out attempt and asserts a single gateway charge; manually
verified against the gateway sandbox.
```

## Phase 3 — Save (don't post)

Keep the artifact isolated, the same way sibling workflow skills do:

```bash
mkdir -p .claude/temp/create-pr-description
```

Write to `.claude/temp/create-pr-description/<branch-or-ticket>.md`, then present it for review and
iterate until it's right.

Do **not** open or push the PR yourself unless explicitly asked — this skill produces the writeup;
posting is a separate, deliberate step (hand the file to the relevant tool, e.g. `gh pr create` or the
`glab-mr-manager` skill). Producing the description and publishing it are different decisions, and the
author owns the second one.
