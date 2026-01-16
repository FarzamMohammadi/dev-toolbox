# Research Anti-Patterns

> Common mistakes to avoid when conducting research. Every anti-pattern here degrades research quality.

---

## Search Anti-Patterns

### 1. Query Tunnel Vision
**Problem**: Using only one search query formulation.

```
BAD: Searching only "RAG best practices"
GOOD: Also searching "retrieval augmented generation guide",
      "RAG production", "RAG lessons learned", "RAG mistakes"
```

**Why It's Bad**: Different phrasings find different sources. One query misses most of the web.

---

### 2. Confirmation Search
**Problem**: Only searching for evidence that supports expected answer.

```
BAD: "Why RAG is the best approach"
GOOD: "RAG limitations", "RAG vs fine-tuning", "when not to use RAG"
```

**Why It's Bad**: You'll find what you're looking for, but miss the truth.

---

### 3. First-Page Syndrome
**Problem**: Only looking at top search results.

**Why It's Bad**: SEO-optimized content often beats quality content. The best sources may be on page 2-3 or require site-specific searches.

---

### 4. Recency Bias
**Problem**: Only using the newest sources, ignoring foundational work.

```
BAD: Only 2024 blog posts
GOOD: Mix of foundational papers, recent developments, and current practice
```

**Why It's Bad**: You miss the "why" behind current practices and may recommend outdated patterns that are only recently popular.

---

## Source Anti-Patterns

### 5. Single-Source Reliance
**Problem**: Treating one source as the truth.

```
BAD: "According to the Google blog post..."
GOOD: "Multiple sources including Google's blog[1], academic research[2],
      and practitioner experience[3] suggest..."
```

**Why It's Bad**: Any single source can be wrong, biased, or incomplete.

---

### 6. Tier Inflation
**Problem**: Treating low-tier sources as high-tier.

```
BAD: Citing a random blog as authoritative (Tier 3)
GOOD: Correctly identifying it as Tier 5-6
```

**Why It's Bad**: Inflated tiers produce inflated confidence scores.

---

### 7. Vendor Source Trust
**Problem**: Treating vendor content as objective.

```
BAD: "Pinecone documentation says Pinecone is the best vector database"
GOOD: "Pinecone documentation describes their architecture[1];
      independent comparisons suggest..."
```

**Why It's Bad**: Vendors are biased toward their own products.

---

### 8. Circular Citation
**Problem**: Sources that cite each other, creating illusion of consensus.

```
BAD: 5 sources all citing the same original blog post
GOOD: 5 independent sources with their own evidence
```

**Why It's Bad**: Circular citations multiply a single opinion, not evidence.

---

## Claim Anti-Patterns

### 9. Compound Claims
**Problem**: Bundling multiple claims together.

```
BAD: "RAG is effective and easy to implement and cheaper than fine-tuning"
GOOD: Three separate claims, each verified independently
```

**Why It's Bad**: One part may be true while others are false.

---

### 10. Opinion as Fact
**Problem**: Presenting subjective assessments as objective truth.

```
BAD: "HNSW is the best index algorithm"
GOOD: "HNSW is widely adopted[1] and shows strong performance on benchmarks[2],
      though some argue [alternative] is better for [specific case][3]"
```

**Why It's Bad**: "Best" is subjective; readers deserve to know it's opinion.

---

### 11. Overgeneralization
**Problem**: Extending findings beyond their scope.

```
BAD: "RAG works" (from one case study)
GOOD: "RAG worked for [Company X]'s use case of [specific application][1]"
```

**Why It's Bad**: Context matters; what works for one may fail for another.

---

### 12. Certainty Overreach
**Problem**: Claiming certainty without sufficient evidence.

```
BAD: "This is definitely the right approach"
GOOD: "Evidence suggests this approach is effective (confidence: 75%),
      though [alternative] may be better for [edge cases]"
```

**Why It's Bad**: False certainty misleads decision-makers.

---

## Process Anti-Patterns

### 13. Premature Conclusion
**Problem**: Stopping research when finding the expected answer.

```
BAD: Found 2 sources agreeing → done
GOOD: Found 2 sources agreeing → look for disagreement → verify → done
```

**Why It's Bad**: You may have found confirming sources first by chance.

---

### 14. Counter-Evidence Avoidance
**Problem**: Not actively seeking counter-evidence.

```
BAD: The Skeptic agent skipped or given minimal budget
GOOD: The Skeptic agent given equal budget and attention
```

**Why It's Bad**: The counter-evidence section is required, not optional.

---

### 15. Methodology Opacity
**Problem**: Not documenting how research was conducted.

```
BAD: "Based on research..."
GOOD: "Based on 47 searches across 23 sources, including 5 Tier 1-2..."
```

**Why It's Bad**: Readers can't assess research quality without methodology.

---

### 16. Time-Bounded vs Quality-Bounded
**Problem**: Stopping when time runs out rather than when quality is sufficient.

```
BAD: "30 minutes passed, we're done"
GOOD: "Confidence thresholds met, novelty exhausted, we're done"
```

**Why It's Bad**: Time limits are arbitrary; quality thresholds are meaningful.

---

## Synthesis Anti-Patterns

### 17. Summary Instead of Synthesis
**Problem**: Just concatenating findings without integration.

```
BAD: "Scholar found X. Investigator found Y. Skeptic found Z."
GOOD: "While academic research emphasizes X[1], practitioners report
      Y is more critical[2]. However, both approaches fail for Z[3],
      suggesting the real answer is..."
```

**Why It's Bad**: Synthesis adds value; summary doesn't.

---

### 18. Forced Consensus
**Problem**: Artificially resolving disagreements.

```
BAD: "Despite some disagreement, X is clearly correct"
GOOD: "Sources disagree on this point: [Position A][1][2] vs
      [Position B][3]. The disagreement appears unresolved because..."
```

**Why It's Bad**: Readers deserve to know when experts disagree.

---

### 19. Minority Suppression
**Problem**: Ignoring dissenting expert opinions.

```
BAD: "Everyone agrees X is best"
GOOD: "Most sources support X[1][2][3], but [Expert Y] argues against it[4]
      based on [their reasoning]"
```

**Why It's Bad**: Minority opinions are often right; they deserve hearing.

---

### 20. Missing Meta-Insights
**Problem**: Not extracting higher-order patterns.

```
BAD: Listing facts without connection
GOOD: "The gap between academic recommendations and practitioner
      experience suggests theoretical best practices may not translate
      directly to production environments"
```

**Why It's Bad**: Meta-insights are often the most valuable output.

---

## Output Anti-Patterns

### 21. Empty Counter-Evidence
**Problem**: "No counter-evidence found" without explanation.

```
BAD: "## Counter-Evidence\n\nNone found."
GOOD: "## Counter-Evidence\n\nWe searched [queries] but found no substantial
      criticism. This may indicate genuine consensus, or that criticism
      exists in venues we didn't access. Limitations include..."
```

**Why It's Bad**: Empty section suggests inadequate research.

---

### 22. Confidence Score Omission
**Problem**: Not showing confidence levels.

```
BAD: "The answer is X."
GOOD: "The answer is X (confidence: 78%, based on 4 Tier 2-3 sources)"
```

**Why It's Bad**: Readers can't calibrate trust without confidence info.

---

### 23. Citation Dumping
**Problem**: Listing many citations without using them meaningfully.

```
BAD: "This is true[1][2][3][4][5][6][7]"
GOOD: "Primary sources confirm this[1], academic research validates it[2],
      and practitioners report similar results[3]"
```

**Why It's Bad**: Citation dumping obscures which sources actually matter.

---

## The Golden Rule

**When in doubt, disclose uncertainty.**

It's always better to say "evidence is limited" than to overstate confidence. Readers can handle uncertainty; they can't handle being misled.
