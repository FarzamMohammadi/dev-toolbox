# Readability Checker Skill

> **Purpose:** Analyze and improve content readability using established metrics. Ensures content meets cognitive load standards for the target audience.

---

## When to Use

- Verifying content meets readability targets
- Content feels too dense or complex
- Audience feedback suggests difficulty
- Before final publication

---

## Readability Metrics

### Target Standards

| Metric | Target | Why |
|--------|--------|-----|
| Flesch-Kincaid Grade | 9-11 | Accessible to professionals |
| Flesch Reading Ease | 50-70 | "Fairly difficult" to "Standard" |
| Avg Sentence Length | 15-20 words | Digestible chunks |
| Avg Word Length | 4-6 letters | Plain language |
| Paragraph Length | 40-150 words | Visual breathing room |

### Flesch-Kincaid Quick Reference

| Grade | Audience | Style |
|-------|----------|-------|
| 5-6 | Everyone | Very simple |
| 7-8 | General public | Easy |
| **9-11** | **Professionals (TARGET)** | **Standard** |
| 12-14 | College level | Somewhat complex |
| 15+ | Academic | Complex |

---

## Analysis Process

### Step 1: Sentence Analysis

**Count and categorize:**
- Short sentences (< 10 words): X%
- Medium sentences (10-20 words): Y%
- Long sentences (> 20 words): Z%

**Targets:**
- Short: 25-35%
- Medium: 45-55%
- Long: 15-25%

**Red Flags:**
- More than 3 consecutive sentences same length
- Any sentence > 40 words
- More than 30% short OR long

### Step 2: Word Analysis

**Check for:**
- Words > 3 syllables (should be < 15% of text)
- Jargon without definition
- Unnecessary complexity

**Common Swaps:**

| Complex | Simple |
|---------|--------|
| utilize | use |
| implement | build, create |
| facilitate | help, enable |
| subsequently | then, after |
| demonstrate | show |
| approximately | about |
| sufficient | enough |
| numerous | many |
| commence | start, begin |
| terminate | end, stop |

### Step 3: Paragraph Analysis

**Check each paragraph:**
- Word count (target: 40-150)
- Single main idea (not multiple)
- Topic sentence present

**Red Flags:**
- Paragraph > 200 words
- Multiple unrelated ideas
- Missing topic sentence
- Wall of text (no breaks)

### Step 4: Section Analysis

**Check each section:**
- Word count (target: ≤ 300)
- Clear header
- Visual breaks present

**Red Flags:**
- Section > 300 words without subheader
- No bullet points, tables, or code blocks
- Dense text walls

### Step 5: Cognitive Load Assessment

**Check:**
- New concepts introduced gradually
- Examples follow explanations
- Familiar before unfamiliar
- Chunking used effectively

**Signs of Overload:**
- Multiple new terms in one paragraph
- Complex concept without example
- No visual breaks for 3+ paragraphs
- Reader needs to hold too much in memory

---

## Readability Fixes

### Too Complex (High Grade Level)

**Problem:** Content reads at grade 12+

**Fixes:**
1. Break long sentences
2. Replace complex words
3. Add more short sentences
4. Use more active voice
5. Remove unnecessary qualifiers

**Before:**
> "The implementation of containerization technologies necessitates a comprehensive understanding of the underlying virtualization mechanisms that facilitate process isolation."

**After:**
> "To use containers well, you need to understand how they isolate processes. Here's the key concept."

### Too Dense (High Cognitive Load)

**Problem:** Too much information packed together

**Fixes:**
1. Add paragraph breaks
2. Use bullet points for lists
3. Add headers for subtopics
4. Include examples after concepts
5. Add visual elements (tables, code blocks)

### Poor Rhythm (Uniform Sentences)

**Problem:** All sentences similar length

**Fixes:**
1. Combine some short sentences
2. Break some long sentences
3. Add very short statement. Like this.
4. Use questions to vary rhythm
5. Add incomplete thoughts. For emphasis.

---

## Readability Checklist

### Before Publishing

- [ ] Average sentence length: 15-20 words
- [ ] No sentences > 40 words
- [ ] Sentence length variety present
- [ ] Paragraphs: 40-150 words each
- [ ] Sections: ≤ 300 words each
- [ ] Complex words: < 15%
- [ ] All jargon defined
- [ ] Visual breaks every 2-3 paragraphs
- [ ] Examples follow concepts
- [ ] Flesch-Kincaid: Grade 9-11

---

## Quick Readability Test

### The "Breath Test"
Read a paragraph out loud. If you run out of breath before a natural pause, sentences are too long.

### The "Scan Test"
Scan the page in 10 seconds. Can you identify:
- Main topic?
- 3 key points?
- Where to find specific info?

If no, add structure (headers, bullets, bold).

### The "Fresh Eyes Test"
Would someone with basic knowledge understand this on first read? If they'd need to re-read, simplify.

---

## Sample Analysis Report

```markdown
## Readability Analysis

### Overall Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Flesch-Kincaid Grade | 10.2 | 9-11 | ✅ |
| Avg Sentence Length | 18 words | 15-20 | ✅ |
| Long Sentences (>20) | 22% | <25% | ✅ |
| Complex Words | 12% | <15% | ✅ |
| Avg Paragraph Length | 95 words | 40-150 | ✅ |

### Sentence Distribution
- Short (<10 words): 28%
- Medium (10-20): 50%
- Long (>20): 22%

### Issues Found
1. Section 3 exceeds 300 words (342) → Split
2. Paragraph in Section 2 has 185 words → Break up
3. "Containerization" undefined → Add definition

### Recommendations
1. Break the long paragraph in Section 2 after "..."
2. Add subheader to Section 3 at "..."
3. Define "containerization" on first use
```

---

## Integration

This skill can be called by:
- `copy-editor` agent (mandatory check)
- `line-editor` agent (optional)
- User directly for analysis

Reference:
- `../philosophy/QUALITY-STANDARDS.md`
