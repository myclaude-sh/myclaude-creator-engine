# Product Spec: Squads

## Definition

Squads are multi-agent teams with coordinated workflows, routing, and inter-agent
communication. A squad is greater than the sum of its agents — the value is in the
orchestration, not just the individual components.

A squad is NOT:
- A single agent with multiple modes
- A workflow (workflows are step sequences; squads are agent coordination)
- A system (systems combine multiple product types including squads; a squad is one component)

A squad IS:
- A team of 2+ agents with defined roles and routing
- An orchestration layer that decides which agent handles which input
- A higher-level product that buyers install as a unit

---

## Canonical File Structure

```
squad-name/
├── SQUAD.md              # Orchestration definition (REQUIRED)
├── README.md             # Setup, usage, installation (REQUIRED)
├── agents/               # Individual agent definitions (REQUIRED 2+)
│   ├── agent-1.md
│   ├── agent-2.md
│   └── agent-n.md
├── config/
│   ├── routing-table.md  # Which agent handles what (REQUIRED)
│   ├── handoff-protocol.md
│   └── capability-index.yaml
├── workflows/            # Multi-agent workflows
│   └── workflow-name.md
└── examples/             # End-to-end squad examples
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `SQUAD.md` | Orchestration definition | MCS-1 |
| `README.md` | Setup and usage documentation | MCS-1 |
| `agents/agent-1.md` + `agents/agent-2.md` | At least 2 agent definitions | MCS-1 |
| `config/routing-table.md` | Which agent handles which input | MCS-1 |

---

## Required Sections in SQUAD.md

### 1. Squad Name, Purpose, and Composition

```markdown
# Squad Name

**Purpose:** One sentence describing what this squad achieves together
**Composition:** N agents (list names and roles)
**Entry Point:** How a user invokes the squad
```

### 2. Agent Roster with Roles

A table or list of every agent in the squad:
- Agent name (matching file in `agents/`)
- Role (what problem they own)
- Trigger conditions (when this agent handles the work)
- Handoff outputs (what they pass to the next agent)

### 3. Routing Logic

The decision tree for which agent handles which input type. This is the cognitive
core of the squad — without explicit routing, the squad becomes a random selector.

```markdown
## Routing Logic

IF input contains [condition] → route to [agent-name]
IF input is [type] AND [condition] → route to [agent-name]
ELSE → [default agent or escalation]
```

### 4. Handoff Protocols

How agents communicate and pass context between each other:
- What format does one agent's output need to be in for the next to consume it?
- What context is required vs. optional on handoff?
- What happens when an agent cannot produce the expected handoff format?

### 5. Workflow Definitions

Multi-step sequences that involve multiple agents:
- Trigger conditions for the workflow
- Step sequence with which agent executes each step
- Dependencies between steps
- Completion criteria

### 6. Quality Gates Per Workflow

Each workflow must define what "done" means and how to verify it:
- Acceptance criteria for workflow output
- Who or what verifies quality (human checkpoint, agent review, automated check)

### 7. Escalation Rules

When the squad as a whole cannot handle the task:
- What conditions trigger escalation
- What information to surface to the human
- How to preserve work-in-progress state for resumption

---

## MCS Requirements

### MCS-1: Publishable

**Universal:**
- [ ] Valid SQUAD.md with all 7 required sections
- [ ] README.md with: what the squad does, how to install, how to invoke, requirements
- [ ] Minimum 2 agent files in `agents/`
- [ ] `config/routing-table.md` present
- [ ] Metadata complete
- [ ] No broken file references
- [ ] No syntax errors
- [ ] License from approved list

**Squad-Specific:**
- [ ] Each agent in the squad has a distinct, non-overlapping role
- [ ] Routing logic covers all documented input types
- [ ] At least 1 workflow defined in SQUAD.md

### MCS-2: Quality

**Universal (beyond MCS-1):**
- [ ] `config/handoff-protocol.md` with format specifications
- [ ] 3+ end-to-end workflow examples
- [ ] `config/capability-index.yaml` listing all capabilities
- [ ] Anti-patterns section
- [ ] Tested with 5 different user intents
- [ ] No placeholder content
- [ ] Semver versioning

**Squad-Specific:**
- [ ] All agents in the squad are at MCS-1+ individually
- [ ] Handoff protocol documents the exact format agents pass between each other
- [ ] Workflow examples show multi-agent coordination (not single-agent work)
- [ ] Capability index maps capabilities to agents (who does what)

### MCS-3: State-of-the-Art

**Universal (beyond MCS-2):**
- [ ] Stress-tested routing (ambiguous inputs, agent failure, partial output)
- [ ] Composable agents (each can be used independently outside the squad)
- [ ] Performance metrics (token budget per workflow, time estimates)
- [ ] Cognitive architecture documented for each agent
- [ ] 5+ end-to-end examples including failure recovery
- [ ] Differentiation statement

**Squad-Specific:**
- [ ] All agents at MCS-2+ individually
- [ ] Routing tested with adversarial inputs that try to confuse routing logic
- [ ] Agent failure handling documented (what happens if agent-2 fails mid-workflow)
- [ ] Squad tested as standalone AND as component of a system

---

## Anti-Patterns for Squads

### Structural
- **No routing table:** SQUAD.md describes agents but doesn't define which agent handles which input. The user has to figure out who to call.
- **Single-purpose routing:** All inputs route to one agent 90% of the time. The squad adds overhead without value — just use a standalone agent.
- **Circular handoffs:** Agent A passes to Agent B which passes back to Agent A without progress. No exit condition defined.

### Content
- **Agents without distinct roles:** Two agents that both do "general analysis." Without distinct role boundaries, routing is arbitrary.
- **Handoff without format spec:** Agents are supposed to pass context to each other but the format is undefined. Each agent interprets the previous agent's output differently.
- **Squad that's really a workflow:** Sequential steps are documented as a squad instead of as a workflow. Use a workflow product type for sequential processes; use squads for parallel or routing-based multi-agent work.

### Quality
- **No escalation rules:** Squad has no definition of what it cannot handle. When it fails, it fails silently.
- **Workflow examples that only show happy path:** Real squads encounter routing edge cases, agent failures, and ambiguous inputs. Document how the squad handles these.

---

## Discovery Questions (from §7)

When creating a squad, answer these before scaffolding:

1. What is the squad's mission? (what problem does the team solve together that no single agent can)
2. How many agents are needed and what distinct roles do they fill?
3. What is the routing logic? (who handles what input types)
4. What workflows does the squad execute? (multi-step, multi-agent sequences)
5. What are the handoff protocols between agents? (what format, what context)
6. When does the squad escalate to a human? (explicit conditions)
7. Can individual agents be used outside this squad? (composability requirement for MCS-3)

---

## DNA Requirements

For the complete DNA pattern applicability matrix for this product type,
see `product-dna/squad.yaml`. That file defines:
- Which of the 18 DNA patterns (D-01 to D-18) are required vs optional
- Validation checks per pattern (grep/glob commands)
- Template file mapping with DNA injection points
- Frontmatter fields (Anthropic Agent Skills spec)
- Discovery questions for /create

**MCS scoring:** `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
See `references/quality/mcs-spec.md` for full scoring formula.
