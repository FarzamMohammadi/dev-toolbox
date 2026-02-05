---
name: work-diary
description: Create a work diary entry from session context. Use when user wants to document work, learnings, or decisions from a session.
argument-hint: [diary-path] [context sources] (e.g., "@../work-diary commits 8b8bf6b..2dfe130", "@../work-diary @thoughts/shared/")
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
disable-model-invocation: true
context: fork
---

# Work Diary

Create portable diary entries that capture your growth as an engineer—intentions, decisions, tools, and learnings—without proprietary or company-specific details.

## Core Principle: Signal Over Noise

Your job is to **distill**, not document. Every line must earn its place.

- **"So what?" test**: Every line should answer "why does this matter?"
- **Outcomes over process**: "Improved X from A to B" not "First did X, then Y, then Z"
- **Consolidate related work**: 3 commits toward one goal → 1 outcome statement
- **Skip internal corrections**: If you added then removed something, just show the final state

## Setup

Ensure year directory and month file exist (safe to run multiple times):

```bash
YEAR=$(date +%Y)
MONTH=$(date +%B | tr '[:upper:]' '[:lower:]')
mkdir -p "${YEAR}" && [ -f "${YEAR}/${MONTH}.md" ] || printf "# %s %s\n\n" "$(date +%B)" "${YEAR}" > "${YEAR}/${MONTH}.md"
```

## Step 1: Gather Context

Read context sources specified by user:
- Current conversation (tickets, specs, research, implementation)
- Files or paths they point to
- Any context they provide directly

**For multiple sources** (tickets, commits, research docs):
- Read all sources before writing—don't start the entry mid-research
- Group by theme or outcome, not by ticket number (related work → one thematic entry)
- For large contexts, consider launching parallel Explore agents to gather efficiently

**Use AskUserQuestion when:**
- Context sources are ambiguous or incomplete
- Unsure what the main intention or goal was
- Need clarification on which decisions were most significant
- Want to capture something the user hasn't mentioned

## Voice & Attribution

**Critical rule: Never speak for the user.**

- Only include content that exists in the provided context (documents, commits, conversation)
- Never invent reflections, opinions, feelings, or personal statements
- If it wasn't documented or explicitly stated by the user, don't include it
- Omit sections entirely rather than filling them with invented content

| Do This | Not This |
|---------|----------|
| "Improved defense rate from 80.2% to 99.6%" (factual, from docs) | "Strong onboarding experience" (invented feeling) |
| "Open question documented: how to keep test suite current" (if in source) | "Open question: ..." (invented by Claude) |
| Skip the Reflections section if nothing documented | Add reflections Claude thinks the user might have |

**When in doubt**: Use AskUserQuestion to ask "Any reflections you want to capture?" rather than inventing them.

## Step 2: Extract Portable Insights

Strip proprietary details. Keep what makes you a better engineer.

| Keep (Transferable) | Omit (Company-Specific) |
|---------------------|-------------------------|
| Why you made decisions | Proprietary business logic |
| Problem-solving approaches | Specific code implementations |
| Tools & technologies used | Internal API/system details |
| Patterns & techniques learned | Credentials, keys, secrets |
| Challenges and how you overcame them | Customer/client information |
| Skills developed | Internal process names |

**Think**: "Could I put this on a resume, share it in a blog post, or discuss it in an interview?" If yes, include it.

## Anti-Patterns: Process vs Outcomes

| Don't Write (Process) | Write Instead (Outcome) |
|-----------------------|-------------------------|
| "Phase 1: Did X. Phase 2: Did Y. Phase 3: Did Z" | "Implemented X across the system" |
| "Before XML: 59%. After XML: 64%. After Pydantic: 92%" | "Improved defense rate: 59% → 92%" |
| "Removed defense from sub-agent (was incorrectly added)" | *(omit—internal correction, not insight)* |
| "Used Pydantic `Field(max_length=250)`" | "Added input validation to constrain LLM outputs" |
| "Changed `prompt.py`, `agent.py`, and `config.py`" | "Refactored prompt injection defense layer" |
| 6 bullets listing each step taken | 2-3 bullets describing what changed |

## Step 3: Write Entry

Target file: `YYYY/month.md` (e.g., `2026/january.md`)

**Append** entry to the month file using this format:

```markdown
---

## [YYYY-MM-DD] - [Brief Title]

### Intention
[What I set out to accomplish and why]

### What Changed
[Outcomes—what's different now? Not steps taken.]

### Decisions & Rationale
[Key choices and reasoning - focus on the "why"]

### Tools & Techniques
[Technologies, patterns, approaches used]

### Learnings
[New insights, skills, patterns discovered]

### Reflections
[Optional: challenges, open questions, next steps]
```

**Guidelines**:
- **Outcomes, not steps**: describe what changed, not what you did
- Keep entries scannable (bullets over prose)
- Multiple entries per day are fine - just append
- Title should capture the essence in 3-7 words
- **Skip sections that don't apply** - never add filler or forced content
- **Use creativity** - the template guides, it doesn't constrain. Add sections that fit, drop ones that don't, rephrase headings if it reads better

## Output

After writing, confirm:
```
Entry added to YYYY/month.md

## [Date] - [Title]
[First 2-3 lines of entry...]
```

## Template Reference

See [assets/template.md](assets/template.md) for detailed section guidance.
