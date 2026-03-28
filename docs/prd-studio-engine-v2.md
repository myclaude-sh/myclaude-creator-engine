---
document: PRD
product: MyClaude Studio Engine
version: 2.0.1
status: APPROVED FOR BUILD
date: 2026-03-28
base: [Ecosystem Deep Map (89.7%), Cognitive Audit, DNA Extraction (4 systems + Genesis + ECC), Official Anthropic Docs (8/73 pages scraped), Wiring Protocol (28 decisions), v1.1.0 Codebase Audit, CLI Codebase Audit]
decisions: 27 (SE-D1 → SE-D27)
phases: 10 sprints (S0 → S10)
audit: "51-gap audit + Blind-Spot Checklist (26 items)"
validated_by: "Multi-pillar cognitive audit (System Diagnosis + Argument Audit)"
---

# MyClaude Studio Engine — PRD v2.0

> The world's most advanced Claude Code creation studio.
> A self-contained meta-system that prints structural DNA into everything it creates.
> Free. Open Source. State-of-the-art. Made in Brazil.

---

## §0. HOW TO READ THIS PRD

### Routing by Role

| Role | Essential Sections | Can Skip |
|------|-------------------|----------|
| **Builder** (implementing) | §1, §3, §4, §5, §6, §7, §8, §9, §10, §11, §13 | §2 details, §15 |
| **Quality Auditor** | §3, §4, §6, §9, §10, §14, §15 | §7, §11 |
| **Creator** (using the Engine) | §1, §5, §6, §9 | §3 internals, §7, §8 |
| **Product Owner** | §1, §2, §5, §13, §14, §15, §16, §17 | §6 internals |

### Glossary

| Term | Definition |
|------|-----------|
| **Studio Engine** | This system — MyClaude Studio Engine |
| **Creator** | Person using the Studio to create products |
| **Buyer** | Claude Code user who installs products created by the Engine |
| **Product** | Any publishable artifact in 9 categories (skill, agent, squad, workflow, design-system, prompt, claude-md, application, system) |
| **DNA** | Structural DNA — 18 patterns that define state-of-the-art Claude Code products |
| **MCS** | MyClaude Creator Spec — 3-tier quality mapped to DNA compliance |
| **LITE** | Free open-source edition (MIT license) |
| **PRO** | Paid edition installed as add-on via marketplace |
| **vault.yaml** | Product manifest consumed by MyClaude CLI |
| **plugin.json** | Product manifest consumed by Anthropic plugin system |
| **Forge Master** | PRO orchestrator agent |
| **WHY comments** | `<!-- WHY: D{N} — explanation -->` annotations in templates/exemplars, stripped during /package |
| **Tier** | DNA pattern difficulty level (1=Universal, 2=Advanced, 3=Expert) |

### Decision Prefix: `SE-D` (Studio Engine Decision)

Cross-refs: `CE-D` (Creator Engine v1), `WP-` (CONDUIT Wiring Protocol), `D` (marketplace PRD).

---

## §1. VISION & DESIGN AXIOMS

### What It Is

MyClaude Studio Engine is a **self-contained Claude Code system** — a repository that transforms any Claude Code session into a professional creation studio. It is the creative motor of the MyClaude ecosystem.

**Mental model:** "The forge where world-class Claude Code products are born."

### What It Feels Like

- **Empowered** — "I have everything I need"
- **Elevated** — "Everything I create has structural DNA I couldn't achieve alone"
- **Connected** — "I can validate, package, and ship without leaving Claude Code"
- **Independent** — "This works even without the marketplace"

### What It Is NOT

- NOT a scaffolder (it's intelligence + creation + validation + publishing)
- NOT dependent on our products (fully agnostic, zero external refs)
- NOT limited to developers (adapts to any creator persona)
- NOT just for MyClaude marketplace (also supports Anthropic plugin marketplace)
- NOT a single skill (it's a complete meta-system)

### The One-Sentence Objective

> Enable any creator to produce Claude Code products with the structural DNA of state-of-the-art systems — regardless of their technical level.

### Design Axioms (govern ALL decisions)

**SE-AXIOM-1: Value = delta WITH Engine vs WITHOUT Engine.**
If a creator can achieve the same result without the Engine, the Engine failed. Every skill, every template, every validation must provide value the creator CANNOT get from raw Claude Code.

**SE-AXIOM-2: Competition is manual creation.**
A developer writes SKILL.md in 10 minutes. The Engine must make the output SIGNIFICANTLY better, not just DIFFERENTLY structured. If the Engine adds process without proportional value, it destroys adoption.

**SE-AXIOM-3: Skills EXECUTE, they don't INSTRUCT.**
Skills run real checks (glob, grep, YAML parse, file analysis). They don't tell Claude "please check if files exist." They CHECK if files exist.

**SE-AXIOM-4: Preserve knowledge, rebuild execution.**
The v1.1.0 knowledge base (product specs, best practices, references) is strong. The execution layer (skills, agents) is weak. Keep what works, rebuild what doesn't.

**SE-AXIOM-5: The Engine is its own best advertisement.**
If the Engine's own CLAUDE.md, templates, and exemplars aren't state-of-the-art, nothing it creates will be.

### Strategic Position

```
CREATOR ─── STUDIO ENGINE ─── CLI ─── MARKETPLACE ─── BUYER
(expertise)   (forge)        (ship)    (discover)    (install+use)
                │
                └── Also distributes via Anthropic Plugin Marketplace
```

**SE-D1:** The Studio Engine is a SYSTEM, not a collection of loose skills.

**SE-D2:** Self-contained and agnostic. Zero dependencies on our products. Zero references to our squads/agents. The arsenal informed the DESIGN but does not appear at RUNTIME.

**SE-D3:** Our arsenal is build-time only.

---

## §2. BRANDING

| Aspect | Value |
|--------|-------|
| Full name | MyClaude Studio Engine |
| Casual | "the Studio" |
| CLI binary | `myclaude` (lowercase) |
| Marketplace | MyClaude Marketplace / myclaude.sh |
| PRO product name | MyClaude Studio Pro |
| Repo | `myclaude-studio-engine` |
| Never use | "VAULT" in user-facing content |

Capitalization: Always "MyClaude" (capital M, capital C, one word).

---

## §3. STRUCTURAL DNA

### The Meta-Architecture

Every state-of-the-art Claude Code system follows this processing flow. The 18 DNA patterns plug into this architecture:

```
BOOT LAYER
  ├─ Load orchestrator definition (CLAUDE.md / SKILL.md)
  ├─ Load routing rules (config, triage)
  └─ Load core config (principles, confidence schema, anti-patterns)
       │
       │  DNA: D1 (Activation Protocol), D3 (Progressive Disclosure)
       ▼
INPUT TRIAGE
  ├─ Classify request (what is really being asked?)
  ├─ Identify required specialists
  └─ Check preconditions (context loaded? dependencies met?)
       │
       │  DNA: D5 (Question System), D7 (Pre-Execution Gate)
       ▼
ACTIVATION SEQUENCE
  ├─ Route to primary specialist(s)
  ├─ Apply Socratic pressure at handoffs
  ├─ Execute with progressive disclosure
  └─ Collect quality signals
       │
       │  DNA: D9 (Orchestrate Don't Execute), D10 (Handoff Spec),
       │       D11 (Socratic Pressure), D18 (Subagent Isolation)
       ▼
STATE CAPTURE
  ├─ Append to decision log (immutable)
  ├─ Update session state (mutable)
  ├─ Check output against quality gates
  └─ Promote patterns confirmed 2+ times
       │
       │  DNA: D8 (State Persistence), D12 (Compound Memory)
       ▼
SYNTHESIS LAYER
  ├─ Integrate specialist outputs
  ├─ Surface tensions (don't smooth)
  ├─ Apply final validation
  └─ Deposit crystallized insight
       │
       │  DNA: D4 (Quality Gate), D6 (Confidence Signaling)
       ▼
OUTPUT WITH CONFIDENCE
  ├─ Graduate confidence (explicit)
  ├─ Show reasoning chain (not just conclusion)
  ├─ Declare uncertainty
  └─ Suggest next steps
       │
       │  DNA: D13 (Self-Documentation), D14 (Graceful Degradation)
```

The Engine is BUILT on this meta-architecture. Products created BY the Engine inherit it.

### The 18 Patterns in 3 Tiers

#### TIER 1 — UNIVERSAL (6 patterns, every product, every MCS level)

| ID | Pattern | Problem It Solves | Validation Check (/validate) |
|----|---------|------------------|------------------------------|
| D1 | **Activation Protocol** | Product that acts without context = generic output | Grep for activation/protocol section in primary file. Must reference at least 1 file in references/ |
| D2 | **Anti-Pattern Guard** | Without documenting errors, users repeat them | Grep for anti-pattern section. Must contain ≥5 items with description + prevention |
| D3 | **Progressive Disclosure** | Loading everything wastes context | Check references/ dir exists with ≥1 file. Primary file <500 lines. No inline knowledge dumps |
| D4 | **Quality Gate** | Without checkpoint, output quality varies | Grep for quality gate/criteria section with ≥3 verifiable criteria |
| D13 | **Self-Documentation** | Product without README isn't installed | README.md exists with sections: what, install, usage, requirements. Each non-empty |
| D14 | **Graceful Degradation** | Product that breaks silently = distrust | Grep for "when not to use" or degradation handling or error section |

#### TIER 2 — ADVANCED (7 patterns, MCS-2+)

| ID | Pattern | Problem It Solves | Validation Check |
|----|---------|------------------|-----------------|
| D5 | **Question System** | Assumes input = misaligned output | Grep for question/input table or "if missing, ask" pattern |
| D6 | **Confidence Signaling** | Claims without certainty = misleading | Grep for confidence levels, certainty markers, or "high/moderate/low" pattern |
| D7 | **Pre-Execution Gate** | Acts without preconditions = silent failure | Grep for precondition checks or "before executing, verify" pattern |
| D8 | **State Persistence** | No state = zero continuity | Check for state file (.yaml/.json) or state management section |
| D15 | **Testability** | Can't test = can't improve | Grep for test scenarios, examples with expected output, or test section |
| D16 | **Composability** | Conflicts with other products = uninstalled | Check: no hardcoded absolute paths, no common slash command names (/help, /status), relative refs only |
| D17 | **Hook Integration** | Manual steps = missed automation | Check for hooks section in frontmatter OR hooks documentation in README |

#### TIER 3 — EXPERT (5 patterns, MCS-3)

| ID | Pattern | Problem It Solves | Validation Check |
|----|---------|------------------|-----------------|
| D9 | **Orchestrate Don't Execute** | Orchestrator does specialist work = mediocre | Check SQUAD.md/SYSTEM.md routing table. Orchestrator must NOT have domain instructions |
| D10 | **Handoff Specification** | Vague context between agents = cascade degradation | Each agent handoff must specify: what_done, what_decided, what_next_needs |
| D11 | **Socratic Pressure** | Accept first output = inconsistent quality | Check for self-challenge pattern: "what's wrong here?", falsification, counter-argument |
| D12 | **Compound Memory** | No cross-session memory = lost patterns | Check for memory configuration (user/project/local scope) in agent frontmatter |
| D18 | **Subagent Isolation** | No isolation = context bleeding | Check for `context: fork` in skill frontmatter OR agent definition with own context |

### DNA Applicability Matrix

| Pattern | skill | agent | squad | workflow | ds | prompt | claude-md | app | system |
|---------|-------|-------|-------|----------|-----|--------|-----------|-----|--------|
| D1 | **R** | **R** | **R** | **R** | o | **R** | **R** | o | **R** |
| D2 | **R** | **R** | **R** | **R** | **R** | o | **R** | **R** | **R** |
| D3 | **R** | **R** | **R** | o | o | o | **R** | o | **R** |
| D4 | **R** | **R** | **R** | **R** | **R** | **R** | o | **R** | **R** |
| D5 | **R** | **R** | **R** | o | — | o | — | o | **R** |
| D6 | o | **R** | **R** | o | — | o | — | o | **R** |
| D7 | **R** | **R** | **R** | **R** | — | o | o | **R** | **R** |
| D8 | o | **R** | **R** | o | — | — | — | o | **R** |
| D9 | — | — | **R** | — | — | — | — | — | **R** |
| D10 | — | — | **R** | o | — | — | — | — | **R** |
| D11 | o | **R** | **R** | — | — | — | — | — | **R** |
| D12 | — | o | **R** | — | — | — | — | — | **R** |
| D13 | **R** | **R** | **R** | **R** | **R** | **R** | **R** | **R** | **R** |
| D14 | **R** | **R** | **R** | **R** | o | o | o | **R** | **R** |
| D15 | o | **R** | **R** | o | — | o | — | o | **R** |
| D16 | **R** | **R** | **R** | **R** | **R** | **R** | **R** | **R** | **R** |
| D17 | o | o | o | o | — | — | o | o | o |
| D18 | — | — | **R** | — | — | — | — | — | **R** |

`R` = Required for MCS of that tier. `o` = optional bonus. `—` = not applicable.

**SE-D4:** MCS v2 = DNA compliance. 10/18 patterns validated by official Anthropic docs.

**SE-D5:** DNA is superset of Anthropic official best practices.

---

## §4. MCS v2 — SCORING & VALIDATION

### Scoring Formula

```
For each applicable DNA pattern:
  PASS   = 1.0 (pattern fully present and functional)
  PARTIAL = 0.5 (pattern present but incomplete)
  FAIL   = 0.0 (pattern absent or broken)

DNA_SCORE = (Σ pattern_scores / applicable_patterns_count) × 100

STRUCTURAL_SCORE = (files_found / files_expected) × 100
INTEGRITY_SCORE  = (valid_refs / total_refs) × 100  [0 broken refs = 100]

OVERALL = (DNA_SCORE × 0.50) + (STRUCTURAL_SCORE × 0.30) + (INTEGRITY_SCORE × 0.20)
```

### MCS Thresholds

| Level | DNA Requirement | Overall Score | What It Proves |
|-------|----------------|--------------|----------------|
| MCS-1 | Tier 1 PASS (D1,D2,D3,D4,D13,D14) | ≥ 75% | Functional, documented, no broken refs |
| MCS-2 | Tier 1+2 PASS (adds D5-D8,D15-D17) | ≥ 85% | Demonstrates craft and professionalism |
| MCS-3 | Tier 1+2+3 PASS (adds D9-D12,D18) | ≥ 92% | State-of-the-art structural DNA |

### Validation Pipeline (/validate implementation)

```
Stage 1: STRUCTURAL (automated — glob, stat)
  ├─ All required files for product type exist?
  ├─ Primary file (SKILL.md/AGENT.md/etc.) exists?
  ├─ README.md exists?
  ├─ Metadata fields populated? (name, description, version)
  └─ SCORE: files_found / files_expected

Stage 2: INTEGRITY (automated — grep, read)
  ├─ All file paths referenced in .md files actually exist?
  ├─ No placeholder content? (grep: TODO, PLACEHOLDER, lorem, coming soon, GUIDANCE:)
  ├─ YAML/JSON files are syntactically valid? (parse test)
  ├─ No broken relative paths?
  └─ SCORE: valid_refs / total_refs

Stage 3: DNA TIER 1 (automated — grep, glob)
  ├─ D1: Activation protocol section present + references ≥1 file?
  ├─ D2: Anti-patterns section with ≥5 items?
  ├─ D3: references/ dir exists + primary file <500 lines?
  ├─ D4: Quality gate section with ≥3 verifiable criteria?
  ├─ D13: README has what/install/usage/requirements sections?
  ├─ D14: "When NOT to use" or error handling section?
  └─ SCORE: passed / 6

Stage 4: DNA TIER 2 (automated + semi-automated — MCS-2 only)
  ├─ D5: Question system or "if missing, ask" pattern?
  ├─ D6: Confidence markers or certainty levels?
  ├─ D7: Pre-execution checks?
  ├─ D8: State file or persistence section?
  ├─ D15: Test scenarios or expected outputs?
  ├─ D16: No hardcoded paths, no common command names?
  ├─ D17: Hooks section or documentation?
  └─ SCORE: passed / applicable_count

Stage 5: DNA TIER 3 (agent-assisted — MCS-3, PRO only)
  ├─ D9: Orchestrator routing table, no domain instructions?
  ├─ D10: Handoff specs between agents?
  ├─ D11: Self-challenge pattern?
  ├─ D12: Memory configuration?
  ├─ D18: context:fork or subagent isolation?
  └─ SCORE: passed / applicable_count

Stage 6: INTEGRITY VIA CLI (delegates to `myclaude validate`)
  ├─ vault.yaml valid?
  ├─ No secrets in files?
  ├─ File sizes within limits?
  └─ RESULT: pass/fail from CLI

Stage 7: ANTI-COMMODITY (MCS-2+, coaching not blocking)
  ├─ "What domain expertise did the creator inject?"
  ├─ "If we removed all AI-generated content, what remains?"
  ├─ "Does this solve a specific problem <5 other products address?"
  └─ RESULT: coaching feedback, not gate
```

---

## §5. ARCHITECTURE

### Two-Layer Design

**SE-D6:** Skills (interface) and Agents (intelligence) are separate layers.

```
SKILLS (10)   — How creator TALKS to Engine. Present in LITE + PRO.
AGENTS (5)    — How Engine THINKS with creator. PRO only.
```

### Skills (10)

| # | Skill | Command | What It DOES (not instructs) |
|---|-------|---------|---------------------------|
| 1 | **Onboard** | `/onboard` | Asks 8 questions → generates `creator.yaml` → scans workspace → recommends first action |
| 2 | **Map** | `/map` | Asks domain questions → structures knowledge → outputs domain-map.md → feeds /create |
| 3 | **Create** | `/create {type}` | Loads exemplar preview → asks discovery questions → loads template → injects DNA patterns → generates scaffold in workspace/ → runs MCS-1 pre-check |
| 4 | **Fill** | `/fill` | Reads .meta.yaml for type → loads product spec → walks each section asking domain questions → writes creator's answers into product files → suggests /validate |
| 5 | **Validate** | `/validate [--level=N]` | Runs 7-stage pipeline (§4) with real checks: glob for files, grep for patterns, YAML parse for syntax, ref verification. Outputs scored report |
| 6 | **Package** | `/package` | Strips WHY comments → generates vault.yaml from .meta.yaml + creator.yaml → generates plugin.json → calculates checksum → creates .publish/ |
| 7 | **Publish** | `/publish` | Shows summary → requires confirmation → runs `myclaude validate` (CLI pre-flight) → runs `myclaude publish` → reports result |
| 8 | **Test** | `/test` | Creates worktree (isolation:worktree) → installs product in worktree → runs 3 test inputs (happy, edge, adversarial) → verifies activation protocol works → cleans up → reports |
| 9 | **Status** | `/status` | Reads STATE.yaml + creator.yaml + globs workspace/ → displays: engine version, edition, creator profile, products in progress (slug/type/state/last_validated), stale products (>30 days) |
| 10 | **Help** | `/help` | Lists all commands with descriptions + current edition features |

### LITE vs PRO Divergence Per Skill

| Skill | LITE Behavior | PRO Additions |
|-------|--------------|---------------|
| `/onboard` | 8-question flow → creator.yaml | Same (no agent needed) |
| `/map` | 9 structured questions → domain-map.md | **Domain Cartographer** does deep analysis: gap discovery, competitive landscape, expertise mapping |
| `/create` | Show exemplar → discovery questions → DNA Tier 1 scaffold | **Product Architect** analyzes: which DNA patterns apply? what architecture? trade-offs? Presents architecture decision BEFORE scaffolding |
| `/fill` | Section-by-section guided extraction | **Cartographer** feeds domain knowledge. Architect suggests content structure |
| `/validate` | Stages 1-3 + 6 (automated DNA Tier 1 + CLI integrity) | Stages 1-7: adds **Quality Sentinel** for Tier 2/3 agent-assisted review + anti-commodity coaching |
| `/package` | vault.yaml + plugin.json generation | Same + **Sentinel** does final quality pre-check |
| `/publish` | CLI delegation | Same + **Market Scout** suggests: tags, description optimization, pricing |
| `/test` | Worktree smoke test (3 inputs) | Same + **Sentinel** generates adversarial test cases |
| `/market` | NOT AVAILABLE | **Market Scout**: marketplace gap analysis, positioning, competitive products |
| `/my-products` | NOT AVAILABLE | **Scout** via CLI: download stats, reviews, revenue |

### PRO Agents (5)

Each agent follows this frontmatter template (official Anthropic subagent spec):

```yaml
---
name: {agent-name}
description: {when Claude should delegate to this agent — SPECIFIC triggers}
tools: {tool list — minimal necessary}
model: {sonnet|opus|inherit}
memory: {user|project|local}
permissionMode: {default|plan|dontAsk}
maxTurns: {number}
---

{System prompt — 30-50 lines MAX. Concise identity, expertise, constraints.}
```

| # | Agent | Name | Description (for Claude routing) | Tools | Model | Memory |
|---|-------|------|--------------------------------|-------|-------|--------|
| 1 | **Forge Master** | forge-master | Orchestrate Studio PRO creation flow. Route between Cartographer, Architect, Sentinel, Scout. Activate when creator uses /create, /validate --level=2+, /market, or any multi-agent task. Use proactively. | Read, Glob, Grep, Agent | inherit | project |
| 2 | **Domain Cartographer** | domain-cartographer | Deep domain analysis for product creation. Map expertise, identify gaps, structure knowledge. Use when /map is invoked in PRO mode. | Read, Glob, Grep, WebSearch | sonnet | project |
| 3 | **Product Architect** | product-architect | Design product architecture with DNA patterns. Analyze type, select applicable DNA, propose structure, justify decisions. Use when /create is invoked in PRO mode. | Read, Glob, Grep | sonnet | project |
| 4 | **Quality Sentinel** | quality-sentinel | Deep quality review and anti-commodity coaching. MCS-2/3 validation, stress testing, DNA compliance audit. Use when /validate --level=2+ is invoked. | Read, Glob, Grep | opus | project |
| 5 | **Market Scout** | market-scout | Marketplace intelligence. Gap analysis, positioning, pricing, competitive landscape. Use when /market or /my-products is invoked. | Read, Glob, Grep, Bash(myclaude *) | sonnet | project |

**SE-D26 (Agent Design Principle):** Agent identity 30-50 lines max. Not 300-line cognitive architectures. Concise: who it is, what it does, how it speaks, what it never does.

**Forge Master Lazy Activation:** Forge Master only activates when request needs routing between 2+ agents. `/create skill` goes directly to Product Architect. `/validate --level=3` goes directly to Quality Sentinel. Forge Master coordinates when `/create` needs both Cartographer + Architect, or when output of one agent feeds another.

### Agent Handoff Template

Every handoff between agents includes:

```
HANDOFF: {source_agent} → {target_agent}
WHAT_DONE: {summary of work completed}
WHAT_DECIDED: {decisions made, options rejected}
WHAT_NEXT_NEEDS: {specific context for target agent}
FILES_MODIFIED: {list of files changed/created}
```

### State Management

**STATE.yaml schema:**
```yaml
engine:
  version: "2.0.0"
  edition: "lite"  # auto-detected: "pro" if forge-master/ exists
  last_session: "2026-03-28"
  last_command: "/create skill"

workspace:
  active_products: 2
  published: 0
  stale: 0  # >30 days since last validation
  products:
    - slug: "my-skill"
      type: "skill"
      state: "content"
      mcs_target: "MCS-2"
```

**.meta.yaml schema (per product):**
```yaml
product:
  slug: "my-skill"
  type: "skill"
  created: "2026-03-28"
  mcs_target: "MCS-2"

state:
  phase: "content"  # scaffold | content | validated | packaged | published
  last_validated: null
  last_validation_score: null
  dna_compliance:
    tier1: null  # 0-100
    tier2: null
    tier3: null
  overall_score: null

history:
  created_at: "2026-03-28"
  validated_at: []  # append timestamps
  packaged_at: null
  published_at: null
  version: "1.0.0"
```

**.decisions.log (PRO only, append-only):**
```
[2026-03-28T14:30:00] DECISION: Selected squad architecture with 3 agents
  RATIONALE: Domain requires parallel analysis + synthesis
  AGENT: product-architect
  ALTERNATIVES_REJECTED: single-agent (insufficient for multi-perspective analysis)

[2026-03-28T14:45:00] DECISION: Added D11 (Socratic Pressure) to routing
  RATIONALE: Quality Sentinel recommended challenger pattern
  AGENT: quality-sentinel
```

### Context Window Budget

**SE-D12:** Engine footprint < 5%.

| Component | Tokens | Notes |
|-----------|--------|-------|
| Claude Code system prompt | ~4,200 | Invisible, unavoidable |
| Auto memory (MEMORY.md) | ~680 | First 200 lines |
| Environment info | ~280 | Working dir, platform, git |
| Engine CLAUDE.md (<200 lines) | ~2,000 | Lean boot |
| Engine skill descriptions (10) | ~1,000 | 2% budget or 16K chars |
| Engine rules | ~500 | Conditional by paths |
| Git status | ~850 | Branch, recent commits |
| **TOTAL** | **~9,500** | **~5% of 200K** |
| **Available for creator** | **~190,000** | **95%** |

PRO agents run in subagent context (context: fork) — separate window, zero main impact.

### PRO Detection Mechanism

CLAUDE.md boot sequence:
```
1. Read STATE.yaml (if exists)
2. Read creator.yaml (if exists)
3. Detect PRO: glob .claude/skills/forge-master/SKILL.md
   → If found: edition = PRO, enable agent routing
   → If not found: edition = LITE, skills-only routing
4. Display status dashboard
5. Route based on input
```

PRO can also activate via:
- Plugin `settings.json` with `"agent": "forge-master"`
- CLI flag: `claude --agent forge-master`
- Both are official Anthropic spec-compliant

---

## §6. CREATION PIPELINE (Internal Engine Flow)

Adapted from Genesis (9-phase pipeline, 8 gates). This is how the Engine INTERNALLY processes creation:

```
P0: UNDERSTAND
  Creator invokes /onboard or /map
  ├─ Capture expertise, domain, goals
  ├─ Generate creator.yaml + domain-map.md
  └─ GATE: creator profile complete?

P1: CLASSIFY
  Creator invokes /create {type}
  ├─ Identify product type (9 categories)
  ├─ Load product spec + exemplar
  ├─ Show exemplar preview ("here's what great looks like")
  ├─ PRO: Domain classification (COGNITIVE/CREATIVE/TECHNICAL/OPERATIONAL)
  └─ GATE: type identified, exemplar shown?

P2: ARCHITECT (PRO: Product Architect activates)
  ├─ Select applicable DNA patterns from applicability matrix
  ├─ Determine MCS target
  ├─ PRO: Propose architecture with trade-off analysis
  ├─ PRO: Creator approves architecture decision
  └─ GATE: DNA patterns selected, architecture approved?

P3: SCAFFOLD
  ├─ Load rich template for type
  ├─ Inject DNA patterns as sections with WHY comments
  ├─ Prefill with creator.yaml defaults (license, version, author)
  ├─ Prefill from domain-map.md if available
  ├─ Generate .meta.yaml
  ├─ Write to workspace/{slug}/
  └─ GATE: MCS-1 structural pre-check passes?

P4: EXTRACT (ETL)
  Creator invokes /fill
  ├─ EXTRACT: Walk each section, ask domain questions
  ├─ TRANSFORM: Structure answers into DNA-compliant format
  ├─ LOAD: Write into product files
  └─ GATE: all required sections non-empty?

P5: VALIDATE
  Creator invokes /validate
  ├─ Run 7-stage pipeline (§4)
  ├─ Output scored report
  ├─ Offer guided fixes for failures
  ├─ Update .meta.yaml with scores
  └─ GATE: meets MCS target?

P6: PACKAGE
  Creator invokes /package
  ├─ Strip WHY comments
  ├─ Generate vault.yaml + plugin.json
  ├─ Calculate SHA-256 checksum
  ├─ Stage to .publish/
  └─ GATE: CLI pre-flight (myclaude validate) passes?

P7: PUBLISH
  Creator invokes /publish
  ├─ Show summary + require confirmation
  ├─ Execute myclaude publish
  ├─ Report result + marketplace link
  └─ GATE: CLI reports success?
```

---

## §7. PRODUCT LIFECYCLE (13 Stages)

### Complete Journey: Idea → Installed

| Stage | What Happens | Who | Where | Data Created | Verification |
|-------|-------------|-----|-------|-------------|-------------|
| 0. DISCOVER | Creator hears about MyClaude | Creator | External (community, marketing) | — | — |
| 1. ONBOARD | Clone repo, open in Claude Code, /onboard | Creator + Studio | Studio repo | creator.yaml | YAML valid, profile type inferred |
| 2. MAP | /map domain knowledge | Creator + Studio (PRO: Cartographer) | Studio | domain-map.md | Coverage ≥ 70% |
| 3. CREATE | /create {type} → scaffold | Creator + Studio (PRO: Architect) | workspace/ | Product files + .meta.yaml | MCS-1 structural pre-check |
| 4. FILL | /fill → content extraction | Creator + Studio | workspace/ | Filled product files | All required sections non-empty |
| 5. VALIDATE | /validate → quality check | Studio + CLI (PRO: Sentinel) | workspace/ | MCS report + updated .meta.yaml | Score ≥ MCS target threshold |
| 6. PACKAGE | /package → bundle | Studio | .publish/ | vault.yaml + plugin.json + bundle | CLI pre-flight passes |
| 7. PUBLISH | /publish → ship | Studio + CLI + Marketplace API | .publish/ → API → Firestore + R2 | Product record + stored files | CLI validates auth + manifest + secrets |
| 8. DISCOVER (buyer) | Buyer finds product | Buyer | CLI search / marketplace web | — | — |
| 9. PURCHASE | Buyer buys (if paid) | Buyer + Marketplace + Stripe | Marketplace → Stripe | Order in Firestore | Webhook signature, server-side order |
| 10. INSTALL | `myclaude install {slug}` | Buyer + CLI | CLI → API → R2 → buyer's project | Product files in .claude/skills/ | File integrity, install target correct |
| 11. USE | Buyer invokes product | Buyer + Product | Buyer's project | Product output | Product's own D4 quality gate |
| 12. FEEDBACK | Buyer reviews | Buyer + Marketplace | Marketplace | Review, rating | Review moderation |
| 13. ITERATE | Creator updates | Creator + Studio + CLI | Studio → CLI → Marketplace | Updated product, new version | Same as stages 5-7 + version bump |

### Product State Machine

```
                        /create
  (none) ──────────────────────────► scaffold
                                        │
                                        │ /fill or manual editing
                                        ▼
                                     content ◄─────────────────┐
                                        │                      │
                                        │ /validate passes     │ Creator edits files
                                        ▼                      │ (auto-detected via
                                    validated                  │  FileChanged hook or
                                        │                      │  manual state regression)
                                        │ /package             │
                                        ▼                      │
                                    packaged                   │
                                        │                      │
                                        │ /publish             │
                                        ▼                      │
                                    published ─────────────────┘
                                    (v1.0.0)    Creator starts v1.1.0

TRANSITIONS:
  scaffold → content:    Creator fills content (/fill or manual)
  content → validated:   /validate passes MCS target
  validated → packaged:  /package succeeds
  packaged → published:  /publish succeeds
  published → content:   Creator modifies for new version (version auto-bumped)
  validated → content:   Creator edits product files (state regresses)
  ANY → scaffold:        /create --force (destructive, requires confirmation)
```

---

## §8. ECOSYSTEM INTEGRATION

### Data Flow Matrix

| FROM ↓ / TO → | Studio Engine | CLI | Marketplace API | Buyer Project |
|---|---|---|---|---|
| **Studio** | — | vault.yaml + files (publish), validate cmd | — (indirect via CLI) | — |
| **CLI** | Validate results, publish status, search results | — | Auth + manifest + files (publish), search query, install request | Product files (install) |
| **Marketplace API** | — (PRO future: stats via CLI) | Product data, download URLs, auth status | — | — |
| **Buyer Project** | — | Installed product list | — (reviews via web) | — |
| **Stripe** | — | — | Webhook events (payment confirmation) | — |

### vault.yaml Complete Schema

```yaml
# REQUIRED FIELDS
name: "my-skill"                    # lowercase, hyphens, regex: ^[a-z0-9][a-z0-9_-]*$
version: "1.0.0"                    # semver: MAJOR.MINOR.PATCH
type: "skill"                       # one of: skill|agent|squad|workflow|design-system|claude-md|prompt|application|system
description: "What it does"         # 10-500 chars
entry: "SKILL.md"                   # main file, must exist
license: "MIT"                      # valid identifier
price: 0                            # >= 0, in dollars
tags: ["category", "domain"]        # array of strings

# ENRICHMENT FIELDS (optional, defaults applied)
displayName: "My Skill"             # human-readable, defaults from name
mcsLevel: 1                         # 1|2|3, from /validate
language: "en"                      # from creator.yaml
longDescription: ""                 # extended description
readme: "README.md"                 # readme file path
installTarget: ".claude/skills/{slug}/"  # auto from type (CE-D38)
compatibility:
  claudeCode: ">=1.0.0"            # minimum version
dependencies:
  myclaude: []                      # slugs of required products
```

### plugin.json Schema (for Anthropic distribution)

```json
{
  "name": "{slug}",
  "description": "{description}",
  "version": "{version}",
  "author": {
    "name": "{from creator.yaml}"
  },
  "license": "{license}",
  "homepage": "https://myclaude.sh/p/{slug}"
}
```

Generated alongside vault.yaml by /package. Plugin directory structure:

```
.plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/           # for skill/agent/squad/workflow/prompt/system types
│   └── {slug}/
│       └── SKILL.md (or AGENT.md, etc.)
├── agents/           # for agent type with subagent spec
├── rules/            # for claude-md type
└── README.md
```

**SE-D14:** /package generates BOTH formats from the same source files.

### Verification at Every Point

| Point | Studio Verifies | CLI Verifies | Marketplace Verifies |
|-------|----------------|-------------|---------------------|
| Create | MCS-1 structural (glob file existence) | — | — |
| Validate | DNA compliance: Stages 1-5 (grep, glob, parse) | Stage 6: manifest + files + secrets | — |
| Package | WHY stripped, manifests valid, checksum | — | — |
| Publish | Creator confirmed | Auth, manifest, secrets, pack, upload | Auth token, user exists, quota |
| Install | — | Auth, purchase verified, integrity, target | Order exists (if paid) |
| Use | — | — | Product's own D4 quality gate |

### Revenue Flow

```
Buyer pays $29 for a product
  ├─ Stripe processes payment
  ├─ Webhook fires → POST /api/stripe/webhooks
  ├─ Order created in Firestore (server-side ONLY)
  ├─ Platform fee: 8% ($2.32) → MyClaude
  ├─ Stripe fee: ~2.9%+30¢ ($1.14) → Stripe
  └─ Creator receives: ~$25.54 → Stripe Connect
```

### Buyer Experience Validation (DNA check for installed products)

Every product created by the Engine must work STANDALONE in the buyer's project:

| Check | What to verify | DNA Pattern |
|-------|---------------|-------------|
| Frontmatter | Has Anthropic Agent Skills spec frontmatter (name, description) | D1 |
| README | Has install (`myclaude install {slug}`) + usage + requirements | D13 |
| Activation | Activation protocol loads correctly without the Engine | D1 |
| Paths | All file references are relative, not absolute | D16 |
| References | No broken refs (every referenced file exists in product bundle) | D16 |
| Commands | Slash command doesn't conflict with common names (/help, /status, etc.) | D16 |
| First use | Product delivers value on first invocation | D4 |
| Degradation | Product handles missing context gracefully (not crash/silence) | D14 |

---

## §9. OFFICIAL CLAUDE CODE SPEC ALIGNMENT

### Skill Spec Features → DNA/Template Mapping

| Feature | What It Does | Where in DNA | Template Includes |
|---------|-------------|-------------|-------------------|
| `context: fork` | Runs skill in isolated subagent | D18 (Subagent Isolation) | Agent/Squad templates include this |
| `agent: Explore\|Plan\|custom` | Which subagent executes | D9 (Orchestrate) | Squad template specifies per-agent |
| `allowed-tools: Read, Grep` | Restricts tools | D16 (Composability) | Templates suggest appropriate tools |
| `paths: ["src/**/*.ts"]` | Conditional activation | D3 (Progressive Disclosure) | CLAUDE.md template uses this |
| `hooks:` in frontmatter | Inline automation | D17 (Hook Integration) | Templates include hooks section |
| `` !`command` `` | Pre-processed shell injection | D7 (Pre-Execution Gate) | Templates show dynamic context pattern |
| `$ARGUMENTS`, `$0` | Positional arguments | D5 (Question System) | Templates include argument handling |
| `${CLAUDE_SKILL_DIR}` | Skill directory path | D3 (Progressive Disclosure) | Templates reference via this |
| `model:` | Force model | — | Agent templates specify model |
| `effort:` | Force effort level | — | Templates note when to use |
| `user-invocable: false` | Background knowledge | D3 | Templates document this option |
| `disable-model-invocation: true` | Manual-only trigger | — | Templates for workflows use this |

### Subagent Spec Features → PRO Agent Mapping

| Feature | Used By | Why |
|---------|---------|-----|
| `memory: project` | All 5 PRO agents | Cross-session learning per project |
| `tools: [restricted list]` | Each agent gets minimal tools | Security + focus |
| `model: sonnet\|opus` | Sentinel=opus (deep), others=sonnet | Cost/quality balance |
| `permissionMode: default` | All agents | Creator controls permissions |
| `maxTurns: 50` | All agents | Prevent runaway |
| `skills: [preloaded]` | Forge Master preloads routing | Knows available commands |
| `isolation: worktree` | /test skill | Real testing in isolated copy |
| `background: false` | All agents | Creator sees agent work in real-time |

### Hooks the Engine Uses

| Event | Hook Type | Purpose |
|-------|-----------|---------|
| `SessionStart` (matcher: startup) | command | Boot: read STATE.yaml, detect edition, display status |
| `PostToolUse` (matcher: Write\|Edit) | command | Auto-detect: if file in workspace/ edited, check if product state should regress |
| `Stop` | command | Save STATE.yaml with last_command |
| `FileChanged` (matcher: creator.yaml) | command | Reload creator profile if changed |

---

## §10. TEMPLATES

**SE-D17:** Templates are RICH. DNA injected. WHY comments educate.

### Template Structure (all 9 types)

```
templates/{type}/
├── {PRIMARY}.md.template      # Main file with WHY comments + DNA sections
├── README.md.template         # Install + usage + examples
├── references/
│   └── domain-knowledge.md.template
├── examples/
│   └── examples.md.template
└── [type-specific files]
```

### WHY Comment Format

```markdown
<!-- WHY: D1 (Activation Protocol) — Without loading context first,
     the product responds generically. Loading domain knowledge BEFORE
     acting ensures output is domain-aware. Order matters: knowledge
     first (what to know), anti-patterns second (what to avoid),
     user intent third (what to do). -->

## Activation Protocol

Before responding to any invocation:

1. **Load domain knowledge:** Read `references/domain-knowledge.md`
2. **Load anti-patterns:** Read `references/anti-patterns.md`
3. **Identify user intent:** Parse input for specific request type
```

WHY comments are stripped during /package (grep + sed). They never appear in published products.

---

## §11. EXEMPLARS

### 9 Original Exemplars

| Type | Name | Domain | MCS Target | Priority |
|------|------|--------|-----------|----------|
| **Skill** | `code-health-check` | Codebase analysis | MCS-3 | P0 |
| **Squad** | `code-review-team` | Multi-agent code review | MCS-3 | P0 |
| **System** | `documentation-engine` | Docs extraction + review | MCS-3 | P0 |
| Agent | `technical-writer` | Documentation from code | MCS-3 | P1 |
| Workflow | `release-checklist` | Release pipeline | MCS-2 | P1 |
| Design System | `terminal-palette` | CLI design tokens | MCS-2 | P1 |
| Prompt | `decision-matrix` | Decision analysis | MCS-2 | P1 |
| CLAUDE.md | `open-source-maintainer` | OSS project config | MCS-2 | P1 |
| Application | `changelog-generator` | Git changelogs | MCS-2 | P1 |

Exemplars version WITH the DNA. DNA v2 → exemplars v2.

---

## §12. v1.1.0 TRIAGE

### KEEP (25 artifacts)

| Artifact | Lines | Action |
|----------|-------|--------|
| references/product-specs/ (9 files) | ~1850 | Add DNA requirements table per type |
| references/best-practices/ (5 files) | ~1056 | Update skill-best-practices with DNA |
| references/quality/mcs-spec.md | 187 | Rewrite as DNA compliance (§4) |
| references/quality/anti-patterns.md | 267 | Expand with D2 patterns |
| references/quality/anti-commodity.md | 178 | Polish, connect to Sentinel |
| references/market/categories.md | 258 | Keep as-is |
| references/market/pricing-guide.md | 217 | Keep (future: update with real data) |
| references/shared-vocabulary.md | 92 | Expand with DNA vocab |
| references/sample-product/ | 306 | Replace with exemplar |
| creator.yaml schema | — | Add edition field |
| .gitignore, .gitattributes, LICENSE | — | Keep |

### EVOLVE (8 artifacts)

| Artifact | From (lines) | To (lines) | Changes |
|----------|-------------|-----------|---------|
| CLAUDE.md | 226 | <200 | Lean boot, edition detection, L0 pattern |
| README.md | 319 | ~400 | Full v2.0 guide with Lite/PRO |
| /onboard | 227 | ~150 | Tighten, add edition detection |
| /create | 339 | ~250 | DNA injection, PRO mode, rich templates |
| /validate | 282 | ~300 | Real checks (glob, grep, YAML parse), 7-stage pipeline |
| /publish | 296 | ~100 | Simplify — delegate to CLI |
| /package | 48 | ~150 | Dual manifests, WHY strip, checksum |
| templates/ (9) | bare | rich | DNA-infused, WHY comments, prefilled |

### KILL (15 artifacts)

5 theatrical agents, 9 fictional exemplars, /create-content (→/fill), /test old (→/test new), /quick-skill, /quick-publish, /engine-status (→/status), /engine-help (→/help), /my-products (→PRO), /differentiate (→Sentinel), /quality-review (→Sentinel), /domain-consult (→Cartographer), /market-scan (→Scout), /packaging-review (→/package), caching-strategy.md

### NEW (20 artifacts)

knowledge/structural-dna.md, knowledge/product-dna/ (9), knowledge/quality-gates.yaml, config.yaml, STATE.yaml, /map, /fill, /test (new), /status, /help, PRO agents (5), workflows (3), exemplars (3→9), hooks config

---

## §13. BUILD SEQUENCE

### S0: Foundation

**Deliverables:** structural-dna.md, CLAUDE.md (<200 lines), STATE.yaml, config.yaml, .claude/settings.json

**Acceptance Criteria:**
- [ ] structural-dna.md contains all 18 patterns with: ID, name, problem, rule, tier, validation check
- [ ] Meta-architecture documented in structural-dna.md
- [ ] CLAUDE.md < 200 lines with: boot sequence, edition detection (glob forge-master/), skill routing, rules
- [ ] STATE.yaml schema implemented
- [ ] config.yaml with: quality gate thresholds, routing rules, MCS scoring weights
- [ ] .claude/settings.json with appropriate permissions

### S1: Knowledge

**Deliverables:** Evolved product-specs (9), evolved MCS spec, quality-gates.yaml, product-dna/ (9)

**Acceptance Criteria:**
- [ ] All 9 product specs have DNA requirements table (which D-patterns required per MCS level)
- [ ] MCS spec rewritten with scoring formula from §4
- [ ] quality-gates.yaml defines state transitions (scaffold→content→validated→packaged→published)
- [ ] product-dna/ has one file per type with: required patterns, template mapping, frontmatter fields

### S2: Core Skills

**Deliverables:** 10 skills in .claude/skills/

**Acceptance Criteria:**
- [ ] All 10 skills have Anthropic Agent Skills spec frontmatter
- [ ] /create generates scaffolds that pass MCS-1 validation (verify by running /validate on generated scaffold)
- [ ] /validate runs REAL checks: glob (file existence), grep (pattern detection), YAML parse (syntax), ref verification (path existence)
- [ ] /validate scoring matches formula in §4 (±2% tolerance)
- [ ] /package generates valid vault.yaml (verified by `myclaude validate`) AND valid plugin.json
- [ ] /publish successfully invokes `myclaude publish` (or correctly handles CLI absence)
- [ ] /test creates worktree, installs product, runs 3 tests, reports, cleans up
- [ ] /map produces structured domain-map.md that /create can consume

### S3: Templates

**Deliverables:** 9 rich templates in templates/

**Acceptance Criteria:**
- [ ] All templates have Anthropic frontmatter (name, description, argument-hint)
- [ ] All templates have WHY comments for every DNA pattern section
- [ ] All templates have prefilled content (not .gitkeep)
- [ ] Generated scaffolds from templates pass MCS-1 validation
- [ ] WHY comments successfully stripped by /package (verify clean output)

### S4: Exemplars (Priority 3)

**Deliverables:** code-health-check (skill), code-review-team (squad), documentation-engine (system)

**Acceptance Criteria:**
- [ ] Each exemplar is ORIGINAL, FUNCTIONAL, SELF-CONTAINED
- [ ] Each exemplar passes MCS-3 validation with score ≥ 92%
- [ ] Each exemplar demonstrates ALL applicable DNA patterns for its type
- [ ] Each exemplar has WHY comments explaining every structural choice
- [ ] Each exemplar could be installed and used standalone by a buyer

### S5: Integration Test

**Acceptance Criteria:**
- [ ] Full pipeline: /onboard → /map → /create skill → /fill → /validate → /package → /publish
- [ ] vault.yaml accepted by `myclaude validate`
- [ ] plugin.json has valid structure
- [ ] DNA scoring produces correct results (manual verification against 3 products)
- [ ] State machine: .meta.yaml correctly tracks state transitions
- [ ] LITE edition complete and functional

**LITE v2.0 SHIPPABLE after S5 passes.**

### S6: PRO Agents

**Deliverables:** 5 agents in .claude/skills/ (installed via marketplace)

**Acceptance Criteria:**
- [ ] All 5 agents have official Anthropic subagent spec frontmatter
- [ ] Agent identity: 30-50 lines each, concise, not theatrical
- [ ] Memory scope: project for all agents
- [ ] Tools: minimal necessary per agent
- [ ] Handoff template used for all inter-agent communication
- [ ] Forge Master correctly routes (only activates for multi-agent requests)

### S7: PRO Features

**Acceptance Criteria:**
- [ ] /validate --level=2 triggers Quality Sentinel for agent-assisted review
- [ ] /validate --level=3 includes stress testing + anti-commodity coaching
- [ ] /create in PRO mode shows architecture decision before scaffolding
- [ ] /map in PRO mode provides deep domain analysis
- [ ] MCS-2/3 validation demonstrably produces better feedback than LITE MCS-1

### S8: PRO Integration

**Acceptance Criteria:**
- [ ] PRO packaged as MyClaude product (vault.yaml with type: system, MCS-3)
- [ ] PRO packaged as Anthropic plugin (plugin.json with settings.json agent: forge-master)
- [ ] Install test: `myclaude install myclaude-studio-pro` → agents appear in .claude/skills/
- [ ] CLAUDE.md correctly detects PRO after install (edition switches to "pro")
- [ ] Full PRO pipeline works: /create with Architect → /validate with Sentinel
- [ ] PRO uninstall: `myclaude uninstall myclaude-studio-pro` → edition reverts to "lite"

**PRO v2.0 SHIPPABLE after S8 passes.**

### S9: Remaining Exemplars

6 remaining: technical-writer (agent), release-checklist (workflow), terminal-palette (ds), decision-matrix (prompt), open-source-maintainer (claude-md), changelog-generator (app)

### S10: Polish

README, CHANGELOG, Contributing guide, Hook automation (SessionStart, PostToolUse, Stop), Self-test suite

---

## §14. SUCCESS CRITERIA

### KPIs (measurable)

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Time-to-first-publish (simple skill) | < 30 minutes | Timed e2e: /onboard → /publish |
| MCS-1 pass rate on fresh scaffolds | > 95% | Run /validate on generated scaffold |
| Creator returns (creates 2+ products) | > 40% | Repeat /create invocations per creator.yaml |
| Products rated ≥ 4/5 on marketplace | > 70% | Marketplace analytics (future) |
| Non-developer creators publishing | > 30% | Profile type distribution in creator.yaml |
| Zero broken products published | 0 | MCS-1 catches all structural issues |
| LITE adoption (clones/stars) | > 1000 in 90 days | GitHub analytics |
| PRO conversion (from LITE users) | > 5% | Marketplace purchase data |

### Value Delta Test

Before declaring v2.0 complete, create THE SAME product:
1. Manually (raw Claude Code, no Engine)
2. With Engine LITE
3. With Engine PRO

Compare: quality (MCS score), time, completeness, DNA compliance. If LITE doesn't beat manual by ≥30%, and PRO doesn't beat LITE by ≥30%, the Engine doesn't provide sufficient value.

---

## §15. RISKS, BLIND SPOTS & TRADE-OFFS

### Risks

| Risk | Category | Probability | Mitigation |
|------|----------|-------------|-----------|
| CLI publish not working | Technical | Medium | Test in S5. Fallback: manual upload guide |
| DNA too complex for beginners | Adoption | Medium | Tier 1 = 6 patterns (minimal). Progressive disclosure |
| PRO doesn't sell | Business | Medium | LITE must be genuinely good. PRO delta must be obvious |
| Anthropic changes skill spec | Technical | Low | 100% aligned with current spec. Monitor changelog |
| Exemplars take too long | Schedule | High | 3 priority first. Others can follow |
| Competition from ECC (113K stars) | Market | Low | ECC = tools collection. Studio = meta-system with DNA |
| Marketplace zero supply | Ecosystem | High | LITE creates products regardless of marketplace |
| Creator abandons mid-creation | UX | Medium | State persistence + /status shows progress |
| Manual creation is faster | Adoption | High | SE-AXIOM-2: every skill must add measurable value |

### 12 Blind Spots (from ecosystem deep map)

| # | Blind Spot | Status in v2.0 | Resolution |
|---|-----------|---------------|-----------|
| 1 | Feedback loop (Marketplace → Engine) | Designed as PRO /my-products | P2 (requires marketplace data) |
| 2 | Lifecycle truncated (no update flow) | State machine includes published → content | v2.0 supports version iteration |
| 3 | Testing fictional | /test uses worktree isolation | v2.0 resolves |
| 4 | Exemplars fictional | 9 original exemplars designed | v2.0 resolves |
| 5 | Agent overengineering | 30-50 line agents, spec-compliant | v2.0 resolves |
| 6 | Cold start | LITE works without marketplace | v2.0 mitigates |
| 7 | Onboarding pre-engine | README + quick start guide | v2.0 addresses |
| 8 | Creator economics | Revenue flow documented, pricing guide exists | v2.0 documents |
| 9 | Dependency management | vault.yaml has dependencies.myclaude field | CLI handles at install |
| 10 | Multi-product management | /status shows portfolio | Future: portfolio mode |
| 11 | Post-publish discovery | /publish suggests tags for discoverability | Future: GHOST framework |
| 12 | Engine self-update | Engine versions via git pull | Future: auto-update mechanism |

### Trade-offs

| Tension | Current Choice | Rationale |
|---------|---------------|-----------|
| Guidance depth vs Speed | Progressive: LITE fast, PRO deep | Serve both personas |
| Quality gates vs Publishing friction | MCS-1 = low bar, MCS-2/3 = opt-in | Don't block first-time creators |
| Generality (9 types) vs Depth per type | product-dna/ per type + exemplars | Specialization via knowledge, not code |
| Automation vs Creator control | Non-destructive default, --fix opt-in | Protect creator's work |
| Opinionated (DNA) vs Flexible | DNA is coaching, not blocking | Guide, don't gate |
| Engine-first vs CLI-first | Engine complements CLI | CLI works standalone, Engine adds intelligence |

---

## §16. CREATOR PERSONAS

| Persona | Technical Level | Primary Goal | Engine Adapts By |
|---------|----------------|-------------|-----------------|
| **Developer** | Advanced/Expert | Monetize code skills | Less guidance, shortcuts (/quick-skill), focus on MCS-2/3 |
| **Domain Expert** | Beginner/Intermediate | Package expertise | More guidance, /map first, focus on /fill for content extraction |
| **Prompt Engineer** | Intermediate | Create prompts/agents | Suggest prompt/agent types, show relevant exemplars |
| **Marketer** | Beginner | Create content products | Guide toward prompt type, simplify validation |
| **Agency** | Mixed | Produce at scale | Portfolio mode (future), batch validation |
| **Hybrid** | Advanced | Complex systems | Suggest system/squad types, show composition patterns |

Persona inferred from creator.yaml during /onboard. Recommendations adapt per persona.

---

## §17. DECISIONS LOG (27 decisions)

| ID | Decision | Section |
|----|----------|---------|
| SE-D1 | Engine is a SYSTEM, not loose skills | §1 |
| SE-D2 | Self-contained, agnostic, zero external deps | §1 |
| SE-D3 | Arsenal is build-time only | §1 |
| SE-D4 | MCS v2 = DNA compliance | §4 |
| SE-D5 | DNA superset of Anthropic best practices | §3 |
| SE-D6 | Skills + Agents = separate layers | §5 |
| SE-D7 | LITE = tools, PRO = tools + cognitive agents | §5 |
| SE-D8 | LITE MIT, PRO paid | §5 |
| SE-D9 | PRO installs into LITE (recursive) | §5 |
| SE-D10 | Dual distribution: vault.yaml + plugin.json | §8 |
| SE-D11 | --agent as PRO entry point | §5 |
| SE-D12 | Context footprint < 5% | §5 |
| SE-D13 | CLI implemented, Engine delegates | §8 |
| SE-D14 | /package generates both manifests | §8 |
| SE-D15 | Exemplars original, functional, educational | §11 |
| SE-D16 | Priority: skill, squad, system first | §11 |
| SE-D17 | Templates rich with DNA + WHY comments | §10 |
| SE-D18 | 18 DNA patterns in 3 tiers | §3 |
| SE-D19 | Hook integration as DNA pattern | §9 |
| SE-D20 | Subagent isolation for agents/squads | §9 |
| SE-D21 | Agent Teams awareness in knowledge | §3 |
| SE-D22 | /map for domain mapping | §5 |
| SE-D23 | /test with worktree isolation | §5 |
| SE-D24 | /fill as ETL content extraction | §5 |
| SE-D25 | /validate delegates integrity to CLI | §4 |
| SE-D26 | Name: MyClaude Studio Engine | §2 |
| SE-D27 | Continuous learning as PRO P2 | §18 |

---

## §18. PENDENCIES

| Item | Owner | Priority | Blocker? |
|------|-------|----------|---------|
| Continuous learning pattern spec | Future | P2 | No |
| Market Scout API integration | Future | P2 | No |
| Remaining 6 exemplars | Builder | P1 | No |
| Portfolio management | Future | P3 | No |
| i18n for Engine skills | Future | P2 | No |
| Self-test suite | Builder | P2 | No |
| Engine self-update mechanism | Future | P3 | No |
| Webhook notifications for sales | Future | P3 | No |
| Product preview (how it looks on marketplace) | Future | P3 | No |
| Rollback mechanism for published versions | Future | P3 | No |
| Bundle/suite product support | Future | P3 | No |

---

## APPENDIX A: SOURCES

| Source | What | Status |
|--------|------|--------|
| Ecosystem Deep Map | 89.7% completude, 12 blind spots | Complete |
| Cognitive Audit | System Diagnosis + Argument Audit | Complete |
| DNA Extraction | 4 production systems + Genesis framework + ECC | Complete |
| Genesis Analysis | Pipeline, 20 principles, 17 generated systems | Complete |
| ECC Analysis | 113K stars, 125 skills, patterns absorbed | Complete |
| Official: Skills spec | Frontmatter, context:fork, paths, hooks, args | Scraped |
| Official: Memory spec | CLAUDE.md, auto memory, rules, imports | Scraped |
| Official: Hooks spec | 20+ events, 4 types, exit codes, matchers | Scraped |
| Official: Subagents spec | Custom agents, memory, isolation, composition | Scraped |
| Official: Plugins spec | Manifest, distribution, marketplace, settings | Scraped |
| Official: Agent Teams spec | Lead/teammate, task list, mailbox, hooks | Scraped |
| Official: Best Practices | Verification, context, CLAUDE.md, scaling | Scraped |
| Official: Context Window | Token counts, budgets, compaction | Scraped |
| CONDUIT Protocol | 28 wiring decisions (WP-1 → WP-28) | Complete |
| CLI Codebase | publish.ts, validate.ts, manifest.ts — implemented | Read |

---

*MyClaude Studio Engine PRD v2.0.1*
*Multi-framework architecture | Multi-pillar cognitive audit | Ecosystem deep map*
*51 gaps identified and closed in audit pass*
*27 decisions | 18 DNA patterns | 10 sprints | 13-stage lifecycle*
*Made in Brazil with the ambition of marking the global AI community*
