---
name: validate
description: >-
  Run MCS quality validation on products in workspace/. Three-tier system: MCS-1
  structure, MCS-2 quality + anti-commodity, MCS-3 deep review. Returns scored reports
  with fix instructions. Use when: 'validate', 'check quality', or before publishing.
argument-hint: "[--level=1|2|3] [--fix] [--batch]"
---

# Validator

Run MCS quality checks on any product in `workspace/` and return actionable, scored reports.

**When to use:** After building or modifying a product, before publishing, or anytime you want a quality snapshot.

**When NOT to use:** On products outside `workspace/` (use path argument in that case). Do not use to validate the Engine itself.

---

## Activation Protocol

1. Detect product type: read `.meta.yaml` from the product directory for `product.type` and `state.phase`
   - If `.meta.yaml` is missing, infer type from file structure (look for SKILL.md, AGENT.md, SQUAD.md, etc.)
   - If type cannot be determined, ask: "What product type is this? (skill/agent/squad/workflow/ds/prompt/claude-md/app/system)"
2. Load DNA requirements: read `product-dna/{type}.yaml` (project root) — get required patterns per tier
3. Load the product spec from `references/product-specs/{type}-spec.md`
4. Load config.yaml → scoring weights, thresholds, placeholder patterns
5. Load quality-gates.yaml → state transition rules

---

## Commands

```
/validate                    → Auto-detect product type, run MCS-1 checks
/validate --level=2          → Run MCS-2 checks (includes all MCS-1)
/validate --level=3          → Run MCS-3 checks (includes MCS-1 + MCS-2, invokes Quality Sentinel — PRO only)
/validate --fix              → Run MCS-1, then auto-remediate fixable issues (non-destructive)
/validate --report           → Run MCS-1, then output detailed quality report as a file
/validate --batch            → Validate ALL products in workspace/ sequentially, produce summary
```

---

## Core Instructions

### VALIDATION PIPELINE (7 Stages — aligned with config.yaml)

Execute stages in order. Blocking stages stop on failure. Non-blocking stages report but continue.

**Stage 1 — STRUCTURAL** (blocking)

Glob: do all required files for the product type exist?
Load `product-dna/{type}.yaml` → `required_files` and `config.yaml` → `routing.{type}.required_files`.
Score: `files_found / files_expected`

Frontmatter check: read the primary file's YAML frontmatter. Verify `description` field is <= 250 characters. If over, report as warning with character count: "Frontmatter description is {N} chars (recommended: <= 250). Trim for marketplace compatibility."

**Stage 2 — INTEGRITY** (blocking)

Grep: no placeholder content (`config.yaml` → `placeholder_patterns`: TODO, PLACEHOLDER, lorem ipsum, etc.)
Ref check: every file path referenced in .md files actually exists on disk.
Circular reference check: build a directed graph of file references (file A references file B). If any cycle is detected (e.g., A→B→A), report as integrity failure: "Circular reference detected: {cycle path}. Break the cycle by removing one reference."
YAML/JSON parse: no syntax errors in metadata files.
Score: `valid_refs / total_refs`

**Stage 3 — DNA TIER 1** (blocking, gates MCS-1)

Load `product-dna/{type}.yaml` → `tier1` patterns where `required: true`.
For each applicable pattern, run the validation check:
- D1 Activation Protocol: grep activation section + references/ ref
- D2 Anti-Pattern Guard: grep anti-pattern section, count >= 5 items
- D3 Progressive Disclosure: primary file < 500 lines + references/ exists
- D4 Quality Gate: grep quality gate section, >= 3 verifiable criteria
- D13 Self-Documentation: README.md with what/install/usage/requirements sections
- D14 Graceful Degradation: grep "when not to use" or degradation section
Score: `passed / applicable_count`

**Stage 4 — DNA TIER 2** (non-blocking, gates MCS-2, LITE+PRO)

Load `product-dna/{type}.yaml` → `tier2` patterns where `required: true`.
- D5 Question System: grep question/input table or "if missing, ask"
- D6 Confidence Signaling: grep confidence levels or certainty markers
- D7 Pre-Execution Gate: grep precondition checks
- D8 State Persistence: state file or persistence section
- D15 Testability: test scenarios or expected outputs
- D16 Composability: no hardcoded paths, no common command names
- D17 Hook Integration: hooks section in frontmatter or docs
Score: `passed / applicable_count`

**Stage 5 — DNA TIER 3** (non-blocking, gates MCS-3, PRO only)

Invoke Quality Sentinel agent for deep review:
- D9 Orchestrate Don't Execute: routing table, no domain instructions
- D10 Handoff Spec: handoff template between agents
- D11 Socratic Pressure: self-challenge pattern
- D12 Compound Memory: memory config with project scope
- D18 Subagent Isolation: context:fork or isolation
Score: `passed / applicable_count`

**Stage 6 — CLI PREFLIGHT** (blocking)

Run `myclaude validate` on the product directory.
If CLI not available, skip with warning.

**Stage 7 — ANTI-COMMODITY** (advisory, NEVER blocking, MCS-2+)

Three coaching questions:
1. "What domain expertise did the creator inject that AI alone couldn't generate?"
2. "If we removed all AI-generated content, what would remain?"
3. "Does this product solve a specific problem that fewer than 5 other products address?"

Result: coaching feedback only. Creator can override and proceed.

### SCORING (DNA-based, per PRD §4)

```
For each applicable DNA pattern (from product-dna/{type}.yaml):
  PASS    = 1.0   PARTIAL = 0.5   FAIL = 0.0

DNA_SCORE        = (sum pattern_scores / applicable_count) x 100
STRUCTURAL_SCORE = (files_found / files_expected) x 100
INTEGRITY_SCORE  = (valid_refs / total_refs) x 100

OVERALL = (DNA_SCORE x 0.50) + (STRUCTURAL_SCORE x 0.30) + (INTEGRITY_SCORE x 0.20)
```

Thresholds: MCS-1 >= 75%, MCS-2 >= 85%, MCS-3 >= 92%.
Report as `{score}%` with breakdown per component.

### AUTO-FIX RULES (--fix flag, CE-D13)

Auto-fix ONLY applies to issues that are:
1. Purely structural (missing required sections that can be scaffolded)
2. Formatting (YAML indentation, missing newlines)
3. Metadata completeness (missing fields that have safe defaults: `version: "1.0.0"`, `language: "en"`)

Auto-fix NEVER:
- Modifies or deletes existing content
- Fills in domain-specific sections with AI-generated content
- Changes product logic or architecture
- Removes examples or exemplars

After auto-fix, re-run the same validation level and report the new score.

### SANDBOX TEST

Sandbox testing is handled by the `/test` skill (separate worktree-isolated skill).
When the creator runs `/test`, it creates a worktree copy, installs the product,
runs 3 test scenarios (happy path, edge case, adversarial), and reports results.
The `/validate` skill focuses on structural + DNA checks; `/test` focuses on runtime behavior.

---

## Output Format

```
═══════════════════════════════════════════════
  MCS VALIDATION REPORT — {product-name} v{version}
═══════════════════════════════════════════════

  Level: MCS-{1|2|3} ({Publishable|Quality|State-of-the-Art})
  Score: {score}/100

  PASSED ({passed}/{total}):
  ✓ {check description}
  ✓ {check description}
  ...

  FAILED ({failed}/{total}):
  ✗ {check description} → {what was found}
    Fix: {specific, actionable instruction}
  ...

  RECOMMENDATION: {one of the following}
    - "All checks passed. Ready for /publish." (score = 100)
    - "Fix {n} items to achieve MCS-{level}." (score < 100)
    - "Run /validate --fix for auto-remediation." (if fixable issues exist)
═══════════════════════════════════════════════
```

### GUIDED ITERATION (when failures exist)

After reporting failures, don't just list them — offer to help fix content issues.
This turns the validator from a reporter into a coach.

For each failed content check, generate a **domain-aware remediation draft** (presented as suggestion only — never auto-fill without explicit creator confirmation):

| Failed Check | Guided Fix |
|---|---|
| Missing anti-patterns section | Draft 3 anti-patterns based on the product's domain (read from .meta.yaml product.type + the product's content) |
| Fewer than 3 exemplars | Draft example scenarios based on the skill's "When to Use" section |
| No quality gate | Draft a quality gate based on the product's Core Instructions (what output should look like) |
| No edge case handling | Suggest 2 edge cases based on the product's scope boundaries |
| Placeholder content found | Show the specific placeholder and suggest domain-specific replacement |

Present as: "I found {N} content issues I can help draft fixes for. Want me to proceed?"

Rules:
- Only write to files if creator explicitly approves
- Show the draft before writing (creator can edit)
- This extends --fix behavior to content, not just structure
- Preserves CE-D13: non-destructive by default, creator controls what gets written

### BATCH VALIDATION (/validate --batch)

When `--batch` is invoked:

1. Glob `workspace/*/.meta.yaml` to find all products
2. For each product found:
   a. Read `.meta.yaml` for product.type and product.mcs_target
   b. Run MCS-1 validation (or target level from meta)
   c. Record: product slug, type, score, pass/fail, critical issues count
3. Output summary table:

```
═══════════════════════════════════════════════
  BATCH VALIDATION REPORT — {date}
═══════════════════════════════════════════════

  Products scanned: {N}

  | Product | Type     | MCS Target | Score | Status |
  |---------|----------|------------|-------|--------|
  | {slug}  | {type}   | MCS-{N}    | {N}/100 | PASS/FAIL |
  | ...     | ...      | ...        | ...   | ...    |

  Summary: {passed}/{total} products passing target MCS level

  Critical issues requiring attention:
  - {product}: {issue description}
  - ...
═══════════════════════════════════════════════
```

4. Update each product's `.meta.yaml` with validation result
5. Flag stale products (>30 days since last validation)

Batch mode runs MCS-1 by default. Use `--batch --level=2` for MCS-2 batch validation.

### PUBLISH PRE-FLIGHT (WP-12, WP-13)

Run automatically when `.publish/` directory exists (i.e., after `/package`). This is the final safety net before the CLI takes over.

**Check:** Does `vault.yaml` in `.publish/` contain all REQUIRED fields?

Required fields per WP-3:
- `name` — slug format, non-empty
- `version` — valid semver
- `type` — one of: skill, agent, squad, workflow, design-system, claude-md, prompt, application, system
- `description` — non-empty, 10-500 chars
- `entry` — file path that exists in `.publish/`
- `license` — valid license identifier

If any required field is missing or invalid:
```
Pre-flight FAILED: vault.yaml is incomplete.
  Missing: {field1}, {field2}
  Fix vault.yaml in .publish/ before running myclaude publish.
```

If all required fields are present:
```
Pre-flight PASSED: vault.yaml has all required fields.
```

This check does NOT validate enrichment fields (display_name, mcs_level, tags, etc.) — those are optional and the CLI applies defaults for them.

---

Update `.meta.yaml` after validation:
```yaml
state:
  phase: "validated"                # only if all checks passed
  last_validated: "{YYYY-MM-DD}"
  last_validation_score: {overall_score}
  dna_compliance:
    tier1: {score}
    tier2: {score}
    tier3: {score or null}
  overall_score: {score}
```

---

## Quality Gate

The Validator skill itself passes if:
- It correctly identifies product type from `.meta.yaml` or file structure
- It runs all checks appropriate for the requested MCS level
- Every failed check includes a specific, actionable fix instruction (not generic advice)
- Score calculation is accurate: `passed / total * 100`
- `.meta.yaml` is updated after every validation run
- `--fix` never modifies content that the creator wrote

---

## Decision Notes

> **Note:** CE-D references are from Creator Engine v1.1.0. SE-D references are from Studio Engine v2.0 PRD.

**CE-D13:** Validation is non-destructive by default. `--fix` has a conservative scope: structural and formatting only. Protecting existing creator content is more important than perfect automation.

**Why stop at first failing stage:** A product with broken file structure cannot be meaningfully content-validated. Stopping early gives the creator the clearest, most actionable feedback instead of a flood of cascading errors.

**CE-D21:** Progressive validation — each level builds on the previous. This means a product that passes MCS-2 is guaranteed to have also passed MCS-1. Levels cannot be skipped.

**CE-D9 (Anti-Commodity Gate):** Runs only at MCS-2+, as MCS-1 is the minimum publishable bar without differentiation requirements. Commodity products at MCS-1 are acceptable; at MCS-2+ they are not.
