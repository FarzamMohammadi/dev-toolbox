# Flow Analyzer Skill

> **Purpose:** Analyze and improve the logical flow of content from opening to closing. Ensures readers experience a coherent journey through the material.

---

## When to Use

- Content feels disjointed
- Transitions are weak
- Reader might get lost
- Sections seem out of order
- Complexity jumps unexpectedly

---

## Flow Analysis Framework

### 1. Opening Flow

**Check:**
- Does it hook immediately?
- Is context established quickly?
- Is the promise clear (what reader will get)?
- Does it connect to reader's situation?

**Good Opening Flow:**
```
Hook (problem/question/surprise)
    ↓
Context (why this matters)
    ↓
Promise (what you'll deliver)
    ↓
First content section
```

**Problems to Fix:**
| Issue | Fix |
|-------|-----|
| Throat-clearing intro | Cut to the hook |
| No clear promise | Add explicit "by the end..." |
| Disconnect from reader | Add relatable problem |

### 2. Section-to-Section Flow

**For Each Transition:**

1. **End of Section A:**
   - Wraps up cleanly
   - Creates forward momentum
   - Hints at what's next

2. **Start of Section B:**
   - Connects back to A
   - Establishes new topic
   - Maintains energy

**Good Transition Pattern:**
```
Section A concludes with insight
    ↓
Brief pause (---) or new header
    ↓
Section B opens by acknowledging A and pivoting
```

**Transition Types:**

| Type | When to Use | Example |
|------|-------------|---------|
| Question | Pivot to new topic | "But what about X?" |
| Building | Add complexity | "Now that we have X, let's add Y" |
| Contrast | Different perspective | "That's the theory. Here's the reality." |
| Example | Illustrate concept | "Let's see this in action." |
| Summary pivot | After complex section | "With that foundation, we can now..." |

### 3. Complexity Progression

**Ideal Pattern:**
```
Simple concept
    ↓
Apply to example
    ↓
Slightly more complex concept
    ↓
Apply to example
    ↓
Complex concept
    ↓
Full example combining all
```

**Check for:**
- [ ] New concepts build on previous
- [ ] No unexplained jumps
- [ ] Examples follow theory
- [ ] Complexity gradual, not sudden

**Red Flags:**
- Advanced concept appears before basics
- Example assumes knowledge not yet covered
- Sudden increase in technical density
- Jargon introduced without definition

### 4. Thread Continuity

**Threads** are themes or concepts that run through the piece.

**Check:**
- Are threads introduced clearly?
- Are they maintained throughout?
- Do they resolve by the end?

**Example Threads:**
- A running example (same scenario used across sections)
- A core metaphor (extended throughout)
- A problem being solved (multiple aspects addressed)

**Thread Map:**
```
Thread: "Building a deployment pipeline"

Section 1: Introduce the goal (pipeline)
Section 2: First component (containers) → relates to pipeline
Section 3: Second component (orchestration) → relates to pipeline
Section 4: Third component (CI/CD) → relates to pipeline
Section 5: Bring it together (full pipeline)
```

### 5. Closing Flow

**Check:**
- Does closing synthesize (not just summarize)?
- Are threads resolved?
- Is there forward momentum?
- Does reader know what to do next?

**Good Closing Flow:**
```
Synthesis (weave together key insights)
    ↓
Resolution (threads concluded)
    ↓
Next steps (what reader can do now)
    ↓
Forward look (what comes next / tease future)
```

---

## Flow Analysis Process

### Step 1: Map the Current Flow

Create a flow diagram:
```
Section 1: [Topic] → [Key insight]
    ↓ Transition: [How connected?]
Section 2: [Topic] → [Key insight]
    ↓ Transition: [How connected?]
[...]
```

### Step 2: Identify Breaks

Mark any transitions that:
- Feel jarring
- Require assumed knowledge
- Don't logically follow
- Jump complexity levels

### Step 3: Check Reader Journey

Answer:
- Can a reader follow from start to finish?
- At any point, would they be lost?
- Is the progression natural?

### Step 4: Suggest Fixes

For each issue:
- Reorder sections (if structural)
- Add transition sentences (if connection weak)
- Add bridging paragraph (if gap significant)
- Move content to better location

---

## Quick Flow Fixes

### Weak Transition
**Before:** Ends abruptly, new section starts cold

**Fix:** Add transition sentence at end of previous section
> "With X covered, we can move on to Y."

### Missing Context
**Before:** Assumes knowledge not yet covered

**Fix:** Add brief setup
> "Before we tackle X, you need to understand Y."

### Complexity Jump
**Before:** Simple → Very complex suddenly

**Fix:** Add intermediate step or example
> "Let's start with a simple case before we get fancy."

### Thread Dropped
**Before:** Theme mentioned early, never returned to

**Fix:** Add explicit callback
> "Remember when we said X? Here's where that pays off."

---

## Flow Quality Checklist

- [ ] Opening hooks immediately
- [ ] Context established within first 2 paragraphs
- [ ] Promise clear to reader
- [ ] Each transition is explicit
- [ ] No jarring section jumps
- [ ] Complexity builds gradually
- [ ] Threads maintained throughout
- [ ] Closing synthesizes (not just summarizes)
- [ ] Next steps clear
- [ ] Reader knows what to do after reading

---

## Integration

This skill can be called by:
- `outline-planner` agent (structure planning)
- `review-aligner` agent (outline review)
- `map-reviewer` agent (section review)
- `line-editor` agent (content polish)

Reference:
- `../philosophy/QUALITY-STANDARDS.md`
- `../templates/blog-template.md`
