# Personas

Reusable AI personas for Claude. Each persona shapes how Claude thinks and works during a session.

All personas inherit from [`philosophies.md`](./philosophies.md) — read it first.

## Two Types

### `roles/` — Identity Personas

Activate a role persona at the start of a chat. Claude becomes that person for the **entire session**.

> "Take the role of `roles/designer.md`. Here's what I need..."

The role stays active throughout. Every response, judgment call, and pushback comes from that identity. Use these for extended working sessions — design reviews, architecture discussions, implementation sprints, strategy conversations.

### `tasks/` — Task Personas

Invoke a task persona for a **specific job**. Claude does the task and the persona is done.

> "Take the role of `tasks/pr-reviewer.md` and review these PR comments."

These are short-lived — usually one or two rounds of execution. Use these for focused, repeatable workflows with a clear start and end.
