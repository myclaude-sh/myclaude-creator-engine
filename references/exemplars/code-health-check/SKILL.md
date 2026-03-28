---
name: code-health-check
description: >-
  Run a comprehensive codebase health analysis covering dead code, dependency
  freshness, test coverage gaps, security surface, and complexity hotspots.
  Produces a scored report with prioritized remediation. Use when the user asks
  to "check health", "audit the codebase", "code quality", or "technical debt".
argument-hint: "[path-or-scope]"
allowed-tools: [Read, Glob, Grep, Bash]
---

<!-- WHY: D1 (Activation Protocol) — Load check definitions and scoring before
     running any analysis. Without this, checks are ad-hoc and inconsistent. -->

# Code Health Check

> Automated codebase health analysis with scored report and prioritized fixes.

**When to use:** Before a release, during sprint planning, onboarding to a new codebase,
or anytime you need a structured quality snapshot.

**When NOT to use:** For runtime debugging (use a debugger). For security-specific audits
(use a dedicated security tool). This is a structural health check, not a pentest.

---

## Activation Protocol

Before running any checks:

1. **Load check definitions:** Read `references/health-checks.md`
2. **Load scoring:** Read `references/scoring-methodology.md`
3. **Detect project type:** Glob for package.json, pyproject.toml, Cargo.toml, go.mod
4. **Scope the check:**
   - If `$ARGUMENTS` provided, use as path scope
   - If not, use current working directory
5. **Verify it's a code repo:** Check for `.git/` or source files
   - If no code found: "This doesn't appear to be a codebase. Point me to a project directory."

---

<!-- WHY: D5 (Question System) — If scope is ambiguous, ask before running
     a potentially expensive analysis on the wrong directory. -->

## Question System

| Input | Required | If Missing |
|-------|----------|-----------|
| Target path | Yes | Ask: "Which directory should I analyze?" |
| Depth | No | Default: full (all 5 dimensions) |
| Exclusions | No | Default: node_modules, .git, dist, build, vendor |

---

## Core Instructions

Run 5 health dimensions in sequence. Each produces a 0-100 score.

### Dimension 1: Dead Code (weight: 15%)

```bash
# Find unused exports
grep -r "export " --include="*.ts" --include="*.js" | # extract export names
# Cross-reference with imports across codebase
# Unused export = dead code candidate
```

- Glob all source files
- Extract exported symbols (functions, classes, constants)
- Grep for imports/usage of each symbol
- Score: 100 - (dead_exports / total_exports × 100)

### Dimension 2: Dependency Health (weight: 20%)

- Read package.json / requirements.txt / Cargo.toml
- Check last publish date of each dependency (if available via Bash)
- Flag: dependencies > 1 year old, deprecated packages, known CVEs
- Score: 100 - (stale_deps / total_deps × 100)

### Dimension 3: Test Coverage (weight: 25%)

- Glob test files (*.test.*, *.spec.*, test_*, *_test.*)
- Glob source files
- Calculate ratio: test_files / source_files
- Check for test configuration (jest.config, pytest.ini, etc.)
- Score: (test_ratio × 50) + (has_config × 25) + (has_ci × 25)

### Dimension 4: Security Surface (weight: 20%)

- Grep for hardcoded secrets (API keys, tokens, passwords)
- Check for eval(), exec(), dangerouslySetInnerHTML
- Check .env.example exists (if .env is gitignored)
- Check dependency audit (npm audit / pip-audit)
- Score: 100 - (findings × 10), min 0

### Dimension 5: Complexity Hotspots (weight: 20%)

- Find files > 500 lines (candidates for splitting)
- Find functions > 50 lines (candidates for extraction)
- Find deeply nested code (> 4 levels of indentation)
- Score: 100 - (hotspots / total_files × 100)

---

<!-- WHY: D4 (Quality Gate) — The report must meet these criteria before
     being presented to the user. Prevents low-quality analysis. -->

## Quality Gate

Before presenting the report, verify:
- [ ] All 5 dimensions produced a numeric score (0-100)
- [ ] At least 10 files were analyzed (otherwise scope is too narrow)
- [ ] Each finding has a specific file path (not generic advice)
- [ ] Remediation priorities are ordered by impact (not alphabetically)

---

<!-- WHY: D7 (Pre-Execution Gate) — Verify preconditions before running
     the potentially expensive analysis. -->

## Pre-Execution Gate

Before running checks:
- [ ] Target directory exists and contains source files
- [ ] At least one recognized language detected
- [ ] Not running inside node_modules or .git
- [ ] Sufficient context to complete analysis

---

<!-- WHY: D14 (Graceful Degradation) — Handle repos that are missing
     tests, deps, or other expected structures without crashing. -->

## Degradation Handling

| Missing Element | Behavior |
|----------------|----------|
| No tests at all | Score dimension 3 at 0, note "No test infrastructure detected" |
| No package manager | Skip dimension 2, note "No dependency manifest found" |
| Binary/generated files | Exclude from analysis, note count |
| Monorepo | Ask which package to analyze, or run on root |
| Empty directories | Skip, don't count as dead code |

---

<!-- WHY: D2 (Anti-Pattern Guard) — Common mistakes when doing health checks. -->

## Anti-Patterns

1. **Counting lines as quality** — More lines ≠ worse. Measure complexity, not volume.
2. **Flagging all old dependencies** — Stable deps (lodash, express) being "old" is fine.
3. **Test file ratio as coverage** — File existence ≠ meaningful test coverage.
4. **Generic advice** — "You should write more tests" is useless. Specify WHICH files need tests.
5. **Ignoring context** — A prototype has different health standards than production code.
6. **Running on vendor code** — Always exclude node_modules, vendor, generated code.
7. **One-time snapshot thinking** — Health checks should be re-run periodically, not once.

---

<!-- WHY: D16 (Composability) — No hardcoded paths. Works in any project. -->

## Output Format

```
CODE HEALTH REPORT — {project_name}
Generated: {date} | Scope: {path} | Files: {N}

OVERALL HEALTH: {score}/100 {grade}

  Dead Code        {score}/100  ████████░░  {dead_count} unused exports
  Dependencies     {score}/100  ██████████  {stale_count} stale, {vuln_count} vulnerable
  Test Coverage    {score}/100  ██████░░░░  {test_ratio}% file coverage
  Security Surface {score}/100  █████████░  {finding_count} findings
  Complexity       {score}/100  ████████░░  {hotspot_count} hotspots

TOP PRIORITIES (fix these first):
  1. {file:line} — {issue} — {impact}
  2. {file:line} — {issue} — {impact}
  3. {file:line} — {issue} — {impact}

DETAILED FINDINGS: {N} total across 5 dimensions
  [See below for per-dimension breakdown]
```

Grade scale: A (90+), B (75-89), C (60-74), D (40-59), F (<40)
