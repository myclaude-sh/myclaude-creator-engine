# Code Health Check

> Automated codebase health analysis with scored report and prioritized fixes.

## What It Does

Runs 5 health dimensions on your codebase:
- **Dead Code** — finds unused exports and unreferenced files
- **Dependency Health** — flags stale, deprecated, or vulnerable dependencies
- **Test Coverage** — measures test file ratio and infrastructure presence
- **Security Surface** — detects hardcoded secrets, eval(), exposed patterns
- **Complexity Hotspots** — identifies long files, deep nesting, complex functions

Produces a scored report (0-100 per dimension, weighted overall) with specific file:line findings and prioritized remediation.

## Installation

```bash
myclaude install code-health-check
```

The skill installs to `.claude/skills/code-health-check/`.

## Usage

```
/code-health-check              # Full analysis on current directory
/code-health-check src/         # Scoped to src/ only
```

### Output

A scored report with letter grade (A-F), per-dimension breakdown, and top 3 priorities.

### When to Use

- Before a release: catch issues before they ship
- Sprint planning: identify tech debt to prioritize
- Onboarding: understand a new codebase's health
- Periodic check: run monthly to track trends

## Requirements

- Claude Code >= 1.0.0
- A codebase with source files (any language)
- Bash tool access (for dependency checks)

---

**Version:** 1.0.0 | **License:** MIT | **MCS:** 3
**Author:** @myclaude-team
