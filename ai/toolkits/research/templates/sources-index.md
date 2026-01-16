# Sources Index Template

> Template for the separate sources file, organized by domain with statistics.

---

## File Naming

Output file: `[topic-slug]-sources.md`

Example: For "RAG best practices" → `rag-best-practices-sources.md`

---

## Template Structure

```markdown
# Sources Index: [Topic]

**Generated**: [Date]
**Research Depth**: [quick|standard|deep|exhaustive]
**Total Sources**: [N]
**Total Domains**: [N]

---

## Summary by Domain

| Domain | Sources | Tier Range | Primary Use |
|--------|---------|------------|-------------|
| arxiv.org | 19 | T1-T2 | Academic foundations |
| github.com | 26 | T3-T4 | Implementation examples |
| docs.*.com | 24 | T1-T3 | Official documentation |
| *.medium.com | 8 | T4-T5 | Practitioner perspectives |
| reddit.com | 5 | T5 | Community discussion |
| ... | ... | ... | ... |

---

## Tier 1-2 Sources (Academic & Primary)

### arxiv.org ([N] sources)

#### 1. [Paper Title]
- **URL**: https://arxiv.org/abs/XXXX.XXXXX
- **Authors**: [Author list]
- **Year**: [YYYY]
- **Tier**: 2 (Peer-Reviewed)
- **Citations**: [N] (if available)
- **Used for**: Sub-questions [1, 3, 5]
- **Key claims**:
  - [Claim 1 extracted from this source]
  - [Claim 2 extracted from this source]
- **Reliability notes**: [Any caveats about this source]

#### 2. [Paper Title]
...

### Official Documentation ([N] sources)

#### 1. [Doc Title]
- **URL**: https://docs.example.com/...
- **Publisher**: [Organization]
- **Last Updated**: [Date if available]
- **Tier**: 1 (Primary - Official)
- **Used for**: Sub-questions [2, 4]
- **Key claims**:
  - [Claim extracted]
- **Reliability notes**: Official source, highly reliable

---

## Tier 3-4 Sources (Authoritative & Expert)

### github.com ([N] sources)

#### 1. [Repo Name]
- **URL**: https://github.com/org/repo
- **Type**: Repository / Discussion / Issue
- **Stars**: [N]k (if repo)
- **Tier**: 3 (Authoritative) or 4 (Expert Community)
- **Used for**: Sub-questions [2]
- **Key claims**:
  - [Implementation pattern observed]
  - [Best practice documented]
- **Reliability notes**: [Official org repo / Community project / etc.]

### Technical Blogs ([N] sources)

#### 1. [Article Title]
- **URL**: https://blog.example.com/...
- **Author**: [Name] ([credentials if known])
- **Published**: [Date]
- **Tier**: 4 (Expert Community)
- **Used for**: Sub-questions [3, 6]
- **Key claims**:
  - [Claim extracted]
- **Reliability notes**: [Author credibility assessment]

---

## Tier 5-6 Sources (Community & Unverified)

### reddit.com ([N] sources)

#### 1. [Thread Title]
- **URL**: https://reddit.com/r/...
- **Subreddit**: r/[subreddit]
- **Upvotes**: [N]
- **Tier**: 5 (Community)
- **Used for**: Sub-questions [4]
- **Key claims**:
  - [Community consensus observed]
- **Reliability notes**: Anecdotal; corroborated by [other sources] OR uncorroborated

### Other Web ([N] sources)

#### 1. [Page Title]
- **URL**: https://...
- **Tier**: 6 (Unverified)
- **Used for**: [Context only / Minor point]
- **Key claims**:
  - [Claim - LOW confidence]
- **Reliability notes**: Unverified source; claim requires independent verification

---

## Source Statistics

### By Tier

| Tier | Description | Count | % | Avg Weight |
|------|-------------|-------|---|------------|
| 1 | Primary | [N] | [%] | 1.0 |
| 2 | Peer-Reviewed | [N] | [%] | 0.9 |
| 3 | Authoritative | [N] | [%] | 0.75 |
| 4 | Expert Community | [N] | [%] | 0.6 |
| 5 | Community | [N] | [%] | 0.4 |
| 6 | Unverified | [N] | [%] | 0.2 |
| **Total** | | **[N]** | **100%** | **[avg]** |

### By Domain Type

| Type | Domains | Sources | % |
|------|---------|---------|---|
| Academic (arxiv, acm, ieee) | [N] | [N] | [%] |
| Documentation (docs.*, learn.*) | [N] | [N] | [%] |
| Code (github, gitlab) | [N] | [N] | [%] |
| News/Media | [N] | [N] | [%] |
| Blogs/Personal | [N] | [N] | [%] |
| Community (reddit, SO, forums) | [N] | [N] | [%] |
| Other | [N] | [N] | [%] |

### Quality Metrics

- **Tier 1-2 coverage**: [%] of claims backed by high-tier sources
- **Cross-verification rate**: [%] of claims verified by 2+ independent sources
- **Recency**: [N]% sources from last 2 years
- **Diversity score**: [N] unique domains across [N] sources

---

## Domain Details

### Top Domains by Source Count

1. **[domain.com]** - [N] sources
   - Tier range: [T1-T3]
   - Primary contribution: [What this domain contributed]

2. **[domain2.com]** - [N] sources
   - Tier range: [T2-T4]
   - Primary contribution: [What this domain contributed]

...

---

## Unused/Rejected Sources

Sources that were found but not included in the final report:

| URL | Reason for Exclusion |
|-----|---------------------|
| [URL] | Outdated (>3 years, superseded) |
| [URL] | Low credibility (unverifiable claims) |
| [URL] | Duplicate content (same as [other source]) |
| [URL] | Off-topic (didn't address research questions) |
| [URL] | Paywall (couldn't access full content) |

---

## Citation Quick Reference

For easy copy-paste into other documents:

### Academic Style
[1] Author et al., "Title," Venue, Year. URL

### Inline Links
- [Short description](URL)
- [Short description](URL)

### Numbered List
1. URL - Brief description
2. URL - Brief description

---

*Generated by Research Parliament | [Date]*
```

---

## Usage Instructions

When generating the sources index:

1. **Collect all sources** during research phases
2. **Extract domain** from each URL
3. **Group by domain**, sorted by source count (descending)
4. **Within each domain**, sort by tier (ascending) then by relevance
5. **Calculate statistics** for the summary tables
6. **Include rejected sources** to show thoroughness

---

## Quality Checklist

Before finalizing sources index:

- [ ] Every cited source in the report appears here
- [ ] Tier assignments are consistent with `source-hierarchy.md`
- [ ] Key claims extracted for each source
- [ ] Statistics calculated correctly
- [ ] Domains properly categorized
- [ ] Rejected sources documented with reasons
