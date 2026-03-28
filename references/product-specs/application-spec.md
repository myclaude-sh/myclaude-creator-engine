# Product Spec: Applications

## Definition

Applications are complete tools, utilities, or applications built with Claude Code.
They are the most concrete product type — shippable software that a buyer can install
and run immediately.

An application is NOT:
- A workflow (workflows are reusable process definitions; apps are specific implementations)
- A skill (skills assist Claude Code; apps are standalone tools)
- A code snippet or library

An application IS:
- Working software with a real entry point
- A complete, installable product with setup instructions
- A Claude Code project that demonstrates the tool being built alongside it

---

## Canonical File Structure

```
app-name/
├── README.md              # Setup and usage (REQUIRED)
├── src/                   # Source code (REQUIRED)
│   └── [implementation]
├── package.json           # Dependencies (REQUIRED for Node.js apps)
├── CLAUDE.md              # Project-specific Claude Code config
└── docs/
    └── architecture.md
```

**Notes:**
- For Python apps: use `pyproject.toml` or `requirements.txt` instead of `package.json`
- For CLI utilities: include `bin/` directory
- For web apps: include `public/` and build configuration

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `README.md` | Setup, usage, examples | MCS-1 |
| `src/` (working code) | The application itself | MCS-1 |
| `package.json` / dependency manifest | Dependencies declaration | MCS-1 |

---

## Required Sections in README.md

### 1. What It Does (Above the Fold)

```markdown
# App Name

One sentence description. [What it does, for whom.]

## Quick Start
[The fastest path from zero to working]
```

The first paragraph is the most important — it determines if a buyer continues reading (H: "Q1 — if it doesn't make someone want to install in 30 seconds, rewrite it").

### 2. Installation

Exact steps to install with specific commands:

```markdown
## Installation

**Requirements:**
- Node.js 20+ (or Python 3.11+, etc.)
- [Other specific requirements]

```bash
git clone [or: download and unzip]
cd app-name
npm install
npm run setup  # if applicable
```
```

### 3. Usage

Concrete usage examples with real commands:

```markdown
## Usage

**Basic:**
```bash
npx app-name [command] [options]
```

**Example:**
```bash
app-name analyze --input data.csv --output report.md
```
```

### 4. Architecture

How the app is structured:
- Key modules and what they do
- Data flow
- External dependencies (APIs, services, databases)

### 5. Configuration

All configurable options:
- Environment variables
- Config file format
- CLI flags

### 6. Requirements

Full requirements list:
- Runtime version
- System dependencies
- External services (APIs, databases)
- Permissions required

---

## MCS Requirements

### MCS-1: Publishable

**Universal:**
- [ ] README.md with all required sections
- [ ] Working source code in `src/` (not placeholder)
- [ ] Dependency manifest (`package.json`, `pyproject.toml`, etc.)
- [ ] Metadata complete
- [ ] No hardcoded secrets or API keys
- [ ] No malicious code patterns
- [ ] License from approved list

**Application-Specific:**
- [ ] App actually runs (not broken on install)
- [ ] At least 1 usage example with real command
- [ ] Dependencies pinned to specific versions (not `latest`)
- [ ] Basic error handling (doesn't crash on bad input)

### MCS-2: Quality

**Universal (beyond MCS-1):**
- [ ] `CLAUDE.md` project config
- [ ] `docs/architecture.md`
- [ ] Tested on clean install
- [ ] No security vulnerabilities in dependencies
- [ ] Anti-patterns section (common misuse)
- [ ] 2+ usage examples
- [ ] Semver versioning

**Application-Specific:**
- [ ] CLAUDE.md config enables future development on the app
- [ ] Architecture docs explain key design decisions
- [ ] Error messages are human-readable and actionable
- [ ] Input validation on all user-provided inputs
- [ ] Graceful degradation when external services fail

### MCS-3: State-of-the-Art

**Universal (beyond MCS-2):**
- [ ] CI/CD configuration (GitHub Actions, etc.)
- [ ] Test suite with meaningful coverage
- [ ] Production-ready (logging, error handling, config management)
- [ ] Architecture docs with decision records
- [ ] Differentiation statement

**Application-Specific:**
- [ ] Test suite covers happy path AND common failure modes
- [ ] CI/CD runs tests and validates build on every push
- [ ] Production configuration separated from development config
- [ ] Observability: structured logging, error tracking (at minimum)
- [ ] Deployment guide for the target environment (local / cloud / container)

---

## Anti-Patterns for Applications

### Structural
- **Broken on install:** App has build errors, missing dependencies, or fails on basic commands. MCS-1 requires the app to actually work.
- **`package.json` without lockfile:** Dependencies without a lockfile (`package-lock.json`, `yarn.lock`) lead to non-reproducible installs.
- **Secrets in source:** Any hardcoded credentials, API keys, or personal data in the source. Grounds for immediate rejection.

### Content
- **README that's a feature list:** Listing all capabilities without showing how to use them. README should lead with "here's what it does and here's the exact command to run it."
- **Architecture doc that's a file tree:** Just listing files and directories without explaining WHY the app is structured that way.
- **No error handling:** App crashes with an unhelpful stack trace on bad input. Error messages should tell the user what went wrong and what to do.

### Quality
- **No CLAUDE.md:** Application has no Claude Code config. Future contributors can't efficiently develop it with Claude Code.
- **Dependencies not pinned:** Using `"^1.0.0"` for all dependencies. Breaking changes in dependencies will break the app for buyers.
- **No clean install test:** App works on creator's machine but fails on a fresh install because of undocumented system dependencies.

---

## Discovery Questions (from §7)

When creating an application, answer these before scaffolding:

1. What does this application do? (utility, tool, template, demo)
2. What is the tech stack? (language, framework, key dependencies)
3. Who is the target user? (developer installing and running it, or end-user operating it)
4. Does it require external services? (APIs, databases, auth — if yes, document clearly)
5. What is the deployment model? (local CLI, web app, Docker container, etc.)
6. What are the most common reasons this type of app breaks? (future error handling requirements)

---

## DNA Requirements

For the complete DNA pattern applicability matrix for this product type,
see `product-dna/application.yaml`. That file defines:
- Which of the 18 DNA patterns (D-01 to D-18) are required vs optional
- Validation checks per pattern (grep/glob commands)
- Template file mapping with DNA injection points
- Frontmatter fields (Anthropic Agent Skills spec)
- Discovery questions for /create

**MCS scoring:** `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
See `references/quality/mcs-spec.md` for full scoring formula.
