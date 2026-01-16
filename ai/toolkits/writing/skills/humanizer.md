# Humanizer Skill

> **Purpose:** Transform AI-sounding text into authentic human writing. This skill can be invoked at any point to "humanize" content that feels robotic.

---

## When to Use

- Draft feels too polished or uniform
- Sentences all sound similar
- Missing personality and voice
- AI tells are present
- Content feels "written" not "spoken"

---

## The Humanization Process

### Step 1: Diagnose the Problem

Read the content and identify:
- [ ] Uniform sentence length (no burstiness)
- [ ] Missing personality markers
- [ ] Forbidden words present
- [ ] Generic transitions
- [ ] Over-formal tone
- [ ] Perfect parallel structures
- [ ] Missing emotional engagement

### Step 2: Apply Burstiness

**Before:**
> "Docker containers provide isolation for applications. They package code with dependencies. This ensures consistent behavior. Teams can deploy with confidence."

**After:**
> "Docker containers? They're essentially isolation bubbles for your apps. Pack your code, throw in the dependencies, and boom - it runs the same everywhere. No more 'works on my machine' excuses."

**Techniques:**
- Very short sentence. Then a longer one that develops the thought more fully.
- Questions create variety.
- Incomplete sentences. For effect.
- Lists broken by explanation.

### Step 3: Inject Personality

**Voice Markers to Add:**

| Type | Examples |
|------|----------|
| Conversational openers | "Here's the thing:", "Look,", "Okay, so" |
| Direct address | "You're going to love this", "Sound familiar?" |
| Honest admissions | "I struggled with this", "Honestly, I had no idea" |
| Enthusiasm | "This is actually pretty cool", "Game changer" |
| Informal transitions | "Now here's where it gets interesting" |

**Before:**
> "It is essential to understand these concepts before proceeding."

**After:**
> "You'll want to grok these concepts first. Trust me, spending 10 minutes here saves you hours of head-scratching later."

### Step 4: Remove AI Tells

**Search and Replace:**

| AI Version | Human Version |
|------------|---------------|
| "It's important to note that" | [Just state it] |
| "In this section, we will" | [Jump to content] |
| "Let's dive into" | "Here's how:", "Check this out:" |
| "Furthermore" | "Also," or [just start next point] |
| "Comprehensive" | "Full", "Complete", or [cut] |
| "Leverage" | "Use", "Take advantage of" |
| "Utilize" | "Use" |
| Em dashes (—) | Commas or sentence breaks |

### Step 5: Add Emotional Engagement

**Techniques:**

1. **Relatable problems:**
   > "You know that sinking feeling when the deploy fails on Friday at 5pm? Yeah, we're going to prevent that."

2. **Celebration of wins:**
   > "And just like that, you've got a working system. Not bad for 10 minutes of work."

3. **Empathy for struggles:**
   > "If this seems confusing, you're not alone. This trips up most people the first time."

4. **Humor (light):**
   > "The official documentation is... let's say 'comprehensive.' Here's the version that won't put you to sleep."

### Step 6: Read Aloud Test

Read the humanized content out loud. Ask:
- Would I actually say this to a colleague?
- Does it flow naturally?
- Any phrases that make me cringe?

If anything sounds "written," keep refining.

---

## Quick Reference Card

### Inject These
- Rhetorical questions ("Sound familiar?")
- Short punchy sentences
- Personal pronouns ("I", "you", "we")
- Contractions ("you'll", "it's", "don't")
- Colloquialisms ("pretty cool", "not bad")
- Opinion markers ("honestly", "in my experience")

### Remove These
- All forbidden words (see ANTI-PATTERNS.md)
- Em dashes
- "In this article, we will..."
- "It's worth noting that..."
- "Let's dive into..."
- Perfectly parallel lists
- All sentences same length

### Transform These
| Generic | Personalized |
|---------|--------------|
| "This is a common problem" | "You've probably hit this before" |
| "The solution involves" | "Here's how to fix it:" |
| "Users should consider" | "You'll want to think about" |
| "It is recommended to" | "I'd suggest" or "Try this:" |
| "One approach is to" | "What works for me:" |

---

## Example Transformation

### Before (AI-Sounding)

> "In this section, we will explore the fundamentals of container networking. It is important to note that understanding these concepts is crucial for successful deployment orchestration. Docker containers utilize isolated network namespaces, which provides a comprehensive solution for application isolation. Furthermore, this approach enables seamless communication between containers while maintaining security boundaries."

### After (Humanized)

> "Container networking trips up a lot of people. Here's what you actually need to know.
>
> Docker gives each container its own little network bubble. They can't see each other by default - which is exactly what you want for security. But then how do they talk?
>
> That's where bridge networks come in. Think of it as a virtual ethernet switch inside your Docker host. Connect your containers to it, and boom - they can communicate. Simple as that."

**Changes Made:**
- Removed "In this section, we will explore"
- Removed "It is important to note"
- Removed "crucial" (forbidden)
- Removed "comprehensive" (forbidden)
- Removed "Furthermore"
- Removed "seamless" (forbidden)
- Added burstiness (varied sentence length)
- Added conversational markers
- Added analogy ("little network bubble", "virtual ethernet switch")
- Added personality ("boom", "Simple as that")

---

## Integration

This skill can be called by:
- `draft-writer` agent during writing
- `line-editor` agent during polish
- User directly via slash command

Reference:
- `../philosophy/VOICE-MANDATE.md`
- `../philosophy/ANTI-PATTERNS.md`
- `../memory/voice-samples.md`
