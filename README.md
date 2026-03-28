# MyClaude Studio Engine

> The world's most advanced Claude Code creation studio.
> A self-contained meta-system that prints structural DNA into everything it creates.
> Free. Open Source. State-of-the-art. Made in Brazil.

---

## What It Is

MyClaude Studio Engine is a **Claude Code-native system** — a repository that transforms any Claude Code session into a professional creation studio. It is the creative motor of the MyClaude ecosystem.

**Mental model:** "The forge where world-class Claude Code products are born."

**What it feels like:**
- **Empowered** — "I have everything I need"
- **Elevated** — "Everything I create has structural DNA I couldn't achieve alone"
- **Connected** — "I can validate, package, and ship without leaving Claude Code"

**What it is NOT:**
- NOT a scaffolder (it's intelligence + creation + validation + publishing)
- NOT limited to developers (adapts to any creator persona)
- NOT dependent on the MyClaude marketplace (also supports Anthropic plugin system)

---

## Prerequisites

| Requirement | Install |
|-------------|---------|
| Claude Code | [claude.ai/download](https://claude.ai/download) |
| MyClaude CLI | `npm i -g @myclaude-cli/cli` |
| MyClaude account | [myclaude.sh](https://myclaude.sh) |

---

## Quick Start

```bash
# 1. Clone the Engine
git clone https://github.com/l0z4n0-a1/myclaude-studio-engine.git
cd myclaude-studio-engine

# 2. Open in Claude Code
claude

# 3. Set up your creator profile (~3 minutes)
/onboard

# 4. Map your domain knowledge (optional but recommended)
/map

# 5. Create your first product
/create skill

# 6. Fill content with guided expertise extraction
/fill

# 7. Validate quality
/validate

# 8. Package and publish
/package
/publish
```

---

## Commands (10)

### Creation

| Command | Description |
|---------|-------------|
| `/onboard` | Set up creator profile (creator.yaml) |
| `/map [topic]` | Extract and structure domain knowledge |
| `/create [type]` | Scaffold a new product (9 types) |
| `/fill [slug]` | Guide content filling for a scaffold |

### Quality

| Command | Description |
|---------|-------------|
| `/validate [--level=N]` | Run MCS quality validation (7-stage DNA pipeline) |
| `/test [slug]` | Sandbox test against sample inputs (worktree isolation) |

### Shipping

| Command | Description |
|---------|-------------|
| `/package [slug]` | Bundle product (vault.yaml + plugin.json) |
| `/publish [slug]` | Ship to myclaude.sh via CLI |

### Utility

| Command | Description |
|---------|-------------|
| `/status` | Dashboard: engine, workspace, products |
| `/help` | Full command reference |

---

## Editions

| Feature | LITE (free) | PRO (marketplace) |
|---------|------------|-------------------|
| 10 core skills | Yes | Yes |
| MCS-1 + MCS-2 validation | Yes | Yes |
| MCS-3 validation (agent-assisted) | — | Yes |
| 5 specialist agents | — | Yes |
| Market intelligence | — | Yes |
| Decision logging | — | Yes |

PRO installs INTO LITE via the marketplace (recursive). Detection: glob `.claude/skills/forge-master/`.

---

## Structural DNA (18 Patterns)

Every product created by the Engine inherits structural DNA — 18 patterns extracted from production systems:

| Tier | Patterns | Required For |
|------|----------|-------------|
| **Tier 1** (6) | Activation Protocol, Anti-Pattern Guard, Progressive Disclosure, Quality Gate, Self-Documentation, Graceful Degradation | MCS-1 (all products) |
| **Tier 2** (7) | Question System, Confidence Signaling, Pre-Execution Gate, State Persistence, Testability, Composability, Hook Integration | MCS-2 |
| **Tier 3** (5) | Orchestrate Don't Execute, Handoff Spec, Socratic Pressure, Compound Memory, Subagent Isolation | MCS-3 |

Full documentation: `structural-dna.md`

---

## MCS Quality System

| Level | Score | What It Proves | Badge |
|-------|-------|----------------|-------|
| **MCS-1** | >= 75% | Functional, documented, no broken refs | Muted |
| **MCS-2** | >= 85% | Demonstrates craft and professionalism | Cyan |
| **MCS-3** | >= 92% | State-of-the-art structural DNA | Gold |

Scoring: `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`

---

## Product Categories (9)

| Category | Type Key | Install Target |
|----------|----------|---------------|
| Skills | `skill` | `.claude/skills/{slug}/` |
| Agents | `agent` | `.claude/skills/{slug}/` |
| Squads | `squad` | `.claude/skills/{slug}/` |
| Workflows | `workflow` | `.claude/skills/{slug}/` |
| Design Systems | `design-system` | `myclaude-products/{slug}/` |
| Prompts | `prompt` | `.claude/skills/{slug}/` |
| CLAUDE.md | `claude-md` | `.claude/rules/{slug}.md` |
| Applications | `application` | `myclaude-products/{slug}/` |
| Systems | `system` | `.claude/skills/{slug}/` |

---

## Architecture

```
CLAUDE.md (Boot + Routing)
  |
  +--- .claude/skills/ (10 skills)
  |      /onboard, /map, /create, /fill, /validate
  |      /test, /package, /publish, /status, /help
  |
  +--- product-dna/ (9 files)
  |      DNA requirements per product type
  |
  +--- references/
  |      product-specs/, exemplars/, quality/, best-practices/
  |
  +--- templates/ (9 types)
  |      Rich templates with WHY comments + DNA sections
  |
  +--- workspace/ (active builds)
         {slug}/.meta.yaml, .publish/
```

---

## Ecosystem

```
CREATOR → STUDIO ENGINE → CLI → MARKETPLACE → BUYER
(expertise)   (forge)     (ship)  (discover)   (install)
                |
                └── Also: Anthropic Plugin Marketplace
```

**CONDUIT Protocol** ensures every field flows unbroken from Engine to buyer.

---

## Related

| Link | Description |
|------|-------------|
| [myclaude.sh](https://myclaude.sh) | MyClaude Marketplace |
| [@myclaude-cli/cli](https://www.npmjs.com/package/@myclaude-cli/cli) | MyClaude CLI |
| [PRD v2.0](docs/prd-studio-engine-v2.md) | Full product requirements |

---

## License

MIT License. See [LICENSE](LICENSE).

---

*MyClaude Studio Engine v2.0.0 — The Engine is its own best advertisement.*
