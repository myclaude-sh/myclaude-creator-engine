---
name: documentation-engine
description: >-
  Multi-component documentation system: scan codebase, extract API signatures,
  generate README, architecture docs, and validate completeness. Use when asked
  to "document this", "generate docs", "write README", or "architecture doc".
argument-hint: "[scope]"
allowed-tools: [Read, Glob, Grep, Write, Bash, Agent]
---

<!-- WHY: D1 (Activation Protocol) — Load doc standards and routing before
     deciding which components to activate. -->

# Documentation Engine

> Extract, generate, and validate documentation from codebases.

## Activation Protocol

1. **Load standards:** Read `references/doc-standards.md`
2. **Load manifest:** Read `config/manifest.yaml`
3. **Load routing:** Read `config/routing.yaml`
4. **Detect scope:** Parse input for target directory
5. **Assess needs:** What docs exist? What is missing? What is stale?

---

<!-- WHY: D9 (Orchestrate Don't Execute) — SYSTEM.md only routes.
     Domain work happens in skills, agents, and workflows. -->

## Component Routing

| Request | Component | Type |
|---------|-----------|------|
| "Generate README" | quick-doc | skill |
| "Analyze architecture" | doc-analyst | agent |
| "Full documentation suite" | full-suite | workflow |
| "Check doc completeness" | doc-analyst | agent |

<!-- WHY: D5 (Question System) — Clarify what documentation is needed. -->

## Question System

| Input | Required | If Missing |
|---|---|---|
| Target codebase | Yes | Ask: "Which project should I document?" |
| Doc type | No | Default: assess and recommend |
| Output format | No | Default: Markdown |

---

## Components

### quick-doc (Skill)
Fast README generation. Reads entry points, extracts purpose, writes README.

### doc-analyst (Agent)
Deep code analysis for architecture documentation. Maps dependencies, identifies patterns.

### full-suite (Workflow)
Complete pipeline: Scan > Extract > Generate README > Generate Architecture > Validate

---

<!-- WHY: D10 (Handoff Spec) — Handoffs between components. -->

## Handoff Protocol

```
Component A > Component B:
  WHAT_DONE: {completed analysis}
  WHAT_DECIDED: {documentation structure chosen}
  WHAT_NEXT_NEEDS: {specific sections to write}
  FILES_CREATED: {list of generated docs}
```

---

<!-- WHY: D4 (Quality Gate) -->

## Quality Gate

- [ ] Generated docs reference only files that exist
- [ ] No placeholder content in output
- [ ] README has: what, install, usage, requirements
- [ ] Architecture doc has: overview, components, data flow

---

<!-- WHY: D2 (Anti-Pattern Guard) -->

## Anti-Patterns

1. **Hallucinating code** — Only document what exists. Never invent APIs.
2. **Copy-paste as docs** — Explain WHAT and WHY, not HOW (the code shows how).
3. **Stale docs** — If docs reference deleted files, flag and fix.
4. **Over-documenting** — Public API yes, private helpers no.
5. **Ignoring existing** — Read existing docs first. Enhance, not replace.

---

<!-- WHY: D14 (Graceful Degradation) -->

## Degradation

| Scenario | Behavior |
|---|---|
| No entry point found | Ask creator to identify main file |
| Monorepo | Ask which package, or doc each separately |
| Existing docs present | Compare, enhance, note differences |
