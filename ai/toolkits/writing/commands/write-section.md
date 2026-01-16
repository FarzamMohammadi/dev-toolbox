---
name: write-section
description: Write a specific section from an existing plan or outline. Provide section details or reference a section plan.
---

# /write-section - Write Specific Section

You are writing a single section of content based on provided plan or guidance.

## What This Does

1. Understand section requirements
2. Load voice and style guidelines
3. Write the section
4. Apply basic editing
5. Deliver draft

## Instructions

### Step 1: Get Section Details

Ask for one of:
- A section plan (from `/write-outline` or manual)
- Section title + key points to cover
- Context about what comes before/after

If they have a section plan, use it. If not, gather:
- What is this section about?
- What key points must be covered?
- What comes before this section? (for transition)
- What comes after? (for setup)
- Target word count?

### Step 2: Load Voice Guidelines

Read:
- `ai/toolkits/writing/memory/voice-samples.md`
- `ai/toolkits/writing/philosophy/ANTI-PATTERNS.md`

### Step 3: Write Section

Follow these rules:
- Max 300 words
- 2-5 sentences per paragraph
- One main idea per paragraph
- Voice consistent with samples
- No forbidden words
- Varied sentence length (burstiness)

Structure:
```markdown
## [Section Title]

[Opening - connects from previous or hooks]

[Content paragraphs]

[Transition to next]
```

### Step 4: Basic Polish

Quick check:
- [ ] Sounds like the author
- [ ] No AI tells
- [ ] Under 300 words
- [ ] Key points covered
- [ ] Transitions work

### Step 5: Deliver

Present section with:
- The content
- Word count
- Any notes or concerns

Ask: "How does this section look? Adjustments needed?"

## Example Usage

**User:** "Write my 'Quick Start' section. It should cover: clone repo, run docker-compose, access localhost:3000. Reader just finished prerequisites."

**Response:** [Write section following pattern above]

## Reference Files

- Voice: `ai/toolkits/writing/memory/voice-samples.md`
- Anti-patterns: `ai/toolkits/writing/philosophy/ANTI-PATTERNS.md`
- Quality: `ai/toolkits/writing/philosophy/QUALITY-STANDARDS.md`
- Draft writing: `ai/toolkits/writing/agents/draft-writer.md`

## Begin

Start with: "Let's write a section! Tell me about it - do you have a section plan, or should I gather details?"
