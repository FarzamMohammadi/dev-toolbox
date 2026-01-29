---
name: literary-editor
description: Transform raw notes into polished prose. Operations include analyze, edit, restructure. Use when improving written content, work diary entries, documentation, or when user mentions editing, writing, or prose refinement.
allowed-tools: Read, Write, Edit
argument-hint: [operation] [file-path]
---

# Literary Editor

Transform rough drafts into clear, compelling prose. This skill applies rigorous writing principles to any text—work diaries, documentation, essays, or technical writing.

## Pre-Flight Check

Verify target file exists:

```bash
[ -f [file-path] ] || echo "File not found: [file-path]"
```

**If file not found:** Confirm path with user before proceeding.

---

## Operations

### `analyze` — Diagnose without changing

Read content, identify issues, report findings. No modifications made.

### `edit` — Apply principles, revise in place

Transform content following writing principles. Preserves meaning, improves clarity.

### `restructure` — Reformat for new purpose

Convert raw notes into structured format appropriate to content type.

---

## Writing Principles

Apply these principles during edit and restructure operations.

### I. The Craft of Compression

**1. Every sentence must earn its place.**
Ask: "If I delete this, does meaning survive?" If yes, delete it.

**2. Verbs carry weight; adjectives are ballast.**
- Weak: "did extensive research"
- Strong: "surveyed 14 attack vectors"

**3. Specificity is credibility.**
- Weak: "improved security significantly"
- Strong: "defense rate: 59% → 99%"

**4. Cut throat-clearing.**
Remove "I think," "basically," "just," "really," "very." Start where meaning starts.

### II. Structure as Thought

**5. Templates are scaffolding, not cages.**
Consistent structure enables scanning. The reader should know where to look.

**6. Chronology is for logs; themes are for diaries.**
Don't recount events in order. Group by insight.

### III. The Economy of Attention

**7. Lead with the delta.**
State what changed first, not what happened.

**8. Bullets over paragraphs for scannable content.**
Reserve prose for synthesis and reflection.

**9. Headers are navigation aids.**
A reader should reconstruct content from headers alone.

### IV. Precision in Language

**10. Active voice, concrete subjects.**
- Weak: "The system was configured to..."
- Strong: "Configured the system to..."

**11. Present tense for observations; past for actions.**
"Defense-in-depth works" (observation). "Added validation layer" (action).

**12. Technical accuracy over elegance.**
If forced to choose, choose precision.

### V. Honesty in Reflection

**13. Document failure without self-flagellation.**
State what happened, what was learned, what changes. Skip emotional spirals.

**14. Distinguish root cause from symptom.**
- Symptom: "Took too long"
- Root: "Didn't align expectations before research"

**15. The "next time" test.**
Every reflection should imply a different future action. Otherwise it's venting.

### VI. The Document as Artifact

**16. Write for the stranger who inherits your role.**
They should understand decisions without your presence.

**17. Date everything.**
"Recently" means nothing in six months.

**18. Link to evidence.**
Reference commits, documents, conversations. The document is an index.

**19. Separate process notes from sharable entries.**
Raw notes are for you. The final document is for the record.

**20. Preserve the author's voice.**
Edit for clarity, not uniformity. Each writer has a rhythm worth keeping.

---

## Operation: Analyze

### Step 1: Read Content

Read the target file completely. Note:
- Overall structure (or lack thereof)
- Recurring patterns (good and problematic)
- Quantifiable issues (passive constructions, filler words, vague claims)

### Step 2: Categorize Issues

Group findings into:
1. **Structural** — Organization, flow, missing sections
2. **Clarity** — Ambiguous phrasing, jargon, complexity
3. **Precision** — Vague claims, missing specifics, unsupported assertions
4. **Voice** — Passive constructions, throat-clearing, inconsistent tone
5. **Mechanics** — Grammar, punctuation, formatting

### Step 3: Output Analysis

Present findings directly to user (do not write to file):

```
## Analysis: [filename]

**Summary:** [One-sentence overall assessment]

### Structural Issues
- [issue 1]
- [issue 2]

### Clarity Issues
- [issue 1 with line reference]

### Precision Issues
- [vague claim] → [suggested specific alternative]

### Voice Issues
- [pattern identified] (occurs N times)

### Mechanics
- [minor issues if any]

**Recommendation:** [analyze | edit | restructure] — [brief rationale]
```

---

## Operation: Edit

### Step 1: Read and Understand

Read target file. Identify:
- Author's intent (what are they trying to communicate?)
- Content type (diary, documentation, prose, technical)
- Author's voice (preserve distinctive patterns)

### Step 2: Apply Principles

Work through content applying principles 1-19. Prioritize:
1. Cut unnecessary content (principle 1)
2. Strengthen verbs (principle 2)
3. Add specificity where vague (principle 3)
4. Convert passive to active (principle 10)
5. Fix mechanics last

### Step 3: Write Edited Version

Save to same file (overwrite) or new file if user specifies `--output [path]`.

After saving, report summary:

```
## Edit Complete: [filename]

**Changes:**
- [type of change 1]
- [type of change 2]
- [type of change 3]

**Preserved:** [aspects of original kept intact]

**Word count:** [before] → [after] ([percent] reduction)
```

---

## Operation: Restructure

### Step 1: Identify Content Type

Detect or ask user for content type:
- **Work diary** — Personal professional log
- **Technical documentation** — How-to, reference, API docs
- **Narrative prose** — Essays, articles, stories
- **Meeting notes** — Action items, decisions, context

### Step 2: Extract Core Content

From raw notes, identify:
- Key facts and outcomes
- Decisions made and rationale
- Learnings and insights
- Action items or next steps
- Dates and references

### Step 3: Apply Appropriate Template

#### Work Diary Entry

```markdown
## [YYYY-MM-DD] - [Brief Title]

### Intention
[One line: why this work existed]

### What Changed
- [Observable outcome 1, quantified if possible]
- [Observable outcome 2]

### Decisions & Rationale
- [Decision 1]—[why]
- [Decision 2]—[why]

### Tools & Techniques
- [Tool/technique 1] for [purpose]
- [Tool/technique 2] for [purpose]

### Learnings
- [Transferable insight 1]
- [Transferable insight 2]

### Reflections
[Personal synthesis, surprises, course corrections. 2-3 sentences max.]
```

#### Technical Documentation

```markdown
# [Title]

[One-paragraph summary: what this is and who it's for]

## Prerequisites
- [Requirement 1]
- [Requirement 2]

## [Main Content Section]

[Step-by-step or structured explanation]

## Common Issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| [issue] | [cause] | [fix] |

## Related
- [Link to related doc]
```

#### Narrative Prose

Restructure into:
1. **Opening** — Hook + thesis/purpose
2. **Body** — Supporting points, each with evidence
3. **Synthesis** — Connection between points
4. **Closing** — Implication or call to action

Preserve author's voice throughout.

#### Meeting Notes

```markdown
## [Meeting Name] — [Date]

**Attendees:** [names]
**Duration:** [time]

### Decisions Made
- [Decision 1]
- [Decision 2]

### Action Items
- [ ] [Action] — [Owner] — [Due date]
- [ ] [Action] — [Owner] — [Due date]

### Key Discussion Points
- [Point 1]: [brief summary]
- [Point 2]: [brief summary]

### Open Questions
- [Question needing follow-up]
```

### Step 4: Write Restructured Version

Save to specified output location. Report:

```
## Restructure Complete

**Source:** [original file]
**Output:** [new file]
**Format:** [content type selected]

**Extracted:**
- [N] key outcomes
- [N] decisions
- [N] learnings

**Notes:** [anything that didn't fit template, requires user input]
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| File not found | Wrong path | Verify path exists |
| Empty file | No content to edit | Confirm correct file |
| Binary file | Not text content | Use text files only |
| Ambiguous content type | Can't detect format | Ask user to specify type |

---

## Usage Examples

```
/literary-editor analyze notes.md
/literary-editor edit draft.md
/literary-editor restructure raw-notes.md --type diary
/literary-editor edit chapter.md --output chapter-v2.md
```

---

## Guidelines for Editor

- **Preserve meaning** — Edit for clarity, never change intent
- **Preserve voice** — The author's rhythm matters; don't homogenize
- **Show your work** — Always report what changed and why
- **Ask when uncertain** — If content type or intent is unclear, ask rather than guess
- **Quantify improvements** — Word count, issue counts, before/after comparisons
