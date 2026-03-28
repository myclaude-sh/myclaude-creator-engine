# Skill Exemplar: Systematic Reasoning Skill

**MCS Level:** 3 (State-of-the-Art)
**Demonstrates:** Activation Protocol (CE-D34), progressive depth modes (CE-D36),
question system (H11), quality gate, full references/ structure.

---

## File: `SKILL.md`

```markdown
# Systematic Reasoning Skill

> Forces rigorous, layer-by-layer analysis of decisions, systems, and arguments
> using the systematic methodology of epistemic discipline before conclusions.

**Version:** 2.1.0
**Category:** Skills
**Author:** @your-username

---

## When to Use

- You need to analyze a complex decision with multiple conflicting factors
- You're evaluating a system, architecture, or plan for hidden weaknesses
- You've reached a conclusion quickly and want to pressure-test it
- You need to build an argument that holds up under adversarial scrutiny
- You want to separate what you know from what you're assuming

## When NOT to Use

- Simple factual lookups with unambiguous answers (use direct response instead)
- Creative tasks where systematic decomposition kills flow (use free generation instead)
- Already well-defined problems with known solutions (use execution, not analysis)

---

## Activation Protocol

Before responding to any invocation:

1. **Load reasoning framework:** Read `references/reasoning-framework.md`
   — Contains: the 6-step systematic analysis framework, confidence tier definitions,
     and epistemic discipline rules
2. **Load exemplars:** Read `references/reasoning-exemplars.md`
   — Contains: 5 complete analysis examples across different domains showing
     what high-quality vs. low-quality reasoning looks like
3. **Load anti-patterns:** Read `references/anti-patterns.md`
   — Contains: 12 common reasoning failures with examples to avoid
4. **Identify user intent:** Determine:
   - Is this a decision analysis, system evaluation, or argument audit?
   - What depth mode is appropriate? (surface / dive / radical)
   - What is the stakes level? (informs recommended confidence thresholds)
5. **Run question system:** Check for required inputs (see below)

---

## Question System

Before generating analysis, check for these inputs:

| Input | Required | If Missing |
|-------|----------|-----------|
| The subject to analyze | Yes | Ask: "What specifically do you want to analyze? Provide the decision, system, or argument." |
| The goal of the analysis | No | Assume: "Identify weaknesses and improve decision quality" |
| Depth mode preference | No | Default to `dive` unless input signals urgency (use `surface`) or deep expertise needed (use `radical`) |
| Domain context | No | Infer from input; note inference explicitly |

When subject is ambiguous, ask ONE clarifying question before proceeding.
Never ask for information you can reasonably infer.

---

## Core Instructions

### Processing Logic

**Step 1 — Intake:** Restate what is being analyzed in your own words.
This forces comprehension before processing and catches misunderstandings early.

**Step 2 — Decompose:** Break the subject into its component parts:
- For decisions: What are the options? What are the constraints? What are the success criteria?
- For systems: What are the components? How do they interact? Where are the dependencies?
- For arguments: What are the claims? What is the evidence? What are the assumptions?

**Step 3 — Epistemic audit:** For each major claim or assumption:
- Is this known (evidence exists) or assumed (inferred)?
- What is the confidence level? (high / medium / low / unknown)
- What would change this assessment?

**Step 4 — Pressure test:** Apply the strongest counterargument you can construct.
If you cannot construct a real objection, the subject is either trivially correct or
you haven't looked hard enough.

**Step 5 — Synthesis:** What does the analysis reveal?
- What are the key risks or weaknesses?
- What are the key strengths?
- What is the recommended action or interpretation?

**Step 6 — Confidence declaration:** State overall confidence in the analysis.
Be explicit about what is known vs. inferred.

### Handling Ambiguity

- **Multiple valid interpretations:** State both, analyze both, then recommend which to use
- **Insufficient context:** Name the gap explicitly ("I don't know X, so I'm assuming Y")
- **Conflicting information:** Flag the conflict, don't quietly pick one

### Modes

| Mode | When to Use | What Changes |
|------|------------|-------------|
| `surface` | Quick scan, time-constrained | Steps 1-3 only, brief synthesis |
| `dive` | Standard analysis | All 6 steps, full output |
| `radical` | Deep expertise, no time constraint | All 6 steps + devil's advocate section + second-order effects + alternative framings |

Default: `dive`

---

## Output Structure

```
## Systematic Analysis: [Subject]
**Mode:** [surface | dive | radical]
**Domain:** [inferred domain]
**Stakes:** [low | medium | high]

### 1. Restatement
[What is being analyzed, in my own words]

### 2. Decomposition
[Components, broken down clearly]

### 3. Epistemic Audit
[Claims and assumptions with confidence levels]

### 4. Pressure Test
**Strongest objection:** [the real counterargument]
**Response to objection:** [how it holds up]

### 5. Synthesis
**Key risks:** [what could go wrong]
**Key strengths:** [what is solid]
**Recommendation:** [what to do / how to interpret]

### 6. Confidence
**Overall:** [high | medium | low]
**Confident about:** [specific elements]
**Uncertain about:** [specific elements]
```

---

## Quality Gate

Before delivering output:

- [ ] Did I restate the subject before analyzing? (Step 1 present)
- [ ] Did I separate known facts from inferred assumptions? (Step 3 present)
- [ ] Did I construct a real objection, not a straw man? (Step 4 genuine)
- [ ] Is my confidence level declared explicitly? (Step 6 present)
- [ ] Is the output actionable? (user can do something with this)

If any check fails: revise before delivering.

---

## Anti-Patterns

- **Conclusion-first analysis:** Stating the recommendation in Step 1, then reverse-engineering justification. Start with decomposition, end with synthesis.
- **Confidence theater:** Saying "high confidence" without declaring what evidence supports it.
- **Missing the counterargument:** A pressure test with only weak objections. The strongest counterargument often isn't the most obvious one.
- **Analysis paralysis:** Using `radical` mode for a low-stakes decision. Match depth to stakes.
- **Assumption blindness:** Treating inferences as facts without flagging them.

---

## Composability

- **As input to:** Decision-documenting workflows, technical proposal reviewers
- **As output from:** Research skills that gather raw material to analyze
- **In workflows:** Can be step `02-analyze` in any decision or architecture review workflow
```

---

## File: `references/reasoning-framework.md` (excerpt)

```markdown
# Systematic Reasoning Framework

## Core Principle

Epistemic discipline before conclusions. Know what you know vs. what you assume
before recommending anything.

## 6-Step Framework

### Step 1: Restatement
Purpose: Force comprehension before processing.
Rule: Cannot move to Step 2 until you can restate the subject without referencing the original.

### Step 2: Decomposition
Purpose: Reveal structure that was implicit.
Rule: Every complex thing can be decomposed. If you can't decompose it, you don't understand it.

### Step 3: Epistemic Audit
Purpose: Separate the known from the assumed.

Confidence tiers:
- **T1 (Known):** Direct evidence, verified data, confirmed facts
- **T2 (Inferred):** Reasonable inference from T1 evidence
- **T3 (Assumed):** Working assumption without direct evidence
- **T4 (Unknown):** Acknowledged gap in knowledge

...
```

---

## File: `references/reasoning-exemplars.md` (excerpt)

```markdown
# Reasoning Exemplars

## Exemplar 1: Architecture Decision Analysis

**Input:** "Should we use microservices or a monolith for our new platform?"

**Output (dive mode):**

## Systematic Analysis: Microservices vs. Monolith Architecture Decision
**Mode:** dive
**Domain:** Software architecture
**Stakes:** high

### 1. Restatement
Evaluating whether to build the new platform as a distributed microservices
architecture or a unified monolith, given an unstated team size, timeline,
and operational capability.

### 2. Decomposition
**Options:** Microservices | Monolith | Modular Monolith (hybrid)

**Key constraints that would change this decision:**
- Team size (< 5 people favors monolith heavily)
- Operational maturity (Kubernetes experience? monitoring?)
- Domain stability (known vs. still-discovering domains)
- Scale requirements (10 users vs. 10M users)

**Note:** None of these constraints were provided. Flagging as T3 assumptions.

### 3. Epistemic Audit
- T1: Microservices have higher operational overhead (Netflix, Google documented this)
- T1: Monolith is faster to develop initially for small teams
- T2: Platform will likely need to scale (inferred from "new platform" language)
- T3: Team has operational maturity for distributed systems (not stated)
- T3: Domains are well-understood enough to define service boundaries (not stated)

### 4. Pressure Test
**Strongest objection to recommending a monolith:**
"You'll have to rewrite it when you scale. Microservices now prevents technical debt."

**Response:** The "you'll have to rewrite it" argument assumes:
(a) you'll reach the scale where it matters, AND
(b) you can't incrementally extract services from a modular monolith.
Both assumptions are contested by evidence from successful companies (Shopify,
Stack Overflow, Basecamp).

### 5. Synthesis
**Key risk of microservices (given unknowns):** Service decomposition along wrong
boundaries is expensive to fix; distributed systems require operational maturity
most early teams don't have.

**Key risk of monolith:** Lock-in if team grows rapidly and service boundaries
become contentious.

**Recommendation:** Start with a **modular monolith** with clearly defined module
boundaries. Extract services when a specific service has clearly different scaling
requirements. This is the "strangler fig" approach — proven, reversible, pragmatic.

### 6. Confidence
**Overall:** medium
**Confident about:** Operational overhead of microservices; value of starting simple
**Uncertain about:** Team's operational maturity; actual scale requirements
If these two T3 assumptions are confirmed, confidence rises to high.

---

## Exemplar 2: Argument Audit (surface mode)

...
```

---

## File: `references/anti-patterns.md` (excerpt)

```markdown
# Reasoning Anti-Patterns

## AP-01: Motte and Bailey
**Pattern:** Defending a controversial position (bailey) by retreating to an obvious
truth (motte) when challenged.
**Detection:** Does the response change the claim under pressure without acknowledging it?
**Fix:** Pin the specific claim being defended. If it changes, name the change.

## AP-02: Availability Heuristic Reasoning
**Pattern:** Overweighting recent or vivid examples when estimating probability.
**Detection:** Is the evidence base representative, or just memorable?
**Fix:** Explicitly ask "what would a base rate analysis show?"

...
```

---

## Quality Verification

This exemplar demonstrates:

- [x] Activation Protocol with 4 load steps (CE-D34)
- [x] Question system with required/optional matrix (CE-D36 / H11)
- [x] Progressive depth modes: surface / dive / radical
- [x] Quality gate with specific, testable checks
- [x] References/ knowledge base with 3 files
- [x] Real domain expertise encoded (not AI-generatable without methodology)
- [x] Anti-patterns documented (H6)
- [x] Composability documented
- [x] MCS-3 criteria met
