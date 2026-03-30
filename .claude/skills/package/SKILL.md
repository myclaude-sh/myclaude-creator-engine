---
name: package
description: >-
  Package a product for distribution across 33+ platforms. Strips WHY comments, generates
  triple manifests (vault.yaml + plugin.json + agentskills.yaml), stages .publish/. Use
  when: 'package', 'prepare for publish', or 'bundle it'.
argument-hint: "[product-slug]"
---

# Packager

Stage a product for distribution with triple manifests (MyClaude + Anthropic Plugin + Agent Skills universal).

**When to use:** After /validate passes. Before /publish.

**When NOT to use:** If the product hasn't been validated yet (run /validate first).

---

## Activation Protocol

1. Identify product: `$ARGUMENTS` as slug → `workspace/{slug}/`
2. Read `.meta.yaml` → verify state is "validated" and MCS score >= 75%
3. Read `creator.yaml` → load author metadata for manifests. If missing → "Creator profile not found. Run `/onboard` first." and stop.
4. Load `product-dna/{type}.yaml` → get install_target
5. Load `config.yaml` → vault_defaults for missing fields

---

## Core Instructions

### PACKAGING PIPELINE

**Step 1 — Verify Validation**

Read `.meta.yaml` for validation state:
- If state != "validated": "Product not validated. Run /validate first."
- If MCS score < 75%: "Product below MCS-1 threshold. Run /validate --fix."

**Step 2 — Strip WHY Comments + Inject Attribution** (SE-D17)

Create a clean copy of all product files.

**REMOVE:**
- `<!-- WHY: ... -->` (HTML comment blocks — may span multiple lines)
- Lines matching `# WHY:` pattern (markdown comment format)

**INJECT** at the very end of the primary product file (SKILL.md, AGENT.md, etc.):
```html
<!-- Published on MyClaude (myclaude.sh) | Quality: MCS-{level} ({score}%) | Engine: Studio v2 -->
```
This attribution comment is:
- Invisible to Claude (HTML comment, does not affect behavior)
- Visible in source code (GitHub renders it in raw view)
- Indexable by search engines (creates discoverable MyClaude references)
- A quality signal (MCS score travels with the product)

Never modify originals — work on the copy in `.publish/`.

**Step 2b — Verify WHY Removal**

Grep all files in `.publish/` for the pattern `WHY:`. If match count > 0, re-run stripping on the matched files. If still > 0 after second pass, report error with file paths and line numbers — do not proceed to manifest generation with unstripped WHY comments.

**Step 3 — Generate vault.yaml**

```yaml
# REQUIRED (from .meta.yaml + creator.yaml)
name: "{slug}"
version: "{from .meta.yaml or config default}"
type: "{product type}"
description: "{from README.md first paragraph or .meta.yaml}"
entry: "{primary file from product-dna/{type}.yaml}"
license: "{from creator.yaml or config default}"
price: {from .meta.yaml or 0}
tags: ["{from .meta.yaml}"]

# ENRICHMENT (from .meta.yaml + creator.yaml + computed)
displayName: "{humanized from name}"
mcsLevel: {from last validation score}
language: "{from creator.yaml}"
longDescription: "{from README.md}"
readme: "README.md"
installTarget: "{from product-dna/{type}.yaml}"
compatibility:
  claudeCode: ">=1.0.0"

# DISTRIBUTION DNA (viral growth layer — links back to MyClaude ecosystem)
engine: "myclaude-studio-engine"
marketplace: "https://myclaude.sh/p/{slug}"
badges:
  mcs: "https://myclaude.sh/badge/mcs/{mcs_level_number}.svg"
  available: "https://myclaude.sh/badge/available.svg"
```

**Step 4 — Generate plugin.json** (Anthropic Plugin Marketplace)

```json
{
  "name": "{slug}",
  "description": "{description}",
  "version": "{version}",
  "author": { "name": "{from creator.yaml}" },
  "license": "{license}",
  "homepage": "https://myclaude.sh/p/{slug}"
}
```

**Step 4b — Generate agentskills.yaml** (Agent Skills Universal — 33+ platforms)

The Agent Skills spec (agentskills.io) is the open standard adopted by Claude Code, Cursor,
GitHub Copilot, VS Code, Gemini CLI, OpenAI Codex, Kiro, JetBrains, and 25+ more platforms.
Generate this manifest so the product is installable everywhere.

```yaml
# Agent Skills Universal Manifest
name: "{slug}"
version: "{version}"
description: "{description}"
type: "{product type}"
author: "{from creator.yaml}"
license: "{license}"
entry: "{primary file}"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini-cli
  - copilot
  - "*"  # Compatible with any Agent Skills-compliant platform
install:
  target: "{from product-dna install_target}"
  files:
    - "{list all files in .publish/ relative paths}"
metadata:
  mcs_level: "{from validation}"
  mcs_score: "{from validation}"
  marketplace: "https://myclaude.sh/p/{slug}"
```

Only generate for types that map to Agent Skills format (skill, agent, prompt, workflow).
For types that don't map cleanly (design-system, application), generate only vault.yaml + plugin.json.

**Step 5 — Calculate Checksum**

SHA-256 of the entire .publish/ directory contents.

**Step 6 — Stage .publish/**

Create `workspace/{slug}/.publish/` with:
- Cleaned product files (WHY comments stripped)
- vault.yaml (MyClaude marketplace)
- plugin.json (Anthropic plugin marketplace)
- agentskills.yaml (Agent Skills universal — if applicable type)
- CHANGELOG.md (generate if missing)
- LICENSE file (generate from license field)

**SYSTEM TYPE — Special packaging rules:**
Products of type `system` are standalone project roots (motors) — like PRISM, Cognitive Refinery, etc.
The user opens the system's folder in Claude Code to operate it. Three critical requirements:

**1. CLAUDE.md at root (brain):**
- Check if `CLAUDE.md` exists in the product source directory
- If it exists → include it in `.publish/`
- If it does NOT exist → generate one from SYSTEM.md (boot instructions, command list, rules)
- Without CLAUDE.md, the exported system is a dead folder

**2. .claude/commands/{name}/SYSTEM.md (slash command registration):**
- Copy the SYSTEM.md into `.publish/.claude/commands/{system-name}/SYSTEM.md`
- This makes `/system-name` available as a slash command when the user opens the folder
- The `name:` field in SYSTEM.md frontmatter determines the slash command name

**3. Bundle assets inside .claude/ (all commands available locally):**
When the system is part of a bundle, ALL other bundle products must be included inside
the system's `.publish/.claude/` so they work as slash commands when the user opens the motor:

```
.publish/
├── CLAUDE.md                          ← brain
├── SYSTEM.md                          ← reference
├── .claude/
│   ├── skills/                        ← skills from the bundle
│   │   ├── {skill-1}/SKILL.md
│   │   └── {skill-2}/SKILL.md
│   └── commands/                      ← agents, squads, workflows, the system itself
│       ├── {system-name}/SYSTEM.md    ← registers /system-name
│       ├── {agent}/AGENT.md
│       ├── {squad}/SQUAD.md + agents/
│       └── {workflow}/WORKFLOW.md
├── workspace/                         ← empty, ready for work
└── memory/                            ← initialized state files
```

Install target mapping for bundle assets:
- skill, prompt → `.claude/skills/{slug}/`
- agent, squad, workflow → `.claude/commands/{slug}/`
- Distribution files (vault.yaml, plugin.json, etc.) are EXCLUDED from these copies

**EXCLUDE from .publish/** (internal Engine files — never distribute):
- `.meta.yaml` (Engine product state tracking)
- `domain-map.md` (creator's working notes)
- Any file starting with `.` (hidden files, including `.env`) — EXCEPT `.claude/` directory
- Files matching secret patterns: `*.pem`, `*.key`, `*.p12`, `credentials*.json`, `*.env`
- If any excluded-for-secrets file is found, WARN: "Sensitive file `{file}` excluded from package. If this is intentional, rename it."

**Step 7 — Re-validate**

Run Stage 1 (structural) + Stage 6 (CLI preflight) on `.publish/` contents.
If any check fails, report and abort — don't leave broken package.

**Step 8 — Update State**

```yaml
# .meta.yaml updates
state:
  phase: "packaged"
  packaged_at: "{ISO timestamp}"
```

---

## Output Format

```
Package ready: workspace/{slug}/.publish/

  Files:    {N}
  Size:     {total size}
  License:  {license}
  MCS:      {level} ({score}%)
  Checksum: {sha256 first 12 chars}...

  WHY comments stripped: {N} occurrences
  Manifests: vault.yaml + plugin.json [+ agentskills.yaml]
  Platforms: MyClaude + Anthropic Plugin [+ 33 Agent Skills platforms]

Next: /publish to ship to myclaude.sh
```

---

## Anti-Patterns

1. **Packaging unvalidated product** — Always check .meta.yaml state first.
2. **Modifying originals** — Work on copies in .publish/. Never touch workspace/{slug}/ source files.
3. **Missing manifests** — vault.yaml + plugin.json required. agentskills.yaml for compatible types. Triple distribution.
4. **Stale checksum** — Recalculate if any file changes after initial staging.
5. **Silent failures** — If WHY stripping breaks markdown structure, detect and report.
