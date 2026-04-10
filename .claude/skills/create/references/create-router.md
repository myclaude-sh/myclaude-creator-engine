# Create Router — Decision Tree, Scaffold Structures, Prefilling

Full routing logic and scaffold details for the `/create` skill.
Load this file when: routing a creator through type selection, generating a scaffold structure, or building prefill content.

---

## SECTION 0: DISCOVERY MODE — The 12-Step Walk (PRIMARY ROUTER)

**Source of truth: `references/capability-matrix.md §3`.**

This is the primary routing layer. Discovery mode reasons from creator intent to a form
proposal via three transversal axes (delivery × nature × depth), derives runtime host from
the `(delivery, nature)` pair, looks up the matched cell in `references/intent-topology.md §4`,
and writes a full `intent_declaration` block to `.meta.yaml`. The legacy Q1/Q2/Q3 tree in
Section 1 below is the fall-through for unroutable cases (Contract C4).

### Mode Selection (fires at /create invocation, before any questions)

Read `creator.yaml`:

| Creator state | Mode | Behavior |
|---|---|---|
| `profile.technical_level ∈ {advanced, expert}` AND `preferences.workflow_style == autonomous` | **Express** | Skip the walk. Creator named the form via sub-command. Apply type+sub-type defaults. Write `intent_declaration` with `mode: express` at Step 11. |
| `profile.technical_level ∈ {beginner, intermediate}` OR `preferences.workflow_style == guided` | **Guided** | Walk the full 12 steps. Ask clarifying question only at natural gates (Step 1 ambiguous verb, Step 6 cognitive justification). Max one question per gate. |
| `creator.yaml` missing | **Guided + micro-onboard** | Run the micro-onboard path first, then enter Guided. Creator never blocked. |
| `--express` flag OR `--discovery` flag | **Manual override** | Flag wins over inferred mode. Announce switch in one line, creator's language. |

**Both modes write the same 19-field `intent_declaration` schema** (see
`.claude/skills/create/SKILL.md` `.meta.yaml` template block). The difference is where the
intelligence operates: Express puts it at the back (Stage 0 validates coherence post-forge);
Guided puts it at the front (the walk reasons before scaffold exists).

### Pre-Walk Setup (runs once before Step 1)

Before entering the 12-step walk, load these substrate files into the router's working context:

1. `references/capability-matrix.md §3` — the 12 steps (THIS is the contract)
2. `references/intent-topology.md §2` — the 3 axis enumerations
3. `references/intent-topology.md §4` — the 7 habitable cells v1
4. `references/runtime-host-dag.md §2` — the (delivery, nature) → host table
5. `references/skill-vs-agent-discriminators.md §2` — the 4 creator-facing questions
6. `references/composition-anatomy.md §5` — GAP-COMPOSITION-1 + v2 orphan cells
7. `config.yaml → routing.common.intent_topology_enums` — canonical enum authority
8. `config.yaml → routing.{type}.intent_topology` — per-type legal combinations

Also scan for scout reports: `Glob workspace/scout-*.md`. If found, extract the Section 5
recommendation and stage it — it feeds Step 1 (verb-family classification context) and
Step 9 (cell ranking boost) in capability-matrix §2.

### The 12 Steps — Express Mode Fast Path

In Express mode, the walk is not interactive — it is a **defaults lookup** that produces
the same `intent_declaration` schema as Guided. The creator already declared the form
via sub-command; Express fills in every field from `config.yaml routing.{type}.intent_topology`
and records `defaults_applied` for every field that fell back to a type default.

| Step | Express behavior |
|---|---|
| 1 PARSE_INTENT | Skip — set `engine_parsed.verb_family` from type → nature mapping in `config.yaml routing.{type}.intent_topology.archetype_to_nature_mapping` (agent) or from type defaults (skill, minds, squad→`coordinate_X`, etc). Set `creator_said: "(express mode)"`. For squad: also load `discovery-questions.md § Squads` and ask archetype question (Q1) even in Express — archetype determines template shape. |
| 2 APPLY_CONTINUITY_TEST | Derive from `routing.{type}.intent_topology.delivery_mechanism_default`. `ambient_*` or `invoked_slash_command` → `parent`. `invoked_task_spawn` → `isolated`. |
| 3 APPLY_INVOCATION_TEST | Read `creator.intent_profile.usage_frequency_expectation`. Default `weekly` if absent + record `defaults_applied: [usage_frequency_expectation]`. |
| 4 APPLY_POLLUTION_TEST | Set `safe` by default (Express creators have already decided). Only `pollutes` if type is `agent` + flag `--adviser`. |
| 5 APPLY_OUTPUT_TEST | Derive: `skill` → `amplified_reasoning`. `agent` → `structured_report`. `minds` → `structured_report`. `squad` → `structured_report` with handoff trail. |
| 6 RESOLVE_DEPTH | Read sub-type flag: `--procedural` → procedural. `--advisory` → advisory. `--cognitive` → cognitive. If no flag, use `routing.{type}.intent_topology.cognitive_depth_default`. For cognitive, **skip the justification gate** — Express creators are trusted. |
| 7 RESOLVE_NATURE | Read `routing.{type}.intent_topology.operational_nature_default` OR archetype mapping for agents. |
| 8 DERIVE_HOST | Read `references/runtime-host-dag.md §2` table. Use the pair `(delivery, nature)` computed above. Write `engine_parsed.host_set`. |
| 9 LOOKUP_CANONICAL_CELL | Lookup `(delivery, nature, depth)` in `references/intent-topology.md §4`. Single match → use it. Zero match → fall through to Section 1 legacy tree (Contract C4). |
| 10 PROPOSE_FORM | Set `proposed_form` from `matched_cell.canonical_form`. Set `creator_choice: accepted` (Express means the creator already chose). Skip the rationale + alternatives output — Express is silent unless Stage 0 later surfaces drift. |
| 11 RECORD_DECISION | Write the full `intent_declaration` block to `.meta.yaml`. Null-safe discipline (Contract C9): every field populated, `mode_switches: []`. |
| 12 APPEND_TO_HISTORY | Append to `STATE.yaml decisions_history`. Scaffold proceeds. |

**Post-scaffold in Express:** `/validate --stage=0` runs automatically on scaffold completion
in Express mode. If the scaffolded files diverge from the declared triple (e.g., a
`--procedural` skill's scaffold includes a cognitive-core.md reference by accident), Stage 0
surfaces the drift as a coherence warning. Warning, never error. The creator can override.

### The 12 Steps — Guided Mode Walk

In Guided mode, the walk is interactive. The Engine asks the creator to express intent in
natural language (Step 1), reads `creator.intent_profile` for the 5 downstream fields,
derives everything else, lookups the cell, proposes the form, and lets the creator confirm
or override. Max **2 AskUserQuestion calls** in the happy path: one at Step 1 (verb family)
and one at Step 10 (confirm proposal). A third call fires only if Step 6 downgrades
cognitive → advisory (the creator is given a chance to justify).

#### Step 1 — PARSE_INTENT (interactive)

**Ask:**

```
O que sua ferramenta deve FAZER quando alguém a usar?

  1. FAZER — executa, transforma, produz um output concreto          → do_X
  2. PENSAR — aconselha, analisa, emite julgamento                    → advise_on_X
  3. COORDENAR — roteia outras ferramentas em sequência               → coordinate_X
  4. OBSERVAR — nota padrões sem interromper o creator                → observe_X
  5. IMPOR — garante ou bloqueia regras                               → enforce_X
  6. REAGIR — dispara automaticamente quando algo acontece            → react_to_X
  7. Não sei ainda — me ajude a descobrir                             → /scout
```

(Localized to `creator.language`. Localization catalog lives in `config.yaml routing.common` —
see `references/locale-adaptive-clause.md §3`.)

**Map answer to `verb_family`:** 1→do_X, 2→advise_on_X, 3→coordinate_X, 4→observe_X,
5→enforce_X, 6→react_to_X, 7→`unroutable` with fall-through to `/scout` suggestion.

**Ambiguity handling (only if Step 1 answer is plain text instead of option):** parse the
creator's free-text input against `capability-matrix.md §3 Step 1` canonical phrasings.
If two verb families match (*"review my code and fix the issues"* = advise + do), ask ONE
follow-up: *"Você quer DUAS ferramentas que trabalham juntas (revisar e corrigir), ou UMA
que faz as duas coisas?"* — two separate forges (one advise, one do) vs. composed system.
Never ask more than one clarifying question at Step 1.

**Preserve:** the creator's verbatim answer in `creator_said`.

#### Step 2 — APPLY_CONTINUITY_TEST (silent, reads creator.yaml)

No question. Read `creator.intent_profile.working_rhythm` + `creator.intent_profile.domain_depth`.
Apply the rules in `capability-matrix.md §3 Step 2`. Output `continuity_bias ∈ {parent, isolated, unclear}`.

If either `intent_profile` field is missing, apply the declared default (`working_rhythm: hybrid`)
and record `defaults_applied: [working_rhythm]`.

#### Step 3 — APPLY_INVOCATION_TEST (silent)

Read `creator.intent_profile.usage_frequency_expectation`. Apply `capability-matrix.md §3 Step 3`
mapping. Output `invocation_mode ∈ {remembered, needs_auto}`. `monthly`/`occasional` forces
`ambient_path_scoped` in Step 8 tiebreaking.

#### Step 4 — APPLY_POLLUTION_TEST (silent, derived)

Read `verb_family` + `continuity_bias`. Apply `capability-matrix.md §3 Step 4` table.
Output `pollution_risk ∈ {pollutes, safe}` + host-axis override for Step 8 if pollutes.

#### Step 5 — APPLY_OUTPUT_TEST (silent, derived)

Read `verb_family` + `continuity_bias`. Apply `capability-matrix.md §3 Step 5` table.
Output `output_shape ∈ {amplified_reasoning, structured_report}`.

#### Step 6 — RESOLVE_DEPTH (silent with escalation gate)

Read `creator.intent_profile.maintenance_appetite` + `domain_depth` + `verb_family`.
Apply the cap rules in `capability-matrix.md §3 Step 6`:

- `fast_and_simple` → cap at `procedural` or `advisory`. Cognitive denied silently.
- `balanced` → prefer `advisory`, allow `cognitive` IF justification gate passes.
- `deep_and_slow` → allow `cognitive` IF justification gate passes.

**Cognitive justification gate (only fires if depth candidate is `cognitive`):**

Check for 3 conditions. If any is missing, downgrade to `advisory` and record the downgrade
with the missing condition named.

1. **Singularity markers** — at least 3 concrete markers specific to this cognition (named
   patterns of thought, declared failure modes, specific domain anchors).
2. **Named cognitive flow** — a 3-to-6 step cognitive sequence the mind runs.
3. **Concrete reasoning patterns** — at least 3 patterns with specific triggers.

If any missing, ask ONE AskUserQuestion with 2 options: *"Fornecer a arquitetura cognitiva
agora"* (creator provides inline) or *"Continuar como mind advisory"* (accept downgrade).
This is the only AskUserQuestion in the walk besides Steps 1 and 10.

#### Step 7 — RESOLVE_NATURE (silent, derived)

Read `verb_family`. Apply `capability-matrix.md §3 Step 7` table. Output `nature ∈ {executor, advisor, orchestrator, observer}`.

#### Step 8 — DERIVE_HOST (silent, computed)

Read the `(delivery, nature)` pair accumulated through Steps 2-7. Apply the tiebreaker:

- `pollution_risk == pollutes` → force `invoked_task_spawn` regardless of earlier biases.
- `invocation_mode == needs_auto` → force `ambient_path_scoped`.
- Otherwise → pick `invoked_slash_command` as primary + offer `ambient_path_scoped` as
  secondary at Step 10.

Lookup `(delivery, nature)` in `references/runtime-host-dag.md §2`. Write `engine_parsed.host_set`.

#### Step 9 — LOOKUP_CANONICAL_CELL (silent, lookup)

Lookup `(delivery, nature, depth)` in `references/intent-topology.md §4` (the 7 habitable
cells). Apply ranking rules from `capability-matrix.md §3 Step 9`:

- **1 match** → use it. Proceed to Step 10.
- **2+ matches** → rank by `target_audience` + `usage_frequency_expectation`. Top cell is
  primary. Up to 2 alternatives preserved for Step 10 proposal.
- **0 matches** → set `unroutable: true` + `unroutable_reason` from the five values
  (`no_habitable_cell`, `v2_cell_deferred`, `blocked_by_composition_gap`, `ambiguous_between_cells`,
  `explicit_legacy_router`). Fall through to **Section 1 legacy tree below**. The creator
  is NEVER blocked (Contract C4). Before fall-through, check
  `references/intent-topology.md §5` — if the triple matches a deferred v2 cell, record
  the cell name in `unroutable_reason` details and show the creator why it is deferred
  before entering legacy mode.

If `unroutable_reason == blocked_by_composition_gap`, record `unroutable_gap_id` from
`references/composition-anatomy.md §5` (currently only `GAP-COMPOSITION-1`).

**Longitudinal ranking boost (decisions_history read-side).**

When 2+ cells match, consult `STATE.yaml → decisions_history` (the per-creator longitudinal
log written by Step 12) to apply a calibrated ranking boost based on accumulated
retrospective verdicts. The boost is grounded in the creator's own forge outcomes — never
cross-creator (Contract C8 — per-creator calibration only).

Procedure:

1. Read `STATE.yaml → decisions_history`. Filter to entries where
   `engine_proposal.cell_id == candidate_cell_id` AND `retrospective_verdict == "correct"`.
2. For each candidate cell in the ranking, count the filtered entries: call this
   `verdict_boost_count`.
3. Apply boost: `final_score = base_score + (verdict_boost_count × 0.5)`, capped at
   `base_score + 2.0` to prevent runaway dominance after many correct verdicts for one cell.
4. Re-rank using `final_score`. The top cell after the boost is the primary proposal; up to
   2 alternatives preserved.
5. Record in `intent_declaration.discriminators_applied` the marker `longitudinal_boost`
   if any cell's rank changed due to the boost. This is auditable evidence the loop fired.

**Calibration tier** (derived once per session, read by Step 10 for tone):

| Accumulated state | Tier | Step 10 proposal tone |
|---|---|---|
| ≥5 correct verdicts across all cells | HIGH | Assertive. *"Based on your pattern, this is a {form}."* + 1 alternative. |
| ≥3 `wrong_*` verdicts across all cells | MODERATE | Humble. *"I've proposed wrong forms for you a few times — let me show you alternatives."* + 3 alternatives + explicit prompt: *"Can you tell me what made the previous proposals wrong? I'll use that to calibrate."* |
| <3 total retrospective verdicts captured | LOW | Learning. *"I'm still learning your patterns."* + 2-3 alternatives equally weighted. |

The tier is computed once at Step 9 and cached for Step 10 — the two steps share the tier
without re-reading `decisions_history`. The calibration caps from `capability-matrix.md §6.3`
apply: HIGH confidence never removes the override affordance in Step 10. The proposal is
always a suggestion, never a command (Constitutional Clause II — Separation of Production
and Judgment).

**Degradation.** If `STATE.yaml decisions_history` is empty (new creator, first forge) OR
the schema stub is present but contains zero entries, skip the boost entirely and use base
scores. This is the expected state for every creator's first forge; the boost activates
gradually as retrospective verdicts accumulate via the 30-day `/status` prompt (loop closure
point 4 in `capability-matrix.md §6.2`).

**Recent-miscalibration override.**

Before caching the calibration tier, apply a short-horizon correction that protects the
Creator from the Engine sounding over-confident right after it got something wrong recently.
The global tier (computed above) is a rolling average across the creator's entire forge
history; a creator at HIGH tier who just had two wrong retrospectives in the last 30 days
deserves a humble tone on the next proposal, not assertiveness. The override reads
`STATE.yaml → decisions_history` with a temporal filter on `retrospective_captured_at`
and counts recent wrong verdicts.

The formal verdict signal lives in `decisions_history` only. `creator-memory.yaml` stays
clean of verdict duplication — the two stocks have different jobs (decisions_history =
formal decisions and retrospective verdicts; creator-memory = emotional/contextual events
like first_forge, first_publish, milestones).

**Why 30 days?** Retrospective verdicts are captured by the 30-day retrospective prompt
in `/status` (see `references/capability-matrix.md §6.3`). A 7d window would almost never
contain captured verdicts because verdicts trail forges by 30 days minimum. A 30d window
on `retrospective_captured_at` (the moment of capture, not the moment of forge) reads
"of the verdicts collected in the last month, how many went wrong?" — which is the honest
short-horizon signal this override is after.

Procedure:

1. Read `STATE.yaml → decisions_history`. If absent, empty, or contains zero entries with
   a non-null `retrospective_captured_at`, skip the override (not enough data). Use the
   tier computed above.
2. Filter entries where `retrospective_captured_at >= now - 30 days` (parse ISO-8601 UTC).
   Null `retrospective_captured_at` entries are excluded — they have not been retrospected
   yet, so they cannot signal miscalibration.
3. Count entries in the filtered set where `retrospective_verdict ∈ {wrong_form, wrong_depth,
   wrong_cell}`.
4. If count ≥ 2: force tier = MODERATE. Record in `intent_declaration.discriminators_applied`
   the marker `recent_miscal_override` — auditable evidence that the override fired.
5. Otherwise: keep the tier from the global computation.

**Voice implication.** When the override fires, Step 10's proposal tone is the humble variant
from the MODERATE row, regardless of how many correct verdicts accumulated historically.
The Engine says, in effect, *"I know I've been right a lot — but I just got two wrong in
the last month, and I'm paying attention to that."* That is the felt level of self-correction
P10 Touch Integrity demands. Trust compounds on admitted imperfection, not on projected
infallibility.

**Degradation for the override itself.** If `STATE.yaml` is unreadable (YAML parse error),
log to stderr and skip the override silently — never crash the forge. If `decisions_history`
exists but the schema differs from the current reader (e.g., `retrospective_captured_at`
field is absent on every entry), skip the override silently and surface a one-line
Engine-fault note at the end of Step 10's proposal:
> *"(decisions_history temporal schema drift detected — tone calibration fell back to global tier.)"*

This makes the override observable without blocking the Creator's flow.

#### Step 10 — PROPOSE_FORM (interactive)

Format the proposal in creator.language:

```
Proposta: {canonical_form from matched_cell}
Porquê: {one-sentence rationale naming the discriminators that produced the match}
Alternativas:
  1. {alt_cell_1 canonical_form} — {one-line reason to prefer}
  2. {alt_cell_2 canonical_form} — {one-line reason to prefer}
Override: Você pode escolher outra forma se não for isso que você quer.
```

Then ask:

```
A proposta acima está correta?

  1. Sim, proceder                             → creator_choice: accepted
  2. Usar alternativa 1                        → creator_choice: overridden, override_to: alt_1
  3. Usar alternativa 2                        → creator_choice: overridden, override_to: alt_2
  4. Outra forma (me diga qual e por quê)      → creator_choice: overridden, override_to: {input}, override_reason: {input}
```

**Invisibility audit** (only if `target_audience ∈ {marketplace_public, hybrid}`): the
proposal text is checked against `scripts/codex-drift-check.py INVISIBILITY_PATTERN` before
being shown. If internal vocabulary (substrate filenames, author names, acronyms) would leak,
replace with archetype descriptors before display.

**Tool pool defaults** (read `creator.intent_profile.external_dependency_tolerance`): set
scaffold defaults for MCP references + external API calls. Creator can override at /fill time.

#### Step 11 — RECORD_DECISION (silent, write)

Write the full 19-field `intent_declaration` block to `.meta.yaml`. Every field populated;
null-safe (Contract C9). Record `captured_at` as ISO timestamp. Record `mode: guided`.
Record `discriminators_applied` as the subset of `[continuity, invocation, pollution, output, depth]`
that actually fired (not just defaults).

Atomic write (Contract C5): the algorithm does not report `forge_ready` until this write succeeds.

**Seed creator-memory `first_forge` event (silent, idempotent).**

After the `.meta.yaml` write above succeeds, check whether this is the Creator's first
forge ever and, if so, append a `first_forge` event to `creator-memory.yaml`. The memory
layer only feels alive when writers and readers match — this writer is the first half of
the pairing that `/status` Ritual of Return Layer 2 reads.

Procedure:

1. Read `creator-memory.yaml`. If the file is absent or the schema is malformed, skip the
   seeding silently — Phase 5b of `/onboard` is responsible for creating the file, and
   this writer is secondary. Never fabricate the file from /create.
2. Scan `events[]` for any entry with `type == "first_forge"`. If one exists, skip — this
   is idempotent. A Creator who has forged before does not re-trigger the first_forge
   marker, even if /create is invoked from a different product.
3. If no `first_forge` event exists, append:
   ```yaml
   - date: "{ISO-8601 now UTC}"
     type: first_forge
     slug: "{new product slug}"
     note: "First forge — cell={matched_cell.cell_id or 'legacy_fallback'}, form={proposed_form}"
   ```
4. Validate the updated file by running `python scripts/creator-memory-validate.py`. If
   validation fails, roll back the append (the in-memory state is unchanged; the intent
   we did NOT write is gone) and surface an Engine-fault voice line at the end of
   Step 12's output:
   > *"(Memory layer — failed to seed first_forge event. The forge itself is safe; only the memory echo is missing.)"*
   Never block the forge for a memory-layer failure. The forge is the product; the memory
   is the continuity layer — the former must never be held hostage to the latter.

**Voice implication.** This write is silent infrastructure (same register as Phase 5b of
/onboard). The Creator does not see a "first_forge recorded" line. The payoff arrives on
the *next* session: the Ritual of Return Layer 2 in `/status` can surface a grounded
memory echo like *"Remember: on {date} you forged your first product — {slug}. It is now
{state}."* Without this writer, that line never fires, and the memory layer is a
stock-with-no-inflow.

#### Step 12 — APPEND_TO_HISTORY (silent, write)

Append a new entry to `STATE.yaml decisions_history` per `capability-matrix.md §6.1 schema`.
The entry records `forge_completed: false`, `published: false`, `outcome_30d: null`,
`retrospective_verdict: null`. These fields are updated by later pipeline stages.

Atomic write (Contract C5): if this write fails, the `intent_declaration` from Step 11
is kept but the session announces the history-append failure and asks the creator
whether to retry or continue without longitudinal tracking (creator's choice is final).

### Transition Protocol (mid-walk Express↔Guided)

Per `capability-matrix.md §5`. Triggers:

**Express → Guided (escalation):** WH-question during Express, explicit hesitation phrases
(PT: "não tenho certeza", "espera", "como assim"; EN: "wait", "not sure", "what does this mean"),
or double rejection. Action: drop to Guided at the current step, re-run from there, announce
in creator.language, append `mode_switch` entry.

**Guided → Express (shortcut):** creator types `--express`, `--autonomous`, or natural
escape phrases (PT: "pode decidir", "você escolhe", "tanto faz"; EN: "just pick", "you choose").
OR fluency detection: 2 consecutive gates without hesitation + creator is advanced/expert.
Action: apply defaults for remaining steps, announce, append `mode_switch`.

Invariants: max 2 switches per product, transitions never silent, schema identical across modes.

### Fall-Through to Legacy (Contract C4)

When Step 9 returns `unroutable`, Section 1 below runs. The creator experiences a seamless
handoff: "A gente descobriu algo que ainda não tem caminho direto aqui. Vou te mostrar as
opções tradicionais." Legacy Q1/Q2/Q3 runs normally, scaffold proceeds, and `intent_declaration`
is written with `unroutable: true` + the appropriate `unroutable_reason`. The creator is
never blocked; the marker accumulates in `decisions_history` for longitudinal learning.

---

## SECTION 1: LEGACY DECISION TREE (fallback when discovery returns unroutable)

**Fall-through role.** This section is the fall-through used when the Section 0 discovery
walk returns `unroutable` or when the creator explicitly picks "I don't know yet" at Step 1.
It is preserved verbatim to guarantee that every creator still has a forge path, even when
discovery mode cannot route cleanly. Creators in Express mode who want this tree explicitly
can invoke it with `--legacy-router`.

### LEGACY FALLBACK WRITE PROTOCOL

Every forge that completes via Section 1 MUST write a minimal `intent_declaration` block
to `.meta.yaml` AND append a minimal `decisions_history` entry to `STATE.yaml`. This is
not optional — Contract C6 (Dual-Mode Data Contract Identical) requires that Section 1
forges honor the same schema as Section 0 forges, differing only in the `mode` field and
the `unroutable` + `unroutable_reason` markers. Without this protocol, legacy-router forges
would be invisible to `/validate` Stage 0, to the intelligence layer, to the longitudinal
feedback loop, and to the v2→v1 promotion queue — creating a two-tier product population
that silently undermines the Engine's self-calibration.

**Trigger condition.** This protocol runs whenever Section 1 resolves to a concrete product
type (skill, agent, squad, workflow, minds, system, bundle, claude-md, hooks, statusline,
design-system, output-style, application) via the decision tree below OR via the level-based
menu OR via scout-aware routing — regardless of which Q1/Q2/Q3 branch was taken.

**What to write in `.meta.yaml intent_declaration`:**

```yaml
intent_declaration:
  captured_at: "{ISO-8601 timestamp}"
  creator_said: "{verbatim text of creator's Q1 answer, or '(legacy router menu)' if menu path}"
  mode: "legacy_fallback"        # NOT 'express' — a distinct third value
  mode_switches: []              # always empty in legacy fallback
  language: "{from creator.yaml → creator.language, fallback to 'en'}"
  scout_source: "{scout-*.md path if scout-aware routing fired, else null}"

  engine_parsed:
    verb_family: null            # legacy router does not classify verb family
    continuity_bias: null        # not computed in legacy path
    invocation_mode: null
    pollution_risk: null
    output_shape: null
    depth: null                  # filled with type default only if type is skill or minds
    nature: null                 # derived from type: skill→executor, minds→advisor, squad→orchestrator, hooks→react_to, claude-md→governor, etc.
    delivery_mechanism: null     # derived from type: skill→invoked_slash_command, minds→invoked_task_spawn, claude-md→ambient_constitutional, hooks→reflex_hook_binding, etc.
    host_set: []                 # derived from (delivery, nature) per runtime-host-dag.md §2

  matched_cell: null             # legacy router does not match cells
  ranked_alternatives: []

  proposed_form: "{resolved product type from legacy tree, e.g. 'skill', 'minds_advisory', 'squad'}"
  creator_choice: "accepted"     # the creator walked the tree to arrive here — that IS the choice
  override_to: null
  override_reason: null

  unroutable: true               # load-bearing — this forge bypassed the canonical topology
  unroutable_reason: "{one of: no_habitable_cell | v2_cell_deferred | blocked_by_composition_gap | ambiguous_between_cells | explicit_legacy_router}"
  unroutable_gap_id: null        # or GAP-COMPOSITION-1 if blocked_by_composition_gap

  discriminators_applied: []     # empty in legacy path
  defaults_applied: ["verb_family", "continuity_bias", "invocation_mode", "pollution_risk", "output_shape", "depth"]
```

**Derivation table for `engine_parsed` fields in legacy mode** (nature + delivery_mechanism
can be derived from the resolved type even though the walk was skipped — this is the minimum
information needed for `/validate` Stage 0 coherence checks and for `/fill` natureza-aware
walk in W4.1):

| Resolved type | nature | delivery_mechanism | depth default |
|---|---|---|---|
| skill | executor | invoked_slash_command | procedural |
| agent | advisor | invoked_task_spawn | advisory |
| minds (advisory) | advisor | invoked_task_spawn | advisory |
| minds (cognitive) | advisor | invoked_task_spawn | cognitive |
| squad | orchestrator | invoked_task_spawn | advisory |
| workflow | orchestrator | invoked_slash_command | procedural |
| system | orchestrator | composed_system | procedural |
| bundle | orchestrator | composed_system | procedural |
| hooks | observer | reflex_hook_binding | procedural |
| claude-md | observer | ambient_constitutional | procedural |
| statusline | observer | ambient_path_scoped | procedural |
| design-system | executor | ambient_path_scoped | procedural |
| output-style | observer | ambient_constitutional | procedural |
| application | executor | composed_system | procedural |

Host derivation follows `references/runtime-host-dag.md §2` using the derived
(delivery, nature) pair.

**What to append to `STATE.yaml decisions_history`:**

```yaml
- date: "{ISO-8601 timestamp}"
  slug: "{new product slug}"
  creator_intent: "{creator's Q1 verbatim or '(legacy router menu)'}"
  mode: "legacy_fallback"
  mode_switches: []
  scout_source: "{scout-*.md if scout-aware routing fired, else null}"
  engine_proposal:
    cell_id: null               # no cell matched
    form: "{resolved type}"
    rationale: "legacy router Q{1|2|3} branch: {branch name}"
    alternatives: []
  unroutable: true
  unroutable_reason: "{same as intent_declaration.unroutable_reason}"
  unroutable_gap_id: null       # or GAP-COMPOSITION-1
  creator_choice: "accepted"
  override_to: null
  override_reason: null
  forge_completed: false        # updated by /validate pass
  published: false              # updated by /publish
  outcome_30d:
    install_count: null
    user_rating: null
    creator_self_uses: null
    reported_issues: []
  retrospective_verdict: null
  retrospective_captured_at: null
```

**Atomicity (Contract C5).** Both writes (`.meta.yaml intent_declaration` + `STATE.yaml
decisions_history` append) must succeed before the scaffold proceeds. If either fails,
roll back the scaffold directory and announce the failure. Legacy forges must not produce
half-instrumented products — that would be a silent two-tier population.

**Cell annotation (creator-visible).** When a legacy branch resolves, announce to the creator
in creator.language: *"Forjado como {resolved_type} via roteador tradicional. Este forge
alimentará o queue de promoção v2→v1 (capability-matrix §6.4) se houver repetidos verdicts
`correct` nos próximos 30 dias."* Keep it one line. The creator learns their forge contributes
to future topology evolution without being overwhelmed.

### Scout-Aware Routing (check FIRST, before any menu)

1. Glob `workspace/scout-*.md` for existing scout reports
2. If one or more reports exist, read the most recent and extract Section 5 (Setup Recommendation)
3. Present scout-informed options:
   ```
   I found a scout report for "{domain}" ({date}).
   It recommends {N} products:

     1. {name} ({type}) — {purpose}
     2. {name} ({type}) — {purpose}
     ...

   Build from this recommendation? Pick a number, or:
   - "all" → scaffold all recommended products in sequence
   - "skip" → ignore scout and choose manually
   - "/scout {new-domain}" → research a different domain first
   ```
4. If creator picks a product from the recommendation:
   - Pre-populate slug, type, description, and MCS target from scout report
   - Load scout report as context during discovery questions (Step 2)
   - Note in `.meta.yaml`: `scout_source: "scout-{slug}.md"` for traceability
5. If "all" → scaffold each product sequentially, pausing after each for confirmation.
   **Each** scaffold gets `scout_source: "scout-{slug}.md"` in its `.meta.yaml` — traceability must be per-product, not just the first.

### No Scout Report + No Argument: Level-Based Menu

**If creator.yaml exists AND technical_level is advanced/expert**, show the direct menu.

**CRITICAL:** Load `references/ux-vocabulary.md` → Product Types table. If `creator.profile.type` is NOT `developer`, use the user-facing names and one-liners from ux-vocabulary.md instead of the internal names below. The menu adapts to who is reading it.

**Developer menu** (profile.type = developer):
```
What do you want to create?

  1. skill        — A reusable capability Claude can run
  2. agent        — A specialized persona with domain expertise
  3. squad        — A team of coordinated agents
  4. workflow     — An automated multi-step process
  5. ds           — A design system (tokens, components, exports)
  6. claude-md    — A project-specific CLAUDE.md configuration
  7. app          — A deployable application
  8. system       — A composite system (skills + agents + workflows)
  9. bundle       — A curated collection of products
  10. statusline  — A Claude Code status bar configuration
  11. hooks       — Event-driven automations for Claude Code
  12. minds        — A domain expertise profile
  13. output-style — Custom output formatting and rendering rules

Enter number or name:
```

**Non-developer menu** (all other profile.type values):
```
What do you want to create?

  1. Tool              — Adds a new capability to Claude Code
  2. Agent             — A specialized persona with domain expertise
  3. Team              — Multiple agents working together
  4. Guided Process    — Step-by-step automation
  5. Design Kit        — Visual design language and components
  6. Project Rules     — Smart defaults for your project type
  7. Application       — Deployable software
  8. Complete Setup    — Full working environment
  9. Collection        — Curated set of tools that work together
  10. Status Bar       — Live info at the bottom of your screen
  11. Auto-Actions     — Things that happen automatically
  12. Advisor / Mind   — An expert you can consult
  13. Response Style   — Changes how Claude communicates

Pick a number:
```

**If creator is beginner/intermediate OR type is domain-expert/operator/marketer**, use the Decision Tree below.

### Decision Tree: Q1 → Q2 → Q3 Routing

Ask via AskUserQuestion (single select):

```
Q1: What does your product need to do?

  1. DO something        — execute tasks, run processes, produce output
  2. THINK about something — advise, analyze, reason, consult
  3. GOVERN something    — enforce rules, react to events, set standards
  4. EVERYTHING          — full domain infrastructure or an app
  5. LOOK / FORMAT       — visual design, output formatting, status display
  6. I don't know yet    — help me figure it out
```

**DO →** Ask Q2:
```
Q2: Is it a single action or a sequence of steps?

  1. Single action
  2. Sequence of steps
  3. Automatic reaction to an event
```
- Single action → Q3: "Does it need judgment to decide WHAT to do, or just execution?"
  - Needs judgment → **agent** ("An agent can assess context and decide how to act.")
  - Just execution → **skill** ("A skill runs the same way every time — focused and reliable.")
- Sequence → **workflow** ("A workflow orchestrates steps in order — like a recipe.")
- Automatic reaction → **hooks** ("Hooks fire automatically when Claude does something.")

**THINK →** Ask Q2:
```
Q2: How many perspectives does it need?

  1. One deep perspective (a specialist advisor)
  2. Multiple perspectives that collaborate
```
- One → Q3: "Does it also need to ACT (do things), or just advise?"
  - Also acts → **agent** ("An agent thinks AND does — judgment plus action.")
  - Just advises → **minds** (depth: advisory by default — fast, ~200 lines)

    **Depth upsell (post-scaffold, not pre-scaffold):** After advisory scaffold is generated, offer. **CRITICAL:** Adapt language to profile.type.

    For developers:
    ```
    Scaffold ready. Want to upgrade this to a deeper cognitive mind?

      1. Keep as advisory mind (done — run /fill to add content)
      2. Upgrade to cognitive mind (5 layers, ~1000 lines, full reasoning engine)
      3. Build from genius profile (da-vinci, etc. — pre-populated cognitive architecture)
    ```

    For non-developers:
    ```
    Your advisor is ready. How deep should it go?

      1. Keep it simple — a quick expert you can ask questions (done — /fill to add your expertise)
      2. Make it deep — a specialist that reasons through problems step by step (more setup, much more powerful)
      3. Start from a famous thinker — pre-built expert personality you customize (da Vinci, etc.)
    ```
    - Option 1: proceed with advisory scaffold as-is
    - Option 2: replace scaffold with cognitive template from `templates/minds/cognitive/`, update .meta.yaml `minds_depth: cognitive`
      - Then ask sub-type: "What's the source?" → Self (scan environment) or Domain (suggest /scout)
    - Option 3: load from genius library `templates/genius-library/{name}/profile.yaml`, pre-populate C1-C7 strands, update .meta.yaml `minds_depth: cognitive, minds_sub_type: genius, genius_profile: "{name}"`

    **Direct shortcuts (skip decision tree entirely):**
    - `/create minds --cognitive` → scaffold cognitive directly
    - `/create minds --genius` → show genius library directly
    - `/create minds --genius da-vinci` → load da-vinci profile directly
    - If creator says "cognitive mind", "genius mind", "da-vinci mind", "self mind" → route directly without Q4

- Multiple → **squad** ("A squad is a team of specialists that collaborate on complex problems.")

**GOVERN →** Ask Q2:
```
Q2: Should the rules be always active or triggered by events?

  1. Always active — every session, no exception
  2. Triggered by specific events
```
- Always active → **claude-md** ("A CLAUDE.md is constitutional — rules that apply every single time.")
- Event-triggered → **hooks** ("Hooks watch for events and react automatically.")

**EVERYTHING →** Ask Q2:
```
Q2: Does this need a dedicated project, or are you extending your current setup?

  1. Dedicated project (its own directory, config, infrastructure)
  2. Extensions to my current setup (add capabilities)
  3. An application (deployable software, not a Claude product)
```
- Dedicated → **system** ("A system is a complete organism — skills, agents, rules, all composed.")
- Extensions → **bundle** ("A bundle packages products together for joint install.")
- Application → **application** ("An application is deployable software — code, not prompts.")

**APPEARANCE / FORMAT →**
```
Q2: What aspect of appearance or formatting?

  1. Visual consistency across UIs (colors, typography, components)
  2. How Claude formats its output (tone, structure, rendering)
  3. Always-visible info in the status bar
```
- Visual consistency → **design-system** ("A design system defines visual DNA — tokens, components, exports.")
- Output formatting → **output-style** ("An output style controls how Claude presents its responses.")
- Status bar → **statusline** ("A statusline shows ambient info without asking — always visible.")

**DON'T KNOW →**
```
No problem. Let me help:

  1. Describe what you're trying to achieve → I'll recommend a type
  2. /scout {domain} → I'll research the domain and recommend products
  3. /explore → Browse what others have built for inspiration
```
If creator describes their goal: parse intent using these patterns:
- "do X" / "automate X" → route to DO branch
- "think about X" / "advise on X" → route to THINK branch
- "enforce X" / "rules for X" → route to GOVERN branch
- Still unclear → suggest `/scout` as next step

After the tree resolves to a type, explain in one sentence why it fits, then proceed to the standard flow (exemplar preview → discovery questions → scaffold).

---

## SECTION 2: PER-CATEGORY SCAFFOLD STRUCTURES

**skill:**
```
workspace/{slug}/
├── SKILL.md              # Main skill definition
├── references/           # Domain knowledge
│   └── .gitkeep
├── examples/             # Usage examples (3+ for MCS-2)
│   └── .gitkeep
└── README.md             # Installation and usage
```

**agent:**
```
workspace/{slug}/
├── AGENT.md              # Agent definition + persona
├── identity/             # Persona detail files
│   └── .gitkeep
├── architecture/         # Cognitive architecture docs
│   └── .gitkeep
└── README.md
```

**squad:**
```
workspace/{slug}/
├── SQUAD.md              # Squad orchestrator — routing, coordination, escalation
├── agents/               # Individual agent definitions (min 2 .md files)
│   ├── orchestrator.md   # Traffic chief / coordinator persona
│   └── specialist-1.md   # First specialist (rename per domain)
├── kernel/               # Orchestration intelligence layer
│   ├── orchestration.md  # Orchestration protocol (custom decision cycle)
│   ├── elicitation-engine.yaml  # Progressive elicitation / JtBD discovery
│   └── intelligence-matrix.yaml # Dynamic scoring / workflow assembly
├── minds/                # Cognitive models for mind-clone specialists (optional)
│   └── .gitkeep
├── tasks/                # Granular task definitions with I/O schemas
│   └── task-registry.yaml
├── chains/               # Multi-agent micro-workflows with cadences
│   └── chain-registry.yaml
├── workflows/            # Full pipeline definitions
│   └── primary-workflow.md
├── config/               # Routing and handoff config
│   ├── routing-table.md  # Declarative routing: intent → agent
│   └── handoff-protocol.md # Handoff envelope format + contracts
├── data/                 # Benchmarks, calibration, decision journal
│   └── .gitkeep
├── references/           # Domain knowledge files
│   └── .gitkeep
├── tests/                # Integration test scenarios
│   └── .gitkeep
└── README.md
```

**workflow:**
```
workspace/{slug}/
├── WORKFLOW.md           # Workflow definition
├── steps/                # Individual step definitions
│   └── .gitkeep
├── config/               # Triggers and error handling
│   └── config.yaml
└── README.md
```

**ds (design system):**
```
workspace/{slug}/
├── DESIGN-SYSTEM.md      # Design system definition
├── tokens/               # Design tokens
│   └── .gitkeep
├── components/           # Component definitions
│   └── .gitkeep
├── exports/              # Export format configs
│   └── .gitkeep
└── README.md
```

**claude-md:**
```
workspace/{slug}/
├── CLAUDE.md             # The CLAUDE.md itself
├── rules/                # Modular rule files
│   └── .gitkeep
└── README.md
```

**app:**
```
workspace/{slug}/
├── APPLICATION.md        # Application definition
├── src/                  # Application source
│   └── .gitkeep
├── CLAUDE.md             # AI pair-programming instructions
├── package.json          # or equivalent manifest
└── README.md
```

**system:**
```
workspace/{slug}/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest — components, routing, install target
├── SYSTEM.md             # System definition + composition + routing
├── skills/               # Included skills
│   └── .gitkeep
├── agents/               # Included agents
│   └── .gitkeep
├── hooks/                # Lifecycle hooks (optional)
│   └── .gitkeep
├── references/           # Shared knowledge base
│   └── .gitkeep
├── config/
│   └── routing.yaml      # Component routing rules
└── README.md
```

**bundle:**
```
workspace/{slug}/
├── vault.yaml            # Bundle manifest with includes[] (IS the product)
└── README.md             # What's included, curation rationale
```

**statusline:**
```
workspace/{slug}/
├── statusline.sh             # Shell script (reads JSON stdin, outputs ANSI stdout)
├── settings-fragment.json    # settings.json merge fragment for activation
├── examples/                 # Sample stdin JSON + expected stdout output
│   └── .gitkeep
└── README.md
```

**hooks:**
```
workspace/{slug}/
├── hooks.json            # settings.json fragment (event bindings)
├── scripts/              # Handler scripts
│   └── handler.sh
├── examples/
│   └── .gitkeep
└── README.md
```

**minds (advisory depth):**
```
workspace/{slug}/
├── AGENT.md              # Mind definition (YAML frontmatter + advisory persona)
├── references/           # Domain knowledge
│   └── .gitkeep
├── examples/             # Conversation examples
│   └── .gitkeep
└── README.md
```

**minds (cognitive depth):**
```
workspace/{slug}/
├── AGENT.md                          # Layer 1: Boot (identity, principles, cognitive patterns)
├── references/
│   ├── cognitive-core.md             # Layer 2: Biography, architecture, singularity
│   ├── personality.md                # Layer 3: Behavioral matrix, style, interaction
│   ├── knowledge-base.md            # Layer 4: Domain depth + explicit boundaries
│   └── reasoning-engine.md          # Layer 5: Patterns, models, triggers
├── examples/
│   └── examples.md                   # 3+ interaction examples
└── README.md
```

When scaffolding cognitive depth: load template from `templates/minds/cognitive/` instead of `templates/minds/`. If genius sub-type: also load `templates/genius-library/{name}/profile.yaml` and pre-populate C1-C7 strands in the scaffold. Record in `.meta.yaml`: `minds_depth: cognitive`, `minds_sub_type: self|genius|domain`, and if genius: `genius_profile: "{name}"`.

**output-style:**
```
workspace/{slug}/
├── OUTPUT-STYLE.md       # Style definition (tone, structure, rendering rules)
├── examples/             # Before/after examples of styled output
│   └── .gitkeep
└── README.md
```

---

## SECTION 3: PREFILLING STRATEGY

When generating scaffold files, prefill key sections to give creators a running start:

**SKILL.md prefill:**
```markdown
# {Product Name}

> {One-liner from discovery answer}

**Version:** 1.0.0
**Category:** Skills
**Author:** {from creator.yaml}

---

## When to Use

- {Prefilled from discovery question "What problem does this skill solve?"}

## When NOT to Use

- General-purpose tasks that don't require specialized knowledge (use direct prompting instead)

---

## Activation Protocol

Before responding to any invocation:

1. **Load domain knowledge:** Read `references/domain-knowledge.md`
2. **Load exemplars:** Read `examples/examples.md`
3. **Identify user intent:** Parse input for specific request type
```

**README.md prefill:**
```markdown
# {Product Name}

{One-liner from discovery}

## Install

```bash
myclaude install {slug}
```

## Usage

```
/{slug} {example input}
```

## Requirements

- Claude Code >= 1.0.0
```

Prefilling reduces blank-page paralysis and ensures MCS-1 structural compliance from the first moment.
