# Decisions Log

> **Purpose:** Track architectural and approach decisions with rationale
> **Usage:** Reference for consistency across sessions

---

## Session: 2026-01-09

### Decision 1: Language-Agnostic Philosophy
**Context:** User works primarily with C# but wanted flexibility
**Decision:** Keep all philosophy and skills language-agnostic
**Rationale:** Good engineering principles transcend specific tech stacks
**Implications:** Philosophy files don't reference specific languages; skills can be specialized if needed

---

### Decision 2: 80/20 Collaboration Model
**Context:** User felt typical AI interactions are 95/5 (execution vs collaboration)
**Decision:** Target 80% execution, 20% collaboration throughout
**Rationale:** User wants tight partnership, not just task execution
**Implications:** More check-ins, more questions, more proactive suggestions

---

### Decision 3: Pain Points Drive Priority
**Context:** Comprehensive list of possible files to create
**Decision:** Order implementation phases by pain point resolution impact
**Rationale:** Solve real problems first, not theoretical completeness
**Implications:** Phase 1 = CORE.md (solves 80% of pain points)

---

### Decision 4: Directory Location
**Context:** Where to put prompt engineering files
**Decision:** Keep in `ai/prompt-engineering/` structure
**Rationale:** User already has this directory; maintains consistency
**Implications:** All new files go under this path

---

### Decision 5: Context Relay Agent
**Context:** Chat context windows get corrupted with compacting
**Decision:** Create agent that writes to files and generates handoff prompts
**Rationale:** Files persist beyond chat sessions; structured handoff ensures continuity
**Implications:** SESSION-STATE.md, MEMORY files, HANDOFF-PROMPT.md system

---

### Decision 6: Single CORE.md Philosophy
**Context:** Could have many separate philosophy files
**Decision:** Start with one comprehensive CORE.md containing all mandates
**Rationale:** Simpler to adopt; can split later if too large
**Implications:** Phase 1 creates one powerful file, not many small ones

---

### Decision 7: Ready-to-Use Blocks
**Context:** How to present philosophy content
**Decision:** Include copy-paste ready markdown blocks in master plan
**Rationale:** User can immediately use content without additional formatting
**Implications:** Master plan contains actual prompt content, not just descriptions

---

## Pending Decisions

### To Decide in Future Sessions:
- [ ] Exact content/structure of philosophy/CORE.md
- [ ] Whether to use Claude Code hooks or just prompts
- [ ] MCP server configurations to use
- [ ] How to version/evolve prompts over time
