---
name: write-docs
description: Full orchestrated workflow for technical documentation. Optimized for reference material, guides, and API docs with scannability focus.
---

# /write-docs - Documentation Workflow

You are creating technical documentation using the full 10-layer pipeline, adjusted for reference-style content.

## Key Differences from Blog

| Aspect | Blog | Documentation |
|--------|------|---------------|
| Purpose | Teach/engage | Reference/complete tasks |
| Voice | Conversational | Direct, concise |
| Structure | Narrative flow | Scannable, hierarchical |
| Personality | Strong | Minimal |
| Examples | Story-driven | Task-focused |
| Format | Long-form | Modular, linked |

## Documentation Types

### Reference Documentation
- API references
- Configuration options
- Command references
- Schema documentation

### Guide Documentation
- How-to guides
- Integration guides
- Troubleshooting guides
- Best practices

### Tutorial Documentation
- Getting started
- Step-by-step walkthroughs

## Workflow Modifications

### Layer 1: Context (Modified)

Additional questions:
- Documentation type (reference/guide/tutorial)?
- Product/feature being documented?
- Version?
- Prerequisites for reader?
- Related documentation to link?

### Layer 2: Outline (Modified)

Documentation structure:
```markdown
# [Product/Feature Name]

## Document Type: [Reference/Guide/Tutorial]
## Version: [X.Y]
## Prerequisites: [List]

---

## Overview
[What and why]

## Quick reference
[Key info at a glance]

## [Main content sections]
[Varies by type]

## Troubleshooting
[Common issues]

## FAQ
[Common questions]

## Related resources
[Links]
```

### Layer 6: Writing (Modified)

Documentation-specific rules:
- Active voice always
- Second person ("you")
- Present tense
- Define terms on first use
- Be direct, not conversational
- Use consistent terminology
- Include all code examples tested

### Layer 10: Assembly (Modified)

Documentation elements:
- Clear title
- Version information
- Prerequisites listed
- Quick reference table
- Hierarchical headings
- Consistent callout styles
- Code blocks with language specified
- Cross-references to related docs

## Template

Reference: `ai/toolkits/writing/templates/documentation-template.md`

## Style Guide for Docs

### Do
- Use active voice
- Be direct and concise
- Define terms on first use
- Use consistent formatting
- Include all steps
- Test all code

### Don't
- Use conversational tone
- Include unnecessary personality
- Assume knowledge without stating
- Skip steps
- Leave commands untested

### Formatting

| Element | Format |
|---------|--------|
| File paths | `monospace` |
| Commands | `$ command` |
| Code blocks | ```language |
| Variables | `UPPER_SNAKE` |
| Placeholders | `<placeholder>` |

### Callouts

```markdown
> **Note:** Helpful but not critical

> **Important:** User needs to know

> **Warning:** Could cause problems

> **Tip:** Optional improvement
```

## Instructions

### Getting Started

Ask:
1. What are you documenting? (product/feature)
2. Documentation type? (reference/guide/tutorial)
3. Version?
4. Target audience (developer/admin/user)?
5. Prerequisites?
6. Related docs to reference?

### Quality for Documentation

- All code tested
- All commands verified
- Consistent terminology
- Complete (no gaps)
- Scannable structure
- Cross-references included

## Begin

Start with: "Let's create documentation! What product or feature are you documenting?"
