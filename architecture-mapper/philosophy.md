# Architecture Mapper Philosophy

## Core Belief

**Understanding comes from patterns, not pixels.**

A senior engineer ramping up on a new codebase doesn't need to read every line of code—they need to understand:

- **Where things live** - Directory structure, naming conventions, organizational patterns
- **How things connect** - Dependencies, data flow, coupling between components
- **What matters most** - Hotspots, high-churn areas, complexity centers
- **How the team thinks** - Patterns, conventions, architectural decisions

---

## Guiding Principles

### 1. High-Level First

Architecture over implementation details. Understand the forest before the trees.

A developer who grasps the system's shape can navigate to any corner. One who starts with details drowns in them.

### 2. Follow the Heat

Prioritize understanding code that changes frequently (hotspots). Dead code doesn't need your attention.

The 80/20 rule applies: 20% of files contain 80% of the action. Find them first.

### 3. Patterns Reveal Intent

How the team solved similar problems before tells you how to solve new ones.

Patterns aren't just technical—they're communication. They say "this is how we do things here."

### 4. History is Data

Git history is a goldmine:
- **Who knows what** - Author patterns reveal domain experts
- **What's coupled** - Files that change together are connected, even without explicit imports
- **What's fragile** - High-churn + high-complexity = dragons here

### 5. Automate Discovery

Manual exploration doesn't scale. Tools should surface insights automatically.

Reading code is expensive. Let machines do the scanning, humans do the thinking.

### 6. LLMs as Force Multipliers

Use AI to synthesize, summarize, and explain—not replace understanding.

LLMs can turn raw analysis into actionable insights, translate patterns into prose, and generate starting points for documentation. They can't replace the judgment that comes from actual understanding.

---

## Modular Design Philosophy

### Language-Agnostic Core

Statistics, git analysis, and visualization work on any repository regardless of language. These form the foundation.

### Language-Specific Plugins

AST analysis, call graphs, and type analysis are inherently language-specific. These are modular add-ons that plug into the core.

### Start Simple, Extend Later

Build Python analysis first—it's widely used and has excellent tooling. The architecture supports adding JavaScript/TypeScript, Go, Rust, etc. later without restructuring.

---

## What This Toolset Is Not

- **Not a linter** - We analyze architecture, not style
- **Not a test runner** - We understand structure, not correctness
- **Not a documentation generator** - We produce insights that inform documentation
- **Not a replacement for reading code** - We help you know what to read first

---

## Success Criteria

A developer using these tools should be able to:

1. **In 5 minutes**: Understand project structure and key directories
2. **In 30 minutes**: Identify the core components and how they connect
3. **In 2 hours**: Know where to look for any type of change
4. **In 1 day**: Be productive and know who to ask about what
