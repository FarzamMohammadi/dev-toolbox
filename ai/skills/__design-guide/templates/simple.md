# Simple Skill Template

Copy this template for basic, single-operation skills.

---

```yaml
---
name: [skill-name]
description: [What it does] and [when to use it]. Use when user mentions [keywords].
disable-model-invocation: true    # Remove if safe to auto-invoke
allowed-tools: Read, Write, Edit  # Adjust to minimum needed
argument-hint: [arg1] [--flag]    # Remove if no arguments
---
```

```markdown
# [Skill Name]

[One-sentence description of what this skill does.]

## Pre-Flight Check

Verify prerequisites before proceeding:

\`\`\`bash
# Example: Check for required tool
command -v [tool] >/dev/null || echo "[tool] not installed"

# Example: Check for required file
[ -f [path/to/file] ] || echo "Required file not found"
\`\`\`

**If check fails**, guide user to resolve before continuing.

## First-Time Setup

> Skip this section if skill doesn't create files/directories.

Create required structure (safe to run multiple times):

\`\`\`bash
mkdir -p [path/to/dir] && \
  [ -f [path/to/file] ] || printf '[initial content]' > [path/to/file]
\`\`\`

## Step 1: Gather

[What information to collect and how]

\`\`\`bash
# Commands to gather information
\`\`\`

## Step 2: Process

[What to do with the gathered information]

## Step 3: Output

[What to produce and where]

### Output Format

[Exact template with placeholders]:

\`\`\`markdown
## [Title]

**[Field 1]:** [value]
**[Field 2]:** [value]

### [Section]
- [item 1]
- [item 2]
\`\`\`

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| [error 1] | [cause] | [fix] |
| [error 2] | [cause] | [fix] |

## Usage Examples

\`\`\`
/[skill-name]
/[skill-name] [arg]
/[skill-name] --flag
\`\`\`
```

---

## Customization Notes

### Frontmatter

- **`name`**: Lowercase, hyphens only, max 64 chars
- **`description`**: Include WHAT and WHEN, third person
- **`disable-model-invocation`**: Add if skill has side effects
- **`allowed-tools`**: Restrict to minimum needed
- **`argument-hint`**: Show expected arguments

### Sections to Keep/Remove

| Section | Keep When |
|---------|-----------|
| Pre-Flight Check | Always (even if just "none required") |
| First-Time Setup | Skill creates files/directories |
| Error Handling | Skill can fail in predictable ways |
| Usage Examples | Skill takes arguments |

### Tool Combinations

| Skill Type | Suggested Tools |
|------------|-----------------|
| Read-only | `Read, Grep, Glob` |
| File editing | `Read, Write, Edit` |
| External commands | `Bash, Read` |
| Full access | Omit `allowed-tools` |
