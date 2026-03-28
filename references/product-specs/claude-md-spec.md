# Product Spec: CLAUDE.md Configurations

## Definition

CLAUDE.md configurations are project configuration files that define rules, conventions,
and architecture for Claude Code projects. They are installed at the project root or
in `.claude/` and are read by Claude Code at session start, establishing the persistent
operating context for all interactions in that project.

A CLAUDE.md config is NOT:
- A skill (skills are invoked; CLAUDE.md is always-on)
- A prompt (prompts are task-specific; CLAUDE.md is project-persistent)
- Documentation for humans (CLAUDE.md is primarily machine-read by Claude Code)

A CLAUDE.md IS:
- A persistent operating system for a specific project type
- A set of enforceable rules and conventions Claude Code follows
- An architecture decision record that Claude Code reads before every response

---

## Canonical File Structure

```
claude-md-name/
├── CLAUDE.md              # The configuration file (REQUIRED)
├── README.md              # Human-readable setup instructions (REQUIRED)
├── rules/                 # Enforcement rules (modular breakout)
│   ├── rule-1.md
│   └── rule-2.md
├── docs/
│   └── architecture.md    # Architecture decisions explained
└── CHANGELOG.md           # Version history
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `CLAUDE.md` | The actual configuration | MCS-1 |
| `README.md` | Setup instructions, what it configures, use case | MCS-1 |

---

## Required Sections in CLAUDE.md

### 1. Header and Identity

```markdown
# Project Name — Claude Code Configuration

> One sentence: what kind of project this config is for.

**Version:** 1.0.0
**Target Stack:** [Next.js 15 + TypeScript | Python FastAPI | etc.]
**Team Size:** [Solo | Small Team | Enterprise]
```

### 2. First Action / Boot Sequence

What Claude Code should read and do at session start:
- Which files to read (architecture, schema, conventions)
- What state to check (current branch, recent changes, open TODOs)
- What context to establish before answering any question

```markdown
## First Action

At the start of every session:
1. Read `docs/architecture.md` — understand current system design
2. Run `git status` — know what's in progress
3. Check `TODO.md` if it exists — know open work items
4. Read any files mentioned in the current user prompt
```

### 3. Architecture Overview

A summary of the project's key architectural decisions:
- Tech stack
- Directory structure and what lives where
- Key patterns used (and why)
- What NOT to change without discussion

### 4. Coding Conventions

Specific, enforceable rules:
- Naming conventions (files, functions, variables, components)
- Import order
- Code organization rules
- TypeScript/type system rules (if applicable)
- Testing conventions

### 5. Security Rules

What Claude Code must never do in this project:
- No hardcoded secrets, API keys, or credentials
- No `eval()` or equivalent
- No network calls to unknown hosts
- No writing to sensitive paths
- Authentication patterns to follow

### 6. Workflow Rules

How to work in this project:
- Branching strategy
- Commit message format
- PR/review requirements
- How to handle breaking changes
- Deployment checklist

---

## MCS Requirements

### MCS-1: Publishable

**Universal:**
- [ ] Valid CLAUDE.md with all required sections
- [ ] README.md with: what this config is for, how to install, what it changes
- [ ] Metadata complete
- [ ] No syntax errors
- [ ] License from approved list
- [ ] No hardcoded project-specific values (should be generic enough to reuse)

**CLAUDE.md-Specific:**
- [ ] Boot sequence defined (at least 2 steps)
- [ ] At least 3 specific coding conventions documented
- [ ] At least 1 security rule documented
- [ ] Target stack/project type clearly specified

### MCS-2: Quality

**Universal (beyond MCS-1):**
- [ ] `rules/` directory with modular rule files
- [ ] `docs/architecture.md` with architecture decisions explained
- [ ] Tested with a real project (not just hypothetical)
- [ ] Anti-patterns section
- [ ] 3+ example scenarios showing rules in action
- [ ] No placeholder content
- [ ] Semver versioning

**CLAUDE.md-Specific:**
- [ ] Rules broken into modular files in `rules/` (not one monolithic file)
- [ ] Architecture decisions explain WHY (not just what)
- [ ] Config tested in real Claude Code project for at least 5 sessions
- [ ] Workflow rules cover the most common operations for the target stack

### MCS-3: State-of-the-Art

**Universal (beyond MCS-2):**
- [ ] Hook configurations (pre-commit, post-commit, etc.)
- [ ] MCP server integration documented
- [ ] Comprehensive security rules
- [ ] Deep stack-specific knowledge encoded
- [ ] Composable (rules can be adopted piecemeal)
- [ ] CHANGELOG with versioning
- [ ] Differentiation statement

**CLAUDE.md-Specific:**
- [ ] Hook configs for at least pre-commit quality gates
- [ ] MCP integration patterns documented for common servers
- [ ] Permission model documented (what Claude Code can vs. cannot do in this project)
- [ ] Tested across team members with different coding styles

---

## Anti-Patterns for CLAUDE.md Configurations

### Structural
- **Project-specific values hardcoded:** `CLAUDE.md` contains `DB_HOST=prod.mycompany.com` or specific file paths from the creator's machine. CLAUDE.md products must be reusable.
- **Rules without justification:** `Always use 2-space indentation.` — no explanation of why. Rules without rationale get ignored or overridden.
- **Monolithic single file:** All 500 lines of rules in one CLAUDE.md. At MCS-2+, break into modular rule files.

### Content
- **Generic rules that apply to all projects:** "Write clean code" and "use meaningful variable names" are not project-specific rules. They add noise without signal.
- **Conflicting rules:** Rule A says "always use `const`" and Rule B says "use `let` for loop variables" — without a precedence rule, Claude Code will be inconsistent.
- **Missing boot sequence:** CLAUDE.md with no first-action protocol. Claude Code loads context randomly instead of systematically.

### Quality
- **Not tested in a real project:** Rules that sound good but break down in practice. A CLAUDE.md must be tested with real Claude Code sessions.
- **No error in rules:** Every rule is a positive instruction but no rules document what to do when a rule is violated.

---

## Discovery Questions (from §7)

When creating a CLAUDE.md, answer these before scaffolding:

1. What type of project is this for? (Next.js app, Python API, monorepo, data pipeline, etc.)
2. What are the key architectural decisions that Claude Code must respect?
3. What security rules apply? (what must Claude Code never do in this project)
4. What coding conventions should be enforced? (naming, formatting, patterns)
5. What is the team composition? (solo developer, small team, or enterprise with review gates)
6. What are the most common things Claude Code does wrong in this type of project? (future rules)

---

## DNA Requirements

For the complete DNA pattern applicability matrix for this product type,
see `product-dna/claude-md.yaml`. That file defines:
- Which of the 18 DNA patterns (D-01 to D-18) are required vs optional
- Validation checks per pattern (grep/glob commands)
- Template file mapping with DNA injection points
- Frontmatter fields (Anthropic Agent Skills spec)
- Discovery questions for /create

**MCS scoring:** `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
See `references/quality/mcs-spec.md` for full scoring formula.
