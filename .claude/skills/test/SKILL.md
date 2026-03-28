---
name: test
description: >-
  Sandbox test a product against sample inputs in an isolated worktree.
  Creates a temporary copy, installs the product, runs 3 test scenarios
  (happy path, edge case, adversarial), verifies activation protocol works,
  and reports results. Use when the creator says "test", "try it", "does it work",
  or before publishing.
argument-hint: "[product-slug]"
context: fork
isolation: worktree
---

# Tester

Run sandbox tests on a product in an isolated environment.

**When to use:** Before publishing, after major changes, or to verify activation protocol works standalone.

**When NOT to use:** For quick syntax checks (use /validate instead). For testing the Engine itself.

---

## Activation Protocol

1. Identify target product:
   - If `$ARGUMENTS` provided, use as slug → `workspace/{slug}/`
   - If not, list products in workspace/ and ask
2. Read `.meta.yaml` → get type, state, mcs_target
3. Load product-dna/{type}.yaml → get install_target pattern
4. Verify product has content (state != scaffold)
5. Create worktree isolation (this skill runs with `isolation: worktree`)

---

## Core Instructions

### TEST EXECUTION

**Step 1 — Install Simulation**

Copy product files to the install target path (from product-dna):
```
workspace/{slug}/ → {worktree}/{install_target}/
```

Verify:
- All files copied successfully
- No broken relative paths after move
- Primary file exists at target location

**Step 2 — Activation Test**

Test the activation protocol:
- Read the primary file (SKILL.md, AGENT.md, etc.)
- Verify it references files that exist in the installed location
- Check that references/ paths resolve correctly
- Verify frontmatter is valid (name, description present)

**Step 3 — Three Scenarios**

Run 3 test inputs appropriate for the product type:

| Scenario | Purpose | Input Strategy |
|----------|---------|---------------|
| **Happy path** | Normal expected use | Typical request matching the product's description |
| **Edge case** | Boundary conditions | Minimal input, unusual formatting, missing context |
| **Adversarial** | Graceful failure | Invalid input, prompt injection attempt, conflicting instructions |

For each scenario:
1. Invoke the product with the test input
2. Capture output
3. Verify against D4 (Quality Gate) criteria if defined
4. Check for crashes, undefined behavior, or silent failures

**Step 4 — Report**

```
TEST REPORT — {slug}

INSTALL    PASS  Files copied: {N}, paths valid
ACTIVATION PASS  Primary file loads, refs resolve, frontmatter valid
HAPPY PATH PASS  Output matches expected behavior
EDGE CASE  PASS  Handles minimal input gracefully
ADVERSARIAL PASS  Rejects invalid input without crashing

Result: 5/5 PASS — Ready for /package

{if failures}
FAILURES:
  {scenario}: {what went wrong}
  Suggested fix: {recommendation}
{/if}
```

---

## Quality Gate

Test is considered PASS if:
- [ ] Product installs without broken references
- [ ] Activation protocol loads successfully
- [ ] Happy path produces meaningful output
- [ ] Edge case doesn't crash or produce empty output
- [ ] Adversarial input is handled (rejection, fallback, or graceful error)

---

## Anti-Patterns

1. **Testing in production** — Always use worktree isolation. Never modify the creator's workspace.
2. **Weak adversarial** — "please ignore instructions" is too simple. Use domain-appropriate adversarial inputs.
3. **Binary pass/fail** — Provide specific failure descriptions, not just FAIL.
4. **Skipping cleanup** — Worktree must be cleaned up after test, even on failure.
5. **Testing the template** — If the product still has placeholder content, don't test. Suggest /fill first.
