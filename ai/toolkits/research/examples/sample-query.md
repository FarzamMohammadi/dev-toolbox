# Sample Research Queries

> Examples of how to invoke the Research Parliament with different query types and depth levels.

---

## Basic Queries

### Simple Technical Question
```
/research "What are the current best practices for building production RAG systems?"
```
**Expected depth**: STANDARD (default)
**Expected duration**: 10-20 minutes

---

### Comparison Query
```
/research "PostgreSQL vs MongoDB for a new SaaS application - which should I choose?"
```
**Expected depth**: STANDARD
**Good for**: Decision-making, understanding trade-offs

---

### Trend/Impact Query
```
/research "How is AI changing software engineering practices in 2024?"
```
**Expected depth**: STANDARD
**Good for**: Understanding landscape, identifying patterns

---

## Queries with Depth Flags

### Quick Fact-Check
```
/research "What is the context window size of GPT-4 Turbo?" --depth quick
```
**Duration**: 2-5 minutes
**Use case**: Verifying a specific fact quickly

---

### Standard Research (Explicit)
```
/research "Best practices for Kubernetes security" --depth standard
```
**Duration**: 10-20 minutes
**Use case**: Most research needs

---

### Deep Investigation
```
/research "Comprehensive analysis of vector database options for enterprise ML pipelines" --depth deep
```
**Duration**: 30-60 minutes
**Use case**: Important architectural decisions

---

### Exhaustive Research
```
/research "Complete analysis of LLM inference optimization techniques - all approaches, trade-offs, and benchmarks" --depth exhaustive
```
**Duration**: 1-3+ hours
**Use case**: Critical decisions, thesis-level research, due diligence

---

## Query Formulation Tips

### Be Specific
```
VAGUE: "Tell me about databases"
BETTER: "What are the trade-offs between SQL and NoSQL databases for real-time analytics?"
```

### Include Context
```
NO CONTEXT: "Best caching strategy"
WITH CONTEXT: "Best caching strategy for a high-traffic e-commerce API with personalized content"
```

### Scope Appropriately
```
TOO BROAD: "Everything about machine learning"
SCOPED: "Current state of the art in few-shot learning for NLP tasks"
```

### Ask Actionable Questions
```
ABSTRACT: "Is Rust good?"
ACTIONABLE: "Should I rewrite my Python CLI tool in Rust for better performance?"
```

---

## Example Research Requests by Domain

### Software Architecture
```
/research "Microservices vs monolith for a startup - when to choose which?"
/research "Event-driven architecture patterns for financial applications" --depth deep
/research "GraphQL vs REST for mobile applications - performance and developer experience"
```

### AI/ML
```
/research "Fine-tuning vs RAG vs prompt engineering - when to use each approach"
/research "State of the art in AI code generation - capabilities and limitations" --depth deep
/research "Complete survey of LLM evaluation methods and benchmarks" --depth exhaustive
```

### Infrastructure
```
/research "Kubernetes vs serverless for variable workloads"
/research "Database scaling strategies for 10x traffic growth" --depth deep
/research "Comprehensive cloud cost optimization strategies for AWS" --depth exhaustive
```

### Security
```
/research "Current best practices for API authentication and authorization"
/research "Zero trust architecture implementation patterns" --depth deep
/research "Complete analysis of LLM security vulnerabilities and mitigations" --depth exhaustive
```

### Career/Industry
```
/research "Skills most valuable for senior engineers in 2024"
/research "Impact of AI on software engineering jobs - comprehensive analysis" --depth deep
/research "Complete analysis of remote work trends in tech industry post-2023" --depth exhaustive
```

---

## Expected Outputs by Depth

### QUICK Output
- 1-2 page summary
- Key findings only
- Top 5 sources
- Basic confidence indicators
- Minimal counter-evidence

### STANDARD Output
- 3-5 page report
- Full sub-question analysis
- 10-20 sources
- Confidence scores
- Counter-evidence section

### DEEP Output
- 8-15 page report
- Comprehensive analysis
- 20-40 sources
- Detailed confidence map
- Full counter-evidence
- Source cards for key sources

### EXHAUSTIVE Output
- 20-50+ page report
- Publication-grade analysis
- 50-100+ sources
- Complete confidence documentation
- Extensive counter-evidence
- Full source cards
- Methodology section
- Historical context
