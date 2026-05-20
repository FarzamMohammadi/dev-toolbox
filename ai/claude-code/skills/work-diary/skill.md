---
name: work-diary
description: Write a work diary entry. Use when the user wants to document work, learnings, reflections, or decisions — any time they say "diary", "entry", "document this", or "write this up."
argument-hint: [diary-path] [context sources] (e.g., "@../work-diary commits 8b8bf6b..2dfe130", "@../work-diary @thoughts/shared/")
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
context: fork
---

# Work Diary

Write diary entries that capture the user's engineering life — what they built, why it mattered, what they learned, and how they felt about it. This is a personal archive: resume-ready raw material, a record to look back on in 5 years, and a defense against forgetting the cool things they did.

## Core Principles

**Story over spec.** Write like you're telling a friend what happened — the problem, the journey, the decisions, the outcome. Not a technical report. Not a changelog.

**Preserve the journey.** The debugging path, the wrong turns, the "aha" moment — that's what makes entries worth reading. Don't collapse the messy middle into a clean outcome statement.

**Personal and honest.** This is a diary. Include the human side — what was frustrating, exciting, satisfying, or embarrassing. A diary entry that reads like a PR description has failed.

**Every line earns its place.** Detail is good when it's story and insight. Detail is noise when it's function signatures, file paths, error code constants, or Prisma enum names. If a reader needs the codebase open to understand a line, cut it.

## Setup

Ensure year directory and month file exist (safe to run multiple times):

```bash
YEAR=$(date +%Y)
MONTH=$(date +%B | tr '[:upper:]' '[:lower:]')
mkdir -p "${YEAR}" && [ -f "${YEAR}/${MONTH}.md" ] || printf "# %s %s\n\n" "$(date +%B)" "${YEAR}" > "${YEAR}/${MONTH}.md"
```

## Step 1: Gather Context

Read everything the user points you at — conversation history, commits, files, whatever they provide. Read all sources before writing. For large contexts, consider launching parallel Explore agents.

**Accept any input.** Current session context, commit ranges, files to read, verbal explanation. No single expected format.

**Group by theme**, not by ticket or commit. If 5 commits serve one goal, that's one entry, not five.

## Step 2: Interview

**Always ask questions before writing.** Every entry gets a short interview — even when context seems complete. Two purposes:

### Fill gaps in the technical story
- What were you trying to accomplish and why?
- What was the hardest part?
- What surprised you?
- Any key decisions that aren't obvious from the code?

### Draw out the personal side
- How do you feel about this one?
- What are you proud of? What frustrated you?
- Anything you'd do differently?
- Any moment that stands out — a breakthrough, a painful mistake, a turning point?

**Keep it light.** 3-5 questions, not an interrogation. If the user waves off a question ("not much to say"), move on. The personal section is optional in the final entry — but the question should always be asked.

### Surface insights for confirmation
When you see patterns, connections, or lessons in the context that the user hasn't mentioned, propose them:
> "I noticed X pattern across these changes — is that a learning worth capturing, or am I reading into it?"

Never silently include proposed insights. Always confirm before writing them in.

## Step 3: Write the Entry

Target file: `YYYY/month.md` (e.g., `2026/may.md`). **Append** the entry.

### Adaptive Format

Pick the structure that fits the content. No rigid template. Here are two examples — use them as starting points, not rules.

**For a shipped project or feature:**
```markdown
---

## [YYYY-MM-DD] - [Title]

### Intention
[What I set out to build and why it mattered]

### The Journey
[What actually happened — the problem, the approach, what broke, what worked.
This is the story, not a list of commits.]

### Key Decisions
[The choices that shaped the outcome and why I made them]

### What I Learned
[Insights, patterns, skills — things I'll carry forward]

### Reflections
[How I feel about it, what I'd do differently, what's next]
```

**For an insight, mistake, or career moment:**
```markdown
---

## [YYYY-MM-DD] - [Title]

### Context
[What happened]

### Insight
[What I learned from it]

### Going Forward
[What I'll do differently]
```

**Guidelines:**
- **Skip sections that don't apply** — never add filler
- **Rename sections freely** — "The Journey" could be "What Happened", "The Debugging Saga", "How It Actually Went" — whatever reads best
- **Add sections that fit** — Results tables, a "What Sucked" section, a "Proud Of" callout — if it belongs, add it
- Title should capture the essence in 3-7 words
- Multiple entries per day are fine
- Bullets over prose for scannability, but prose is fine when telling a story

### Detail Level

| Write This (Story-Level) | Not This (Implementation-Level) |
|---|---|
| "Built server-side validation because AI agents kept fabricating IDs despite being told not to" | "Added `findInvalidId` helper in `utils/id-validation.ts` that detects fabricated IDs" |
| "The auth flow had 5 layers, and I had to understand all of them before the write tool could mirror it correctly" | "`ensureUserCanUpdateRequestStatus` validates trusted callers, self-cancel, internal users, PTO managers, and company admins" |
| "Improved defense rate from 59% to 92% through layered prompt hardening" | "Before XML: 59%. After XML: 64%. After Pydantic: 92%" |
| "Used AsyncLocalStorage for per-request isolation after discovering the global singleton leaked auth between concurrent sessions" | "Request context via `AsyncLocalStorage` — each MCP message gets its own store" |
| "Discovered the model was calling tools in parallel and fabricating IDs because the list result hadn't arrived yet" | "Docker logs showed Gemini calling list and update in the same parallel batch" |

**The test:** Would this detail mean anything to someone (including future you) who doesn't have the codebase open? If yes, keep it. If it only makes sense with the code in front of you, elevate it to the story level or cut it.

### Company-Specific Details

Use judgment, not a blanket filter.

**Keep:** Product names that are publicly known (Alfie, Athena), technologies and frameworks used, the nature of the problem and solution, team dynamics and collaboration moments, metrics and outcomes.

**Omit:** Credentials, keys, secrets. Customer/client data. Internal DB schemas and auth flow internals. Proprietary business logic that's genuinely confidential.

**The interview test still applies:** "Could I discuss this in an interview?" If yes, it's fine. If you'd hesitate, genericize it or cut it.

## Output

After writing, confirm:
```
Entry added to YYYY/month.md

## [Date] - [Title]
[First 2-3 lines of entry...]
```
