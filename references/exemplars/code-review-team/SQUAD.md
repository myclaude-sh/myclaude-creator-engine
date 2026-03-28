---
name: code-review-team
description: >-
  Multi-agent code review squad with 3 specialists: security, architecture, and
  performance. Produces unified review with severity ratings. Use when asked to
  "review code", "PR review", "code review", or "check this before merging".
argument-hint: "[file-or-directory]"
allowed-tools: [Read, Glob, Grep, Agent]
---

<!-- WHY: D1 (Activation Protocol) — Load review standards and routing before
     dispatching to agents. Without shared standards, each agent uses different criteria. -->

# Code Review Team

> Three-perspective code review: security + architecture + performance.

## Activation Protocol

1. **Load standards:** Read `references/review-standards.md`
2. **Load routing:** Read `config/routing-table.md`
3. **Identify scope:** Parse input for files/directories to review
4. **Pre-check:** Verify files exist and are source code (not binary/generated)

---

<!-- WHY: D9 (Orchestrate Don't Execute) — SQUAD.md ONLY routes. It never
     analyzes code itself. All domain work happens in specialist agents. -->

## Routing Table

| Input Pattern | Route To | Why |
|---|---|---|
| Security-related files (auth, crypto, env) | Security Reviewer first | Highest blast radius |
| Architecture files (config, routing, schemas) | Architecture Reviewer first | Structural decisions |
| Performance-sensitive (loops, queries, renders) | Performance Reviewer first | User-facing impact |
| General code changes | All three in parallel | Comprehensive review |
| Single file < 100 lines | Security + Architecture only | Performance review unnecessary |

Default: route to all three agents in parallel, synthesize results.

---

<!-- WHY: D5 (Question System) — Clarify scope before expensive multi-agent review. -->

## Question System

| Input | Required | If Missing |
|---|---|---|
| Files to review | Yes | Ask: "Which files or directory should I review?" |
| Review focus | No | Default: all three perspectives |
| Severity threshold | No | Default: report all findings |

---

## Core Instructions

<!-- WHY: D10 (Handoff Spec) — Each agent handoff includes what_done, what_decided, what_next_needs. -->

### Step 1: Dispatch to Agents

Route to agents based on routing table. Each agent receives:
```
HANDOFF: Orchestrator → {Agent}
WHAT_DONE: Scope identified, standards loaded
WHAT_DECIDED: Review scope is {files}. Focus: {all|security|arch|perf}
WHAT_NEXT_NEEDS: Analyze these files against your domain criteria
FILES_TO_REVIEW: {list}
```

### Step 2: Collect Results

Wait for all dispatched agents to complete. Each returns:
```
HANDOFF: {Agent} → Orchestrator
WHAT_DONE: {N} files reviewed, {M} findings
WHAT_DECIDED: {severity breakdown}
WHAT_NEXT_NEEDS: Synthesis with other perspectives
FINDINGS: [{file, line, severity, description, suggestion}]
```

### Step 3: Synthesize

<!-- WHY: D11 (Socratic Pressure) — Challenge findings before presenting.
     If two agents disagree, surface the tension instead of smoothing it. -->

- Merge findings, deduplicate overlaps
- If agents disagree (e.g., Security says "remove" but Architecture says "keep"): surface BOTH views
- Order by severity: critical → high → medium → low
- Add cross-perspective insights (e.g., "This security fix also resolves the performance concern")

### Step 4: Present

```
CODE REVIEW — {scope}
Reviewers: Security + Architecture + Performance

CRITICAL ({N}):
  {file}:{line} [{perspective}] — {description}
    Suggestion: {fix}

HIGH ({N}):
  ...

MEDIUM ({N}):
  ...

Summary: {total} findings ({critical}C / {high}H / {medium}M / {low}L)
Recommendation: {APPROVE | REQUEST_CHANGES | BLOCK}
```

---

<!-- WHY: D4 (Quality Gate) — Review quality criteria. -->

## Quality Gate

- [ ] All dispatched agents returned results
- [ ] Every finding has: file, line, severity, description, suggestion
- [ ] No duplicate findings across agents
- [ ] Recommendation is justified by findings

---

<!-- WHY: D6 (Confidence Signaling) — Signal certainty of findings. -->

## Confidence Levels

| Level | Meaning | When to Use |
|---|---|---|
| Certain | Pattern is objectively wrong | SQL injection, hardcoded secret |
| Likely | Pattern is probably wrong | Unused import, missing error handling |
| Suggestion | Pattern could be improved | Naming, structure, style |

---

<!-- WHY: D2 (Anti-Pattern Guard) — Common review mistakes. -->

## Anti-Patterns

1. **Style policing** — Don't flag formatting. That's a linter's job.
2. **Bikeshedding** — Don't debate naming unless it causes confusion.
3. **Drive-by nitpicking** — Every finding must have a concrete suggestion.
4. **Ignoring context** — A prototype has different standards than production.
5. **Piling on** — If a file has 10+ issues, summarize patterns instead of listing each.
6. **Missing the forest** — Don't get lost in details. Flag architectural concerns first.

---

<!-- WHY: D14 (Graceful Degradation) — Handle edge cases. -->

## Degradation

| Scenario | Behavior |
|---|---|
| Binary files in scope | Skip, note "N binary files excluded" |
| Generated code | Skip if detectable (*.generated.*, dist/), otherwise review |
| Too many files (>100) | Ask to narrow scope or run in batch mode |
| Agent timeout | Report partial results from completed agents |

---

<!-- WHY: D8 (State Persistence) — Track review decisions. -->

## State

Reviews are stateless — each invocation is independent.
However, if the creator runs multiple reviews on the same files,
note "Previous review found {N} issues. {M} appear to be fixed."
