---
name: publish
description: >-
  Publish a packaged product to myclaude.sh via the CLI. Shows summary,
  requires confirmation, runs myclaude validate + myclaude publish.
  Use when the creator says "publish", "ship it", "go live", or after /package.
argument-hint: "[product-slug]"
---

# Publisher

Publish a packaged product to the MyClaude marketplace via CLI delegation.

**When to use:** After /package has staged .publish/ directory.

**When NOT to use:** If product hasn't been packaged yet (run /package first).

---

## Activation Protocol

1. Identify product: `$ARGUMENTS` as slug → `workspace/{slug}/`
2. Read `.meta.yaml` → verify state is "packaged"
3. Verify `.publish/` exists with vault.yaml
4. Check CLI: `which myclaude` — if not found, show install instructions
5. Read `creator.yaml` → verify auth status. If missing → "Creator profile not found. Run `/onboard` first." and stop.

---

## Core Instructions

### PUBLISH FLOW

**Step 1 — Summary**

Display what will be published:

```
Ready to publish:

  Name:     {displayName}
  Slug:     {slug}
  Type:     {type}
  Version:  {version}
  Price:    {price == 0 ? "Free" : "$" + price}
  License:  {license}
  MCS:      {level} ({score}%)
  Files:    {N} in .publish/

Publish to myclaude.sh? (yes/no)
```

**Step 2 — Confirmation**

Wait for explicit "yes" from creator. Do NOT proceed without confirmation.

**Step 3 — CLI Pre-flight**

```bash
cd workspace/{slug}/.publish && myclaude validate
```

If validation fails, report errors and abort.

**Step 4 — Publish**

```bash
cd workspace/{slug}/.publish && myclaude publish
```

Report CLI output verbatim.

**Step 5 — Update State**

On success:
```yaml
# .meta.yaml updates
state:
  phase: "published"
  published_at: "{ISO timestamp}"
  version: "{version}"
```

**Step 6 — Report**

```
Published! {displayName} v{version} is live on myclaude.sh

  URL:     https://myclaude.sh/p/{slug}
  Install: myclaude install {slug}
  MCS:     {mcs_level} ({score}%)
  Platforms: MyClaude + Anthropic Plugin + 33 Agent Skills platforms
```

**Step 7 — Distribution Amplification**

After successful publish, suggest multi-channel distribution:

```
Maximize your reach! Your product is ready for:

  1. GitHub — Push to a public repo. Your README already has MyClaude badges.
     Topics: claude-code, agent-skills, myclaude, {type}

  2. Anthropic Plugin Marketplace — Your plugin.json is ready.
     Run: /plugin marketplace add {your-github-repo}

  3. Community — Share on:
     - Reddit: r/ClaudeCode, r/ClaudeAI
     - X: #ClaudeCode #MyClaude
     - Dev.to / Hashnode article

  4. Awesome Lists — Submit to:
     - github.com/hesreallyhim/awesome-claude-code
     - github.com/travisvn/awesome-claude-skills

Every distribution point links back to your MyClaude product page.
```

---

## CLI Not Found

If `myclaude` CLI is not installed:

```
MyClaude CLI not found. Install it:
  npm install -g @myclaude-cli/cli

Then run /publish again.

Alternative: upload manually at myclaude.sh/publish
```

---

## Anti-Patterns

1. **Publishing without confirmation** — Always require explicit "yes".
2. **Publishing unpackaged product** — Check .meta.yaml state first.
3. **Swallowing CLI errors** — Report all CLI output, don't hide failures.
4. **Re-publishing without version bump** — If already published, require version increment.
5. **Publishing with secrets** — CLI pre-flight catches this, but mention it if found.
