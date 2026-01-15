---
name: research
description: Deep research with multi-agent deliberative architecture
---

# /research - Research Parliament

> Invoke deep research that surpasses OpenAI and Anthropic through adversarial multi-agent architecture.

---

## Usage

```
/research "<topic or question>"
/research "<topic>" --depth <quick|standard|deep|exhaustive>
```

---

## Examples

```
/research "What are the current best practices for building production RAG systems?"

/research "How do modern LLM inference engines like vLLM and TensorRT-LLM compare?" --depth deep

/research "Comprehensive analysis of AI's impact on software engineering employment over the next 5 years" --depth exhaustive
```

---

## Depth Levels

| Level | Duration | Searches | Description |
|-------|----------|----------|-------------|
| `quick` | 2-5 min | 5-10 | Fast fact-check, simple questions |
| `standard` | 10-20 min | 20-40 | Balanced research for most queries |
| `deep` | 30-60 min | 60-120 | Thorough investigation with recursion |
| `exhaustive` | 1-3+ hours | 200-500+ | Publication-grade, leave no stone unturned |

---

## What Happens

### Phase 1: Understanding
- Query decomposed into 3-7 sub-questions
- Expertise domains identified
- Scope determined based on depth

### Phase 2: Divergent Research (Parallel)
Three researchers with different perspectives:
- **Scholar**: Academic papers, official docs, peer-reviewed sources
- **Investigator**: News, case studies, real-world implementations
- **Skeptic**: Counter-evidence, edge cases, criticisms, failures

### Phase 3: Claim Extraction
- Atomic claims extracted from all findings
- Claims categorized: factual | opinion | projection
- Conflicts between researchers identified

### Phase 4: Adversarial Validation
- **Validator**: Cross-references every claim, scores source credibility
- **Critic**: Attacks strongest claims, finds methodology weaknesses

### Phase 5: Deliberative Synthesis
- **Synthesizer**: Resolves conflicts, determines strongest evidence
- Minority opinions preserved with context
- Meta-insights generated

### Phase 6: Depth Recursion
(If `deep` or `exhaustive`)
- Low-confidence claims trigger targeted sub-research
- Continues until quality thresholds met

### Phase 7: Final Assembly
Structured report with:
- Executive Summary
- Key Findings (with confidence scores)
- Full Report (with inline citations)
- Counter-Evidence & Limitations
- Confidence Map
- Source Cards

---

## Output Format

```markdown
# Research Report: [Topic]
Generated: [Date] | Depth: [Level] | Searches: [N] | Sources: [N]

## Executive Summary
[1 page max - key conclusions]

## Key Findings
- Finding 1 (Confidence: HIGH | Sources: 4)
- Finding 2 (Confidence: MEDIUM | Sources: 2)
- ...

## Full Report
### Sub-question 1
[Detailed findings with inline citations[1][2]]

### Sub-question 2
...

## Counter-Evidence & Limitations
- [What disagrees with main findings]
- [Edge cases and caveats]
- [Methodology limitations]

## Confidence Map
| Claim | Confidence | Sources | Notes |
|-------|------------|---------|-------|
| ...   | HIGH       | 4       | Strong consensus |
| ...   | LOW        | 1       | Needs verification |

## Sources
[1] Author, "Title", URL (Tier 2, Weight: 0.9)
[2] ...
```

---

## Source Credibility

All sources are classified:

| Tier | Weight | Examples |
|------|--------|----------|
| 1 - Primary | 1.0 | Official docs, APIs, government, standards |
| 2 - Peer-Reviewed | 0.9 | Academic papers, journals, RFCs |
| 3 - Authoritative | 0.75 | Major news, analysts, known experts |
| 4 - Expert Community | 0.6 | Tech blogs, conference talks |
| 5 - Community | 0.4 | Reddit, forums, general blogs |
| 6 - Unverified | 0.2 | Random web, social media |

---

## Completion Criteria

Research completes when:
1. All sub-questions have answers meeting confidence threshold
2. Novelty exhausted (no new info from recent searches)
3. Contradictions resolved or explicitly flagged
4. Counter-evidence section populated

---

## Tips for Best Results

1. **Be specific**: "Best practices for RAG with PostgreSQL pgvector" > "How to do RAG"
2. **Use exhaustive for important decisions**: Job changes, architecture choices, investments
3. **Review counter-evidence**: The disagreements are often more valuable than agreements
4. **Check confidence scores**: LOW confidence claims need verification

---

## Begin

To start research, read `ai/research/CLAUDE.md` and follow the Research Parliament protocol.
