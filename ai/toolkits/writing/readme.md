# writing toolkit

A 10-layer orchestrated writing system for blogs, books, and documentation.

---

## how to use

### option 1: paste a command

Copy the content of any file in `commands/` and paste it into Claude to activate that workflow.

```
Example: Copy contents of commands/write-blog.md → Paste into chat
```

### option 2: reference files directly

Tell Claude to read and follow a specific file:

```
"Read ai/toolkits/writing/commands/write-blog.md and follow those instructions"
```

### option 3: manual agent invocation

For granular control, invoke specific agents:

```
"Use the context-gatherer agent from ai/toolkits/writing/agents/context-gatherer.md to gather context for my blog post about Docker networking"
```

---

## what each folder does

| folder | purpose | how to use |
|--------|---------|------------|
| `commands/` | entry points - start here | paste or reference to begin a workflow |
| `agents/` | specialized agents for each layer | called by commands, or invoke directly |
| `philosophy/` | rules for voice, quality, anti-patterns | agents reference these automatically |
| `templates/` | document structure templates | used by agents to format outputs |
| `skills/` | reusable capabilities | call for specific tasks (humanize, check flow) |
| `memory/` | your voice fingerprint | agents read this to match your style |

---

## available commands

### creating new content

| command | what it does |
|---------|--------------|
| `write-blog` | full 10-layer workflow for blog posts |
| `write-outline` | just context + outline (quick) |
| `write-section` | write one section from a plan |
| `write-book-chapter` | full workflow for book chapters |
| `write-docs` | full workflow for documentation |

### editing existing content

| command | what it does |
|---------|--------------|
| `write-review` | analyze for voice, AI tells, quality |
| `write-polish` | line edit to humanize content |
| `write-fact-check` | verify claims, links, code |

---

## the 10-layer pipeline

When you run a full workflow (`write-blog`, `write-book-chapter`, `write-docs`):

```
1. context      → gather topic, audience, goals
2. outline      → create high-level structure
3. review       → YOU approve outline ✓
4. section plan → detail each section
5. map review   → YOU approve detailed plan ✓
6. write        → draft the content
7. line edit    → polish voice and flow
8. copy edit    → grammar, consistency
9. fact-check   → verify claims, gather resources
10. assemble    → final publication-ready output ✓
```

checkmarks (✓) = user approval gates

---

## quick examples

### write a new blog post
```
Paste contents of: commands/write-blog.md
Then answer the questions it asks you
```

### polish existing content
```
Paste contents of: commands/write-polish.md
Then paste your content when asked
```

### just get an outline
```
Paste contents of: commands/write-outline.md
```

### check content for AI smell
```
Paste contents of: commands/write-review.md
```

---

## key files to know

| file | what it contains |
|------|------------------|
| `memory/voice-samples.md` | your writing patterns - edit to update your voice |
| `philosophy/anti-patterns.md` | forbidden words and AI tells to avoid |
| `philosophy/voice-mandate.md` | rules for preserving authentic voice |
| `philosophy/quality-standards.md` | readability and cognitive load standards |

---

## directory structure

```
writing/
├── readme.md           # you are here
├── commands/           # 8 workflow entry points
│   ├── write-blog.md
│   ├── write-outline.md
│   ├── write-section.md
│   ├── write-review.md
│   ├── write-polish.md
│   ├── write-fact-check.md
│   ├── write-book-chapter.md
│   └── write-docs.md
├── agents/             # 11 specialized agents
├── philosophy/         # 3 mandate files
├── templates/          # 7 document templates
├── skills/             # 5 reusable skills
└── memory/             # voice samples
```

---

## tips

- **start simple:** use `write-polish` on existing content to see immediate value
- **full workflow:** use `write-blog` when starting from scratch
- **update your voice:** edit `memory/voice-samples.md` with your own writing examples
- **check the forbidden list:** `philosophy/anti-patterns.md` has words that make writing smell like AI
