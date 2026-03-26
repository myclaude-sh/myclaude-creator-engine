# MyClaude Creator Engine
**Version:** 1.0.0 | **Product:** MyClaude Creator Engine | **Marketplace:** myclaude.sh

> The official creation studio for producing, validating, packaging, and publishing
> products to the MyClaude marketplace. Skills-first. Quality-enforced. CLI-integrated.

---

## BOOT SEQUENCE

Execute on every session start:

```
1. READ creator.yaml
   → EXISTS: load profile into context, greet by creator type
   → MISSING: "No creator profile found. Run /onboard to get started (takes ~3 min)."

2. DETECT WORKSPACE STATE
   → Glob workspace/*/.engine-meta.yaml
   → For each found: read status, last_validated, mcs_target
   → Flag stale builds (>30 days since last validation)

3. READ .engine-meta.yaml (root, if exists)
   → Load engine version, last command, last publish

4. SHOW ENGINE STATUS
   Profile: {creator name} ({type}) | Products in progress: {N} | Last validated: {date}
   Active workspace: {list slugs or "empty"}
   → If stale builds exist: "⚠ {N} product(s) not validated in 30+ days."
```

---

## SKILL ROUTING TABLE

All commands are Claude Code skills in `.claude/skills/{name}/SKILL.md` with official
Anthropic frontmatter. They appear automatically in the `/` autocomplete menu.

### P0 — Core Creation

| Command | Skill | Description |
|---------|-------|-------------|
| `/onboard` | `.claude/skills/onboard/` | Set up creator profile (creator.yaml) |
| `/create [type]` | `.claude/skills/create/` | Scaffold new product — routes to category |
| `/validate [flags]` | `.claude/skills/validate/` | Run MCS validation (--level=1\|2\|3, --fix, --batch) |
| `/package` | `.claude/skills/package/` | Strip guidance, generate vault.yaml, stage .publish/ |
| `/publish` | `.claude/skills/publish/` | Full publish workflow to myclaude.sh |
| `/create-content` | `.claude/skills/create-content/` | Guide content filling after scaffold |
| `/test` | `.claude/skills/test/` | Sandbox test product against sample inputs |

### P0 — Quality & Coaching

| Command | Skill | Description |
|---------|-------|-------------|
| `/differentiate` | `.claude/skills/differentiate/` | Anti-commodity coaching (Porter + Godin + Ries) |
| `/quality-review` | `.claude/skills/quality-review/` | Deep MCS-3 quality audit (Feathers + Deming + Popper) |

### P0 — Utility

| Command | Skill | Description |
|---------|-------|-------------|
| `/engine-status` | `.claude/skills/engine-status/` | Show profile, workspace state, stale builds |
| `/engine-help` | `.claude/skills/engine-help/` | List all available commands |

### P0 — Workflow Shortcuts

| Shortcut | Skill | Pipeline |
|----------|-------|----------|
| `/quick-skill` | `.claude/skills/quick-skill/` | `/create skill` → `/validate` → `/package` → `/publish` |
| `/quick-publish` | `.claude/skills/quick-publish/` | `/validate` → `/package` → `/publish` |

### Internal Agents (not user-invocable, Claude uses when needed)

| Skill | Purpose |
|-------|---------|
| `.claude/skills/market-scan/` | Market opportunity analysis (available for future `/scan-market`) |
| `.claude/skills/packaging-review/` | README/tag/metadata optimization during packaging |
| `.claude/skills/domain-consult/` | Category-specific guidance during scaffolding |

### FUTURE — P1 (Creation Phase)

| Command | Status |
|---------|--------|
| `/create-content` | AVAILABLE — `.claude/skills/create-content/` |
| `/generate-docs` | FUTURE — P1 |
| `/upgrade` | FUTURE — P1 |

### FUTURE — P2 (Intelligence Phase)

| Command | Status |
|---------|--------|
| `/scan-market` | FUTURE — P2 (agent ready at `.claude/skills/market-scan/`) |
| `/price` | FUTURE — P2 |
| `/analytics` | FUTURE — P2 |

When a FUTURE command is invoked: "This command is on the roadmap (Phase {N}). Currently available: run `/engine-help` for the full list."

---

## MCS ENFORCEMENT RULES

**MCS = MyClaude Creator Spec** — 3-tier quality system.

```
MCS-1 (Bronze): Minimum viable quality. Structure present, no broken refs, README exists.
MCS-2 (Silver): Anti-Commodity Gate required. Unique value prop documented.
MCS-3 (Gold):   Agent quality review + exemplar comparison.
```

**Hard Rules — never bypass:**

1. **NEVER publish without MCS-1 validation passing.** If `/publish` is called without
   a passing validation: run MCS-1 checks first, block if failures exist.

2. **Anti-Commodity Gate required for MCS-2+** (CE-D9). Before approving MCS-2,
   invoke `/differentiate` skill if differentiation score is LOW.
   This coaches, never blocks — creator can override with explicit intent.

3. **Validation is non-destructive** (CE-D13). Never modify product files without
   explicit `--fix` flag. Report issues, let creator decide.

4. **Confirm before publish.** Always show summary (product name, MCS level, price,
   category) and ask for explicit confirmation before invoking CLI publish.

5. **CLI PUBLISH — AVAILABLE** (CE-D33 resolved per CONDUIT WP-20).
   The `myclaude publish` command is fully functional. The Engine
   invokes it directly from the .publish/ directory after /package.

---

## CREATOR CONTEXT

Load `creator.yaml` at session start and apply adaptive behavior:

| Creator Type | Engine Behavior |
|-------------|-----------------|
| **developer** | Lead with scaffolding, show CLI integration, expose architecture docs |
| **prompt-engineer** | Focus on prompt structure, context engineering, exemplar references |
| **domain-expert** | Emphasize AI-assisted creation, packaging, market positioning |
| **marketer** | Lead with market opportunities, pricing benchmarks, competitive positioning |
| **agency** | Show batch operations, multi-product workspace management, team patterns |
| **hybrid** | Ask which mode for this session, then apply accordingly |

Creator profile fields to inject into every decision:
- `expertise_domains` — tailor vocabulary and examples to creator's domain
- `technical_level` — calibrate how much scaffolding detail to explain
- `preferred_categories` — prioritize templates and exemplars for these types
- `monetization_intent` — free / paid / both — affects packaging recommendations

If `creator.yaml` is missing a field, ask once and update the file.

---

## ECOSYSTEM INTEGRATION

**MyClaude CLI** — available commands (CE-D28: Engine invokes CLI, never reimplements):

| Command | Purpose |
|---------|---------|
| `myclaude search <query>` | Search marketplace products |
| `myclaude info <product-id>` | Get product details |
| `myclaude install <product-id>` | Install a product |
| `myclaude list` | List installed products |
| `myclaude login` | Authenticate with MyClaude |
| `myclaude logout` | Log out |
| `myclaude whoami` | Show current authenticated user |
| `myclaude uninstall <product-id>` | Remove a product |
| `myclaude status` | Show CLI + marketplace connection status |

**CLI PUBLISH — AVAILABLE** (CE-D33 resolved per CONDUIT WP-20).
The `myclaude publish` command is fully functional. The Engine invokes it
directly from the `.publish/` directory after `/package`.

**Marketplace:** https://myclaude.sh

---

## WORKSPACE RULES (CE-D41)

- All product creation happens inside `workspace/{product-slug}/`
- Never create product files outside `workspace/` during a creation session
- Each product has its own `.engine-meta.yaml` tracking: `created_at`, `last_validated`,
  `mcs_target`, `status` (scaffolded | in-progress | validated | packaged | published)
- Multiple products can coexist in workspace simultaneously
- `workspace/` is gitignored — products are copied out during `/package`

---

## ANTI-PATTERNS

```
NEVER create product files outside workspace/ during /create
NEVER publish without creator explicit confirmation
NEVER skip validation before packaging
NEVER reference files that don't exist in the scaffold
NEVER leave placeholder content (TODO, lorem ipsum) in published products
NEVER reimplement CLI logic — invoke myclaude CLI commands (CE-D28)
NEVER assume creator profile — always load creator.yaml first
NEVER modify files with /validate unless --fix is explicitly passed (CE-D13)
```

---

## REFERENCES

| Resource | Path |
|----------|------|
| Product specs (9 types) | `references/product-specs/` |
| MCS specification | `references/quality/mcs-spec.md` |
| Anti-patterns | `references/quality/anti-patterns.md` |
| Anti-commodity guide | `references/quality/anti-commodity.md` |
| Gold-standard exemplars | `references/exemplars/` |
| Pricing benchmarks | `references/market/pricing-guide.md` |
| Skill best practices | `references/best-practices/skill-best-practices.md` |
| Naming guide | `references/best-practices/naming-guide.md` |
| Shared vocabulary | `references/shared-vocabulary.md` |
| Caching strategy | `references/caching-strategy.md` |

---

*MyClaude Creator Engine v1.0.0 — myclaude.sh*
