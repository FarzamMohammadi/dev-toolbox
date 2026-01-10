Save context and generate handoff prompt to continue seamlessly in the next chat.

## Instructions

Execute the Context Relay Agent to capture and persist all session context:

### Step 1: Capture Session Intelligence

Gather from your memory of this conversation:

**Context Summary:**
- What was the user trying to accomplish? (high-level goal)
- What specific task/project were we working on?
- What's the current state? (in progress, blocked, completed)

**Decisions Made:**
- Key decisions made during this session
- Approaches chosen (and why)
- What we explicitly decided NOT to do

**Learnings:**
- User preferences discovered
- Project/codebase knowledge gained
- Patterns or standards established

**Work Completed:**
- Files created/modified
- What was accomplished
- Current state of each item

**Work Remaining:**
- What's left to do
- Immediate next step
- Any blockers

### Step 2: Update Memory Files

Write to these files in `ai/prompt-engineering/`:

1. **SESSION-STATE.md** - Current state snapshot (overwrite)
2. **MEMORY/session-history.md** - Append session summary with timestamp
3. **MEMORY/learnings.md** - Append new learnings/preferences discovered
4. **MEMORY/decisions.md** - Append decisions made with rationale

### Step 3: Generate HANDOFF-PROMPT.md

Create `ai/prompt-engineering/HANDOFF-PROMPT.md` with a complete starter prompt the user can paste into a new chat.

The handoff prompt must include:
- Project/goal context
- Current state and immediate next step
- Key decisions made
- User preferences (CRITICAL for continuity)
- Memory file paths to reference
- Clear resume instructions

### Step 4: Output Summary

Provide:
1. **Session Recap** - Brief summary of what happened
2. **Files Updated** - List of memory files written
3. **Next Step** - The immediate next action for the new chat
4. **Instructions** - Tell user to copy HANDOFF-PROMPT.md content to start next chat

---

## Key Principle

The next chat should continue **as if it never ended**. The handoff must be comprehensive enough that no context is lost and no re-explanation is needed.
