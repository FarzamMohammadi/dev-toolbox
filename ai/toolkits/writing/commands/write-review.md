---
name: write-review
description: Review existing content for quality, voice, flow, and AI tells. Provides actionable feedback and suggested improvements.
---

# /write-review - Content Review Mode

You are reviewing existing content for quality and providing actionable feedback.

## What This Does

1. Analyze content against quality standards
2. Check for voice consistency
3. Identify AI tells
4. Assess flow and structure
5. Provide specific, actionable feedback

## Instructions

### Step 1: Get Content

Ask: "Share the content you'd like me to review. You can paste it here or point me to a file."

### Step 2: Multi-Pass Review

#### Pass 1: Voice & Personality
Check against `ai/toolkits/writing/philosophy/VOICE-MANDATE.md`:
- Does it sound like the author?
- Are signature phrases present?
- Is personality showing through?
- Energy level appropriate?

#### Pass 2: AI Tell Detection
Check against `ai/toolkits/writing/philosophy/ANTI-PATTERNS.md`:
- Forbidden words present?
- Generic phrases?
- Em dashes?
- Uniform sentence length?
- Corporate/robotic tone?

#### Pass 3: Quality Standards
Check against `ai/toolkits/writing/philosophy/QUALITY-STANDARDS.md`:
- Section length (≤300 words)?
- Paragraph length (40-150 words)?
- Sentence variety?
- Reading level (~grade 10)?
- Visual breaks adequate?

#### Pass 4: Flow & Structure
Check:
- Does opening hook?
- Are transitions smooth?
- Does complexity build?
- Does closing provide forward momentum?

#### Pass 5: Technical (if applicable)
- Code syntax correct?
- Commands accurate?
- Links formatted properly?

### Step 3: Generate Report

```markdown
## Content Review Report

### Summary
[1-2 sentence overall assessment]

### Strengths
- [What's working well]

### Areas for Improvement

#### Voice & Personality
| Issue | Location | Suggestion |
|-------|----------|------------|
| [Issue] | [Where] | [Fix] |

#### AI Tells Found
| Tell | Location | Replacement |
|------|----------|-------------|
| [Word/phrase] | [Where] | [Alternative] |

#### Quality Concerns
| Concern | Details | Suggestion |
|---------|---------|------------|
| [Issue] | [Specifics] | [Fix] |

#### Flow Issues
| Issue | Location | Fix |
|-------|----------|-----|
| [Issue] | [Where] | [How] |

### Priority Fixes
1. [Most important fix]
2. [Second priority]
3. [Third priority]

### Optional Enhancements
- [Nice to have improvements]
```

### Step 4: Offer Next Steps

Ask: "Would you like me to:
1. Make these changes for you?
2. Focus on a specific area?
3. Review after you make changes?"

## Reference Files

- Voice: `ai/toolkits/writing/philosophy/VOICE-MANDATE.md`
- Anti-patterns: `ai/toolkits/writing/philosophy/ANTI-PATTERNS.md`
- Quality: `ai/toolkits/writing/philosophy/QUALITY-STANDARDS.md`
- Line editing: `ai/toolkits/writing/agents/line-editor.md`

## Begin

Start with: "I'll review your content for quality, voice, and AI tells. Share the content you'd like me to analyze."
