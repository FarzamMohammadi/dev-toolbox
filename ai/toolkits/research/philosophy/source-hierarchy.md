# Source Hierarchy

> The definitive guide to source credibility tiers used throughout the Research Parliament.

---

## The 6-Tier System

```
┌─────────────────────────────────────────────────────────────────┐
│ TIER 1: PRIMARY                                    Weight: 1.0  │
│ The source of truth. Original, authoritative, definitive.      │
├─────────────────────────────────────────────────────────────────┤
│ TIER 2: PEER-REVIEWED                              Weight: 0.9  │
│ Vetted by experts. Reproducible methodology. Academic rigor.   │
├─────────────────────────────────────────────────────────────────┤
│ TIER 3: AUTHORITATIVE                              Weight: 0.75 │
│ Editorial oversight. Known experts. Industry recognition.      │
├─────────────────────────────────────────────────────────────────┤
│ TIER 4: EXPERT COMMUNITY                           Weight: 0.6  │
│ Verifiable practitioners. Technical depth. Community respect.  │
├─────────────────────────────────────────────────────────────────┤
│ TIER 5: COMMUNITY                                  Weight: 0.4  │
│ Open discussion. Multiple voices. Some substance.              │
├─────────────────────────────────────────────────────────────────┤
│ TIER 6: UNVERIFIED                                 Weight: 0.2  │
│ Unknown credibility. Use only with corroboration.              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tier 1: PRIMARY (Weight: 1.0)

### Definition
The original, authoritative source of information. When you can go to the source itself, you should.

### Examples
| Source Type | Examples |
|-------------|----------|
| Official Documentation | `docs.python.org`, `developer.mozilla.org`, AWS docs |
| Standards Bodies | IETF RFCs, W3C specs, ISO standards, IEEE |
| Primary Research | Studies with original data collection |
| Government/Institutional | NIH, NSF, government statistics |
| Creator Announcements | OpenAI blog for GPT releases, company announcements |
| API References | Official API documentation |

### Indicators
- Comes directly from the creator/authority
- Is the canonical source others cite
- Contains original information, not derived
- Has clear institutional authority

### When to Assign
- Official product documentation → Tier 1
- RFC or technical specification → Tier 1
- Original research data → Tier 1
- Government statistics → Tier 1

---

## Tier 2: PEER-REVIEWED (Weight: 0.9)

### Definition
Content that has undergone expert review before publication. Academic rigor with reproducible methodology.

### Examples
| Source Type | Examples |
|-------------|----------|
| Academic Journals | Nature, Science, PNAS, IEEE TPAMI |
| Conference Proceedings | NeurIPS, ICML, ACL, SIGMOD, CHI |
| Published Research | Papers with DOIs from reputable venues |
| Technical Reports | From research institutions with review |

### Indicators
- Published in venue with peer review process
- Methodology described and reproducible
- Author affiliations verifiable
- Citations and references provided
- Not retracted

### When to Assign
- NeurIPS/ICML paper → Tier 2
- Nature article → Tier 2
- arXiv preprint later published → Tier 2
- Peer-reviewed journal article → Tier 2

### Notes on arXiv
- arXiv without publication: Usually Tier 3-4
- arXiv with many citations: May be Tier 2
- arXiv later published: Tier 2

---

## Tier 3: AUTHORITATIVE (Weight: 0.75)

### Definition
Credible sources with editorial oversight or established expert reputation, but not peer-reviewed academic work.

### Examples
| Source Type | Examples |
|-------------|----------|
| Major News | NYT, Washington Post, Reuters, WSJ |
| Industry Analysts | Gartner, Forrester, McKinsey |
| Research Blogs | Google AI Blog, Meta AI, OpenAI Blog |
| Expert Books | O'Reilly, from recognized authors |
| Respected Preprints | Highly-cited arXiv without formal publication |

### Indicators
- Editorial process exists
- Fact-checking or review happens
- Author/organization has track record
- Corrections policy exists
- Not primarily marketing

### When to Assign
- NYT tech article → Tier 3
- Gartner report → Tier 3
- Google AI Blog post → Tier 3
- O'Reilly book → Tier 3

---

## Tier 4: EXPERT COMMUNITY (Weight: 0.6)

### Definition
Content from verifiable practitioners with demonstrated expertise, but without formal editorial oversight.

### Examples
| Source Type | Examples |
|-------------|----------|
| Expert Blogs | Martin Fowler, Julia Evans, known practitioners |
| Stack Overflow | High-rep answers with explanations |
| Conference Talks | Recordings from reputable conferences |
| Substacks | From recognized domain experts |
| Technical Podcasts | From known experts |

### Indicators
- Author expertise is verifiable
- Technical depth in content
- Community recognition (reputation, followers)
- Specific, substantive claims
- Active in the field

### When to Assign
- Blog by known ML engineer → Tier 4
- Stack Overflow 10k+ rep answer → Tier 4
- KubeCon talk recording → Tier 4
- Expert newsletter issue → Tier 4

---

## Tier 5: COMMUNITY (Weight: 0.4)

### Definition
Open community discussions without formal vetting, but with collective intelligence signals.

### Examples
| Source Type | Examples |
|-------------|----------|
| Reddit | Technical subreddits (r/MachineLearning, r/programming) |
| Hacker News | Discussions with upvotes |
| Forums | Specialized technical forums |
| Medium/Dev.to | Posts from unknown authors |
| Discord/Slack | Community discussions |

### Indicators
- Multiple participants
- Some substantive content
- Recency
- Engagement signals (upvotes, comments)
- No obvious spam

### When to Assign
- Reddit discussion with technical depth → Tier 5
- Hacker News comments → Tier 5
- Medium post from unknown author → Tier 5
- Forum thread with solutions → Tier 5

---

## Tier 6: UNVERIFIED (Weight: 0.2)

### Definition
Sources with no verifiable credibility. Use only when corroborated by higher-tier sources.

### Examples
| Source Type | Examples |
|-------------|----------|
| Anonymous | Posts without identifiable author |
| Random Blogs | Unknown authors, no track record |
| Social Media | Tweets, posts without verification |
| Marketing | Promotional content disguised as education |
| SEO Content | Thin content farms |

### Indicators
- No verifiable author
- No credentials evident
- No community validation
- Potential commercial bias
- Factual errors present

### When to Assign
- Anonymous blog post → Tier 6
- Tweet from unknown account → Tier 6
- Content farm article → Tier 6
- Marketing whitepaper → Tier 6

---

## Decision Flowchart

```
Is it from the creator/standards body?
├─ YES → TIER 1
└─ NO → Is it peer-reviewed academic work?
         ├─ YES → TIER 2
         └─ NO → Is there editorial oversight or known expert author?
                  ├─ Editorial oversight (news/analysts) → TIER 3
                  └─ Known expert without oversight → TIER 4
                          └─ Unknown author?
                               ├─ Community validation → TIER 5
                               └─ No validation → TIER 6
```

---

## Tier Adjustment Rules

### Downgrade When
- Source is outdated for fast-moving topic (>3 years)
- Author has undisclosed conflicts of interest
- Source has been corrected or partially retracted
- Evidence of significant errors
- Community has rejected conclusions

### Upgrade When
- Multiple independent confirmations
- Source widely cited by higher-tier sources
- Predictions have been validated over time
- Author has since gained recognition
- Content has stood test of time

---

## Domain-Specific Notes

### For AI/ML Topics
- arXiv is common; evaluate by citations and author credentials
- Corporate research blogs (FAIR, Google AI) are Tier 3
- Hugging Face docs are Tier 1 for their tools

### For Programming/Software
- Official language docs are Tier 1
- Stack Overflow high-rep answers are Tier 4
- Random Medium tutorials are Tier 5-6

### For Business/Industry
- Analyst reports (Gartner, Forrester) are Tier 3
- Company press releases are biased but Tier 3 for company facts
- LinkedIn posts are Tier 5-6 depending on author

### For Scientific Topics
- Peer-reviewed journals are Tier 2
- Science journalism is Tier 3
- Preprint without review is Tier 3-4
