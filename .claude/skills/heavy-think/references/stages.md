# Stages — Full Protocol

## Table of Contents
1. Stage 1 — Parallel Reasoning
   1.1 Trajectory generation
   1.2 Memory cache construction
   1.3 Five universal lenses
   1.4 Domain-specific lens customization
2. Stage 2 — Sequential Deliberation
   2.1 Mode selection (full)
   2.2 Deliberation prompt template
   2.3 Tier-3 voice-anchor mode

---

## 1. Stage 1 — Parallel Reasoning

### 1.1 Trajectory generation

K trajectories solve the problem **independently from scratch**. Independence is the load-bearing structural requirement.

**Diversity mechanism — temperature-primary.** Temperature ≥ 0.9 is the **primary** independence mechanism. Empirically, explicit Max-Diversity selection does not significantly outperform random sampling (Wang et al. 2026, App. A). Diversity emerges from stochastic sampling; it does not need to be imposed.

**Strategy hints (secondary diversity):**
- Algebraic vs geometric
- Top-down vs bottom-up decomposition
- Brute force vs elegant shortcut
- Abstract reasoning vs concrete example-driven

**Generic spawn template:**
```
Solve the following problem step by step. Show your complete reasoning chain
and arrive at a final answer.

Problem: {query}

Think carefully and solve this independently. Show all work.
[Optional strategy hint: "Try approaching this {algebraically | geometrically |
by working backwards | with a concrete example first} if possible."]
```

### 1.2 Memory cache construction

The cache is the bridge between Stage 1 and Stage 2. Its quality directly determines deliberation quality.

**Pruning protocol:**
- **Extract:** final answer · key reasoning steps · critical branching decisions · novel approaches · error-recovery moments.
- **Remove:** verbose intermediate computation · repetitive restatements · exploratory dead-ends that don't inform the final chain.
- **Target:** each pruned trajectory ≤ 30% of original token count.
- **Shuffle order** after pruning to defeat positional/recency bias (empirically documented).

**Cache budget enforcement:** memory cache ≤ 60% of available context for deliberation. If exceeded, increase pruning aggressiveness or reduce K. Always preserve deliberation budget over cache completeness.

**Serialization format:**
```
# ====== Problem ======
{problem}
# ====== Problem End ======

# ====== Reasoning Trajectories ======

# ----- Trajectory #1 -----
{pruned_trajectory_1}

# ----- Trajectory #2 -----
{pruned_trajectory_2}

# ----- Trajectory #K -----
{pruned_trajectory_K}

# ====== Trajectories End ======
```

### 1.3 Five universal lenses (default framework)

When no domain-specific decomposition is available, use the five universal lenses. Derived from Aristotelian causation extended with temporality. Designed to be philosophically orthogonal — substantive independence, not stylistic variation.

| Lens | Mother-question | Vocabulary anchors | Artifact |
|------|-----------------|--------------------|----------|
| **Anatomy** (Form) | How is this organized? Parts and relations? | modules, interfaces, hierarchy, scope, granularity, decomposition, layering, encapsulation | Structural map |
| **Mechanism** (Cause) | How does this work? Through what dynamic? | causes, dynamics, feedback, latency, throughput, bottleneck, coupling, propagation | Causal/process model |
| **Purpose** (Telos) | What is this for? Success means what? | intent, fit, success criteria, jobs-to-be-done, stakeholders, value, alignment | Statement of purpose with success conditions |
| **Context** (Origin) | Where does this come from? Environment? | precedent, tradition, environment, constraints, dependencies, history, ecosystem | Contextual map |
| **Trajectory** (Future) | Where does this go? Futures opened/closed? | consequences, second-order effects, optionality, evolution, lock-in, path-dependence | Trajectory analysis with risks/reversibility |

**When to use universal lenses:**
- T1 math/code → generic trajectories with strategy hints are sufficient. Skip lenses.
- T2 analysis/strategy/diagnostic → universal lenses add structural diversity that temperature alone does not produce.
- Domain provides better decomposition → substitute (§1.4).

**Per-lens prompt template:**
```
Analyze the following problem exclusively through the {LENS_NAME} lens.

Mother-question: {MOTHER_QUESTION}
Stay within this vocabulary: {VOCABULARY_ANCHORS}
Address only dimensions that fit this lens; defer the rest to their owning lenses.

Problem: {query}

Produce your analysis as a {ARTIFACT_TYPE}.
```

### 1.4 Domain-specific lens customization

Substitute when the domain provides more incisive decomposition.

**Customization rules:**
- **Replace existing lenses rather than adding new ones.** K must remain manageable.
- Each replacement lens **substantively distinct**.
- Each replacement carries its **own vocabulary anchor** to prevent lens collapse.
- Document the substitution in the output rationale.

**Catalog of valid customizations:**

| Domain | Lenses |
|--------|--------|
| Code review | Security · Performance · Maintainability · Testability · Edge Cases |
| Architecture decision | Service Boundaries · Failure Modes · Business Velocity · Team Topology · Operational Cost |
| Medical differential | Anatomic · Infectious · Autoimmune · Metabolic · Iatrogenic |
| Strategic decision | Porter's Forces · Jobs-to-be-Done · Financial NPV · Optionality · Competitive Response |
| Diagnostic investigation | System Topology · Causality Chain · Impact Assessment · Recent Changes · Recurrence Risk |

Vocabulary discipline matters — anchors are what keep lenses substantively distinct during deliberation. Each lens reasons predominantly in its own conceptual vocabulary.

---

## 2. Stage 2 — Sequential Deliberation

This is **synthesis under explicit criteria**, not selection from candidates. The K trajectory artifacts arrive; the deliberator reads them, classifies the situation, identifies tensions and convergences, applies criteria, and produces an integrated result.

### 2.1 Mode selection (full)

```
answer_distribution = distribution of final answers across K trajectories
agreement_ratio    = freq(most_common_answer) / K
reasoning_divergence = degree to which reasoning chains differ structurally

IF agreement_ratio ≥ 0.75 AND task has verifiable correctness criteria:
  MODE = VERIFICATION
  Focus: validate consensus correctness. Check whether any dissenting
  trajectory has stronger underlying logic despite minority status.
  A rigorous minority can be correct when the majority makes the same
  error independently (shared blind spot).

ELSE IF agreement_ratio < 0.50 OR reasoning_divergence is high:
  MODE = SYNTHESIS
  Focus: genuine cross-trajectory synthesis. Identify what each
  trajectory got right. Resolve contradictions. Cross-pollinate
  partial insights into a complete solution. May need to re-derive
  from scratch using trajectory insights as input.

ELSE:
  MODE = HYBRID
  Focus: verify the leading position while actively mining minority
  trajectories for missed insights or edge cases.
```

**Why mode matters.** Empirically, deliberation functions as an implicit verifier in most cases (majority agreement → verify), and as a genuine synthesizer when trajectories diverge significantly or with frontier models. Treating all deliberation as synthesis wastes capacity; treating all as verification misses synthesis opportunities. Match mechanism to situation.

Use `Run python scripts/mode_select.py --answers "..."` to compute deterministically.

### 2.2 Deliberation prompt template

```
You are analyzing {K} independent reasoning attempts for the same problem.

# ====== Problem ======
{query}
# ====== Problem End ======

{serialized_memory_cache}

Deliberation mode: {VERIFICATION | SYNTHESIS | HYBRID}

Execute these steps:

1. ANSWER DISTRIBUTION — What answers appear across trajectories and how
   frequently? Map the landscape before analyzing.

2. REASONING EVALUATION — For each distinct answer/approach:
   - Is the logical chain sound? Where does it break?
   - What assumptions does it make? Are they justified?
   - What does it handle well? What does it miss?

3. MODE-SPECIFIC ANALYSIS:
   [VERIFICATION] The majority says {X}. Is their shared reasoning valid?
     Does any dissenting trajectory expose a flaw the majority missed?
   [SYNTHESIS] Trajectories diverge. What partial truths does each hold?
     What unified answer absorbs the best of each while resolving
     contradictions?
   [HYBRID] Verify the leading answer. Then: does any minority trajectory
     add an insight the majority missed?

4. CRITICAL CHECK — Could ALL trajectories be wrong? If the most common
   error pattern is shared (same faulty assumption, same calculation
   mistake), the consensus is contaminated. Re-derive independently using
   the trajectories' errors as negative examples.

5. FINAL ANSWER — State the answer with confidence (High/Moderate/Low).
   Show key supporting reasoning. Match output format to domain.

Rules:
- Majority is a SIGNAL, not proof. Do NOT default to "most said X, therefore X."
- You may re-derive if no trajectory is satisfactory.
- Match output language to the original query.
- Match output format to domain conventions.
```

### 2.3 Tier-3 voice-anchor mode

For preference-based or creative tasks where heavy thinking risks mediocrity-by-committee:

- **Reduce K to 3** (Light) to limit averaging effects.
- **Designate one trajectory as voice anchor** — the one with the strongest, most distinctive perspective or stylistic identity.
- **Use remaining trajectories as stress-tests** rather than co-equal sources. They check structural integrity, logical coherence, factual accuracy while preserving the anchor's voice.
- **Synthesis criterion shifts:** from "best integrated answer" → "voice anchor refined by valid structural critiques from other trajectories."
- **Be explicit with the user:** "This task has subjective components — using voice-anchor mode rather than full integration."

This preserves rigor while respecting that a strong singular vision often beats committee average in creative and aesthetic work.
