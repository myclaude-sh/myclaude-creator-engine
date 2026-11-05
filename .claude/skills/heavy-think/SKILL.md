---
name: heavy-think
description: Execute heavy parallel reasoning followed by criterion-driven synthesis when single-pass thinking is insufficient. Use when: (1) complex STEM/math/code with non-obvious solutions, (2) diagnostic investigation under uncertainty, (3) architecture or strategic decision with irreversible stakes, (4) multi-stakeholder analysis with conflicting framings, (5) user explicitly asks for deliberation, multi-perspective, or heavy thinking, (6) prior single-pass attempt was judged inadequate. Do NOT use for simple factual queries, casual conversation, retrieval tasks, time-critical brief answers, or subjective creative work (unless voice-anchor mode requested). Anti-loop guard prevents recursive self-invocation. Keywords: heavy-think, deliberation, parallel reasoning, synthesis, multi-perspective, K-trajectories, verification, deep reasoning, Kairo, deliberate, robust reasoning.
---

# HeavyThink — Heavy Thinking as Inner Skill

**Version:** 3.1.1 · **Empirical basis:** Wang et al. (2026), *HeavySkill*.

## Table of Contents

1. [Quick-Start (the core loop)](#quick-start-the-core-loop)
2. [Activation](#activation)
3. [Constraint-aware execution](#constraint-aware-execution-run-before-stage-1)
4. [Stage 1 — Parallel Reasoning](#stage-1--parallel-reasoning-essentials)
5. [Stage 2 — Sequential Deliberation](#stage-2--sequential-deliberation-essentials)
6. [Confidence gradient](#confidence-gradient-mandatory-in-output)
7. [Output structure](#output-structure)
8. [Verification](#verification-binary-checklist--run-before-delivery)
9. [Iteration · Dual-model · Composability](#iteration--dual-model--composability--empirical-defaults)
10. [Pocket Reference](#pocket-reference-load-this-not-the-full-doc-when-executing)
11. [Scripts](#scripts)
12. [References](#references-load-on-demand)

**Dependencies:** scripts use only the Python standard library — no `pip install` needed.

> **Core claim.** Any problem that gains from independent perspectives followed by criterion-driven synthesis becomes tractable when perspectives are diverse, synthesis is criterion-driven (not vote-driven), and execution is constraint-aware.
>
> **Empirical basis.** Wang et al. (2026) — parallel reasoning + sequential deliberation outperforms single-pass and Best-of-N voting on verifiable tasks. Synthesis stage produces correct answers absent from any individual trajectory in ~50% of frontier-model trials.
>
> **Honest limitation.** Gains are marginal or negative on subjective/preference tasks. Strongest where correctness is verifiable.

**Operate as a deliberate reasoner.** Every conclusion auditable. Every framing provisional. Tensions are features. Do not narrate the protocol — manifest it through output quality.

---

## Quick-Start (the core loop)

```
constraint-check → K parallel trajectories → prune+shuffle cache →
classify mode → deliberate → confidence → answer
```

1. **Activate?** §Activation below. If borderline, ask one clarifying question instead.
2. **Calibrate K, N.** Light=3·1 · Standard=5·1 · Deep=5–8·1–2.
3. **Constraint check.** Run `Run python scripts/constraint_check.py --context <N> --K <K>`. If K<3 → abort to enriched single-pass.
4. **Generate K trajectories** independently (temperature ≥ 0.9, optional strategy hints).
5. **Prune** each to ≤30% of original, **shuffle** order, build cache.
6. **Classify deliberation mode** via `Run python scripts/mode_select.py --answers <list>` → Verification / Synthesis / Hybrid.
7. **Deliberate** under hierarchical criteria: Correctness → Completeness → Consistency → Elegance → Operability → Robustness.
8. **Answer first.** Confidence: High/Moderate/Low. Meta-analysis only on request or Low confidence.

For full stage protocols load `references/stages.md`. For failure modes load `references/failure-modes.md`. For verification checklist load `references/verification.md`. For iteration/dual-model/composability load `references/advanced.md`.

---

## Activation

### Activate when
- User explicitly asks for heavy thinking, multi-perspective analysis, deliberation, or robust reasoning.
- Complex reasoning where single-pass is likely insufficient.
- Math, logic, algorithmic problems with non-obvious solutions.
- Tasks where correctness is critical and verifiable.
- High-stakes decisions where error cost justifies compute cost.
- Multiple valid framings — choosing among them is part of the task.
- A prior single-pass attempt was judged inadequate.

### Do NOT activate when
- Simple factual queries or information retrieval.
- Casual conversation.
- User requested a brief or direct answer.
- Subjective creative tasks (unless voice-anchor mode requested — see `references/stages.md` §Tier-3).
- Time-criticality outweighs depth (offer Light mode and proceed).
- Already activated in this turn (anti-loop).
- Primarily retrieval, not reasoning.

### Fitness tiers (calibrate expectations)

| Tier | Task | Expected gain | Confidence |
|------|------|---------------|------------|
| **T1** | STEM, math, code, formal logic, verifiable | +5–30% accuracy | High — empirically validated |
| **T2** | Diagnosis, architecture, strategy, multi-source analysis | Meaningful, variable | Moderate — structurally plausible |
| **T3** | Creative, subjective, aesthetic | Marginal to negative | Low — documented limitation |

Tier 3 requires explicit user request and uses voice-anchor mode (`references/stages.md`).

### Calibration heuristic (sequential — first match decides)

1. Reversible within hours, low-cost? → **Light** (K=3, N=1)
2. Spans >2 professional domains? → **Deep** (K=5–8, N≤2)
3. Irreversible or commits significant resources? → **Deep**
4. SME would need >1 sitting? → **Standard** (escalate to Deep if ≥2 domains)
5. None of the above? → **Standard** (K=5, N=1)

Uncertain → default to Standard, offer to escalate.

### Anti-loop guard

If heavy-think trajectories already exist in current turn context, operate in direct mode without spawning new parallel reasoning.

### Ambiguity rule

Borderline activation → one clarifying question is cheaper than a full pipeline executed off-target.

---

## Constraint-aware execution (run before Stage 1)

```
available    = context_window − system_prompt − conversation
cache_est    = K × ~1200 tokens per pruned trajectory
delib_budget = available − cache_est

R1: cache_est ≤ 0.6 × available           else reduce K
R2: delib_budget ≥ 2000 tokens            else reduce K
R3: K ≥ 3                                 else ABORT → enriched single-pass + self-critique
R4: K × per_trajectory_latency ≤ target   else reduce K
```

Use `Run python scripts/constraint_check.py` to compute. Log any K reduction in one sentence.

---

## Stage 1 — Parallel Reasoning (essentials)

K trajectories solve the problem **independently from scratch**. Independence is load-bearing.

- **Diversity primary mechanism: temperature ≥ 0.9.** Random sampling > explicit Max-Diversity selection (Wang et al. 2026, App. A).
- **Strategy hints (secondary):** algebraic vs geometric, top-down vs bottom-up, brute force vs elegant, abstract vs example-driven.
- **Five universal lenses** (when problem is T2 analysis/strategy and no domain-specific decomposition fits): Anatomy / Mechanism / Purpose / Context / Trajectory. See `references/stages.md` for vocabulary anchors and prompts.
- **Domain lenses** replace universal when more incisive (code review, architecture, medical differential, strategic, diagnostic). See `references/stages.md`.
- **Cache construction:** prune each trajectory to ≤30% (keep final answer, key steps, branching decisions, error-recovery; remove verbose computation, dead-ends, restatements). **Shuffle** to defeat recency bias. Cache ≤ 60% of available context.

Prompts, vocabulary anchors, and serialization format → `references/stages.md`.

---

## Stage 2 — Sequential Deliberation (essentials)

**Synthesis under criteria, not selection from candidates.**

### Mode selection

```
agreement = freq(most_common_answer) / K

agreement ≥ 0.75  AND verifiable  → VERIFICATION  (validate consensus; mine dissent for stronger logic)
agreement < 0.50  OR  high divergence → SYNTHESIS  (cross-pollinate partial truths; resolve contradictions; may re-derive)
otherwise                              → HYBRID    (verify majority + mine minority for missed insight)
```

### Synthesis criteria (apply in order; higher overrides lower)

1. **Correctness** — supreme on verifiable tasks. Elegant ≠ correct.
2. **Completeness** — address every concern raised. Silent omission = failure.
3. **Internal consistency** — resolve conflicts, don't merely report them.
4. **Elegance** — simpler when correctness/completeness tied (unless robustness suffers).
5. **Operability** — actionable. Unclear next step = incomplete synthesis.
6. **Robustness** — anticipate failure modes; embed mitigations.

### Mandatory steps

1. Identify tensions explicitly.
2. Identify convergences (same conclusion via independent chains = robust signal).
3. Resolve each tension via criteria; document which criterion decided.
4. Compose integrated answer; verify completeness + operability.

### Critical check
Could **all** trajectories be wrong (shared faulty assumption)? If yes, re-derive independently, treating their errors as negative examples.

### Anti-patterns
- ❌ "Take a bit from each" → dilution.
- ❌ "Most said X, so X" → voting, not deliberation.
- ❌ Concatenating trajectories as sections → collation.
- ❌ Deciding without naming the criterion → arbitrary.
- ❌ Hiding tensions to appear coherent → suppresses problem structure.
- ❌ Presenting meta-analysis instead of the answer.

Full prompt template + Tier-3 voice-anchor mode → `references/stages.md`.

---

## Confidence gradient (mandatory in output)

| Level | Trigger | Output language |
|-------|---------|-----------------|
| **High** | ≥3 trajectories converge with sound independent reasoning; verification confirms | "The evidence strongly supports…" |
| **Moderate** | Convergence with 1–2 unverified assumptions, or tensions resolved via criteria 4–6 | "It is reasonable to conclude… given…" |
| **Low** | Mostly judgment calls, or high divergence with no clear winner | "Working hypothesis: … Requires further validation because…" |

---

## Output structure

### Default — answer-first

```
[Final answer in domain-native format]

Confidence: High | Moderate | Low
[One sentence: what would change this conclusion, if confidence < High]
```

### Extended (on user request OR Low confidence OR multiple defensible answers)

```
[Final answer]

## Deliberation Summary
- Key tensions and how resolved (which criterion decided)
- What each trajectory contributed
- What deliberation produced beyond any single trajectory

## Confidence: [Level]
- Evidence basis
- What additional info would raise confidence
```

### Convention matching
- **Language:** match the user's query language.
- **Format:** math → `\boxed{}` · code → fenced blocks · strategy → prose with clear recommendation.
- **Register:** concise if they were concise; depth if they invited it.

---

## Verification (binary checklist — run before delivery)

```
□ Constraint check passed (cache fits, K≥3, latency ok)
□ K trajectories show meaningful diversity (not collapsed)
□ Cache pruned, shuffled, ≤60% of context
□ Mode correctly selected (Verification / Synthesis / Hybrid)
□ Deliberation = analysis, not selection
□ All 6 synthesis criteria considered in order
□ Confidence stated and matches evidence pattern
□ Final answer clear, actionable, domain-native format
□ Output language matches query language
□ Pre-iteration diagnostic passed (if N>1)
□ Problem-specific failure modes anticipated
□ Caveat naming what would change conclusion present (if conf < High)
```

≥2 fail → return to Stage 2. 1 fail → fix inline.

Full failure-mode catalog (6 modes with symptom · cause · mitigation) → `references/failure-modes.md`.

---

## Iteration · Dual-model · Composability · Empirical defaults

Default N=1. Iterate only when pre-iteration diagnostic signals addressable gaps. Cap N=3 (returns negative beyond).

For pre-iteration diagnostic, dual-model configuration, RLVR scaling, adaptive K, skill emergence, and reference parameter tables → `references/advanced.md`.

---

## Pocket Reference (load this, not the full doc, when executing)

```
╔═══════════════════════════════════════════════════════════════╗
║                  HEAVYTHINK · POCKET REFERENCE                ║
╠═══════════════════════════════════════════════════════════════╣
║ LOOP   constraint → K parallel → prune+shuffle → mode →       ║
║        deliberate → confidence → answer                       ║
║                                                               ║
║ TIERS  T1 STEM/code (+5–30%) · T2 strategy (variable) ·       ║
║        T3 creative (voice-anchor only)                        ║
║                                                               ║
║ CALIB  Light K=3 N=1 · Standard K=5 N=1 · Deep K=5–8 N≤2      ║
║                                                               ║
║ CONSTR cache ≤60% · K≥3 (else abort) · log reductions         ║
║                                                               ║
║ MODES  ≥75% agree → VERIFY · <50% → SYNTHESIZE · else HYBRID  ║
║                                                               ║
║ CRIT   1 Correct · 2 Complete · 3 Consistent · 4 Elegant ·    ║
║        5 Operable · 6 Robust                                  ║
║                                                               ║
║ CONF   High ≥3-converge+sound · Moderate convergence+gaps ·   ║
║        Low judgment-driven                                    ║
║                                                               ║
║ STOP-ITER  HM≈HP · no new resolution · reasoning weakening ·  ║
║            N≥3                                                ║
║                                                               ║
║ FAIL   collapse · selection-not-synth · operability vacuum ·  ║
║        confidence misalign · overload · cascade               ║
║                                                               ║
║ OUT    answer first · meta on request or Low conf · match     ║
║        language + format + register                           ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Scripts

| Script | Run | When |
|--------|-----|------|
| `constraint_check.py` | `Run python scripts/constraint_check.py --context <tokens> --K <K> [--per-traj <tokens>] [--latency-target <s>] [--per-traj-latency <s>]` | Before Stage 1 — compute cache fit, K viability |
| `mode_select.py` | `Run python scripts/mode_select.py --answers "a,a,b,a,c"` | Before Stage 2 — classify Verification / Synthesis / Hybrid |
| `pre_iteration.py` | `Run python scripts/pre_iteration.py --hm <q> --hp <q> --prev-answer <s> --new-answer <s> --reasoning-strength <prev,new> --N <n>` | Before any iteration N>1 — gate against decay/cascade |

All stdlib-only. No external dependencies.

---

## References (load on demand)

| File | Provides |
|------|----------|
| `references/stages.md` | Full Stage 1+2 protocols · five universal lenses with vocabulary anchors · domain lens catalog · prompt templates · Tier-3 voice-anchor mode |
| `references/failure-modes.md` | Six named failure modes (collapse · selection-not-synthesis · operability vacuum · confidence misalignment · protocol overload · contamination cascade) with symptom · cause · mitigation |
| `references/verification.md` | Extended verification checklist with adjudication rules |
| `references/advanced.md` | Iteration mechanics · pre-iteration diagnostic · dual-model · RLVR scaling · adaptive K · skill emergence · empirical reference values · activation flow diagram · changelog |

---

*HeavyThink v3.1 — answer-first · constraint-aware · dual-mode · progressive-disclosure. Designed to survive its own §Protocol-Overload failure mode.*
