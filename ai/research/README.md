# Research Parliament

> A deep research skill for Claude Code that surpasses OpenAI Deep Research and Anthropic Claude Research through multi-agent deliberative architecture.

---

## What Makes This Different

| Traditional Deep Research | Research Parliament |
|---------------------------|---------------------|
| Single agent with tools | 7 specialized agents with different biases |
| Stops by time limit | Stops by confidence threshold |
| Aggregates findings | Deliberative synthesis through debate |
| No adversarial checking | Dedicated Critic + Validator agents |
| Hidden uncertainty | Explicit confidence scores per claim |
| Counter-evidence buried | First-class counter-evidence section |

---

## Quick Start

### Basic Usage
```
/research "What are the best practices for building RAG systems?"
```

### With Depth Control
```
/research "Impact of AI on software engineering jobs" --depth deep
```

### Depth Levels

| Level | Duration | Searches | Use Case |
|-------|----------|----------|----------|
| `quick` | 2-5 min | 5-10 | Quick fact-check, simple questions |
| `standard` | 10-20 min | 20-40 | Most research queries (DEFAULT) |
| `deep` | 30-60 min | 60-120 | Important decisions, complex topics |
| `exhaustive` | 1-3+ hours | 200-500+ | Critical decisions, thesis-level research |

---

## The Research Parliament Architecture

```
                    ┌─────────────────┐
                    │  ORCHESTRATOR   │
                    │ (Master Control)│
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│    SCHOLAR    │   │ INVESTIGATOR  │   │    SKEPTIC    │
│ (Academic)    │   │ (Practical)   │   │ (Counter)     │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                   ┌─────────────────┐
                   │    VALIDATOR    │
                   │ (Cross-check)   │
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │     CRITIC      │
                   │ (Attack)        │
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │   SYNTHESIZER   │
                   │ (Resolve)       │
                   └─────────────────┘
```

### Agent Roles

- **Orchestrator**: Master controller, manages phases, decides when complete
- **Scholar**: Seeks academic papers, official documentation, peer-reviewed sources
- **Investigator**: Seeks real-world examples, case studies, news, implementations
- **Skeptic**: Actively seeks counter-evidence, edge cases, criticisms, failures
- **Validator**: Cross-references all claims, scores source credibility
- **Critic**: Attacks the research methodology, finds weaknesses
- **Synthesizer**: Resolves conflicts, generates meta-insights

---

## The 7-Phase Process

1. **Understanding** - Decompose query into sub-questions
2. **Divergent Research** - Scholar, Investigator, Skeptic research in parallel
3. **Claim Extraction** - Extract atomic claims, identify conflicts
4. **Adversarial Validation** - Validator cross-checks, Critic attacks
5. **Deliberative Synthesis** - Resolve conflicts, generate insights
6. **Depth Recursion** - Deep-dive on low-confidence areas (if depth permits)
7. **Final Assembly** - Generate structured report with full provenance

---

## Source Credibility Tiers

Every source is classified and weighted:

| Tier | Weight | Description |
|------|--------|-------------|
| 1 - Primary | 1.0 | Official docs, APIs, government, standards bodies |
| 2 - Peer-Reviewed | 0.9 | Academic papers, journals, RFCs |
| 3 - Authoritative | 0.75 | Major news, industry analysts, known experts |
| 4 - Expert Community | 0.6 | Tech blogs (known authors), conference talks |
| 5 - Community | 0.4 | Reddit, forums, general blogs |
| 6 - Unverified | 0.2 | Random web, social media, anonymous |

---

## Output Format

Every research report includes:

1. **Executive Summary** - 1 page max, key conclusions
2. **Key Findings** - Bullet points with confidence indicators
3. **Full Report** - Detailed findings by sub-question with inline citations
4. **Counter-Evidence & Limitations** - What disagrees, edge cases, caveats
5. **Confidence Map** - Table showing confidence per claim
6. **Sources** - Numbered list with credibility tiers
7. **Source Cards** - Detailed analysis of each source

---

## Confidence Scoring

Claims are scored based on:
- Number of supporting sources
- Source tier weights
- Agreement vs contradiction between sources

**Thresholds**:
- **HIGH (>80%)**: Strong consensus from authoritative sources
- **MEDIUM (50-80%)**: Mixed support or minor contradictions
- **LOW (<50%)**: Limited evidence or significant contradictions

---

## Directory Structure

```
research/
├── CLAUDE.md              # System instructions (read this first)
├── readme.md              # This file
├── commands/
│   └── research.md        # /research command entry point
├── agents/
│   ├── orchestrator.md    # Master controller
│   ├── scholar.md         # Academic researcher
│   ├── investigator.md    # Practical researcher
│   ├── skeptic.md         # Counter-evidence seeker
│   ├── validator.md       # Claim cross-referencer
│   ├── critic.md          # Adversarial checker
│   └── synthesizer.md     # Insight generator
├── skills/
│   ├── query-decomposer.md
│   ├── source-evaluator.md
│   ├── claim-extractor.md
│   ├── confidence-scorer.md
│   └── citation-formatter.md
├── philosophy/
│   ├── research-standards.md
│   ├── source-hierarchy.md
│   └── anti-patterns.md
├── templates/
│   ├── research-report.md
│   ├── executive-summary.md
│   ├── source-card.md
│   ├── claim-card.md
│   └── research-state.md
└── examples/
    ├── sample-research.md
    └── sample-query.md
```

---

## Usage in Any Project

To use Research Parliament in any repository:

1. Copy the `/ai/research/` directory to your project
2. Ensure Claude Code can read the files
3. Invoke with `/research "your topic"`

Or reference directly:
```
Read ai/research/CLAUDE.md and follow those instructions to research: [topic]
```

---

## Why This Works

### Multi-Perspective Research
Three researchers with different biases ensure comprehensive coverage:
- Scholar won't miss academic consensus
- Investigator won't miss practical reality
- Skeptic won't miss the downsides

### Adversarial Verification
The Critic actively attacks findings, catching:
- Overconfident claims
- Methodology weaknesses
- Missing evidence

### Confidence-Bounded Completion
Instead of stopping after 20 minutes, we stop when:
- Claims meet confidence thresholds
- Novelty is exhausted
- Contradictions are resolved or flagged

### Full Provenance
Every claim traces back to:
- Specific sources with URLs
- Credibility tier and weight
- Agreement/disagreement with other sources

---

## Comparison to Alternatives

| Feature | OpenAI Deep Research | Anthropic Research | Research Parliament |
|---------|---------------------|-------------------|---------------------|
| Multi-agent | No | Partial | Yes (7 agents) |
| Adversarial | No | No | Yes (Critic + Skeptic) |
| Confidence scores | No | Partial | Yes (per claim) |
| Counter-evidence | Minimal | Some | Required section |
| Source tiers | No | No | 6-tier hierarchy |
| Depth control | Time-based | Time-based | Quality-based |

---

## License

Part of the dev-toolbox AI collection. Use freely.
