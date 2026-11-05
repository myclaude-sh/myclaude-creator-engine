# Failure Modes

Six named failure modes. Each: symptom · cause · mitigation.

## Table of Contents
1. Trajectory Collapse
2. Deliberation Becomes Selection
3. Operability Vacuum
4. Confidence Misalignment
5. Protocol Overload
6. Contamination Cascade

---

## 1. Trajectory Collapse

**Symptom.** K trajectories are substantively identical — same approach, same intermediate steps, same conclusion. Could be merged without loss.

**Cause.** Temperature too low; problem has a single obvious approach; or model training creates a strong attractor toward one solution path.

**Mitigation.**
- Verify diversity by checking whether trajectories took meaningfully different paths, not just different wording of the same path.
- If collapse detected, inject explicit strategy hints ("try approaching geometrically" vs "try brute force enumeration").
- If persistent: reduce K and fall back to single-pass + structured self-critique. Collapsed trajectories add cost without value.

---

## 2. Deliberation Becomes Selection

**Symptom.** Output reads as "Trajectory #3 has the best answer" without genuine comparative analysis or synthesis.

**Cause.** Deliberation prompt too weak; model defaults to picking rather than analyzing; or model lacks sufficient synthesis capability.

**Mitigation.**
- The Stage 2 template (`references/stages.md` §2.2) explicitly requires step-by-step evaluation before conclusion.
- If model consistently selects without analyzing, reinforce: "You MUST evaluate the reasoning chain of each trajectory before selecting or synthesizing."
- If model fundamentally cannot synthesize, accept verification mode as the ceiling. Verification (checking the best answer's reasoning) is still valuable.

---

## 3. Operability Vacuum

**Symptom.** Rich analytical output but the user does not know what the actual answer is or what to do with it.

**Cause.** Deliberation prioritized meta-analysis over conclusion.

**Mitigation.**
- Default output is **answer-first** (SKILL.md §Output structure). Meta-analysis only on user request, Low confidence, or multiple defensible answers.
- Verification checklist confirms "final answer is clear and actionable."
- If operability fails, add a final pass that translates analysis into concrete answer + next steps.

---

## 4. Confidence Misalignment

**Symptom.** High-authority language on weak evidence, or excessive hedging on strong convergence.

**Cause.** Confidence gradient not applied, or applied inconsistently with the actual evidence pattern.

**Mitigation.**
- SKILL.md §Confidence-gradient mandates explicit level in output.
- During verification, cross-check: does stated confidence match number of convergences, resolution quality, evidence basis?
- If misaligned, adjust the label before delivery.

---

## 5. Protocol Overload

**Symptom.** The protocol's operational complexity exceeds the executor's capacity to follow it faithfully. Sections get skipped, steps get merged, quality degrades not from bad reasoning but from too many simultaneous instructions.

**Cause.** Heavy thinking is comprehensive by design — covers edge cases, failure modes, advanced configurations. A single-context LLM holding all of it while reasoning about the problem creates cognitive budget competition.

**Mitigation.**
- **References (this folder) are the spec.** They exist for understanding the protocol's design, rationale, edge cases.
- **The Pocket Reference in SKILL.md is for execution.** When executing, work from the pocket reference; load full references only when needed.
- **Prioritize the core loop:** generate K trajectories → classify mode → deliberate → output answer. The rest is refinement.
- This skill is structured precisely to defeat this failure mode — SKILL.md body deliberately stays slim and offloads detail to references.

---

## 6. Contamination Cascade

**Symptom.** Iterative deliberation amplifies errors from earlier rounds instead of correcting them. Each iteration produces weaker reasoning despite reaching the same or similar conclusion.

**Cause.** Previous deliberation output carries biases (anchoring, confirmation) that contaminate subsequent synthesis. The deliberation model treats its own prior output as authoritative rather than as one more trajectory to evaluate.

**Mitigation.**
- Pre-iteration diagnostic (`references/advanced.md` §Iteration-mechanics, Check 3) catches this by monitoring **reasoning quality**, not just answer stability.
- Use `Run python scripts/pre_iteration.py` with reasoning-strength scores to detect quantitatively.
- When appending previous deliberation as "Expert Trajectory," explicitly frame it in the cache as **"a previous analysis attempt"** — not as "the current best answer." Language matters for how the model treats it.
- If cascading detected, **stop iteration**. The v1 deliberation output is almost certainly better than the degraded vN output.
