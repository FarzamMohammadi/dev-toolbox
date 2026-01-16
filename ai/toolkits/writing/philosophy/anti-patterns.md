# Anti-Patterns Mandate

> **Purpose:** Catalog everything that makes writing smell of AI and provide concrete fixes. This is your detection and elimination guide.

---

## Core Principle

**If a reader suspects AI wrote it, you've failed.** This document defines the specific tells that expose AI-generated content and provides alternatives that pass the human test.

---

## Forbidden Words

These words are statistically overused by AI models and instantly signal machine generation:

### Tier 1: Absolute Blacklist (Never Use)

| Forbidden | Why | Alternatives |
|-----------|-----|--------------|
| delve | AI's favorite word | explore, examine, look at, get into |
| tapestry | Poetic cliché | mix, combination, blend |
| vibrant | Empty descriptor | active, busy, energetic, specific adjective |
| landscape | Metaphor abuse | space, field, market, area |
| realm | Fantasy novel leak | area, domain, space, field |
| embark | Overly formal | start, begin, kick off |
| myriad | Pretentious | many, numerous, lots of |
| multifaceted | Consultant speak | complex, varied, many-sided |
| furthermore | Robotic connector | also, and, plus |
| moreover | Academic padding | also, and, what's more |
| comprehensive | Self-congratulatory | thorough, complete, full |
| intricate | Vague complexity | complex, detailed, specific description |
| pivotal | Overhyped importance | important, key, critical |
| arguably | Hedging | [just state the claim] |
| notably | Unnecessary emphasis | [remove and just state it] |
| crucial | Overused emphasis | important, essential, key |
| seamlessly | Marketing speak | smoothly, easily, without issues |
| leverage | Corporate jargon | use, apply, take advantage of |
| utilize | Fancy "use" | use |
| facilitate | Bureaucratic | help, enable, make possible |
| paradigm | Buzzword | model, approach, framework |
| synergy | Empty corporate | [describe actual benefit] |
| robust | Tech marketing | strong, reliable, solid |
| scalable | Often meaningless | [describe actual capacity] |
| cutting-edge | Cliché | new, latest, advanced |
| game-changer | Hyperbole | significant improvement, breakthrough |
| empower | Corporate fluff | enable, help, give [specific ability] |
| impactful | Not a real word | effective, significant, powerful |

### Tier 2: Use Sparingly (Once per 1000 words max)

| Word | When Acceptable |
|------|-----------------|
| innovative | Only for genuinely new things |
| essential | Only for truly required items |
| significant | Only for measurable significance |
| unique | Only for genuinely one-of-a-kind |
| transform | Only for actual transformations |
| optimize | Only for actual optimization work |

---

## Forbidden Phrases

### Opening Phrases (Never Start With)

| Forbidden | Problem | Fix |
|-----------|---------|-----|
| "In this article, we will..." | Robotic meta-commentary | Jump into content |
| "Welcome to this guide..." | Unnecessary greeting | Start with hook |
| "In today's digital age..." | Cliché + dated | Be specific about context |
| "Have you ever wondered..." | Clickbait pattern | State the problem directly |
| "In the ever-evolving world of..." | Empty padding | Get to the point |
| "As technology continues to advance..." | Generic filler | Specific context |

### Transition Phrases (Eliminate)

| Forbidden | Problem | Fix |
|-----------|---------|-----|
| "It's important to note that..." | Condescending | Just state it |
| "It's worth mentioning..." | Padding | Just mention it |
| "Let's dive into..." | Overused AI phrase | "Here's how it works:" |
| "Let's explore..." | Vague AI pattern | Specific action |
| "Let's take a look at..." | Filler | Just look at it |
| "Moving forward..." | Corporate speak | [remove or be specific] |
| "That being said..." | Unnecessary hedge | [remove] |
| "At the end of the day..." | Cliché | [remove] |
| "In a nutshell..." | Dated expression | "In short:" or just summarize |
| "Without further ado..." | Filler | [remove] |

### Closing Phrases (Never End With)

| Forbidden | Problem | Fix |
|-----------|---------|-----|
| "In conclusion..." | Announces the obvious | Just conclude |
| "To sum up..." | Same problem | Just summarize |
| "In summary..." | Same problem | Just summarize |
| "Happy coding!" | AI signature | [remove or personalize] |
| "I hope this helps!" | Generic | [remove or be specific about what to do next] |

---

## Forbidden Formatting

### Typography to Avoid

| Pattern | Problem | Fix |
|---------|---------|-----|
| Em dashes (—) | Overused by AI | Use commas, parentheses, or split sentence |
| Excessive semicolons | Signals AI | Use periods, split into sentences |
| Colons in headings | Robotic | Rephrase without colon |
| ALL CAPS for emphasis | Aggressive | Bold or italics |
| Exclamation marks!!! | Forced enthusiasm | One max, sparingly |

### Structural Patterns to Avoid

| Pattern | Problem | Fix |
|---------|---------|-----|
| Numbered headings ("1. Introduction") | Academic/robotic | Descriptive headings |
| Perfectly parallel lists | Unnatural uniformity | Vary structure slightly |
| Every section same length | Too balanced | Natural variation |
| Three-item lists always | AI pattern | 2, 4, or 5 items sometimes |

---

## Sentence Pattern Detection

### The Uniformity Problem

AI tends to produce sentences of similar length and structure. Humans write with "burstiness" - dramatic variation.

**AI Pattern (Bad):**
> "Docker containers provide isolation for applications. They package code with dependencies. This ensures consistent behavior across environments. Teams can deploy with confidence."

**Human Pattern (Good):**
> "Docker containers? They're essentially isolated environments for your apps. Pack your code, throw in the dependencies, and boom - it runs the same everywhere. No more 'works on my machine' excuses."

### Achieving Burstiness

Mix:
- Very short sentences. Like this.
- Medium-length sentences that explain a single concept clearly.
- Longer sentences that might combine multiple ideas, use dashes or parentheses, and create a more complex rhythm that mirrors natural speech patterns.

**Target:** Standard deviation of sentence length should be high, not low.

---

## AI-Specific Tell Detection

### The "Setup" Pattern

AI often sets up information before delivering it:

**AI Pattern (Bad):**
> "Before we begin, it's important to understand the basics. Let me explain the fundamentals. First, we need to establish..."

**Human Pattern (Good):**
> "Here's what you need to know: [actual information]"

### The "Completeness" Pattern

AI tries to be comprehensive, often padding with obvious statements:

**AI Pattern (Bad):**
> "Security is very important in software development. Without proper security, systems can be vulnerable to attacks. Therefore, we should implement security measures."

**Human Pattern (Good):**
> "Skip authentication at your own peril. Here's the minimum viable security setup that won't make you hate yourself later."

### The "Balanced" Pattern

AI hedges and balances excessively:

**AI Pattern (Bad):**
> "There are both advantages and disadvantages to consider. On one hand, X provides benefits. On the other hand, there are drawbacks."

**Human Pattern (Good):**
> "Look, X is great for [specific use]. But if you're doing [other thing], it'll drive you crazy. Here's when to use it and when to run."

---

## The Authenticity Test

### Read Aloud Check

Read the text aloud. Ask:
- Would a human actually say this?
- Does it sound like a conversation?
- Are there any phrases that feel "written" rather than "spoken"?

### The Friend Test

Imagine sending this to a friend. Would they:
- Roll their eyes at any phrase?
- Ask "did AI write this?"
- Feel talked down to?

### The 30% Replacement Rule

Replace approximately 30% of common words with less common synonyms (but still natural ones):
- "good" → "solid", "decent", "legit"
- "bad" → "rough", "painful", "a mess"
- "important" → "key", "critical", "the thing that matters"

---

## Recovery Protocols

### If Writing Feels Generic

1. Add a specific personal experience
2. Insert a strong opinion
3. Use informal language for one sentence
4. Add a rhetorical question
5. Include a mini-story or analogy

### If Writing Feels Over-Polished

1. Introduce sentence length variation
2. Start a sentence with "And" or "But"
3. Use a parenthetical aside (like this one)
4. Add an incomplete sentence. For effect.
5. Include a colloquialism

---

## Integration Points

This mandate applies to:
- **All Layers** - Forbidden words/phrases are universal
- **Layer 7** (Line Editor) - Primary enforcement
- **Layer 8** (Copy Editor) - Final sweep

Referenced by:
- `agents/draft-writer.md`
- `agents/line-editor.md`
- `agents/copy-editor.md`
- `skills/humanizer.md`

---

## Automated Detection (Future)

Consider implementing checks for:
- Forbidden word scanning
- Sentence length variance calculation
- Transition phrase detection
- Heading pattern analysis
