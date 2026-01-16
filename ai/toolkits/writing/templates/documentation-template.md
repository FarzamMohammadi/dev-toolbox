# Documentation Template

> **Instructions:** This template is for technical documentation - reference material, guides, and API docs. Prioritizes scannability, accuracy, and task completion.

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Document Type** | [Reference / Guide / Tutorial / API] |
| **Product/Feature** | |
| **Version** | |
| **Last Updated** | |
| **Audience** | [Developer / Admin / End User] |
| **Prerequisites** | |

---

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
- Example implementations

---

## Standard Structure

### Title and Overview

```markdown
# [Feature/Product Name]

[One-sentence description of what this is]

## Overview

[2-3 paragraphs covering:]
- What this does
- When to use it
- Key concepts

## Quick reference

| Item | Description |
|------|-------------|
| [Key term] | [Brief definition] |
| [Key term] | [Brief definition] |
```

---

### Prerequisites Section

```markdown
## Prerequisites

Before you begin, ensure you have:

- [ ] [Requirement 1] - [Brief note on how to verify]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

**Versions tested:** [List compatible versions]
```

---

### Installation/Setup Section

```markdown
## Installation

### Option 1: [Method name]

```bash
[installation command]
```

### Option 2: [Alternative method]

[Instructions]

### Verify installation

```bash
[verification command]
```

Expected output:
```
[expected output]
```
```

---

### Usage Section

```markdown
## Usage

### Basic usage

```[language]
[minimal working example]
```

### Common patterns

#### [Pattern 1 name]

```[language]
[code example]
```

**When to use:** [Brief explanation]

#### [Pattern 2 name]

[...]
```

---

### Configuration Section

```markdown
## Configuration

### Configuration file

Location: `[path]`

```[format]
[example configuration]
```

### Configuration options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | string | `"default"` | [What it does] |
| `option2` | boolean | `false` | [What it does] |
| `option3` | number | `100` | [What it does]. Range: 1-1000 |

### Environment variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VAR_NAME` | [What it controls] | `value` |
```

---

### API Reference Section (If Applicable)

```markdown
## API Reference

### `functionName(param1, param2)`

[Brief description]

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `param1` | `string` | Yes | [Description] |
| `param2` | `object` | No | [Description] |

**Returns:** `ReturnType` - [Description]

**Example:**

```[language]
[usage example]
```

**Throws:**
- `ErrorType` - [When this occurs]
```

---

### Troubleshooting Section

```markdown
## Troubleshooting

### [Problem description]

**Symptoms:** [What the user sees]

**Cause:** [Why this happens]

**Solution:**

1. [Step 1]
2. [Step 2]

**Prevention:** [How to avoid this]

---

### [Another problem]

[...]
```

---

### FAQ Section

```markdown
## FAQ

### [Common question 1]?

[Concise answer]

### [Common question 2]?

[Concise answer]
```

---

### Related Resources Section

```markdown
## Related resources

- [Resource 1](url) - [Why relevant]
- [Resource 2](url) - [Why relevant]

## See also

- [Related doc 1]
- [Related doc 2]
```

---

## Style Guidelines for Documentation

### Writing Style

| Do | Don't |
|----|-------|
| Use active voice | Use passive voice |
| Be direct and concise | Be verbose |
| Use second person ("you") | Use first person ("we") |
| Use present tense | Use future tense |
| Define terms on first use | Assume knowledge |

### Formatting Conventions

| Element | Format |
|---------|--------|
| File paths | `monospace` |
| Code | ```language blocks |
| Commands | `$ command` |
| Variables | `UPPER_SNAKE_CASE` |
| Placeholders | `<placeholder>` |
| Optional items | `[optional]` |

### Callout Types

```markdown
> **Note:** Helpful information that isn't critical.

> **Important:** Information the user needs to know.

> **Warning:** Something that could cause problems if ignored.

> **Tip:** Optional advice to improve the experience.
```

---

## Complete Example Structure

```markdown
# Widget API

High-performance widget management for Node.js applications.

## Overview

The Widget API provides programmatic access to widget creation, configuration, and lifecycle management.

## Quick reference

| Method | Description |
|--------|-------------|
| `create()` | Creates a new widget |
| `configure()` | Updates widget settings |
| `destroy()` | Removes a widget |

## Prerequisites

- Node.js 18+
- npm or yarn

## Installation

```bash
npm install @company/widget-api
```

## Basic usage

```javascript
import { Widget } from '@company/widget-api';

const widget = await Widget.create({ name: 'my-widget' });
```

## Configuration

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `name` | string | required | Widget identifier |
| `timeout` | number | 5000 | Operation timeout in ms |

## API Reference

### `Widget.create(options)`

Creates a new widget instance.

[Full documentation...]

## Troubleshooting

### Widget fails to initialize

**Symptoms:** Error "WIDGET_INIT_FAILED"

**Solution:** Verify credentials are set...

## FAQ

### How do I handle rate limits?

The API automatically handles rate limiting...

## Related resources

- [Widget Best Practices Guide](url)
- [API Changelog](url)
```

---

## Quality Checklist

- [ ] Purpose clear from title and overview
- [ ] Prerequisites explicitly listed
- [ ] Installation steps verified
- [ ] All code examples tested
- [ ] Configuration options complete
- [ ] API signatures accurate
- [ ] Error scenarios documented
- [ ] Troubleshooting covers common issues
- [ ] Related resources linked
- [ ] Version information current
- [ ] Formatting consistent
- [ ] No broken links
