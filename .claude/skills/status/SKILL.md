---
name: status
description: >-
  Display Studio Engine status dashboard. Shows version, edition, creator profile,
  products with scores, and stale warnings. Use when: 'status', 'dashboard', 'show my
  products', or at session start.
---

# Status Dashboard

Display comprehensive engine status in a compact terminal-style dashboard.

**When to use:** Session start, or anytime the creator wants a status overview.

---

## Activation Protocol

1. Read `STATE.yaml` — engine version, edition, last session, workspace state
2. Read `creator.yaml` — creator name, type, expertise domains. If missing, show "Creator: not configured — run /onboard" in dashboard and continue with available data.
3. Glob `workspace/*/` — list all product directories
4. For each product, read `.meta.yaml` — slug, type, state, scores, timestamps
5. Detect edition: glob `.claude/skills/forge-master/SKILL.md`
   - Found → PRO edition
   - Not found → LITE edition
6. Render dashboard

---

## Dashboard Format

```
MyClaude Studio Engine v{version} [{edition}]
Creator: {name} ({type}) | Products: {total} | Published: {published}

WORKSPACE
  {slug}  [{type}]  {state}  MCS-{target}  {score}%  {last_validated}
  {slug}  [{type}]  {state}  MCS-{target}  —         {created}
  ...

{if stale > 0}
  {stale} product(s) not validated in 30+ days.
{/if}

COMMANDS
  /create {type}  — Start a new product
  /fill           — Add content to a scaffold
  /validate       — Check quality
  /package        — Bundle for publishing
  /publish        — Ship to marketplace
  /map            — Extract domain knowledge
  /test           — Sandbox test
  /help           — Full command reference
```

### State Display Rules

| State | Display | Color Hint |
|-------|---------|------------|
| scaffold | `scaffold` | dim |
| content | `content` | default |
| validated | `validated` | green |
| packaged | `packaged` | cyan |
| published | `published vX.Y.Z` | gold |
| stale | append ` (stale)` | warning |

---

## Anti-Patterns

1. **Verbose status** — Keep it compact. One line per product. No essays.
2. **Stale data** — Always read fresh from files. Never cache.
3. **Missing files** — If STATE.yaml or creator.yaml missing, say so clearly and suggest /onboard.
4. **Empty workspace** — If no products, show: "Workspace empty. Run /create to start your first product."
5. **Broken meta** — If .meta.yaml is malformed, show product with `[error]` state, don't crash.
