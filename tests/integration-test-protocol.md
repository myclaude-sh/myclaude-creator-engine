# S5 Integration Test Protocol — Studio Engine v2.0

> Execute this protocol to verify the complete creator pipeline works end-to-end.
> All tests must PASS for LITE v2.0 to be shippable.
> Run in a FRESH Claude Code session with the Engine repo open.

---

## Pre-requisites

- [ ] MyClaude CLI installed (`myclaude --version` returns >= 0.3.0)
- [ ] No creator.yaml exists (delete if present: `rm creator.yaml`)
- [ ] workspace/ is empty (only .gitkeep)
- [ ] STATE.yaml is clean (sessions_total: 0)

---

## TEST 1: /onboard → creator.yaml

**Run:** `/onboard`

**Verify:**
- [ ] Asks language preference
- [ ] Asks name + username
- [ ] Asks expertise domains (accepts 1-5)
- [ ] Asks goals (multi-select)
- [ ] Asks technical level
- [ ] Infers creator type without asking directly
- [ ] Scans environment (reports 10 skills, 0 products)
- [ ] Asks preferences (license, category, pricing, quality target)
- [ ] Generates `creator.yaml` in project root
- [ ] Shows persona-adaptive next action recommendation
- [ ] Suggests /map or /create as next step

**Validate creator.yaml:**
- [ ] Has `creator.name`, `creator.myclaude_username`
- [ ] Has `creator.profile.type` (one of: developer, prompt-engineer, domain-expert, marketer, hybrid)
- [ ] Has `creator.preferences.default_license`
- [ ] Has `creator.preferences.quality_target`
- [ ] YAML parses without errors

---

## TEST 2: /map → domain-map.md

**Run:** `/map "code review automation"`

**Verify:**
- [ ] Loads creator.yaml (uses expertise + technical level)
- [ ] Asks Phase 1 questions (domain boundaries, target user, existing approaches)
- [ ] Asks Phase 2 questions (core knowledge, anti-patterns, decision framework, terminology)
- [ ] Asks Phase 3 questions (ideal output, edge cases)
- [ ] Generates `workspace/domain-map.md`
- [ ] domain-map.md has: Domain Boundaries, Core Knowledge, Anti-Patterns, Decision Framework, Vocabulary, Ideal Output, Edge Cases, Recommended Product Type
- [ ] At least 3 knowledge pillars substantive
- [ ] At least 3 anti-patterns documented
- [ ] Recommends a product type with reasoning

---

## TEST 3: /create skill → scaffold

**Run:** `/create skill`

**Verify:**
- [ ] Reads creator.yaml defaults
- [ ] Shows exemplar preview (from references/exemplars/skill-exemplar.md)
- [ ] Asks name + description
- [ ] Asks discovery questions (from discovery-questions.md)
- [ ] Loads domain-map.md (from workspace/) and prefills sections
- [ ] Generates scaffold in workspace/{slug}/
- [ ] Creates .meta.yaml with v2.0 schema:
  - [ ] `product.slug` present
  - [ ] `product.type: "skill"` present
  - [ ] `state.phase: "scaffold"` present
  - [ ] `product.mcs_target` present
- [ ] Creates SKILL.md with WHY comments
- [ ] Creates README.md with 4 sections (what, install, usage, requirements)
- [ ] Creates references/ directory
- [ ] Moves domain-map.md into product directory
- [ ] Runs MCS-1 structural pre-check
- [ ] Suggests /fill as next step

---

## TEST 4: /fill → content

**Run:** `/fill {slug}`

**Verify:**
- [ ] Reads .meta.yaml → gets type=skill, state=scaffold
- [ ] Loads product-dna/skill.yaml → gets DNA requirements
- [ ] Loads references/product-specs/skill-spec.md
- [ ] Loads domain-map.md if present
- [ ] Walks sections in priority order (Identity → Activation → Core → Quality Gate → Anti-Patterns → References → Examples → Edge cases)
- [ ] Asks domain-specific questions (adapts to technical level)
- [ ] Writes answers into SKILL.md sections
- [ ] Shows what was written before proceeding
- [ ] Updates .meta.yaml: `state.phase: "content"`
- [ ] Reports sections filled count
- [ ] Suggests /validate as next step

---

## TEST 5: /validate → validated

**Run:** `/validate`

**Verify:**
- [ ] Reads .meta.yaml → product.type and state.phase
- [ ] Loads product-dna/skill.yaml
- [ ] Loads config.yaml → scoring weights and thresholds
- [ ] **Stage 1 (Structural):** Checks required files exist → reports score
- [ ] **Stage 2 (Integrity):** Checks no placeholders, refs resolve, YAML valid → reports score
- [ ] **Stage 3 (DNA Tier 1):** Checks D1, D2, D3, D4, D13, D14 → reports per-pattern pass/fail
- [ ] **Stage 4 (DNA Tier 2):** Checks D5, D7, D16 (required for skills) → reports
- [ ] **Stage 6 (CLI Preflight):** Runs `myclaude validate` if CLI available
- [ ] **Stage 7 (Anti-Commodity):** Asks 3 coaching questions (advisory only)
- [ ] Calculates OVERALL score: (DNA×0.50) + (Structural×0.30) + (Integrity×0.20)
- [ ] Reports score with breakdown
- [ ] Updates .meta.yaml: `state.phase: "validated"`, scores populated
- [ ] If score >= 75%: "MCS-1 achieved"

**Scoring Verification:**
- [ ] DNA_SCORE = passed_patterns / applicable_patterns × 100
- [ ] STRUCTURAL_SCORE = files_found / files_expected × 100
- [ ] INTEGRITY_SCORE = valid_refs / total_refs × 100
- [ ] OVERALL = (DNA × 0.50) + (STRUCTURAL × 0.30) + (INTEGRITY × 0.20)
- [ ] Score is >= 75% (MCS-1 threshold)

---

## TEST 6: /package → packaged

**Run:** `/package {slug}`

**Verify:**
- [ ] Reads .meta.yaml → state is "validated"
- [ ] Creates workspace/{slug}/.publish/ directory
- [ ] Copies product files with WHY comments stripped
- [ ] Generates vault.yaml with ALL required fields:
  - [ ] name, version, type, description, entry, license, price, tags
  - [ ] displayName, mcsLevel, language, installTarget, compatibility
- [ ] Generates plugin.json with correct structure
- [ ] Calculates SHA-256 checksum
- [ ] EXCLUDES .meta.yaml from .publish/
- [ ] EXCLUDES domain-map.md from .publish/
- [ ] EXCLUDES hidden files from .publish/
- [ ] Re-validates .publish/ contents (structural + CLI preflight)
- [ ] Updates .meta.yaml: `state.phase: "packaged"`
- [ ] Reports file count, size, license, MCS level

**vault.yaml Verification:**
- [ ] `myclaude validate` accepts it (if CLI available)
- [ ] All required fields present
- [ ] installTarget matches product-dna/{type}.yaml

**plugin.json Verification:**
- [ ] Valid JSON
- [ ] Has name, description, version, author.name, license, homepage

---

## TEST 7: /publish (dry run)

**Run:** `/publish {slug}`

**Note:** This test verifies the publish FLOW, not actual marketplace upload.
If CLI is not authenticated or Stripe is inactive, the test passes if /publish
correctly shows the summary, asks for confirmation, and attempts CLI invocation.

**Verify:**
- [ ] Reads .meta.yaml → state is "packaged"
- [ ] Shows summary (name, type, version, price, license, MCS, file count)
- [ ] Requires explicit confirmation before proceeding
- [ ] Attempts `myclaude validate` on .publish/
- [ ] Attempts `myclaude publish` (expected: may fail if not authenticated)
- [ ] If CLI not found: shows install instructions
- [ ] If publish succeeds: updates .meta.yaml with published_at + version

---

## TEST 8: State Machine Integrity

After running tests 1-7 in sequence, verify:

- [ ] .meta.yaml shows `state.phase: "packaged"` (or "published" if T7 succeeded)
- [ ] .meta.yaml has `history.created_at` set
- [ ] .meta.yaml has validation scores populated
- [ ] STATE.yaml has workspace.active_products >= 1
- [ ] STATE.yaml has workspace.products[0].slug matching the created product

**Regression test:**
- [ ] Edit any file in workspace/{slug}/ (add a comment)
- [ ] Run `/validate` again
- [ ] Verify .meta.yaml state REGRESSED (should prompt re-validation, not show old scores)

---

## TEST 9: /status Dashboard

**Run:** `/status`

**Verify:**
- [ ] Shows engine version (2.0.0)
- [ ] Shows edition (LITE)
- [ ] Shows creator profile (from creator.yaml)
- [ ] Lists product with correct state
- [ ] Shows MCS target and score
- [ ] Shows last validated date

---

## TEST 10: /test Sandbox

**Run:** `/test {slug}`

**Verify:**
- [ ] Creates worktree isolation
- [ ] Copies product to install target path
- [ ] Verifies activation protocol loads
- [ ] Runs 3 test scenarios (happy, edge, adversarial)
- [ ] Reports pass/fail per scenario
- [ ] Cleans up worktree after test

---

## PASS CRITERIA

- **LITE v2.0 SHIPPABLE** when all 10 tests pass
- Tests 1-6 are BLOCKING (must pass)
- Test 7 is CONDITIONAL (passes if flow is correct, even if CLI auth fails)
- Tests 8-10 are VALIDATION (confirm system coherence)
- Minimum: Tests 1-6 all pass + Test 8 state machine is coherent

---

## EXECUTION LOG

| Test | Status | Notes | Date |
|------|--------|-------|------|
| T1: /onboard | | | |
| T2: /map | | | |
| T3: /create | | | |
| T4: /fill | | | |
| T5: /validate | | | |
| T6: /package | | | |
| T7: /publish | | | |
| T8: State Machine | | | |
| T9: /status | | | |
| T10: /test | | | |
