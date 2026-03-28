# MyClaude Studio Engine
**v2.0.0** | **Edition:** detect at boot | **myclaude.sh**

> Create, validate, package, publish Claude Code products with structural DNA.

## GLOSSARY

| Term | Meaning |
|------|---------|
| Creator | Human using this Engine to build products |
| Product | Publishable artifact (9 types below) |
| DNA | 18 structural patterns defining quality (`structural-dna.md`) |
| MCS | Quality tiers: MCS-1 (>=75%) MCS-2 (>=85%) MCS-3 (>=92% PRO) |
| WHY comment | `<!-- WHY: D{N} ({Name}) — ... -->` in templates. Stripped by /package |
| .meta.yaml | Per-product state: type, phase, scores. In `workspace/{slug}/` |
| LITE | Free: 10 skills, MCS-1/2 validation |
| PRO | Paid add-on: 5 agents + MCS-3 + market intelligence |

## BOOT

```
1. READ STATE.yaml → version, edition, workspace. Missing → defaults.
2. READ creator.yaml → name, type, level. Missing → "Run /onboard (~3 min)."
3. DETECT EDITION → Glob .claude/skills/forge-master/SKILL.md → PRO or LITE
4. SCAN WORKSPACE → Glob workspace/*/.meta.yaml → read phase, flag stale (>30d)
5. DASHBOARD → Engine v{ver} [{ed}] | Creator: {name} | Products: {N}
```

## SKILLS (10)

| Command | Does | Output |
|---------|------|--------|
| `/onboard` | 8 questions → creator profile | creator.yaml |
| `/map [topic]` | Extract domain knowledge | workspace/domain-map.md |
| `/create {type}` | Scaffold + DNA + WHY comments | workspace/{slug}/ + .meta.yaml |
| `/fill [slug]` | Walk sections, ask, write answers | state → content |
| `/validate [--level=N --fix --batch]` | 7-stage DNA pipeline | scored report, state → validated |
| `/package [slug]` | Strip WHY → vault.yaml + plugin.json | .publish/ |
| `/publish [slug]` | Summary → confirm → myclaude publish | live on marketplace |
| `/test [slug]` | Worktree isolation, 3 scenarios | pass/fail report |
| `/status` | Dashboard | formatted status |
| `/help` | Command list + edition | reference |

PRO adds: `/market` (Market Scout), `/my-products` (stats via CLI).
LITE → PRO message: "Requires MyClaude Studio Pro. Install from myclaude.sh."

## 9 TYPES

| Type | File | Install Target | DNA |
|------|------|----------------|-----|
| skill | SKILL.md | .claude/skills/{slug}/ | product-dna/skill.yaml |
| agent | AGENT.md | .claude/skills/{slug}/ | product-dna/agent.yaml |
| squad | SQUAD.md | .claude/skills/{slug}/ | product-dna/squad.yaml |
| workflow | WORKFLOW.md | .claude/skills/{slug}/ | product-dna/workflow.yaml |
| design-system | DESIGN-SYSTEM.md | myclaude-products/{slug}/ | product-dna/design-system.yaml |
| prompt | PROMPT.md | .claude/skills/{slug}/ | product-dna/prompt.yaml |
| claude-md | CLAUDE.md | .claude/rules/{slug}.md | product-dna/claude-md.yaml |
| application | APPLICATION.md | myclaude-products/{slug}/ | product-dna/application.yaml |
| system | SYSTEM.md | .claude/skills/{slug}/ | product-dna/system.yaml |

## VALIDATION (7 Stages)

| Stage | Name | Blocking | Gates |
|-------|------|----------|-------|
| 1 | Structural | yes | files exist |
| 2 | Integrity | yes | no placeholders, refs resolve |
| 3 | DNA Tier 1 | yes | D1,D2,D3,D4,D13,D14 → MCS-1 |
| 4 | DNA Tier 2 | no | D5-D8,D15-D17 → MCS-2 |
| 5 | DNA Tier 3 | no | D9-D12,D18 → MCS-3 (PRO) |
| 6 | CLI Preflight | yes | myclaude validate |
| 7 | Anti-Commodity | never | 3 coaching questions |

**Score:** `(DNA×0.50) + (Structural×0.30) + (Integrity×0.20)`

## STATE MACHINE

```
/create→scaffold → /fill→content → /validate→validated → /package→packaged → /publish→published
                         ↑ file edited = state regresses ←──────────────────────────────┘
```

## EDITIONS

**LITE:** 10 skills, Stages 1-4+6, MCS-1/2.
**PRO** (forge-master/ detected): adds 5 agents — Cartographer, Architect, Sentinel, Scout, Master.

## ADAPTATION

| Creator Type | Behavior |
|---|---|
| developer | scaffolding, CLI, architecture |
| prompt-engineer | prompt structure, exemplars |
| domain-expert | AI-assisted creation, packaging |
| marketer | market opportunities, pricing |
| agency | batch ops, multi-product |
| hybrid | ask per session |

Calibrate: `technical_level`, `preferred_categories`, `pricing_strategy`.

## RULES

```
NEVER create files outside workspace/
NEVER publish without explicit confirmation
NEVER skip validation before packaging
NEVER reference nonexistent files in scaffolds
NEVER leave placeholders in published products
NEVER reimplement CLI logic — invoke myclaude commands
NEVER assume creator profile — load creator.yaml first
NEVER modify files in /validate unless --fix passed
NEVER activate Forge Master for single-agent requests
NEVER include .meta.yaml or domain-map.md in .publish/
```

## FILE MAP

```
CLAUDE.md                ← YOU ARE HERE
STATE.yaml               ← Engine state
config.yaml              ← Scoring, routing, thresholds, pipeline
structural-dna.md        ← 18 DNA patterns (D1-D18)
quality-gates.yaml       ← State transitions + regression
product-dna/             ← 9 type-specific DNA requirements
.claude/skills/          ← 10 skills
references/
  product-specs/         ← 9 canonical file structures
  exemplars/             ← 9 gold-standard examples
  quality/               ← MCS spec, anti-patterns, anti-commodity
  best-practices/        ← Naming, licensing, versioning
  market/                ← Pricing, categories
templates/               ← 9 scaffold templates with WHY comments
workspace/               ← Active builds (gitignored)
```

## LOAD ON DEMAND

| Trigger | Load |
|---------|------|
| /create | product-dna/{type}.yaml, product-specs/{type}, templates/{type}/ |
| /validate | product-dna/{type}.yaml, config.yaml, quality-gates.yaml |
| /fill | product-dna/{type}.yaml, product-specs/{type} |
| /package | config.yaml (vault_defaults), product-dna/{type}.yaml |
| quality question | references/quality/mcs-spec.md |
| pricing question | references/market/pricing-guide.md |
| DNA question | structural-dna.md |

Context footprint: < 5% of session window.

---

*MyClaude Studio Engine v2.0.0 — myclaude.sh*
