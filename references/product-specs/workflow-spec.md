# Product Spec: Workflows

## Definition

Workflows are multi-step automation sequences that compose skills, agents, and tools
into repeatable processes. Workflows make implicit processes explicit — they transform
"things I do repeatedly" into a documented, shareable, runnable sequence.

A workflow is NOT:
- A skill (skills are single-pass cognitive routines; workflows are multi-step sequences)
- A squad (squads route between agents; workflows sequence steps with dependencies)
- A procedure document (workflows are executable, not just descriptive)

A workflow IS:
- A defined sequence of steps with explicit inputs, outputs, and dependencies
- A repeatable process that can be run consistently by anyone
- A composable unit that can be part of a larger system

---

## Canonical File Structure

```
workflow-name/
├── WORKFLOW.md            # Workflow definition (REQUIRED)
├── README.md              # Setup and usage (REQUIRED)
├── steps/                 # Individual step definitions
│   ├── 01-step-name.md
│   ├── 02-step-name.md
│   └── nn-step-name.md
├── config/
│   └── variables.yaml     # Configurable parameters
└── examples/              # Execution examples
    └── example-run.md
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `WORKFLOW.md` | Complete workflow definition | MCS-1 |
| `README.md` | Usage documentation | MCS-1 |
| `steps/01-*.md` through `steps/03-*.md` | At least 3 step files | MCS-1 |

---

## Required Sections in WORKFLOW.md

### 1. Workflow Name and Purpose

```markdown
# Workflow Name

**Purpose:** One sentence describing what process this automates
**Trigger:** [Manual / Event-driven / Scheduled]
**Duration:** [Estimated time to complete]
**Tools Required:** [List of tools this workflow needs]
```

### 2. Trigger Conditions

When should this workflow run? Be specific:
- What user action or system event starts the workflow?
- What preconditions must be true before starting?
- What data/files/context must exist before the workflow can run?

### 3. Input Requirements

Everything the workflow needs to start successfully:
- Required inputs (workflow fails without these)
- Optional inputs (enhance output but not required)
- Input format specifications
- Validation checks to run on inputs

### 4. Step Sequence with Dependencies

The heart of the workflow. For each step:
- Step name and number (1-indexed, zero-padded: 01, 02, etc.)
- What the step does
- Inputs: what the step consumes
- Outputs: what the step produces
- Dependencies: which previous steps must complete first
- Reference to step file in `steps/`

```markdown
## Steps

| Step | Name | Depends On | Input | Output |
|------|------|-----------|-------|--------|
| 01 | [name] | — | [input] | [output] |
| 02 | [name] | 01 | [output of 01] | [output] |
| 03 | [name] | 01, 02 | [outputs] | [final output] |
```

### 5. Output / Deliverables

What the completed workflow produces:
- Specific files, data, or artifacts created
- Format specifications for outputs
- Where outputs are stored

### 6. Error Handling and Fallbacks

What happens when steps fail:
- Retry logic (when to retry, how many times)
- Fallback paths (alternative steps when primary fails)
- Abort conditions (when to stop and alert the user)
- State preservation (how to resume a failed workflow)

### 7. Completion Criteria

What "done" looks like:
- Acceptance criteria for workflow output
- How to verify the workflow completed successfully
- Quality checks on final outputs

---

## MCS Requirements

### MCS-1: Publishable

**Universal:**
- [ ] Valid WORKFLOW.md with all 7 required sections
- [ ] README.md with: what the workflow does, prerequisites, how to run, expected outputs
- [ ] At least 3 step files in `steps/`
- [ ] Metadata complete
- [ ] No broken file references
- [ ] No syntax errors
- [ ] License from approved list

**Workflow-Specific:**
- [ ] Step dependencies explicitly defined
- [ ] Inputs and outputs documented for each step
- [ ] Trigger conditions specified

### MCS-2: Quality

**Universal (beyond MCS-1):**
- [ ] `config/variables.yaml` with configurable parameters
- [ ] Error handling documented for each step
- [ ] 2+ execution examples with realistic inputs/outputs
- [ ] Anti-patterns section
- [ ] Tested with 5 different input scenarios
- [ ] No placeholder content
- [ ] Semver versioning

**Workflow-Specific:**
- [ ] All configurable parameters documented in `variables.yaml`
- [ ] Execution examples show full workflow run (not just one step)
- [ ] Retry logic and abort conditions specified
- [ ] State preservation strategy documented

### MCS-3: State-of-the-Art

**Universal (beyond MCS-2):**
- [ ] Composable with other workflows (can be nested or chained)
- [ ] Adaptive modes (fast/thorough, minimal/full, etc.)
- [ ] Stress-tested with missing inputs, step failures, invalid data
- [ ] Performance metrics (steps count, token budget, estimated time)
- [ ] Cognitive architecture documented (why this sequence vs. alternatives)
- [ ] CHANGELOG with versioning history
- [ ] 5+ examples including failure recovery scenarios
- [ ] Differentiation statement

**Workflow-Specific:**
- [ ] Workflow tested as standalone AND as component in a system
- [ ] Parallel step execution documented where applicable
- [ ] Recovery procedures for each failure mode
- [ ] Integration patterns with skills, agents, and squads documented

---

## Anti-Patterns for Workflows

### Structural
- **Steps without inputs/outputs:** Steps describe what happens but not what data flows between them. The workflow is a list of actions, not a connected sequence.
- **Missing `steps/` directory:** All steps defined inside WORKFLOW.md as prose. Steps should be individual files for maintainability and referenceability.
- **No error handling:** Workflow assumes all steps succeed. First failure leaves everything in an undefined state.

### Content
- **Implicit dependencies:** "Step 3 assumes step 2 has been completed" — written as prose instead of explicit dependency declarations. Dependencies must be machine-readable.
- **Steps that do too much:** One step that covers intake, processing, AND output. Each step should do one thing. Complex steps should be broken into sub-steps.
- **Variables hardcoded in steps:** Configuration values (paths, thresholds, formats) embedded in step files instead of `config/variables.yaml`. Makes the workflow non-reusable across contexts.

### Quality
- **Examples that skip failures:** Every execution example shows a perfect run. Real users encounter failures. Show at least one failure recovery path.
- **No completion criteria:** Workflow ends but there's no definition of what "complete" means. Users don't know if they succeeded.

---

## Discovery Questions (from §7)

When creating a workflow, answer these before scaffolding:

1. What process does this workflow automate? (what are you doing repeatedly that this should formalize)
2. What triggers it? (manual invocation, event, schedule, or when another workflow completes)
3. What are the required inputs and expected outputs?
4. How many steps are needed and what are the dependencies between them?
5. What happens when a step fails? (retry? fallback? abort? alert?)
6. What tools or external services does it need? (file system, web, code execution, APIs)
7. Should this workflow be used standalone or as a component in a larger system?

---

## DNA Requirements

For the complete DNA pattern applicability matrix for this product type,
see `product-dna/workflow.yaml`. That file defines:
- Which of the 18 DNA patterns (D-01 to D-18) are required vs optional
- Validation checks per pattern (grep/glob commands)
- Template file mapping with DNA injection points
- Frontmatter fields (Anthropic Agent Skills spec)
- Discovery questions for /create

**MCS scoring:** `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
See `references/quality/mcs-spec.md` for full scoring formula.
