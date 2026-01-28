---
name: work-diary
description: Create a work diary entry from session context. Use when user wants to document work, learnings, or decisions from a session.
disable-model-invocation: true
argument-hint: [context description or sources]
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
context: fork
---

# Work Diary

Create portable diary entries that capture your growth as an engineer—intentions, decisions, tools, and learnings—without proprietary or company-specific details.

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

**Use AskUserQuestion when:**
- Context sources are ambiguous or incomplete
- Unsure what the main intention or goal was
- Need clarification on which decisions were most significant
- Want to capture something the user hasn't mentioned

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

## Step 3: Write Entry

Target file: `YYYY/month.md` (e.g., `2026/january.md`)

**Append** entry to the month file using this format:

```markdown
---

## [YYYY-MM-DD] - [Brief Title]

### Intention
[What I set out to accomplish and why]

### Work Done
[Concise summary - bullet points work well]

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
