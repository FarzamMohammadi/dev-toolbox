# Sample Research Output

> Example of a completed STANDARD depth research report to illustrate the expected output format.

---

# Research Report: RAG Best Practices

**Generated**: 2024-01-15
**Depth**: STANDARD
**Duration**: 18 minutes
**Searches**: 32
**Sources**: 14 total (Tier 1-2: 4 | Tier 3-4: 7 | Tier 5-6: 3)

---

## Executive Summary

Retrieval-Augmented Generation (RAG) has emerged as the dominant pattern for grounding LLM outputs in external knowledge. This research analyzed current best practices for building production RAG systems, drawing from academic research, practitioner experience, and documented case studies.

**Key findings**: Successful RAG implementations focus on retrieval quality over generation quality, with hybrid search (combining dense and sparse retrieval) showing the strongest results. Chunk sizing between 256-512 tokens works well for general Q&A, though optimal sizing depends heavily on use case. Re-ranking is critical for precision but adds latency. The most common failure mode is poor retrieval—if the right documents aren't retrieved, no amount of prompt engineering helps.

**Important caveat**: RAG is not a silver bullet. It works best for factual Q&A with structured knowledge bases and struggles with complex reasoning, multi-hop questions, and domains requiring synthesis across many documents.

**Overall confidence**: 72% (MEDIUM-HIGH) - Strong consensus on core practices, some variation in specific recommendations.

---

## Key Findings

- **Retrieval quality is more important than generation quality** (Confidence: HIGH | Sources: 5)
  - If wrong documents are retrieved, the LLM cannot produce correct answers

- **Hybrid search (dense + sparse) outperforms either alone** (Confidence: HIGH | Sources: 4)
  - Combines semantic understanding with keyword precision

- **256-512 token chunks work well for general Q&A** (Confidence: MEDIUM | Sources: 4)
  - Larger for technical docs, smaller for conversational content

- **Re-ranking significantly improves precision** (Confidence: HIGH | Sources: 3)
  - Cross-encoders like Cohere Rerank or BGE-reranker are recommended

- **Evaluation is the hardest part** (Confidence: MEDIUM | Sources: 3)
  - No consensus on best evaluation approach; RAGAS and human evaluation both used

---

## Full Report

### Sub-Question 1: What are the core components of a RAG system?

A production RAG system consists of several key components working together[1][2]:

1. **Document Processing Pipeline**: Ingests raw documents, chunks them into appropriate sizes, and creates embeddings. Most implementations use recursive character splitters with overlap[3].

2. **Vector Store**: Stores embeddings for efficient similarity search. Popular choices include Pinecone, Weaviate, Qdrant, and pgvector[1][4].

3. **Retriever**: Fetches relevant documents given a query. Can be dense (embedding-based), sparse (BM25), or hybrid[2][5].

4. **Re-ranker** (optional but recommended): Reorders retrieved documents for precision using cross-encoder models[6].

5. **Generator**: The LLM that produces final responses given retrieved context and the query[1].

**Key Claims:**
- RAG separates knowledge (retrieval) from reasoning (generation)[1][2]
- Hybrid retrieval is becoming the standard approach[2][5]
- Re-ranking adds 100-300ms latency but significantly improves precision[6]

**Confidence**: 89% - Well-documented across academic and practitioner sources.

---

### Sub-Question 2: What chunk sizes and strategies work best?

Chunking strategy significantly impacts retrieval quality, but optimal settings vary by use case[3][7]:

**General recommendations**:
- 256-512 tokens for general Q&A and conversational contexts
- 512-1024 tokens for technical documentation
- Overlap of 10-20% between chunks to preserve context

**Advanced strategies**:
- Semantic chunking (splitting on topic boundaries) outperforms fixed-size in some tests[7]
- Parent-child chunking retrieves small chunks but includes parent context[3]
- Sentence-window retrieval provides surrounding sentences for context[3]

Practitioners report that chunk size is often overoptimized—retrieval quality and re-ranking matter more[8].

**Key Claims:**
- No universal optimal chunk size exists[3][7]
- Overlap prevents context fragmentation[3]
- Semantic chunking promising but more complex to implement[7]

**Confidence**: 65% - Significant variation in recommendations; depends on use case.

---

### Sub-Question 3: What retrieval strategies are most effective?

Hybrid search combining dense and sparse retrieval has emerged as the best practice[2][5][9]:

**Dense retrieval** (embedding-based):
- Good for semantic similarity
- Uses models like OpenAI embeddings, BGE, E5
- Can miss exact keyword matches

**Sparse retrieval** (BM25/TF-IDF):
- Good for exact keyword matching
- Works well for technical terms, names, IDs
- Misses semantic similarity

**Hybrid approach**:
- Combines both with weighted fusion
- Reciprocal Rank Fusion (RRF) is common technique
- Typically 0.7 dense + 0.3 sparse as starting point[5]

Academic benchmarks show 5-15% improvement with hybrid over dense-only[2].

**Key Claims:**
- Hybrid search outperforms single-method approaches[2][5]
- Dense retrieval alone misses keyword-specific queries[9]
- BM25 remains competitive for many use cases[2]

**Confidence**: 82% - Strong academic and practitioner consensus.

---

### Sub-Question 4: What are the common failure modes?

The Skeptic's investigation revealed several well-documented failure modes[8][10][11]:

1. **Poor retrieval** (most common): If relevant documents aren't retrieved, the LLM will hallucinate or admit ignorance. This is the #1 cause of RAG failures[10].

2. **Context window overflow**: Retrieving too many documents can exceed context limits or dilute relevant information[8].

3. **Lost in the middle**: LLMs tend to focus on beginning and end of context, missing information in the middle[11].

4. **Hallucination despite correct retrieval**: LLM may generate plausible but incorrect information even with correct documents[10].

5. **Latency issues**: Re-ranking and multiple retrieval steps can push latency to unacceptable levels[8].

**Key Claims:**
- Retrieval failure is more common than generation failure[10]
- "Lost in the middle" is a documented phenomenon in long contexts[11]
- Production RAG requires significant latency optimization[8]

**Confidence**: 78% - Well-documented failure modes across multiple sources.

---

### Sub-Question 5: What evaluation methods are recommended?

Evaluation emerged as the most contested area, with no clear consensus[12][13][14]:

**Automated evaluation**:
- RAGAS framework provides automated metrics (faithfulness, answer relevancy, context precision)[12]
- LLM-as-judge approaches using GPT-4 to evaluate responses[13]
- Retrieval metrics (recall@k, precision@k, MRR)

**Human evaluation**:
- Still considered gold standard but expensive and slow[13]
- Often used for final validation, not iteration

**Hybrid approaches**:
- Automated for iteration, human for validation
- A/B testing in production for real impact[14]

Practitioners note that evaluation is often neglected until production issues arise[8].

**Key Claims:**
- RAGAS is most popular automated framework[12]
- No single metric captures RAG quality completely[13]
- Human evaluation still necessary for high-stakes applications[13]

**Confidence**: 58% - Significant disagreement on best approach.

---

## Counter-Evidence & Limitations

### Counter-Evidence Found

1. **RAG may not be the best approach for all use cases**[10]
   - Fine-tuning outperforms RAG for consistent domain adaptation
   - For small, static knowledge bases, prompting with examples may suffice
   - Assessment: Valid - RAG is not always the right choice

2. **Dense retrieval criticized as overhyped**[9]
   - Some argue BM25 remains competitive in many scenarios
   - Dense models expensive to train and deploy
   - Assessment: Partially valid - BM25 still relevant for specific use cases

3. **Re-ranking latency concerns**[8]
   - 100-300ms additional latency may be unacceptable for real-time
   - Some production systems skip re-ranking for speed
   - Assessment: Valid trade-off - latency vs quality decision

### Edge Cases & Caveats

- **Multi-hop reasoning**: RAG struggles with questions requiring synthesis across multiple documents
- **Temporal knowledge**: RAG can return outdated information if corpus not updated
- **Domain-specific terminology**: Embedding models may not handle specialized vocabulary well

### Methodology Limitations

- Limited access to paywalled academic sources
- Practitioner sources may have survivorship bias (publishing successes)
- Rapidly evolving field; recommendations may date quickly

### What We Couldn't Determine

- Optimal re-ranker model for specific domains (limited comparative studies)
- Cost comparison across different RAG architectures
- Long-term maintenance burden of different approaches

---

## Confidence Map

| Claim | Confidence | Sources | Tier Breakdown | Notes |
|-------|------------|---------|----------------|-------|
| Hybrid search is best practice | HIGH (82%) | 4 | T2:2, T3:1, T4:1 | Strong consensus |
| 256-512 tokens for general Q&A | MEDIUM (65%) | 4 | T3:2, T4:2 | Varies by use case |
| Re-ranking improves precision | HIGH (85%) | 3 | T2:1, T3:2 | Clear academic evidence |
| Retrieval > generation quality | HIGH (88%) | 5 | T2:2, T3:2, T4:1 | Universal agreement |
| RAGAS is best evaluation | MEDIUM (58%) | 3 | T3:1, T4:2 | Contested area |

### Confidence Summary
- **HIGH confidence claims**: 3 (60%)
- **MEDIUM confidence claims**: 2 (40%)
- **LOW confidence claims**: 0 (0%)

---

## Sources

### Tier 2 - Peer-Reviewed

[1] Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", NeurIPS 2020, https://arxiv.org/abs/2005.11401
    Tier: 2 | Weight: 0.9 | Seminal RAG paper

[2] Chen et al., "Dense Passage Retrieval Survey", ACL 2023
    Tier: 2 | Weight: 0.9 | Comprehensive academic survey

### Tier 3 - Authoritative

[3] LangChain Documentation, "RAG Techniques", 2024, https://python.langchain.com/docs/
    Tier: 3 | Weight: 0.75 | Official framework documentation

[5] Pinecone, "Hybrid Search", https://docs.pinecone.io/
    Tier: 3 | Weight: 0.75 | Official documentation

[6] Cohere, "Rerank Best Practices", https://docs.cohere.com/
    Tier: 3 | Weight: 0.75 | Official documentation

[11] Liu et al., "Lost in the Middle", 2023, https://arxiv.org/abs/2307.03172
    Tier: 3 | Weight: 0.75 | Highly-cited preprint

[12] RAGAS Documentation, "Evaluation Metrics", https://docs.ragas.io/
    Tier: 3 | Weight: 0.75 | Official documentation

### Tier 4 - Expert Community

[7] J. Briggs, "Advanced RAG Techniques", Pinecone Blog, 2024
    Tier: 4 | Weight: 0.6 | Known ML practitioner

[8] E. Yang, "RAG in Production: Lessons Learned", Personal Blog, 2024
    Tier: 4 | Weight: 0.6 | Experienced practitioner

[9] BM25 discussion, Hacker News, 2024
    Tier: 4 | Weight: 0.6 | Expert community discussion

[10] S. Curry, "When RAG Fails", Towards Data Science, 2024
    Tier: 4 | Weight: 0.6 | Documented failure modes

### Tier 5 - Community

[13] r/MachineLearning, "RAG Evaluation Methods", Reddit, 2024
    Tier: 5 | Weight: 0.4 | Community discussion

[14] r/LocalLLaMA, "RAG Best Practices Thread", Reddit, 2024
    Tier: 5 | Weight: 0.4 | Community discussion

---

## Methodology

### Research Process
- **Depth level**: STANDARD
- **Total searches**: 32
- **Total sources reviewed**: 23
- **Sources cited**: 14
- **Time spent**: 18 minutes

### Agent Involvement
- Scholar: 12 searches, 6 sources (academic focus)
- Investigator: 11 searches, 5 sources (practitioner focus)
- Skeptic: 9 searches, 4 counter-evidence items
- Validator: 14 claims verified
- Critic: 3 issues identified, all addressed
- Synthesizer: 2 conflicts resolved

---

*Generated by Research Parliament | 2024-01-15*
