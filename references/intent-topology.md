# Intent Topology — How the Engine Translates Creator Intent Into Product Form

This document defines how the Engine translates a creator's natural-language intent into the correct product form, without forcing the creator to know the Engine's type vocabulary first. It is the canonical substrate for the `/create` skill in discovery mode — the moment where a creator says *"I want a tool that does X"* and the Engine answers with a form proposal grounded in three transversal axes, a derived runtime host, and a small set of empirically habitable cells.

**Layer:** Canonical substrate. Consumed by `.claude/skills/create/` and `.claude/skills/validate/` Stage 0 Intent Coherence. Extended by `references/capability-matrix.md` (the 12-step decision algorithm), `references/skill-vs-agent-discriminators.md`, `references/composition-anatomy.md`, and `references/runtime-host-dag.md` (the derivation table).

**Reading order:** §1 problem → §2 three axes → §3 runtime host derivation → §4 habitable cells (v1) → §5 deferred cells (v2) → §6 how this document is used.

---

## §1 — Why This Exists

The Engine previously asked creators to choose between 13 flat product types (skill, agent, squad, workflow, design-system, claude-md, application, system, bundle, statusline, hooks, minds, output-style) **before** they had expressed what they actually wanted the tool to do. This is mechanism before purpose — a direct violation of the Engine's own Principle 1 (P1 Purpose Before Shape, `structural-dna.md`). The observed consequence: creators chose type by familiarity or by guess, not by adherence to the use case. Products were born in the wrong format, and marketplace quality degraded asymmetrically with creator experience — beginners shipped skills that should have been agents, experts shipped agents that should have been skills.

The fix is not a larger type menu. The fix is moving the Engine's intelligence earlier in the flow: the creator expresses intent in natural language; the Engine translates that intent into three orthogonal-enough axes; the runtime host follows deterministically by derivation; the canonical form falls out of the translation; the creator confirms and forges. The creator's cognitive load stays constant (one intent expressed in their own words); the Engine's cognitive load increases (three-axis reasoning inside `/create`) — and that is the correct direction for complexity to move.

Two operating modes preserve autonomy on both ends of the experience spectrum:

- **Express mode** — zero discovery questions. The creator names the form directly (`/create skill my-tool --cognitive`) and the Engine validates coherence at the back via Stage 0 in `/validate`. Triggered automatically for advanced/expert creators with autonomous workflow preference.
- **Guided mode** — full discovery walk. The creator expresses intent in natural language and the Engine walks the 12-step decision algorithm (defined in `references/capability-matrix.md`) to propose a form. Triggered automatically for beginner/intermediate creators or when workflow preference is guided.

Both modes write the same `intent_declaration` schema and feed the same `decisions_history` longitudinal feedback loop (defined in `references/capability-matrix.md` §6). The dual mode is not two separate systems — it is one system with a single data contract and two entry points.

---

## §2 — The Three Transversal Axes

The core discovery: delivery mechanism, operational nature, and cognitive depth are **transversal attributes of artifacts**, not properties of types. A skill can be procedural or cognitive. An advisor can be delivered as a skill (ambient, in-parent) or as an agent (task-spawned, isolated). A cognitive architecture can live inside an ambient skill or inside a task-spawned mind. The flat 13-type menu hid these axes by collapsing them into pre-composed bundles — and pre-composition only matches use cases when the creator happened to need exactly that bundle.

The three axes below are the Engine's internal reasoning surface. Creators never see them named as axes — they see their translated output (a form proposal, a rationale, alternatives). The axes exist to make the Engine's judgment traceable and testable, not to educate creators about taxonomy.

### §2.1 — Axis 1: Delivery Mechanism (6 values)

How the artifact reaches the session. Each value is traced to a verified source in the Claude Code platform.

| Value | Description | Used by types | Cost profile |
|---|---|---|---|
| `ambient_constitutional` | Loaded every turn as part of the CLAUDE.md 4-tier hierarchy. Always in the ambient window. | claude-md | Always in ambient window (≤4K chars per file, 40K total hard cap) |
| `ambient_path_scoped` | Skill dormant until a file matching its `paths:` glob is touched. Injected as isMeta user message on match. | skill | Zero until match; full skill body after match |
| `invoked_slash_command` | Skill invoked explicitly via `/{command}`. User-initiated, preserves parent context. | skill | Zero until invoked; full skill body after invocation |
| `invoked_task_spawn` | Agent spawned via Task tool. Forked context, own tool pool, own system prompt, own memory. | agent, minds, squad | Full agent context fork per spawn; catalog cost ~50-80 tokens per agent always visible |
| `reflex_hook_binding` | Hook handler bound to one of 27 canonical hook events. Fires automatically when matching event emitted. | hooks | Ambient evaluation cost per matching event; handler cost per fire |
| `composed_system` | myClaude convention — multi-destination install dispatching CLAUDE.md fragment + sub-agents + sub-squads + hooks + output-style as a reversible bundle. | system | Varies by composed parts; inherits costs of each sub-part |

**Note on task-spawn heredity.** Agents spawned via `invoked_task_spawn` may optionally preload skills into their fork via the `skills:` frontmatter field — those skills are injected as isMeta messages at spawn time. This does not change the delivery vector; it adds hereditary cognition on top of it. An agent with a preloaded cognitive skill is still delivered by task-spawn; the preloaded skill rides along.

**Verification:** each delivery mechanism's behavior is grounded in `references/claude-code-ground-truth.md` Layer 0 (CLAUDE.md hierarchy), Layer 1 (agent primitives), Layer 2 (27 canonical hook events). No value in this table is asserted without platform-source backing.

### §2.2 — Axis 2: Operational Nature (4 primitives)

What the artifact does when it runs. The tool pool signature is the primary discriminator — it maps deterministically to a small number of permission shapes.

| Value | Description | Tool pool signature | Inherits from archetype |
|---|---|---|---|
| `executor` | Mutates external state (files, shell, APIs). | write-capable (Write, Edit, Bash, NotebookEdit) | agent.specialist, agent.generalist, agent.fork_heir |
| `advisor` | Delivers judgment without mutating state. Confidence signaling via certainty bands mandatory. | read-only | agent.scout, agent.architect, agent.adviser, all minds archetypes |
| `orchestrator` | Routes to other artifacts without executing the work itself. | delegation-only (Agent tool, no direct mutation) | agent.orchestrator, all squad archetypes |
| `observer` | Writes to memory scope without responding to user. Background actor, typically fired via AgentHook. | write-to-memory-only | hooks with AgentHook handlers |

**On the removed `augmenter` primitive.** An earlier draft of this topology declared `augmenter` as a fifth operational nature. Structural analysis proved the label was tautological with `advisor` crossed with ambient delivery — specifically, `delivery_mechanism ∈ {ambient_path_scoped, invoked_slash_command} AND operational_nature == advisor`. The label survives in user-facing copy where it communicates the felt experience of *"something appears beside me and makes my current thinking better"*, but it is not a primitive — it is an emergent label computed from the axes above. Including it as a primitive would duplicate information and double-count cells in §4.

### §2.3 — Axis 3: Cognitive Depth (3 values)

How much cognitive architecture the artifact needs. This axis is preserved verbatim from `product-dna/minds.yaml` — the minds codex defined the `depth_discriminator` rubric and the Engine inherits it unchanged.

| Value | Description | DNA minimum | Forge cost |
|---|---|---|---|
| `procedural` | Operates by declared rules without persona or cognitive architecture. The classic deterministic handler. | D1, D2, D3, D4, D13, D14 | Low |
| `advisory` | Declared persona with voice, bounded knowledge, and confidence signaling — but without 5-layer architecture. | D1, D2, D3, D4, D5, D6, D13, D14 | Medium |
| `cognitive` | Deep cognitive architecture: 5 layers (L1 Boot, L2 Cognitive Core, L3 Personality Engine, L4 Knowledge Domains, L5 Reasoning Engine) plus 7 cognitive DNA strands C1-C7. | D1, D2, D3, D4, D5, D6, D11, D13, D14, D15 + C1-C7 | High (5-10× advisory) |

Cognitive depth becomes available for type `skill` via the `depth_discriminator` extension to `product-dna/skill.yaml` (delivered in the codex-extension wave). Before that wave, cognitive skills exist empirically (the reasoning-companion skill and Renaissance-perspective skill both live on disk as cognitive skills) but the codex does not yet formally discriminate them — which is exactly why this topology exists: to retire the fiction that cognitive depth belongs only to type `minds`.

---

## §3 — Runtime Host Derivation

The runtime host of an artifact — where its execution actually happens at the moment of invocation — is **derived**, not declared. Given the pair `(delivery_mechanism, operational_nature)`, the host set is computable with zero ambiguity. Enumerating the 6 × 4 = 24 combinations produces a deterministic lookup table; every habitable combination has exactly one host set, and no combination requires a separate declaration on the artifact itself.

An earlier draft of this topology declared host as a fourth axis with four classes (`session_root`, `agent_spawn`, `preloaded_in_agent`, `hook_handler`). That draft failed a structural test: no consumer in `config.yaml` or in any of the six certified codices reads a `host_compatibility` field. The field duplicated information without having its own nerve — it was vestigial. The fix is to compute host from the pair at validate time and never declare it on artifacts.

```
# Runtime host derivation — computed from (delivery, nature), not declared

ambient_constitutional + any                   → [session_root]
ambient_path_scoped    + executor|advisor      → [session_root, preloaded_in_agent*]
invoked_slash_command  + executor|advisor      → [session_root]
invoked_task_spawn     + any                   → [agent_spawn]
reflex_hook_binding    + executor              → [session_root, agent_spawn]
reflex_hook_binding    + observer              → [hook_handler → agent_spawn chain]
composed_system        + any                   → [multi — inherited from composed sub-parts]

* preloaded_in_agent is a specialization of session_root reachable only when an agent
  is spawned with an ambient_path_scoped skill in its skills: frontmatter. It is not
  an independent host.
```

The full DAG with examples per row lives in `references/runtime-host-dag.md`. This document declares the principle; the DAG document declares the table.

**Consequence for codex extensions:** when the six certified codices are extended with the new fields (in the codex-extension wave), they receive `delivery_mechanism` and `operational_nature` as declared fields. They do **not** receive a `host` field. Any future code that needs the host computes it from the pair at read time.

---

## §4 — Habitable Cells (v1 — 7 cells)

The cartesian product of the three axes is 6 × 4 × 3 = 72 theoretical combinations. The three axes are not fully orthogonal — many combinations are physically impossible (e.g., `composed_system` with `observer` nature has no forge path; `reflex_hook_binding` with `cognitive` depth requires composition). The habitable subset is small.

A **habitable cell** is a combination that is both (a) physically possible in the platform, and (b) empirically grounded — meaning at least one real exemplar in `references/exemplars/` or in the creator's current workspace can be classified into the cell without ambiguity. A cell without an exemplar is a hypothesis, not a habitable cell, and lives in §5 instead.

The v1 set below is the full set of cells that `/create` in discovery mode routes into. Wave regression tests for the `/create` rewrite run **only** against v1 cells. The v2 cells in §5 are documented, not tested — they are deferred until production validates them or a review wave deprecates them.

### Cell 1 — `reasoning_skill_cognitive`

| Field | Value |
|---|---|
| delivery | `invoked_slash_command`, `ambient_path_scoped` |
| nature | `advisor` |
| depth | `cognitive` |
| canonical form | cognitive skill |
| type | skill |
| archetype hint | reasoning orchestrator |
| covered by | reasoning-companion skill (cognitive audit), payload-designer skill |

**Why this cell.** Cognition that needs to think **with** the parent context, not for it. Continuity preserved; the creator's current working memory is the substrate the skill reasons over. Isolation would defeat the purpose — there is no parent context to think alongside after a task spawn.

### Cell 2 — `perspective_skill_cognitive`

| Field | Value |
|---|---|
| delivery | `ambient_path_scoped`, `invoked_slash_command` |
| nature | `advisor` |
| depth | `cognitive` |
| canonical form | cognitive skill (ambient-preferred) |
| type | skill |
| archetype hint | perspective augmenter |
| covered by | Renaissance-perspective skill for design contexts |

**Why this cell.** Valuable when it appears without being asked. Ambient delivery beats invoked delivery for this case because the creator benefits most when the perspective arrives **before** they thought to ask for it — the whole point of a perspective skill is catching blind spots the creator would not have named.

### Cell 3 — `apex_cognitive_mind`

| Field | Value |
|---|---|
| delivery | `invoked_task_spawn` |
| nature | `advisor` |
| depth | `cognitive` |
| canonical form | cognitive minds |
| type | minds |
| archetype hint | cognitive mentor, research partner, strategic thinker, or creative catalyst |
| covered by | fusion mind for high-stakes decisions |

**Why this cell.** Apex embodied cognition delivered in isolation. The 5-layer architecture is mandatory — this is the cell where a mind fully inhabits its own cognitive frame without leaking into the parent's reasoning. Used when the creator explicitly wants the cognition **to be another mind in the room**, not another perspective in their own mind.

### Cell 4 — `code_reviewer_agent`

| Field | Value |
|---|---|
| delivery | `invoked_task_spawn` |
| nature | `advisor` |
| depth | `procedural` |
| canonical form | agent adviser (read-only) |
| type | agent |
| archetype hint | adviser |
| covered by | security audit specialist |

**Why this cell.** Isolation prevents review bias from being polluted by the parent's own code-in-progress. An advisor that reviews the same code it is helping to write is structurally compromised — it inherits the same justifications. Task-spawn with read-only tool pool is the correct shape.

### Cell 5 — `domain_specialist_executor`

| Field | Value |
|---|---|
| delivery | `invoked_task_spawn` |
| nature | `executor` |
| depth | `procedural` |
| canonical form | agent specialist |
| type | agent |
| archetype hint | specialist |
| covered by | TypeScript refactor specialist |

**Why this cell.** Write-capable narrow-scope delegation with enforced tool boundary. The specialist archetype exists precisely because unbounded executors are dangerous and unbounded generalists are imprecise. Narrow scope + enforced boundary = the shape that ships.

### Cell 6 — `procedural_skill`

| Field | Value |
|---|---|
| delivery | `ambient_path_scoped`, `invoked_slash_command` |
| nature | `executor` or `advisor` |
| depth | `procedural` |
| canonical form | skill (procedural) |
| type | skill |
| archetype hint | procedural skill (no persona) |
| covered by | scout domain researcher, handoff creator skill, payload designer skill (template-layer) |

**Why this cell.** The classic skill — focused reusable capability with no persona and no cognitive architecture. This is the most common cell in the marketplace and the most common cell a creator should be forging. When in doubt, this is the default.

### Cell 7 — `project_constitution`

| Field | Value |
|---|---|
| delivery | `ambient_constitutional` |
| nature | `advisor` |
| depth | `procedural` |
| canonical form | claude-md product |
| type | claude-md |
| archetype hint | paths-scoped constitutional rules |
| covered by | Engine rules constitution fragment |

**Why this cell.** Rules always active in session. The `paths:` frontmatter enables conditional activation by file type, which is the only sustainable way to carry constitutional content without blowing the ambient token budget.

---

### Cell 8 — `squad_coordinator`

| Field | Value |
|---|---|
| delivery | `invoked_task_spawn` |
| nature | `orchestrator` |
| depth | `procedural` (squad-level; sub-agents carry their own depth) |
| canonical form | squad |
| type | squad |
| archetype hint | sequential_pipeline, parallel_fan_out, conditional_router, iterative_refinement, hierarchical_delegation |
| covered by | cognitive-fusion-lab (5 agents, fusion protocols), published squad products in workspace |

**Why this cell.** Multi-agent coordination delivered as one installable organism. The orchestrator routes, delegates, and synthesizes — it never executes domain work directly (D9). Sub-agents carry their own cognitive depth (procedural, advisory, or cognitive minds). The squad's depth is always procedural at the coordination layer; intelligence lives in the specialists.

---

## §5 — Deferred Cells (v2 — 11 cells)

The cells below are physically possible in the platform but lack v1 exemplar coverage. They are documented here for two reasons: (a) to make the deferral explicit and honest, instead of silently pretending they don't exist; (b) to give future waves a prioritized queue when promoting v2 cells to v1 as exemplars accumulate.

**Deferred cells are not tested by `/create` regression in v1.** Attempting to scaffold into a deferred cell falls through to the existing Q1/Q2/Q3 legacy router as a "don't know yet" branch — the creator is not blocked, they simply get the pre-discovery-mode experience for that specific request until a future wave promotes the cell.

| Cell id | Axes | Canonical form | Deferred because |
|---|---|---|---|
| `domain_advisor_agent` | task_spawn × advisor × advisory | advisory minds or agent adviser | Overlaps structurally with `code_reviewer_agent`; the ambiguous `type: [minds, agent]` needs cell↔form disambiguation first |
| `general_purpose_agent` | task_spawn × executor × procedural | agent generalist | The general-purpose archetype is a native Claude Code built-in, not a forged product — discovery mode should not scaffold it |
| `squad_coordinator` | task_spawn × orchestrator × procedural | squad | Promoted to v1 Cell 8. See §4. |
| `event_reflex` | hook_binding × executor|observer × procedural | hooks product | Hooks forge has a mature direct path; discovery mode adds no v1 value |
| `longitudinal_observer` | hook_binding × observer × cognitive | AgentHook spawning cognitive minds (composition) | **Orphan cell** — `/create` has no forge path for multi-type composition in v1. Blocked by GAP-COMPOSITION-1: multi-type composition forge path does not exist. Revisit in a future wave that designs type+type composition |
| `procedural_workflow` | slash_command × executor × procedural | workflow | Workflow forge has a mature direct path; discovery mode adds no v1 value |
| `voice_fragment` | ambient_constitutional|slash_command × advisor (augmenter emergent) × procedural | output-style | Output-style forge has a mature direct path; discovery mode adds no v1 value |
| `visual_design_language` | slash_command × advisor × procedural | design-system | Design-system is its own vertical; discovery mode routing not required for v1 |
| `ambient_status_display` | ambient_constitutional × advisor × procedural | statusline | Statusline forge has a mature direct path; discovery mode adds no v1 value |
| `cognitive_organism_full_stack` | composed_system × orchestrator × cognitive | system | Self-referential (the Engine is this cell); no independent v1 exemplar; system forge is its own apex codex |
| `marketplace_composition` | composed_system × orchestrator × procedural | bundle | Bundle forge has a mature direct path; discovery mode adds no v1 value |
| `deployable_application` | composed_system × executor × procedural | application | Non-Claude-Code-primitive product (real software); application forge is orthogonal to discovery mode |

**Promotion path v2 → v1.** A v2 cell is promoted to v1 when: (a) at least one real exemplar in `references/exemplars/` or creator workspace can be classified into the cell without ambiguity, (b) the disambiguation note (if any) is resolved, and (c) the regression test for the cell can be written and passes on at least one held-out model run. Promotion is additive — it requires writing, not rewriting — and is safer than the reverse direction.

---

## §6 — How This Document Is Used

This topology is the substrate for three consumers:

1. **`.claude/skills/create/`** — `/create` in discovery mode walks the 12-step decision algorithm (defined in `references/capability-matrix.md`) using the three axes above, derives the host from §3, and looks up the matched cell in §4. The existing Q1/Q2/Q3 router in `.claude/skills/create/references/create-router.md` is preserved as fallback for the "don't know yet" branch — specifically, for intents that route into §5 deferred cells or fail to route at all.

2. **`.claude/skills/validate/` Stage 0 Intent Coherence** — a new validation stage reads the `intent_declaration` written by `/create` at forge time and verifies that the forged product still matches the declared cell. If a product's files drifted from the cell after `/fill`, Stage 0 surfaces the drift as a coherence warning. Stage 0 is advisory, not blocking — it informs the creator, not the gate.

3. **Codex extensions (codex-extension wave)** — `product-dna/skill.yaml` gains a `depth_discriminator` section mirroring `minds.yaml`. All six certified codices (output-style, skill, agent, squad, system, minds) gain `delivery_mechanism` and `operational_nature` fields as declared attributes. None of them gain a `host` field — host is derived per §3 and never declared on artifacts.

**What this document is not.** This document is not the decision algorithm. It declares the axes, the derivation, and the cells. The algorithm — the 12 decision steps, the afferent/efferent wiring between `creator.intent_profile` fields and decision steps, the Express↔Guided transition protocol — lives in `references/capability-matrix.md`. Read this document first, then that one.

**What the creator ever sees of this document.** Nothing, directly. The creator sees the translated output — a form proposal, a one-sentence rationale, two alternatives, and the ability to override. The axes, cells, and derivation table are the Engine's internal reasoning surface. Keeping that surface invisible to the creator is a direct application of the Engine's P8 (Invisibility of Mechanism) — users experience capability, not machinery.

---

**Status.** Canonical substrate, v1. Extended by the four companion documents listed in the reading order above. This document is immutable for the duration of the discovery-mode `/create` rewrite — changes require a new wave, not an edit.
