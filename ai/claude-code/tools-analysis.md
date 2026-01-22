# Claude Code Tooling: Skills, Commands, and Agents

A comprehensive guide to understanding and effectively using Claude Code's three core extensibility mechanisms. Written for daily driver users who leverage Claude Code for coding, learning, brainstorming, ideation, software design, and more.

---

## Quick Decision Matrix

**Which tool should I use?**

| I want to... | Use |
|--------------|-----|
| Add reusable knowledge/instructions that Claude loads automatically | **Skill** |
| Create a quick `/slash-command` for manual invocation | **Skill** or **Command** |
| Run tasks in isolated context to preserve main conversation | **Agent** (subagent) |
| Parallelize multiple independent tasks | **Agent** (subagent) |
| Share team conventions and workflows | **Skill** (in `.claude/skills/`) |
| Restrict tool access for specific workflows | **Skill** or **Agent** |
| Let Claude decide when to delegate complex work | **Agent** (subagent) |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Skills: Reusable Knowledge & Workflows](#skills-reusable-knowledge--workflows)
3. [Commands: Slash Commands](#commands-slash-commands)
4. [Agents: Specialized Task Handlers](#agents-specialized-task-handlers)
5. [Detailed Comparison Analysis](#detailed-comparison-analysis)
6. [Real-World Patterns for Daily Drivers](#real-world-patterns-for-daily-drivers)
7. [Best Practices](#best-practices)
8. [Common Pitfalls & How to Avoid Them](#common-pitfalls--how-to-avoid-them)
9. [References & Resources](#references--resources)

---

## Executive Summary

Claude Code provides three mechanisms to extend its capabilities:

### Skills
**What**: Markdown files with YAML frontmatter that teach Claude how to perform specific tasks or provide domain knowledge.

**Key characteristics**:
- Auto-discoverable: Claude loads relevant skills when your prompts match skill descriptions
- Invocable: Trigger manually with `/skill-name`
- Flexible context: Run inline or in isolated subagent (`context: fork`)
- Portable: Follow the [Agent Skills open standard](https://agentskills.io), compatible across AI tools

**Best for**: Team conventions, workflow automation, reference documentation, domain expertise.

### Commands
**What**: Slash commands that trigger specific actions or custom prompts. Now unified with Skills (legacy `.claude/commands/` still works).

**Key characteristics**:
- Manual invocation only (type `/command-name`)
- Simple prompt templates with `$ARGUMENTS` substitution
- Quick to create, lightweight

**Best for**: Simple prompt shortcuts, quick actions you trigger explicitly.

### Agents (Subagents)
**What**: Specialized AI assistants that operate in isolated context windows with custom system prompts and tool permissions.

**Key characteristics**:
- Auto-delegation: Claude routes tasks based on agent descriptions
- Isolated context: Keeps verbose output out of main conversation
- Parallel execution: Multiple agents can run simultaneously
- Independent permissions: Each agent has its own tool access

**Best for**: Complex multi-step tasks, context-heavy operations, parallel work, specialized domains.

---

## Skills: Reusable Knowledge & Workflows

### What Are Skills?

Skills are the most versatile extensibility mechanism in Claude Code. They're Markdown files with optional YAML frontmatter that:

1. **Teach Claude domain expertise** (coding standards, API conventions, security practices)
2. **Define repeatable workflows** (code review procedures, deployment steps)
3. **Provide reference documentation** (project architecture, legacy system quirks)

Skills follow the **Agent Skills open standard**, making them portable across Claude Code, Codex, Gemini CLI, and other compatible tools.

### Skill Lifecycle

```
Discovery → Claude loads skill descriptions into context
     ↓
Matching → Your prompt matches a skill's description
     ↓
Loading → Full skill content loads into Claude's context
     ↓
Execution → Claude follows skill instructions
     ↓
Results → Output returns to conversation (or summary if forked)
```

### Creating Skills

#### Location Options

```
~/.claude/skills/<name>/SKILL.md      # Personal (all projects)
.claude/skills/<name>/SKILL.md        # Project (version-controlled)
<plugin>/skills/<name>/SKILL.md       # Plugin (distributed)
```

Project skills override personal skills with the same name.

#### Basic Structure

```yaml
---
name: my-skill
description: What this skill does and when Claude should use it
---

Your instructions in Markdown...
```

#### Complete Configuration Reference

```yaml
---
# Required fields
name: code-reviewer              # Becomes /code-reviewer command

# Highly recommended
description: Reviews code for security issues, performance, and best practices

# Invocation control
disable-model-invocation: false  # true = manual only, Claude won't auto-invoke
user-invocable: true             # false = hidden from / menu, Claude-only

# Tool restrictions
allowed-tools: Read, Grep, Glob  # Comma-separated list of permitted tools

# Execution context
context: default                 # 'fork' runs in isolated subagent
agent: Explore                   # Subagent type when context: fork
model: sonnet                    # Override model: haiku, sonnet, opus, inherit

# Arguments hint
argument-hint: [file] [options]  # Shown in autocomplete

# Lifecycle hooks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
---
```

#### Supporting Files

Organize complex skills with multiple files:

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── reference.md       # Detailed documentation
├── examples.md        # Usage examples
├── templates/         # Templates Claude fills in
│   └── component.tsx
└── scripts/           # Executable scripts
    └── validate.sh
```

Reference them from SKILL.md:
```markdown
For complete API reference, see [reference.md](reference.md)
```

### Skill Invocation Patterns

#### Automatic Invocation (Default)
Claude loads skills when your prompt matches the description:
```
You: "review this code for security issues"
→ Claude loads code-reviewer skill (matches "security" in description)
```

#### Manual Invocation
Always available via slash command:
```
/code-reviewer src/auth.ts
```

#### Controlling Invocation

| Setting | You Invoke | Claude Invokes | In `/` Menu |
|---------|-----------|----------------|-------------|
| Default | Yes | Yes | Yes |
| `disable-model-invocation: true` | Yes | No | Yes |
| `user-invocable: false` | No | Yes | No |
| Both true/false | No | No | No |

**Use `disable-model-invocation: true`** for actions with side effects (deploy, commit, send-email).

**Use `user-invocable: false`** for background knowledge that isn't a meaningful command.

### Dynamic Context Injection

Skills can execute shell commands before Claude sees them:

```yaml
---
name: pr-context
description: Analyze current pull request
---

## Current PR Context
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

Analyze this PR and suggest improvements.
```

The `!`command`` syntax executes immediately, replacing the placeholder with actual output.

### The `context: fork` Pattern

Run skills in isolated subagent context:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

Research $ARGUMENTS thoroughly:
1. Find all relevant files
2. Analyze code patterns
3. Return a concise summary
```

**Benefits**:
- Verbose exploration stays out of main context
- Uses specialized agent (Explore = read-only, fast)
- Only summary returns to main conversation

**Trade-offs**:
- No conversation history in subagent
- Slightly higher latency
- Task must be self-contained

### Extended Thinking in Skills

Include "ultrathink" anywhere in skill content to enable extended thinking:

```yaml
---
name: architecture-analysis
---

# Architecture Analysis (ultrathink enabled)

Deeply analyze the system architecture...
```

---

## Commands: Slash Commands

### Understanding Commands in 2025+

The distinction between "commands" and "skills" has largely merged. The official documentation now refers to everything as **Skills**, but the legacy `.claude/commands/` directory still works.

**Key insight**: If you're starting fresh, use Skills. They provide all command functionality plus additional features.

### Built-in Commands

Claude Code provides ~25 built-in commands. Type `/` to see the full list:

| Command | Purpose |
|---------|---------|
| `/help` | Usage help |
| `/clear` | Clear conversation history |
| `/compact [focus]` | Compress conversation, optionally focusing on specific topics |
| `/cost` | Show token usage statistics |
| `/context` | Visualize context usage |
| `/doctor` | Check installation health |
| `/export [file]` | Export conversation |
| `/init` | Initialize CLAUDE.md |
| `/mcp` | Manage MCP servers |
| `/memory` | Edit CLAUDE.md files |
| `/model` | Change AI model |
| `/permissions` | View/update permissions |
| `/plan` | Enter plan mode |
| `/resume [session]` | Resume previous conversation |
| `/rewind` | Undo conversation/code changes |
| `/stats` | Usage analytics |
| `/tasks` | Manage background tasks |
| `/theme` | Change color theme |

### Creating Custom Commands (Legacy Method)

If you have existing commands in `.claude/commands/`, they continue to work:

```
.claude/commands/fix-issue.md:

Please analyze and fix GitHub issue: $ARGUMENTS

1. Use 'gh issue view' to get details
2. Search codebase for relevant files
3. Implement the fix
4. Run tests
5. Create descriptive commit
```

Invoke with `/fix-issue 123`.

### Migration: Commands → Skills

To convert a command to a skill:

**Before** (`.claude/commands/review.md`):
```markdown
Review the code in $ARGUMENTS for:
- Security issues
- Performance problems
- Best practices
```

**After** (`.claude/skills/review/SKILL.md`):
```yaml
---
name: review
description: Review code for security, performance, and best practices
allowed-tools: Read, Grep, Glob
---

Review the code in $ARGUMENTS for:
- Security issues
- Performance problems
- Best practices
```

**What you gain**:
- Auto-invocation when description matches
- Tool restrictions
- Supporting files organization
- `context: fork` option
- Model override capability

---

## Agents: Specialized Task Handlers

### What Are Agents (Subagents)?

Agents are specialized AI assistants that:

1. **Run in isolated context windows** - their verbose output stays separate from your main conversation
2. **Have custom system prompts** - tailored instructions for specific domains
3. **Control their own tools** - can restrict or expand tool access
4. **Execute independently** - work autonomously and return results

Claude automatically delegates tasks to agents based on their descriptions.

### Built-in Agents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| **Explore** | Haiku | Read, Grep, Glob | Fast read-only codebase exploration |
| **Plan** | Inherit | Read, Grep, Glob | Research for planning mode |
| **General-purpose** | Inherit | All | Complex multi-step tasks |
| **Bash** | Inherit | Bash | Terminal command execution |

### Creating Custom Agents

#### Method 1: Interactive (`/agents` command)

```
/agents
→ Select "Create new agent"
→ Choose scope (user or project)
→ Generate with Claude or create manually
→ Configure tools, model, permissions
→ Save
```

#### Method 2: File-based

Create `.claude/agents/agent-name.md`:

```yaml
---
name: code-reviewer
description: Reviews code for quality, security, and best practices. Use after code changes.
tools: Read, Grep, Glob
model: sonnet
permissionMode: default
---

You are a senior code reviewer specializing in:
- Security vulnerability detection
- Performance optimization
- Code clarity and maintainability
- Test coverage assessment

When reviewing code:
1. Identify issues by severity (Critical, High, Medium, Low)
2. Provide specific file and line references
3. Suggest concrete improvements with examples
```

### Agent Configuration Reference

```yaml
---
name: security-auditor           # Unique identifier
description: When Claude should delegate to this agent
tools: Read, Grep, Glob, Bash    # Allowed tools (inherits all if omitted)
disallowedTools: Write, Edit     # Explicitly denied tools
model: opus                      # haiku, sonnet, opus, inherit
permissionMode: default          # default, acceptEdits, dontAsk, bypassPermissions, plan
skills:                          # Preload skills into agent context
  - security-guidelines
  - owasp-patterns
hooks:                           # Lifecycle hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
---
```

### Permission Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `default` | Standard permission prompts | Interactive work |
| `acceptEdits` | Auto-approve file edits | Trusted development |
| `dontAsk` | Auto-deny unapproved tools | Restricted workflows |
| `bypassPermissions` | Skip all checks | Fully autonomous (use carefully) |
| `plan` | Read-only exploration | Planning phases |

### Why Use Agents?

#### 1. Context Management
Operations producing large output (tests, logs, exploration) stay in agent context:

```
Main conversation: "Run all tests and fix failures"
→ Test output (1000s of lines) stays in agent
→ Only "Fixed 3 failing tests in auth module" returns to main
```

#### 2. Parallel Execution
Multiple agents can work simultaneously:

```
You: "Research the auth, database, and API modules in parallel"
→ Claude spawns 3 Explore agents concurrently
→ Each returns a summary
→ You get results faster without sequential waiting
```

#### 3. Specialized Expertise
Each agent can have domain-specific instructions:

```yaml
---
name: database-expert
description: Database schema design and query optimization
tools: Bash, Read
---

You are a database specialist. Focus on:
- Schema normalization
- Index optimization
- Query performance
- Migration safety
```

#### 4. Tool Restrictions
Agents can have limited tool access for safety:

```yaml
---
name: safe-auditor
tools: Read, Grep, Glob  # No Write, Edit, or Bash
---

Analyze code but never modify anything.
```

### Agent Limitations

1. **Agents cannot spawn agents** - No nested delegation. Chain from main conversation instead.

2. **Fresh context each invocation** - No conversation history unless you resume with agent ID.

3. **Background agents have restrictions**:
   - Cannot prompt for user input
   - Auto-deny unapproved permissions
   - No MCP tool access

4. **Token usage multiplies** - Each agent uses its own context window. Parallel agents = parallel costs.

---

## Detailed Comparison Analysis

### Feature Comparison Table

| Aspect | Skills | Commands | Agents |
|--------|--------|----------|--------|
| **Primary purpose** | Knowledge + workflows | Quick actions | Task delegation |
| **Invocation** | Auto + manual (`/name`) | Manual only (`/name`) | Auto-delegation |
| **Context** | Inline or forked | Inline | Always isolated |
| **Conversation history** | Yes (inline) / No (fork) | Yes | No |
| **Parallel execution** | Via `context: fork` | No | Yes |
| **Tool restrictions** | `allowed-tools` field | Inherits all | `tools` field |
| **Model override** | Yes | No | Yes |
| **File location** | `.claude/skills/` | `.claude/commands/` | `.claude/agents/` |
| **Supporting files** | Yes | No | Yes (via skills preload) |
| **Auto-discovery** | Yes (by description) | No | Yes (by description) |
| **Version controllable** | Yes | Yes | Yes |
| **Standard compliance** | Agent Skills standard | Claude Code only | Claude Code + SDK |

### Decision Flowchart

```
START: I need to extend Claude Code
  │
  ├─ Is this reusable knowledge or team conventions?
  │   └─ YES → SKILL (possibly user-invocable: false)
  │
  ├─ Is this a simple prompt I want as a shortcut?
  │   └─ YES → SKILL (with disable-model-invocation: true)
  │
  ├─ Does this task produce lots of verbose output?
  │   └─ YES → AGENT or SKILL with context: fork
  │
  ├─ Do I need parallel execution?
  │   └─ YES → AGENT (multiple can run simultaneously)
  │
  ├─ Should Claude auto-invoke based on context?
  │   ├─ YES, for knowledge → SKILL
  │   └─ YES, for complex tasks → AGENT
  │
  ├─ Do I need strict tool restrictions?
  │   └─ YES → SKILL (allowed-tools) or AGENT (tools)
  │
  └─ None of the above?
      └─ Default to SKILL (most flexible)
```

### When Each Shines

#### Skills Excel At:
- Team coding standards and conventions
- API usage patterns and documentation
- Workflow templates (PR reviews, deployments)
- Reference material Claude needs in-context
- Cross-project portable expertise

#### Commands Excel At:
- Simple prompt shortcuts (legacy use)
- Quick one-off actions
- Compatibility with existing `.claude/commands/` setups

#### Agents Excel At:
- Running tests and analyzing failures
- Large codebase exploration
- Parallel research tasks
- Log analysis and debugging sessions
- Tasks requiring specialized tool sets

### The Spectrum of Isolation

```
LEAST ISOLATED                              MOST ISOLATED
      │                                            │
      ▼                                            ▼
   Skill          Skill              Skill       Agent
  (inline)    (inline +          (context:      (always
              auto-invoke)         fork)        isolated)
      │             │                │             │
   Shares       Shares            Isolated      Isolated
   full         full              context,      context,
   context      context           returns       returns
                                  summary       summary
```

---

## Real-World Patterns for Daily Drivers

### Pattern 1: The Knowledge Base Approach

**Use case**: You want Claude to always know your project conventions.

**Implementation**: Create non-invocable skills that auto-load:

```yaml
# .claude/skills/conventions/SKILL.md
---
name: project-conventions
description: Coding standards and patterns for this project
user-invocable: false
---

## Our Coding Standards

- TypeScript strict mode always
- Use functional components with hooks
- Error handling: wrap async in try-catch, use Result types
- Testing: Jest + React Testing Library
- Naming: camelCase variables, PascalCase components
```

Claude sees this context automatically without cluttering your `/` menu.

### Pattern 2: The Deployment Pipeline

**Use case**: You want controlled deployment steps that only run when explicitly triggered.

**Implementation**: Manual-only skill with tool restrictions:

```yaml
# .claude/skills/deploy/SKILL.md
---
name: deploy
description: Deploy to production environment
disable-model-invocation: true
argument-hint: [environment]
allowed-tools: Bash, Read
---

Deploy $ARGUMENTS:

1. **Verify branch**: Must be on main
   ```bash
   git rev-parse --abbrev-ref HEAD
   ```

2. **Run tests**: All must pass
   ```bash
   npm test
   ```

3. **Build**: Create production build
   ```bash
   npm run build
   ```

4. **Deploy**: Push to environment
   ```bash
   ./scripts/deploy.sh $ARGUMENTS
   ```

5. **Verify**: Check health endpoint
   ```bash
   curl https://$ARGUMENTS.myapp.com/health
   ```
```

Only `/deploy staging` or `/deploy production` triggers this - Claude won't auto-deploy.

### Pattern 3: The Research Deep Dive

**Use case**: You want thorough research without cluttering your main conversation.

**Implementation**: Forked skill with Explore agent:

```yaml
# .claude/skills/research/SKILL.md
---
name: deep-research
description: Research a topic thoroughly in the codebase
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

Research $ARGUMENTS thoroughly:

1. **Find files**: Use Glob to locate all relevant files
2. **Search patterns**: Use Grep to find usage and definitions
3. **Read and analyze**: Understand the code structure
4. **Map dependencies**: How do components interact?

Return ONLY a concise summary with:
- Key files involved (with paths)
- Main patterns discovered
- Potential issues or improvements
- Questions for follow-up
```

Invoke with: `/deep-research authentication flow`

All verbose exploration stays in the subagent. You get a clean summary.

### Pattern 4: The Parallel Investigation

**Use case**: You need to investigate multiple areas simultaneously.

**Implementation**: Custom agent for parallel work:

```yaml
# .claude/agents/investigator.md
---
name: investigator
description: Investigate a specific module or area of the codebase
tools: Read, Grep, Glob
model: haiku
---

You are a focused investigator. Your task:

1. Thoroughly explore the assigned area
2. Document key findings with file references
3. Note any issues or concerns
4. Return a structured summary

Be concise but complete.
```

Usage in conversation:
```
You: "Investigate the auth, payment, and notification modules in parallel"

Claude: [Spawns 3 investigator agents simultaneously]
        [Each returns summary independently]
        [Claude synthesizes findings]
```

### Pattern 5: The Code Review Pipeline

**Use case**: Every code change should be reviewed systematically.

**Implementation**: Auto-invoke skill for reviews:

```yaml
# .claude/skills/review/SKILL.md
---
name: code-review
description: Review code changes for security, performance, and best practices. Use after any code modification.
allowed-tools: Read, Grep, Glob
---

## Code Review Checklist

### Security
- [ ] No hardcoded credentials or secrets
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] XSS prevention in frontend code

### Performance
- [ ] No N+1 query patterns
- [ ] Efficient data structures
- [ ] Proper caching considered

### Quality
- [ ] Clear naming and documentation
- [ ] Error handling present
- [ ] Tests added or updated

Provide specific file:line references for all findings.
Categorize by severity: Critical, Warning, Suggestion.
```

Claude auto-invokes this after you ask it to write code, giving you immediate feedback.

### Pattern 6: The Learning Companion

**Use case**: You're using Claude Code to learn a new codebase or technology.

**Implementation**: Combination approach:

```yaml
# .claude/skills/explain/SKILL.md
---
name: explain-code
description: Explain code in detail with examples and analogies
---

Explain $ARGUMENTS:

1. **High-level overview**: What does it do?
2. **Step-by-step walkthrough**: How does it work?
3. **Key concepts**: What patterns/techniques are used?
4. **Analogies**: Relate to familiar concepts
5. **Examples**: Show simplified versions
6. **Questions to explore**: What should I investigate next?

Adjust complexity to my apparent skill level.
```

```yaml
# .claude/agents/mentor.md
---
name: mentor
description: Technical mentor for learning and understanding code
tools: Read, Grep, Glob, WebSearch
model: opus
---

You are a patient technical mentor. When explaining:

- Start with the "why" before the "how"
- Use analogies to familiar concepts
- Provide progressively complex examples
- Ask Socratic questions to check understanding
- Suggest related topics to explore

Never make the learner feel bad for not knowing something.
```

### Pattern 7: The Daily Driver Context Manager

**Use case**: Managing context across long coding sessions.

**Implementation**: `/catchup` skill for context restoration:

```yaml
# .claude/skills/catchup/SKILL.md
---
name: catchup
description: Restore context from uncommitted changes
disable-model-invocation: true
---

## Catchup Context

!`git status --short`

## Recent Changes
!`git diff --stat`

## Uncommitted Diff
!`git diff`

## Recent Commits
!`git log --oneline -10`

---

Based on the above, understand:
1. What work is in progress
2. What was recently completed
3. What might need attention

Summarize the current state briefly.
```

Usage: After `/clear` (when context gets full), run `/catchup` to reload work-in-progress context.

---

## Best Practices

### From Official Documentation

1. **Start with evaluation**: Run agents on representative tasks, observe where they struggle, then build skills to address gaps.

2. **Structure for scale**: When SKILL.md exceeds ~500 lines, split into separate files. Keep mutually exclusive content in separate paths to reduce token usage.

3. **Code as documentation**: Scripts can be both executable tools and reference documentation. Clarify whether Claude should run or read them.

4. **Limit tool access**: Principle of least privilege. Give agents/skills only the tools they need.

5. **Check into version control**: Share project skills/agents with your team via `.claude/skills/` and `.claude/agents/`.

### From Community Experience

1. **Use subagents for context management** ([Source](https://shipyard.build/blog/claude-code-subagents-guide/)): Isolate verbose operations (test runs, log analysis) in subagents. Only summaries return to main context.

2. **Parallel agents for research** ([Source](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)): When investigating multiple areas, spawn parallel agents. Faster results, though higher token usage.

3. **Use cheaper models for read-only tasks** ([Source](https://www.anthropic.com/engineering/claude-code-best-practices)): Haiku for exploration/search, Sonnet for balanced work, Opus for complex reasoning.

4. **Don't over-architect with custom subagents** ([Source](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)): Sometimes it's better to give main Claude the context (in CLAUDE.md) and let it use built-in Task/Explore. Custom subagents can gatekeep context from the main agent.

5. **Use "think" keywords for extended reasoning** ([Source](https://www.anthropic.com/engineering/claude-code-best-practices)): "think" < "think hard" < "think harder" < "ultrathink" for increasing thinking budgets.

6. **Be explicit about when to use agents** ([Source](https://www.builder.io/blog/claude-code)): Write clear descriptions. Vague descriptions like "helps with code" won't trigger auto-delegation reliably.

7. **Chain agents, don't nest** ([Source](https://code.claude.com/docs/en/sub-agents)): Since agents can't spawn agents, design workflows that chain from main conversation:
   ```
   Main → Agent A → Results → Main → Agent B → Results
   ```

### For Daily Driver Users

1. **Create a `/catchup` skill**: After `/clear`, reload uncommitted changes and recent context.

2. **Use skills for learning**: Create explanation-focused skills that teach as they assist.

3. **Keep deployment manual**: Use `disable-model-invocation: true` for any skill that could cause production issues.

4. **Build incrementally**: Start with one skill for your most common pain point. Add more as patterns emerge.

5. **Share with your team**: Put skills/agents in `.claude/skills/` and `.claude/agents/` and commit to git. Everyone benefits.

---

## Common Pitfalls & How to Avoid Them

### Pitfall 1: Agent Not Delegating

**Symptom**: Claude does work directly instead of using your agent.

**Causes & Fixes**:
- Ensure `Task` tool is in allowed tools list
- Make description specific: "Expert security reviewer for vulnerabilities" not "Reviews code"
- Explicitly request: "Use the code-reviewer agent to..."

### Pitfall 2: Skill Loading Too Often

**Symptom**: Claude loads irrelevant skills, cluttering context.

**Fixes**:
- Make descriptions more specific and narrow
- Add `disable-model-invocation: true` if manual-only
- Reduce overlap in skill descriptions

### Pitfall 3: Context Overflow

**Symptom**: Main conversation runs out of context.

**Fixes**:
- Use `context: fork` for verbose skills
- Delegate exploration to Explore agent
- Run `/clear` then `/catchup` to reset
- Use `/compact` with focus instructions

### Pitfall 4: Parallel Agents Eating Usage

**Symptom**: Hit rate limits quickly when using parallel agents.

**Fixes**:
- Use Haiku for read-only tasks (cheaper)
- Limit parallelism to 2-3 agents
- Consider if parallel is actually faster for your use case

### Pitfall 5: Secrets in Skills/Agents

**Symptom**: Credentials exposed in version control.

**Fixes**:
- Use environment variables: `$JIRA_TOKEN` not actual tokens
- Source from shell config: `source ~/.zshrc`
- Add credential files to `.gitignore`

### Pitfall 6: Skill/Agent Files Not Loading

**Symptom**: New skill/agent doesn't appear after creation.

**Fixes**:
- Skills load at session start - restart Claude Code session
- Use `/agents` command to reload agents
- Check file location and naming (lowercase, hyphens only)

### Pitfall 7: Subagent Losing Context

**Symptom**: Agent doesn't know about previous conversation.

**Explanation**: This is by design. Subagents start fresh.

**Fixes**:
- Include necessary context in the delegation prompt
- Use `resume` parameter to continue previous agent work
- Preload skills with context the agent needs

### Pitfall 8: Over-Engineering with Custom Agents

**Symptom**: Rigid workflows that don't adapt well.

**Alternative approach** ([Source](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)):
> "Give your main agent the context (in CLAUDE.md) and let it use its own Task/Explore feature to manage delegation."

Sometimes CLAUDE.md + built-in agents is simpler than custom subagents.

---

## References & Resources

### Official Documentation
- [Skills Documentation](https://code.claude.com/docs/en/skills)
- [Subagents Documentation](https://code.claude.com/docs/en/sub-agents)
- [Slash Commands](https://code.claude.com/docs/en/slash-commands)
- [Agent Skills Standard](https://agentskills.io)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

### Community Resources
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code) - Curated collection of skills, hooks, commands
- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills) - Collection of Claude Skills
- [Awesome Claude Code Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) - 100+ specialized subagents
- [Claude Command Suite](https://github.com/qdhenry/Claude-Command-Suite) - 148+ slash commands and workflows

### Blog Posts & Tutorials
- [Skills Explained: How Skills Compares to Prompts, Projects, MCP, and Subagents](https://claude.com/blog/skills-explained)
- [Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Understanding Claude Code: Skills vs Commands vs Subagents vs Plugins](https://www.youngleaders.tech/p/claude-skills-commands-subagents-plugins)
- [When to Use Claude Code Skills vs Commands vs Agents](https://danielmiessler.com/blog/when-to-use-skills-vs-commands-vs-agents)
- [How I Use Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)
- [Claude Code Subagents Quickstart](https://shipyard.build/blog/claude-code-subagents-guide/)
- [Best Practices for Claude Code Subagents](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- [How to Use Claude Code Subagents to Parallelize Development](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/)
- [Claude Code Custom Commands: 3 Practical Examples](https://www.aiengineering.report/p/claude-code-custom-commands-3-practical)
- [How I Use Claude Code + Best Tips](https://www.builder.io/blog/claude-code)

### Deep Dives
- [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
- [Claude Code Customization Guide](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/)
- [A Guide to Claude Code 2.0](https://sankalp.bearblog.dev/my-experience-with-claude-code-20-and-how-to-get-better-at-using-coding-agents/)

---

## Summary: Your Daily Driver Toolkit

| Need | Solution | Quick Setup |
|------|----------|-------------|
| Team conventions | Skill (`user-invocable: false`) | `.claude/skills/conventions/SKILL.md` |
| Deployment | Skill (`disable-model-invocation: true`) | `.claude/skills/deploy/SKILL.md` |
| Deep research | Skill (`context: fork`) | `.claude/skills/research/SKILL.md` |
| Parallel investigation | Agent | `.claude/agents/investigator.md` |
| Code review | Skill (auto-invoke) | `.claude/skills/review/SKILL.md` |
| Context recovery | Skill (manual) | `.claude/skills/catchup/SKILL.md` |
| Learning | Agent + Skills | `.claude/agents/mentor.md` |

**Start simple**: Create one skill for your biggest daily pain point. Add more as you identify patterns.

**Share with team**: Commit `.claude/skills/` and `.claude/agents/` to version control.

**Iterate**: Skills and agents are just Markdown files. Refine them as you learn what works.
