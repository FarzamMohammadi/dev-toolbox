---
name: write-outline
description: Quick context gathering and outline generation. Use when you just need a structured outline without the full writing workflow.
---

# /write-outline - Context + Outline Only

You are creating a content outline. This is Layers 1-2 of the full pipeline, stopping after outline approval.

## What This Does

1. Gather context (topic, audience, goals)
2. Research the topic
3. Create structured outline
4. Get user approval

Output: Approved outline ready for detailed planning or writing.

## Instructions

### Step 1: Gather Context

Ask:
1. What are you writing about?
2. Who is this for? (audience)
3. What should they know/do after reading?
4. Content type: blog, documentation, or book chapter?
5. Approximate length?

### Step 2: Research

Use web search to understand:
- Current state of topic
- What content already exists
- Gaps we can fill
- Key concepts to cover

### Step 3: Select Framework

Based on content type, choose:

| Content Goal | Framework |
|--------------|-----------|
| Persuade/sell | AIDA (Attention, Interest, Desire, Action) |
| Solve problem | PAS (Problem, Agitate, Solution) |
| Teach step-by-step | Tutorial Flow |
| Explain concept | Explanatory Flow |
| Share journey | Hero's Journey |

### Step 4: Create Outline

Structure:
```markdown
# [Working Title]

## Framework: [Selected]
**Rationale:** [Why this fits]

---

## Section 1: [Title]
[2-3 sentences on what this covers]

## Section 2: [Title]
[Description]

[... 5-7 sections total ...]

---

## Flow Summary
[Why this order makes sense]
```

Rules:
- 5-7 H2 sections maximum
- Sentence case headers
- No colons or dashes in headers
- Each section earns its place

### Step 5: Present for Approval

Show outline with:
- Section summaries
- Framework rationale
- Coverage confirmation

Ask: "Does this outline work for you? What would you adjust?"

## Reference Files

- Outline planning: `ai/toolkits/writing/agents/outline-planner.md`
- Templates: `ai/toolkits/writing/templates/`

## After Approval

Once approved, user can:
- Run `/write-blog` to continue full workflow
- Run `/write-section` to write specific sections
- Use outline manually

## Begin

Start with: "Let's create an outline! What topic are you working on?"
