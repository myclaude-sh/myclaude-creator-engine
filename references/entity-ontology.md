# Entity Ontology — Operational Reference
<!-- Loaded by /create, /fill, /validate, /scout when type ∈ {squad, system, agent, minds, workflow} -->
<!-- Source: S100-uemf-product-taxonomy + S118b-uemf-epistemic-map + S100-ecosystem-anatomy -->
<!-- Budget: ~300 lines, ~3K tokens. On-demand only — zero ambient cost. -->
<!-- Update policy: when source docs change, this extract must be updated in the same session. -->

---

## §HERITAGE — Family-Skill Inheritance Chain

```
skill (root primitive)
  └─ agent (adds: persona, tool boundary, memory scopes, context isolation, MCP)
       ├─ minds (agent variant — denied-tools enforced, depth: advisory|cognitive)
       └─ squad (adds: routing.yaml, handoff protocol, install_manifest, D9/D10/D18)
            └─ system (adds: CLAUDE.md fragment, hooks, output-style, STATE.yaml, 13 gears)
```

**Inheritance rules:**
- **skill** carries: D1 (activation protocol), D2 (anti-patterns), D3 (progressive disclosure), D4 (quality gate), D5 (questions), D7 (pre-action read), D13 (self-documentation), D14 (graceful degradation), D16 (composability)
- **agent** inherits ALL skill DNA + adds: D6 (confidence signaling), D8 (state persistence), D11 (socratic pressure), D15 (testability). Gains persona, tool boundary (`tools: ∩ disallowedTools:`), `memory:` scopes, `mcpServers`, `criticalSystemReminder`, `omitClaudeMd`, `isolation: worktree`
- **minds** branches from agent: same DNA, adds denied-tools (Write, Edit, Bash, NotebookEdit). At `depth: cognitive`, adds 5-layer architecture (L1-L5) + 7 cognitive strands (C1-C7). At `depth: advisory`, adds persona + voice + confidence signaling without layers
- **squad** inherits ALL agent DNA + adds: D9 (orchestrate don't execute), D10 (handoff specification), D12 (compound memory), D18 (subagent isolation). Gains routing.yaml, handoff_format_spec, install_manifest
- **system** inherits ALL squad DNA + adds: CLAUDE.md fragment (ambient constitutional), hooks integration, output-style composition, STATE.yaml, 13 functional gears (E0-E12). System is the only entity that both inherits from AND composes squads

**Independent types (no heritage chain):** claude-md, hooks, output-style, statusline, design-system, application, bundle, workflow

---

## §COMPOSITION — What Composes With What

**Containment relations:**
```
system  ──contains──→ { squads, agents, minds, skills, workflows, hooks, claude-md, output-style }
squad   ──contains──→ { agents(2+), minds(0+), skills(0+), workflows(0+) }
bundle  ──aggregates──→ { any combination for joint install }
```

**Usage relations:**
```
agents    ──use──→ skills (as instruments via /skill-name or skills: frontmatter)
agents    ──consult──→ minds (via Agent tool spawn, read-only)
agents    ──spawn──→ agents (subagents for parallel work)
workflows ──orchestrate──→ skills (in fixed sequence)
squads    ──route-to──→ agents (based on routing table + LLM judgment)
```

**Governance relations:**
```
claude-md ──governs──→ ALL (always in context, constitutional)
hooks     ──guards──→ tool execution (PreToolUse blocks, rest observe)
quality-gates ──gate──→ workflow/squad steps (must pass to proceed)
```

**Forbidden compositions:**
- Squad with <2 agents (orchestrator + minimum 1 specialist)
- Orchestrator agent with Write/Edit/NotebookEdit in tool pool (D9 violation)
- Recursive squad spawning without declared depth budget
- Agent calling itself recursively without explicit loop budget
- Product self-validating (Constitution II: production and judgment separated)

---

## §AGENT_ROLES — 7 Functional Archetypes

| Role | Tool Boundary | Handoff Format | Nature | Analogy |
|------|--------------|----------------|--------|---------|
| EXECUTOR | Write, Edit, Bash enabled | Artifacts produced (files, code, output) | Receives task, executes, returns result | The hand that acts |
| SPECIALIST | Read, Glob, Grep only (no write) | Analysis report with findings + confidence | Analyzes, diagnoses, reports. Never modifies. | The eye that examines |
| ORCHESTRATOR | Agent tool only. No Write/Edit/NotebookEdit | Routing decisions + synthesis | Decomposes, delegates, integrates | The conductor |
| ROUTER | Minimal (Read for routing rules) | Classification + direction (which agent next) | Classifies input, applies rules, directs | The synapse |
| ADVISOR | denied-tools: Write, Edit, Bash, NotebookEdit | Judgment + reasoning + recommendation | Reasons, advises, questions. Zero action. | The inner voice |
| VALIDATOR | Read-only tools | Score + verdict + fix instructions | Reads output, applies criteria, recommends | The judge |
| TRANSFORMER | Read + Write (reads input, writes converted output) | Converted output in target format | Input format A → process → output format B | The translator |

**Role determines:**
- Tool boundary (what tools the agent can access)
- Handoff format (what the agent produces for the next agent)
- Spawning pattern (executors get full tools, advisors get read-only)
- Validation criteria (executor = did it produce correct artifact? advisor = was reasoning sound?)

**Role selection heuristic:**
- "This agent needs to write files" → EXECUTOR
- "This agent needs deep analysis without changing anything" → SPECIALIST
- "This agent coordinates other agents" → ORCHESTRATOR
- "This agent classifies and routes requests" → ROUTER
- "This agent thinks alongside the user" → ADVISOR (or minds product)
- "This agent checks quality of other agents' work" → VALIDATOR
- "This agent converts between formats/domains" → TRANSFORMER

---

## §SQUAD_ANATOMY — 8 Mandatory Components

Every squad is a **coordination operating system**, not just "agents in a folder."

| # | Component | Location | Purpose | Without it... |
|---|-----------|----------|---------|---------------|
| 1 | **Agent Roster** | `agents/*.md` | Who is in the team — each agent as separate file with own identity | No team, just files |
| 2 | **Routing Table** | `config/routing-table.md` | Who does what — IF intent → agent mapping | Orchestrator guesses |
| 3 | **Handoff Protocols** | `config/handoff-protocol.md` | How agents communicate — structured envelope (from, to, task, state, constraints) | Information lost between agents (context firewall) |
| 4 | **Workflows** | `workflows/*.md` | Multi-agent sequences — step-by-step with gates and loops | Ad hoc coordination |
| 5 | **Skills-as-Instruments** | `skills/` | Shared tools agents invoke — reusable skill fragments | Each agent reinvents the wheel |
| 6 | **Checklists** | In `SQUAD.md` quality section | Deterministic verification — no judgment needed | Quality is subjective |
| 7 | **Templates** | In `kernel/` | Output format standards — parseable handoff payloads | Each agent invents its own format → handoffs break |
| 8 | **Escalation / Quality Gates** | In `SQUAD.md` escalation section | When to escalate to human — confidence thresholds, loop limits | System never asks for help |

**Completeness rule:** A squad scaffold MUST contain provisions for all 8. Missing any = skeleton, not organism.

---

## §INTELLIGENCE_GRADIENT — Determinism to Autonomy Spectrum

```
DETERMINISTIC ──────────────────────────────────────────→ AUTONOMOUS
hooks        →  skills    →  workflows  →  agents    →  squads    →  systems
│               │            │             │             │             │
always fire     no judgment  fixed         judges        multi-        full
on event        procedural   sequence      autonomous    perspective   organism
                                           context-dep   collaborative
```

**Use this gradient to calibrate product type selection:**
- "Does this need judgment?" → move right (agent, squad)
- "Always the same answer?" → move left (skill, hook)
- "Multiple steps in fixed order?" → workflow
- "Multiple perspectives needed?" → squad
- "Complete environment with governance?" → system
- "Reactive to events, invisible?" → hooks
- "Constitutional, always governing?" → claude-md

---

## §HEURISTICS — Promotion and Demotion Rules

**When to promote:**
- Skill >800 lines of instructions → wants to be agent (H1)
- 2+ distinct expertise areas with different tool needs → squad (H3)
- Skill that needs persistent state across sessions → agent with memory scope
- Squad that needs ambient governance + hooks + output style → system
- Single domain expert with no action needed → minds (advisory)

**When to demote:**
- Agent that never uses judgment (always same response) → demote to skill (H2)
- Squad with 1 useful agent + filler agents → just agent (H3)
- System with no hooks, no claude-md fragment, no cross-cutting governance → just squad

**Critical discriminators:**
- "It depends on context" → agent (needs LLM judgment)
- "Always the same answer" → skill (procedural, deterministic)
- "Fixed sequence, no branching" → workflow (YAML decides, not LLM)
- "Routing varies by input type" → squad (LLM decides next agent)

---

## §WORKFLOW_VS_SQUAD — The Boundary

| Dimension | Workflow | Squad |
|-----------|----------|-------|
| **Who decides next step?** | YAML (declarative, fixed) | LLM (orchestrator applies judgment) |
| **Routing** | Fixed sequence or simple conditionals | Contextual per input, may vary |
| **Agents involved?** | No — skills only (no autonomous units) | Yes — 2+ specialist agents with own identities |
| **Handoffs** | Output passes directly to next step | Structured envelope between isolated contexts |
| **State** | Stateless (each step fresh) | Stateful (routing table + task registry + memory) |
| **When to use** | Repeatable process, no branching by judgment | Multi-perspective analysis, routing needs judgment |
| **Install target** | `.claude/skills/{slug}/` as WORKFLOW.md | Multi-target via install_manifest |
| **Delivery** | Invoked as slash command | Invoked via Agent tool spawn |

**The discriminator is judgment in routing.** If the sequence never changes regardless of input → workflow. If the system must decide which specialist handles this particular input → squad.

---

## §ISOMORPHIC — Human Cognitive System ↔ Claude Code Setup

```
HUMAN COGNITIVE FUNCTION          CLAUDE CODE PRODUCT TYPE
─────────────────────────────────────────────────────────
Skills    ("I can do X")          .claude/skills/         → skill
Advisors  ("I consult X")        .claude/agents/         → minds (denied-tools)
Team      ("We discuss X")       .claude/agents/         → squad (multi-agent)
Values    ("I always do X")      .claude/rules/          → claude-md
Reflexes  ("I automatically X")  settings.json hooks     → hooks
Awareness ("I notice X")         statusline config       → statusline
Identity  ("I look like X")      output-styles/          → output-style
Process   ("I repeat X")         .claude/skills/         → workflow
Environment ("My workspace")     full project            → system
Toolkit   ("My complete gear")   multiple slots          → bundle
```

A fully-equipped Claude Code user has the cognitive equivalent of: skills for executing, minds for thinking, rules for governing, hooks for protecting, squads for multi-perspective analysis, workflows for processes, and a system tying it all together.

---

## §SCOUT_INTELLIGENCE — Research-Informed Type Recommendation

When /scout researches a domain, use this matrix to recommend the optimal product setup:

| Domain Signal | Recommended Type | Rationale |
|---|---|---|
| Single well-defined task | skill | One capability, no judgment |
| Deep expertise area, advisory | minds (advisory) | Think alongside, never act |
| Cognitive modeling of a real person/archetype | minds (cognitive) | 5-layer deep clone |
| Domain with governance rules | claude-md | Always-on constitutional |
| Repeatable multi-step process | workflow | Fixed sequence of skills |
| Domain with distinct specialties | squad | Multi-perspective coordination |
| Complete domain environment | system | Full organism with governance |
| Multiple complementary products | bundle | Curated collection for install |
| Event-driven protections | hooks | Reactive reflexes |

**Composition signals:**
- Domain needs 3+ distinct specialist roles → squad
- Domain has entity lifecycles (objects flow through stages) → squad with task registry
- Domain needs ambient governance + reactive protection + execution → system
- Domain is narrow + deep → skill or minds (not squad)

---

## §RUNTIME_BEHAVIOR — What Happens When Each Type Activates

| Type | Boot | Invocation | Context | Token Cost |
|------|------|------------|---------|------------|
| skill | Catalog (name+desc) always in context | Full SKILL.md injected on `/slug` | Runs in parent context (shared) | Low (~2K on invoke) |
| agent | Catalog always in context | Task tool spawns | Own forked context (isolated) | Medium (~5K+ on spawn) |
| minds | Same as agent | Same as agent | Own forked context, denied-tools | Medium |
| squad | Orchestrator catalog in context | Task spawns orchestrator | Orchestrator → spawns specialists (each isolated) | High (N × agent cost) |
| system | CLAUDE.md fragment every turn | Ambient + slash commands | Full project scope | High (ambient + on-demand) |
| workflow | Catalog in context | Slash command | Runs in parent (like skill) | Low-Medium |
| hooks | Registered at session start | Event fires → if: match | Invisible (shell/agent) | Near-zero until fire |
| claude-md | Always loaded every turn | Automatic (ambient) | Always in context window | Critical (every turn) |
| bundle | Zero runtime cost | myclaude install dispatches | N/A | Zero |
| output-style | Loaded when active | Formatting rules applied | In context when active | Low |

**Critical constraint:** Every agent spawn creates a NEW context with its own token budget. The parent pays the spawn cost. Deep squad hierarchies (orchestrator → specialist → sub-specialist) multiply cost. Design squads flat (orchestrator + specialists), not deep.

---

## §ENTITY_LIFECYCLE — From Intent to Install

```
CREATOR INTENT
  ↓ /scout (research domain, identify gaps, recommend types)
  ↓ /create (scaffold with ontology-aware structure)
  ↓ /fill (walk sections with role-aware questions, ontology-guided elicitation)
  ↓ /validate (check heritage, composition, role coherence)
  ↓ /test (sandbox behavioral verification)
  ↓ /package (strip WHY, generate manifests)
  ↓ /publish (to marketplace)
USER INSTALL
  ↓ myclaude install {slug}
  ↓ Product lands in correct slot per §RUNTIME_BEHAVIOR
  ↓ COMPOSE: multiple products form a setup (the real value)
```

**The Engine's ultimate output is not "a product." It's "a setup that makes someone superhuman in domain X."**
