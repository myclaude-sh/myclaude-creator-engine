---
name: publish
description: >-
  Package and publish a product to myclaude.sh. Strips guidance comments, generates
  vault.yaml manifest, stages .publish/ directory, and invokes the myclaude CLI.
  Use when a product has passed validation and the creator is ready to ship,
  or when they say "publish", "ship it", "put it on the marketplace", or "go live".
disable-model-invocation: true
---

# Publisher

Package and publish a product to the MyClaude marketplace.

**When to use:** When a product has passed MCS-1 validation and the creator is ready to distribute it.

**When NOT to use:** Before running `/validate`. Do not publish a product that has not passed MCS-1 — the Publisher will catch this and abort, but it is faster to validate first.

---

## Activation Protocol

1. Verify MCS-1 validation has passed recently — check `.engine-meta.yaml`:
   - If `last_validation_result: "passed"` and `last_validated` is today → proceed
   - Otherwise → run `/validate` first and wait for it to complete
2. Load `creator.yaml` from project root for author metadata
3. Check CLI availability: does the `myclaude` command exist? (`which myclaude` or `where myclaude`)
   - If yes → CLI path available, will use for publish step
   - If no → note this, will provide install instructions at publish step

---

## Commands

```
/package     → Strip guidance comments, generate vault.yaml, stage .publish/ directory
/publish     → Run /package (if needed), invoke myclaude publish from .publish/
```

---

## Core Instructions

### /package FLOW

**Step 1 — Strip Guidance Comments (CE-D12)**

Scan all files in `workspace/{product-slug}/` recursively.
Remove all lines/blocks matching:
- `<!-- GUIDANCE: ... -->` (HTML comment format)
- `# GUIDANCE: ...` (YAML/inline comment format, only when the entire line is a GUIDANCE comment)

Create the cleaned output in a staging directory: `workspace/{product-slug}/.publish/`
Do NOT modify the original files in `workspace/{product-slug}/` — the staging copy is what gets packaged.

Verify nothing was unintentionally stripped: count lines before and after, report delta.

**Step 2 — Generate vault.yaml**

Write `vault.yaml` to the `.publish/` directory using the WP-3 unified schema:

```yaml
# vault.yaml v2 — unified manifest for MyClaude ecosystem
name: "{product-slug}"
display_name: "{product display name}"
version: "{semver from product}"
type: "{skill|agent|squad|workflow|design-system|claude-md|prompt|application|system}"
description: "{one-line description, 10-500 chars}"
long_description: "{extended description — supports markdown, up to 2000 chars}"
license: "{MIT|Apache-2.0|GPL-3.0|BSD-3-Clause|ISC|CC-BY-4.0|CC-BY-SA-4.0|CC0-1.0|Proprietary|Custom}"

tags: ["{tag1}", "{tag2}"]
price: 0  # USD, 0 = free. Set by creator during /publish confirmation.
mcs_level: {1|2|3}  # From most recent validation result
language: "{en|pt-BR|es|other}"  # CE-D37: from creator.yaml language field

install_target: "{path per CE-D38 rules}"
  # skill|agent|squad|workflow|prompt|system → .claude/skills/{slug}/
  # claude-md → .claude/rules/{slug}.md
  # design-system|application → myclaude-products/{slug}/
compatibility:
  claude_code: ">=1.0.0"
dependencies:
  myclaude: []  # list other MyClaude product slugs required

entry: "{main file — SKILL.md for skills/agents/squads, index.ts for apps}"
readme: "README.md"
```

CE-D38 install_target rules:
- `skill`, `agent`, `squad`, `workflow`, `prompt`, `system` → `.claude/skills/{slug}/`
- `claude-md` → `.claude/rules/{slug}.md`
- `design-system`, `application` → `myclaude-products/{slug}/`

**Step 3 — Generate / Update CHANGELOG.md**

If `CHANGELOG.md` exists in the staging directory → read it and append new version entry if version changed.

If `CHANGELOG.md` does not exist → generate initial entry:

```markdown
# Changelog

## [1.0.0] — {YYYY-MM-DD}

### Added
- Initial release
```

**Step 4 — Copy LICENSE**

If `LICENSE` exists in the workspace directory → copy to `.publish/`.
If not → generate a LICENSE file matching the license field in vault.yaml.

**Step 5 — Quality Gate: Re-validate Package**

Run MCS-1 structural validation on the `.publish/` directory contents.
This catches any accidental breakage from the stripping step.

If re-validation fails → abort packaging, report what broke, do NOT mark as ready for publishing.

**Step 6 — Report**

```
Package ready at: workspace/{product-slug}/.publish/
  Files: {count}
  Size: {total size}
  License: {license}
  MCS Level: MCS-{level}
  Guidance comments stripped: {n} occurrences removed
```

---

### /publish FLOW

**Step 1 — Verify .publish/ exists**

If `.publish/` directory does not exist or is stale (not from today):
→ Run `/package` first.

**Step 2 — Optimize Description for Discoverability**

Before finalizing metadata, review the product's description:
1. Read the description from vault.yaml
2. Generate 5 sample search queries a buyer might use to find this product
3. Check: would this description surface for those queries?
4. If description is vague or missing trigger keywords, suggest improvements:
   "Your description says '{current}'. A buyer searching for '{query}' might not find it. Consider: '{improved}'"
5. Let the creator accept or edit — this is coaching, not blocking

**Step 3 — Collect Publish Metadata**

Ask the creator for any fields not already confirmed in `vault.yaml`:
```
Price (USD, 0 = free): [default: 0]
Tags (comma-separated, 3-5 recommended):
```

For pricing, provide context from `references/market/pricing-guide.md`:
"Products in {category} at MCS-{level} typically range from ${low} to ${high}."

Update `vault.yaml` in `.publish/` with provided values.

**Step 4 — Show Summary and Require Confirmation**

```
Ready to publish:

  Product:   {display_name} v{version}
  Category:  {type}
  License:   {license}
  MCS Level: MCS-{level}
  Price:     ${price} (free if 0)
  Tags:      {tags}

Publish to myclaude.sh? [y/n]
```

Do NOT proceed unless the creator types `y` or `yes`. Exact confirmation is required.

**Step 5 — Invoke CLI**

Execute from the `.publish/` directory:
```bash
cd workspace/{product-slug}/.publish && myclaude publish
```

The CLI reads `vault.yaml` from CWD, packs the directory, uploads to R2, and creates the product.

Stream CLI output to the creator. Wait for success/error response.

If `myclaude` CLI is NOT installed:

```
The `myclaude` CLI is not installed or not in PATH.

Install it with:
  npm i -g @myclaude/cli

Then run:
  cd workspace/{product-slug}/.publish && myclaude publish
```

Do not fail silently. Inform the creator clearly.

**Step 6 — Record Result**

On success, update `.engine-meta.yaml`:
```yaml
scaffold_state: "published"
published_at: "{YYYY-MM-DD}"
marketplace_url: "{URL from CLI response}"
```

Update `creator.yaml` inventory:
```yaml
published_products: {increment by 1}
unpublished_drafts: {decrement by 1 if applicable}
```

Report to creator:
```
Published! View at: myclaude.sh/p/{product-slug}
```

---

## Output Structure

```
workspace/{product-slug}/.publish/          ← staged package directory
workspace/{product-slug}/.publish/vault.yaml  ← unified manifest
workspace/{product-slug}/.publish/CHANGELOG.md
workspace/{product-slug}/.publish/LICENSE
.engine-meta.yaml                           ← updated with publish state
creator.yaml                                ← updated inventory
```

---

## vault.yaml Schema Reference

Full schema with all fields and valid values (WP-3):

```yaml
# Required
name: string                    # slug format: lowercase-hyphenated
version: string                 # semver: MAJOR.MINOR.PATCH
type: enum                      # skill|agent|squad|workflow|design-system|prompt|claude-md|application|system
description: string             # one-line, 10-500 characters
license: enum                   # MIT|Apache-2.0|GPL-3.0|BSD-3-Clause|ISC|CC-BY-4.0|CC-BY-SA-4.0|CC0-1.0|Proprietary|Custom
entry: string                   # main file path
readme: string                  # README file path

# Enrichment (optional, defaults applied by CLI)
display_name: string            # human-readable name (default: title-cased name)
long_description: string        # markdown, up to 2000 characters
tags: string[]                  # 1-10 tags, lowercase
price: number                   # USD, 0 = free
mcs_level: 1|2|3               # from validation result (default: 1)
language: string                # ISO 639-1: en, pt-BR, es, etc. (default: "en")
install_target: string          # CE-D38: where CLI installs the product
compatibility:
  claude_code: string           # semver range (default: ">=1.0.0")
dependencies:
  myclaude: string[]            # required MyClaude product slugs (default: [])
```

---

## Quality Gate

The Publisher passes if:
- MCS-1 validation passed before packaging
- All guidance comments were stripped from the staged copy (original files untouched)
- `vault.yaml` is valid YAML with all required fields populated
- `CHANGELOG.md` exists in the package
- Re-validation of the `.publish/` directory contents passes MCS-1
- Creator explicitly confirmed publish before any CLI call was made

---

## Decision Notes

**CE-D12:** Guidance comments exist to help creators fill content. They must be stripped before distribution so buyers receive clean, professional files. The staging copy ensures originals are never modified.

**CE-D33 (RESOLVED per WP-20):** The `myclaude publish` CLI command is fully functional. The Engine invokes it directly from the `.publish/` directory. If the CLI is not installed, the Publisher provides install instructions — it does not provide a manual upload fallback.

**CE-D38:** `install_target` tells the MyClaude CLI where to place files on the buyer's machine. This field is category-specific and must be exact — buyers rely on it for correct installation. When in doubt, default to `.claude/skills/{slug}/`.

**CE-D37:** The `language` field enables marketplace filtering by language. Always inherit from `creator.yaml` unless the product explicitly targets a different language than the creator's default.

**WP-3:** `vault.yaml` is the unified manifest for the entire MyClaude ecosystem. The CLI reads it directly. The Engine generates it. There is no separate `manifest.yaml`.

**Why re-validate after packaging:** The stripping step could theoretically remove content that was incorrectly formatted as a guidance comment. Re-validation is a safety net that catches this before a broken package reaches the marketplace.
