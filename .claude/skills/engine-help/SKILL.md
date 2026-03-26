---
name: engine-help
description: >-
  List all available myClaude Creator Engine commands with descriptions and usage.
  Use when the creator asks "what can I do", "help", "list commands", or "what commands
  are available".
---

# Engine Help

Display all available Creator Engine commands, organized by function.

## Commands

### Creation
| Command | Description |
|---------|-------------|
| `/onboard` | Set up your creator profile (~3 min guided conversation) |
| `/create [type]` | Scaffold new product (skill, agent, squad, workflow, ds, prompt, claude-md, app, system) |
| `/create-content` | Guide content filling after scaffold — extracts your expertise section by section |

### Quality
| Command | Description |
|---------|-------------|
| `/validate` | Run MCS-1 validation on a product |
| `/validate --level=2` | Run MCS-2 validation (includes anti-commodity gate) |
| `/validate --level=3` | Run MCS-3 validation (agent-assisted deep review) |
| `/validate --fix` | Auto-fix structural issues |
| `/validate --batch` | Validate all products in workspace |
| `/test` | Sandbox test product against sample inputs |
| `/quality-review` | Deep MCS-3 quality audit with expert agent |
| `/differentiate` | Anti-commodity coaching session |

### Publishing
| Command | Description |
|---------|-------------|
| `/package` | Strip guidance, generate vault.yaml, stage .publish/ |
| `/publish` | Full publish workflow to myclaude.sh |

### Shortcuts
| Command | Description |
|---------|-------------|
| `/quick-skill` | Create + validate + package + publish in one flow |
| `/quick-publish` | Validate + package + publish for existing product |

### Utility
| Command | Description |
|---------|-------------|
| `/engine-status` | Show profile, workspace, and engine state |
| `/engine-help` | This help listing |

### Marketplace (via myClaude CLI)
| Command | Description |
|---------|-------------|
| `myclaude search <query>` | Search marketplace products |
| `myclaude install <slug>` | Install a product |
| `myclaude list` | List installed products |
| `myclaude login` | Authenticate with myClaude |
