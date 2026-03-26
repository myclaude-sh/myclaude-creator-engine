---
name: validate
description: >-
  Run MCS quality validation on products in workspace/. Three-tier system:
  MCS-1 checks structure and metadata, MCS-2 checks quality and anti-commodity,
  MCS-3 runs agent-assisted deep review with stress tests. Returns scored reports
  with specific fix instructions. Use after building or modifying a product,
  before publishing, when the creator asks to "check quality", "validate",
  "run checks", or "is this ready to publish".
argument-hint: "[--level=1|2|3] [--fix] [--batch]"
---

# Validator

Run MCS quality checks on any product in `workspace/` and return actionable, scored reports.

**When to use:** After building or modifying a product, before publishing, or anytime you want a quality snapshot.

**When NOT to use:** On products outside `workspace/` (use path argument in that case). Do not use to validate the Engine itself.

---

## Activation Protocol

1. Detect product type: read `.engine-meta.yaml` from the product directory for `category` and `scaffold_state`
   - If `.engine-meta.yaml` is missing, infer type from file structure (look for SKILL.md, AGENT.md, SQUAD.md, etc.)
   - If type cannot be determined, ask: "What product type is this? (skill/agent/squad/workflow/ds/prompt/claude-md/app/system)"
2. Load the product spec for the detected type from `references/product-specs/{type}-spec.md` (if it exists — project root)
3. Load the appropriate MCS check references based on requested level:
   - MCS-1: `${CLAUDE_SKILL_DIR}/references/mcs-1-checks.md`
   - MCS-2: `${CLAUDE_SKILL_DIR}/references/mcs-1-checks.md` + `${CLAUDE_SKILL_DIR}/references/mcs-2-checks.md`
   - MCS-3: all three check files from `${CLAUDE_SKILL_DIR}/references/`

---

## Commands

```
/validate                    → Auto-detect product type, run MCS-1 checks
/validate --level=2          → Run MCS-2 checks (includes all MCS-1)
/validate --level=3          → Run MCS-3 checks (includes MCS-1 + MCS-2, invokes quality-reviewer agent)
/validate --fix              → Run MCS-1, then auto-remediate fixable issues (CE-D13: non-destructive)
/validate --report           → Run MCS-1, then output detailed quality report as a file
/validate --batch              → Validate ALL products in workspace/ sequentially, produce summary
/test                        → Sandbox test: run the product against 3 sample inputs and report behavior (CE-D35)
```

---

## Core Instructions

### VALIDATION PIPELINE

Execute stages in order. If a stage fails, report failures and stop — do not proceed to the next stage unless `--level` flag requires it.

**Stage 1 — STRUCTURAL VALIDATION**

Check that the file structure matches the expected layout for the product type.
- Are the required files present? (per product type — see product-spec or MCS-1 checks)
- Are required metadata fields populated in the primary definition file?

**Stage 2 — CONTENT VALIDATION**

Check that content is filled in and valid:
- Are all required sections present and non-empty?
- Are there any unfilled placeholders? (scan for `{placeholder}`, `TODO`, `lorem ipsum`, `coming soon`, `GUIDANCE:` left in non-comment positions)
- Are all file references valid? (every file path mentioned actually exists)
- Are there syntax errors in any YAML or JSON files?

**Stage 3 — QUALITY VALIDATION** (MCS-2+)

Check that the product demonstrates craft:
- Does it have at least 3 exemplars/examples?
- Is there an anti-patterns section?
- Are there documented test scenarios covering 5+ user intents?
- Is there a quality gate defined?
- Is error handling for edge cases present?
- Is naming consistent throughout all files?
- Does the version follow semver (MAJOR.MINOR.PATCH)?

**Stage 4 — EXCELLENCE VALIDATION** (MCS-3 only)

Invoke quality-reviewer agent for:
- Depth review: does `references/` contain real domain expertise?
- Composability test: does the product work with standard MyClaude products?
- Stress test: can it handle ambiguous, adversarial, and edge-case inputs?
- Differentiation check: is it a commodity product?
- Architecture review: are design decisions justified?
- Token efficiency: is context usage reasonable?

**Stage 5 — ANTI-COMMODITY GATE** (MCS-2+ only, CE-D9)

Ask three questions:
1. "What domain expertise did the creator inject that AI alone couldn't generate?"
2. "If we removed all AI-generated content, what would remain?"
3. "Does this product solve a specific problem that fewer than 5 other products address?"

If all three answers are weak → GATE FAILS with feedback.

### SCORING

Calculate score as: `(passed_checks / total_checks) * 100`

Round to nearest integer. Report as `{score}/100`.

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

### SANDBOX TEST (--test, CE-D35)

Generate 3 sample inputs appropriate for the product type:
- A clear, well-formed request (happy path)
- An ambiguous or underspecified request (edge case)
- An adversarial or off-topic request (boundary case)

Run the product against each input. Report:
- Did the product handle it correctly?
- Did it fail gracefully?
- What was the output quality?

This does not modify any files.

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

For each failed content check, generate a **domain-aware remediation draft**:

| Failed Check | Guided Fix |
|---|---|
| Missing anti-patterns section | Draft 3 anti-patterns based on the product's domain (read from .engine-meta.yaml category + the product's content) |
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

1. Glob `workspace/*/.engine-meta.yaml` to find all products
2. For each product found:
   a. Read `.engine-meta.yaml` for category and mcs_target
   b. Run MCS-1 validation (or target level from meta)
   c. Record: product slug, category, score, pass/fail, critical issues count
3. Output summary table:

```
═══════════════════════════════════════════════
  BATCH VALIDATION REPORT — {date}
═══════════════════════════════════════════════

  Products scanned: {N}

  | Product | Category | MCS Target | Score | Status |
  |---------|----------|------------|-------|--------|
  | {slug}  | {type}   | MCS-{N}    | {N}/100 | PASS/FAIL |
  | ...     | ...      | ...        | ...   | ...    |

  Summary: {passed}/{total} products passing target MCS level

  Critical issues requiring attention:
  - {product}: {issue description}
  - ...
═══════════════════════════════════════════════
```

4. Update each product's `.engine-meta.yaml` with validation result
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

Update `.engine-meta.yaml` after validation:
```yaml
last_validated: "{YYYY-MM-DD}"
last_validation_result: "{passed|failed}"
scaffold_state: "validated"  # only if all checks passed
```

---

## Quality Gate

The Validator skill itself passes if:
- It correctly identifies product type from `.engine-meta.yaml` or file structure
- It runs all checks appropriate for the requested MCS level
- Every failed check includes a specific, actionable fix instruction (not generic advice)
- Score calculation is accurate: `passed / total * 100`
- `.engine-meta.yaml` is updated after every validation run
- `--fix` never modifies content that the creator wrote

---

## Decision Notes

**CE-D13:** Validation is non-destructive by default. `--fix` has a conservative scope: structural and formatting only. Protecting existing creator content is more important than perfect automation.

**Why stop at first failing stage:** A product with broken file structure cannot be meaningfully content-validated. Stopping early gives the creator the clearest, most actionable feedback instead of a flood of cascading errors.

**CE-D21:** Progressive validation — each level builds on the previous. This means a product that passes MCS-2 is guaranteed to have also passed MCS-1. Levels cannot be skipped.

**CE-D9 (Anti-Commodity Gate):** Runs only at MCS-2+, as MCS-1 is the minimum publishable bar without differentiation requirements. Commodity products at MCS-1 are acceptable; at MCS-2+ they are not.
