---
name: confidence-scorer
description: Calculates confidence scores for claims based on source quality and agreement
---

# Confidence Scorer Skill

> Calculate and assign confidence scores to research claims using a systematic formula based on source tiers and agreement factors.

---

## When to Use

- Phase 4 of Research Parliament (Adversarial Validation)
- After Validator has cross-referenced claims
- When preparing final report

---

## The Confidence Formula

```
confidence = (support_score / max_possible_score) × 100

Where:
- support_score = Σ(tier_weight × agreement_factor) for all sources
- max_possible_score = Σ(tier_weight) for all sources
```

### Tier Weights

| Tier | Weight | Description |
|------|--------|-------------|
| 1 - Primary | 1.0 | Official docs, standards, primary research |
| 2 - Peer-Reviewed | 0.9 | Academic papers, journals |
| 3 - Authoritative | 0.75 | Major news, analysts, known experts |
| 4 - Expert Community | 0.6 | Practitioner blogs, talks |
| 5 - Community | 0.4 | Reddit, forums, general blogs |
| 6 - Unverified | 0.2 | Unknown sources |

### Agreement Factors

| Factor | Value | When to Apply |
|--------|-------|---------------|
| Full Support | 1.0 | Source explicitly supports the claim |
| Partial Support | 0.5 | Source partially supports or is neutral |
| Contradiction | 0.0 | Source contradicts the claim |

---

## Calculation Process

### Step 1: List All Sources for Claim
```
Claim: "HNSW is the most common vector index algorithm"

Sources:
1. Pinecone official docs (Tier 1)
2. Survey paper in ACM (Tier 2)
3. Engineering blog (Tier 4)
4. Reddit discussion (Tier 5)
```

### Step 2: Assess Agreement for Each Source
```
1. Pinecone docs: Explicitly states HNSW is default → FULL (1.0)
2. Survey paper: Lists HNSW as "widely adopted" → FULL (1.0)
3. Blog: Mentions HNSW among options → PARTIAL (0.5)
4. Reddit: Agrees but notes alternatives → PARTIAL (0.5)
```

### Step 3: Calculate Scores
```
Support score:
- Tier 1 × Full:    1.0 × 1.0 = 1.0
- Tier 2 × Full:    0.9 × 1.0 = 0.9
- Tier 4 × Partial: 0.6 × 0.5 = 0.3
- Tier 5 × Partial: 0.4 × 0.5 = 0.2
Total support: 2.4

Max possible:
- 1.0 + 0.9 + 0.6 + 0.4 = 2.9

Confidence: (2.4 / 2.9) × 100 = 82.8% → HIGH
```

---

## Confidence Thresholds

| Level | Range | Interpretation |
|-------|-------|----------------|
| **HIGH** | >80% | Strong consensus from quality sources |
| **MEDIUM** | 50-80% | Mixed support or lower-tier sources |
| **LOW** | <50% | Limited evidence or contradictions |

---

## Depth-Specific Requirements

| Depth | Minimum for Key Claims | Action if Below |
|-------|------------------------|-----------------|
| QUICK | 40% | Note as unverified |
| STANDARD | 60% | Flag for attention |
| DEEP | 70% | Trigger sub-research |
| EXHAUSTIVE | 80% | Must reach or explicitly flag |

---

## Example Calculations

### Example 1: Strong Confidence

**Claim**: "GPT-4 was released in March 2023"

| Source | Tier | Agreement | Score |
|--------|------|-----------|-------|
| OpenAI announcement | 1 | Full (1.0) | 1.0 |
| Wikipedia (citing OpenAI) | 4 | Full (1.0) | 0.6 |
| News articles | 3 | Full (1.0) | 0.75 |

Support: 1.0 + 0.6 + 0.75 = 2.35
Max: 1.0 + 0.6 + 0.75 = 2.35
**Confidence: 100% (HIGH)**

---

### Example 2: Medium Confidence

**Claim**: "512 tokens is the optimal chunk size for RAG"

| Source | Tier | Agreement | Score |
|--------|------|-----------|-------|
| LangChain docs | 3 | Full (1.0) | 0.75 |
| Blog post A | 4 | Full (1.0) | 0.6 |
| Blog post B | 4 | Partial (0.5) | 0.3 |
| Reddit | 5 | Contradicts (0.0) | 0.0 |

Support: 0.75 + 0.6 + 0.3 + 0 = 1.65
Max: 0.75 + 0.6 + 0.6 + 0.4 = 2.35
**Confidence: 70.2% (MEDIUM)**

---

### Example 3: Low Confidence

**Claim**: "AI will replace 50% of software engineers by 2030"

| Source | Tier | Agreement | Score |
|--------|------|-----------|-------|
| News article | 3 | Full (1.0) | 0.75 |
| Academic paper | 2 | Contradicts (0.0) | 0.0 |
| Expert blog | 4 | Partial (0.5) | 0.3 |
| Another expert | 4 | Contradicts (0.0) | 0.0 |

Support: 0.75 + 0 + 0.3 + 0 = 1.05
Max: 0.75 + 0.9 + 0.6 + 0.6 = 2.85
**Confidence: 36.8% (LOW)**

---

## Special Cases

### No High-Tier Sources
If only Tier 4-6 sources exist:
- Calculate normally
- Add note: "No Tier 1-2 sources found"
- Consider flagging for more research

### Single Source
If only one source:
- Confidence = tier_weight × 100
- Add note: "Single source - needs verification"
- Flag for additional research

### All Sources Contradict
If no supporting sources:
- Confidence = 0%
- The claim should be marked as REFUTED
- Note what the evidence actually says

### Expert Disagreement
If high-tier sources disagree:
- Calculate normally (will be MEDIUM/LOW)
- Add note: "Expert disagreement exists"
- Document both positions in report

---

## Output Format

```markdown
## Confidence Assessment

### Claim: "[claim text]"

**Confidence Score**: [X]% ([HIGH|MEDIUM|LOW])

**Calculation**:
| Source | Tier | Weight | Agreement | Score |
|--------|------|--------|-----------|-------|
| [source 1] | [N] | [W] | [factor] | [score] |
| [source 2] | [N] | [W] | [factor] | [score] |
| ... | ... | ... | ... | ... |

**Support Score**: [X]
**Max Possible**: [Y]
**Final**: [X/Y × 100]%

**Notes**:
- [Any special considerations]
- [Any flags or caveats]

**Recommendation**: [Action if below threshold]
```

---

## Aggregation for Reports

### Key Findings Confidence
For the overall report:
```
- HIGH confidence claims: [N]
- MEDIUM confidence claims: [N]
- LOW confidence claims: [N]
- Overall research confidence: [average or weighted average]
```

### When to Downgrade Overall Confidence
- More than 30% of key claims are LOW
- Core claims (answering main question) are not HIGH
- Significant contradictions unresolved
- Limited source diversity

---

## Common Pitfalls

### Don't Double-Count
If the same source is cited multiple times:
- Count it once
- Use the most relevant citation

### Don't Inflate Agreement
- "Doesn't mention" ≠ "Agrees"
- Neutral sources get 0.5, not 1.0

### Don't Ignore Contradictions
- A single high-tier contradiction matters
- Must be reflected in score

### Don't Ignore Recency
- Outdated sources on evolving topics
- Consider downgrading tier for old sources
