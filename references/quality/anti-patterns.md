# Anti-Patterns Reference

Documented anti-patterns across all product types. Each pattern includes the problem,
why it fails, and the correct approach.

---

## Structural Anti-Patterns

### AP-S01: Primary file in wrong location

**Problem:** `SKILL.md` placed in a subdirectory instead of the product root.
**Why it fails:** MCS-1 structure check looks for the primary file at the root.
Automated validation fails immediately.
**Fix:** Always place the primary file (SKILL.md, AGENT.md, etc.) at the product root,
not in a subdirectory.

---

### AP-S02: Required directory missing but referenced

**Problem:** SKILL.md references `references/domain-knowledge.md` but the `references/`
directory doesn't exist.
**Why it fails:** Broken file reference — MCS-1 `reference-check` fails. Product installs
but Activation Protocol reads nothing.
**Fix:** Create all directories and files that are referenced before publishing.
Run `/validate` and fix all broken references.

---

### AP-S03: Capability index inconsistent with agents

**Problem:** Squad's `config/capability-index.yaml` lists 4 capabilities but the squad
only has 2 agents. Two capabilities reference `agent-3` which doesn't exist.
**Why it fails:** Broken references in config. Users try to invoke capabilities that
route to non-existent agents.
**Fix:** Regenerate capability index after finalizing agent roster. Every capability must
map to an agent that exists.

---

### AP-S04: Manifest.yaml out of sync with actual files

**Problem:** `config/manifest.yaml` lists a component at `skills/analysis-skill/` but
that directory was renamed to `skills/analysis/`.
**Why it fails:** System routing reads the manifest. Stale paths cause routing failures.
**Fix:** Update `manifest.yaml` every time a component is renamed or moved. Run
`/validate` to catch any stale references.

---

### AP-S05: Steps directory missing for Workflow product

**Problem:** `WORKFLOW.md` describes 5 steps but all step definitions are inline in
WORKFLOW.md. No `steps/` directory.
**Why it fails:** MCS-1 requires 3+ step files in `steps/`. Inline steps are not
addressable or composable.
**Fix:** Create `steps/01-*.md` through `steps/0N-*.md`. WORKFLOW.md should reference
these files, not duplicate their content.

---

## Content Anti-Patterns

### AP-C01: Placeholder content published

**Problem:** README contains `[TODO: add usage examples]` or `lorem ipsum...`.
**Why it fails:** MCS-2 `placeholder-scan` explicitly checks for TODO, lorem, and
placeholder markers. A product with visible TODOs signals the creator didn't finish.
**Fix:** Complete all content before running `/validate --level=2`. If a section is
genuinely not needed, remove the heading, not replace it with a placeholder.

---

### AP-C02: Variables not substituted in prompt

**Problem:** Published PROMPT.md contains `{{AUDIENCE}}` as a literal — the variable
was never substituted or documented.
**Why it fails:** Buyers who use the prompt get `{{AUDIENCE}}` in their AI's context.
The product is broken by default.
**Fix:** Either (a) substitute all variables before publishing, or (b) document the
variables explicitly and make substitution a clear step in the README.

---

### AP-C03: Inconsistent naming within a product

**Problem:** The agent is called "Security Analyst" in AGENT.md, "security-auditor"
in the squad's routing table, and "audit-agent" in the capability index.
**Why it fails:** MCS-2 `consistency-check` flags naming inconsistencies. More
practically, routing breaks when names don't match.
**Fix:** Pick one name per component and use it everywhere. Search for all occurrences
before publishing.

---

### AP-C04: Generic identity for an agent

**Problem:** AGENT.md Identity section reads: "I am a helpful, knowledgeable, and
friendly AI assistant who excels at analysis."
**Why it fails:** This describes no agent specifically. It predicts nothing about how
the agent will behave in edge cases. MCS-3 agent review will flag this.
**Fix:** Identity should describe cognitive style, specific knowledge domain, and the
trade-offs the agent makes. "Approaches problems like a forensic investigator:
evidence first, hypothesis second. Will not speculate without data."

---

### AP-C05: Ambiguous routing in squads

**Problem:** Squad's routing table says "route security questions to security-agent
and development questions to dev-agent." What routes when the question is both?
**Why it fails:** The most interesting routing cases are compound. Without explicit
rules for compound intents, the squad routes arbitrarily.
**Fix:** Define compound intent routing explicitly. "If both security and development
intent detected: route to security-agent first, pass output to dev-agent."

---

### AP-C06: Design system with raw values only

**Problem:** `colors.yaml` only contains `blue-500: "#3B82F6"` with no semantic layer.
**Why it fails:** Buyers have to hunt through their codebase to change the primary color.
The value of a design system is the semantic layer — `primary: $blue-500` — not the
raw palette.
**Fix:** Always provide two layers: primitives (raw values) and semantics (named by role).

---

### AP-C07: Missing error states in component specs

**Problem:** Design system's `button.md` only defines the default state.
**Why it fails:** Interactive components have 4-5 states (default, hover, focus, active,
disabled). A button spec without states is incomplete — buyers can't implement it.
**Fix:** Document all interactive states. At minimum: default, hover, focus, disabled.
For destructive actions: add destructive variant.

---

## Quality Anti-Patterns

### AP-Q01: Exemplars that only show happy path

**Problem:** Skill has 3 exemplars that all show ideal, clear input producing
perfect output. None show ambiguity, edge cases, or failure modes.
**Why it fails:** Real usage always includes ambiguous inputs. Buyers discover quality
by seeing how the skill handles difficult cases — not just easy ones.
**Fix:** At least 1 of 3 exemplars must show: ambiguous input, edge case handling,
or graceful failure recovery.

---

### AP-Q02: Quality gate with trivial checks

**Problem:** SKILL.md Quality Gate contains: "Check that output is relevant to input"
and "Verify response is complete."
**Why it fails:** These checks cannot fail — they're not gates, they're reminders.
A quality gate should have checks that a well-crafted output might actually fail.
**Fix:** Quality gate checks must be specific and testable: "Verify that every claim
in the output has a source cited" or "Confirm activation protocol was executed
(at least 2 reference files loaded)."

---

### AP-Q03: Anti-patterns section that documents non-issues

**Problem:** "Anti-patterns" section says "Do not use this skill for illegal activities"
and "Do not provide false information."
**Why it fails:** These are not anti-patterns specific to the product. They waste the
buyer's reading time and signal the creator didn't think carefully about real misuse.
**Fix:** Anti-patterns should document how THIS specific product is commonly misused or
misunderstood. "Do not use this skill in `radical` mode for time-sensitive tasks —
radical mode is designed for thorough analysis, not speed."

---

### AP-Q04: No stress test documentation

**Problem:** Creator publishes at MCS-3 claiming "stress-tested" but no documentation
shows what was tested or what the results were.
**Why it fails:** MCS-3 agent review will ask: "What ambiguous inputs were tested?
What adversarial inputs? What edge cases?" With no documentation, the claim is
unverifiable.
**Fix:** Document stress tests as part of the product. A `tests/stress-results.md`
file showing inputs tried and outputs produced is sufficient evidence.

---

## Publishing Anti-Patterns

### AP-P01: Publishing without running `/validate`

**Problem:** Creator packages and publishes without running validation first.
**Why it fails:** MCS-1 structural checks catch 80% of publishable issues. Skipping
them means buyers receive a broken product, generating support questions and reviews.
**Fix:** Run `/validate` before packaging. Fix all failures. This is non-negotiable.

---

### AP-P02: Generic README that doesn't earn the install

**Problem:** README's first paragraph is a 3-sentence description of what the
product type is (explaining what a "skill" is to someone browsing the marketplace).
**Why it fails:** Buyers already know what a skill is. The first paragraph must
immediately answer: "what does THIS specific skill do and why would I want it?"
**Fix:** Lead with the specific capability and who benefits: "Analyzes security
vulnerabilities in Node.js code using OWASP Top 10 and produces remediation-ready
findings. For teams who want Claude Code to be a security audit partner."

---

### AP-P03: No CHANGELOG on version update

**Problem:** Creator updates a product from v1.0.0 to v1.1.0 without adding a
CHANGELOG entry.
**Why it fails:** Buyers who have the product installed don't know what changed.
They don't know if they need to update, or if the update is breaking.
**Fix:** Every version bump must have a CHANGELOG entry. See `references/best-practices/
versioning-guide.md` for CHANGELOG format.

---

### AP-P04: Version number that doesn't follow semver

**Problem:** Creator publishes `v1.0`, then `v1`, then `v2.0.0-beta`.
**Why it fails:** Marketplace metadata requires semver (MAJOR.MINOR.PATCH). Inconsistent
versioning breaks automated update checks.
**Fix:** Always use three-part semver: `1.0.0`, `1.1.0`, `2.0.0`. See
`references/best-practices/versioning-guide.md`.

---

### AP-P05: Secrets committed to product files

**Problem:** `config/variables.yaml` contains an actual API key in a "default value."
**Why it fails:** Critical security violation. MCS-1 `security-scan` catches common
patterns but not all. Publishing credentials is grounds for immediate delisting.
**Fix:** Never include real credentials anywhere in a published product. Use
`YOUR_API_KEY_HERE` or `process.env.MY_SERVICE_API_KEY` as examples.

---

## Summary Table

| ID | Category | Severity | Caught By |
|----|----------|---------|----------|
| AP-S01 | Structural | MCS-1 blocker | Automated |
| AP-S02 | Structural | MCS-1 blocker | Automated |
| AP-S03 | Structural | MCS-2 blocker | Automated |
| AP-S04 | Structural | MCS-1 blocker | Automated |
| AP-S05 | Structural | MCS-1 blocker | Automated |
| AP-C01 | Content | MCS-2 blocker | Automated |
| AP-C02 | Content | MCS-1 issue | Manual + User feedback |
| AP-C03 | Content | MCS-2 blocker | Automated |
| AP-C04 | Content | MCS-3 feedback | Agent review |
| AP-C05 | Content | MCS-2 feedback | Manual |
| AP-C06 | Content | MCS-2 blocker | Manual |
| AP-C07 | Content | MCS-2 feedback | Manual |
| AP-Q01 | Quality | MCS-3 feedback | Agent review |
| AP-Q02 | Quality | MCS-3 feedback | Agent review |
| AP-Q03 | Quality | MCS-3 feedback | Agent review |
| AP-Q04 | Quality | MCS-3 blocker | Agent review |
| AP-P01 | Publishing | All tiers | Workflow enforcement |
| AP-P02 | Publishing | Marketplace impact | Creator awareness |
| AP-P03 | Publishing | User trust | Creator awareness |
| AP-P04 | Publishing | MCS-1 blocker | Automated |
| AP-P05 | Publishing | Critical | Automated + Manual |
