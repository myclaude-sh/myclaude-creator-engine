# Product Spec: Agents

## Definition

Agents are individual agent definitions with persona, cognitive architecture, and behavioral
rules. They are used as `subagent_type` in Claude Code's Agent tool, or as standalone command
agents invoked via `@agent-name`.

An agent is NOT:
- A skill (agents have persistent persona and decision autonomy; skills are stateless routines)
- A squad (agents are single-entity; squads coordinate multiple agents)
- A prompt (agents have identity and can reason across turns; prompts are input templates)

An agent IS:
- A defined synthetic identity with consistent behavior
- A decision-making entity with explicit protocols
- A composable building block for squads and systems

---

## Canonical File Structure

```
agent-name/
├── AGENT.md              # Full agent definition (REQUIRED)
├── identity.md           # Persona, voice, personality (optional at MCS-1)
├── architecture.md       # Cognitive architecture, decision protocols
├── tools.md              # Tool access and usage patterns
└── examples/             # Example interactions
    ├── example-1.md
    └── example-2.md
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `AGENT.md` | Complete agent definition | MCS-1 |
| `README.md` | Setup, usage, integration instructions | MCS-1 |
| Tool list (in AGENT.md) | What tools the agent can use | MCS-1 |

---

## Required Sections in AGENT.md

### 1. Agent Name and Role Description

```markdown
# Agent Name

**Role:** One-sentence description of the agent's purpose
**Type:** [THINKER | HYBRID | EXECUTOR]
**Version:** 1.0.0
```

### 2. Identity and Persona

Who this agent IS — not just what it does. Includes:
- Cognitive style (analytical, creative, systematic, etc.)
- Voice and communication style
- Values and operating principles
- Inspirational models (real people or archetypes whose thinking patterns inform this agent)

A strong identity makes agent behavior predictable and consistent across contexts.

### 3. Capabilities and Limitations

What the agent CAN do (explicit scope) and CANNOT do (explicit non-scope).
Explicit limitations prevent scope creep and set correct buyer expectations.

```markdown
## Capabilities
- [Specific capability with context]
- [Another specific capability]

## Limitations
- Cannot [specific limitation — not "cannot do bad things"]
- Will not [explicit refusal condition]
- Escalates when [specific trigger]
```

### 4. Tool Access List

Which tools the agent uses and HOW it uses them. Not just listing tools — explaining
the decision logic around tool invocation.

```markdown
## Tools

| Tool | When to Use | Usage Pattern |
|------|------------|---------------|
| Read | Loading context files | Always load before responding |
| Bash | Running analysis scripts | Only when Read can't provide needed info |
| WebSearch | Verifying current information | When knowledge may be stale |
```

### 5. Decision Protocols

How the agent makes choices. This is the cognitive architecture of the agent:
- When to act vs. ask for clarification
- How to prioritize competing objectives
- How to handle ambiguity
- What counts as a successful output

### 6. Output Format and Standards

The specific format the agent produces. Include:
- Structure of outputs
- Tone and style standards
- Length guidelines
- What to include vs. exclude

### 7. Handoff Protocols

When and how this agent passes work to other agents or escalates to humans:
- Escalation triggers (when the agent cannot handle the task)
- Output format for agent-to-agent handoffs
- What context to pass on handoff

---

## MCS Requirements

### MCS-1: Publishable

**Universal:**
- [ ] Valid AGENT.md with all 7 required sections
- [ ] README.md with: what the agent does, how to invoke, requirements, tool permissions needed
- [ ] Tool list explicitly documented
- [ ] Metadata: name, description, category (agents), version, license
- [ ] No broken file references
- [ ] No syntax errors
- [ ] License from approved list
- [ ] No hardcoded secrets

**Agent-Specific:**
- [ ] Identity section establishes distinct persona (not generic "helpful assistant")
- [ ] Capabilities section has at least 3 specific capabilities
- [ ] Limitations section has at least 2 explicit non-capabilities

### MCS-2: Quality

**Universal (beyond MCS-1):**
- [ ] Architecture doc in `architecture.md`
- [ ] 3+ example interactions covering different scenarios
- [ ] Edge case handling documented
- [ ] Anti-patterns section
- [ ] Tested with 5 different user intents
- [ ] No placeholder content
- [ ] Consistent naming
- [ ] Semver versioning

**Agent-Specific:**
- [ ] `examples/` directory with 2+ real interaction examples
- [ ] `identity.md` with full persona details
- [ ] Decision protocol covers at least: act vs. ask, ambiguity handling, failure mode
- [ ] Handoff protocol documented (what agent does when it can't handle input)

### MCS-3: State-of-the-Art

**Universal (beyond MCS-2):**
- [ ] Deep domain expertise encoded in identity and architecture
- [ ] Composable with squads and systems
- [ ] Stress-tested: ambiguity, adversarial, and edge case prompts
- [ ] Cognitive architecture documented with justification
- [ ] Versioning strategy with CHANGELOG
- [ ] 5+ exemplar interactions including difficult cases
- [ ] Performance-optimized prompting
- [ ] Differentiation statement

**Agent-Specific:**
- [ ] 7-layer or equivalent cognitive architecture documented
- [ ] Agent tested as standalone AND as squad component
- [ ] Stress test results documented in `architecture.md`
- [ ] Tools.md with usage patterns and security considerations

---

## Anti-Patterns for Agents

### Structural
- **Identity-free agents:** AGENT.md defines what to do but not who the agent IS. Behavior becomes inconsistent across contexts.
- **Missing escalation protocol:** Agent has no definition of when to stop and hand off. It will attempt tasks beyond its competence.
- **Tool list without usage logic:** Listing tools without explaining when/how to use them leads to over-reliance on expensive tools.

### Content
- **Generic persona:** "I am a helpful, knowledgeable, and friendly AI assistant" — this is a non-persona. It predicts nothing.
- **Overlapping capabilities with role description:** Describing capabilities and role in the same sentence without separating what the agent IS from what it CAN DO.
- **Implicit limitations:** Not documenting what the agent won't do assumes users will figure it out. They won't.

### Quality
- **No decision protocol:** Agent has no rules for choosing between action and clarification. It either acts too fast (hallucinating assumptions) or asks too many questions.
- **Examples that only show success:** All example interactions show happy-path scenarios. Real value is in showing how the agent handles failure, ambiguity, and edge cases.

---

## Discovery Questions (from §7)

When creating an agent, answer these before scaffolding:

1. What role does this agent play? (specific job title or function, not "helper")
2. What personality or cognitive style should it have? (systematic, intuitive, adversarial, diplomatic, etc.)
3. What tools does it need access to? (and specifically which permissions)
4. What decisions can it make autonomously vs. what must it escalate?
5. How does it interact with other agents if part of a squad?
6. What does "done" look like for this agent — what counts as a successful output?
7. What are the 3 scenarios where this agent is most likely to fail? (future stress tests)

---

## DNA Requirements

For the complete DNA pattern applicability matrix for this product type,
see `product-dna/agent.yaml`. That file defines:
- Which of the 18 DNA patterns (D-01 to D-18) are required vs optional
- Validation checks per pattern (grep/glob commands)
- Template file mapping with DNA injection points
- Frontmatter fields (Anthropic Agent Skills spec)
- Discovery questions for /create

**MCS scoring:** `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
See `references/quality/mcs-spec.md` for full scoring formula.
