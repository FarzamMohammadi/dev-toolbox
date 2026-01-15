---
name: query-decomposer
description: Breaks research queries into actionable sub-questions
---

# Query Decomposer Skill

> Transform a broad research query into specific, actionable sub-questions that guide the research process.

---

## When to Use

- Phase 1 of Research Parliament (Understanding)
- When a query is too broad to research directly
- When the topic has multiple dimensions

---

## The Process

### Step 1: Identify Query Components

Parse the query for:
```
- Core topic (the main subject)
- Qualifiers (best, current, modern, etc.)
- Scope limiters (for X, in Y context, etc.)
- Implicit questions (what's really being asked)
- Time frame (current, historical, future)
```

### Step 2: Generate Sub-Questions

Create 3-7 sub-questions that:
1. Cover all aspects of the query
2. Are specific enough to search for
3. Are independent (can research in parallel)
4. Together, fully answer the original query

### Question Types to Include:
```
- WHAT: Definitions, components, mechanisms
- HOW: Implementation, process, methods
- WHY: Reasoning, benefits, motivations
- WHEN: Timing, conditions, context
- WHO: Key players, experts, users
- COMPARISON: Alternatives, trade-offs
- LIMITATION: Edge cases, problems, constraints
```

### Step 3: Prioritize

Rank sub-questions by:
1. Centrality to the original query
2. Dependency (some questions build on others)
3. Importance for user's likely intent

---

## Output Format

```markdown
## Query Decomposition

**Original Query**: "[user's query]"

**Core Topic**: [identified main subject]
**Scope**: [any limiters identified]
**Time Frame**: [current/historical/future]
**Implicit Intent**: [what they likely really want to know]

### Sub-Questions

| # | Question | Type | Priority | Dependencies |
|---|----------|------|----------|--------------|
| 1 | [question] | WHAT | HIGH | None |
| 2 | [question] | HOW | HIGH | Q1 |
| 3 | [question] | WHY | MEDIUM | None |
| 4 | [question] | COMPARISON | MEDIUM | Q1 |
| 5 | [question] | LIMITATION | HIGH | Q1, Q2 |

### Research Order
1. First: Q1, Q3 (no dependencies)
2. Then: Q2, Q4 (depend on Q1)
3. Finally: Q5 (depends on Q1, Q2)
```

---

## Examples

### Example 1: Technical Query

**Original**: "What are the current best practices for building production RAG systems?"

**Decomposition**:
| # | Question | Type | Priority |
|---|----------|------|----------|
| 1 | What is RAG and what are its core components? | WHAT | HIGH |
| 2 | What are the current recommended architectures for RAG systems? | HOW | HIGH |
| 3 | What retrieval strategies work best (dense, sparse, hybrid)? | HOW | HIGH |
| 4 | How should chunks be sized and documents be processed? | HOW | MEDIUM |
| 5 | What are common failure modes and how to avoid them? | LIMITATION | HIGH |
| 6 | How do production RAG systems differ from prototypes? | COMPARISON | MEDIUM |
| 7 | What evaluation methods and metrics should be used? | HOW | MEDIUM |

### Example 2: Comparative Query

**Original**: "Should I use PostgreSQL or MongoDB for my new project?"

**Decomposition**:
| # | Question | Type | Priority |
|---|----------|------|----------|
| 1 | What are the fundamental differences between PostgreSQL and MongoDB? | WHAT | HIGH |
| 2 | What use cases favor PostgreSQL over MongoDB? | WHEN | HIGH |
| 3 | What use cases favor MongoDB over PostgreSQL? | WHEN | HIGH |
| 4 | What are the performance characteristics of each? | COMPARISON | MEDIUM |
| 5 | What are the operational considerations (scaling, maintenance)? | HOW | MEDIUM |
| 6 | What are the limitations of each database? | LIMITATION | HIGH |

### Example 3: Exploratory Query

**Original**: "How is AI changing software engineering?"

**Decomposition**:
| # | Question | Type | Priority |
|---|----------|------|----------|
| 1 | What AI tools are currently used in software engineering? | WHAT | HIGH |
| 2 | How are AI coding assistants affecting developer productivity? | HOW | HIGH |
| 3 | What software engineering tasks are being automated by AI? | WHAT | HIGH |
| 4 | What are the limitations of AI in software engineering? | LIMITATION | HIGH |
| 5 | How might AI change software engineering roles in the future? | WHAT | MEDIUM |
| 6 | What skills are becoming more/less valuable due to AI? | WHAT | MEDIUM |

---

## Anti-Patterns

### Too Broad
```
BAD: "What is RAG?"
GOOD: "What are the core components and mechanisms of RAG systems?"
```

### Too Narrow
```
BAD: "What is the default chunk size in LangChain?"
GOOD: "What chunk sizes are recommended for different use cases in RAG systems?"
```

### Redundant
```
BAD: Including both "What are advantages?" and "Why is X good?"
GOOD: Combine into single question about benefits
```

### Missing Critical Dimension
```
BAD: Only asking "how to do X" without "when not to do X"
GOOD: Include limitations and counter-cases
```

---

## Quick Reference

**Minimum questions**: 3 (for simple queries)
**Maximum questions**: 7 (to prevent scope creep)
**Must include**: At least one LIMITATION question
**Prioritization**: Rank by centrality to user's intent
