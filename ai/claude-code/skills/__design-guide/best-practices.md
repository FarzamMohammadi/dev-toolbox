# Best Practices

Guidance for writing effective skills that Claude can discover and use successfully.

---

## Core Principles

### 1. Concise is Key

The context window is a **public good**. Your skill shares context with:
- System prompt
- Conversation history
- Other skills' metadata
- The user's actual request

**Default assumption:** Claude is already very smart. Only add context Claude doesn't already have.

Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

```markdown
# Good: Concise (~50 tokens)
## Extract PDF text

Use pdfplumber for text extraction:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

# Bad: Too verbose (~150 tokens)
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available...
```

### 2. Set Appropriate Degrees of Freedom

Match specificity to task fragility.

**High freedom** (text-based instructions):
Use when multiple approaches are valid, decisions depend on context.

```markdown
## Code review process
1. Analyze the code structure
2. Check for potential bugs
3. Suggest improvements
4. Verify adherence to conventions
```

**Medium freedom** (pseudocode or parameterized scripts):
Use when a preferred pattern exists but some variation is acceptable.

```markdown
## Generate report
Use this template and customize as needed:
```python
def generate_report(data, format="markdown"):
    # Process data, generate output
```

**Low freedom** (specific scripts, no parameters):
Use when operations are fragile, consistency is critical.

```markdown
## Database migration
Run exactly this script:
```bash
python scripts/migrate.py --verify --backup
```
Do not modify the command.
```

**Analogy:** Think of Claude navigating a path:
- **Narrow bridge with cliffs:** One safe way forward → low freedom, specific guardrails
- **Open field:** Many paths lead to success → high freedom, general direction

### 3. Write Effective Descriptions

The `description` field enables skill discovery. Claude uses it to choose the right skill from potentially 100+ available skills.

**Rules:**
- Write in **third person** (critical—first/second person causes discovery problems)
- Include both **what** and **when**
- Be **specific** and include key terms

```yaml
# Good - third person, specific, includes triggers
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Bad - vague
description: Helps with documents

# Bad - wrong person
description: I can help you process Excel files
```

---

## Progressive Disclosure Patterns

SKILL.md serves as an overview pointing to detailed materials. Think of it as a table of contents.

### Pattern 1: High-Level Guide with References

```markdown
---
name: pdf-processing
description: Extract text from PDFs, fill forms, merge documents...
---

# PDF Processing

## Quick start
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features
- **Form filling**: See [forms.md](forms.md)
- **API reference**: See [reference.md](reference.md)
- **Examples**: See [examples.md](examples.md)
```

Claude loads additional files only when needed.

### Pattern 2: Domain-Specific Organization

For skills with multiple domains, organize by domain to avoid loading irrelevant context.

```
bigquery-skill/
├── SKILL.md
└── reference/
    ├── finance.md
    ├── sales.md
    └── product.md
```

```markdown
# BigQuery Data Analysis

## Available datasets
- **Finance**: Revenue, ARR, billing → See [reference/finance.md]
- **Sales**: Pipeline, accounts → See [reference/sales.md]
- **Product**: API usage, features → See [reference/product.md]
```

When asking about revenue, Claude only loads `finance.md`.

### Pattern 3: Conditional Details

Show basic content, link to advanced:

```markdown
# DOCX Processing

## Creating documents
Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents
For simple edits, modify XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

---

## Workflows and Feedback Loops

### Use Workflows for Complex Tasks

Break complex operations into clear, sequential steps. For particularly complex workflows, provide a checklist:

```markdown
## PDF form filling workflow

Copy this checklist and track progress:
```
- [ ] Step 1: Analyze form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**
Run: `python scripts/analyze_form.py input.pdf`
...
```

### Implement Feedback Loops

**Common pattern:** Run validator → fix errors → repeat

```markdown
## Document editing process

1. Make edits to `word/document.xml`
2. **Validate immediately**: `python scripts/validate.py dir/`
3. If validation fails:
   - Review error message
   - Fix issues in XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python scripts/pack.py dir/ output.docx`
```

Validation loops catch errors early.

---

## Content Guidelines

### Avoid Time-Sensitive Information

Don't include information that will become outdated:

```markdown
# Bad - will become wrong
If you're doing this before August 2025, use the old API.

# Good - use "old patterns" section
## Current method
Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used: `api.example.com/v1/messages`
</details>
```

### Use Consistent Terminology

Choose one term and use it throughout:

```markdown
# Good - consistent
- Always "API endpoint"
- Always "field"
- Always "extract"

# Bad - inconsistent
- Mix "API endpoint", "URL", "API route", "path"
- Mix "field", "box", "element", "control"
```

---

## Common Patterns

### Template Pattern

Provide templates for output format:

```markdown
## Report structure

Use this exact template:
```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1 with data
- Finding 2 with data

## Recommendations
1. Actionable recommendation
2. Actionable recommendation
```
```

### Examples Pattern

Provide input/output pairs:

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
```
fix(reports): correct date formatting in timezone conversion
```
```

### Conditional Workflow Pattern

Guide through decision points:

```markdown
## Document modification workflow

1. Determine the modification type:
   - **Creating new content?** → Follow "Creation workflow"
   - **Editing existing content?** → Follow "Editing workflow"

2. Creation workflow:
   - Use docx-js library
   - Build from scratch
   - Export to .docx

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

---

## Iterative Development

### Build Evaluations First

Create evaluations **before** writing extensive documentation:

1. **Identify gaps**: Run Claude on tasks without a skill. Document failures.
2. **Create evaluations**: Build 3 scenarios that test these gaps
3. **Establish baseline**: Measure performance without the skill
4. **Write minimal instructions**: Just enough to pass evaluations
5. **Iterate**: Execute, compare, refine

### Develop with Claude

Work with one Claude instance ("Claude A") to create a skill used by other instances ("Claude B"):

1. **Complete a task without a skill**: Note what context you repeatedly provide
2. **Identify reusable pattern**: What would be useful for similar future tasks?
3. **Ask Claude A to create a skill**: Capture the pattern
4. **Review for conciseness**: Remove unnecessary explanations
5. **Test with Claude B**: Use the skill on related tasks
6. **Iterate based on observation**: Refine when Claude B struggles

---

## Technical Notes

### Avoid Windows-Style Paths

Always use forward slashes:

```markdown
# Good
scripts/helper.py
reference/guide.md

# Bad
scripts\helper.py
```

### Avoid Too Many Options

Don't present multiple approaches unless necessary:

```markdown
# Bad - too many choices
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image...

# Good - provide default with escape hatch
Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
```

### Solve, Don't Punt

When writing scripts, handle errors explicitly:

```python
# Good - handle errors
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''

# Bad - punt to Claude
def process_file(path):
    return open(path).read()  # Just fail
```
