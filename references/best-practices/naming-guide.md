# Naming Guide

Naming conventions for all MyClaude marketplace products. Consistent naming
improves discoverability and communicates professionalism.

---

## Slug Format

**Rule:** Lowercase letters, hyphens only, no spaces, no special characters.

```
security-audit-skill     ✓
code-review-skill        ✓
next-js-enterprise       ✓

Security Audit Skill     ✗ (spaces)
security_audit_skill     ✗ (underscores)
SecurityAuditSkill       ✗ (PascalCase)
security-audit-v2-NEW    ✗ (uppercase)
```

**Length:** 3-40 characters. Shorter is better if unambiguous.

**Uniqueness:** Slugs must be unique within the marketplace. If your preferred slug
is taken, add a qualifier: `security-audit-nodejs` instead of `security-audit`.

---

## Display Name

**Rule:** Title Case. Clear and specific. Describes what it IS, not a brand name.

```
Security Audit Skill             ✓  (clear, specific)
Next.js Enterprise CLAUDE.md     ✓  (includes qualifier)
Structured Code Analysis         ✓  (evocative but specific)

My Amazing Skill                 ✗  (vanity, not descriptive)
The Best Code Reviewer           ✗  (superlative claim)
Assistant Helper Tool            ✗  (generic filler words)
```

**Maximum length:** 60 characters (what fits in marketplace listing card).

---

## Description

**Rule:** One sentence. Starts with a verb. States the specific benefit.

```
Analyzes security vulnerabilities in Node.js APIs using OWASP Top 10 methodology.    ✓
Transforms content briefs into publication-ready articles with editorial consistency. ✓
Enforces TypeScript strict mode, App Router patterns, and security rules for Next.js. ✓

A helpful skill for security tasks.                                                   ✗  (too vague)
This product helps you with code review, security, documentation, and more.           ✗  (unfocused)
The best security tool on the marketplace.                                             ✗  (superlative claim)
```

**Length:** 80-160 characters. First 80 characters must stand alone (truncation in listings).

**Verb choices:** Analyzes, Transforms, Enforces, Generates, Audits, Validates,
Synthesizes, Routes, Orchestrates, Reviews, Extracts, Encodes.

---

## File Naming Conventions Per Product Type

### Skills

| File | Convention | Example |
|------|-----------|---------|
| Primary | `SKILL.md` (uppercase) | `SKILL.md` |
| References | `kebab-case.md` | `domain-knowledge.md`, `reasoning-exemplars.md` |
| Agents | `agent-name.md` (kebab) | `specialist-analyst.md` |
| Tasks | `task-name.md` (kebab) | `deep-analysis.md` |

### Agents

| File | Convention | Example |
|------|-----------|---------|
| Primary | `AGENT.md` (uppercase) | `AGENT.md` |
| Identity | `identity.md` | `identity.md` |
| Architecture | `architecture.md` | `architecture.md` |
| Examples | `example-N.md` | `example-1.md`, `example-2.md` |

### Squads

| File | Convention | Example |
|------|-----------|---------|
| Primary | `SQUAD.md` (uppercase) | `SQUAD.md` |
| Agents | `agent-name.md` in `agents/` | `agents/content-strategist.md` |
| Config | `routing-table.md`, `handoff-protocol.md`, `capability-index.yaml` | (exact names required) |
| Workflows | `workflow-name.md` in `workflows/` | `workflows/full-production.md` |

### Workflows

| File | Convention | Example |
|------|-----------|---------|
| Primary | `WORKFLOW.md` (uppercase) | `WORKFLOW.md` |
| Steps | `NN-step-name.md` (zero-padded, kebab) | `01-context-load.md`, `02-analysis.md` |
| Config | `variables.yaml` | `config/variables.yaml` |

### Design Systems

| File | Convention | Example |
|------|-----------|---------|
| Primary | `DESIGN-SYSTEM.md` (uppercase) | `DESIGN-SYSTEM.md` |
| Tokens | `category.yaml` | `colors.yaml`, `typography.yaml`, `spacing.yaml` |
| Components | `component-name.md` | `button.md`, `card.md` |
| Exports | format-specific names | `tailwind.config.js`, `css-variables.css`, `dtcg.json` |

### Prompts

| File | Convention | Example |
|------|-----------|---------|
| Primary | `PROMPT.md` (uppercase) | `PROMPT.md` |
| Variants | `variant-name.md` | `concise.md`, `detailed.md`, `expert.md` |
| Examples | `example-N.md` | `example-1.md`, `example-2.md` |

### CLAUDE.md

| File | Convention | Example |
|------|-----------|---------|
| Primary | `CLAUDE.md` (uppercase) | `CLAUDE.md` |
| Rules | `rule-name.md` | `rules/typescript.md`, `rules/naming.md` |
| Docs | `document-name.md` | `docs/architecture.md` |

### Applications

| File | Convention | Example |
|------|-----------|---------|
| Primary | `README.md` (uppercase) | `README.md` |
| Source | Follow language convention | `src/` (Node), `main.py` (Python) |
| Config | Follow tool convention | `package.json`, `pyproject.toml` |
| Project config | `CLAUDE.md` | `CLAUDE.md` |

### Systems

| File | Convention | Example |
|------|-----------|---------|
| Primary | `SYSTEM.md` (uppercase) | `SYSTEM.md` |
| Distribution manifest | `vault.yaml` | `.publish/vault.yaml` |
| System config | `manifest.yaml` | `config/manifest.yaml` |
| Routing | `routing.yaml` | `config/routing.yaml` |

---

## Version Naming

See `references/best-practices/versioning-guide.md` for full versioning rules.

**Summary:**
- Version: `MAJOR.MINOR.PATCH` (semver)
- No `v` prefix in version field: `1.0.0` not `v1.0.0`
- Pre-release: `1.0.0-beta.1`, `1.0.0-rc.1`

---

## Common Naming Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Version in product name | `security-audit-v2` | Use version field; slug stays `security-audit` |
| Type in product name | `my-amazing-skill` | Type is already declared by category |
| Superlatives | `best-code-reviewer` | Describe what it does, not how good it is |
| Author name in name | `johns-security-tool` | Author is shown separately as `@john` |
| Abbreviations | `sec-aud-ts-njs` | Spell it out: `security-audit-typescript-nextjs` |
