# Anti-Patterns to Avoid

Common mistakes when creating skills and how to fix them.

---

## 1. Agent When You Need Context

**Problem:** Creating an agent for something that needs conversation history.

```yaml
# Wrong - this agent won't know what you discussed
name: summarize-session
description: Summarize what we talked about
agent: SomeAgent
context: fork
```

**Why it fails:** Agents and forked contexts start fresh—they don't see previous conversation.

**Fix:** Use an inline skill (default behavior) that sees the full conversation.

```yaml
# Right - inline skill sees everything
name: summarize-session
description: Summarize what we talked about
# No context: fork, no agent delegation
```

---

## 2. Vague Instructions

**Problem:** Instructions that don't guide Claude's actions.

```markdown
# Wrong
Analyze the code and provide feedback.
```

**Why it fails:** Claude doesn't know what to look for or how to format output.

**Fix:** Be specific about what to check and how to report.

```markdown
# Right
## Step 1: Identify Issues
Check for:
- [ ] Hardcoded credentials
- [ ] SQL injection vulnerabilities
- [ ] Missing input validation

## Step 2: Output
For each issue found:
| File:Line | Severity | Issue | Fix |
|-----------|----------|-------|-----|
```

---

## 3. Missing Output Format

**Problem:** Telling Claude to produce output without showing the format.

```markdown
# Wrong
Generate a summary and save it.
```

**Why it fails:** Output varies wildly between runs. Users don't know what to expect.

**Fix:** Show the exact template with `[placeholders]` Claude fills in.

```markdown
# Right
## Output Format

Save to `summary.md`:
```markdown
## [DATE] - Session Summary

**Goal:** [what user was trying to accomplish]
**State:** [in progress / blocked / completed]
**Work Done:**
- [bullet list of completed items]
**Next Step:** [immediate next action]
```
```

---

## 4. Over-Permissive Tools

**Problem:** Not restricting tools for a read-only skill.

```yaml
# Wrong - omitting allowed-tools for read-only work
name: explore-codebase
description: Research patterns in the codebase
# No allowed-tools = can do anything
```

**Why it fails:** Skill might accidentally modify files when it only needs to read.

**Fix:** Explicitly restrict to minimum needed tools.

```yaml
# Right - explicit minimum
name: explore-codebase
description: Research patterns in the codebase
allowed-tools: Read, Grep, Glob
```

**Quick reference:**
| Skill Type | Tools |
|------------|-------|
| Read-only research | `Read, Grep, Glob` |
| File modification | `Read, Write, Edit` |
| External API | `Bash, Read, Write` |

---

## 5. Hardcoded Secrets

**Problem:** Including credentials in the skill file.

```markdown
# Wrong
Use API token: sk-abc123def456...
```

**Why it fails:** Credentials exposed in version control, shared with anyone who gets the skill.

**Fix:** Use environment variables with a pre-flight check.

```markdown
# Right
## Pre-Flight Check
```bash
echo "API_TOKEN: ${API_TOKEN:+set}"
```

If not set, add to `~/.zshrc`:
```bash
export API_TOKEN="your-token-here"
```
```

---

## 6. No Setup Section

**Problem:** Assuming directories and files exist.

```markdown
# Wrong - assumes directories exist
## Step 1: Save Data
Save the response to `.claude/skills/my-skill/data.json`
```

**Why it fails:** Skill breaks when copied to a new project.

**Fix:** Include first-time setup that creates everything needed.

```markdown
# Right
## First-Time Setup

Before first use, create required directories:
```bash
mkdir -p .claude/skills/my-skill && \
  echo '*' > .claude/skills/my-skill/.gitignore
```

Run this once per project.

## Step 1: Save Data
Save the response to `.claude/skills/my-skill/data.json`
```

---

## 7. Auto-Invoke for Dangerous Actions

**Problem:** Allowing auto-invocation for skills with side effects.

```yaml
# Wrong - Claude might auto-invoke!
name: deploy
description: Deploy to production
# Missing disable-model-invocation
```

**Why it fails:** Claude might deploy when user just mentioned "deploy" in passing.

**Fix:** Add `disable-model-invocation: true` for any irreversible action.

```yaml
# Right - manual only
name: deploy
description: Deploy to production
disable-model-invocation: true
```

**Rule:** If it commits, deploys, deletes, or sends, make it manual-only.

---

## 8. Setup That Overwrites Data

**Problem:** Setup that destroys existing data.

```bash
# Wrong - overwrites existing data
mkdir -p ai/memory && printf 'content' > ai/memory/file.md
```

**Why it fails:** Running setup twice destroys user's saved data.

**Fix:** Use `[ -f file ] ||` pattern to only create if missing.

```bash
# Right - safe to run multiple times
mkdir -p ai/memory && \
  [ -f ai/memory/file.md ] || printf 'content' > ai/memory/file.md
```

---

## 9. Windows-Style Paths

**Problem:** Using backslashes in file paths.

```markdown
# Wrong - breaks on Unix/Mac
See scripts\helper.py for details.
Save to output\results.json
```

**Why it fails:** Backslashes don't work on Unix-based systems.

**Fix:** Always use forward slashes.

```markdown
# Right - works everywhere
See scripts/helper.py for details.
Save to output/results.json
```

---

## 10. Too Many Options

**Problem:** Presenting multiple approaches without guidance.

```markdown
# Wrong - confusing
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image...
```

**Why it fails:** Claude doesn't know which to choose, might pick wrong one.

**Fix:** Provide a default with an escape hatch for special cases.

```markdown
# Right - clear default
Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
```

---

## 11. Deeply Nested References

**Problem:** Reference files that link to other reference files.

```markdown
# Wrong - too deep
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

**Why it fails:** Claude may partially read files, miss information.

**Fix:** Keep references one level deep from SKILL.md.

```markdown
# Right - one level deep
# SKILL.md
- **Basic usage**: [instructions here]
- **Advanced features**: See [advanced.md](advanced.md)
- **API reference**: See [reference.md](reference.md)
```

---

## 12. Wrong Person in Description

**Problem:** Using first or second person in description.

```yaml
# Wrong - causes discovery problems
description: I can help you process Excel files
description: You can use this to analyze data
```

**Why it fails:** Description is injected into system prompt; inconsistent POV breaks discovery.

**Fix:** Always write in third person.

```yaml
# Right - third person
description: Processes Excel files and generates reports
description: Analyzes data and produces visualizations
```

---

## Quick Reference: Anti-Pattern → Fix

| Anti-Pattern | Quick Fix |
|--------------|-----------|
| Agent when need context | Remove `context: fork` and `agent:` |
| Vague instructions | Add checklists and specific steps |
| Missing output format | Add template with `[placeholders]` |
| Over-permissive tools | Add `allowed-tools:` with minimum set |
| Hardcoded secrets | Use env vars + pre-flight check |
| No setup section | Add "First-Time Setup" with mkdir/file creation |
| Auto-invoke dangerous | Add `disable-model-invocation: true` |
| Setup overwrites | Use `[ -f file ] ||` pattern |
| Windows paths | Use forward slashes everywhere |
| Too many options | Provide default + escape hatch |
| Deep nesting | Keep references one level from SKILL.md |
| Wrong person | Write description in third person |
