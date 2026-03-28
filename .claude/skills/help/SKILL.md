---
name: help
description: >-
  Show all available Studio Engine commands with descriptions. Displays
  command list organized by category, current edition features, and quick
  start guide. Use when the creator asks "help", "commands", "what can I do",
  or "how does this work".
---

# Help

Display all available commands and quick start guide.

---

## Core Instructions

Detect edition first (glob `.claude/skills/forge-master/SKILL.md`), then display:

```
MyClaude Studio Engine — Command Reference

CREATION
  /onboard          Set up creator profile (creator.yaml)
  /map [topic]      Extract and structure domain knowledge
  /create [type]    Scaffold a new product (9 types available)
  /fill [slug]      Guide content filling for a scaffolded product

QUALITY
  /validate [opts]  Run MCS quality validation
                    --level=1|2|3  --fix  --batch
  /test [slug]      Sandbox test against sample inputs

SHIPPING
  /package [slug]   Bundle product (vault.yaml + plugin.json)
  /publish [slug]   Ship to myclaude.sh marketplace

UTILITY
  /status           Dashboard: engine, workspace, products
  /help             This command reference

{if PRO}
PRO AGENTS (active)
  Forge Master      Orchestrates multi-agent creation flows
  Domain Cartographer  Deep domain analysis for /map
  Product Architect    Architecture decisions for /create
  Quality Sentinel     MCS-2/3 deep review for /validate
  Market Scout         Marketplace intelligence for /publish
{/if}

QUICK START
  1. /onboard         → Set up your profile
  2. /create skill    → Scaffold your first product
  3. /fill            → Add your expertise
  4. /validate        → Check quality
  5. /package         → Bundle for publishing
  6. /publish         → Ship it!

Learn more: https://myclaude.sh/docs/studio-engine
```

---

## Anti-Patterns

1. **Wall of text** — Keep it scannable. One line per command.
2. **Stale info** — Always detect edition dynamically, don't hardcode.
3. **Missing commands** — If new skills exist in .claude/skills/ that aren't listed, mention them.
