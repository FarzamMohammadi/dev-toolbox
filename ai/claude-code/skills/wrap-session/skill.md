---
name: wrap-session
description: Wrap up a session by capturing context, decisions, and state into project-native documentation, then generate a continuation prompt for the next chat. Use when ending a session, switching context, or preparing a handoff.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [optional focus or notes]
---

# Session Wrap

Capture the current session's context and produce two things:
1. **Persistent documentation** — updated or created in the project's own style
2. **A continuation prompt** — a self-contained message that lets the next chat pick up exactly where this one ends

---

## Philosophy

You are intelligent. Don't follow a rigid template — **think about what matters** for this specific session and project. The goal is: if someone opens a fresh chat tomorrow with zero context, what do they need to seamlessly continue?

---

## Step 1: Discover the Project's Documentation Conventions

Before writing anything, understand how this project already documents things:

- Look for existing patterns: session summaries, ADRs, changelogs, README, CLAUDE.md, `ai/memory/`, `docs/`, decision logs, plan files
- Check git log for recent documentation commits
- Note the naming conventions, file locations, and formats already in use

**Adapt to what exists.** If the project uses ADRs, update ADRs. If it uses session summaries, create the next one. If nothing exists, create something minimal and well-placed.

---

## Step 2: Capture What Matters

Reflect on the full conversation and extract:

- **What was accomplished** — decisions made, files created/modified, problems solved
- **What's still open** — unresolved questions, next steps, blockers
- **Critical context** — things the next session must know that aren't obvious from the code alone (rationale, rejected approaches, user preferences, constraints discovered)
- **The exact pickup point** — what specific task or question should the next session start with

Be ruthless about signal vs noise. Only capture what a smart engineer with access to the codebase couldn't figure out on their own.

---

## Step 3: Write Project Documentation

Update or create documentation using the project's conventions:

- **Update existing files** that track progress (session summaries, plans, decision logs)
- **Create new files** only if the project's pattern calls for it (e.g., a new session summary in a series)
- **Keep it scannable** — bullets, tables, clear headers. A reader should get 80% of the value in 30 seconds.

If no conventions exist, create a single `SESSION-HANDOFF.md` at the project root.

---

## Step 4: Generate Continuation Prompt

Create a prompt the user can paste into a new chat. This is the most important output.

The prompt should:
- **Set the role and mission** — what kind of work is being done
- **Point to prerequisite files** — what to read first (be specific with paths)
- **State what's already decided** — so the next session doesn't re-debate settled questions
- **Define the pickup point** — the exact next step, framed as an actionable instruction
- **Be self-contained** — the prompt alone (plus the files it references) should be enough

Write it in the voice of the user giving instructions to a new collaborator. Make it feel natural, not robotic.

---

## Output

Present to the user:

1. **Session summary** — 3-5 sentences of what happened
2. **Files written/updated** — list with paths
3. **The continuation prompt** — ready to copy-paste, in a code block
