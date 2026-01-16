# Audience Adapter Skill

> **Purpose:** Adjust content depth, terminology, and approach based on target audience. The same topic requires different treatment for beginners vs. experts.

---

## When to Use

- Starting a new piece (to calibrate)
- Content feels wrong for audience
- Feedback suggests mismatch
- Repurposing content for different audience

---

## Audience Profiles

### Beginner

**Characteristics:**
- New to the topic
- Unfamiliar with terminology
- Needs motivation and context
- May be intimidated
- Wants quick wins

**Content Approach:**
| Aspect | Approach |
|--------|----------|
| Terminology | Define everything; avoid jargon |
| Depth | Surface level; concepts over details |
| Examples | Simple, relatable, everyday analogies |
| Pace | Slower; more explanation per concept |
| Motivation | Heavy; "why should I care" constantly |
| Assumptions | Almost none |

**Typical Structure:**
1. Why this matters (motivation)
2. Core concept (simplified)
3. Simple example
4. Try it yourself (guided)
5. What you learned
6. Next steps (clear path forward)

### Intermediate

**Characteristics:**
- Knows basics
- Has some experience
- Ready for depth
- Wants practical application
- May have knowledge gaps

**Content Approach:**
| Aspect | Approach |
|--------|----------|
| Terminology | Define advanced terms only |
| Depth | Moderate; balance theory and practice |
| Examples | Realistic scenarios; some complexity |
| Pace | Normal; can move through basics quickly |
| Motivation | Moderate; focus on skill improvement |
| Assumptions | Basic knowledge of fundamentals |

**Typical Structure:**
1. Brief context (not motivation)
2. Concept with nuance
3. Practical example
4. Common pitfalls
5. Advanced considerations
6. Further exploration

### Advanced/Expert

**Characteristics:**
- Deep existing knowledge
- Wants specifics and edge cases
- Time-sensitive (values brevity)
- Seeking efficiency gains
- May challenge content

**Content Approach:**
| Aspect | Approach |
|--------|----------|
| Terminology | Use freely; no basic definitions |
| Depth | Deep; edge cases, trade-offs, nuance |
| Examples | Complex real-world scenarios |
| Pace | Fast; skip fundamentals |
| Motivation | Minimal; they already care |
| Assumptions | Strong foundation |

**Typical Structure:**
1. TL;DR / Quick reference
2. Deep dive into specifics
3. Edge cases and gotchas
4. Performance/trade-off analysis
5. When NOT to use this
6. Alternative approaches

---

## Adaptation Techniques

### Vocabulary Scaling

| Concept | Beginner | Intermediate | Advanced |
|---------|----------|--------------|----------|
| Container | "A container is like a lightweight virtual machine that packages your app with everything it needs to run" | "Containers isolate processes using namespaces and cgroups" | "cgroups v2 memory controller with PSI metrics" |
| Deployment | "Putting your code on a server where users can access it" | "Release process from staging to production" | "Blue-green with canary analysis and automatic rollback thresholds" |

### Explanation Depth

**Same concept, three levels:**

**Beginner:**
> "Docker creates containers. Think of a container as a box that holds your app and everything it needs. When you move the box to another computer, everything inside still works."

**Intermediate:**
> "Docker containers use Linux namespaces for isolation and cgroups for resource limiting. Each container shares the host kernel but has its own filesystem, network, and process tree."

**Advanced:**
> "Containers leverage the kernel's namespace isolation (pid, net, mnt, uts, ipc, user, cgroup) and control groups for resource quotas. Consider the security implications of shared kernel space and the performance overhead of overlay filesystems in write-heavy workloads."

### Example Complexity

**Beginner Example:**
```bash
# Run a container
docker run hello-world
```

**Intermediate Example:**
```bash
# Run nginx with custom config and port mapping
docker run -d \
  --name my-nginx \
  -p 8080:80 \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  nginx:alpine
```

**Advanced Example:**
```bash
# Production nginx with resource limits, health checks, and logging
docker run -d \
  --name nginx-prod \
  --memory=512m --memory-swap=512m \
  --cpus=1.5 \
  --health-cmd="curl -f http://localhost/ || exit 1" \
  --health-interval=30s \
  --log-driver=json-file --log-opt max-size=10m \
  -p 80:80 -p 443:443 \
  -v /etc/nginx:/etc/nginx:ro \
  -v /var/log/nginx:/var/log/nginx \
  nginx:alpine
```

---

## Quick Adaptation Checklist

### Before Writing

- [ ] Identified specific audience segment
- [ ] Listed what they already know
- [ ] Listed what they need to learn
- [ ] Chosen appropriate vocabulary level
- [ ] Planned example complexity
- [ ] Set appropriate pace

### During Writing

- [ ] Terminology matches audience
- [ ] Not over-explaining for experts
- [ ] Not under-explaining for beginners
- [ ] Examples are relevant to their use cases
- [ ] Assumed knowledge is accurate

### After Writing

- [ ] Would target reader find value?
- [ ] Would they understand first read?
- [ ] Would they be bored/lost anywhere?

---

## Common Mistakes

### Writing for Beginners
❌ Skipping "why" and jumping to "how"
❌ Using jargon without definition
❌ Assuming they'll figure it out
❌ Too fast pace

### Writing for Intermediates
❌ Re-explaining basics they know
❌ Being too basic (wastes time)
❌ Being too advanced (creates gaps)
❌ Forgetting practical application

### Writing for Advanced
❌ Spending time on motivation
❌ Explaining fundamentals
❌ Simple examples that don't reflect reality
❌ Missing the nuance they came for

---

## Audience Signals

### Beginner Indicators
- "Getting started with..."
- "Introduction to..."
- "What is X?"
- "How do I begin?"

### Intermediate Indicators
- "Best practices for..."
- "How to optimize..."
- "Common mistakes in..."
- "Improving your..."

### Advanced Indicators
- "Deep dive into..."
- "Advanced techniques..."
- "Performance tuning..."
- "Architecture of..."

---

## Integration

This skill can be called by:
- `context-gatherer` agent (audience profiling)
- `draft-writer` agent (calibration)
- `line-editor` agent (verification)

Reference:
- `../templates/context-document.md` (audience section)
