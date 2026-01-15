# Claim Card Template

> Detailed documentation for individual claims, including verification status and confidence scoring.

---

```markdown
## Claim Card: [Claim ID]

### Claim Statement

> "[The exact claim being tracked]"

---

#### Classification

| Field | Value |
|-------|-------|
| **Claim Type** | [FACTUAL / OPINION / PROJECTION / METHODOLOGICAL] |
| **Sub-Question** | Q[N]: [question text] |
| **Importance** | [KEY / SUPPORTING / MINOR] |

---

#### Source Attribution

**Original Source**:
- Source: [N] - [title]
- Tier: [N]
- Context: [where in source this appeared]

**Supporting Sources**:
| Source | Tier | Agreement | Score Contribution |
|--------|------|-----------|-------------------|
| [N] - [title] | [N] | FULL / PARTIAL | [weight × factor] |
| [N] - [title] | [N] | FULL / PARTIAL | [weight × factor] |
| ... | ... | ... | ... |

**Contradicting Sources**:
| Source | Tier | Contradiction |
|--------|------|---------------|
| [N] - [title] | [N] | [what it says instead] |
| ... | ... | ... |

---

#### Confidence Calculation

**Formula Applied**:
```
Support score: [calculation]
Max possible: [calculation]
Confidence: [result]%
```

**Final Confidence**: [X]% ([HIGH / MEDIUM / LOW])

**Factors Affecting Confidence**:
- [Factor 1]: [how it affects score]
- [Factor 2]: [how it affects score]

---

#### Verification Status

| Check | Status | Notes |
|-------|--------|-------|
| Cross-referenced | [YES / NO / PARTIAL] | [notes] |
| Primary source checked | [YES / NO / N/A] | [notes] |
| Counter-evidence sought | [YES / NO] | [notes] |
| Expert disagreement | [YES / NO] | [notes] |
| Temporal validity | [CURRENT / OUTDATED / UNKNOWN] | [notes] |

---

#### Contextualization

**Conditions Where True**:
- [Condition 1]
- [Condition 2]

**Conditions Where False/Limited**:
- [Exception 1]
- [Exception 2]

**Related Claims**:
- Supports: [Claim ID]
- Contradicts: [Claim ID]
- Depends on: [Claim ID]

---

#### Critic Assessment

**Weaknesses Identified**:
- [Weakness 1]
- [Weakness 2]

**Strength of Evidence**:
[STRONG / MODERATE / WEAK] - [explanation]

**Recommendation**:
- [ ] Include as high-confidence finding
- [ ] Include with caveats
- [ ] Flag for more research
- [ ] Downgrade confidence
- [ ] Exclude from findings

---

#### Final Status

**Status**: [VERIFIED / PARTIALLY VERIFIED / UNVERIFIED / CONTRADICTED]

**In Report**: [YES - Section X / NO - reason]

**Confidence Level**: [HIGH / MEDIUM / LOW]

**Caveats to Include**:
- [Caveat 1]
- [Caveat 2]
```

---

## Claim Types Explained

### FACTUAL
Objectively verifiable statements about reality.
- Can be confirmed with primary sources
- Either true or false
- Examples: dates, names, measurements, events

### OPINION
Subjective assessments, even from experts.
- Cannot be objectively verified
- Must be attributed to source
- Examples: "best", "should", "recommended"

### PROJECTION
Forward-looking or predictive statements.
- About the future
- Inherently uncertain
- Examples: "will become", "is expected to", "by 2030"

### METHODOLOGICAL
Claims about how things work or should be done.
- Process descriptions
- Best practices
- Can be verified against implementations
- Examples: "use X for Y", "the process involves"

---

## When to Create Full Claim Cards

### Always Create For:
- Key claims (central to findings)
- Contested claims (have contradictions)
- Low-confidence claims (need documentation)
- Claims with complex verification

### Abbreviated Card For:
- Supporting claims (straightforward)
- High-confidence with clear consensus
- Minor claims

### Abbreviated Format:

```markdown
**Claim [ID]**: [statement]
- Type: [type] | Confidence: [X]%
- Sources: [N] (Tier breakdown: [X])
- Status: [VERIFIED / etc.]
- Notes: [brief caveat if any]
```
