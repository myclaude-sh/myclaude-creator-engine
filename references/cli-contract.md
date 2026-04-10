# CLI ↔ Engine Contract

> Unified contract for all `myclaude` CLI invocations across Studio Engine v3.0.0.

## Architecture

The CLI (`@myclaude-cli/cli`) is the primary channel between the Engine and the
marketplace. Engine skills invoke CLI commands via `Bash("myclaude ...")`. This
works reliably and is how all 31 commands are consumed today.

The CLI also exposes an MCP server (`myclaude setup-mcp`) with 5 tools
(vault_search, vault_info, vault_install, vault_list, vault_update). When
configured, Claude can call these tools directly without shell commands. This
is a **complementary channel** — not a replacement. Skills should continue
using CLI commands as documented below. MCP availability is a bonus.

## Requirements

| Property | Value |
|----------|-------|
| CLI package | `@myclaude-cli/cli` |
| Install | `npm i -g @myclaude-cli/cli` |
| Minimum version | `0.9.0` |
| Engine version | `3.0.0` |

## Version Detection

```bash
myclaude --version 2>/dev/null
```

If absent or below minimum: degrade gracefully per fallback column below.

---

## Command Map

Every CLI invocation across all Engine skills, organized by command.

### Authentication

| Command | Skills | Phase | Output | Fallback |
|---------|--------|-------|--------|----------|
| `myclaude whoami` | /onboard, /publish | onboard:6c, publish:pre-flight | text (username or error) | Skip marketplace features; prompt `myclaude login` |
| `myclaude login` | /onboard, /publish | guided (user-initiated) | interactive | Manual auth at myclaude.sh; block publish |

### Validation

| Command | Skills | Phase | Output | Fallback |
|---------|--------|-------|--------|----------|
| `myclaude validate --json` | /validate (stage 6), /publish | validate:cli-preflight, publish:step-5 | JSON `{ valid, errors[], warnings[] }` | Skip stage 6; warn "CLI not installed" |
| `myclaude doctor --json` | /validate (stage 6) | validate:health-check | JSON `{ score }` | Skip; no marketplace health data |

### Publishing

| Command | Skills | Phase | Output | Fallback |
|---------|--------|-------|--------|----------|
| `myclaude publish` | /publish | publish:step-6 | interactive + text confirmation | Block — cannot publish without CLI. Show manual upload URL: `myclaude.sh/publish` |

### Marketplace Search

| Command | Skills | Phase | Output | Fallback |
|---------|--------|-------|--------|----------|
| `myclaude search "{query}" --json` | /explore, /create, /think, /onboard, /publish | explore:discovery, create:1.5, think:research, onboard:6c-hints, publish:post-publish | JSON array of products | Skip silently; no marketplace context |
| `myclaude search --category {cat} --sort {sort} --limit {n} --json` | /explore, /package, /publish | explore:category-browse, package:pricing-scan, publish:competitive | JSON array | Skip silently |
| `myclaude trending --json` | /explore, /think | explore:trending, think:research | JSON array | Skip silently |
| `myclaude workspace --recommend --json` | /explore | explore:recommendations | JSON array | Skip silently |

### Analytics & Profile

| Command | Skills | Phase | Output | Fallback |
|---------|--------|-------|--------|----------|
| `myclaude stats {slug} --json` | /status | status:enrichment | JSON `{ installs, downloads, rating }` | Show "—" for marketplace metrics |
| `myclaude stats --json` | /status | status:aggregate | JSON | Skip marketplace section |
| `myclaude my-products --json` | /status | status:marketplace-intelligence | JSON array | Skip marketplace section |
| `myclaude notifications --json` | /status | status:activity | JSON array | Skip notifications |
| `myclaude profile pull --json` | /status, /publish | status:level, publish:post-publish | JSON `{ level, xp }` | Skip level display |
| `myclaude profile sync` | /onboard | onboard:6c | text | Skip; manual sync later |

### Payments

| Command | Skills | Phase | Output | Fallback |
|---------|--------|-------|--------|----------|
| `myclaude stripe status` | /onboard, /package | onboard:6c, package:paid-products | text (connected/not) | Warn; block paid product packaging |
| `myclaude stripe connect` | /onboard, /package | guided (user-initiated) | interactive | Direct to myclaude.sh Stripe setup |

### Diagnostics

| Command | Skills | Phase | Output | Fallback |
|---------|--------|-------|--------|----------|
| `myclaude --version` | /explore | explore:activation-step-2 | text (version string) | Degrade to offline mode; show install instructions |

### Setup

| Command | Skills | Phase | Output | Fallback |
|---------|--------|-------|--------|----------|
| `myclaude setup-mcp` | /onboard | onboard:6c | text | Skip with pro-tip message |

### Product Management

| Command | Skills | Phase | Output | Fallback |
|---------|--------|-------|--------|----------|
| `myclaude install {slug}` | /explore, /create (README) | explore:install-action, create:readme-template | interactive | Manual install instructions |
| `myclaude update --all` | utility | user-initiated | text | Manual per-product update |
| `myclaude list` | utility | user-initiated | text | Glob `.claude/skills/*/` |
| `myclaude info {slug}` | utility | user-initiated | text | Direct to myclaude.sh/p/{slug} |

---

## Auth Flow

### When is `myclaude login` needed?

1. **Before `/publish`** — mandatory. Detected by `myclaude whoami` returning non-zero or "not logged in".
2. **During `/onboard` phase 6c** — optional but recommended. Enables marketplace features.
3. **Before any write operation** to the marketplace (publish, profile sync).

### Detection Pattern

```bash
AUTH_STATUS=$(myclaude whoami 2>/dev/null)
if [ $? -ne 0 ] || echo "$AUTH_STATUS" | grep -qi "not logged"; then
  # Not authenticated
  echo "Run: myclaude login"
fi
```

### Stripe Flow

Required when: `vault.yaml` contains `pricing.model` other than `"free"`.

Detection:
```bash
STRIPE=$(myclaude stripe status 2>/dev/null)
if [ $? -ne 0 ] || echo "$STRIPE" | grep -qi "not connected"; then
  # Stripe not connected — block paid product packaging
  echo "Run: myclaude stripe connect"
fi
```

---

## Error Handling — Unified Pattern

All CLI invocations follow this pattern:

```bash
# Standard invocation template
RESULT=$(myclaude <command> --json 2>/dev/null)
EXIT_CODE=$?
```

### Error Cases

| Condition | Detection | Engine Response |
|-----------|-----------|-----------------|
| CLI not installed | `which myclaude` fails | Degrade gracefully; show install instructions once per session |
| CLI too old | Version < 0.9.0 | Warn "Update CLI: `npm i -g @myclaude-cli/cli`"; degrade |
| Auth expired | Exit code non-zero + "unauthorized"/"expired" in stderr | Prompt `myclaude login`; do not retry |
| Network down | Exit code non-zero + "ENOTFOUND"/"ETIMEDOUT" in stderr | Skip marketplace features; continue offline |
| CLI timeout | No response within 15s | Kill process; skip with warning |
| Rate limited | 429 in output | Back off; skip marketplace features for this session |
| Invalid JSON | `--json` flag but output is not parseable | Treat as CLI absent; warn |

### Unified Handler (pseudocode)

```bash
cli_invoke() {
  local cmd="$1"
  local timeout="${2:-15}"

  if ! command -v myclaude &>/dev/null; then
    echo '{"_cli_error": "not_installed"}'
    return 1
  fi

  local result
  result=$(timeout "$timeout" myclaude $cmd 2>/dev/null)
  local rc=$?

  if [ $rc -ne 0 ]; then
    echo '{"_cli_error": "command_failed", "_exit_code": '$rc'}'
    return 1
  fi

  echo "$result"
}
```

### Severity Levels

Default severity per command. Skills may **escalate** (never downgrade) based on context — see notes.

| Severity | Commands | Behavior on failure |
|----------|----------|---------------------|
| **Blocking** | `publish`, `validate --json` (during /publish), `whoami` (during /publish) | Stop pipeline; show fix instructions |
| **Warning** | `stripe status`, `whoami` (during /onboard), `doctor --json`, `profile sync`, `setup-mcp` | Warn; allow pipeline to continue |
| **Silent skip** | All `search`, `trending`, `stats`, `my-products`, `notifications`, `profile pull`, `workspace --recommend`, `--version`, `install {slug}` | Skip without user-visible warning |

**Context-dependent escalation rules:**
- `whoami` is Warning by default but **Blocking during /publish** — authentication is a publish prerequisite
- `stripe status` is Warning by default but **Blocking in /package when product price > 0** — paid products require Stripe
- `stripe status` is **Silent-skip in /package when product price == 0** — irrelevant for free products
- `install {slug}` is Silent-skip but shows manual install instructions as fallback (not a warning — the user still gets the path)
- `validate --json` is Warning in /validate Stage 6 (advisory) but **Blocking during /publish** Step 3 (publish gate)

---

## Conventions

1. **All marketplace queries append `2>/dev/null`** — stderr is never shown to the creator.
2. **All marketplace queries append `--json`** — structured output for parsing.
3. **Working directory for validate/publish**: `cd workspace/{slug}/.publish` before invocation.
4. **No CLI calls during /fill, /map, /import, /help, /test** — these are content-only or internal-only skills.
5. **Scout declares `Bash(myclaude *)` permission** but delegates marketplace queries to /explore.
6. **First-product guard** (/create step 1.5): skip marketplace scan for first-time creators.
7. **Think uses CLI conditionally** — only for product strategy questions (search + trending), both silent-skip.
