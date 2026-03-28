# MCS-1 Checks — Publishable

> **v2.0 alignment:** These checks map to Stages 1-3 of the 7-stage validation pipeline.
> Stage 1 (Structural) = U1-U3. Stage 2 (Integrity) = U4-U5. Stage 3 (DNA Tier 1) = D1,D2,D3,D4,D13,D14.
> Security checks U8-U9 are in Stage 6 (CLI Preflight). See config.yaml for scoring formula.
> For DNA pattern requirements per type, see `product-dna/{type}.yaml`.

Minimum bar for marketplace listing. All checks are automated.

**Total checks in this tier:** 9 universal + DNA Tier 1 (6 patterns) + per-type structural checks.

---

## Universal Checks (all product types)

| # | Check | Description | Auto-fixable |
|---|-------|-------------|--------------|
| U1 | Valid structure | Correct files exist in correct locations for the declared product type | No (requires creator input) |
| U2 | Required metadata | Primary definition file has: `name`, `description`, `category`, `version`, `license` | Partially (version, category can default) |
| U3 | README.md present | README.md exists with four required sections: what it does, how to install, how to use, requirements | No (content must be written) |
| U4 | No broken references | Every file path mentioned in any file actually exists in the package | No |
| U5 | No syntax errors | All `.md`, `.yaml`, `.json` files parse without errors | Partially (indentation, trailing commas) |
| U6 | Size under 50MB | Total package size is below 50MB | No |
| U7 | Approved license | License field matches one of: MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, ISC, CC-BY-4.0, CC-BY-SA-4.0, CC0-1.0, Proprietary, Custom | Yes (default to MIT if missing) |
| U8 | No secrets | No hardcoded API keys, passwords, tokens, or credentials in any file | No (BLOCKING — cannot auto-fix) |
| U9 | No malicious patterns | No `eval()`, `exec()`, network calls to unknown/untrusted hosts, or obfuscated code | No (BLOCKING — cannot auto-fix) |

---

## Automated Check Suite

```
/validate → runs MCS-1 suite
  ├── structure-check    U1: correct files for product type?
  ├── metadata-check     U2: all required fields present?
  ├── readme-check       U3: required sections present?
  ├── reference-check    U4: all file references resolve?
  ├── syntax-check       U5: valid markdown/yaml/json?
  ├── size-check         U6: under limits?
  ├── license-check      U7: approved license declared?
  └── security-scan      U8+U9: no secrets or malicious patterns?
```

---

## Per-Type Structural Requirements

### Skill

Required files:
- `SKILL.md` — primary definition
- `README.md` — documentation

Required sections in `SKILL.md`:
- Title and one-line description
- When to use / when NOT to use
- Activation Protocol
- Core Instructions
- Output Structure
- Quality Gate

### Agent

Required files:
- `AGENT.md` — primary definition
- `README.md` — documentation

Required sections in `AGENT.md`:
- Identity (name, role, persona)
- Knowledge Substrate
- Core Behaviors
- Activation Protocol

### Squad

Required files:
- `SQUAD.md` — primary definition
- `agents/` directory (at least 2 agent definitions)
- `README.md` — documentation

Required sections in `SQUAD.md`:
- Mission and purpose
- Agent roster with roles
- Routing logic
- Handoff protocols

### Workflow

Required files:
- `WORKFLOW.md` — primary definition
- `README.md` — documentation

Required sections in `WORKFLOW.md`:
- Purpose and trigger
- Inputs and outputs
- Step sequence
- Error handling

### Design System

Required files:
- `tokens/` directory (at least one token file)
- `README.md` — documentation

Required sections in README:
- Brand identity
- Platform targets
- Export formats
- Installation instructions

### Prompt

Required files:
- `PROMPT.md` — primary definition
- `README.md` — documentation

Required sections in `PROMPT.md`:
- Purpose
- Variables (with descriptions)
- Usage example
- Expected output format

### CLAUDE.md

Required files:
- `CLAUDE.md` — the configuration file itself
- `README.md` — documentation

Required sections in `CLAUDE.md`:
- Project type and context
- Key conventions
- Prohibited patterns

### Application

Required files:
- `src/` directory (at least one source file)
- `README.md` — documentation
- Package manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, or equivalent)

Required sections in README:
- What it does
- Installation
- Usage
- Dependencies

### System

Required files:
- `SYSTEM.md` — primary definition
- At least one subdirectory (`skills/`, `agents/`, or `workflows/`)
- `README.md` — documentation

Required sections in `SYSTEM.md`:
- Purpose and scope
- Component inventory
- Entry point
- Installation

---

## Security Scan Patterns

Patterns that trigger U8 (secrets):
- Strings matching: `sk-`, `AIza`, `ghp_`, `xox`, `Bearer `, `api_key`, `apikey`, `secret`, `password`, `token` followed by `=` and a value
- Base64-encoded strings longer than 40 characters in non-example contexts
- Private key headers: `-----BEGIN RSA PRIVATE KEY-----`, `-----BEGIN PRIVATE KEY-----`

Patterns that trigger U9 (malicious code):
- `eval(` in any scripting context
- `exec(` in any scripting context
- `__import__('os').system(` or similar
- Network calls to IPs directly (not domain names) in non-configurable locations
- Obfuscated strings (hex-encoded executable code)

**Note:** U8 and U9 failures are BLOCKING. The package cannot be published until they are resolved. Auto-fix is not available for security issues.
