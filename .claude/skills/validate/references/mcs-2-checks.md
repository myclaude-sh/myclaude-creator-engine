# MCS-2 Checks — Quality

> **v2.0 alignment:** These checks map to Stage 4 (DNA Tier 2) + Stage 7 (Anti-Commodity).
> DNA Tier 2 patterns: D5,D6,D7,D8,D15,D16,D17 — check `product-dna/{type}.yaml` for which are required per type.
> Scoring: OVERALL = (DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20). Threshold: >= 85%.

Products that demonstrate craft and thoroughness. Builds on all MCS-1 requirements.

**Prerequisite:** All MCS-1 checks must pass before MCS-2 checks are evaluated.

**Total additional checks in this tier:** 7 DNA Tier 2 patterns + Anti-Commodity gate

---

## Additional Requirements (beyond MCS-1)

| # | Check | Description | Automated |
|---|-------|-------------|-----------|
| Q1 | Exemplars count | At least 3 exemplars/examples covering different use cases | Yes (count files in `examples/`) |
| Q2 | Anti-patterns section | An explicit section or file documenting what NOT to do with this product | Yes (scan for section heading) |
| Q3 | Intent testing | Tested with at least 5 different user intents/scenarios (documented) | Semi (creator self-reports) |
| Q4 | Quality gate defined | The product itself defines how to validate its output quality | Yes (scan for quality gate section) |
| Q5 | Edge case handling | Error handling or fallback behavior for edge cases is documented | Yes (scan for section) |
| Q6 | No placeholder content | No `TODO`, `lorem ipsum`, `coming soon`, `PLACEHOLDER`, unfilled `{variable}` markers outside of intentional variable syntax | Yes (pattern scan) |
| Q7 | Consistent naming | Product name, slug, and terminology are consistent across all files | Yes (cross-file name comparison) |
| Q8 | Semver version | Version field follows MAJOR.MINOR.PATCH format | Yes (regex: `^\d+\.\d+\.\d+$`) |

---

## Semi-Automated Check Suite

```
/validate --level=2 → runs MCS-2 suite
  ├── All MCS-1 checks
  ├── exemplar-count      Q1: >= 3 exemplars?
  ├── anti-pattern-check  Q2: anti-patterns section exists?
  ├── placeholder-scan    Q6: no TODO/lorem/placeholder content?
  ├── consistency-check   Q7: naming consistent throughout?
  ├── semver-check        Q8: version follows MAJOR.MINOR.PATCH?
  ├── quality-gate-check  Q4: quality gate section present?
  ├── edge-case-check     Q5: edge case handling documented?
  └── [MANUAL] Q3: intent-test — tested with 5 intents? (creator self-reports)
```

---

## Anti-Commodity Gate (CE-D9)

MCS-2 products must also pass the differentiation check:

```
DIFFERENTIATION GATE:
1. "What domain expertise did the creator inject that AI alone couldn't generate?"
2. "If we removed all AI-generated content, what would remain?"
3. "Does this product solve a specific problem that fewer than 5 other products address?"
```

If all three answers are weak → GATE FAILS.

Feedback when gate fails:
```
This product lacks differentiation. Consider:
- Adding domain-specific knowledge from your expertise
- Targeting a more specific use case
- Including proprietary methodology or frameworks
```

---

## Check Details

### Q1 — Exemplars Count

Look for:
- Files in `examples/` directory
- Files matching `example-*.md`, `exemplar-*.md`, `use-case-*.md`
- Numbered example sections within the primary definition file (e.g., `### Example 1`, `### Exemplar 1`)

Count distinct examples. Minimum 3 required. Report count if below threshold.

### Q2 — Anti-Patterns Section

Look for any of:
- A file named `anti-patterns.md` in the product directory
- A section heading containing "Anti-Pattern", "What NOT to do", "Avoid", "Common Mistakes"
- An explicit anti-patterns block in the primary definition file

### Q3 — Intent Testing (Self-Reported)

The Validator presents this as a checklist item for the creator to confirm:
```
  [ ] Q3: Have you tested this product with at least 5 different user requests?
      (Mark as confirmed to pass this check)
```

The creator must explicitly confirm. If not confirmed, this check is recorded as MANUAL-PENDING.

### Q4 — Quality Gate Defined

Look for a section heading containing "Quality Gate", "Validation", "Success Criteria", or "Definition of Done" in the primary definition file.

### Q5 — Edge Case Handling

Look for:
- A section addressing error states, failure modes, or edge cases
- Documented fallback behavior
- "When NOT to use" section (counts as partial credit — still requires active handling)

### Q6 — Placeholder Scan

Scan all files for patterns:
- `TODO` (case-insensitive, not in code comments that are intentional)
- `lorem ipsum` (case-insensitive)
- `coming soon` (case-insensitive)
- `PLACEHOLDER`
- `{fill this in}`, `[add here]`, `[describe here]`
- `<!-- WHY:` — guidance comments should have been stripped before MCS-2 target is declared

Flag exact file and line number for each occurrence.

### Q7 — Consistent Naming

Extract product name/slug from:
1. Primary definition file title
2. `.meta.yaml` `product.slug`
3. `vault.yaml` `name` (if exists)
4. Directory name in `workspace/`

All four should be consistent (same slug, same display name). Flag mismatches with specific locations.

### Q8 — Semver Version

Extract version from primary definition file metadata or `vault.yaml`.
Validate against regex: `^\d+\.\d+\.\d+$`
Examples that pass: `1.0.0`, `2.3.1`, `0.1.0`
Examples that fail: `1.0`, `v1.0.0`, `1.0.0-beta`, `latest`
