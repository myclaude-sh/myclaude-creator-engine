---
document: structural-dna
product: MyClaude Studio Engine
version: 2.0.0
status: CANONICAL
date: 2026-03-28
---

# Structural DNA — 18 Patterns for State-of-the-Art Claude Code Products

> Every DNA pattern is a lesson extracted from production systems. Each one represents
> a failure mode that has caused real products to underperform or be abandoned.
> Apply them and your products inherit structure that took years to discover.

---

## Meta-Architecture

Every state-of-the-art Claude Code product follows a six-layer processing flow.
The 18 DNA patterns distribute across these layers:

```
BOOT LAYER
  Load context, routing rules, core config
  DNA: D1 (Activation Protocol), D3 (Progressive Disclosure)
    |
INPUT TRIAGE
  Classify request, identify specialists, check preconditions
  DNA: D5 (Question System), D7 (Pre-Execution Gate)
    |
EXECUTION
  Route to specialist, apply pressure, execute with disclosure
  DNA: D9 (Orchestrate Don't Execute), D10 (Handoff Spec),
       D11 (Socratic Pressure), D18 (Subagent Isolation)
    |
STATE CAPTURE
  Log decisions, update state, check quality signals
  DNA: D8 (State Persistence), D12 (Compound Memory)
    |
SYNTHESIS
  Integrate outputs, surface tensions, apply final validation
  DNA: D4 (Quality Gate), D6 (Confidence Signaling)
    |
OUTPUT
  Graduate confidence, show reasoning, declare uncertainty
  DNA: D13 (Self-Documentation), D14 (Graceful Degradation)
```

### How Tiers Compose

Tiers are cumulative. Tier 2 requires Tier 1 as foundation. Tier 3 requires Tier 2.
A product at MCS-2 must pass all Tier 1 AND Tier 2 checks. A product at MCS-3 must
pass all 18. The tiers reflect structural complexity:

- **Tier 1** patterns apply to everything. A single-file prompt needs D1, D4, D13.
- **Tier 2** patterns require that the product has nontrivial execution logic.
  A prompt with no branching doesn't need D8 (state) — it's not applicable.
- **Tier 3** patterns apply to multi-agent systems. A solo skill has no agents to
  orchestrate, no handoffs to specify, no subagents to isolate.

The DNA Applicability Matrix in the PRD defines R (required) / o (optional) / — (not applicable)
per product type. The /validate skill reads this matrix to determine which patterns to check.

---

## TIER 1 — UNIVERSAL
*6 patterns. Required for every product at every MCS level.*

---

### D1: Activation Protocol

**Tier:** 1 — Universal

**Problem it solves:**
A product that responds without loading context produces generic output. Without an explicit
activation sequence, Claude uses whatever is ambient in the session — which may be wrong,
incomplete, or from a different project entirely.

**Rule:**
Every product must define an explicit activation sequence that loads domain knowledge,
anti-patterns, and user intent BEFORE taking action. The sequence must be ordered:
knowledge first, constraints second, intent third.

**Example structure:**
```markdown
## Activation Protocol

Before responding to any invocation:
1. Read `references/domain-knowledge.md`
2. Read `references/anti-patterns.md`
3. Parse input for specific request type
4. Apply domain context to interpretation
```

**Validation check:**
```
grep -i "activation protocol\|## activation\|before responding\|load.*context\|context.*load" {PRIMARY_FILE}
AND
grep -c "references/" {PRIMARY_FILE} → must be ≥1
```
PASS if both match. PARTIAL if activation section found but no references/ link.

---

### D2: Anti-Pattern Guard

**Tier:** 1 — Universal

**Problem it solves:**
Without documenting what NOT to do, users and the product itself repeat known errors.
Anti-patterns are accumulated failure knowledge — without them, every session risks the
same mistakes that were already discovered and solved.

**Rule:**
Every product must contain a section listing at least 5 anti-patterns with description
and prevention. Anti-patterns are failure modes specific to this product's domain —
not generic "don't break things" advice.

**Example structure:**
```markdown
## Anti-Patterns

| Pattern | Why It Fails | Prevention |
|---------|-------------|------------|
| Reviewing code without reading tests | Misses intended behavior | Always read tests/ before reviewing src/ |
```

**Validation check:**
```
grep -i "anti-pattern\|## anti-pattern\|## what not\|## never\|## avoid" {PRIMARY_FILE}
AND count items in section → must be ≥5
```
PASS if section found with ≥5 items. PARTIAL if section found but <5 items.

---

### D3: Progressive Disclosure

**Tier:** 1 — Universal

**Problem it solves:**
Loading all knowledge into the primary file wastes context window on every invocation.
A product whose SKILL.md is 2000 lines burns context before the creator even types a request.

**Rule:**
Primary file must be under 500 lines. Deep knowledge lives in references/. Primary file
contains structure and protocols; references/ contains domain content loaded on-demand.
Product type determines required depth: skills can be tighter, systems need more.

**Validation check:**
```
wc -l {PRIMARY_FILE} → must be <500
AND
glob: references/ → must exist with ≥1 file
AND
grep "inline knowledge dump\|CONTEXT:\|BACKGROUND:" {PRIMARY_FILE} → must be 0 matches
```
PASS if primary file <500 lines and references/ exists. PARTIAL if references/ exists but
primary file >500 lines.

---

### D4: Quality Gate

**Tier:** 1 — Universal

**Problem it solves:**
Without explicit checkpoints, output quality varies based on ambient session state.
Quality gates force verification before delivery — they make implicit standards explicit.

**Rule:**
Every product must define at least 3 verifiable quality criteria that can be checked
before output is delivered. Criteria must be checkable, not aspirational.
"Output must be clear" is aspirational. "Output contains exactly 3 sections" is checkable.

**Example structure:**
```markdown
## Quality Gate

Before delivering output, verify:
- [ ] All referenced files exist
- [ ] No placeholder content (TODO, lorem ipsum)
- [ ] Output matches requested format
- [ ] If skill: activation protocol was followed
```

**Validation check:**
```
grep -i "quality gate\|## quality\|before deliver\|before output\|output criteria\|acceptance" {PRIMARY_FILE}
AND count verifiable items (grep "- \[" or "1\. " in quality section) → must be ≥3
```
PASS if section with ≥3 checkable items. PARTIAL if section found but <3 items.

---

### D13: Self-Documentation

**Tier:** 1 — Universal
*(ID gap is intentional — D13 belongs in Tier 1 per the PRD applicability matrix.)*

**Problem it solves:**
A product without a README isn't installed. Buyers need install instructions, usage
examples, and requirements. A product that assumes context will underperform for
every new user.

**Rule:**
Every product must have README.md with four non-empty sections: what it does, how to
install, how to use, and requirements. Install section must include the
`myclaude install {slug}` command. Usage section must include at least one example.

**Validation check:**
```
glob: README.md → must exist
AND
grep -i "## what\|## overview\|## description" README.md → must match
AND
grep -i "## install\|## setup\|## getting started" README.md → must match
AND
grep -i "## usage\|## how to use\|## commands" README.md → must match
AND
grep -i "## requirements\|## prerequisites\|## requires" README.md → must match
```
PASS if all 4 sections found and non-empty. PARTIAL if README exists but missing sections.

---

### D14: Graceful Degradation

**Tier:** 1 — Universal

**Problem it solves:**
A product that fails silently or crashes on missing context destroys creator trust.
Buyers don't know what went wrong; they just see a non-working product and uninstall it.

**Rule:**
Every product must document how it behaves when context is incomplete, input is
ambiguous, or dependencies are unavailable. The product must degrade gracefully:
produce partial output with explanation, or ask for clarification — never fail silently.

**Example structure:**
```markdown
## When Not To Use

- If {required_context} is unavailable: explain what's needed, suggest alternatives
- If input is ambiguous: ask one clarifying question, not five
- If dependencies not installed: report exactly what's missing and how to install
```

**Validation check:**
```
grep -i "when not to use\|degradation\|## limitations\|## error handling\|## if.*missing\|## fallback" {PRIMARY_FILE}
```
PASS if section found with at least 2 handled cases. PARTIAL if section found but only 1 case.

---

## TIER 2 — ADVANCED
*7 patterns. Required for MCS-2. Products with nontrivial execution logic.*

---

### D5: Question System

**Tier:** 2 — Advanced

**Problem it solves:**
A product that assumes input produces misaligned output. When input is ambiguous,
guessing is worse than asking — it produces confident wrong output that takes longer
to correct than if the product had simply asked.

**Rule:**
Every product with variable input must define a question system: what to ask, when to
ask it, and what to do with the answer. Questions must be minimal (one at a time),
specific (not "tell me more"), and actionable (the answer must change behavior).

**Validation check:**
```
grep -i "question\|if missing.*ask\|ask.*if\|clarif\|\$ARGUMENTS\|\$0" {PRIMARY_FILE}
AND presence of argument handling table or "if not provided" pattern
```
PASS if question/argument handling found. PARTIAL if $ARGUMENTS used but no handling logic.

---

### D6: Confidence Signaling

**Tier:** 2 — Advanced

**Problem it solves:**
Claims stated without certainty markers are indistinguishable from facts. A product
that says "This code has a race condition" with the same confidence as "I'm 40% sure
this code has a race condition" misleads users and erodes trust when it's wrong.

**Rule:**
Every product that makes claims or recommendations must use graduated confidence signals.
Use explicit markers: (high confidence), (moderate confidence), (low confidence),
or quantitative ranges. Never present uncertain output as certain.

**Validation check:**
```
grep -i "confidence\|high confidence\|moderate confidence\|low confidence\|certainty\|likely\|may be\|possible" {PRIMARY_FILE}
```
PASS if confidence signaling pattern found with at least 2 levels. PARTIAL if only one level.

---

### D7: Pre-Execution Gate

**Tier:** 2 — Advanced

**Problem it solves:**
Acting without precondition checks causes silent failures deep in execution.
A product that starts work before verifying that required files exist, auth is valid,
or dependencies are present will fail in unpredictable ways that are hard to debug.

**Rule:**
Every product with external dependencies or required context must define and run
pre-execution checks BEFORE starting work. Checks must be explicit (not assumed),
automated where possible, and must produce clear failure messages with remediation steps.

**Validation check:**
```
grep -i "precondition\|pre-execution\|before executing\|verify.*before\|check.*exists\|requires.*present" {PRIMARY_FILE}
```
PASS if pre-execution check pattern found. PARTIAL if checks described but not gated.

---

### D8: State Persistence

**Tier:** 2 — Advanced

**Problem it solves:**
Without state, every session starts from zero. Patterns discovered, decisions made,
and preferences learned disappear when the session closes. State persistence is what
distinguishes a product from a one-shot prompt.

**Rule:**
Any product that learns, tracks, or builds across sessions must define a state file
(YAML or JSON) with explicit schema. State must be append-safe (reading never breaks
if state is partial) and the schema must be documented in the product.

**Validation check:**
```
glob: *.yaml OR *.json in product directory (excluding vault.yaml, plugin.json)
AND grep "state\|session\|persist\|memory\|track" in that file or PRIMARY file
```
PASS if state file exists with documented schema. PARTIAL if state section documented but no file.

---

### D15: Testability

**Tier:** 2 — Advanced

**Problem it solves:**
A product that can't be tested can't be improved. Without test scenarios, creators
ship products they can't verify and buyers can't trust. Testability is not optional
for products that execute nontrivial logic.

**Rule:**
Every product with execution logic must include test scenarios with expected outputs.
Minimum 3 scenarios: happy path, edge case, adversarial input. Expected output must
be specific enough to verify (not "output should be good").

**Validation check:**
```
grep -i "## test\|## example\|## scenario\|expected output\|sample input\|test case" {PRIMARY_FILE_OR_README}
AND count examples → must be ≥3
```
PASS if 3+ scenarios with expected outputs. PARTIAL if examples exist but <3 or without expected output.

---

### D16: Composability

**Tier:** 2 — Advanced

**Problem it solves:**
A product that conflicts with other products gets uninstalled. Hardcoded absolute paths,
common command names that clash, and global state mutations make products incompatible
with real-world Claude Code environments where many products coexist.

**Rule:**
All file references must be relative. Command names must be specific to the product
domain (not /help, /status, /run, /start, /stop). No modifications to global config
or shared state. Product must be installable alongside any other MyClaude product.

**Validation check:**
```
grep -n "absolute path\|^/[a-z]" {ALL_FILES} → must be 0 matches
AND grep -n "^command: /help\|^command: /status\|^command: /run\b" SKILL.md → must be 0
AND grep -n "globalconfig\|global state\|~/" {ALL_FILES} → must be 0 matches
```
PASS if zero violations. PARTIAL if references are relative but command name conflicts.

---

### D17: Hook Integration

**Tier:** 2 — Advanced

**Problem it solves:**
Manual steps that could be automated become bottlenecks and are frequently skipped.
Hooks (PostToolUse, FileChanged, SessionStart, Stop) allow products to automate
workflow integration without requiring the user to remember to trigger them.

**Rule:**
Any product that benefits from lifecycle automation must document which Claude Code hooks
it uses (or could use), what they trigger, and how to configure them. Hook documentation
belongs in README or a dedicated hooks section in the primary file.

**Validation check:**
```
grep -i "hook\|sessionstart\|posttooluse\|filechanged\|stop\|automation" {PRIMARY_FILE_OR_README}
```
PASS if hooks section documented with at least 1 hook. PARTIAL if hooks mentioned but not documented.

---

## TIER 3 — EXPERT
*5 patterns. Required for MCS-3. Multi-agent systems only.*

---

### D9: Orchestrate, Don't Execute

**Tier:** 3 — Expert

**Problem it solves:**
An orchestrator that does specialist work produces mediocre output across all domains.
When the squad leader also does the code review AND the security audit AND the
documentation check, none of them get specialist-quality attention.

**Rule:**
Orchestrators route and coordinate. They do NOT contain domain instructions. A squad
orchestrator's SQUAD.md must contain a routing table with specialist assignments —
not the actual logic for how to do any of the specialties. Domain expertise lives
in the specialist agents.

**Validation check:**
```
For squad/system types:
grep "routing table\|route to\|delegate to\|assign to\|orchestrat" SQUAD.md OR SYSTEM.md → must match
AND grep -i "domain instruction\|specifically.*you should check\|step.*by.*step.*how to" SQUAD.md → must be 0
```
PASS if routing table found and no domain instructions in orchestrator. PARTIAL if orchestrator has both
routing AND some domain instructions.

---

### D10: Handoff Specification

**Tier:** 3 — Expert

**Problem it solves:**
Vague context at agent handoffs causes cascade degradation — each agent compounds the
ambiguity of the previous one, producing output that drifts progressively further from
the original intent.

**Rule:**
Every agent-to-agent handoff must specify exactly: what was done, what was decided
(including rejected alternatives), and what the next agent specifically needs.
The handoff template must be embedded in the product and used consistently.

**Example:**
```
HANDOFF: {source} → {target}
WHAT_DONE: {completed work summary}
WHAT_DECIDED: {decisions made + alternatives rejected}
WHAT_NEXT_NEEDS: {specific context for target}
FILES_MODIFIED: {list}
```

**Validation check:**
```
grep -i "handoff\|what_done\|what_decided\|what_next\|files_modified" {AGENT_FILES}
AND all agent files have handoff section
```
PASS if handoff template found in all agent files. PARTIAL if found in some but not all.

---

### D11: Socratic Pressure

**Tier:** 3 — Expert

**Problem it solves:**
Agents that accept their first output produce consistent but not improving quality.
Socratic pressure — challenging the output before delivering it — catches errors,
weak reasoning, and incomplete analysis that would otherwise reach the user.

**Rule:**
Agents that produce analysis or recommendations must include a self-challenge step:
"What is wrong with this output?" or "What would a critic say?" before finalizing.
The challenge must be genuine (not rhetorical) — it must be capable of changing the output.

**Validation check:**
```
grep -i "socratic\|challenge.*output\|what.*wrong\|critic\|falsif\|counter.*argument\|self.*challenge" {AGENT_FILES}
```
PASS if self-challenge pattern in ≥1 agent. PARTIAL if language suggests challenge but not structured.

---

### D12: Compound Memory

**Tier:** 3 — Expert

**Problem it solves:**
Without cross-session memory, agents start fresh every session. Patterns discovered,
anti-patterns encountered, and architectural decisions made disappear. Compound memory
is what allows a system to improve over time rather than plateau.

**Rule:**
Multi-agent systems must define memory configuration using Claude's native memory scopes
(user, project, local). Project memory persists patterns per-project. User memory
persists creator preferences across projects. At least one memory scope must be
configured in agent frontmatter.

**Validation check:**
```
grep -i "memory:\|user memory\|project memory\|local memory" {AGENT_FRONTMATTER}
AND at least one agent has memory: project or memory: user
```
PASS if ≥1 agent has memory configuration. PARTIAL if memory section present but scope unspecified.

---

### D18: Subagent Isolation

**Tier:** 3 — Expert

**Problem it solves:**
Agents without context isolation bleed session state into each other. When one agent's
conversation history is visible to another, it introduces bias, context pollution,
and makes the second agent's output dependent on the first's phrasing choices rather
than the actual task.

**Rule:**
Every subagent in a squad or system must run in isolated context (context: fork in
skill frontmatter OR defined as a separate subagent with own context window). Agents
must communicate through explicit handoffs, not shared session state.

**Validation check:**
```
grep "context: fork\|context:fork" {AGENT_SKILL_FILES} → must match ≥1
AND each agent is defined as separate subagent (own SKILL.md or AGENT.md)
```
PASS if context:fork present in all multi-agent definitions. PARTIAL if present in some agents but not all.

---

## Reference: DNA Applicability Matrix

| Pattern | skill | agent | squad | workflow | ds | prompt | claude-md | app | system |
|---------|-------|-------|-------|----------|----|--------|-----------|-----|--------|
| D1  | R | R | R | R | o | R | R | o | R |
| D2  | R | R | R | R | R | o | R | R | R |
| D3  | R | R | R | o | o | o | R | o | R |
| D4  | R | R | R | R | R | R | o | R | R |
| D5  | R | R | R | o | — | o | — | o | R |
| D6  | o | R | R | o | — | o | — | o | R |
| D7  | R | R | R | R | — | o | o | R | R |
| D8  | o | R | R | o | — | — | — | o | R |
| D9  | — | — | R | — | — | — | — | — | R |
| D10 | — | — | R | o | — | — | — | — | R |
| D11 | o | R | R | — | — | — | — | — | R |
| D12 | — | o | R | — | — | — | — | — | R |
| D13 | R | R | R | R | R | R | R | R | R |
| D14 | R | R | R | R | o | o | o | R | R |
| D15 | o | R | R | o | — | o | — | o | R |
| D16 | R | R | R | R | R | R | R | R | R |
| D17 | o | o | o | o | — | — | o | o | o |
| D18 | — | — | R | — | — | — | — | — | R |

`R` = Required for MCS of that tier | `o` = Optional bonus | `—` = Not applicable

---

*structural-dna.md v2.0.0 — MyClaude Studio Engine*
