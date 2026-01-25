# Annotated Example: Skill Creator

Analysis of Anthropic's skill-creator showing a meta-skill that creates other skills.

**Source:** https://github.com/anthropics/skills/tree/main/skills/skill-creator

---

## Why This Skill Matters

This is a "meta-skill" - it teaches Claude how to create skills. Studying it reveals Anthropic's best practices for skill design.

---

## Key Principles from skill-creator

### 1. Context Window is a Public Good

> "The context window is a public good. Only include information Claude doesn't already have."

**Application:** Challenge each piece of information:
- "Does Claude really need this?"
- "Can I assume Claude knows this?"
- "Does this justify its token cost?"

### 2. Appropriate Constraints

> "Match specificity to task fragility."

| Task Type | Freedom Level | Approach |
|-----------|--------------|----------|
| Fragile operations | Low | Exact scripts, no variation |
| Preferred patterns | Medium | Pseudocode, parameters |
| Context-dependent | High | Text instructions, heuristics |

**Analogy provided:**
- **Narrow bridge with cliffs:** One safe way → specific guardrails (low freedom)
- **Open field:** Many paths work → general direction (high freedom)

### 3. Progressive Disclosure

Loading order:
1. **Metadata** (~100 tokens) - Always loaded
2. **SKILL.md body** (<5000 tokens) - On activation
3. **Referenced files** - On demand
4. **Scripts** - Executed, not loaded

---

## Skill Structure Guidance

### Required Components

```markdown
Every skill needs:
1. SKILL.md with YAML frontmatter
   - name (required)
   - description (required, critical for triggering)
2. Markdown body with instructions
```

### Optional Components

```
skill-name/
├── SKILL.md              # Required
├── scripts/              # Executable code
│   └── helper.py         # Executed, not loaded
├── references/           # Detailed documentation
│   └── api.md            # Loaded on demand
└── assets/               # Templates, boilerplate
    └── template.json     # Used in output, not loaded
```

**Key insight:** Different directories have different purposes:
- `scripts/` - Executed (output goes to context)
- `references/` - Loaded when Claude needs details
- `assets/` - Used in generated output

---

## Workflow Pattern

The skill-creator recommends this workflow:

### 1. Understand
Gather concrete examples:
- What inputs does the skill receive?
- What outputs should it produce?
- What are common edge cases?

### 2. Plan
Identify reusable components:
- Scripts for deterministic operations
- References for detailed documentation
- Assets for output templates

### 3. Initialize
Create skill structure with provided scripts:
```bash
python scripts/init_skill.py my-skill
```

### 4. Edit
Customize:
- SKILL.md with instructions
- Add references as needed
- Add scripts for complex operations

### 5. Package
Prepare for distribution:
```bash
python scripts/package_skill.py my-skill
```

### 6. Iterate
Test and refine:
- Test with real tasks
- Observe how Claude uses the skill
- Refine based on actual usage

---

## Description Writing Guidance

The skill emphasizes description quality:

> "Write descriptions comprehensively—this triggers skill selection."

**Good description elements:**
1. **What** the skill does
2. **When** to use it
3. **Keywords** that match user queries

```yaml
# Comprehensive
description: Extract text and tables from PDF files, fill forms, merge documents.
  Use when working with PDF files or when the user mentions PDFs, forms,
  or document extraction.

# Too vague (triggers incorrectly or not at all)
description: Helps with documents
```

---

## Avoiding Auxiliary Documentation

The skill advises against:
- README files (information belongs in SKILL.md)
- CHANGELOG files (version in metadata)
- Separate "getting started" docs

**Why:** Claude reads SKILL.md. Extra files fragment the knowledge.

**Exception:** For complex skills with many operations, a README.md for **human** users can be helpful (like `jira/README.md`).

---

## Key Takeaways

### For Skill Authors

1. **Challenge every token** - Only include what Claude doesn't know
2. **Match constraints to risk** - Fragile ops need specific scripts
3. **Description is critical** - Determines when skill activates
4. **Progressive disclosure** - Keep main file concise, details elsewhere
5. **Test with real usage** - Iterate based on actual Claude behavior

### For Skill Structure

1. **SKILL.md** - Overview and quick start (<500 lines)
2. **references/** - Detailed docs loaded on demand
3. **scripts/** - Deterministic operations (executed, not loaded)
4. **assets/** - Templates for output generation

### For Development Process

1. Start with concrete examples
2. Identify what's reusable
3. Create minimal viable skill
4. Test with real tasks
5. Iterate based on observation

---

## Application to Your Skills

When creating a new skill:

1. **Ask:** "What does Claude not already know?"
2. **Structure:** Put quick-start in SKILL.md, details in references
3. **Describe:** Include what, when, and keywords
4. **Test:** Run the skill on real tasks
5. **Iterate:** Refine based on how Claude actually uses it

The skill-creator demonstrates that good skill design is about **efficient context usage** and **clear triggering**, not comprehensive documentation.
