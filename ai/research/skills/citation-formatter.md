---
name: citation-formatter
description: Formats citations consistently for research reports
---

# Citation Formatter Skill

> Format all citations consistently throughout the research report, including inline references and the full source list.

---

## When to Use

- Phase 7 of Research Parliament (Final Assembly)
- When creating the Sources section
- When adding inline citations to the report

---

## Citation Formats

### Inline Citations

Use numbered references in square brackets:
```
Vector databases commonly use HNSW indexes[1] which provide
logarithmic search complexity[2]. However, some argue that
exact search may be preferable for smaller datasets[3].
```

For multiple sources supporting one claim:
```
This approach has become standard practice[1][2][3].
```

For source with specific location:
```
According to the official documentation[1, §3.2]...
```

---

### Source List Entry

Format each source with full metadata:

```markdown
[1] Author(s), "Title", Source/Publication, Date, URL
    Tier: X | Weight: X.X | Credibility: Brief note
```

#### Examples by Source Type

**Official Documentation (Tier 1)**:
```
[1] Pinecone, "Vector Database Architecture", Pinecone Documentation, 2024,
    https://docs.pinecone.io/docs/architecture
    Tier: 1 | Weight: 1.0 | Official documentation from provider
```

**Academic Paper (Tier 2)**:
```
[2] Y. Malkov, D. Yashunin, "Efficient and Robust Approximate Nearest
    Neighbor Search Using Hierarchical Navigable Small World Graphs",
    IEEE TPAMI, 2020, https://doi.org/10.1109/TPAMI.2018.2889473
    Tier: 2 | Weight: 0.9 | Peer-reviewed, seminal HNSW paper
```

**News/Analysis (Tier 3)**:
```
[3] J. Smith, "The Rise of Vector Databases", TechCrunch, Jan 2024,
    https://techcrunch.com/2024/01/rise-of-vector-databases
    Tier: 3 | Weight: 0.75 | Major tech publication with editorial oversight
```

**Expert Blog (Tier 4)**:
```
[4] L. Harrison, "Lessons from Building RAG at Scale", Personal Blog,
    Mar 2024, https://example.com/rag-lessons
    Tier: 4 | Weight: 0.6 | ML engineer at [Company], verified expertise
```

**Community Source (Tier 5)**:
```
[5] u/vectordb_expert, "Comparison of vector index algorithms",
    Reddit r/MachineLearning, Feb 2024,
    https://reddit.com/r/MachineLearning/comments/xxx
    Tier: 5 | Weight: 0.4 | Community discussion with technical depth
```

**Unverified (Tier 6)**:
```
[6] Anonymous, "Vector DB Performance Tips", Medium, 2024,
    https://medium.com/xxx
    Tier: 6 | Weight: 0.2 | Unknown author, no verifiable credentials
```

---

## Source Card Format

For the detailed appendix, each source gets a full card:

```markdown
### Source [N]: [Title]

**Basic Info**:
- URL: [url]
- Author: [name or organization]
- Date: [publication date]
- Type: [documentation | paper | blog | news | discussion]

**Credibility Assessment**:
- Tier: [1-6] - [tier name]
- Weight: [0.2-1.0]
- Rationale: [why this tier]

**Key Claims Extracted**:
1. [claim 1]
2. [claim 2]
3. [claim 3]

**Agreement with Other Sources**:
- Agrees with: [N] sources on [topic]
- Disagrees with: [N] sources on [topic]
- Unique contribution: [what only this source provided]

**Notes**:
- [any caveats about this source]
- [potential biases]
- [special context]
```

---

## Numbering System

### Sequential Numbering
Number sources in order of first appearance in the report:
```
First citation in text → [1]
Second citation → [2]
...
```

### Grouping by Section (Alternative)
For very long reports, may use section prefixes:
```
Section 2 sources: [2.1], [2.2], [2.3]
Section 3 sources: [3.1], [3.2]
```

### Re-using Citations
When referencing the same source again:
```
As previously noted[1], this approach... (reuse same number)
```

---

## Special Cases

### Multiple Authors
```
[N] A. Smith, B. Jones, C. Lee, et al., "Title"...
```
(Use "et al." for more than 3 authors)

### No Author
```
[N] "Title", Organization/Website, Date, URL
```

### No Date
```
[N] Author, "Title", Source, n.d., URL
```
("n.d." = no date)

### Archived/Changed Pages
```
[N] Author, "Title", Source, Date, URL
    (Archived: [archive URL] on [archive date])
```

### Paywalled Content
```
[N] Author, "Title", Source, Date, URL
    (Paywalled - summary accessed via [method])
```

---

## Sources Section Template

```markdown
## Sources

### Tier 1 - Primary Sources
[1] ...
[2] ...

### Tier 2 - Peer-Reviewed
[3] ...
[4] ...

### Tier 3 - Authoritative
[5] ...
[6] ...

### Tier 4 - Expert Community
[7] ...
[8] ...

### Tier 5-6 - Community & Other
[9] ...
[10] ...

---

**Source Statistics**:
- Total sources: [N]
- Tier 1-2 (highest credibility): [N] ([X]%)
- Tier 3-4 (good credibility): [N] ([X]%)
- Tier 5-6 (limited credibility): [N] ([X]%)
```

---

## Quality Checks

### Before Finalizing Citations

- [ ] All inline citations have corresponding entries
- [ ] All sources have URLs (or reason for missing)
- [ ] All sources have tier assignments
- [ ] No duplicate entries
- [ ] Consistent formatting throughout
- [ ] Authors attributed where known
- [ ] Dates included where available
- [ ] Source types correctly identified

### Citation Coverage

- [ ] Every factual claim has at least one citation
- [ ] Key claims have multiple citations
- [ ] Counter-evidence properly cited
- [ ] Opinions attributed to sources

---

## Anti-Patterns

### Bad Citation Practices

**Too Vague**:
```
BAD: According to experts[1]...
GOOD: According to Dr. Smith, ML researcher at Stanford[1]...
```

**Missing for Claims**:
```
BAD: Vector databases are faster than SQL databases.
GOOD: Vector databases are faster than SQL databases for similarity search[1][2].
```

**Citation Dumping**:
```
BAD: This is true[1][2][3][4][5][6][7][8].
GOOD: This is well-established, with extensive documentation[1][2] and
      academic validation[3][4].
```

**Wrong Tier**:
```
BAD: Tier 2 for a random blog post
GOOD: Tier 4 or lower for unvetted content
```
