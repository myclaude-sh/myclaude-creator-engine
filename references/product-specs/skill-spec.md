# Product Spec: Skills

## Definition

Skills are callable prompt routines installed to `.claude/skills/`. They are invoked
via `/skill-name` and execute a defined cognitive task using context loaded at activation
time. Skills are the primary product type — the Engine optimizes for skill creation above
all other types (CE-D5).

A skill is NOT:
- A standalone agent with persistent state
- A general-purpose chat assistant
- A wrapper around a single prompt with no structure

A skill IS:
- A focused, reusable cognitive routine
- Triggered by a specific user intent
- Self-contained but composable with other products

---

## Canonical File Structure

```
skill-name/
├── SKILL.md              # Identity, triggers, instructions (REQUIRED)
├── README.md             # Marketplace documentation (REQUIRED)
├── references/           # Knowledge base files
│   ├── domain-knowledge.md
│   └── exemplars.md
├── agents/               # Sub-agents (for complex skills)
│   └── specialist.md
├── tasks/                # Pre-defined task protocols
│   └── task-name.md
├── config/               # Configuration tables
│   └── routing-table.md
└── workflows/            # Multi-step workflows
    └── workflow-name.md
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `SKILL.md` | Identity, activation protocol, instructions, quality gate | MCS-1 |
| `README.md` | Install instructions, usage, examples, requirements | MCS-1 |
| `references/` (1+ files) | Domain knowledge used at activation | MCS-1 |

---

## Required Sections in SKILL.md

### 1. Title and One-Line Description

```markdown
# Skill Name

> One sentence: what this skill does and who it's for.
```

### 2. When to Use / When NOT to Use

```markdown
## When to Use
- [Scenario where this skill is the right tool]
- [Trigger condition 1]
- [Trigger condition 2]

## When NOT to Use
- [Scenario where a different approach is better]
- [Common misuse to prevent]
```

### 3. Activation Protocol (CE-D34)

The activation protocol defines what context to load BEFORE generating any response.
This is mandatory — skills that don't load context before responding produce generic output.

```markdown
## Activation Protocol

Before responding to any invocation, load in this order:
1. Read `references/domain-knowledge.md` — [what it contains]
2. Read `references/exemplars.md` — [what exemplars teach]
3. Identify the user's intent from their input
4. Select the appropriate mode/variant
5. Apply the instructions below
```

### 4. Core Instructions

The actual skill logic. Should include:
- Decision tree or routing logic (if applicable)
- Question system that runs BEFORE output (CE-D36)
- Processing steps
- Handling for ambiguous input

### 5. Output Structure / Format

```markdown
## Output Format

[Describe the exact format the skill must produce]
[Include structural templates if applicable]
[Specify when to use different formats]
```

### 6. Quality Gate

```markdown
## Quality Gate

Before delivering output, verify:
- [ ] [Check 1: specific condition]
- [ ] [Check 2: specific condition]
- [ ] [Check 3: specific condition]

If any check fails: [what to do]
```

---

## MCS Requirements

### MCS-1: Publishable

**Universal:**
- [ ] Valid SKILL.md with all 6 required sections
- [ ] README.md with: what it does, how to install, how to use, requirements
- [ ] At least 1 file in `references/`
- [ ] Metadata: name, description, category (skills), version, license
- [ ] No broken file references
- [ ] No syntax errors in markdown
- [ ] File size under 50MB
- [ ] License from approved list
- [ ] No hardcoded secrets or API keys

**Skill-Specific:**
- [ ] Activation Protocol section present with at least 2 load steps
- [ ] At least 1 trigger condition documented
- [ ] Output format specified

### MCS-2: Quality

**Universal (beyond MCS-1):**
- [ ] At least 3 exemplars covering different use cases
- [ ] Anti-patterns section documenting what NOT to do
- [ ] Tested with at least 5 different user intents
- [ ] Quality gate defined with specific checks
- [ ] Error handling for edge cases
- [ ] No placeholder content (no TODO, lorem ipsum, coming soon)
- [ ] Consistent naming throughout
- [ ] Version follows semver (MAJOR.MINOR.PATCH)

**Skill-Specific:**
- [ ] `references/exemplars.md` with 3+ concrete examples
- [ ] At least 1 anti-pattern documented with explanation
- [ ] At least 1 optional file from structure (agents/, tasks/, config/, or workflows/)

### MCS-3: State-of-the-Art

**Universal (beyond MCS-2):**
- [ ] Deep knowledge base in `references/` with real domain expertise
- [ ] Adaptive modes (surface / dive / radical — CE-D36 progressive depth)
- [ ] Composable with other MyClaude products
- [ ] Stress-tested: ambiguity test, edge case test, adversarial test passed
- [ ] Cognitive architecture documented (WHY it's designed this way)
- [ ] Versioning strategy with CHANGELOG
- [ ] At least 5 exemplars including edge cases
- [ ] Performance-optimized (minimal token usage for maximum value)
- [ ] Differentiation statement (what makes this product unique)

**Skill-Specific:**
- [ ] Progressive depth modes implemented: surface / dive / radical
- [ ] Question system designed (forces structured inquiry before output)
- [ ] Full `references/` knowledge base with domain expertise
- [ ] Skill is independently useful AND composable as a component

---

## Anti-Patterns for Skills

### Structural
- **Missing Activation Protocol:** Skill.md has no protocol for loading context before responding. All context sits unused in `references/`.
- **References without routing:** Files exist in `references/` but SKILL.md never tells the skill to read them.
- **Monolithic SKILL.md:** Putting everything in one file instead of breaking domain knowledge into `references/`.

### Content
- **Generic trigger conditions:** "Use when you want to do X" — too vague. Triggers should be specific enough to distinguish this skill from a general assistant.
- **Output format not specified:** Skill produces different formats depending on the prompt, making output unreliable.
- **No question system:** Skill immediately generates output without clarifying ambiguous inputs first (violates H11 / CE-D36).

### Quality
- **Exemplars that are too simple:** 3 trivial examples don't demonstrate real-world utility. Exemplars should cover the interesting, non-obvious cases.
- **Quality gate without teeth:** Checklist items that are impossible to fail ("verify output is related to input") don't improve quality.
- **No anti-patterns documented:** Creators who don't document anti-patterns generate 10x the support questions (H6).

---

## Discovery Questions (from §7)

When creating a skill, answer these before scaffolding:

1. What specific problem does this skill solve? (One sentence, not "helps with X")
2. Who is the target user? (developer, marketer, analyst, security professional, etc.)
3. What triggers should activate this skill? (specific patterns or keywords)
4. What output format should the skill produce? (markdown, JSON, structured text, etc.)
5. What domain knowledge must the skill have access to? (what goes in `references/`)
6. What tools or integrations does it need? (file access, web search, code execution, etc.)
7. What are the 3 most common ways users will misuse this skill? (future anti-patterns)
8. Can this skill be part of a larger workflow? If so, what are its inputs/outputs as a component?

---

## DNA Requirements

For the complete DNA pattern applicability matrix for this product type,
see `product-dna/skill.yaml`. That file defines:
- Which of the 18 DNA patterns (D-01 to D-18) are required vs optional
- Validation checks per pattern (grep/glob commands)
- Template file mapping with DNA injection points
- Frontmatter fields (Anthropic Agent Skills spec)
- Discovery questions for /create

**MCS scoring:** `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
See `references/quality/mcs-spec.md` for full scoring formula.
