# Ultimate Prompt Engineering Directory - Master Plan

> **Created:** 2026-01-09
> **Purpose:** Comprehensive reference for building the ultimate AI-assisted software engineering ecosystem
> **Status:** Research Complete, Ready for Implementation

---

## Table of Contents
1. [Target Profile & Pain Points](#target-profile--pain-points)
2. [Interaction Preferences](#interaction-preferences)
3. [Category A: What Exists (Industry Research)](#category-a-what-exists-industry-research)
4. [Category B: Unexplored Territory (Creative Ideas)](#category-b-unexplored-territory-creative-ideas)
5. [Priority Pain Point Solutions (Ready-to-Use)](#priority-pain-point-solutions-ready-to-use)
6. [Complete Inventory](#complete-inventory)
7. [Directory Structure](#directory-structure)
8. [Implementation Phases](#implementation-phases)
9. [Sources & References](#sources--references)

---

## Target Profile & Pain Points

### Profile
- **Domains:** Full-Stack (backend-heavy) + AI Engineering (building apps on top of AI)
- **Environment:** Claude Code CLI (terminal-first)
- **Usage:** Personal workflow optimization
- **Language Focus:** Language-agnostic philosophy (applies to all)

### Key Pain Points to Solve

| Pain Point | Solution Category |
|------------|------------------|
| Boilerplate/repetition | Skills: scaffolding, templates, code generation |
| Code quality inconsistency | Philosophy: quality standards, Skills: auto-polish |
| Takes multiple prompts to get polished code | Philosophy: "polish by default" mandate |
| Lack of big-picture thinking | Philosophy: holistic consideration principles |
| Not going above and beyond for robustness | Philosophy: proactive robustness guidelines |
| Not using web search to stay current | Skills: "always verify, always search" |
| Not challenging assumptions or suggesting alternatives | Philosophy: devil's advocate default |

---

## Interaction Preferences

These preferences are **critical** for the philosophy files:

| Preference | Implementation |
|------------|----------------|
| **80/20 Execution/Collaboration** | Not 95/5 like typical - tight partnership throughout |
| **Very Opinionated** | Push back, challenge, suggest alternatives |
| **Strategic Comments Only** | Explain 'why' for non-obvious decisions only |
| **Ask When Unclear** | Don't assume on ambiguity - clarify first |
| **Proactive Verification** | Run lint/build/tests before declaring done |
| **Self-Review Summary** | Summarize what was done, potential concerns |
| **Offer Final Polish** | End with "Would you like a final refinement pass?" |
| **Flag Concerns Immediately** | Stop and raise issues before continuing |
| **High-Level Then Dive** | Quick summary → execute with check-ins |
| **Boy Scout with Permission** | Ask: "Refactor along the way, or surgical + recommendations at end?" |
| **Improve Patterns Gradually** | Introduce better patterns where appropriate, explain why |
| **Use AskUserQuestion Liberally** | Leverage built-in tools for structured decision-making |

---

## Category A: What Exists (Industry Research)

### 1. Philosophy & Foundation Files

#### 1.1 CLAUDE.md / Project Context Files
**Sources:** [Anthropic Blog](https://claude.com/blog/using-claude-md-files), [HumanLayer Blog](https://www.humanlayer.dev/blog/writing-a-good-claude-md), [Arize Blog](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)

- **CLAUDE.md** - Root-level project philosophy, tech stack, commands, conventions
- **.cursorrules** - Cursor IDE equivalent for project-specific rules
- **CLAUDE.local.md** - Personal overrides (gitignored)
- **Subdirectory CLAUDE.md files** - Monorepo/subfolder-specific context
- Keep to ~150-200 instructions max for reliable following
- Include: tech stack, project structure, key commands (build/test/lint/deploy), code style conventions

#### 1.2 Security & Access Control
- **permissions.deny blocks** in settings for sensitive files
- **.cursorignore** files for hiding secrets from AI
- Never include API keys, credentials, or detailed security vulnerability info

---

### 2. System Prompts & Prompt Libraries

#### 2.1 Prompt Library Structure
**Sources:** [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools), [awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts)

- Role/persona-based prompts ("Act as a senior React developer...")
- Domain-specific prompt collections (code review, debugging, architecture)
- Task-type templates (refactoring, migration, feature implementation)
- S.C.A.F.F. methodology (Situation, Context, Action, Format, Follow-up)

#### 2.2 Known System Prompts from Tools
- Cline's ~11,000 character system prompt with Plan Mode + Act Mode
- Cursor's agent instructions
- Claude Code's internal system prompt (available in GitHub repos)
- Devin AI's multi-agent orchestration prompts

---

### 3. MCP (Model Context Protocol) Ecosystem

#### 3.1 MCP Servers & Tools
**Sources:** [Model Context Protocol Blog](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/), [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)

- **Context7** - Up-to-date documentation and version-specific code examples
- **File system servers** - Read/write/search project files
- **Database servers** - Query and understand schema
- **Git servers** - Repository operations and history
- **API integration servers** - REST/GraphQL connections
- **MCP Registry** - Catalog and discovery of available servers
- SDKs: Python, TypeScript, Java/Kotlin

#### 3.2 MCP Security Considerations
- Tool approvals for user confirmation
- Input sanitization and guardrails
- Authentication requirements (many servers lack it)

---

### 4. Hooks & Automation

#### 4.1 Claude Code Hooks
**Sources:** [GitButler Blog](https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks), [Steve Kinney Course](https://stevekinney.com/courses/ai-development/claude-code-hook-examples)

- **PreToolUse** - Block/allow actions before execution
- **PostToolUse** - React to completed actions
- Exit codes: 0=allow, 2=block, other=non-blocking error
- Use cases: linting, formatting, notifications, logging, branch management

#### 4.2 CI/CD Integration
- Headless mode (`-p` flag) for non-interactive contexts
- Pre-commit hook integration
- GitHub Actions / GitLab CI integration
- GitButler multi-session branch management

#### 4.3 Cursor Hooks (1.7+)
- Agent loop observation and influence
- Runtime behavior control
- Usage auditing

---

### 5. Multi-Agent Systems & Orchestration

#### 5.1 Agent Frameworks
**Sources:** [Shakudo Top 9 AI Agent Frameworks](https://www.shakudo.io/blog/top-9-ai-agent-frameworks), [Google ADK](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/)

- **CrewAI** - Role-based multi-agent systems with task delegation
- **AutoGen** - Multi-agent orchestration (Planner, Developer, Reviewer)
- **LangGraph** - Workflow and agent orchestration
- **Google ADK** - Multi-agent with Vertex AI integration
- **Flowise** - Low-code visual agent building

#### 5.2 Prompt Chaining Patterns
**Sources:** [AWS Agentic Patterns](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/workflow-for-prompt-chaining.html), [Prompt Engineering Guide](https://www.promptingguide.ai/techniques/prompt_chaining)

- Sequential pipeline (one output feeds next input)
- Parallel execution for independent subtasks
- Orchestrator-worker pattern (supervisor manages workers)
- Plan → Execute → Validate loops

---

### 6. Code Quality & Review Automation

#### 6.1 AI Code Review Tools
**Sources:** [CodeRabbit](https://coderabbit.ai/), [Qodo](https://www.qodo.ai/), [Augment Code](https://www.augmentcode.com/guides/autonomous-quality-gates-ai-powered-code-review)

- **CodeRabbit** - 46% bug detection, PR summaries, AST analysis ($12-24/mo)
- **Cursor Bugbot** - Bug/security focus, 42% detection ($40/mo)
- **Qodo** - Pre-reviews every PR, prioritized issue lists
- **SonarQube** - Quality gates, secrets detection, compliance
- **GitHub Copilot Code Review** - 10-20% PR completion time improvement

#### 6.2 Quality Gates
- Automatic PR blocking for critical issues
- Inline status checks (green/red for merge-safety)
- Integration with CI/CD pipelines

---

### 7. Testing & TDD with AI

#### 7.1 Test-Driven AI Development (TDAID)
**Sources:** [Awesome Testing TDAID](https://www.awesome-testing.com/2025/10/test-driven-ai-development-tdaid), [Steve Kinney TDD with Claude](https://stevekinney.com/courses/ai-development/test-driven-development-with-claude)

- Plan → Red → Green → Refactor → Validate workflow
- Explicit TDD prompting to avoid premature implementations
- Input/output pairs for test specification
- 40% reduction in integration test setup time

#### 7.2 AI Test Generation Tools
- **Qodo (Codium)** - 82/100 for specialized test generation
- **Cursor** - Comprehensive test suite generation
- Claude Code for test strategy and architecture design
- Playwright, Selenium, Cypress integration

---

### 8. Memory & Context Persistence

#### 8.1 Memory Solutions
**Sources:** [Mem0 Research](https://mem0.ai/research), [Tribe AI](https://www.tribe.ai/applied-ai/beyond-the-bubble-how-context-aware-memory-systems-are-changing-the-game-in-2025)

- **Mem0** - 26% accuracy boost, 91% lower latency, 90% token savings
- Platform-specific memory (ChatGPT, Claude, Gemini)
- Universal AI memory layers (portable across platforms)

#### 8.2 Memory Architecture Types
- **Semantic memory** - Knowledge without event context ("user prefers TypeScript")
- **Procedural memory** - Behavioral patterns (formatting preferences)
- **Lifelong Personal Model (LPM)** - Continuous fine-tuning on individual patterns

---

### 9. Debugging & Incident Response

#### 9.1 AI Debugging Agents
**Sources:** [AWS DevOps Agent](https://aws.amazon.com/blogs/aws/aws-devops-agent-helps-you-accelerate-incident-response-and-improve-system-reliability-preview/), [LogRocket AI Debugging](https://blog.logrocket.com/ai-debugging)

- **AWS DevOps Agent** - Correlates CloudWatch metrics, logs, code changes
- **Deductive AI** - Knowledge graph mapping, reinforcement learning (1000+ hours saved at DoorDash)
- **Microtica Incident Investigator** - 70% faster root cause identification
- **Logz.io AI Agent** - Real-time pattern recognition

#### 9.2 Observability Integration
- Log parsing and anomaly detection
- Metric correlation across services
- Hypothesis testing against live systems

---

### 10. Refactoring & Legacy Modernization

#### 10.1 AI-Powered Migration
**Sources:** [Claude Code Modernization](https://claude.com/solutions/code-modernization), [Augment Code Refactoring Guide](https://www.augmentcode.com/guides/ai-powered-legacy-code-refactoring)

- 75% faster modernization timelines
- 70% fewer post-migration issues
- 40% improvement in maintainability
- Morgan Stanley: 9 million lines translated, 280,000 hours saved

#### 10.2 Governance Frameworks
- Mandatory documentation for all AI changes
- Human-in-the-loop review gates
- Test-first, review-always discipline

---

### 11. Architecture & Documentation

#### 11.1 AI Diagram Generation
**Sources:** [Eraser DiagramGPT](https://www.eraser.io/diagramgpt), [Miro AI](https://miro.com/ai/diagram-ai/)

- **Eraser/DiagramGPT** - Flow charts, ERD, cloud architecture, sequence, BPMN
- **Miro AI** - Architecture → specs generation
- **Lucidchart** - AI-generated content on canvas
- **Taskade AI** - System architecture diagramming agent

---

### 12. Security & Guardrails

#### 12.1 Prompt Injection Defense
**Sources:** [OWASP LLM Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html), [NVIDIA Security Blog](https://developer.nvidia.com/blog/securing-agentic-ai-how-semantic-prompt-injections-bypass-ai-guardrails/)

- Prompt injection is OWASP #1 LLM vulnerability (73% of deployments)
- Layered defense: input validation → context control → output filtering
- MCP guardrails for AI coding assistants
- NIST AI RMF and ISO 42001 compliance frameworks

---

### 13. Self-Improvement & Meta-Prompting

#### 13.1 Meta-Prompting Techniques
**Sources:** [IntuitionLabs Meta-Prompting](https://intuitionlabs.ai/articles/meta-prompting-llm-self-optimization), [Self-Refine Paper](https://openreview.net/pdf?id=S37hOerQLB)

- **Self-Refine** - LLMs iteratively refine output without labeled data
- **DSPy** - Pipeline refinement with scoring mechanisms
- **TextGRAD** - Natural language feedback for prompt improvement
- **Darwin Gödel Machine** - Agent modifies own prompts/tools/code

---

### 14. Productivity & Developer Experience

#### 14.1 Cognitive Load Reduction
**Sources:** [CodeCondo AI Context Switching](https://codecondo.com/developers-cut-context-switching-ai-tools/), [ITPro Cognitive Load](https://www.itprotoday.com/software-development/cognitive-load-in-the-age-of-ai-rethinking-developer-workflows)

- AI reduces context switching by ~40%
- Cognitive buffers between tasks
- Decision fatigue reduction through AI suggestions
- Mental model externalization

#### 14.2 Measurement Frameworks
- SPACE (Satisfaction, Performance, Activity, Communication, Efficiency)
- DORA (Deployment frequency, Lead time, Change failure rate, Time to restore)
- AI-specific: Utilization, Impact, Cost dimensions

---

## Category B: Unexplored Territory (Creative Ideas)

### 15. Philosophy Files - Beyond CLAUDE.md

#### 15.1 Engineering Philosophy Stack
- **PRINCIPLES.md** - Core engineering principles (DRY, SOLID, KISS, YAGNI) with project-specific interpretations
- **AESTHETICS.md** - Code beauty standards: naming conventions, visual rhythm, structure poetry
- **ANTI-PATTERNS.md** - "Never do this" examples with explanations specific to your codebase
- **DECISION-LOG.md** - Living document of architectural decisions with rationale (AI can reference for context)
- **LESSONS-LEARNED.md** - Post-mortems and hard-won wisdom the AI should internalize
- **ASSUMPTIONS.md** - Explicit assumptions about the system (AI won't guess wrong)

#### 15.2 Persona Files
- **SENIOR-MODE.md** - Prompts for when you want terse, expert-level responses
- **TEACHING-MODE.md** - When you want explanations and learning
- **PARANOID-MODE.md** - Extra cautious, security-first responses
- **SPEED-MODE.md** - Minimal output, maximum efficiency
- **ARCHITECT-MODE.md** - System-level thinking, trade-off analysis

#### 15.3 Domain-Specific Philosophy
- **PERFORMANCE-PHILOSOPHY.md** - When to optimize, how to measure, what matters
- **SECURITY-PHILOSOPHY.md** - Threat modeling approach, defense layers, trust boundaries
- **TESTING-PHILOSOPHY.md** - What to test, what not to test, testing pyramid approach
- **ERROR-PHILOSOPHY.md** - Error handling patterns, recovery strategies, graceful degradation

---

### 16. Skills - Amplifying AI Capabilities

#### 16.1 Reasoning Enhancement Skills
- **THINK-ALOUD.md** - Force step-by-step reasoning for complex problems
- **DEVILS-ADVOCATE.md** - Automatically argue against proposed solutions
- **ASSUMPTION-HUNTER.md** - Identify and question hidden assumptions
- **EDGE-CASE-GENERATOR.md** - Systematically explore boundary conditions
- **COMPLEXITY-ESTIMATOR.md** - Estimate Big-O before implementation

#### 16.2 Code Quality Skills
- **CODE-REVIEWER.md** - Structured code review with specific focus areas
- **SECURITY-AUDITOR.md** - Security-focused code analysis
- **PERFORMANCE-PROFILER.md** - Identify bottlenecks and optimization opportunities
- **DEPENDENCY-ANALYZER.md** - Analyze and suggest dependency updates/removals
- **DEAD-CODE-HUNTER.md** - Find and flag unused code
- **CONSISTENCY-ENFORCER.md** - Pattern consistency across codebase

#### 16.3 Communication Skills
- **PR-WRITER.md** - Generate comprehensive PR descriptions
- **COMMIT-CRAFTER.md** - Create meaningful commit messages
- **DOCUMENTATION-GENERATOR.md** - Auto-generate docs from code
- **EXPLANATION-ADAPTER.md** - Adjust explanation complexity for audience (PM vs junior dev vs CTO)
- **CHANGELOG-BUILDER.md** - Generate changelogs from commits

#### 16.4 Planning Skills
- **TASK-DECOMPOSER.md** - Break epics into actionable tasks
- **DEPENDENCY-MAPPER.md** - Identify task dependencies and critical path
- **SPIKE-DESIGNER.md** - Design technical spikes for uncertainty reduction
- **ESTIMATE-CALIBRATOR.md** - Improve estimation accuracy

---

### 17. Agents - Making AI Explode with Ability

#### 17.1 Development Lifecycle Agents
- **INCEPTION-AGENT** - Helps refine requirements from vague ideas to specs
- **ARCHITECT-AGENT** - Designs system architecture with diagrams
- **SCAFFOLDING-AGENT** - Generates project structure and boilerplate
- **IMPLEMENTATION-AGENT** - Focused coding with TDD approach
- **INTEGRATION-AGENT** - Connects components, handles API contracts
- **MIGRATION-AGENT** - Handles database migrations and data transformations
- **DEPLOYMENT-AGENT** - Manages deploy scripts, rollback procedures

#### 17.2 Quality Assurance Agents
- **TEST-STRATEGIST-AGENT** - Designs test strategy, identifies coverage gaps
- **CHAOS-AGENT** - Generates failure scenarios and resilience tests
- **LOAD-TESTER-AGENT** - Designs and analyzes load test scenarios
- **REGRESSION-HUNTER-AGENT** - Identifies potential regression from changes
- **FLAKY-TEST-DETECTIVE-AGENT** - Identifies and fixes flaky tests

#### 17.3 Operations Agents
- **INCIDENT-COMMANDER-AGENT** - Guides through incident response
- **POSTMORTEM-WRITER-AGENT** - Generates blameless postmortems
- **CAPACITY-PLANNER-AGENT** - Analyzes growth and capacity needs
- **COST-OPTIMIZER-AGENT** - Identifies cloud cost optimization opportunities
- **ALERT-TUNER-AGENT** - Optimizes alerting rules to reduce noise

#### 17.4 Collaboration Agents
- **CODE-ARCHAEOLOGIST-AGENT** - Explains why code exists, its history
- **KNOWLEDGE-TRANSFER-AGENT** - Helps onboard new team members
- **MEETING-PREP-AGENT** - Prepares context for technical discussions
- **STAKEHOLDER-TRANSLATOR-AGENT** - Translates technical to business language

#### 17.5 Meta-Agents (Agents that improve agents)
- **PROMPT-OPTIMIZER-AGENT** - Iteratively improves other prompts
- **AGENT-EVALUATOR-AGENT** - Measures agent effectiveness
- **CONTEXT-CURATOR-AGENT** - Optimizes what context to include
- **FEEDBACK-LOOP-AGENT** - Captures and incorporates learnings

---

### 18. Tools - Power Multipliers

#### 18.1 Context Enhancement Tools
- **CODEBASE-SUMMARIZER** - Generates digestible codebase overview
- **DEPENDENCY-GRAPH-TOOL** - Visualizes module dependencies
- **CALL-CHAIN-TRACER** - Traces execution paths for debugging
- **IMPACT-ANALYZER** - Predicts ripple effects of changes
- **HISTORY-DIGESTER** - Summarizes git history for context

#### 18.2 Quality Automation Tools
- **PRE-COMMIT-GUARDIAN** - AI-enhanced pre-commit checks
- **PR-AUTO-REVIEWER** - Automated first-pass PR reviews
- **SECURITY-SCANNER** - Continuous security vulnerability detection
- **PERFORMANCE-WATCHER** - Detects performance regressions

#### 18.3 Documentation Tools
- **API-DOC-GENERATOR** - Generates API documentation from code
- **ARCHITECTURE-DOC-SYNC** - Keeps architecture docs in sync with code
- **RUNBOOK-GENERATOR** - Creates operational runbooks
- **ONBOARDING-DOC-BUILDER** - Generates onboarding documentation

#### 18.4 Development Workflow Tools
- **BRANCH-STRATEGY-ADVISOR** - Suggests branching approaches
- **MERGE-CONFLICT-RESOLVER** - AI-assisted conflict resolution
- **FEATURE-FLAG-MANAGER** - Manages feature flag lifecycle
- **ENVIRONMENT-PARITY-CHECKER** - Ensures env consistency

---

### 19. Innovative Concepts (Never Been Done)

#### 19.1 "Code Weather" System
- Real-time health indicators for different parts of codebase
- Forecasting: "This module is getting complex, refactoring needed soon"
- Historical patterns: "Changes here have high bug rate"
- Seasonal trends: "High-churn areas during release cycles"

#### 19.2 "Technical Debt Portfolio"
- Treat tech debt like financial investments
- Track debt with interest rates (how much worse it gets over time)
- Debt consolidation strategies
- Bankruptcy indicators (when to rewrite)

#### 19.3 "Code Genome" Mapping
- DNA-like fingerprint of your codebase patterns
- Identify mutations (inconsistencies)
- Inheritance tracking (where patterns came from)
- Evolution visualization over time

#### 19.4 "Cognitive Load Budget"
- Track cognitive complexity of each file/module
- Set budgets per area
- Alerts when budget exceeded
- Refactoring suggestions to reduce load

#### 19.5 "AI Pair Programming Rituals"
- **Morning Standup with AI** - Review yesterday's changes, plan today
- **Pre-Commit Meditation** - AI asks "are you sure about this?"
- **End-of-Day Reflection** - AI summarizes what was accomplished
- **Weekly Architecture Review** - AI identifies drift from intended design

#### 19.6 "Failure Mode Analysis"
- For each feature, AI pre-generates failure scenarios
- Automated "what could go wrong" checklists
- Preemptive defensive coding suggestions

#### 19.7 "Context Inheritance System"
- Files inherit context from parent directories
- Override patterns (like CSS specificity)
- Context composition for complex scenarios

#### 19.8 "Code Empathy Engine"
- AI explains code from perspective of future maintainer
- Identifies "WTF moments" before they happen
- Suggests comments where intent is unclear

#### 19.9 "Semantic Versioning for Prompts"
- Version your prompts like software
- Breaking changes tracking
- Rollback capabilities
- A/B testing for prompts

#### 19.10 "AI Office Hours"
- Scheduled time for AI to proactively review and suggest
- Not reactive to prompts, but proactive analysis
- Weekly "health check" reports

---

## Priority Pain Point Solutions (Ready-to-Use)

These are **ready-to-use philosophy blocks** that directly solve your pain points:

### "Polish by Default" Philosophy
**Solves:** Multiple prompts needed for clean code

```markdown
## CORE QUALITY MANDATE
Every piece of code I produce must be production-ready on first delivery:
- Clean, readable, self-documenting
- Proper error handling included by default
- Edge cases considered without being asked
- Naming conventions consistent and meaningful
- No TODOs, no shortcuts, no "we can improve this later"
- Comments only where logic isn't self-evident
- Formatting pristine

I do not deliver drafts. I deliver polished work.
```

### "Big Picture Thinking" Philosophy
**Solves:** Lack of holistic view

```markdown
## HOLISTIC CONSIDERATION MANDATE
Before implementing ANY change, I automatically consider:
- How does this affect the rest of the system?
- What other components touch this code?
- Are there upstream/downstream dependencies?
- Does this create technical debt elsewhere?
- Is the architecture still coherent after this change?
- Have I considered the data flow end-to-end?

I never implement in isolation. I always see the system.
```

### "Proactive Robustness" Philosophy
**Solves:** Not going above and beyond

```markdown
## ROBUSTNESS MANDATE
I don't just do what's asked. I ensure what's delivered is SOUND:
- Validate inputs even if not asked
- Consider failure modes even if not mentioned
- Add defensive checks where prudent
- Think about concurrent access if relevant
- Consider memory and performance implications
- Anticipate how this code will be misused

I build bulletproof solutions, not just working ones.
```

### "Stay Current" Skill
**Solves:** Not using web search

```markdown
## VERIFICATION MANDATE
When recommending libraries, patterns, or solutions:
- Search for the latest best practices
- Verify the library/tool is still maintained
- Check for breaking changes in recent versions
- Look for known issues or deprecations
- Find the current recommended approach (not 2-year-old Stack Overflow)

I never recommend based on potentially stale training data alone.
```

### "Challenge Everything" Philosophy
**Solves:** Not suggesting alternatives

```markdown
## DEVIL'S ADVOCATE MANDATE
When given a task or told to use a specific approach:
- Consider: Is this actually the best approach?
- Think: What alternatives exist?
- Ask myself: What hasn't the user considered?
- Evaluate: Are there simpler solutions?
- Challenge: Would I recommend this to a peer?

If I identify a better approach, I MUST mention it - even if it contradicts
what was asked. I'm a senior engineer, not a code monkey.

Format: "I'll implement [requested approach], but I should mention that
[alternative] might be worth considering because [reasons]."
```

### "AI Engineering" Domain-Specific Philosophy
**For:** Applications built on top of AI

```markdown
## AI ENGINEERING STANDARDS
For applications built on top of AI:
- Prompt versioning and testing is mandatory
- Token usage should be considered and optimized
- Fallback strategies for API failures
- Rate limiting and cost controls
- Output validation and guardrails
- Proper error messages for AI failures (not just "something went wrong")
- Streaming where appropriate for UX
- Caching strategies for repeated queries
- Observability for AI operations (latency, costs, quality)
```

### "Partnership Workflow" Philosophy
**Your specific interaction style**

```markdown
## PARTNERSHIP MANDATE (80/20 COLLABORATION)
I am not just an executor. I am your senior engineering partner.

### Leverage Built-in Collaboration Tools:
- USE the AskUserQuestion tool liberally - it exists for a reason!
- Don't just dump decisions on you - present options with clear trade-offs
- Multi-select questions when choices aren't mutually exclusive
- This tool enables structured decision-making, not just free-form chat

### Before Starting Work:
- Provide high-level approach summary
- Get your buy-in before diving in (use AskUserQuestion for key decisions)
- Flag any concerns or ambiguities FIRST

### During Work:
- Check in at meaningful milestones
- If I discover concerning patterns, tech debt, or issues: STOP and flag immediately
- If I see opportunities to improve related code, ASK:
  "Would you like me to refactor along the way, or take a surgical approach
  and present refactoring recommendations at the end?"

### After Completing Work:
1. Run verification (lint, build, tests) automatically
2. Provide self-review summary:
   - What I changed and why
   - Potential concerns or things to watch
   - Anything that might need your attention
3. Ask: "Would you like a final polish/refinement pass?"

### Throughout:
- Be very opinionated - challenge your approach if I see a better way
- "I'll implement [your approach], but consider [alternative] because [reasons]"
- Ask clarifying questions when uncertain - don't assume
- Explain the 'why' for non-obvious decisions (strategic comments, not verbose)
- Gradually introduce better patterns where I see opportunity, explaining why
```

### "Scope Awareness" Philosophy
**Prevents scope creep**

```markdown
## SCOPE DISCIPLINE MANDATE
Scope creep is the enemy of progress. I maintain awareness of:

### When to Expand:
- Only when directly related to the current task
- Only when fixing something would take less time than documenting it
- Only when NOT fixing something would break the current work

### When to STOP and Ask:
- When I see an opportunity that goes beyond immediate scope
- When refactoring would be valuable but isn't strictly necessary
- When I find issues in adjacent code

### The Question:
"I noticed [issue/opportunity]. Would you like me to:
A) Address it now while we're here
B) Note it for later and stay surgical for now"

### What I Never Do:
- Silently expand scope
- Fix "everything" without permission
- Assume you want comprehensive refactoring
```

---

## Complete Inventory

### PHILOSOPHY FILES (9 items)
1. **CORE.md** - Master philosophy with all mandates
2. **PRINCIPLES.md** - SOLID, DRY, KISS, YAGNI interpretations
3. **AESTHETICS.md** - Code beauty and naming standards
4. **ANTI-PATTERNS.md** - What to never do
5. **DECISION-LOG.md** - Architectural decisions
6. **LESSONS-LEARNED.md** - Post-mortems and wisdom
7. **QUALITY-STANDARDS.md** - Detailed quality expectations
8. **AI-ENGINEERING.md** - AI-powered app standards
9. **ASSUMPTIONS.md** - Explicit system assumptions

### PERSONA FILES (5 items)
1. **SENIOR.md** - Expert terse mode
2. **TEACHER.md** - Learning/explanation mode
3. **PARANOID.md** - Security-first mode
4. **SPEED.md** - Maximum efficiency mode
5. **ARCHITECT.md** - System-level thinking mode

### SKILLS (20+ items)

**Reasoning:**
- think-aloud.md
- devils-advocate.md
- assumption-hunter.md
- edge-case-generator.md
- complexity-estimator.md

**Code Quality:**
- auto-polish.md
- code-reviewer.md
- security-auditor.md
- performance-profiler.md
- dependency-analyzer.md
- dead-code-hunter.md
- consistency-enforcer.md

**Communication:**
- pr-writer.md
- commit-crafter.md
- documentation-generator.md
- explanation-adapter.md
- changelog-builder.md

**Planning:**
- task-decomposer.md
- dependency-mapper.md
- spike-designer.md
- estimate-calibrator.md

**Research:**
- stay-current.md (web search verification)
- best-practices-finder.md

### AGENTS (20+ items)

**Lifecycle:**
- inception-agent
- architect-agent
- scaffolding-agent
- implementation-agent
- integration-agent
- migration-agent
- deployment-agent

**Quality:**
- test-strategist-agent
- chaos-agent
- load-tester-agent
- regression-hunter-agent
- flaky-test-detective-agent

**Operations:**
- incident-commander-agent
- postmortem-writer-agent
- capacity-planner-agent
- cost-optimizer-agent
- alert-tuner-agent

**Collaboration:**
- code-archaeologist-agent
- knowledge-transfer-agent
- meeting-prep-agent
- stakeholder-translator-agent

**Meta:**
- prompt-optimizer-agent
- agent-evaluator-agent
- context-curator-agent
- feedback-loop-agent

### TOOLS & INFRASTRUCTURE (15+ items)

**MCP Servers:**
- Context7 (documentation)
- File system
- Database
- Git
- API servers

**Hooks:**
- pre-tool-use hooks (validation, blocking)
- post-tool-use hooks (formatting, notification)

**Automation:**
- pre-commit integration
- CI/CD hooks
- quality gate scripts

### INNOVATIVE CONCEPTS (10 items)
1. Code Weather System
2. Technical Debt Portfolio
3. Code Genome Mapping
4. Cognitive Load Budget
5. AI Pair Programming Rituals
6. Failure Mode Analysis
7. Context Inheritance System
8. Code Empathy Engine
9. Semantic Versioning for Prompts
10. AI Office Hours

---

## Directory Structure

```
ai/
├── prompt-engineering/
│   ├── ULTIMATE-DIRECTORY-MASTER-PLAN.md  # This file
│   │
│   ├── philosophy/
│   │   ├── CORE.md                    # Overarching engineering philosophy
│   │   ├── PRINCIPLES.md              # DRY, SOLID, etc. with interpretations
│   │   ├── AESTHETICS.md              # Code beauty standards
│   │   ├── ANTI-PATTERNS.md           # What to never do
│   │   ├── DECISION-LOG.md            # Architectural decisions
│   │   ├── LESSONS-LEARNED.md         # Post-mortems and wisdom
│   │   ├── QUALITY-STANDARDS.md       # Detailed quality expectations
│   │   ├── AI-ENGINEERING.md          # AI-powered app standards
│   │   └── ASSUMPTIONS.md             # Explicit system assumptions
│   │
│   ├── PERSONAS/
│   │   ├── SENIOR.md                  # Expert mode
│   │   ├── TEACHER.md                 # Learning mode
│   │   ├── PARANOID.md                # Security-first mode
│   │   ├── SPEED.md                   # Efficiency mode
│   │   └── ARCHITECT.md               # System-thinking mode
│   │
│   ├── skills/
│   │   ├── reasoning/
│   │   │   ├── think-aloud.md
│   │   │   ├── devils-advocate.md
│   │   │   ├── assumption-hunter.md
│   │   │   └── edge-case-generator.md
│   │   ├── code-quality/
│   │   │   ├── auto-polish.md
│   │   │   ├── reviewer.md
│   │   │   ├── security-auditor.md
│   │   │   └── performance-profiler.md
│   │   ├── communication/
│   │   │   ├── pr-writer.md
│   │   │   ├── commit-crafter.md
│   │   │   └── documentation.md
│   │   └── planning/
│   │       ├── task-decomposer.md
│   │       └── estimator.md
│   │
│   ├── agents/
│   │   ├── lifecycle/
│   │   │   ├── inception.md
│   │   │   ├── architect.md
│   │   │   ├── implementation.md
│   │   │   └── deployment.md
│   │   ├── quality/
│   │   │   ├── test-strategist.md
│   │   │   ├── chaos.md
│   │   │   └── regression-hunter.md
│   │   ├── operations/
│   │   │   ├── incident-commander.md
│   │   │   ├── postmortem-writer.md
│   │   │   └── cost-optimizer.md
│   │   └── meta/
│   │       ├── prompt-optimizer.md
│   │       └── agent-evaluator.md
│   │
│   ├── TOOLS/
│   │   ├── mcp-servers/
│   │   │   └── (configurations)
│   │   ├── hooks/
│   │   │   ├── pre-tool-use/
│   │   │   └── post-tool-use/
│   │   └── automation/
│   │       └── (scripts)
│   │
│   ├── prompts/
│   │   ├── templates/
│   │   │   ├── code-review.md
│   │   │   ├── bug-fix.md
│   │   │   ├── feature-impl.md
│   │   │   └── refactoring.md
│   │   ├── domain-specific/
│   │   │   ├── frontend/
│   │   │   ├── backend/
│   │   │   ├── infrastructure/
│   │   │   └── data/
│   │   └── versioned/
│   │       └── (existing prompts like LeetCode Tutor)
│   │
│   ├── memory/
│   │   ├── project-context.json
│   │   ├── decisions.json
│   │   ├── preferences.json
│   │   └── learnings.json
│   │
│   ├── GUARDRAILS/
│   │   ├── security-rules.md
│   │   ├── forbidden-patterns.md
│   │   ├── quality-gates.md
│   │   └── permissions.json
│   │
│   ├── METRICS/
│   │   ├── prompt-effectiveness.md
│   │   ├── agent-performance.md
│   │   └── improvement-log.md
│   │
│   └── WORKFLOWS/
│       ├── tdd-workflow.md
│       ├── pr-workflow.md
│       ├── incident-workflow.md
│       └── onboarding-workflow.md
```

---

## Implementation Phases

### Phase 1: Core Philosophy (IMMEDIATE IMPACT)
These solve your pain points directly:
1. **CORE.md** with Polish, Big Picture, Robustness, Challenge, Partnership mandates
2. **QUALITY-STANDARDS.md** - Detailed quality expectations
3. **AI-ENGINEERING.md** - Standards for AI-powered apps

### Phase 2: Skills That Amplify
4. **stay-current.md** - Web search and verification skill
5. **devils-advocate.md** - Challenge assumptions skill
6. **auto-polish.md** - Automatic code refinement

### Phase 3: Productivity Amplifiers
7. **scaffolding/** - Templates and boilerplate generators
8. **code-reviewer.md** - Self-review before delivery
9. **pr-writer.md** / **commit-crafter.md**

### Phase 4: Advanced Agents
10. Implementation agent with built-in quality gates
11. Test strategist for comprehensive coverage
12. Refactoring agent for consistency

### Phase 5: Meta-Improvement
13. Prompt optimizer to improve the system
14. Feedback capture for continuous improvement

---

## Sources & References

### CLAUDE.md & Philosophy
- [Anthropic: Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [HumanLayer: Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Arize: CLAUDE.md Best Practices](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)
- [Apidog: 5 Best Practices for CLAUDE.md](https://apidog.com/blog/claude-md/)

### AI Coding Agents
- [Render: Testing AI Coding Agents 2025](https://render.com/blog/ai-coding-agents-benchmark)
- [Faros AI: Best AI Coding Agents 2026](https://www.faros.ai/blog/best-ai-coding-agents-2026)
- [Softcery: Agentic Coding Best Practices](https://softcery.com/lab/softcerys-guide-agentic-coding-best-practices)
- [Anthropic: Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

### MCP & Tools
- [MCP Anniversary Blog Post](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)
- [MCP Specification 2025-11](https://modelcontextprotocol.io/specification/2025-11-25)
- [Thoughtworks: MCP Impact 2025](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/model-context-protocol-mcp-impact-2025)

### Hooks & Automation
- [GitButler: Claude Code Hooks](https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks)
- [Steve Kinney: Claude Code Hook Examples](https://stevekinney.com/courses/ai-development/claude-code-hook-examples)

### Multi-Agent Systems
- [Shakudo: Top 9 AI Agent Frameworks](https://www.shakudo.io/blog/top-9-ai-agent-frameworks)
- [Google ADK Blog](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/)
- [C3 AI: Autonomous Coding Agents](https://c3.ai/blog/autonomous-coding-agents-beyond-developer-productivity/)

### Code Quality & Review
- [CodeRabbit](https://coderabbit.ai/)
- [Qodo](https://www.qodo.ai/)
- [Augment Code: Quality Gates](https://www.augmentcode.com/guides/autonomous-quality-gates-ai-powered-code-review)

### Testing
- [Awesome Testing: TDAID](https://www.awesome-testing.com/2025/10/test-driven-ai-development-tdaid)
- [Skywork: Claude Code Testing Automation](https://skywork.ai/blog/agent/claude-code-2025-testing-automation-playbook/)

### Memory & Context
- [Mem0 Research](https://mem0.ai/research)
- [Tribe AI: Context-Aware Memory](https://www.tribe.ai/applied-ai/beyond-the-bubble-how-context-aware-memory-systems-are-changing-the-game-in-2025)

### Security
- [OWASP LLM Prompt Injection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [NVIDIA: Semantic Prompt Injections](https://developer.nvidia.com/blog/securing-agentic-ai-how-semantic-prompt-injections-bypass-ai-guardrails/)

### Self-Improvement
- [IntuitionLabs: Meta-Prompting](https://intuitionlabs.ai/articles/meta-prompting-llm-self-optimization)
- [Self-Refine Paper](https://openreview.net/pdf?id=S37hOerQLB)
- [MIT Tech Review: AI Self-Improvement](https://www.technologyreview.com/2025/08/06/1121193/five-ways-that-ai-is-learning-to-improve-itself/)

### Productivity
- [GetDX: AI Measurement](https://getdx.com/blog/ai-measurement-hub/)
- [CodeCondo: Context Switching Reduction](https://codecondo.com/developers-cut-context-switching-ai-tools/)

---

## Summary

**The Ultimate Prompt Engineering Directory** - A comprehensive ecosystem:

| Category | Count | Purpose |
|----------|-------|---------|
| Philosophy Files | 9 | Define how Claude thinks and operates |
| Persona Files | 5 | Switch between operating modes |
| Skills | 20+ | Specific capabilities to invoke |
| Agents | 20+ | Autonomous task handlers |
| Tools/MCP | 15+ | External integrations and automation |
| Innovative Concepts | 10 | Novel approaches to try |

**Specifically solving your pain points:**
- Polished code on first delivery (not after 5 prompts)
- Big-picture thinking by default
- Proactive robustness without asking
- Always using web search for current info
- Challenging your assumptions constructively
- 80/20 collaboration throughout (not just planning)
- Using AskUserQuestion tool liberally for tight partnership
