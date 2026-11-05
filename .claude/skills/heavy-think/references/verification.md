# Verification — Extended Checklist

Operable. Binary-checkable. Execute before delivering final output.

## Pre-execution gates

```
□ Activation criteria matched (§Activation in SKILL.md)?
□ Anti-trigger clear (task is reasoning-heavy and outside the anti-loop window)?
□ Fitness tier correctly classified (T1/T2/T3)?
□ Calibration mode chosen (Light/Standard/Deep) per heuristic?
□ Constraint check passed (cache fits, K≥3, latency within budget)?
□ If K reduced: reason logged in one sentence?
```

## Stage 1 gates

```
□ K trajectories generated independently from scratch?
□ Temperature ≥ 0.9 used?
□ Diversity verified — meaningfully different solution paths beyond paraphrase?
□ If T2: lenses applied with vocabulary discipline?
□ If domain lenses: substitution documented?
□ Pruning ≤ 30% of original token count?
□ Cache shuffled to defeat recency bias?
□ Cache ≤ 60% of available context?
```

## Stage 2 gates

```
□ Mode correctly selected (Verification ≥75% / Synthesis <50% / Hybrid otherwise)?
□ Deliberation = analysis, not selection?
□ Tensions identified explicitly?
□ Convergences identified (independent reasoning chains)?
□ Each tension resolved via criterion (criterion named)?
□ All 6 synthesis criteria considered in priority order?
□ Critical check executed (could ALL trajectories share an error)?
□ Confidence level stated?
□ Confidence level matches evidence pattern (calibrated to actual convergence)?
```

## Output gates

```
□ Answer-first format used (default) or extended format justified?
□ Final answer clear, actionable, in domain-native format?
□ Output language matches query language?
□ Caveat present if confidence < High ("what would change this conclusion")?
□ Meta-analysis kept silent unless explicitly requested or confidence is Low?
□ Protocol narration kept out of output ("Now I'm activating heavy thinking…")?
```

## Iteration gates (only if N>1)

```
□ Pre-iteration diagnostic passed (Run python scripts/pre_iteration.py)?
□ HM-HP gap measurable (room above the ceiling exists)?
□ Previous iteration produced new resolution (fresh insight, beyond decay)?
□ Reasoning strength holding or rising (cascade-free)?
□ N stays below 3 (within the empirical return horizon)?
□ Previous deliberation framed as "previous analysis attempt" in cache?
```

## Adjudication

- **≥2 fail** → return to Stage 2 and re-deliberate before delivering.
- **1 fail** → address inline before delivering.
- **0 fail** → deliver.

## Self-test for the skill itself

```
□ SKILL.md body ≤ ~300 lines?
□ References loaded on demand (lazy-loading honored)?
□ Pocket reference present in SKILL.md?
□ Strange-loop check: skill follows its own §Protocol-Overload mitigation?
```
