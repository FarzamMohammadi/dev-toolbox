---
name: repo-docs-overhaul
description: Overhaul a repository's documentation layer for clarity and navigability. Rewrites root README, creates section READMEs, renames vague files, adds contributor guides, and codifies documentation conventions. Use when a repo needs to be made OSS-ready or its docs feel generic/sparse.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
argument-hint: [repo-path]
---

# Philosophy

**Reader's time is sacred.** Every sentence transfers knowledge. Generic descriptions, vague filenames, and filler text waste the reader's most valuable resource — their attention.

This skill transforms a repo's documentation layer so that anyone in the world can land on it and immediately understand what's inside, where to find it, and how it's organized — without clicking into files.

**Never modify technical content** (code, articles, research, configs). Only the documentation layer changes.

---

## Principles

- **Specific over generic** — "Sorting algorithms in C++ (bubble, merge, quick)" not "Algorithm implementations"
- **Tables for structured references** — not paragraphs listing items
- **Adapt to the repo** — discover existing conventions, don't impose a template
- **Ask when unsure** — use `AskUserQuestion` for grouping decisions, naming choices, structural ambiguity
- **Concise is kind** — a 3-line README is better than no README; don't over-document thin sections

---

## Workflow

### Step 1: Explore

Map the repo's full structure and read all existing documentation.

```
1. List all tracked files: git ls-files
2. Read: README.md, CLAUDE.md, CONTRIBUTING.md, any guidelines files
3. Read representative content files from each top-level section
4. Note: directory structure, naming conventions, content types, depth per section
```

**Output**: Mental model of what content lives where and how it's currently documented.

### Step 2: Diagnose

Identify documentation gaps by checking each item:

| Check | Symptom |
|-------|---------|
| Root README quality | Generic description, vague table, bullet list of content types |
| Section READMEs | Missing — top-level directories have no README.md |
| Vague filenames | Files named `random.md`, `misc.md`, `notes.md`, `stuff.md` |
| Contributor guide | No CLAUDE.md or CONTRIBUTING.md |
| Conventions doc | No documented naming/formatting/tone standards |
| Case consistency | Git index paths don't match filesystem case |

### Step 3: Confirm with User

Present the diagnosis and proposed changes via `AskUserQuestion`:

```
Found [N] documentation gaps in [repo-name]:

1. Root README — [specific issue]
2. Missing section READMEs — [which directories]
3. Vague filenames — [list them with proposed renames]
4. No contributor guide
5. No conventions documented

Proposed changes:
- [summary of what will be created/modified/renamed]

Anything you'd like adjusted before I proceed?
```

**Wait for confirmation before making any changes.**

### Step 4: Rename Vague Files

For each vague filename, determine the right name based on content:

| Content type | New name |
|-------------|----------|
| Collection of links | `reading-list.md` |
| Actual notes on a topic | Descriptive kebab-case name from the content |
| Empty placeholder | Delete (confirm with user first) |

Use `git mv` to preserve history. Fix case mismatches in the same pass.

### Step 5: Create Section READMEs

Add a README.md to every top-level content directory that lacks one.

**Template** (adapt to section size):

```markdown
# [Section Name]

[One sentence: what this section contains and at what depth.]

## Contents

| [File/Directory] | [Description] |
|-------------------|--------------|
| [item](./path/) | [Specific description of what's inside] |
```

**Guidelines:**
- One-liner must describe actual content, not category names
- Table descriptions should be specific enough to skip clicking
- Thin sections (1-2 files) get 3-5 lines total — don't pad
- Match the repo's existing formatting conventions (heading style, link format)
- If a section already has its own documentation system (like a CLAUDE.md), don't create a competing README

### Step 6: Rewrite Root README

Replace the root README with a sharp, scannable entry point.

**Structure:**

```markdown
# [Repo Name]

[One sentence capturing what this repo actually contains — specific technologies, topics, depth.]

> [Any important callouts (contributor guidelines, etc.)]

> **Note:** Sections listed alphabetically.

---

## Sections

| Section | What's inside |
|---------|--------------|
| [section](./section/) | [Specific, scannable description of actual contents] |
```

**Rules:**
- Hook line must mention concrete things (languages, topics, tools) — not abstract categories
- Table descriptions: specific enough that a reader knows whether to click
- No "Overview" section with generic bullet lists
- No fluff sentences ("This repository contains..." → just describe what it contains)

### Step 7: Create/Update CLAUDE.md

If no root-level AI contributor guide exists, create one.

**Content:**

```markdown
# [Repo Name]

[One-line purpose.]

## Structure
[Brief structure overview with pointer to root README.]

## Rules
- [Read conventions doc before changes]
- [Never modify technical content without explicit request]
- [Section README template convention]
- [Any repo-specific rules discovered in Step 1]

## Conventions
- [File naming convention + exceptions]
- [Documentation tone]
- [Numbered series pattern if applicable]
- [Defer to section-specific guides where they exist]
```

If CLAUDE.md already exists, update it to reference the new documentation patterns.

### Step 8: Update/Create Conventions Doc

If no conventions document exists (repo-guidelines.md, CONTRIBUTING.md, etc.), create one. If one exists, add sections for new patterns.

**New sections to codify:**

- **Section READMEs** — every top-level directory has a README.md
- **Link collections** — standard filename for curated link files (e.g., `reading-list.md`)
- **Documentation tone** — reader's time is sacred, active voice, concrete over abstract, no filler

### Step 9: Verify

```
1. Confirm no vague filenames remain: find . -name "random.md" -o -name "misc.md" -o -name "stuff.md"
2. Confirm all section READMEs exist: check each top-level directory
3. Confirm root README links resolve correctly
4. Confirm git status shows expected changes (renames, new files, modifications)
5. Read the root README as a newcomer — can you understand what's in each section without clicking?
```

---

## Constraints

- **Never modify technical content** — code, articles, research, configs are off-limits
- **Never reorganize folder structure** — existing grouping is intentional
- **Preserve git history** — use `git mv` for renames, not delete + create
- **No hardcoded paths** — skill works on any repo
- **Adapt, don't impose** — discover conventions before creating new ones
- **Ask before destructive changes** — deleting files, major renames, structural decisions
