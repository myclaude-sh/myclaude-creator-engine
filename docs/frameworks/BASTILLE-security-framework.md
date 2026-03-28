# BASTILLE — Boundary Architecture for Security, Trust, Integrity & Lifecycle Enforcement

```
ID: FW-ESCUDO+GOVERNANCA-2026-03-28-001
Version: 1.0
Archetype: Escudo do Risco + Espinha Dorsal da Governanca + Bisturi Diagnostico
DNA: Defense-in-Depth | Zero Trust Boundaries | Fail-Safe Defaults
```

> Security framework for the MyClaude ecosystem (Engine + CLI + Marketplace).
> Designed for global-scale distribution under hostile conditions.

---

## 1. Objective

Protect the MyClaude marketplace ecosystem against all classes of attacks — from amateur script injection to sophisticated supply chain compromise — while maintaining creator UX that enables adoption at scale.

**Principle:** Security is a tax. The best tax is invisible. Every control must justify its friction with a proportional risk reduction.

**North Star Metric:** `(products_published_safely / products_attempted) * (1 - false_positive_rate)` — maximize both safety AND throughput.

---

## 2. Scope

### Inside

| System | Responsibility |
|--------|---------------|
| **Engine** (L1) | Product creation, validation, packaging — prompt-based security controls |
| **CLI** (L2) | Authentication, manifest validation, upload, secret scanning |
| **API/Backend** (L3) | Server-side validation, storage, rate limiting, abuse detection |
| **Distribution** (L4) | CDN integrity, install verification, buyer-side warnings |

### Outside

| System | Why Outside |
|--------|------------|
| Claude Code runtime | Anthropic controls execution sandbox, tool permissions, network access |
| Buyer's environment | Post-install behavior is buyer's responsibility |
| Third-party platforms | Cursor, Codex, Gemini CLI have their own security models |

---

## 3. Threat Model (STRIDE-Adapted)

### 3.1 Attack Surface Map

```
                    CREATOR
                       │
           ┌───────────┼───────────┐
           ▼           ▼           ▼
       /onboard     /create     /fill
           │           │           │
           ▼           ▼           ▼
       creator.yaml  scaffold   content
                       │
                       ▼
                   /validate ◄──── L1 GATE (Engine)
                       │
                       ▼
                   /package
                       │
                       ▼
                   .publish/
                       │
                       ▼
               myclaude validate ◄──── L2 GATE (CLI)
                       │
                       ▼
               myclaude publish
                       │
                       ▼
                   API endpoint ◄──── L3 GATE (Server)
                       │
                       ▼
                   CDN / Registry
                       │
                       ▼
               myclaude install ◄──── L4 GATE (Distribution)
                       │
                       ▼
                    BUYER
```

### 3.2 Threat Categories

| ID | Threat | STRIDE | Layer | Severity | Likelihood |
|----|--------|--------|-------|----------|------------|
| T1 | Prompt injection in skill body | Tampering | L4 (buyer-side) | CRITICAL | HIGH |
| T2 | Secrets leaked in published product | Info Disclosure | L1+L2 | CRITICAL | MEDIUM |
| T3 | Path traversal via slug | Elevation | L1 | HIGH | LOW (regex blocks) |
| T4 | Shell command injection via slug | Elevation | L1+L2 | HIGH | LOW (regex blocks) |
| T5 | Malicious YAML in frontmatter | Tampering | L2 | MEDIUM | LOW |
| T6 | WHY comment weaponization | Tampering | L1 | LOW | LOW |
| T7 | Auth token theft/replay | Spoofing | L2 | HIGH | MEDIUM |
| T8 | Race condition on publish | Tampering | L2+L3 | MEDIUM | LOW |
| T9 | Slug squatting | Denial of Service | L3 | MEDIUM | HIGH |
| T10 | Supply chain via Engine deps | Tampering | L1 | HIGH | LOW |
| T11 | Abuse of marketplace (spam, scam) | Repudiation | L3 | HIGH | HIGH |
| T12 | File size bomb (zip bomb, huge files) | Denial of Service | L2+L3 | MEDIUM | MEDIUM |
| T13 | Dependency confusion in products | Tampering | L4 | HIGH | LOW |
| T14 | OAuth/token storage insecurity | Info Disclosure | L2 | HIGH | MEDIUM |

---

## 4. Defense Architecture (5 Layers)

### Layer 1: Engine (Creator-Side, Prompt-Based)

**Principle:** Strict pattern matching. Zero false positives. Block BEFORE packaging.

| Control | Implementation | Status |
|---------|---------------|--------|
| **C1.1 Slug Validation** | Regex `^[a-z0-9][a-z0-9-]{2,39}$` in /create | DONE |
| **C1.2 Secret File Exclusion** | config.yaml `secret_file_patterns`: .env, .pem, .key, credentials.json, .p12 | DONE |
| **C1.3 Secret Content Scan** | config.yaml `secret_content_patterns`: sk-, AKIA, ghp_, PRIVATE KEY, etc. | DONE |
| **C1.4 Placeholder Detection** | config.yaml `placeholder_patterns`: TODO, PLACEHOLDER, lorem ipsum, etc. | DONE |
| **C1.5 WHY Strip + Verify** | /package Step 2 strip + Step 2b two-pass grep verification | DONE |
| **C1.6 Auth Pre-check** | /publish checks `myclaude whoami` before attempting publish | DONE |
| **C1.7 Creator Profile Guard** | 5 skills check creator.yaml existence before proceeding | DONE |
| **C1.8 Circular Ref Detection** | /validate Stage 2 builds reference graph, detects cycles | DONE |
| **C1.9 Description Length Check** | /validate Stage 1 warns if frontmatter description > 250 chars | DONE |
| **C1.10 Sensitive File Block** | /package excludes .env, .pem, .key, credentials from .publish/ | DONE |

**False Positive Mitigation:**
- Secret content patterns use REGEX (not substring) to avoid false matches
- Placeholder patterns check CONTEXT — "TODO" in a code scanner's rules is domain content, not a placeholder
- Description length is a WARNING, not a blocker — creator can override with justification

---

### Layer 2: CLI (Creator-Side, Programmatic)

**Principle:** Heuristic scanning. Low false positives. Block BEFORE upload.

| Control | Implementation | Status | Priority |
|---------|---------------|--------|----------|
| **C2.1 vault.yaml Schema Validation** | CLI validates all required fields, types, ranges | DONE | — |
| **C2.2 Frontmatter Validation** | CLI validates YAML syntax, required fields | DONE | — |
| **C2.3 File Size Limits** | CLI rejects files > 1MB, packages > 10MB | VERIFY | HIGH |
| **C2.4 Secret Scanning** | CLI greps for secret patterns in all files | PARTIAL (missed .env) | CRITICAL |
| **C2.5 License Validation** | CLI validates SPDX identifier | DONE | — |
| **C2.6 Auth Token Security** | JWT storage location, encryption, expiry | AUDIT NEEDED | HIGH |
| **C2.7 HTTPS Enforcement** | All API calls over TLS 1.2+ | VERIFY | CRITICAL |
| **C2.8 Upload Integrity** | SHA-256 checksum of .publish/ contents | VERIFY | HIGH |
| **C2.9 Rate Limiting (client)** | Prevent rapid publish/unpublish cycles | AUDIT NEEDED | MEDIUM |
| **C2.10 YAML Safe Loading** | Use safe YAML parser (no anchors/aliases/execution) | AUDIT NEEDED | HIGH |
| **C2.11 Dependency Audit** | `npm audit` on CLI dependencies | AUDIT NEEDED | HIGH |
| **C2.12 Binary/Executable Detection** | Reject .exe, .dll, .so, .sh files in packages | AUDIT NEEDED | HIGH |

**Action Items for CLI Hardening:**
1. Audit token storage — must use OS keychain (Windows Credential Manager / macOS Keychain), NOT plaintext
2. Add .env detection to secret scan (CRITICAL — tested and confirmed gap)
3. Verify HTTPS pinning on API endpoints
4. Add binary file detection and rejection
5. Run `npm audit` and fix all HIGH/CRITICAL vulnerabilities
6. Verify YAML parser uses `safeLoad` not `load`

---

### Layer 3: API/Backend (Server-Side)

**Principle:** Trust nothing from the client. Re-validate everything. Rate limit aggressively.

| Control | Implementation | Priority |
|---------|---------------|----------|
| **C3.1 Server-Side Manifest Validation** | Re-validate vault.yaml schema (don't trust CLI) | CRITICAL |
| **C3.2 Content Re-scan** | Server-side secret + malware scan on upload | CRITICAL |
| **C3.3 Slug Uniqueness + Squatting Prevention** | Rate limit new slugs per account (max 10/day) | HIGH |
| **C3.4 Auth Verification** | Verify JWT signature, expiry, audience on every request | CRITICAL |
| **C3.5 Rate Limiting** | Publish: 5/hour, Install: 100/hour, Search: 1000/hour | HIGH |
| **C3.6 File Size Enforcement** | Server rejects > 10MB regardless of CLI check | HIGH |
| **C3.7 Content Hash Storage** | Store SHA-256 of every published version | HIGH |
| **C3.8 Abuse Reporting** | API endpoint for community abuse reports | MEDIUM |
| **C3.9 Account Reputation** | Track publish history, flag accounts with flagged products | MEDIUM |
| **C3.10 Immutable Audit Log** | Every publish/unpublish/flag action logged immutably | HIGH |

---

### Layer 4: Distribution (Buyer-Side)

**Principle:** Inform. Never silently install. Buyer has final authority.

| Control | Implementation | Priority |
|---------|---------------|----------|
| **C4.1 Install Integrity Check** | Verify SHA-256 matches server hash on install | CRITICAL |
| **C4.2 Manifest Display** | Show product metadata before install (author, MCS level, files) | HIGH |
| **C4.3 New Author Warning** | "This is a new publisher with no track record" for first-time authors | HIGH |
| **C4.4 Content Review Badge** | "Reviewed" badge for products that passed manual/AI review | MEDIUM |
| **C4.5 Permission Disclosure** | Show what the skill will access (files, network, tools) | HIGH |
| **C4.6 Uninstall Clean** | `myclaude uninstall` removes ALL files, no residue | HIGH |
| **C4.7 Version Pinning** | Install specific versions, don't auto-update without consent | MEDIUM |

---

### Layer 5: Execution (Anthropic-Controlled)

**Controls we rely on but don't implement:**

| Control | Provider | Our Role |
|---------|----------|----------|
| Tool permission prompts | Claude Code | Ensure skills document required tools in frontmatter |
| Sandbox isolation | Claude Code | Use `context: fork` and `isolation: worktree` appropriately |
| Network access control | Claude Code | Document network requirements in skill metadata |
| File system boundaries | Claude Code | Skills specify `paths` in frontmatter when possible |

---

## 5. Scan Architecture

### 5.1 What to Scan, When, How

```
CREATION TIME                  PACKAGE TIME                UPLOAD TIME
(/validate)                    (/package)                  (myclaude publish)
    │                              │                            │
    ├─ Structural files exist      ├─ WHY comments stripped     ├─ vault.yaml schema
    ├─ Placeholders cleared        ├─ WHY verify (grep)        ├─ File sizes
    ├─ References resolve          ├─ Sensitive files excluded  ├─ Secret patterns
    ├─ Circular refs detected      ├─ Manifests generated      ├─ License valid
    ├─ Secret file patterns        ├─ SHA-256 calculated       ├─ Frontmatter valid
    ├─ Secret content patterns     ├─ Re-validate structural   ├─ *** SERVER RE-SCANS ***
    ├─ Description length          │                            │
    └─ DNA compliance              │                            │
                                   │                            │
    DEFENSE DEPTH: ─────────────► DEFENSE DEPTH: ─────────────► DEFENSE DEPTH:
    Pattern match (exact)          File analysis (heuristic)    Server-side (definitive)
```

### 5.2 False Positive Strategy

The #1 killer of security adoption is false positives. Strategy:

| Layer | Strictness | False Positive Rate | Override Mechanism |
|-------|-----------|--------------------|--------------------|
| L1 Engine | EXACT patterns only | < 1% | Context-aware (LLM understands domain content vs placeholder) |
| L2 CLI | Heuristic + pattern | < 5% | `--force` flag with explicit acknowledgment |
| L3 Server | Re-scan + AI review | < 0.1% | Manual appeal process |

**Rules for adding new patterns:**
1. Pattern must have < 2% false positive rate in testing
2. Every pattern needs 3+ real-world test cases (positive AND negative)
3. Domain content exceptions must be documented (e.g., "TODO" in a code scanner)
4. New patterns go through 30-day shadow mode before blocking

### 5.3 Secret Scan Deep Dive

**Engine (L1) — config.yaml patterns:**

```yaml
# File patterns (block from .publish/)
secret_file_patterns:
  - "*.env"           # Environment files
  - "*.pem"           # Certificates
  - "*.key"           # Private keys
  - "*.p12"           # PKCS12 keystores
  - "*.pfx"           # Windows keystores
  - "credentials*.json"
  - "service-account*.json"
  - ".npmrc"          # NPM auth tokens
  - ".pypirc"         # PyPI auth tokens

# Content patterns (grep in all files)
secret_content_patterns:
  - "sk-[a-zA-Z0-9]{20,}"              # OpenAI
  - "AKIA[A-Z0-9]{16}"                 # AWS
  - "ghp_[a-zA-Z0-9]{36}"             # GitHub PAT
  - "glpat-[a-zA-Z0-9]{20}"           # GitLab PAT
  - "xox[bps]-[a-zA-Z0-9-]+"          # Slack
  - "-----BEGIN.*PRIVATE KEY"           # Generic PEM
  - "API_KEY\\s*=\\s*['\"]?[a-zA-Z0-9]" # Generic key assignment
  - "SECRET\\s*=\\s*['\"]?[a-zA-Z0-9]"  # Generic secret assignment
  - "PASSWORD\\s*=\\s*['\"]?[a-zA-Z0-9]" # Generic password
```

**CLI (L2) — should add:**
```
- .env file content parsing (KEY=VALUE detection)
- Base64-encoded secrets (entropy analysis)
- Database connection strings (mongodb://, postgres://)
- Cloud provider tokens (az, gcloud patterns)
```

**Server (L3) — should add:**
```
- AI-based content classification (is this a real secret or documentation?)
- Entropy analysis (high-entropy strings > 40 chars)
- Known-leaked credential database cross-reference
```

---

## 6. Auth & Trust Architecture

### 6.1 Authentication Flow

```
Creator                    CLI                     API
   │                        │                       │
   ├─ myclaude login ──────►│                       │
   │                        ├─ Open browser ───────►│ /auth/login
   │                        │                       ├─ OAuth2 PKCE flow
   │  ◄── Browser callback ─┤                       │
   │                        ├─ Exchange code ──────►│ /auth/token
   │                        │◄── JWT + refresh ─────┤
   │                        ├─ Store in OS keychain  │
   │                        │                       │
   ├─ myclaude publish ───►│                       │
   │                        ├─ Load token from keychain
   │                        ├─ Attach Bearer JWT ──►│ /products/publish
   │                        │                       ├─ Verify JWT signature
   │                        │                       ├─ Check expiry
   │                        │                       ├─ Check scope
   │                        │◄── 200 OK ────────────┤
```

### 6.2 Token Security Requirements

| Requirement | Implementation | Priority |
|-------------|---------------|----------|
| Storage | OS Keychain (NOT plaintext file) | CRITICAL |
| Encryption | AES-256 if keychain unavailable (fallback) | HIGH |
| Expiry | JWT: 1 hour. Refresh: 30 days. | HIGH |
| Refresh rotation | New refresh token on each use (rotation) | HIGH |
| Revocation | Server-side revocation list checked on each API call | MEDIUM |
| Scope | Separate scopes: `publish`, `install`, `manage` | MEDIUM |
| MFA | Optional MFA for publish actions (TOTP) | MEDIUM |

### 6.3 Trust Levels

```
NEW ACCOUNT ──► VERIFIED ──► TRUSTED ──► CERTIFIED
(0 publishes)   (email+1pub)  (5+ pubs,    (manual review,
                              0 flags)      badge earned)

Restrictions by level:
  NEW:       1 publish/day, max 5MB, manual review queue
  VERIFIED:  5 publish/day, max 10MB, fast-track review
  TRUSTED:   20 publish/day, max 20MB, auto-approve
  CERTIFIED: Unlimited, 50MB, featured placement
```

---

## 7. Incident Response Protocol

### 7.1 Severity Classification

| Severity | Definition | Response Time | Example |
|----------|-----------|---------------|---------|
| P0 CRITICAL | Active exploitation, data breach | < 1 hour | Secrets leaked in published product |
| P1 HIGH | Vulnerability discovered, no active exploit | < 24 hours | Auth bypass found |
| P2 MEDIUM | Potential vulnerability, limited impact | < 1 week | False positive in scan causes friction |
| P3 LOW | Improvement opportunity, no immediate risk | Next sprint | New pattern to add to scan |

### 7.2 Response Playbooks

**P0: Secret Leaked in Published Product**
1. CONTAIN: Unpublish product immediately (API admin action)
2. NOTIFY: Email creator with specific secret found
3. ROTATE: Advise creator to rotate all exposed credentials
4. SCAN: Re-scan all products from same creator
5. POSTMORTEM: Why did L1+L2+L3 all miss it? Add new pattern.

**P0: Malicious Product Discovered**
1. CONTAIN: Unpublish + flag account
2. NOTIFY: All buyers who installed (via CLI update mechanism)
3. REMOVE: Push uninstall advisory
4. ANALYZE: What made it past review? Update L3 detection.
5. COMMUNICATE: Public advisory if > 100 installs

**P1: Auth Token Compromise**
1. REVOKE: Invalidate all tokens for affected account
2. FORCE: Password reset
3. AUDIT: Review all recent publish actions from account
4. HARDEN: Require MFA for future publishes

---

## 8. Metrics & Monitoring

### 8.1 Security KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| False positive rate (L1) | < 1% | `secrets_flagged_incorrectly / total_flagged` |
| False positive rate (L2) | < 5% | `validate_false_fails / total_validates` |
| Time to detect malicious product | < 24 hours | `report_time - publish_time` |
| Secret leak rate | 0% | `products_with_leaked_secrets / total_published` |
| Auth token theft incidents | 0/quarter | Incident count |
| Mean time to contain (P0) | < 1 hour | `contain_time - detect_time` |
| Creator friction score | > 8/10 | Survey: "How easy was publishing?" |

### 8.2 Continuous Monitoring

```
REAL-TIME:
  - Failed auth attempts per account (threshold: 5/min → lock)
  - Publish rate per account (threshold: trust level limits)
  - API error rate (threshold: > 5% → alert)

DAILY:
  - New secret patterns in published products (re-scan latest 100)
  - npm audit on CLI dependencies
  - Certificate expiry checks

WEEKLY:
  - Full re-scan of all published products with updated patterns
  - False positive review (adjust patterns)
  - Trust level recalculation for all accounts

MONTHLY:
  - Penetration test on API endpoints
  - CLI dependency update + audit
  - Threat model review (new attack vectors?)
```

---

## 9. Anti-Patterns

| Anti-Pattern | Symptom | Prevention |
|-------------|---------|------------|
| **Security Theater** | Lots of checks, no real protection | Every control must have a tested attack it blocks |
| **Castle-and-Moat** | Hard perimeter, soft interior | Defense-in-depth: every layer re-validates |
| **Alert Fatigue** | So many warnings creators ignore them all | Tiered: ERROR (blocks), WARN (advises), INFO (logs) |
| **Security by Obscurity** | "They won't figure it out" | Assume attacker has source code (it's open source) |
| **Checkbox Compliance** | "We have a security framework" (unused) | Metrics prove it works. Monthly drill. |
| **One-Size-Fits-All** | Same checks for all product types | Risk-proportional: skills need more scrutiny than prompts |
| **Paranoid Lockdown** | Block everything, kill adoption | False positive rate < 1%. Override with `--force` + log. |

---

## 10. Implementation Roadmap

### Phase 1: NOW (Engine hardened) — DONE

All L1 controls implemented:
- [x] C1.1-C1.10 in Engine skills
- [x] Secrets scan in config.yaml
- [x] OBSIDIAN audit + fixes + Kairo meta-audit

### Phase 2: NEXT (CLI hardening) — 1-2 sessions

- [ ] Audit CLI source code for C2.1-C2.12
- [ ] Fix C2.4 secret scan gap (.env detection)
- [ ] Audit token storage (C2.6)
- [ ] Verify HTTPS enforcement (C2.7)
- [ ] Run npm audit (C2.11)
- [ ] Add binary detection (C2.12)

### Phase 3: BACKEND (Server-side) — 2-3 sessions

- [ ] Implement C3.1-C3.10 in API
- [ ] Server-side re-scan on upload
- [ ] Rate limiting and trust levels
- [ ] Abuse reporting endpoint
- [ ] Immutable audit log

### Phase 4: DISTRIBUTION (Buyer-side) — 1 session

- [ ] Implement C4.1-C4.7 in CLI install flow
- [ ] Hash verification on install
- [ ] New author warning
- [ ] Permission disclosure

### Phase 5: CONTINUOUS — Ongoing

- [ ] Weekly re-scan with updated patterns
- [ ] Monthly penetration testing
- [ ] Quarterly threat model review
- [ ] Community bug bounty program

---

## 11. Quick Start Guide

**For the Engine team (us):**
1. Engine L1 controls are DONE — no action needed
2. Next: open `D:\vault-marketplace\packages\cli\` and audit against C2.1-C2.12
3. Every new pattern added to config.yaml must have 3 test cases
4. Run `/validate` on your own products before publishing — eat your own dogfood

**For the CLI team (us):**
1. Prioritize: C2.4 (secret scan), C2.6 (token storage), C2.7 (HTTPS), C2.11 (npm audit)
2. Every CLI command that takes user input must validate against injection
3. Add `--security-report` flag to `myclaude validate` for detailed scan output

**For future marketplace reviewers:**
1. Products from NEW accounts go through manual review queue
2. Flag: products that reference external URLs, request network access, or include executable code
3. Auto-reject: products with detected secrets, binaries, or > 50MB

---

## 12. DNA

| Element | Value |
|---------|-------|
| **Dominant Principle** | Defense-in-Depth: no single layer is the last line of defense |
| **Base Archetype** | Escudo do Risco (threat anticipation) + Espinha Dorsal da Governanca (enforcement) |
| **Central Trade-off** | Security strictness vs. creator friction. Resolve by: strict patterns (low FP) at L1, heuristics at L2, human judgment at L3 |
| **Falsification Test** | "Can a determined attacker publish a malicious product?" If yes at ANY layer → add control |
| **Kill Signal** | If false positive rate > 5% at any layer → loosen patterns before creators abandon the platform |

---

*BASTILLE v1.0 — Forged by ATHENA on 2026-03-28*
*For: MyClaude Studio Engine + CLI + Marketplace ecosystem*
*Threat model: Global-scale distribution under hostile conditions*
