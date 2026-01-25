# Annotated Example: PDF Skill

Analysis of Anthropic's PDF skill showing complex skill structure with scripts and references.

**Source:** https://github.com/anthropics/skills/tree/main/skills/pdf

---

## Directory Structure

```
pdf/
├── SKILL.md          # Main instructions (~300 lines)
├── forms.md          # Form handling reference
├── reference.md      # API/library reference
├── scripts/          # Utility scripts (not loaded into context)
└── LICENSE.txt
```

**Key insight:** Content is split across multiple files for progressive disclosure. Claude loads only what's needed.

---

## Frontmatter Analysis

```yaml
---
name: pdf
license: Proprietary (details in LICENSE.txt)
description: When Claude needs to fill in a PDF form or programmatically
  process, generate, or analyze PDF documents at scale
---
```

**Notes:**
- `name: pdf` - Short, matches directory
- `description` - Specific about "fill in a PDF form" and "process, generate, or analyze"
- Includes trigger scenarios ("at scale" suggests when to use)

---

## Progressive Disclosure Pattern

### SKILL.md (Overview)
Provides:
- Quick start for common operations
- Library recommendations (pypdf, pdfplumber, reportlab)
- Command-line tools overview
- Links to detailed references

```markdown
## Quick start

Use pdfplumber for text extraction:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced topics

For form filling, see [forms.md](forms.md)
For detailed API reference, see [reference.md](reference.md)
```

### forms.md (Specialized Reference)
Loaded only when user needs form handling:
- PDF form field types
- Form filling techniques
- Validation patterns

### reference.md (Comprehensive API Docs)
Loaded only for advanced operations:
- All library methods
- Code examples
- Performance tips

**Why this works:** User asking "extract text from PDF" gets quick answer. User asking "fill complex form" gets detailed guidance. Context stays efficient.

---

## Library Recommendations Pattern

The skill recommends specific libraries for specific tasks:

```markdown
## Libraries

| Task | Library | Why |
|------|---------|-----|
| Text extraction | pdfplumber | Layout preservation |
| Creating PDFs | reportlab | Full control |
| Basic operations | pypdf | Merge, split, rotate |
```

**Key insight:** Don't present all options equally. Guide toward the right tool for each job.

---

## Command-Line Tools Section

Provides alternatives when Python isn't available:

```markdown
## Command-line tools

- **pdftotext** (poppler-utils) - Fast text extraction
- **qpdf** - Merge, split, decrypt
- **pdftk** - Form filling, metadata
```

**Key insight:** Cover multiple approaches but organize by use case.

---

## Scripts Directory

Contains utility scripts that Claude executes (not loads):

```
scripts/
├── analyze_form.py    # Extract form fields
├── fill_form.py       # Apply values to form
└── validate.py        # Check form output
```

**How referenced in SKILL.md:**

```markdown
## Form analysis workflow

1. Run: `python scripts/analyze_form.py input.pdf`
2. Review extracted fields in `fields.json`
3. Fill values, then run: `python scripts/fill_form.py input.pdf fields.json output.pdf`
```

**Key insight:** Scripts are executed, not loaded. Only output consumes context.

---

## Techniques to Learn

### 1. Split by Use Case
Not all users need all information:
- Quick start for common cases
- Detailed references for advanced cases
- Scripts for complex workflows

### 2. Library Recommendations Table
Guide users to right tool:
```markdown
| Task | Use | Why |
|------|-----|-----|
| X | Library A | Reason |
| Y | Library B | Reason |
```

### 3. Workflow with Scripts
For complex multi-step operations:
```markdown
## Workflow

1. Run: `python scripts/step1.py input`
2. Review output
3. Run: `python scripts/step2.py intermediate output`
```

### 4. Reference Links
Keep main file concise:
```markdown
For advanced usage, see [reference.md](reference.md)
```

---

## What Makes This Skill Effective

1. **Concise main file** - Quick answers for common tasks
2. **Progressive depth** - Details available when needed
3. **Clear organization** - By task type, not by library
4. **Executable scripts** - Complex operations without context cost
5. **Multiple approaches** - Python libraries AND command-line tools
6. **Specific recommendations** - "Use X for Y" instead of "you can use X or Y or Z"

---

## How to Apply This Pattern

For skills with:
- Multiple libraries/tools
- Common + advanced use cases
- Complex multi-step workflows

Structure as:
```
my-skill/
├── SKILL.md          # Overview + quick start + links
├── [topic]-ref.md    # Detailed reference for topic
├── scripts/          # Utility scripts
│   └── helper.py
└── LICENSE.txt       # If distributing
```

In SKILL.md:
```markdown
# Quick Start
[Common operations with code]

# Advanced
- For [topic]: See [topic-ref.md](topic-ref.md)
- For [workflow]: Run `python scripts/helper.py`
```
