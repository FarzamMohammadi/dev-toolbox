---
name: claim-extractor
description: Extracts atomic, verifiable claims from research findings
---

# Claim Extractor Skill

> Transform narrative findings into atomic, categorized, verifiable claims that can be individually validated and scored.

---

## When to Use

- Phase 3 of Research Parliament (Claim Extraction)
- After receiving findings from Scholar, Investigator, Skeptic
- When preparing for validation

---

## What is an Atomic Claim?

An **atomic claim** is:
- A single, specific assertion
- Independently verifiable
- Not compound (no "and" combining multiple facts)
- Clear enough to confirm or refute

### Examples

**BAD (Compound)**:
"Vector databases use HNSW indexes and are faster than traditional databases for similarity search."

**GOOD (Atomic)**:
1. "Vector databases commonly use HNSW indexes."
2. "HNSW indexes are faster than brute-force for similarity search."

---

## Claim Categories

### FACTUAL
Objectively verifiable statements about reality.

Examples:
- "HNSW was introduced in 2016."
- "PostgreSQL 15 added support for HNSW indexes via pgvector."
- "OpenAI's GPT-4 was released in March 2023."

Verification: Can be confirmed with primary sources.

### OPINION
Subjective assessments, even from experts.

Examples:
- "HNSW is the best algorithm for vector search."
- "RAG is more practical than fine-tuning for most use cases."
- "The future of AI is in multi-agent systems."

Attribution: Always attribute to the source making the claim.

### PROJECTION
Predictions or forward-looking statements.

Examples:
- "Vector databases will become standard in enterprise by 2025."
- "AI will automate 30% of coding tasks within 5 years."
- "This approach will likely become the standard."

Handling: Note as projection, assess basis for prediction.

### METHODOLOGICAL
Claims about how things work or should be done.

Examples:
- "Chunking documents into 500-token segments improves retrieval."
- "Hybrid search combines dense and sparse retrieval."
- "Re-ranking improves precision at the cost of latency."

Verification: Check against implementations and research.

---

## Extraction Process

### Step 1: Read Source Material
Identify all statements that make claims about:
- Facts about the world
- How things work
- What's recommended
- What will happen
- What's true/false

### Step 2: Decompose Compound Statements
```
Source: "RAG systems use vector databases for efficient semantic
search, which dramatically improves relevance compared to keyword search."

Extract:
1. "RAG systems use vector databases for semantic search." (FACTUAL)
2. "Vector databases enable efficient semantic search." (FACTUAL)
3. "Semantic search improves relevance compared to keyword search." (METHODOLOGICAL)
```

### Step 3: Categorize Each Claim
- FACTUAL: Can be verified objectively
- OPINION: Subjective, even if from expert
- PROJECTION: About the future
- METHODOLOGICAL: About processes/practices

### Step 4: Note Provenance
For each claim, record:
- Source URL
- Source tier
- Author (if known)
- Date (if known)
- Context (what section/discussion)

### Step 5: Map to Sub-Questions
Connect each claim to which research sub-question it addresses.

---

## Output Format

```markdown
## Extracted Claims

### Summary
- Total claims: [N]
- Factual: [N]
- Opinion: [N]
- Projection: [N]
- Methodological: [N]

### Claim List

#### Claim 1
- **Text**: "[claim statement]"
- **Category**: FACTUAL
- **Source**: [url or title]
- **Source Tier**: [1-6]
- **Sub-question**: Q[N] - [question text]
- **Context**: [where in source this appeared]

#### Claim 2
- **Text**: "[claim statement]"
- **Category**: OPINION
- **Attribution**: [who said this]
- **Source**: [url or title]
- **Source Tier**: [1-6]
- **Sub-question**: Q[N]
- **Context**: [context]

[Continue for all claims...]

### Conflicts Identified

| Claim A | Claim B | Nature of Conflict |
|---------|---------|-------------------|
| [claim] | [contradicting claim] | [description] |

### Coverage Map

| Sub-Question | # Claims | Categories |
|--------------|----------|------------|
| Q1 | 5 | 3 FACTUAL, 2 METHODOLOGICAL |
| Q2 | 3 | 1 FACTUAL, 1 OPINION, 1 PROJECTION |
| ... | ... | ... |
```

---

## Extraction Guidelines

### Be Specific
```
VAGUE: "Vector databases are fast."
SPECIFIC: "Vector databases with HNSW indexes can search millions of vectors in milliseconds."
```

### Preserve Nuance
```
LOST NUANCE: "RAG works."
PRESERVED: "RAG works well for factual Q&A with structured documents."
```

### Include Conditions
```
UNCONDITIONAL: "Use 512-token chunks."
CONDITIONAL: "512-token chunks work well for general Q&A; technical docs may need larger chunks."
```

### Note Uncertainty
```
CERTAIN: "HNSW is O(log n) for search."
UNCERTAIN: "HNSW may achieve O(log n) search under certain conditions."
```

---

## Common Patterns

### From Academic Papers
- Abstract claims (high-level findings)
- Methodology claims (how they did it)
- Results claims (what they found)
- Limitation claims (what didn't work)

### From Blog Posts
- Experience claims (what author encountered)
- Recommendation claims (what author suggests)
- Comparison claims (X vs Y)

### From Documentation
- Capability claims (what software does)
- Usage claims (how to use it)
- Limitation claims (what it can't do)

### From News
- Event claims (what happened)
- Quote claims (what someone said)
- Analysis claims (interpretation)

---

## Claim Conflict Detection

### Types of Conflicts

**Direct Contradiction**:
- Claim A: "X is true"
- Claim B: "X is false"

**Scope Conflict**:
- Claim A: "X always works"
- Claim B: "X fails in Y cases"

**Degree Conflict**:
- Claim A: "X is very effective"
- Claim B: "X is somewhat effective"

**Temporal Conflict**:
- Claim A (2022): "X is the best approach"
- Claim B (2024): "X is outdated"

### Flagging Conflicts
When detected:
1. Note both claims
2. Identify conflict type
3. Note sources for each
4. Flag for Validator attention

---

## Quality Checks

### Each Claim Should:
- [ ] Be a single assertion (atomic)
- [ ] Be clear and specific
- [ ] Have a source attribution
- [ ] Have a category
- [ ] Map to a sub-question
- [ ] Preserve original nuance
