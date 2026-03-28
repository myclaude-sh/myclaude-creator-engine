# MCS v2.0 Specification — MyClaude Creator Spec

> The quality system for MyClaude marketplace. Three tiers of ascending quality
> mapped to DNA pattern compliance. Products must pass lower tiers to reach higher.

**SE-D4:** MCS v2 = DNA compliance. Not structural checklists.

---

## Scoring Formula

```
For each applicable DNA pattern (from product-dna/{type}.yaml):
  PASS    = 1.0  (pattern fully present and functional)
  PARTIAL = 0.5  (pattern present but incomplete)
  FAIL    = 0.0  (pattern absent or broken)

DNA_SCORE        = (sum of pattern_scores / applicable_patterns_count) x 100
STRUCTURAL_SCORE = (files_found / files_expected) x 100
INTEGRITY_SCORE  = (valid_refs / total_refs) x 100  [0 broken refs = 100]

OVERALL = (DNA_SCORE x 0.50) + (STRUCTURAL_SCORE x 0.30) + (INTEGRITY_SCORE x 0.20)
```

Weights are configured in `config.yaml` → `scoring.weights`.

---

## MCS Thresholds

| Level | DNA Requirement | Overall Score | What It Proves | Badge |
|-------|----------------|--------------|----------------|-------|
| **MCS-1** | Tier 1 ALL PASS (D1,D2,D3,D4,D13,D14) | >= 75% | Functional, documented, no broken refs | muted |
| **MCS-2** | Tier 1+2 ALL PASS (adds D5-D8,D15-D17) | >= 85% | Demonstrates craft and professionalism | cyan |
| **MCS-3** | Tier 1+2+3 ALL PASS (adds D9-D12,D18) | >= 92% | State-of-the-art structural DNA | gold |

Not all patterns apply to all types. See `product-dna/{type}.yaml` for type-specific applicability.

---

## 7-Stage Validation Pipeline

```
Stage 1: STRUCTURAL (automated — glob, stat)
  Check: all required files for product type exist
  Score: files_found / files_expected
  Blocking: YES

Stage 2: INTEGRITY (automated — grep, read)
  Check: file refs resolve, no placeholders, YAML/JSON valid
  Score: valid_refs / total_refs
  Blocking: YES

Stage 3: DNA TIER 1 (automated — grep, glob)
  D1:  Activation protocol section + references/ ref
  D2:  Anti-pattern section >= 5 items
  D3:  references/ dir exists + primary file < 500 lines
  D4:  Quality gate section >= 3 verifiable criteria
  D13: README.md with what/install/usage/requirements
  D14: "When not to use" or degradation section
  Blocking: YES (gates MCS-1)

Stage 4: DNA TIER 2 (automated + semi-automated — MCS-2)
  D5:  Question/input table or "if missing, ask" pattern
  D6:  Confidence levels or certainty markers
  D7:  Precondition checks
  D8:  State file or persistence section
  D15: Test scenarios or expected outputs
  D16: No hardcoded paths, no common command names
  D17: Hooks section in frontmatter or docs
  Blocking: NO (advisory for MCS-1, gates MCS-2)
  Editions: lite + pro

Stage 5: DNA TIER 3 (agent-assisted — MCS-3, PRO only)
  D9:  Routing table, no domain instructions in orchestrator
  D10: Handoff specs between agents
  D11: Self-challenge or falsification pattern
  D12: Memory configuration with project scope
  D18: context:fork or subagent isolation
  Blocking: NO (advisory for MCS-2, gates MCS-3)
  Editions: pro only

Stage 6: CLI PREFLIGHT (delegates to myclaude validate)
  Check: vault.yaml valid, no secrets, file sizes OK
  Blocking: YES

Stage 7: ANTI-COMMODITY (coaching, never blocking)
  Q1: "What domain expertise did the creator inject?"
  Q2: "If we removed all AI-generated content, what remains?"
  Q3: "Does this solve a specific problem < 5 products address?"
  Blocking: NEVER (feedback only, SE-D4)
  Editions: lite + pro (MCS-2+)
```

---

## DNA Applicability Matrix

Patterns marked **R** are required for MCS at that tier. `o` = optional bonus. `—` = not applicable.

| Pattern | skill | agent | squad | workflow | ds | prompt | claude-md | app | system |
|---------|-------|-------|-------|----------|-----|--------|-----------|-----|--------|
| D1  Activation Protocol      | **R** | **R** | **R** | **R** | — | **R** | **R** | o | **R** |
| D2  Anti-Pattern Guard       | **R** | **R** | **R** | **R** | **R** | o | **R** | **R** | **R** |
| D3  Progressive Disclosure   | **R** | **R** | **R** | o | — | — | **R** | o | **R** |
| D4  Quality Gate             | **R** | **R** | **R** | **R** | **R** | **R** | — | **R** | **R** |
| D5  Question System          | **R** | **R** | **R** | — | — | o | — | o | **R** |
| D6  Confidence Signaling     | o | **R** | **R** | o | — | o | — | o | **R** |
| D7  Pre-Execution Gate       | **R** | **R** | **R** | **R** | — | — | o | **R** | **R** |
| D8  State Persistence        | o | **R** | **R** | o | — | — | — | o | **R** |
| D9  Orchestrate Don't Execute| — | — | **R** | — | — | — | — | — | **R** |
| D10 Handoff Spec             | — | — | **R** | o | — | — | — | — | **R** |
| D11 Socratic Pressure        | o | **R** | **R** | — | — | — | — | — | **R** |
| D12 Compound Memory          | — | o | **R** | — | — | — | — | — | **R** |
| D13 Self-Documentation       | **R** | **R** | **R** | **R** | **R** | **R** | **R** | **R** | **R** |
| D14 Graceful Degradation     | **R** | **R** | **R** | **R** | o | o | o | **R** | **R** |
| D15 Testability              | o | **R** | **R** | o | — | o | — | o | **R** |
| D16 Composability            | **R** | **R** | **R** | **R** | **R** | **R** | **R** | **R** | **R** |
| D17 Hook Integration         | o | o | o | o | — | — | o | o | o |
| D18 Subagent Isolation       | — | — | **R** | — | — | — | — | — | **R** |

---

## Badge Display

| Level | Visual | Label |
|-------|--------|-------|
| MCS-1 | `muted` color | Publishable |
| MCS-2 | `cyan` color | Quality |
| MCS-3 | `gold` color | State-of-the-Art |

Badges render on marketplace product cards via the MCS Badge atom component.

---

## Score Report Format

```
MCS VALIDATION REPORT — {product_name}
Target: MCS-{level} | Type: {type}

STRUCTURAL  ████████░░  80%  (4/5 files found)
INTEGRITY   ██████████  100% (12/12 refs valid)
DNA TIER 1  ██████████  100% (6/6 pass)
DNA TIER 2  ████████░░  86%  (6/7 pass — D17 missing)
DNA TIER 3  ░░░░░░░░░░  N/A  (not targeted)
CLI         ██████████  PASS

OVERALL: 88% → MCS-2 ACHIEVED

Findings:
  D17 (Hook Integration): PARTIAL — hooks documented but not in frontmatter

Recommendation: Add hooks to SKILL.md frontmatter for D17 PASS
```

---

## Type-Specific Expectations

For detailed DNA requirements per type, see: `product-dna/{type}.yaml`

| Type | Max Practical MCS | Notes |
|------|------------------|-------|
| skill | MCS-2 | Few Tier 3 patterns apply |
| agent | MCS-3 | D11 required at Tier 3 |
| squad | MCS-3 | ALL 18 patterns required |
| workflow | MCS-2 | Limited Tier 2/3 applicability |
| design-system | MCS-2 | No Tier 3 patterns |
| prompt | MCS-2 | No Tier 3 patterns |
| claude-md | MCS-2 | No Tier 3 patterns |
| application | MCS-2 | Limited DNA applicability |
| system | MCS-3 | ALL 18 patterns required |
