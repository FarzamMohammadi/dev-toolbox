---
name: write-polish
description: Line edit existing content to improve voice, flow, and readability. Removes AI tells and ensures authentic human tone.
---

# /write-polish - Line Edit & Polish

You are performing a line edit to polish existing content for voice, flow, and authenticity.

## What This Does

1. Check voice consistency
2. Apply burstiness (sentence variety)
3. Remove AI tells
4. Smooth transitions
5. Enhance emotional engagement
6. Return polished content

## Instructions

### Step 1: Get Content

Ask: "Share the content you'd like me to polish. I'll focus on making it sound more natural and authentic."

### Step 2: Load Guidelines

Reference:
- `ai/toolkits/writing/memory/voice-samples.md`
- `ai/toolkits/writing/philosophy/ANTI-PATTERNS.md`
- `ai/toolkits/writing/philosophy/VOICE-MANDATE.md`

### Step 3: Multi-Pass Polish

#### Pass 1: AI Tell Removal
Find and replace:
- Forbidden words (delve, tapestry, comprehensive, etc.)
- Forbidden phrases ("It's important to note...", "Let's dive into...")
- Em dashes → commas or sentence breaks
- Generic transitions → natural ones

#### Pass 2: Burstiness
Analyze sentence length distribution.
Target:
- ~30% short (<10 words)
- ~50% medium (10-20 words)
- ~20% long (>20 words)

Vary adjacent sentences. No two consecutive sentences should be similar length.

#### Pass 3: Voice Injection
Add personality markers:
- Signature phrases ("Here's the thing:", "Buckle up")
- Conversational elements
- Direct address ("You'll want to...")
- Honest admissions where appropriate

#### Pass 4: Transition Smoothing
Check every section transition:
- Remove abrupt jumps
- Add bridging sentences
- Echo concepts across sections

#### Pass 5: Read-Aloud Test
Would someone naturally say this? If not, rework.

### Step 4: Present Polished Content

Deliver:
- Full polished content
- Summary of changes made
- Before/after examples for significant changes

### Step 5: Summary Report

```markdown
## Polish Summary

### Changes Made
- AI tells removed: X
- Sentences restructured: Y
- Voice markers added: Z
- Transitions improved: W

### Key Improvements
| Location | Before | After | Why |
|----------|--------|-------|-----|
| [Where] | [Original] | [Changed] | [Reason] |

### Sentence Length Distribution
- Short: X%
- Medium: Y%
- Long: Z%

### Remaining Considerations
[Any areas that might benefit from further attention]
```

### Step 6: Offer Options

Ask: "Here's the polished version. Would you like me to:
1. Explain any specific change?
2. Adjust the intensity of the polish?
3. Focus on a particular section?"

## Quick Reference

### Remove These
- delve, tapestry, vibrant, landscape, comprehensive
- furthermore, moreover, additionally
- "It's important to note..."
- "In this article, we will..."
- Em dashes (—)

### Add These (Where Natural)
- "Here's the thing:"
- "Buckle up"
- "Sound familiar?"
- Short punchy sentences. Like this.
- Questions to engage reader

### Transform These
| From | To |
|------|-----|
| "utilize" | "use" |
| "It is essential" | "You need" |
| "facilitate" | "help", "enable" |
| "comprehensive" | "full", "complete" |

## Reference Files

- Line editing: `ai/toolkits/writing/agents/line-editor.md`
- Humanizer: `ai/toolkits/writing/skills/humanizer.md`
- Voice: `ai/toolkits/writing/memory/voice-samples.md`
- Anti-patterns: `ai/toolkits/writing/philosophy/ANTI-PATTERNS.md`

## Begin

Start with: "I'll polish your content for voice, flow, and authenticity. Share what you'd like me to work on."
