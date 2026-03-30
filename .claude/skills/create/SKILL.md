---
name: create
description: >-
  Scaffold a new product with MCS-1 valid structure and WHY comments. Supports all
  9 categories. Use when the creator says 'new skill', 'create', 'scaffold', 'start
  building', or wants to start a new product.
argument-hint: "[product-type]"
---

# Scaffolder

Generate complete, MCS-1-valid project structure for any product type with guidance comments baked in.

**When to use:** Starting a new product — any of the 9 categories.

**When NOT to use:** When the product already exists in `workspace/` and you want to add content (use `/fill`). Do not use to overwrite an existing scaffold unless `--force` is specified.

---

## Activation Protocol

1. Read `creator.yaml` from project root — load defaults (`default_category`, `default_license`, `quality_target`). If `creator.yaml` is missing → respond: "Profile not found. Run `/onboard` first (~3 min)." and stop.
2. Identify which category was requested (from sub-command or by asking)
3. **Show the destination first** — Load the exemplar for this category from `references/exemplars/{category}-exemplar.md`. Show a condensed preview (title, structure, key sections) so the creator understands what "great" looks like before building. "Here's what an MCS-3 {category} looks like. Yours will follow this structure."
4. Load DNA requirements from `product-dna/{category}.yaml` — inject required DNA patterns into scaffold
5. Load discovery questions from `${CLAUDE_SKILL_DIR}/references/discovery-questions.md` for that category
6. Load the product spec from `references/product-specs/{category}-spec.md`
7. Load the scaffold template from `templates/{category}/`
8. **Load domain-map.md** if it exists in `workspace/domain-map.md` — prefill scaffold sections with domain knowledge
9. Generate scaffold in `workspace/{product-slug}/` with DNA patterns as sections + WHY comments
10. Create `.meta.yaml` with v2.0 schema (product.type, state.phase=scaffold, mcs_target)
11. Move `workspace/domain-map.md` → `workspace/{product-slug}/domain-map.md` if it was loaded
12. After scaffold is generated, suggest: "Run `/fill` to add your expertise, or start editing directly."

---

## Core Instructions

### ROUTER LOGIC

When invoked as `/create` with no argument, determine creator's comfort level first.

**If creator.yaml exists AND technical_level is advanced/expert**, show the direct menu:

```
What do you want to create?

  1. skill       — A reusable capability Claude can run
  2. agent       — A specialized persona with domain expertise
  3. squad       — A team of coordinated agents
  4. workflow    — An automated multi-step process
  5. ds          — A design system (tokens, components, exports)
  6. prompt      — A structured, reusable prompt template
  7. claude-md   — A project-specific CLAUDE.md configuration
  8. app         — A deployable application
  9. system      — A composite system (skills + agents + workflows)
  10. bundle     — A package of connected products (skills + agents + squads + workflow + system)

Enter number or name:
```

**If creator is beginner/intermediate OR type is domain-expert/operator/marketer**, use need-based routing:

```
Tell me what you want to build — in your own words.

Examples:
  "I want Claude to analyze my financial reports every week"
  "I need a team that handles content creation for my brand"
  "I want to automate my client onboarding process"
  "I want a reusable prompt for writing sales emails"
  "I need a set of rules for how Claude works on my projects"
```

Then map the need to a product type using these rules:

| Need Pattern | Recommended Type | Reasoning |
|---|---|---|
| "I want Claude to do X" (single task) | **skill** | One focused capability |
| "I want a specialist that knows about X" | **agent** | Persistent persona + domain knowledge |
| "I need a team that handles X" | **squad** | Multiple agents coordinating |
| "I want to automate X step by step" | **workflow** | Sequential process automation |
| "I want a reusable prompt for X" | **prompt** | Structured template |
| "I need rules/standards for my project" | **claude-md** | Project configuration |
| "I need a complete solution for X" | **system** | Multi-type composite |
| "I want a tool/app that does X" | **application** | Deployable software |
| "I need consistent visual patterns" | **design-system** | Tokens + components |
| "I want a package of connected products" | **bundle** | Skills + agents + squads + workflow + system |

After recommending, explain in one sentence why that type fits, then proceed to the standard flow (exemplar preview → discovery questions → scaffold).

Direct sub-commands skip this menu and go straight to the category flow:
- `/create skill` → Skill creation flow
- `/create agent` → Agent creation flow
- `/create squad` → Squad creation flow
- `/create workflow` → Workflow creation flow
- `/create ds` → Design System creation flow
- `/create prompt` → Prompt creation flow
- `/create claude-md` → CLAUDE.md creation flow
- `/create app` → Application creation flow
- `/create system` → System creation flow
- `/create bundle` → Bundle creation flow

### UNIVERSAL CREATION FLOW

After category is identified:

**Step 1 — Name + Description**

```
Product name: (e.g., "security-audit-skill", "sales-email-prompt")
One-line description: (what does it do?)
```

Derive `{product-slug}` from name: lowercase, hyphens, no spaces.

Validate slug against regex `^[a-z0-9][a-z0-9-]{2,39}$` (see `references/best-practices/naming-guide.md`). If invalid, explain the format rules and ask for a corrected name.

If `workspace/{product-slug}/` already exists → respond: "Product `{slug}` already exists. Use `/fill` to continue working on it, or `/create --force` to reset the scaffold." Do not overwrite without `--force`.

**Tip:** If the creator hasn't run `/map` yet and the product involves deep domain knowledge, suggest: "Consider running `/map` first to structure your domain expertise — `/create` will use that knowledge automatically."

**Step 2 — Discovery Questions**

Load and ask all category-specific questions from `${CLAUDE_SKILL_DIR}/references/discovery-questions.md`.

Ask them conversationally, not as a form dump. Wait for answers before generating.

**Step 3 — Load Defaults from creator.yaml**

Pre-populate scaffold with:
- `license` ← `creator.preferences.default_license`
- `version` ← `1.0.0` (always start here)
- `author` ← `creator.name` + `creator.myclaude_username`
- Quality target awareness ← `creator.preferences.quality_target` (determines how many optional sections to pre-populate)

**Step 4 — Generate Scaffold**

Create directory `workspace/{product-slug}/` and all required files for the category.

Every generated file must include guidance comments:
```
<!-- WHY: Describe what the skill does in 1-2 sentences. Be specific about the problem it solves. -->
```

These are stripped during `/package`. (CE-D12)

Create `.meta.yaml` in the product directory `workspace/{product-slug}/`:

```yaml
# Product metadata — not distributed, stripped during /package
product:
  slug: "{product-slug}"
  type: "{category}"               # skill|agent|squad|workflow|design-system|prompt|claude-md|application|system
  created: "{YYYY-MM-DD}"
  mcs_target: "{MCS-1|MCS-2|MCS-3}"

state:
  phase: "scaffold"                # scaffold | content | validated | packaged | published
  last_validated: null
  last_validation_score: null
  dna_compliance:
    tier1: null                    # 0-100
    tier2: null
    tier3: null
  overall_score: null
  last_tested: null
  test_result: null              # "pass" | "fail" | null
  test_scenarios: null           # "{passed}/{total}" | null

history:
  created_at: "{YYYY-MM-DD}"
  validated_at: []                 # append timestamps
  packaged_at: null
  published_at: null
  version: "1.0.0"
```

**Step 5 — MCS-1 Structural Validation**

Before showing the scaffold to the creator, silently verify:
- All required files for the category are present
- All required metadata fields exist (name, description, category, version, license)
- README.md skeleton is present with required sections

If structural validation fails, fix automatically and note what was corrected.

**Step 6 — Print Next Steps**

```
Scaffold created: workspace/{product-slug}/

Files generated:
  {list of generated files}

Next steps:
  [ ] Run /fill to add your expertise with guided extraction
  [ ] Or edit files directly — WHY comments explain each section
  [ ] Run /validate to check quality
  [ ] Run /package + /publish when ready

Tip: The WHY comments (<!-- WHY: ... -->) explain what each section needs.
     They are stripped automatically during /package.
```

### PER-CATEGORY SCAFFOLD STRUCTURES

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
├── SQUAD.md              # Squad definition + routing
├── agents/               # Individual agent definitions
│   └── .gitkeep
├── config/               # Routing and handoff config
│   └── routing.yaml
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

**prompt:**
```
workspace/{slug}/
├── PROMPT.md             # Prompt definition + variables
├── variants/             # Alternative versions
│   └── .gitkeep
├── examples/             # Usage examples
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
├── SYSTEM.md             # System definition + composition
├── skills/               # Included skills
│   └── .gitkeep
├── agents/               # Included agents
│   └── .gitkeep
├── config/               # System configuration
│   └── .gitkeep
└── README.md
```

### PREFILLING STRATEGY

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
2. **Load exemplars:** Read `references/exemplars.md`
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

---

## Output Structure

```
workspace/{product-slug}/
  [category-specific files — see per-category structures above]
  .meta.yaml        ← internal metadata, stripped during packaging
```

---

## Quality Gate

Generated scaffold must pass MCS-1 structural validation before being shown to the creator:
- All required files for the product type are present
- All required metadata fields are populated (even if with placeholders that need filling)
- README.md skeleton contains the four required sections: what it does, install, usage, requirements
- No syntax errors in any generated YAML or JSON files
- `.meta.yaml` is valid and contains all required fields

---

## Decision Notes

> **Note:** CE-D references are from Creator Engine v1.1.0. SE-D references are from Studio Engine v2.0 PRD.

**CE-D12:** WHY comments (format: `<!-- WHY: ... -->`) are included in every scaffold section to explain what the creator must fill in. They are stripped during `/package`. Creators should NOT remove them manually — they're harmless in the workspace.

**Why pre-validate at scaffold time:** Starting at MCS-1 means the creator never has to "fix the basics." They start publishable and build up. Failure to scaffold correctly is a bug in the Scaffolder, not the creator's responsibility.

**Category routing via sub-commands:** Direct sub-commands (`/create skill`) skip the menu for experienced creators. The menu exists for first-time users who don't know the vocabulary yet.
