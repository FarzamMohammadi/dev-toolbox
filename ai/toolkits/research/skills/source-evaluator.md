---
name: source-evaluator
description: Evaluates and scores source credibility using the 6-tier hierarchy
---

# Source Evaluator Skill

> Assess the credibility of any source and assign it to the appropriate tier with a credibility weight.

---

## When to Use

- Validator agent assessing sources
- Any agent encountering a new source
- Orchestrator compiling final source list

---

## The 6-Tier Hierarchy

### Tier 1: PRIMARY (Weight: 1.0)

**Definition**: Original, authoritative sources from creators or official bodies.

**Indicators**:
- Official documentation from technology creators
- Primary research with original data collection
- Government or institutional sources
- Standards bodies (IETF, W3C, ISO, IEEE)
- API references and specifications
- Original announcements from creators

**Examples**:
- `docs.python.org` (Python official docs)
- RFC 2616 (HTTP/1.1 specification)
- Research paper with original experiments
- `openai.com/research` (for OpenAI topics)

---

### Tier 2: PEER-REVIEWED (Weight: 0.9)

**Definition**: Vetted by expert review processes.

**Indicators**:
- Published in academic journals
- Conference proceedings (major venues)
- Technical specifications with review
- Peer-reviewed preprints
- Reproducible methodology described

**Examples**:
- Nature, Science, PNAS articles
- NeurIPS, ICML, ACL proceedings
- ACM/IEEE journal papers
- arXiv papers later published

**Note**: arXiv preprints without peer review are Tier 3 or 4.

---

### Tier 3: AUTHORITATIVE (Weight: 0.75)

**Definition**: Credible sources with editorial oversight or established expertise.

**Indicators**:
- Major news outlets with fact-checking
- Industry analysts (Gartner, Forrester, etc.)
- Known experts with verifiable credentials
- Corporate research with methodology
- Well-edited technical books

**Examples**:
- New York Times technology coverage
- Gartner Magic Quadrant reports
- O'Reilly books by known experts
- Google AI Blog, Meta AI Blog

---

### Tier 4: EXPERT COMMUNITY (Weight: 0.6)

**Definition**: Content from verifiable practitioners with demonstrated expertise.

**Indicators**:
- Author has verifiable credentials
- Technical depth in content
- Community recognition (high reputation)
- Specific, substantive claims
- Active in the field

**Examples**:
- Engineering blogs by known practitioners
- High-rep Stack Overflow answers
- Conference talk recordings
- Substacks by recognized experts
- Martin Fowler's blog, Julia Evans' blog

---

### Tier 5: COMMUNITY (Weight: 0.4)

**Definition**: Open community discussions without formal vetting.

**Indicators**:
- Multiple participants
- Some substantive content
- Recency
- Upvotes/engagement signals quality

**Examples**:
- Reddit technical subreddits
- Hacker News discussions
- General programming forums
- Medium articles (unknown authors)
- Dev.to posts

---

### Tier 6: UNVERIFIED (Weight: 0.2)

**Definition**: Sources with no verifiable credibility.

**Indicators**:
- Anonymous or unknown author
- No verifiable credentials
- Unsubstantiated claims
- No community validation
- Potential bias/conflicts not disclosed

**Examples**:
- Random blog posts
- Social media claims
- Anonymous forum posts
- Marketing content disguised as education

---

## Evaluation Process

### Step 1: Identify the Source Type
```
- Is this official documentation? → Check Tier 1
- Is this peer-reviewed? → Check Tier 2
- Is this from a major outlet/analyst? → Check Tier 3
- Is the author a known expert? → Check Tier 4
- Is this community discussion? → Check Tier 5
- Unknown/anonymous? → Tier 6
```

### Step 2: Verify Indicators
```
For Tier 1-2: Check publication venue, review process
For Tier 3: Check editorial standards, author credentials
For Tier 4: Verify author expertise, check their background
For Tier 5: Assess discussion quality, engagement
For Tier 6: Default for unverifiable
```

### Step 3: Check for Downgrades
```
Reasons to downgrade a tier:
- Outdated (>3 years for fast-moving topics)
- Conflicts of interest not disclosed
- Significant errors found
- Retracted or corrected
- Cherry-picked data
```

### Step 4: Check for Upgrades
```
Reasons to upgrade a tier:
- Multiple independent confirmations
- Proven track record of accuracy
- Widely cited by higher-tier sources
- Subsequently validated by research
```

---

## Output Format

```markdown
## Source Evaluation

**URL**: [url]
**Title**: [title]
**Author**: [author if known]

**Tier Assignment**: [1-6]
**Weight**: [0.2-1.0]

**Rationale**:
- Source type: [what kind of source]
- Credibility indicators: [what qualifies it]
- Downgrades/Upgrades: [if any]

**Confidence in Assessment**: [HIGH|MEDIUM|LOW]
**Notes**: [any caveats]
```

---

## Quick Evaluation Checklist

### For Academic Sources
- [ ] Published in recognized venue?
- [ ] Peer review process?
- [ ] Methodology described?
- [ ] Results reproducible?
- [ ] Not retracted?

### For Practitioner Sources
- [ ] Author credentials verifiable?
- [ ] Specific, substantive claims?
- [ ] Evidence provided?
- [ ] No obvious conflicts of interest?

### For News/Analysis
- [ ] Editorial oversight?
- [ ] Fact-checking process?
- [ ] Sources cited?
- [ ] Track record of accuracy?

### For Community Sources
- [ ] Substantive discussion?
- [ ] Multiple perspectives?
- [ ] Any expert participants?
- [ ] Recency?

---

## Special Cases

### arXiv Preprints
- If later published: Tier 2
- If highly cited but unpublished: Tier 3
- If new/uncited: Tier 4

### Corporate Blogs
- From research division with methodology: Tier 3
- Marketing with technical content: Tier 4
- Pure marketing: Tier 6

### Wikipedia
- As starting point: Not a primary source (don't cite)
- For references it cites: Evaluate those sources
- For well-referenced technical articles: Tier 4-5

### Stack Overflow
- High-rep answer with explanations: Tier 4
- Random answer: Tier 5
- Accepted answer with verification: Tier 4

---

## Common Mistakes

### Overrating
- Blog post is NOT Tier 1 even if correct
- News article is NOT Tier 2 even if well-written
- Reddit post is NOT Tier 4 even if upvoted

### Underrating
- Official docs are always Tier 1
- Peer-reviewed is at least Tier 2
- Known expert blogs deserve Tier 4 minimum

### Ignoring Context
- Old source about current topic: downgrade
- Current source about historical topic: may be fine
- Vendor source about own product: note bias
