---
name: improve-skill
description: Reflect on a skill's performance and iterate on improvements. Use after running any skill to identify gaps and refine it.
disable-model-invocation: true
argument-hint: [skill-name]
allowed-tools: Read, Write, Edit, AskUserQuestion
---

# Improve Skill

Reflect on how a skill performed, identify gaps, and iterate on improvements.

## Step 1: Locate the Skill

Find the skill file based on the provided name:
```bash
ls ai/claude-code/skills/[skill-name]/skill.md
```

Read the skill's current implementation.

## Step 2: Review Recent Usage

Examine the conversation for how the skill was just used. Ask yourself:

**Clarity & Instructions**
- Were any instructions ambiguous?
- Did I have to guess or interpret what was meant?
- Were there missing steps I filled in myself?

**Edge Cases**
- Did I encounter situations the skill didn't handle?
- What did I improvise that should be documented?

**Output Quality**
- Did the output format work well?
- Was anything awkward to produce?

**Missing Features**
- What would have made this easier?
- What did the user have to clarify that should be in the skill?

**Friction Points**
- Where did I slow down or struggle?
- What felt repetitive or unnecessary?

## Step 3: Generate Reflection

Output findings in this format:

```markdown
## Skill Reflection: [skill-name]

### What Worked Well
- [strength]

### Gaps Identified
| Gap | Suggested Fix |
|-----|---------------|
| [issue] | [concrete change] |

### Suggested Improvements
1. [specific edit to skill.md with line reference]
2. [specific edit]
```

**Use AskUserQuestion** to validate findings or get more context if unsure.

## Step 4: Apply Improvements

Ask user: "Apply these improvements? [Y/n/select]"

- **Y**: Apply all suggested changes
- **n**: Skip, just provide the reflection
- **select**: Let user pick which improvements to apply

When applying, make precise edits to the skill file. Verify each change doesn't break existing functionality.

## Guidelines

- Be specific—vague feedback like "make it clearer" isn't actionable
- Reference exact lines or sections when suggesting changes
- Small, incremental improvements beat large rewrites
- If nothing needs improvement, say so honestly
