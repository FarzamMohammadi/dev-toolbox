# Quality Standards Mandate

> **Purpose:** Define measurable quality standards grounded in cognitive science and proven readability research.

---

## Core Principle

**Respect the reader's cognitive limits.** Working memory holds only 3-7 items at once. Every quality standard serves one goal: reduce cognitive load so readers can focus on understanding, not decoding.

---

## Readability Standards

### Target: Flesch-Kincaid 10th Grade Level

| Metric | Target | Why |
|--------|--------|-----|
| Flesch-Kincaid Grade | 9-11 | Accessible to professionals without dumbing down |
| Flesch Reading Ease | 50-70 | "Fairly difficult" to "Standard" |
| Average Sentence Length | 15-20 words | Digestible chunks |
| Syllables per Word | 1.4-1.8 avg | Plain language preference |

### How to Achieve It

1. **Prefer shorter words** when meaning is equivalent
   - "use" not "utilize"
   - "help" not "facilitate"
   - "show" not "demonstrate"

2. **Break long sentences** at natural pause points
   - If a sentence has more than one main idea, split it
   - Use periods instead of semicolons when possible

3. **Front-load meaning**
   - Put the key point first, then explain
   - Avoid throat-clearing ("As we all know...", "It should be noted...")

---

## Information Density Standards

### The 300-Word Rule

**Maximum 300 words per section** (H2 heading to next H2 heading)

Rationale: Research shows comprehension drops 50% when readers are overloaded. Short sections:
- Create natural rest points
- Allow scanning
- Improve retention
- Enable non-linear reading

### Section Structure

Every substantial section should follow:

```
[Hook - 1-2 sentences that grab attention]

[Core content - 3-5 paragraphs max]

[Takeaway - What should reader remember]
```

### Paragraph Standards

| Standard | Target |
|----------|--------|
| Sentences per paragraph | 2-5 |
| Words per paragraph | 40-150 |
| Ideas per paragraph | 1 main idea |

---

## Structural Standards

### Heading Hierarchy

```
# Title (H1) - One per document
## Major Sections (H2) - Max 5-7 per document
### Subsections (H3) - Use sparingly, only when truly needed
```

**Rules:**
- Sentence case for all headings ("How to deploy containers" not "How To Deploy Containers")
- No colons or dashes in headings
- No numbered heading prefixes ("1. Introduction")
- H3 only when subsections genuinely need grouping

### Content Chunking

Use visual chunking to reduce cognitive load:

| Format | When to Use |
|--------|-------------|
| Bullet lists | 3+ parallel items |
| Numbered lists | Sequential steps |
| Tables | Comparisons, specifications |
| Code blocks | Any code, even one line |
| Blockquotes | Emphasis, quotes, callouts |

### White Space

- One blank line between paragraphs
- One blank line before and after code blocks
- One blank line before headings
- Never more than 2 consecutive paragraphs without a visual break

---

## Flow Standards

### Logical Progression

Every piece must follow a coherent sequence:

**For Tutorials/Guides:**
1. Problem/Context (Why does this matter?)
2. Prerequisites (What do I need?)
3. Implementation (Step by step)
4. Verification (Did it work?)
5. Next Steps (Where do I go from here?)

**For Explanatory Content:**
1. Hook (Why should I care?)
2. Context (What's the background?)
3. Core Concept (What is it?)
4. Examples (How does it work?)
5. Implications (What does it mean for me?)

**For Opinion/Analysis:**
1. Claim (What's your position?)
2. Evidence (Why do you think this?)
3. Counterarguments (What about X?)
4. Synthesis (So what?)

### Transition Quality

| Bad Transition | Good Transition |
|----------------|-----------------|
| "Additionally..." | [No word needed - just start the next point] |
| "Furthermore..." | "This matters because..." |
| "In conclusion..." | [Just conclude without announcing it] |
| "Let's dive into..." | "Here's how it works:" |

---

## Dual-Level Content Standard

Every blog/article should support two reading modes:

### Quick Grasp Path (Scanners)
- Clear, descriptive headings
- First sentence of each section captures the key point
- Bullet points for key takeaways
- TL;DR or summary at top for long pieces

### Deep Dive Path (Readers)
- Full explanations with context
- Examples and analogies
- Code samples with annotations
- Links to additional resources

**Test:** Someone scanning only headings and first sentences should get 80% of the value.

---

## Technical Content Standards

### Code Blocks

```
✓ Always specify language for syntax highlighting
✓ Keep examples minimal but complete
✓ Include comments for non-obvious lines
✓ Test all code before including
✓ Show expected output when relevant
```

### Commands

```bash
# Always include what the command does
docker-compose up -d

# Show expected output if useful
# Output: Creating network "myapp_default"...
```

### Package/Tool References

- Verify package names exist
- Include version if version-sensitive
- Link to official documentation on first mention

---

## Quality Verification Checklist

### Readability
- [ ] Flesch-Kincaid grade level 9-11
- [ ] No section exceeds 300 words
- [ ] Average sentence length under 20 words
- [ ] No jargon without explanation

### Structure
- [ ] Max 5-7 H2 sections
- [ ] H3 used sparingly
- [ ] Visual breaks every 2-3 paragraphs
- [ ] Tables/lists for comparisons and lists

### Flow
- [ ] Clear logical progression
- [ ] Each section flows to the next
- [ ] No redundant transitions
- [ ] Opening hooks reader
- [ ] Ending provides closure

### Technical
- [ ] All code tested
- [ ] Commands verified
- [ ] Links working
- [ ] Package names correct

---

## Integration Points

This mandate applies to:
- **Layer 4** (Section Planner) - Section sizing and structure
- **Layer 6** (Draft Writer) - Applying standards during writing
- **Layer 7** (Line Editor) - Readability optimization
- **Layer 8** (Copy Editor) - Final standards verification

Referenced by:
- `agents/section-planner.md`
- `agents/draft-writer.md`
- `agents/copy-editor.md`
- `skills/readability-checker.md`
