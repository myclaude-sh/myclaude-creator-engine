---
name: create
description: >-
  Scaffold a new product for the myClaude marketplace with MCS-1 valid structure
  and guidance comments. Supports all 9 product categories: skills, agents, squads,
  workflows, design systems, prompts, CLAUDE.md configs, applications, and systems.
  Use when the creator wants to start a new product, build something, or says
  "new skill", "new agent", "create", "scaffold", or "start building".
argument-hint: "[product-type]"
---

# Scaffolder

Generate complete, MCS-1-valid project structure for any product type with guidance comments baked in.

**When to use:** Starting a new product — any of the 9 categories.

**When NOT to use:** When the product already exists in `workspace/` and you want to add content (use `/create-content`). Do not use to overwrite an existing scaffold.

---

## Activation Protocol

1. Read `creator.yaml` from project root — load defaults (`default_category`, `default_license`, `quality_target`)
2. Identify which category was requested (from sub-command or by asking)
3. **Show the destination first** — Load the exemplar for this category from `references/exemplars/{category}-exemplar.md`. Show a condensed preview (title, structure, key sections) so the creator understands what "great" looks like before building. "Here's what an MCS-3 {category} looks like. Yours will follow this structure."
4. Load discovery questions from `${CLAUDE_SKILL_DIR}/references/discovery-questions.md` for that category
5. Load the product spec for that category from `references/product-specs/{category}-spec.md` (if it exists — project root)
6. Load the scaffold template from `templates/{category}/` (project root) — this is the structural source of truth for the generated files
7. Generate scaffold in `workspace/{product-slug}/` using the loaded template as base structure
8. After scaffold is generated, suggest: "Run `/create-content` to fill in the sections with your expertise, or start editing directly."

---

## Core Instructions

### ROUTER LOGIC

When invoked as `/create` with no argument, ask:

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

Enter number or name:
```

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

### UNIVERSAL CREATION FLOW

After category is identified:

**Step 1 — Name + Description**

```
Product name: (e.g., "security-audit-skill", "sales-email-prompt")
One-line description: (what does it do?)
```

Derive `{product-slug}` from name: lowercase, hyphens, no spaces.

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
<!-- GUIDANCE: Describe what the skill does in 1-2 sentences. Be specific about the problem it solves. -->
```

These are stripped during `/package`. (CE-D12)

Create `.engine-meta.yaml` in the workspace root for the product: (CE-D41)

```yaml
# Engine metadata — do not distribute, stripped during packaging
engine_meta:
  product_slug: "{product-slug}"
  category: "{category}"
  created_at: "{YYYY-MM-DD}"
  creator_engine_version: "1.0.0"
  scaffold_state: "generated"  # generated | in-progress | validated | packaged | published
  mcs_target: "{MCS-1|MCS-2|MCS-3}"
  last_validated: null
  last_validation_result: null
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
  [ ] Fill in the sections marked with GUIDANCE comments
  [ ] Add your domain-specific content and examples
  [ ] Run /validate to check MCS-1 compliance
  [ ] Run /validate --level=2 when targeting MCS-2
  [ ] Run /publish when ready

Tip: The GUIDANCE comments explain what each section needs.
     They are stripped automatically during packaging.
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
  .engine-meta.yaml        ← internal metadata, stripped during packaging
```

---

## Quality Gate

Generated scaffold must pass MCS-1 structural validation before being shown to the creator:
- All required files for the product type are present
- All required metadata fields are populated (even if with placeholders that need filling)
- README.md skeleton contains the four required sections: what it does, install, usage, requirements
- No syntax errors in any generated YAML or JSON files
- `.engine-meta.yaml` is valid and contains all required fields

---

## Decision Notes

**CE-D12:** Guidance comments (format: `<!-- GUIDANCE: ... -->`) are included in every scaffold section to explain what the creator must fill in. They are stripped during `/package`. Creators should NOT remove them manually — they're harmless in the workspace.

**Why pre-validate at scaffold time:** Starting at MCS-1 means the creator never has to "fix the basics." They start publishable and build up. Failure to scaffold correctly is a bug in the Scaffolder, not the creator's responsibility.

**Category routing via sub-commands:** Direct sub-commands (`/create skill`) skip the menu for experienced creators. The menu exists for first-time users who don't know the vocabulary yet.
