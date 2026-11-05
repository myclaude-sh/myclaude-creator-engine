# Advanced — Iteration · Dual-Model · Composability · Empirical Defaults

## Table of Contents
1. Iteration mechanics + pre-iteration diagnostic
2. Dual-model support
3. Composability
4. Evolution paths (RLVR · adaptive K · vocabulary discovery · skill emergence)
5. Empirical reference values
6. Activation decision flow
7. Changelog

---

## 1. Iteration mechanics

### 1.1 Pre-iteration diagnostic

Iteration earns its cost only when the first pass reveals **specific addressable gaps**. Default N=1. Extend only on signal.

```
PRE-ITERATION DIAGNOSTIC (execute before any N > 1):

CHECK 1: Mean ↔ potential gap.
  IF HM (mean deliberation quality) ≈ HP (best deliberation quality):
    STOP. Ceiling reached. Further iteration trades potential for consistency.

CHECK 2: New resolution.
  IF iteration N produced same conclusion as N-1 with no stronger reasoning:
    STOP. Consistency-without-insight decay.

CHECK 3: Reasoning trajectory.
  IF iteration N produced same answer as N-1 with WEAKER supporting reasoning:
    STOP IMMEDIATELY. Contamination cascade.

CHECK 4: Iteration cap.
  IF N ≥ 3:
    STOP. Empirically, returns are negative past N=3.

CHECK 5: User satisfaction.
  IF user signals the answer is sufficient:
    STOP.

ALL PASS → ITERATE.
```

Use `Run python scripts/pre_iteration.py` to gate.

### 1.2 Iteration mechanics (when warranted)

1. Append previous deliberation output as "Expert Trajectory #(K+1)" in the memory cache.
2. **Re-shuffle all trajectories** including the new one (defeat recency bias).
3. Frame the appended trajectory as "a previous analysis attempt" — not as "current best."
4. Re-run Stage 2 with the augmented cache.
5. Track quality improvement; if Δ not measurable on verifiable metrics, stop.
6. When stopping, name the stop reason briefly: "Stopping at iteration 2: subsequent passes converging without new resolution."

---

## 2. Dual-model support

Empirically, parallel reasoning and sequential deliberation require **different cognitive capabilities**:

- **Parallel reasoning (πθ)** benefits from strong intrinsic reasoning. The model needs to solve hard problems from scratch.
- **Sequential deliberation (πϕ)** benefits from strong analysis, comparison, and synthesis. Does **not** require peak reasoning power. Models with good instruction-following and analysis can deliberate effectively even with weaker standalone reasoning.

A non-reasoning instruction-following model that achieves only 12.8% on AIME25 independently can still produce strong deliberation results when given good reasoning trajectories to analyze (Wang et al. 2026, §4.2).

| Config | When | Trade-off |
|--------|------|-----------|
| **Single-model** (πθ = πϕ) | Default. Simplest. | Higher cost if model expensive; may under-utilize deliberation |
| **Dual-model** (πθ ≠ πϕ) | Advanced. Smaller/cheaper for trajectories; larger/general for deliberation | Better cost-efficiency; needs two endpoints; slight coordination overhead |

Dual-model is an optimization, not a requirement. Start single-model; graduate when cost-efficiency matters.

---

## 3. Composability

Heavy-think is a capability, not a destination.

- **Receives input from:** research tools, retrieval systems, user queries, prior analyses, information-gathering skills.
- **Delivers output to:** implementation tools (code generation, document drafting), evaluation skills (testing, review), or directly to the user.
- **May be invoked by:** orchestration systems that detect high-complexity problems.
- **Complements (rather than replaces) domain-specialized skills** with their own rigorous protocols. When such skills exist, **defer or co-invoke** — keep their boundaries intact.

When another skill is more appropriate, delegate explicitly rather than absorb.

---

## 4. Evolution paths

### 4.1 RLVR scaling (Reinforcement Learning from Verifiable Rewards)
- ~10% improvement on HM@K metrics in initial training.
- **Constraint:** K ≥ 16 may cause entropy collapse during training with smaller models (≤7B).
- **Recommendation:** start with K=8 for RLVR; scale K cautiously.
- Train deliberation capability separately from reasoning capability when possible.

### 4.2 Adaptive K
Estimate problem difficulty from surface features, then set K proportionally. Automates the Light/Standard/Deep calibration that is currently manual.

### 4.3 Vocabulary discovery
During deliberation, watch for patterns that recur across multiple invocations but lack canonical naming. When detected: surface the pattern, propose a candidate name, note where observed. Converts the skill from a static operator into a vocabulary-generating operator over time.

### 4.4 Skill emergence
If a synthesis structure (specific lens combination + criteria + domain constraints) appears reusable across a class of problems, flag explicitly as a candidate sub-skill:

> "This synthesis structure ({lenses} + {criteria}) appears reusable for {problem class}. Recommend extracting as a domain-specific skill."

Converts heavy-think from flat operator to **skill-generating** operator. Over repeated invocations the user accumulates a library of derived skills, each addressing a more specific problem class with greater efficiency.

---

## 5. Empirical reference values

From Wang et al. (2026). Treat as starting points, not validated constants outside original experimental conditions (RL-trained models on STEM/code benchmarks).

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| K (parallel trajectories) | 5 | 3–8 | K>8 diminishing returns; K=16+ only with large context |
| K⁽¹⁾ (deliberation outputs) | 4 | 1–4 | More than 4 adds noise without clear gain |
| N (iterations) | 1 | 1–3 | Past N=3, HP typically decays |
| Temperature (Stage 1) | 1.0 | 0.7–1.2 | Primary diversity mechanism |
| Pruning ratio | 30% | 20–50% | Preserve reasoning chain, remove verbose computation |

**Transferability notice.** These values were derived from coding and math benchmarks. Strategic decisions may saturate at lower K. Creative tasks may need different temperature. Open-ended design problems may tolerate more iterations before decay. Calibrate to your domain over repeated use.

---

## 6. Activation decision flow

```
                ┌──────────────────────┐
                │  User query arrives  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Already active in    │── Yes → Direct mode (no respawn)
                │ this turn?           │
                └──────────┬───────────┘
                           │ No
                           ▼
                ┌──────────────────────┐
                │ Matches activation   │── No  → Standard response
                │ triggers?            │
                └──────────┬───────────┘
                           │ Yes
                           ▼
                ┌──────────────────────┐
                │ Matches anti-        │── Yes → Standard response
                │ triggers?            │
                └──────────┬───────────┘
                           │ No
                           ▼
                ┌──────────────────────┐
                │ Classify fitness     │
                │ tier                 │
                └──────────┬───────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
            Tier 1       Tier 2       Tier 3
              │            │            │
              ▼            ▼            ▼
         Calibrate    Calibrate    Voice-anchor
         intensity    intensity    mode (Light)
              │            │            │
              └────────────┼────────────┘
                           ▼
                ┌──────────────────────┐
                │ Constraint check     │
                └──────────┬───────────┘
                           │
                ┌──────────┼──────────┐
                ▼                     ▼
              K ≥ 3                K < 3
                │                     │
                ▼                     ▼
          Execute pipeline    Fallback: enriched
          (Stage 1 → Stage 2  single-pass +
          → output → verify)  self-critique
```

---

## 7. Changelog

| Version | Changes |
|---------|---------|
| v1.0 | Original. Basic parallel → deliberation pipeline. |
| v2.0 | Calibration heuristic; single-model independence; confidence gradient; transferability notice; epistemic honesty grounding. |
| v3.0 (Kairo) | Fitness tiers; dual-mode deliberation (verification/synthesis/hybrid); constraint-aware execution; pre-iteration diagnostic with cascade detection; dual-model support; protocol overload + contamination cascade as named failure modes; RLVR evolution path; answer-first output; domain lens customization with vocabulary anchors; diversity-mechanism repositioning (temperature primary). |
| v3.0.1 | Restored five universal lenses; restored skill emergence. |
| **v3.1** | **State-of-art repackage.** Description rewritten with action verb + numbered triggers + scope + keywords (matcher score 2/10 → ≥9/10). Body trimmed 955→~290 lines (passes own §Protocol-Overload mitigation). Progressive disclosure: stages/failure-modes/verification/advanced split into references/. Three deterministic scripts added (`constraint_check.py`, `mode_select.py`, `pre_iteration.py`) replacing prose pseudocode for L8 (determinism over generation). Pocket Reference moved to SKILL.md body for at-execution availability. Strange-loop closed: skill now follows what it preaches. |
