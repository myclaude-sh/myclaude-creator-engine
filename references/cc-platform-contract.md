# Claude Code Platform Contract — Creator Reference
<!-- Adapted from OBSIDIAN extraction (S92). Every claim has [SOURCE:] evidence. -->
<!-- This file is the DEFINITIVE reference for how Claude Code processes products. -->
<!-- Load on-demand by /create, /fill, /validate, /package when platform context needed. -->

**Version:** 2.0.0 | **Extracted from:** Claude Code source (2026-04-04) | **Session:** S92→S93→S94 (Codex enrichment)
**v2.0 additions:** §1.3 (@include depth/external/text-only), §1.7 (type labels + override header), §3.5 (cache architecture), §9.3 (section taxonomy). All with [SOURCE:] citations.

---

## 1. Memory Architecture — How Claude Code Loads Your Product

Claude Code loads instruction files in a strict priority order. Files loaded LATER have HIGHER priority (the model pays more attention to them).

### 1.1 Loading Order
[SOURCE: claudemd.ts:790-960]

```
LOWEST PRIORITY (loaded first)
│
│  1. Managed    — /etc/claude-code/CLAUDE.md (enterprise policies)
│  2. User       — ~/.claude/CLAUDE.md (buyer's personal instructions)
│  3. Project    — For EACH directory from repo root → CWD:
│     3a. CLAUDE.md
│     3b. .claude/CLAUDE.md
│     3c. .claude/rules/*.md (path-scoped via frontmatter)
│  4. Local      — CLAUDE.local.md (private, gitignored, per-project)
│  5. Auto-Memory — MEMORY.md (auto-managed, highest priority)
│
HIGHEST PRIORITY (loaded last)
```

**What this means for creators:**
- **skill** products (.claude/skills/) are NOT memory files — loaded only on `/invoke`
- **claude-md** products (.claude/rules/) ARE memory files — loaded EVERY turn, always in context
- **agent/minds** products (.claude/commands/ or .claude/agents/) — loaded only when spawned
- **hooks** products (.claude/settings.local.json) — event-triggered, never in context

### 1.2 Memory Limits
[SOURCE: claudemd.ts:92, memdir.ts:34-38, doctorContextWarnings.ts:44-47]

| Limit | Value | Type | What Happens |
|-------|-------|------|-------------|
| Per-file recommended | ~4,000 chars | Best practice | Optimal performance |
| Per-file warning | 40,000 chars | /doctor warning | Degrades context quality |
| Per-file hard cap | None in client | Technical | Files >40K still load |
| MEMORY.md lines | 200 | Hard truncation | Lines after 200 silently dropped |
| MEMORY.md bytes | 25,000 (25KB) | Hard truncation | Content beyond 25KB dropped |
| Agent descriptions | ~9,000 tokens total | /doctor warning | All agents combined |
| MCP tools | 25,000 tokens total | /doctor warning | All servers combined |

**Creator guidance:**
- Keep primary files (SKILL.md, AGENT.md) under 4K chars for best performance
- Move detailed content to references/ (loaded on-demand, zero ambient cost)
- claude-md products: every character costs tokens EVERY turn — be ruthless about size

### 1.3 @include Directive
[SOURCE: claudemd.ts:18-25, 451-469]

```markdown
Syntax (in any memory file):
  @path              — relative to current file
  @./relative/path   — explicit relative
  @~/home/path       — home directory
  @/absolute/path    — absolute path
  @path#heading      — fragment identifiers stripped (loads full file)
  @path\ with\ spaces — escaped spaces supported

Rules:
  - Circular references prevented (silently via processedPaths tracking)
  - Non-existent files silently ignored (no error, no warning)
  - Works in text only (NOT inside code blocks or code spans)
  - Included files load BEFORE the including file
  - External @includes require user approval (see below)
```

**Depth limit:**
[SOURCE: claudemd.ts:537]
```
MAX_INCLUDE_DEPTH = 5
@include chains deeper than 5 levels: files beyond level 5 are SILENTLY IGNORED.
No error. No warning. The content simply doesn't load.
```

**External @include approval:**
[SOURCE: claudemd.ts:667-670, 799-801]
```
@include targets OUTSIDE the project directory require explicit approval:
  - Config flag: hasClaudeMdExternalIncludesApproved
  - The buyer sees an approval prompt on first load
  - Exception: User memory (~/.claude/) can always include external files

Creator implication: If your system/bundle product uses @include to reference
files outside its install directory, the buyer will see a permission prompt.
Consider copying the referenced file INTO your product instead.
```

**Text-only restriction:**
[SOURCE: claudemd.ts:96-227]
```
Only ~100 text file extensions are allowed for @include:
  .md .txt .json .yaml .yml .toml .xml .csv .html .css
  .js .ts .tsx .jsx .py .rb .go .rs .java .kt .c .cpp .h
  .cs .swift .sh .bash .sql .graphql .vue .svelte .astro
  .php .lua .r .dart .ex .erl .hs .elm ... (full list in source)

Binary files (.pdf .png .zip .jpg etc.) are SILENTLY IGNORED.
If your @include points to a binary, it's as if the line doesn't exist.
```

**Creator opportunity:** Use @include for modular products. A system product can @include separate knowledge bases without bloating the primary file. Keep @include trees shallow (recommend ≤3 levels, hard cap at 5).

### 1.4 HTML Comment Stripping
[SOURCE: claudemd.ts:282-334]

```
Memory files: <!-- comments --> are AUTO-STRIPPED (invisible to model)
Skill files:  <!-- comments --> are VISIBLE (skills are not memory files)
```

**Creator implication:**
- `<!-- WHY: -->` annotations in CLAUDE.md or .claude/rules/ = invisible to model (good for docs, bad for instructions)
- `<!-- WHY: -->` in SKILL.md = visible to model (WHY comments are part of the skill's content)
- /package strips WHY comments when building .publish/ directory

### 1.5 Path-Scoped Rules
[SOURCE: claudemd.ts:254-268]

```yaml
# In .claude/rules/api-standards.md frontmatter:
---
paths:
  - src/api/**
  - src/routes/**
---
# This rule ONLY loads when the user works on matching files.
# Uses picomatch for glob matching.
# If all patterns are ** (match-all), treated as unscoped.
```

**Creator opportunity:** claude-md products can target specific file types. A "SQL Review Rules" product only loads when the user touches `.sql` files — zero cost otherwise.

### 1.6 CLAUDE.local.md
[SOURCE: claudemd.ts:922-933]

Private, gitignored, per-project instructions. Loaded as LOCAL type (high priority).

**Creator opportunity:** system products can include a CLAUDE.local.md template for buyer-specific config (API keys context, private preferences) without polluting the shared project.

### 1.7 How the Model Sees Your Product — Type Labels & Override Header
[SOURCE: claudemd.ts:89-90, 1169-1177]

When Claude Code injects your product into the model's context, it wraps it with two critical elements:

**1. Override Header (before ALL memory files):**
```
"Codebase and user instructions are shown below. Be sure to adhere to
these instructions. IMPORTANT: These instructions OVERRIDE any default
behavior and you MUST follow them exactly as written."
```

This means: your product isn't a suggestion — it's compiled as LAW. The model treats your instructions as overriding its default behavior. Write directives ("always do X"), not suggestions ("consider doing X").

**2. Type Labels (per file):**
Each file gets a label the model sees:

| Product Type | Install Path | Model Sees |
|-------------|-------------|------------|
| claude-md | `.claude/rules/{slug}.md` | "(project instructions, checked into the codebase)" |
| CLAUDE.local.md | `CLAUDE.local.md` | "(user's private project instructions, not checked in)" |
| User rules | `~/.claude/rules/*.md` | "(user's private global instructions for all projects)" |
| Auto-memory | `MEMORY.md` | "(user's auto-memory, persists across conversations)" |

**Creator implication:**
- Products in `.claude/rules/` are labeled as "project instructions" — the model treats them as team-level authority
- The override header means your rules ARE law, not suggestions — write accordingly
- Products installed to `~/.claude/` are labeled as "personal" — lower authority than project-level

---

## 2. Frontmatter Specification — Your Product's Metadata

Frontmatter is how Claude Code discovers, catalogs, and controls your product.

### 2.1 Complete Field Inventory
[SOURCE: loadSkillsDir.ts, frontmatterParser.ts, AgentTool.ts, loadOutputStylesDir.ts]

| Field | Type | Skills | Agents | Rules | Output Styles | Effect |
|-------|------|:------:|:------:|:-----:|:------------:|--------|
| `name` | string | **REQ** | **REQ** | — | **REQ** | Invocation name, catalog display |
| `description` | string | **REQ** | **REQ** | — | **REQ** | Catalog display. Token counted. |
| `allowed-tools` | string[] | OPT | OPT | — | — | Restrict tool access (whitelist) |
| `denied-tools` | string[] | OPT | OPT | — | — | Block specific tools (blacklist) |
| `model` | string | OPT | OPT | — | — | Force model: `sonnet`, `opus`, `haiku` |
| `paths` | string[] | OPT | — | OPT | — | Glob patterns for activation scope |
| `effort` | string/int | OPT | OPT | — | — | `low`/`medium`/`high`/`max` or integer |
| `maxTurns` | int | OPT | OPT | — | — | Limit agentic iterations |
| `shell` | object | OPT | — | — | — | Shell-based execution config |
| `hooks` | object | OPT | — | — | — | Frontmatter-defined hooks |
| `whenToUse` | string | OPT | — | — | — | Auto-trigger conditions. Token counted. |
| `argument-hint` | string | OPT | — | — | — | Usage hint in /help |
| `keep-coding-instructions` | bool | — | — | — | OPT | Preserve default coding instructions |
| `user-invocable` | bool | OPT | — | — | — | `false` = hidden from / menu |
| `disable-model-invocation` | bool | OPT | — | — | — | `true` = only explicit /slug triggers |

**REQ** = required | **OPT** = optional | **—** = not applicable

### 2.2 Token Economics
[SOURCE: loadSkillsDir.ts:100-105]

```
CATALOG COST (always in context):
  name + description + whenToUse → roughTokenCountEstimation (chars ÷ 4)
  Example: 200 chars = ~50 tokens per skill, always loaded

INVOCATION COST (on-demand):
  Full SKILL.md content loaded only when user invokes /skill-name
  References/ loaded only when skill reads them

AMBIENT COST (always loaded, no opt-out):
  .claude/rules/*.md files — loaded every turn
  CLAUDE.md files — loaded every turn

ZERO COST (event-triggered):
  Hooks — only fire on matching events
  Output styles — only when active
```

**Creator optimization:**
- Short, focused `description` = lower catalog cost
- Long reference content in references/ = zero cost until invoked
- claude-md products: EVERY character is always in context — optimize aggressively
- 12 skills × 50 tokens each = ~600 tokens ambient catalog cost

### 2.3 Tool Restriction Patterns
[SOURCE: loadSkillsDir.ts, AgentTool.ts]

```yaml
# Whitelist (only these tools available):
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(npm test *)    # Glob pattern matching on command

# Blacklist (all tools EXCEPT these):
denied-tools:
  - Write
  - Edit
  - Bash

# Both: allowed-tools takes precedence, denied-tools further restricts
```

**Security patterns:**
- Read-only skills: `allowed-tools: [Read, Glob, Grep]`
- Analysis agents: `denied-tools: [Write, Edit]` (can read everything, write nothing)
- Scoped execution: `allowed-tools: [Bash(npm test *)]` (only test commands)

---

## 3. Context Window & Compact System

### 3.1 Context Sizes
[SOURCE: context.ts:9-98, 167-169]

| Model | Context Window | 1M Available? | Output Default | Output Upper |
|-------|:-------------:|:-------------:|:--------------:|:------------:|
| Opus 4.6 | 200K | Yes ([1m] suffix) | 64,000 | 128,000 |
| Sonnet 4.6 | 200K | Yes ([1m] suffix) | 32,000 | 128,000 |
| Haiku 4.5 | 200K | No | 32,000 | 64,000 |

### 3.2 AutoCompact — When Context Gets Full
[SOURCE: autoCompact.ts:63-70]

```
threshold = (contextWindow - 20,000 summary reserve - 13,000 buffer)

200K model → autocompact triggers at ~167,000 tokens
1M model   → autocompact triggers at ~967,000 tokens

Circuit breaker: 3 consecutive compact failures → stop trying
```

### 3.3 Compact Instructions — CRITICAL for Products
[SOURCE: compact/prompt.ts:133-143]

When Claude Code runs out of context, it summarizes the conversation. By default, the summary preserves what the model thinks is important — but YOUR product's priorities may differ.

**The `## Compact Instructions` section** in any memory file tells the compact system what to preserve:

```markdown
## Compact Instructions

When summarizing this conversation, always preserve:
- The product type and slug being worked on
- Current MCS scores and validation results
- Creator intent captured during /fill
- Active acceptance criteria
- Any error states or blockers
```

**Why this matters:**
- Without compact instructions, a 2-hour skill-building session loses product context on compaction
- The compact system is TEXT-ONLY — it cannot call tools to re-read files
- Compact instructions are your product's survival strategy for long sessions
- This section is recognized by Claude Code at `compact/prompt.ts:133-143`

### 3.4 How Compact Works Internally
[SOURCE: compact/prompt.ts:19-44, 61-220]

```
3 variants:
  BASE        — Full conversation summary (9 sections)
  PARTIAL     — Only recent messages summarized
  PARTIAL_UP_TO — Prefix summary for unseen recent messages

Analysis scratchpad:
  <analysis>[Claude's reasoning]</analysis>  → STRIPPED before injection
  <summary>[Final summary]</summary>          → KEPT in context

Constraints:
  - TEXT-ONLY: "Tool calls will be REJECTED and waste your only turn"
  - Max output: 20,000 tokens
  - Max turns: 1 (single-shot forked agent)

MicroCompact targets (tool-result level compression):
  Read, Shell, Grep, Glob, WebSearch, WebFetch, Edit, Write
```

### 3.5 Cache Architecture — How Prompt Caching Affects Your Product
[SOURCE: prompts.ts:106-115, systemPromptSections.ts:20-38, claudemd.ts:790, context.ts:155]

Claude Code's system prompt is split into two zones by an internal boundary marker:

```
┌─────────────────────────────────────────────┐
│  STATIC ZONE (cached globally)              │
│  Role, tools, guidelines, tone, efficiency  │
│  → Identical for ALL users of same build    │
│  → Cached and reused across millions of     │
│    requests (cost: near-zero after first)   │
├─────────────────────────────────────────────┤
│  __SYSTEM_PROMPT_DYNAMIC_BOUNDARY__         │
├─────────────────────────────────────────────┤
│  DYNAMIC ZONE (per-session)                 │
│  Environment info, memory, MCP, settings    │
│  → YOUR PRODUCT LIVES HERE                 │
│  → claude-md products are injected into     │
│    this zone every turn                     │
│  → Each character adds to per-turn cost     │
└─────────────────────────────────────────────┘
```

**What this means for creators:**

1. **claude-md products are in the DYNAMIC zone** — they're loaded every turn, every session. A badly-written claude-md product doesn't just cost the buyer tokens — it can fragment the prompt cache, increasing cost for ALL subsequent turns.

2. **skill/agent products have ZERO ambient cost** — they're only loaded when invoked. Size doesn't affect the prompt cache at all. Put your detailed content here.

3. **The compilation model:** Context is compiled ONCE at session start (memoized), then served every turn without recomputation. Changes to your files take effect on next session or after `/clear`. This means:
   - Don't design products that depend on mid-session file changes
   - State that must survive across turns should be in .meta.yaml or conversation, not in files you expect to re-read

4. **Each section is individually memoized** via a section registry pattern. Sections that MUST recompute every turn are explicitly marked as "DANGEROUS_uncached" with a mandatory reason — cache-breaking is treated as a conscious cost, not a default.

**Creator optimization:**
- claude-md: every character is ambient cost. Use `paths:` to scope. Decompose via @include.
- skill/agent: zero ambient cost. Rich references/ content is free until invoked.
- hooks: zero context cost. Event-driven, never in the prompt.

---

## 4. Settings Architecture

### 4.1 Resolution Chain (Later Wins)
[SOURCE: settings/constants.ts:7-22]

```
1. userSettings     — ~/.claude/settings.json           [TRUSTED]
2. projectSettings  — .claude/settings.json             [PARTIALLY TRUSTED]
3. localSettings    — .claude/settings.local.json       [TRUSTED]
4. flagSettings     — --settings CLI flag                [TRUSTED]
5. policySettings   — managed-settings.json / remote     [HIGHEST, TRUSTED]
```

### 4.2 Security Exclusions — CRITICAL for Hook Creators
[SOURCE: settings/settings.ts, autoMode files]

```
projectSettings (.claude/settings.json) is EXCLUDED from:
  ✗ Permission rules (allow/deny/ask)
  ✗ Auto-mode classifier config
  ✗ Dangerous mode activation

ONLY trusted sources (user, local, flag, policy) can:
  ✓ Set permission rules
  ✓ Configure auto-mode
  ✓ Enable bypass permissions
```

**Creator implication:** If your hooks product targets `.claude/settings.local.json` (localSettings) — permissions WILL work. If it targets `.claude/settings.json` (projectSettings) — permissions are SILENTLY IGNORED.

### 4.3 Defensive Parsing
[SOURCE: settings/settings.ts]

- All cached settings CLONED before return (prevent mutation)
- Invalid permission rules stripped BEFORE schema validation (one bad rule doesn't break the file)
- Drop-in files sorted alphabetically (later files override earlier)

---

## 5. Hook System

### 5.1 All 15 Hook Events
[SOURCE: hooks/hookEvents.ts, settings/types.ts]

| Event | Blocking? | Always Emitted? | Product Use Case |
|-------|:---------:|:---------------:|-----------------|
| **SessionStart** | No | Yes | Boot scripts, context loading, status display |
| **Setup** | No | Yes | First-run initialization |
| **PreToolUse** | **Yes** | No | Block/modify tool calls before execution |
| **PostToolUse** | No | No | React to tool results, logging |
| **PostToolUseFailure** | No | No | Error recovery, notifications |
| **UserPromptSubmit** | **Yes** | No | Validate/transform user input |
| **SubagentStart** | No | No | Monitor agent spawning |
| **Notification** | No | No | External notifications |
| **PermissionRequest** | **Yes** | No | Custom permission logic |
| **PermissionDenied** | No | No | Log denied permissions |
| **Elicitation** | **Yes** | No | Custom elicitation UI |
| **ElicitationResult** | No | No | Process elicitation results |
| **CwdChanged** | No | No | React to directory changes |
| **FileChanged** | No | No | React to file modifications |
| **WorktreeCreate** | No | No | React to worktree creation |

### 5.2 Hook Types
[SOURCE: schemas/hooks.ts]

| Type | Mechanism | Use Case |
|------|-----------|----------|
| **BashCommand** | Execute shell command | Scripts, git ops, notifications |
| **AgentHook** | Spawn agent | Complex analysis, content generation |
| **HttpHook** | HTTP request | Webhooks (Slack, Discord, CI/CD) |
| **PromptHook** | Inject prompt text | Context injection mid-session |

### 5.3 Hook Security
[SOURCE: ssrfGuard.ts, hooks implementation]

- SSRF guard protects HTTP hooks
- Deferred event delivery (max 100 pending events queue)
- Always-emitted events (SessionStart, Setup) need no opt-in
- All other events require explicit configuration
- Hook errors surface to user with full output

---

## 6. Skill/Agent System

### 6.1 Skill Loading Sources (Priority Order)
[SOURCE: loadSkillsDir.ts:67-94]

```
1. policySettings  — /etc/claude-code/.claude/skills/  [Enterprise]
2. userSettings     — ~/.claude/skills/                  [Personal global]
3. projectSettings  — .claude/skills/                    [Project-level]
4. plugin           — Plugin directory                   [Marketplace]
5. bundled          — Built into CC                      [Lowest]
6. mcp              — MCP server tools as skills         [Dynamic]
```

### 6.2 Agent Override Chain
[SOURCE: loadAgentsDir.ts]

```
built-in → plugin → user → project → flag → managed
(later silently shadows earlier with same name)
```

### 6.3 One-Shot Optimization
[SOURCE: AgentTool.ts — omitClaudeMd]

Built-in Explore and Plan agents skip CLAUDE.md loading entirely. This saves 5-15 Gtok/week globally. Product creators can leverage this: read-only analysis agents don't need project instructions.

### 6.4 Agent Memory Scopes
[SOURCE: AgentTool internals]

| Scope | Path | Persistence | Use Case |
|-------|------|-------------|----------|
| `user` | ~/.claude/ | Forever (global) | Personal preferences |
| `project` | .claude/agent-memory/ | Shared with team | Team knowledge |
| `local` | Session-only | Not persisted | Temporary state |

### 6.5 Agent Memory Snapshots
[SOURCE: AgentTool — AGENT_MEMORY_SNAPSHOT flag]

```
Path: .claude/agent-memory-snapshots/<agentType>/snapshot.json
Behavior: Auto-initialize agent from snapshot if local memory missing
Status: Gated by AGENT_MEMORY_SNAPSHOT feature flag
```

---

## 7. Product Type → Platform Mapping

### 7.1 Install Paths
[SOURCE: Multiple — validated S92, cross-referenced with product-dna/*.yaml]

**Note:** "Engine Install Target" = where MyClaude products install via `myclaude install`. "CC Native Path" = where Claude Code natively looks for that artifact type. These may differ because Engine products are designed for marketplace distribution via the skills system.

| Product Type | Engine Install Target | CC Native Path | Memory Type | Auto-Loaded? |
|-------------|----------------------|----------------|:-----------:|:------------:|
| skill | `.claude/skills/{slug}/` | .claude/skills/ | Not memory | No (on invoke) |
| agent | `.claude/skills/{slug}/` | .claude/commands/ (native) | Not memory | No (on invoke) |
| squad | `.claude/skills/{slug}/` | .claude/commands/ (native) | Not memory | No (on invoke) |
| system | `.claude/commands/{slug}/` | .claude/commands/ | Not memory | No (on invoke) |
| claude-md | `.claude/rules/{slug}.md` | .claude/rules/ | **Project** | **Yes (every turn)** |
| minds | `.claude/agents/{slug}.md` | .claude/agents/ | Not memory | No (on spawn) |
| hooks | `.claude/settings.local.json` | .claude/settings*.json | Not memory | No (event-triggered) |
| statusline | `~/.claude/statusline-scripts/` | ~/.claude/statusline-scripts/ | Not memory | No (on render) |
| output-style | `.claude/output-styles/{slug}.md` | .claude/output-styles/ | Not memory | No (when active) |
| application | `.claude/skills/{slug}/` | .claude/skills/ | Not memory | No (on invoke) |
| workflow | `.claude/skills/{slug}/` | .claude/skills/ | Not memory | No (on invoke) |
| design-system | `.claude/skills/{slug}/` | .claude/skills/ | Not memory | No (on invoke) |
| bundle | Multiple | Composite | Varies | Varies |

**Why agent/squad install to skills/ not commands/:** Engine products use the skill system for marketplace distribution (discoverable via / menu). The SKILL.md frontmatter makes them invokable. Internally, agent products spawn subagents via Agent() tool — the skill acts as an orchestrator entry point.

### 7.2 Token Cost by Product Type

| Type | Ambient Cost | Invocation Cost | Optimization Strategy |
|------|:------------:|:---------------:|----------------------|
| **claude-md** | **HIGH** (always loaded) | N/A | Every char matters. Minimize ruthlessly. |
| **skill** | LOW (catalog only) | MEDIUM (full content) | Short description, rich references/ |
| **agent/minds** | ZERO | HIGH (full content) | No ambient cost — size doesn't matter for catalog |
| **hooks** | ZERO | ZERO | Event-driven, never in context |
| **output-style** | ZERO | LOW (style prompt) | Only loaded when user selects |
| **statusline** | ZERO | ZERO | Runs in shell, not in context |
| **bundle** | SUM of components | SUM of components | Each component follows its own type rules |

### 7.3 Composability Contracts — How Products Connect

Products are designed to compose. A skill's output can feed a workflow's input. A system orchestrates multiple skills and agents. But for composability to work reliably, products need to declare their **interfaces**.

**Output Declaration** (in product's primary file or README):
```markdown
## Composability

**Produces:** {output_type} — {description}
  Format: {markdown | yaml | json | text}
  Example: "Produces: audit-report — structured quality analysis with scores and recommendations"

**Consumes:** {input_type} — {description}
  Format: {format}
  Example: "Consumes: domain-map — structured domain knowledge from /map"

**Pairs with:** {product_slugs or types}
  Example: "Pairs with: any workflow that needs quality-gated input"
```

**Why this matters:**
- Marketplace can suggest "compatible products" based on declared interfaces
- Buyers can build pipelines: skill A → workflow B → system C
- Creators design products that are part of an ecosystem, not isolated tools

This is enforced by D16 (Composability) in structural-dna.md and checked by /validate.

### 7.4 Architecture Patterns — Choosing the Right Product Type

When deciding which product type to build, match your problem to an architecture pattern:

| Pattern | Structure | Best Product Type | When to Use |
|---------|-----------|------------------|-------------|
| **Pipeline** | A→B→C→D | `workflow` | Steps happen in sequence, each depends on the previous |
| **Hub-and-Spoke** | Hub→[A,B,C]→Hub | `squad` | One coordinator distributes to specialists and collects results |
| **Multi-Agent** | Agents debate/collaborate | `squad` with D11 (Socratic Pressure) | Problem benefits from multiple contradicting perspectives |
| **Refinement Loop** | Generate→Evaluate→Refine→loop | `workflow` with step loops | First attempt is rarely good enough, quality needs iteration |
| **Cascading Enrichment** | A(+)→B(++)→C(+++) | `system` | Build complexity progressively, layer by layer |
| **Smart Router** | Gateway classifies→routes | `system` with D9 routing | Diverse inputs need different specialist handling |

**The test:** If you can describe your product as one of these patterns, you've chosen the right type. If your product doesn't fit any pattern, it might be trying to do too much — decompose it.

---

## 8. Feature Flags — Unreleased Capabilities
[SOURCE: tools.ts, query.ts, various feature gate files]

| Flag | Capability | Readiness |
|------|-----------|-----------|
| KAIROS | Proactive agent (Sleep, SendFile, PushNotification) | Design for autonomous products |
| AGENT_TRIGGERS | Scheduled agents (Cron) | Recurring task products |
| TEAMMEM | Shared team memory | Team-level products |
| COORDINATOR_MODE | Multi-agent coordinator/worker | Squad orchestration |
| CONTEXT_COLLAPSE | Context view projection | Context-heavy products |
| REACTIVE_COMPACT | Reactive compaction strategy | Long-session products |

**Creator guidance:** These flags exist in source but are not yet publicly available. Design products that will benefit when they activate — but don't depend on them today.

---

## 9. DX Patterns Worth Adopting

### 9.1 From Claude Code's 101 Commands
[SOURCE: Multiple command files]

| Pattern | CC Implementation | Product Opportunity |
|---------|------------------|-------------------|
| Chain-of-strategies | Compact: session→reactive→micro | Validate: quick→deep→expert |
| Graceful degradation | Missing feature → message + fix link | Missing dep → install instructions |
| Doctor health checks | >40K warning, >9K agents, >25K MCP | Product health, token budget |
| Safety-first | Never --amend, --no-verify, force push | Never publish without confirmation |
| Transparent state | Git status, plan, balance | MCS scores, phase, trajectory |
| Atomic updates | Permission changes in single tx | State transitions atomically |

### 9.2 Non-Dev UX Patterns
[SOURCE: OBSIDIAN persona analysis]

| Pattern | What It Means |
|---------|--------------|
| Plain language errors | "Missing a README" not "Stage 1 structural check failed" |
| Guided choices | 2-4 options with action verbs ("Publish", "Fix", "Skip") |
| Progressive reveal | Type selection → relevant options → deep config if asked |
| Domain adaptation | Detect creator.yaml profile.type → adapt language |
| Contextual next step | ALWAYS show what to do next |

### 9.3 System Prompt Section Architecture — How Anthropic Organizes Instructions
[SOURCE: prompts.ts:175-442, 444-576]

Anthropic organizes Claude Code's system prompt in 7 functional sections. Each serves ONE cognitive dimension. Products that mirror this structure work better because they align with how the model's own instructions are structured.

| Section | Cognitive Function | Product Equivalent |
|---------|-------------------|-------------------|
| **Intro** | Identity + boundaries | Who this product IS and what it does NOT do |
| **System** | Metacognition | How to handle tags, hooks, permissions |
| **Doing Tasks** | Execution heuristics | Domain-specific how-to guidance |
| **Executing Actions** | Risk assessment | When to ask vs act, reversibility checks |
| **Using Your Tools** | Tool selection | Which tools to use, dedicated > bash |
| **Tone and Style** | Communication norms | Voice, formatting, emoji rules |
| **Output Efficiency** | Output constraints | Conciseness, structure, length |

**Creator takeaway:** Structure your product's primary file in functional layers:
1. **Identity** — Who/what is this product (D1 Activation Protocol)
2. **Knowledge** — What it knows, references to load (D3 Progressive Disclosure)
3. **Execution** — How it processes and decides (D7 Pre-Execution Gate, D9 Orchestrate)
4. **Constraints** — What it must NOT do (D2 Anti-Pattern Guard)
5. **Output** — How it communicates results (D4 Quality Gate, D6 Confidence Signaling)

This isn't aesthetic. It mirrors how Claude Code's own system prompt is structured — and the model pays more attention to content at the END (Principle MP-1: Recency = Authority). Put your most critical constraints LAST.

---

## 10. Execution Engine — How Claude Code Runs
[SOURCE: query.ts:219-318, QueryEngine.ts:184-250]

### 10.1 The Query Loop

```
User input → QueryEngine.submitMessage()
  → processUserInput()     (slash commands, attachments)
  → recordTranscript()     (BEFORE API call — crash-safe)
  → queryLoop() while(true)
    1. snip              — token-free history trimming
    2. microcompact      — inline tool result compression
    3. context-collapse  — context view projection
    4. autocompact       — full summarization if near limit
    5. blocking check    — surface error if irrecoverable
    6. callModel()       — streaming API call
    7. tool execution    — tools queued during stream, parallel
    8. error recovery    — 3-stage cascade
    9. stop hooks + budget check
    10. continue OR return
```

### 10.2 Error Recovery Strategies

**prompt_too_long (413):**
1. Context collapse drain → retry
2. Reactive compact (full summary) → retry
3. Surface error to user

**max_output_tokens:**
1. Escalate 8K → 64K
2. Inject "resume directly" meta message
3. After 3 failures → surface error

**Model fallback:**
On FallbackTriggeredError → switch model, strip thinking blocks

---

## 11. MyClaude CLI Integration
[SOURCE: myclaude CLI v0.9.0 — live system, verified 2026-04-06]

The MyClaude CLI (`@myclaude-cli/cli`) is the distribution layer. The Engine creates → the CLI distributes.

### 11.1 CLI Commands Relevant to Product Creators

| Command | What It Does | When to Use |
|---------|-------------|-------------|
| `myclaude init` | Scaffold basic product structure | Alternative to Engine /create (less DNA) |
| `myclaude validate` | Check vault.yaml, secrets, frontmatter, license | Engine Stage 6 calls this on .publish/ |
| `myclaude publish` | Ship to myclaude.sh marketplace | Engine /publish delegates to this |
| `myclaude doctor` | System health check (auth, API, lockfile) | Pre-publish sanity check |
| `myclaude workspace` | Scan project Claude Code setup | Diagnose buyer's environment |
| `myclaude workspace --recommend` | Gap analysis + product recommendations | Discovery engine for buyers |
| `myclaude search` | Search marketplace catalog | Find competing/complementary products |
| `myclaude trending` | Top 10 products by downloads | Market intelligence |
| `myclaude my-products` | List creator's published products | Track portfolio performance |
| `myclaude stats {slug}` | Downloads, revenue, ratings | Per-product analytics |
| `myclaude info {slug}` | Detailed product page | Research before publishing |

### 11.2 CLI Validate Checks (6 checks)

```json
// myclaude validate --json output:
{
  "checks": [
    {"check": "vault.yaml",       "pass": true},  // Manifest exists + valid
    {"check": "files",            "pass": true},  // File count + size
    {"check": "secret scan",      "pass": true},  // No secrets in published files
    {"check": "license",          "pass": true},  // Valid SPDX identifier
    {"check": "frontmatter",      "pass": true},  // Primary file has valid frontmatter
    {"check": "agent-skills-spec","pass": true}   // Recommended fields present
  ],
  "manifest": { /* vault.yaml contents */ },
  "valid": true
}
```

### 11.3 Engine ↔ CLI Pipeline

```
ENGINE /create → scaffold with DNA patterns (20 structural patterns)
ENGINE /fill   → guided content filling (persona-aware, mid-fill persistence)
ENGINE /validate → 7-stage quality check (DNA + MCS scoring)
ENGINE /package → strip WHY, generate manifests, stage .publish/
CLI    myclaude validate → check .publish/ integrity (vault, secrets, frontmatter)
CLI    myclaude publish → ship to myclaude.sh
CLI    myclaude install → buyer installs to their Claude Code
```

The Engine adds quality DNA that the CLI cannot. The CLI adds marketplace distribution that the Engine cannot. Together they form a complete creation-to-distribution pipeline.

### 11.4 MCP Integration — Claude Code ↔ Marketplace Native Bridge

Running `myclaude setup-mcp` configures 5 MCP tools that Claude Code can call DIRECTLY:

| MCP Tool | What It Does | Engine Use Case |
|----------|-------------|-----------------|
| `vault_search` | Search marketplace catalog | /create: competitive scan before building |
| `vault_info` | Product details by slug | /validate: compare against published versions |
| `vault_install` | Install product | /publish: test install flow |
| `vault_list` | List installed products | /status: show buyer's perspective |
| `vault_update` | Update installed products | /status: check for updates |

**When MCP is configured:** Engine skills can call these tools directly instead of shelling out to `myclaude` commands. This is faster, more reliable, and enables richer integration (e.g., /create can search for competing products before the creator starts building).

**Setup:** `myclaude setup-mcp` or `myclaude setup-mcp --global`

### 11.5 CLI Auth & Config

```bash
myclaude login          # Authenticate with myclaude.sh
myclaude whoami         # Check current user
myclaude config get     # View CLI configuration
myclaude doctor         # System health (score /10)
myclaude doctor --fix   # Auto-fix systemic issues
```

---

## 12. Security Boundaries — What Product Creators Must Know
[SOURCE: competitive-intelligence S97 — 68 CVEs, 1,184 malicious skills documented across ecosystem]

### 12.1 The Threat Landscape (2026)

The Claude Code product ecosystem has documented supply chain attacks at scale:
- **36.82%** of skills on public registries have security flaws (Snyk ToxicSkills, 3,984 skills scanned)
- **1,184+** confirmed malicious skills across typosquatting campaigns (ClawHavoc: crypto, YouTube, Polymarket)
- **70+** CVEs in the MCP protocol ecosystem (no built-in auth, no default sandbox)
- **17,500+** internet-exposed OpenClaw instances vulnerable to WebSocket token theft

**Implication for creators:** Products you build may reference MCP servers, install packages, or execute shell commands. Each is an attack vector. The Engine's /validate runs automated threat scans against `references/quality/known-threats.yaml`.

### 12.2 Settings Trust Boundaries

| Layer | File | Trust Level | Permissions Work? |
|-------|------|------------|-------------------|
| User global | `~/.claude/settings.json` | TRUSTED | Yes |
| Project shared | `.claude/settings.json` | PARTIALLY TRUSTED | **No — silently ignored** |
| Project local | `.claude/settings.local.json` | TRUSTED | Yes |

**Critical for hook products:** Hooks that set permissions MUST target `.claude/settings.local.json`. Hooks in `.claude/settings.json` will appear to work but permissions are silently dropped. This is intentional security — project-shared settings cannot grant permissions because any repo collaborator could modify them.

### 12.3 Defense-in-Depth for Products

No single security layer is sufficient. Product creators should implement layered defenses:

1. **Layer 1 — permissions.deny:** Block known-dangerous tools/patterns in frontmatter
2. **Layer 2 — PreToolUse hooks:** Runtime interception before execution (only blocking gate)
3. **Layer 3 — External secrets management:** Never hardcode credentials; use env vars or Claude Code's native secret handling
4. **Layer 4 — Manual approval gates:** Require human confirmation for destructive/irreversible actions

### 12.4 MCP Server Vetting (for products that reference MCP)

Before referencing any MCP server in a product:
1. **Author identity:** Public, verifiable. Anonymous authors = higher risk
2. **Repo activity:** Recent commits, responsive to issues. Abandoned repos = unpatched vulns
3. **Version pinning:** Always pin exact version. Never `latest`. The ecosystem has documented "rug pull" attacks where benign servers turn malicious after gaining trust
4. **Transport security:** HTTP Streamable is vulnerable to CORS/CSRF by design. Document any HTTP-based MCP usage explicitly

### 12.5 Known Dangerous Patterns (BLOCKING in /validate)

| Pattern | Why Dangerous | What to Do |
|---------|--------------|------------|
| `enableAllProjectMcpServers` | Bypasses MCP trust dialog (CVE-2025-59536) | Never use in product settings |
| `ANTHROPIC_BASE_URL` override | Enables API key theft (CVE-2026-21852) | Never override in product files |
| `curl\|sh` or `wget\|sh` | Remote code execution | Use package managers with checksum verification |
| `eval()` in handlers | Code injection vector | Use explicit function calls, not eval |
| `base64 -d \| sh` | Obfuscated code execution | Never decode-and-execute in products |

See `references/quality/known-threats.yaml` for the complete registry including malicious authors, IOCs, and vulnerable MCP servers.

---

*CC Platform Contract v2.1.0 — 40 Crown Jewels + CLI integration + Context Engineering Codex + Security Boundaries.*
*Every claim traced to source. Zero inference without [SOURCE:].*
*v1.0: Alan Nicolas (Knowledge Architect) | S92→S93*
*v2.0: Codex enrichment (cache architecture, @include constraints, type labels, section taxonomy) | S94*
*v2.1: Security boundaries from competitive intelligence extraction (68 CVEs, threat landscape) | S97*
