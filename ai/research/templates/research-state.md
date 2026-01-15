# Research State Template

> Track the current state of research across phases. Used by the Orchestrator to manage progress and enable pause/resume.

---

```markdown
# Research State: [Topic]

**Started**: [timestamp]
**Last Updated**: [timestamp]
**Status**: [IN_PROGRESS / PAUSED / COMPLETE]

---

## Configuration

| Setting | Value |
|---------|-------|
| **Original Query** | [user's query] |
| **Depth Level** | [quick / standard / deep / exhaustive] |
| **Confidence Threshold** | [40% / 60% / 70% / 80%] |
| **Max Iterations** | [varies by depth] |

---

## Phase Progress

| Phase | Status | Notes |
|-------|--------|-------|
| 1. Understanding | [COMPLETE / IN_PROGRESS / PENDING] | [notes] |
| 2. Divergent Research | [status] | [notes] |
| 3. Claim Extraction | [status] | [notes] |
| 4. Adversarial Validation | [status] | [notes] |
| 5. Deliberative Synthesis | [status] | [notes] |
| 6. Depth Recursion | [status] | [notes] |
| 7. Final Assembly | [status] | [notes] |

**Current Phase**: [N] - [Phase Name]

---

## Sub-Questions

| # | Question | Status | Confidence | Notes |
|---|----------|--------|------------|-------|
| 1 | [question text] | [RESEARCHED / PENDING] | [X%] | [notes] |
| 2 | [question text] | [status] | [X%] | [notes] |
| 3 | [question text] | [status] | [X%] | [notes] |
| ... | ... | ... | ... | ... |

**Coverage**: [N/M] sub-questions addressed
**Below Threshold**: [N] sub-questions need more research

---

## Agent Activity

### Scholar
- Status: [COMPLETE / IN_PROGRESS / PENDING]
- Searches: [N]
- Sources found: [N]
- Claims extracted: [N]

### Investigator
- Status: [status]
- Searches: [N]
- Sources found: [N]
- Claims extracted: [N]

### Skeptic
- Status: [status]
- Searches: [N]
- Counter-evidence found: [N]
- Criticisms documented: [N]

### Validator
- Status: [status]
- Claims verified: [N/M]
- Contradictions found: [N]
- Sources evaluated: [N]

### Critic
- Status: [status]
- Issues identified: [N]
- Critical issues: [N]
- Recommendations: [N]

### Synthesizer
- Status: [status]
- Conflicts resolved: [N/M]
- Meta-insights generated: [N]

---

## Research Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Total searches | [N] | [varies by depth] |
| Sources collected | [N] | [varies by depth] |
| Claims extracted | [N] | - |
| Claims verified | [N] | all |
| HIGH confidence claims | [N] | ≥50% |
| LOW confidence claims | [N] | ≤20% |
| Contradictions | [N] unresolved | 0 |
| Counter-evidence items | [N] | ≥3 |

---

## Iteration History

### Iteration 1
- Phase completed: [N]
- Key findings: [summary]
- Gaps identified: [list]

### Iteration 2
- Phase completed: [N]
- Additional findings: [summary]
- Remaining gaps: [list]

[Continue for each iteration in DEEP/EXHAUSTIVE mode]

---

## Pending Actions

### High Priority
- [ ] [Action 1]
- [ ] [Action 2]

### Normal Priority
- [ ] [Action 3]
- [ ] [Action 4]

### If Time Permits
- [ ] [Action 5]

---

## Blockers / Issues

| Issue | Severity | Status | Resolution |
|-------|----------|--------|------------|
| [Issue 1] | HIGH | [OPEN / RESOLVED] | [resolution] |
| [Issue 2] | MEDIUM | [status] | [resolution] |

---

## Resume Instructions

If paused, resume by:
1. Review current phase and status
2. Check pending actions
3. Continue with [specific next step]
4. After completion, update this state file

**Next Action**: [specific instruction for resuming]

---

## Completion Checklist

Before marking complete:
- [ ] All sub-questions addressed
- [ ] Confidence thresholds met (or flagged)
- [ ] Counter-evidence section populated
- [ ] Contradictions resolved or documented
- [ ] All sources evaluated and cited
- [ ] Final report assembled
- [ ] Quality gates passed

---

*Last modified: [timestamp]*
```

---

## Usage Notes

### When to Update
- After completing each phase
- After each search batch
- When encountering blockers
- When pausing research
- After each iteration (DEEP/EXHAUSTIVE)

### For Pause/Resume
This file enables:
- Pausing research mid-way
- Resuming in a new session
- Tracking what's done vs pending
- Debugging issues

### For EXHAUSTIVE Depth
- More detailed iteration tracking
- More granular metric targets
- Longer pending action lists
