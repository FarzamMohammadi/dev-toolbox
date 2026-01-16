---
name: write-blog
description: Full 10-layer orchestrated workflow for blog posts. Guides you from topic to publication-ready content with multiple review checkpoints.
---

# /write-blog - Full Blog Writing Workflow

You are now initiating the complete blog writing pipeline. This orchestrated workflow will guide the user through all 10 layers of content creation.

## Workflow Overview

```
Layer 1: Context Gathering     → Collect all requirements
Layer 2: Outline Planning      → Create structure
GATE 1: User approval of outline
Layer 4: Section Planning      → Detailed section plans
GATE 2: User approval of section map
Layer 6: Draft Writing         → Write the content
Layer 7: Line Editing          → Polish voice and flow
Layer 8: Copy Editing          → Grammar and consistency
Layer 9: Fact-Check            → Verify and gather resources
GATE 3: User approval of resources
Layer 10: Final Assembly       → Publication-ready
GATE 4: Final approval
```

## Instructions

### Step 1: Gather Context

Start by asking:
1. What topic are you writing about?
2. Who is the target audience?
3. What should readers be able to do/know after reading?
4. Any specific things to include or avoid?
5. Target length (short: ~1000 words, medium: ~2000, long: ~3000+)?

Use web search to research the topic and competitive content.

Create a context document using `ai/toolkits/writing/templates/context-document.md`.

### Step 2: Create Outline

Based on context, select an appropriate framework:
- **AIDA** - For persuasive content
- **PAS** - For problem-solving content
- **Tutorial Flow** - For step-by-step guides
- **Explanatory Flow** - For concept explanations

Create outline with 5-7 H2 sections. Reference `ai/toolkits/writing/agents/outline-planner.md`.

### Step 3: Gate 1 - Outline Approval

Present outline to user:
- Section titles and descriptions
- Why this structure makes sense
- Coverage confirmation

Ask: "Does this outline cover everything? Any adjustments?"

**Do not proceed until approved.**

### Step 4: Section Planning

For each section, create detailed plans:
- Objective
- Key points (3-5)
- Examples to include
- Research tasks
- Word count target

Reference `ai/toolkits/writing/agents/section-planner.md`.

### Step 5: Gate 2 - Section Map Approval

Present section map:
- Summary of each section's focus
- Coverage confirmation

Ask: "Does this detailed plan look good? Anything missing?"

**Do not proceed until approved.**

### Step 6: Write Draft

Write section by section following:
- Voice samples from `ai/toolkits/writing/memory/voice-samples.md`
- Quality standards from `ai/toolkits/writing/philosophy/QUALITY-STANDARDS.md`
- Anti-patterns from `ai/toolkits/writing/philosophy/ANTI-PATTERNS.md`

Reference `ai/toolkits/writing/agents/draft-writer.md`.

### Step 7: Line Edit

Polish for voice, tone, and flow:
- Read-aloud test
- Voice consistency
- Sentence variety (burstiness)
- AI tell elimination

Reference `ai/toolkits/writing/agents/line-editor.md`.

### Step 8: Copy Edit

Check for:
- Grammar and punctuation
- Consistency
- Code verification
- Reading level (target: grade 9-11)

Prepare fact-check queue.

### Step 9: Fact-Check & Resources

- Verify all claims with web search
- Validate links
- Gather supporting resources
- Create embedding plan

### Step 10: Gate 3 - Resource Approval

Present:
- Resources gathered
- Where they'll be embedded
- Any corrections needed

Ask: "These resources will be added. Approve?"

### Step 11: Final Assembly

- Embed all resources
- Add compelling title and subtitle
- Add credits/shoutouts
- Final proofread

### Step 12: Gate 4 - Final Approval

Present complete blog post.

Ask: "Ready for publication? Any final adjustments?"

## Key Files Reference

- Philosophy: `ai/toolkits/writing/philosophy/`
- Agents: `ai/toolkits/writing/agents/`
- Templates: `ai/toolkits/writing/templates/`
- Skills: `ai/toolkits/writing/skills/`
- Voice: `ai/toolkits/writing/memory/voice-samples.md`

## Begin

Start with: "Let's create a blog post! First, tell me: What topic are you writing about?"
