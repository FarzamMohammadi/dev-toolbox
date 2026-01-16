---
name: write-fact-check
description: Verify factual claims, validate links, check code accuracy, and gather supporting resources. Fact-checking mode for existing content.
---

# /write-fact-check - Fact-Check Mode

You are verifying claims and gathering supporting evidence for existing content.

## What This Does

1. Identify all factual claims
2. Verify with authoritative sources
3. Validate links and code
4. Document sources
5. Suggest corrections

## Instructions

### Step 1: Get Content

Ask: "Share the content you'd like me to fact-check. I'll verify all claims, links, and code."

### Step 2: Identify Claims

Scan content for:
- Statistics and numbers
- Technical specifications
- Version information
- "Best practice" claims
- Performance claims
- Specific dates/timelines
- Command syntax
- Package/tool names

Categorize:
- **Critical:** Readers will act on this
- **Important:** Affects credibility
- **Background:** Nice to verify

### Step 3: Verify Claims

For each claim:
1. Search for authoritative sources
2. Check official documentation
3. Cross-reference multiple sources

Document:
```markdown
### Claim: "[exact claim]"
**Location:** [where in content]
**Status:** ✅ Verified / ⚠️ Partially / ❌ Wrong / 🔄 Outdated

**Sources:**
- [Source 1]
- [Source 2]

**Notes:** [any caveats]
**Action:** Keep / Update to: [correction] / Remove
```

### Step 4: Validate Links

For each link:
- Check if URL is valid format
- Attempt to verify content matches description
- Note any redirects

### Step 5: Check Code

For code blocks:
- Verify syntax is correct
- Check commands exist
- Verify against current versions
- Note deprecated patterns

### Step 6: Generate Report

```markdown
## Fact-Check Report

### Summary
- Claims checked: X
- Verified: Y
- Needs correction: Z
- Could not verify: W

### Critical Findings
[Any wrong claims that could mislead readers]

### Corrections Required
| Original | Correction | Source |
|----------|------------|--------|
| [Wrong] | [Right] | [URL] |

### Verified Claims
[Claims confirmed with sources]

### Unverifiable
[Claims that couldn't be verified - recommend action]

### Link Status
| Link | Status | Notes |
|------|--------|-------|
| [URL] | ✅/❌/⚠️ | [Notes] |

### Code Status
| Block | Status | Notes |
|-------|--------|-------|
| [Code] | ✅/⚠️/❌ | [Notes] |

### Source Quality
- Official docs: X
- Established sources: Y
- Needs better source: Z
```

### Step 7: Offer Next Steps

Ask: "Would you like me to:
1. Apply these corrections?
2. Find better sources for unverified claims?
3. Gather additional supporting resources?"

## Source Evaluation

### Prefer
- Official documentation
- First-party blog posts
- Peer-reviewed sources
- Established publications

### Accept with Caution
- Stack Overflow (verified answers)
- Wikipedia (verify further)
- Well-known tech blogs

### Avoid
- Random blog posts
- Outdated content (>2 years for tech)
- Sources with commercial bias

## Reference Files

- Fact-checking: `ai/toolkits/writing/agents/fact-checker.md`
- Report template: `ai/toolkits/writing/templates/fact-check-report.md`

## Begin

Start with: "I'll fact-check your content. Share it here and I'll verify all claims, links, and code."
