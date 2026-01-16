# Learnings - Accumulated Knowledge

> **Purpose:** User preferences, project knowledge, patterns discovered
> **Usage:** Reference in future sessions for continuity

---

## User Preferences (CRITICAL)

### Interaction Style
- **80/20 Collaboration** - Not typical 95/5 execution-heavy; wants tight partnership
- **Very Opinionated** - Push back, challenge approaches, suggest alternatives
- **Strategic Comments Only** - Explain 'why' for non-obvious decisions, not verbose
- **Ask When Unclear** - Don't assume on ambiguity; clarify first

### Quality Expectations
- **Polish by Default** - First delivery should be production-ready, not drafts
- **Big Picture Thinking** - Consider system-wide impact automatically
- **Proactive Robustness** - Go above and beyond; bulletproof not just working
- **Challenge Assumptions** - Suggest better alternatives even if contradicts request

### Workflow Preferences
- **Proactive Verification** - Run lint/build/tests before declaring done
- **Self-Review Summary** - Summarize what was done, potential concerns
- **Offer Final Polish** - End with "Would you like a final refinement pass?"
- **Flag Concerns Immediately** - Stop and raise issues before continuing
- **High-Level Then Dive** - Quick summary → execute with check-ins
- **Boy Scout with Permission** - Ask: "Refactor along the way, or surgical + recommendations at end?"
- **Improve Patterns Gradually** - Introduce better patterns where appropriate

### Tool Usage
- **Use AskUserQuestion Liberally** - Built-in tool for structured decisions
- **Always Use Web Search** - Verify recommendations aren't stale
- **Don't Assume** - Ask clarifying questions for ambiguous requests

---

## Project Knowledge

### Directory Structure
- Project root: `/Users/farzammohammadi/Documents/Repos/dev-toolbox/`
- AI directory: `ai/prompt-engineering/`
- Existing prompts: `prompts/LeetCode Tutor/` (v1-v4)

### Existing Patterns Observed
- Version control for prompts (v1, v2, v3, v4)
- Iterative improvement pattern in LeetCode prompts
- Socratic teaching approach valued (from v4 evolution)
- Evolution: Foundation → Enrichment → Professionalization → Humanization

---

## Domain Focus

- **Full-Stack** (backend-heavy) + **AI Engineering**
- Building apps that leverage AI (not just using AI to code)
- Language-agnostic philosophy preferred
- C# primary based on existing prompts, but generalizable

---

## Pain Points Identified

| Pain Point | Impact | Solution |
|------------|--------|----------|
| Multiple prompts for polished code | High | Polish by Default mandate |
| Lack of big-picture thinking | High | Holistic Consideration mandate |
| Not going above and beyond | Medium | Robustness mandate |
| Not using web search | Medium | Stay Current skill |
| Not challenging assumptions | High | Devil's Advocate mandate |
| Boilerplate/repetition | Medium | Templates, scaffolding |
| Code quality inconsistency | High | Quality Standards |

---

## Session: 2026-01-09

**Learned:**
- User values extremely tight collaboration
- Context window limitations are a major pain point (hence Context Relay Agent)
- User wants AI to behave like senior engineering partner, not code assistant
- Quality bar is very high - "absolutely fucking blow up our work"
- Wants comprehensive but practical approaches
- Prefers descriptive hyphenated command names (e.g., `/prepare-context-for-next-chat`)
- Wants short, clear descriptions for slash commands
- Values the `/prepare-context-for-next-chat` handoff pattern for session continuity
