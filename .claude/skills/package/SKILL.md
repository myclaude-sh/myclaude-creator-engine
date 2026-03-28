---
name: package
description: >-
  Package a product for distribution. Strips WHY comments, generates vault.yaml
  + plugin.json dual manifests, calculates checksum, and stages .publish/ directory.
  Use when preparing a product for publishing, or when the creator says "package",
  "prepare for publish", "bundle it", or "stage it".
argument-hint: "[product-slug]"
---

# Packager

Stage a product for distribution with dual manifests (MyClaude + Anthropic).

**When to use:** After /validate passes. Before /publish.

**When NOT to use:** If the product hasn't been validated yet (run /validate first).

---

## Activation Protocol

1. Identify product: `$ARGUMENTS` as slug → `workspace/{slug}/`
2. Read `.meta.yaml` → verify state is "validated" and MCS score >= 75%
3. Read `creator.yaml` → load author metadata for manifests
4. Load `product-dna/{type}.yaml` → get install_target
5. Load `config.yaml` → vault_defaults for missing fields

---

## Core Instructions

### PACKAGING PIPELINE

**Step 1 — Verify Validation**

Read `.meta.yaml` for validation state:
- If state != "validated": "Product not validated. Run /validate first."
- If MCS score < 75%: "Product below MCS-1 threshold. Run /validate --fix."

**Step 2 — Strip WHY Comments** (SE-D17)

Create a clean copy of all product files. Remove:
- `<!-- WHY: ... -->` (HTML comment blocks — may span multiple lines)
- Lines matching `# WHY:` pattern (markdown comment format)

Never modify originals — work on the copy in `.publish/`.

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
```

**Step 4 — Generate plugin.json** (SE-D14)

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

**Step 5 — Calculate Checksum**

SHA-256 of the entire .publish/ directory contents.

**Step 6 — Stage .publish/**

Create `workspace/{slug}/.publish/` with:
- Cleaned product files (WHY comments stripped)
- vault.yaml
- plugin.json
- CHANGELOG.md (generate if missing)
- LICENSE file (generate from license field)

**EXCLUDE from .publish/** (internal Engine files — never distribute):
- `.meta.yaml` (Engine product state tracking)
- `domain-map.md` (creator's working notes)
- Any file starting with `.` (hidden files)

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
  Manifests: vault.yaml + plugin.json

Next: /publish to ship to myclaude.sh
```

---

## Anti-Patterns

1. **Packaging unvalidated product** — Always check .meta.yaml state first.
2. **Modifying originals** — Work on copies in .publish/. Never touch workspace/{slug}/ source files.
3. **Missing manifests** — Both vault.yaml AND plugin.json must be generated. Dual distribution.
4. **Stale checksum** — Recalculate if any file changes after initial staging.
5. **Silent failures** — If WHY stripping breaks markdown structure, detect and report.
