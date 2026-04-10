# Entity Ontology — Operational Reference
<!-- Loaded by /create, /fill, /validate, /scout when type ∈ {squad, system, agent, minds, workflow} -->
<!-- Source: Engine internal ontology research (docs/briefs/ + docs/research/). Do not distribute. -->
<!-- Budget: ~420 lines, ~4.5K tokens. On-demand only — zero ambient cost. -->
<!-- Update policy: when source docs change, this extract must be updated in the same session. -->

---

## §FOUNDATIONAL_THESIS — Why Restrictions Generate Intelligence

A cognitive system is NOT defined by what it CAN do — it's defined by what it physically CANNOT do and what useful flow that impossibility channels. `disallowedTools` is not a wall — it's a mitral valve. `omitClaudeMd` is not deprivation — it's focus. Every restriction in Claude Code (`tools: ∩ disallowedTools:`, `denied-tools`, `context: fork`, `paths:` scoping) generates a specific cognitive flow:

- Agent denied Write → forced to reason and advise (ADVISOR flow)
- Agent denied all except Agent tool → forced to coordinate (ORCHESTRATOR flow)
- Skill with `paths:` scoping → activates only in relevant context (METABOLIC efficiency)
- Fork with `omitClaudeMd` → focused specialist uncorrupted by parent constitution

**Design principle:** When creating any product, ask: "What should this NEVER be able to do?" — the answer generates the intelligence flow. Capability without restriction is noise. Restriction without capability is paralysis. The dance between both IS the system.

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

## §TRANSVERSAL_AXES — Beyond Linear Hierarchy

Product type is NOT the only dimension. Three orthogonal axes cut across all types:

| Axis | Values | What it determines |
|------|--------|-------------------|
| **Delivery** | slash-command (skill/workflow) · agent-spawn (agent/minds/squad) · ambient (claude-md/hooks) · install-only (bundle) | HOW the product activates at runtime |
| **Nature** | procedural (no judgment) · advisory (judgment, no action) · executive (judgment + action) · orchestrative (judgment + delegation) | WHAT kind of cognition the product applies |
| **Depth** | surface (~100 lines, one concern) · functional (~500 lines, domain slice) · cognitive (~1000+ lines, deep model) | HOW MUCH intelligence the product carries |

**Why this matters:** A skill CAN be cognitive-depth (e.g., Kairo has deep reasoning despite being a skill). A minds CAN be procedural (e.g., a simple Q&A advisor). The type determines the delivery mechanism and tool boundary — but Nature and Depth are chosen by the creator. Don't assume skill=shallow or minds=deep.

**Use during /create:** After type selection, calibrate Nature and Depth: "Your tool will be [procedural/advisory/cognitive]. How deep should the expertise go?"

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

## §SYSTEM_ENGINES — 13 Functional Gears of a System (type=system only)

A system is NOT a "squad with extras." It is an **organism** with 13 functional gears that couple together. Each gear has a counterpart — without the counterpart, the gear is a drawer, not a muscle.

| # | Engine | One-line essence | Mechanism | Counterpart | Without it... |
|---|--------|-----------------|-----------|-------------|---------------|
| E0 | **Clausura operacional** | Boundary between inside and outside | `omitClaudeMd`, `context: fork`, `tools: ∩ disallowedTools:`, ephemeral MCP | E4 (perception) | No boundary = no organism |
| E1 | **Metabolismo declarado** | Token cost to exist at rest + operate on demand | `paths:` scoping, `omitClaudeMd`, fork cache, Clause VIII budgets | E0 (clausura) | Cost invisible = death by tokens |
| E2 | **Constituição re-injetada** | Identity re-declared every turn — active, not passive | `criticalSystemReminder`, CLAUDE.md per-turn reload, `initialPrompt` | E1 (costs tokens) | Identity only in prose = drift |
| E3 | **Camada mnemônica tripla** | Memory in 3 orthogonal substances: hereditary + procedural + declarative | `skills:` frontmatter (hereditary), STATE.yaml (procedural), `memory:project` (declarative) | E11 (self-observation feeds declarative) | Memory collapses to single layer |
| E4 | **Percepção ambiental** | System senses what changed since last turn | 4 hook types, `if:` matching, SessionStart/PreToolUse/PostToolUse/Stop events | E0 + E5 (perception needs boundary + reflex) | Blind organism |
| E5 | **Reflexo cognitivo** | Automatic responses to perceptions — **including responses that need judgment** | AgentHook (reflex that thinks), PromptHook (LLM evaluates), Bash/Http (mechanical) | E6 (deliberate judgment) | Rigid or slow — never both adaptive and fast |
| E6 | **Julgamento isolado** | Specialized decision units with own context, own tools, own constitution | `context: fork`, `tools: ∩ disallowedTools:`, 7 agent roles | E7 (network connects judgments) | Isolated opinions, not coordinated system |
| E7 | **Rede de coordenação** | Connective tissue between specialized judgments | routing.yaml, handoff_format_spec, install_manifest, native parallelism | E8 (voice — network without presence is invisible) | Ad hoc coordination |
| E8 | **Voz externa** | Identity signature to the world — how the system presents itself | output-style composition across agents | E2 (voice without constitution = empty performance) | No recognizable identity |
| E9 | **Integridade recursiva** | System passes its own validator pointed at itself (Clause VII) | `/validate --target=self`, AgentHook as verifier | E11 (point vs continuous recursion) | Hypocrisy — preaches but doesn't practice |
| E10 | **Estado persistente** | Serialized artifacts that survive /compact, reinstall, update | STATE.yaml, .meta.yaml, install_manifest, .manifest-lock, memory scopes | E1 (IO has cost) | Amnesia between sessions |
| E11 | **Auto-observação longitudinal** | Observer agent building semantic dossier on system's own operation over time | PostToolUse hook → AgentHook spawns observer → observer reads recent context → writes narrative to memory:project → next session's agents read accumulated narrative → creator reviews dossier → updates criticalSystemReminder. This is a SECOND-ORDER recursion loop: the system observes itself observing. | E3 (bidirectional) + E9 (continuous vs point) | Self-blindness — no learning from own behavior |
| E12 | **Ciclo de vida reversível** | Install → operate → uninstall, all auditable and reversible via hash-verified manifest | install_manifest, .manifest-lock, `myclaude install/uninstall` | E1 (install cost) | Can't coexist ecologically with other systems |
| META | **Acoplamento declarado** | For each active gear, creator declares its counterpart and why | `coupling_declaration:` field in system codex | ALL gears | Pile of drawers, not organism |

**Critical chains:**
- **Sensorimotor chain:** E4 → E5 → E6 → E7 (perception → reflex → judgment → coordination). Break any link = organism can't respond to environment.
- **Self-narrative pair:** E3 ↔ E11 (memory + self-observation feed each other). This produces the self-narrative — the system that knows itself.
- **Recursive pair:** E9 ↔ E11 (point recursion + continuous recursion). Together = honest system.
- **Condition of possibility:** E0 (clausura) must be the first gear declared — without boundary, nothing else matters.

**Discovery for /create system:** Ask the creator which gears they want active. Not all 13 are needed for every system — E11 is optional for MCS-1/MCS-2, E12 only matters for distributed systems. But the creator must **declare** which gears are active and which are deferred.

**Anti-patterns (one per gear):**
- AP-S1: Pile without counterparts — gears listed but no coupling declared
- AP-S3: Identity only in prose — E2 constitution not re-injected at runtime
- AP-S5: Reflex without judgment OR judgment without reflex — E5/E6 must be paired
- AP-S7: Free-text routing — E7 coordination without structured handoffs
- AP-S9: Structural hypocrisy — claims P9 but can't pass own validator
- AP-S11: Self-blindness — no E11, system can't learn from own behavior

**Orthogonal dimensions of coupling (how gears connect across time):**
1. **Dual temporal homeostasis** — system must wake up correct (SessionStart hook → verifier) AND stay correct per-turn (criticalSystemReminder re-injection). Two clocks, one identity.
2. **Dual plasticity** — habitat adapts at install time (install_manifest places files) AND moment-to-moment at operation (paths: scoping, conditional skill activation). Structure AND behavior adapt.
3. **Dual cognition (spinal cord + brain)** — stigmergic reflexes (hooks fire without thinking) AND deliberate orchestration (agents reason about routing). Medulla AND cortex. Fast AND deep.
4. **Triple memory** — hereditary (skills: frontmatter preloads knowledge), procedural (STATE.yaml tracks what happened), declarative (memory:project stores narrative understanding). DNA AND habits AND autobiography.

---

## §CONSTITUTIONAL_PRIMITIVES — Identity Enforcement at Runtime

`criticalSystemReminder_EXPERIMENTAL` is the most powerful and least documented Claude Code primitive. It re-injects a constraint string at EVERY turn of an agent's conversation — making it physically impossible for the agent to "forget" its mandate over long conversations. This is D1 (Activation Protocol) + D14 (Graceful Degradation) made physical.

**Use for:** Any agent/minds that must maintain identity over 50+ turns. The verification agent uses it to prevent mandate drift. Cognitive minds should use it to preserve their cognitive architecture.

**How it works:** Declared in agent frontmatter or programmatically. Re-injected by Claude Code runtime before each assistant turn. The agent cannot remove or override it — it's constitutional, not conversational.

---

## §COMPOSITION_PRINCIPLES — How Products Think Together

Beyond containment rules (§COMPOSITION), products compose with cognitive principles:

1. **Convergence by independence** — Multi-mind analysis (e.g., Kairo + Leonardo + Lozano) produces apex insight when each mind reasons INDEPENDENTLY and results converge. Consensus is weak. Convergence from independent paths is strong. Design squads where specialists don't see each other's work until synthesis.

2. **Symbiosis > aggregation** — mind + skill = advisor watches while hands work (1+1>2). mind + mind = debate without action (1+1<2 unless one orchestrates). hooks + claude-md = automatic enforcement of constitutional rules (immune system). Design compositions where each product fills a cognitive gap the other can't.

3. **Intelligence gradient as composition axis** — Compose along the gradient: hooks (reactive) → skill (procedural) → workflow (sequential) → agent (autonomous) → squad (collaborative). A complete setup has products at MULTIPLE points on the gradient, not all at the same level.

---

## §INTELLIGENCE_PIPELINE — How Knowledge Enters Products

The Engine's soul is **condensing intelligence into installable tools**. This pipeline is how:

```
DOMAIN EXPERTISE (raw, unstructured)
  ↓ /scout — test Claude's baseline, identify gaps, research via web
  ↓         Output: scout-{domain}.md with baseline, gaps, findings, recommendations
  ↓
  ↓ /create — scaffold WITH scout intelligence injected
  ↓           Scout findings become WHY comments in the scaffold
  ↓           Type recommendation comes from §SCOUT_INTELLIGENCE
  ↓
  ↓ /fill — ACTIVE distillation (not passive read)
  ↓         Step 1: Load scout report → extract baseline, gaps, findings
  ↓         Step 2: For each section, PROPOSE content from research
  ↓         Step 3: Creator VALIDATES, REFINES, or REJECTS
  ↓         Step 4: Sparring challenges generic answers
  ↓         Step 5: Deepening methods extract tacit knowledge
  ↓         Result: Product carries structured intelligence, not just instructions
  ↓
  ↓ /validate — verify substance
  ↓             Baseline delta: is this better than Claude vanilla?
  ↓             Anti-commodity: does this have genuine expertise?
  ↓             Cognitive fidelity: does the knowledge survive compression?
  ↓
OUTPUT: Installable tool that carries a domain's intelligence
        Not a formatted prompt — a cognitive extension
```

**The discriminator:** A product from the Engine should contain knowledge that the user CANNOT get from vanilla Claude. If `/validate` can't demonstrate this delta, the product is commodity.

**Hermeneutic spiral (for apex products — systems, cognitive minds):**
For complex products where a simple scout isn't enough, the Engine can run a deeper intelligence cycle:
1. **Raw observation** — multiple independent observers (Leonardo, Kairo, domain expert) examine the domain without structure
2. **Rigorous audit** — a second pass where the auditor DISAGREES with the first observer, finding what was missed
3. **Latent breaches** — surface patterns that no single observer caught but that emerge from the disagreements
4. **Relational map** — synthesize into a UEMF-grade epistemic map that becomes the product's knowledge substrate
This spiral is optional (scout alone suffices for most products) but produces orders-of-magnitude deeper intelligence for MCS-3 targets.

**How /fill should actively inject intelligence (not passively read):**
1. Load scout report findings
2. For each product section, check: "Does the scout report have relevant research for this section?"
3. If YES → propose: "Based on research, {finding}. Does this match your experience? What would you change?"
4. If NO → extract from creator: "The research didn't cover this. What's YOUR insight here?"
5. After each major section, sparring challenge: "If I removed this section, would the product still be better than Claude vanilla?"

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

**Feedback loop (publish → learn → improve):**
When a product is published and used, its performance data (installs, ratings, usage patterns) feeds back into the Engine's intelligence:
- Low substance score on published product → /fill increases sparring intensity for same domain
- Unroutable intent during /create → logged with reason enum (no_match / composition_gap / ambiguous) → informs what to build next
- Products that survive daily use teach the Engine what patterns work — products that fail teach what doesn't

**Confidence discipline:**
- **Spec confidence** (is the design sound?) ≠ **execution confidence** (is the implementation correct?). Never collapse these — a brilliant spec badly implemented is worse than no spec.
- When /validate reports scores, distinguish: structural score (is it built right?) vs substance score (does it carry real intelligence?) vs delta score (is it better than vanilla?).
