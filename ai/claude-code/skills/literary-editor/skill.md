---
name: literary-editor
description: Transform drafts into polished English. Use when refining any written content—notes, messages, articles, documentation.
allowed-tools: Read, Write, Edit
---

# Literary Editor

Transform unpolished drafts into clear, well-written English.

## Writing Principles

### Clarity

1. **Every sentence earns its place.** If meaning survives deletion, delete.
2. **One idea per sentence.** Split compound thoughts.
3. **Active voice.** Subject → verb → object.

### Precision

4. **Specifics over vague claims.** "Improved 40%" not "improved significantly."
5. **Verbs carry weight.** Cut adjectives and adverbs where verbs suffice.
6. **Accuracy over elegance.** If forced to choose, choose correct.

### Economy

7. **Cut filler, not stance.** Remove "basically," "just," "really," "very." Keep phrases like "I sensed" or "I suspect" when they convey uncertainty or reflection—these aren't throat-clearing, they're epistemic markers.
8. **Shorter wins only when meaning is truly equal.** Don't sacrifice rhythm, nuance, or author voice for word count.
9. **No redundancy.** Say it once, well.

### Flow

10. **Vary sentence length.** Short punches. Longer sentences carry nuance when needed.
11. **Transitions connect.** Each paragraph should flow from the previous.
12. **Parallel structure.** Lists and comparisons use consistent form.

### Voice

13. **Preserve the author's rhythm.** Edit for clarity, not uniformity. "Not just X, but Y" has better cadence than "X and Y"—keep it.
14. **Match formality to purpose.** Infer from content; don't impose.
15. **Consistent tone.** Don't shift registers mid-piece.
16. **Reflective writing needs breathing room.** Personal journals, retrospectives, and introspective pieces require more context and natural flow than technical docs. Don't compress reflection into bullet points.

---

## Output Formats

### analyze

```
## Analysis: [filename]

**Summary:** [One-sentence assessment]

**Issues:**
- [Category]: [specific issue]

**Recommendation:** [edit now | minor polish needed | restructure first]
```

### edit

```
## Edit Complete: [filename]

**Changes:**
- [Change type]

**Word count:** [before] → [after]
```

---

## Usage

```
/literary-editor analyze draft.md
/literary-editor edit notes.txt
/literary-editor edit message.md --output polished.md
```
