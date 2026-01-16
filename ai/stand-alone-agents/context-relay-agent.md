# Context Relay Agent

> **Purpose:** Seamlessly transfer context between chat sessions so the next chat continues as if it never ended.
> **Trigger:** User says "prepare handoff", "relay context", "end session", or similar

---

## What This Agent Does

When invoked, this agent:
1. **Captures** everything from the current session (learnings, decisions, state, progress)
2. **Writes** to persistent memory files
3. **Generates** a complete starter prompt for the next chat
4. **Ensures** the next chat continues seamlessly - as if it never ended

---

## Agent Instructions

When the user asks to prepare a handoff or relay context to the next chat:

### Step 1: Gather Session Intelligence

Capture the following from your memory of this conversation:

**Context Summary:**
- What was the user trying to accomplish? (high-level goal)
- What specific task/project were we working on?
- What's the current state? (in progress, blocked, completed phase X)

**Decisions Made:**
- What key decisions were made during this session?
- What approaches did we choose (and why)?
- What did we explicitly decide NOT to do?

**Learnings Captured:**
- What did we learn about the user's preferences?
- What did we learn about the codebase/project?
- What patterns or standards were established?
- Any pain points identified?

**Work Completed:**
- What files were created/modified?
- What was accomplished?
- What's the current state of each item?

**Work Remaining:**
- What's left to do?
- What's the immediate next step?
- Any blockers or dependencies?

**Important Context:**
- User preferences discovered (interaction style, coding style, etc.)
- Project-specific knowledge gained
- Technical decisions and rationale
- Anything the next session MUST know

### Step 2: Write to Memory Files

Update the following files with session intelligence:

**File: `ai/memory/session-history.md`**
- Append session summary with timestamp
- Cumulative history across sessions

**File: `ai/memory/learnings.md`**
- Append new learnings discovered
- User preferences, project knowledge, patterns

**File: `ai/memory/decisions.md`**
- Append decisions made with rationale
- Reference for future sessions

### Step 3: Generate Starter Prompt

Create a comprehensive prompt that the user can paste into a new chat to continue seamlessly.

---

## Starter Prompt Template

```markdown
# Session Continuation - [DATE]

## Context
I'm continuing a previous session. Here's everything you need to know:

### Project/Goal
[What we're working on and why]

### Current State
[Where we are right now - what's done, what's in progress]

### Immediate Next Step
[The very next thing to do]

### Key Decisions Made
[Important decisions from previous sessions with brief rationale]

### User Preferences (CRITICAL - Follow These)
[Interaction style, quality expectations, workflow preferences]

### Memory Files to Reference
- `ai/memory/session-history.md` - Latest session state
- `ai/memory/learnings.md` - Accumulated learnings
- `ai/memory/decisions.md` - Decision history

### Important Context
[Anything else critical for continuity]

---

## Resume Instructions

Please read the memory files referenced above, then continue where we left off. The immediate next step is:

**[SPECIFIC NEXT ACTION]**

Treat this as a continuation - no need to re-explain context I've provided. Let's pick up where we left off!
```

---

## Output Format

When invoked, output:

1. **Session Summary** (brief recap of what happened)
2. **Files Updated** (list of memory files written)
3. **Starter Prompt** (complete prompt to paste in new chat)
4. **Quick Resume** (one-liner for simple continuation)

---

## Example Invocation

**User:** "Prepare handoff for next session"

**Agent Response:**

---

### Session Summary

This session focused on creating the Ultimate Prompt Engineering Directory. We:
- Researched industry approaches (CLAUDE.md, MCP, hooks, agents, etc.)
- Captured user preferences (80/20 collaboration, opinionated, etc.)
- Created comprehensive master plan and implementation phases
- Created the Context Relay Agent (this tool)

**Current State:** Planning complete, ready to implement Phase 1

**Next Step:** Create `philosophy/CORE.md`

---

### Files Updated

✅ `ai/memory/session-history.md`
✅ `ai/memory/learnings.md`
✅ `ai/memory/decisions.md`

---

### Starter Prompt for Next Chat

[Full prompt provided here - user copies this]

---

### Quick Resume (Alternative)

> "Continue building the Ultimate Prompt Engineering Directory. Read `ai/memory/session-history.md` for full context. Next step: Create philosophy/CORE.md"

---

## Notes

- This agent should be invoked at natural stopping points
- The more context captured, the better the next session
- Memory files accumulate knowledge over time
- User can invoke with "prepare handoff", "relay", "end session", "prepare for next chat"
