### VALIDATION PIPELINE (7 Stages + 3 sub-stages — aligned with config.yaml)

Execute stages in order. Blocking stages stop on failure. Non-blocking stages report but continue.

**Stage 1 — STRUCTURAL** (blocking)

For each issue found, classify:
- `[BLOCKING]` — Must fix before proceeding. Cannot advance state.
- `[WARNING]` — Can proceed with explicit risk acceptance. Creator must confirm.

Glob: do all required files for the product type exist?
Load `product-dna/{type}.yaml` → `required_files` and `config.yaml` → `routing.{type}.required_files`.
**Bundle exception:** If type=bundle, skip primary file check. Instead check: vault.yaml exists with `bundle.includes[]` array AND `bundle.includes.length >= 2` (a bundle with fewer than 2 products has no curation value — fail with: "Bundle must include at least 2 products. Found: {N}. Add more products to vault.yaml → bundle.includes[] then re-run /validate.").
Score: `files_found / files_expected`

Frontmatter check: read the primary file's YAML frontmatter. Verify `description` field is <= 250 characters. If over, report as warning with character count: "Frontmatter description is {N} chars (recommended: <= 250). Trim for marketplace compatibility."

**Stage 2 — INTEGRITY** (blocking)

For each issue found, classify:
- `[BLOCKING]` — Must fix before proceeding. Cannot advance state.
- `[WARNING]` — Can proceed with explicit risk acceptance. Creator must confirm.

Grep: no placeholder content (`config.yaml` → `placeholder_patterns`: TODO, PLACEHOLDER, lorem ipsum, etc.)
**Template variable check:** Grep all product files for `\{\{[A-Za-z_][A-Za-z0-9_-]*\}\}` pattern. Any match = `[BLOCKING]` integrity failure: "Unfilled template variable `{match}` found in {file}:{line}. This was not replaced during /create scaffold generation. Either fill it manually or report this as a bug in /create."
Ref check: every file path referenced in .md files actually exists on disk.
Circular reference check — deterministic DFS algorithm:
  1. Build adjacency list: For each .md file in product directory, grep for file path references (patterns: `references/`, `agents/`, `skills/`, `workflows/`, `config/`, any `.md` or `.yaml` path). Each reference = directed edge from current file to referenced file.
  2. Run iterative DFS with 3-color marking (WHITE=unvisited, GRAY=in-stack, BLACK=done):
     - For each WHITE node, push to stack and mark GRAY
     - For each neighbor: if GRAY → cycle detected (back edge). Record the cycle path from stack
     - When all neighbors processed, mark BLACK
  3. If any cycle detected, report as integrity failure: "Circular reference detected: {file_A} → {file_B} → ... → {file_A}. Break the cycle by removing one reference direction, then re-run /validate."
  4. Optimization: Skip files in node_modules/, .git/, .publish/ directories
YAML/JSON parse: no syntax errors in metadata files.
**Hooks security scan:** If type=hooks, parse `hooks.json` (must be valid JSON — report parse failure as blocking). Check all `command` fields in handler scripts for: shell injection (`;`, `&&`, `||`, backticks, `$()`), `eval`, `source`/`.` commands, unquoted single `|`, `base64` decode-and-execute, `curl|sh`/`wget|sh`, `python -c`/`node -e` inline execution, file system access outside project scope, and network calls without README documentation.
**Statusline script check:** If type=statusline, validate `statusline.sh`:
  1. File starts with a shebang line (`#!/usr/bin/env bash` or `#!/bin/bash`) — if missing, report blocking failure: "statusline.sh must start with a shebang (#!/usr/bin/env bash). Add it as the first line, then re-run /validate."
  2. File contains `cat` reading from stdin (pattern: `$(cat)` or `read` from stdin) — if missing, report warning: "statusline.sh should read JSON from stdin via INPUT=\$(cat). Add stdin reading to enable live context injection."
  3. File contains `printf` or `echo` writing to stdout — if missing, report blocking failure: "statusline.sh must output to stdout. Add a printf or echo statement, then re-run /validate."
  4. `settings-fragment.json` is valid JSON with a `statusLine` key containing `type` and `command` fields — if invalid, report blocking failure: "settings-fragment.json must be valid JSON with statusLine.type and statusLine.command. Fix the JSON syntax or missing fields, then re-run /validate."
**@include depth check:** [SOURCE: claudemd.ts:537 — MAX_INCLUDE_DEPTH = 5]
For products using @include directives (grep for lines starting with `@` followed by a path — pattern `^@[a-zA-Z0-9./~_]`, excluding lines inside code blocks):
1. Build @include tree by following each @path reference recursively
2. Measure maximum depth of the tree
- Depth <= 3: PASS — "@ include depth: {N} (within safe range)."
- Depth 4-5: WARNING — "@include depth is {N}. Claude Code's hard limit is 5. Files at level 6+ are silently ignored — no error, no warning, content simply doesn't load. Consider flattening."
- Depth > 5: BLOCKING — "@include depth is {N} — exceeds Claude Code's MAX_INCLUDE_DEPTH of 5. Files at depth {N} will NEVER load. Flatten your @include tree to depth ≤5."

**External @include detection:** [SOURCE: claudemd.ts:667-670, 799-801]
For products using @include directives:
1. Detect @includes with absolute paths (`@/path`), home paths (`@~/path`), or paths that resolve outside the product directory
- If found: WARNING — "External @include detected: '{path}'. When a buyer installs this product, they will see an approval prompt for external @includes. This adds friction. Consider copying the referenced file into your product's references/ directory instead."
- If all @includes are relative within product dir: PASS (no friction for buyers)
This check is non-blocking (coaching) — external @includes are valid, just add UX friction.

**Binary @include detection:** [SOURCE: claudemd.ts:96-227 — TEXT_FILE_EXTENSIONS whitelist]
For products using @include directives:
1. Check file extension of each @include target
- If target has a binary extension (.pdf, .png, .jpg, .zip, .docx, etc.): WARNING — "@include target '{path}' is a binary file. Claude Code only allows text files in @include (~100 extensions: .md, .yaml, .json, .ts, .py, etc.). Binary files are silently ignored — the content won't load."
This check is non-blocking but catches a common creator mistake.

**Scope integrity check:** Compare filled sections against the scaffold template (`templates/{type}/`). For each section, count content words. Flag sections where content is less than 20% of the template's guidance text length as "potentially reduced scope" (coaching, not blocking). Report: "Section '{name}' has {N} words vs {M} expected minimum. Content may be thin — consider expanding."
Secrets scan: check for sensitive file patterns (`.env`, `*.pem`, `*.key`, `credentials*.json`, `*.p12`) and content patterns (`sk-`, `AKIA`, `ghp_`, `glpat-`, `xox[bps]-`, `-----BEGIN.*PRIVATE KEY`, API_KEY=, SECRET=, PASSWORD=). If any match found, report as blocking integrity failure: "Potential secret detected in {file}:{line}. Remove the secret, add the file to .gitignore if needed, then re-run /validate."
**Supply chain threat scan:** [SOURCE: competitive-intelligence S97 — references/quality/known-threats.yaml]
Load `references/quality/known-threats.yaml` PROGRESSIVELY — read only the section needed for each check (dangerous_patterns for check 1, iocs for check 2, etc.). Do NOT load the entire file at once. Use the **Grep tool** (ripgrep syntax) for pattern matching against product files. Patterns in the YAML are ripgrep-compatible regex. Execute these checks in order:

1. **Dangerous pattern scan (BLOCKING/WARNING):** For ALL files in the product, grep for each pattern in `dangerous_patterns`. Match action per entry:
   - BLOCKING patterns (enableAllProjectMcpServers, curl|sh, wget|sh, base64|sh): Report as blocking integrity failure — "CRITICAL: Dangerous pattern '{pattern}' detected in {file}:{line}. Reason: {reason}. This pattern is associated with known attack vectors and MUST be removed."
   - WARNING patterns (eval, shell:true spawn, $(curl): Report as warning — "Security concern: '{pattern}' in {file}:{line}. {reason}. Document why this is necessary or use a safer alternative."
   - COACHING patterns (non-standard env access): Report as coaching — "'{pattern}' in {file}:{line} accesses non-standard environment variables. If this reads secrets, use Claude Code's native secret management instead."

2. **IOC scan (BLOCKING):** Grep ALL product files for IPs and domains in `iocs`. ANY match = blocking failure — "CRITICAL: Known malicious indicator detected in {file}:{line}. IP/domain '{match}' is associated with {campaign}. Product cannot be published with IOCs present."

3. **Malicious prefix scan (WARNING):** Grep product files (including README, package.json, vault.yaml) for dependency names matching `malicious_prefixes[].pattern`. Match = WARNING — "Dependency name matches known malicious campaign pattern '{pattern}' ({campaign}: {payload}). Verify this is a LEGITIMATE package, not a typosquat. If legitimate, document the verification in README."

4. **Vulnerable MCP server scan (WARNING):** Grep product files for MCP server names in `vulnerable_mcp_servers`. Match = WARNING — "MCP server '{name}' has known vulnerability ({cve}). Minimum safe version: {min_safe_version}. Verify your product pins a safe version or document the risk acceptance."

5. **Malicious author scan (WARNING):** If product references external skill/package authors, check against `malicious_authors[].id`. Match = WARNING — "Author '{id}' is flagged as malicious ({threat}). Source: {source}. Do NOT use products from this author."

6. **External dependency documentation check (COACHING):** Grep primary file + README for MCP server references (patterns: `mcp__`, `mcp-server`, `mcp_config`, `npx -y`, `pip install`). If found without explicit documentation (author, version, security note): COACHING — "External dependency '{dep}' referenced but not documented in README. Add a 'Dependencies' section with: name, author, pinned version, and purpose."

7. **Network call documentation check (COACHING):** For type=hooks, grep handler scripts for network calls (curl, wget, fetch, http, https). If found without README documentation: COACHING — "Hook makes network calls to '{pattern}'. Document the endpoint, purpose, and data transmitted in README."

This scan runs AUTOMATICALLY for all product types. Items 1-2 are blocking. Items 3-5 are warnings. Items 6-7 are coaching.

**Implementation substance check:** [SOURCE: competitive-intelligence S97 — anti-hallucination pattern]
For MCS-2+ products, assess whether the product has genuine implementation beyond scaffold boilerplate:
1. Count unique domain-specific words in primary file (exclude common English words and template variables)
2. If domain-specific word count < 30: WARNING — "Product may lack substantive domain expertise. Template structure is present but content appears thin. Consider: Does this product encode real knowledge a buyer couldn't get from a generic prompt?"
3. Check references/ directory: if exists, verify at least 1 file has >50 lines of domain content (not just headers). If all reference files are <10 lines: WARNING — "references/ directory exists but files appear to be stubs. Progressive disclosure (D3) requires substantive reference content."
This check is non-blocking (coaching) — encourages genuine expertise injection over template-filling.

**Instruction file size check:** Verify primary file (SKILL.md, AGENT.md, etc.) character count. [SOURCE: claudemd.ts:92, doctorContextWarnings.ts:44-47]
- Under 4,000 chars: OPTIMAL — best performance, no action needed.
- 4,000–10,000 chars: WARNING — "Primary file is {N} chars (recommended: <4,000 for optimal performance). Consider moving detail to references/ for better context efficiency."
- Over 40,000 chars: BLOCKING — "Primary file is {N} chars (exceeds 40K /doctor warning threshold). Claude Code's /doctor will flag this. Must reduce — move content to references/."
Note: There is no hard truncation cap in CC source code. 4K is best practice for performance. 40K is where /doctor warns. Files >40K still load but degrade context quality.
**Token economics awareness check:** [SOURCE: loadSkillsDir.ts:100-105] For claude-md products ONLY: verify the primary file is aggressively optimized (every char is always in context). Report character count with context: "This claude-md product is {N} chars. Since claude-md products are loaded EVERY turn (always in context), every character costs tokens. Consider using @include for modular composition or paths: frontmatter to scope activation." This check only applies when type=claude-md; all other types are loaded on-demand.
**Attention-position check (claude-md only):** [SOURCE: claudemd.ts:9-10 — "latest files are highest priority with the model paying more attention to them"]
For claude-md products: scan the primary file for sections containing keywords "critical", "rules", "always", "never", "must", "constraints", "important". Check if these sections are in the LAST 30% of the file (by line count).
- If critical sections are in the last 30%: PASS — "Critical rules are positioned at end of file (attention-optimal)."
- If critical sections are in the first 50%: COACHING — "Your most critical rules are near the top of the file. Claude pays more attention to content at the END. Consider moving your 'Rules' or 'Constraints' sections to the bottom for better enforcement."
This check is coaching only, never blocking. Applies to claude-md products only — other types are loaded on-demand where position matters less.

**Semantic scoping check (claude-md only):** [SOURCE: claudemd.ts:254-279 — path-scoped rules via frontmatter]
For claude-md products: check if the primary file's frontmatter contains a `paths:` field.
- If `paths:` present with specific globs: PASS — "Product scoped to {patterns}. Zero token cost when user works on non-matching files."
- If `paths:` absent: COACHING — "This claude-md product loads EVERY turn for EVERY file. If your rules only apply to specific file types (e.g., *.py, src/api/**), add `paths:` to your frontmatter to scope activation. This reduces buyer token cost to zero when working on unrelated files. See references/cc-platform-contract.md §1.5."
- If `paths:` contains only `**` (match-all): COACHING — same as absent (match-all = unscoped).
This check is coaching only, never blocking. It's the single highest-impact optimization for claude-md products.

**Compact Instructions check:** [SOURCE: compact/prompt.ts:133-143] Check if the product's primary file contains a `## Compact Instructions` section. Read product-dna/{type}.yaml compact_instructions.applicable field:
- If applicable=true AND section missing: WARNING — "Product has no ## Compact Instructions section. Long sessions may lose product context on compaction. Add this section to preserve critical state during context compression. See references/cc-platform-contract.md Section 3.3."
- If applicable=false (hooks, bundle, statusline): SKIP — these types are never in the LLM context.
- If applicable=true AND section present: PASS — verify section has at least 3 bullet points of preservation rules.
This check is non-blocking (coaching) for MCS-1, but required for MCS-2+.
**acceptance_criteria verification:** If `.meta.yaml` contains `creator_intent.acceptance_criteria`, verify each criterion:
  - `truths`: For each stated behavior, grep product files for evidence the behavior is implemented (keywords, sections, instructions). Report unaddressed truths as `[WARNING]`: "acceptance criterion truth '{truth}' has no matching content in product files."
  - `artifacts`: For each required file, verify it exists AND has substantive content (>20 lines or >500 chars). Report missing/thin artifacts as `[WARNING]`: "acceptance criterion artifact '{artifact}' is missing or has insufficient content ({N} lines)."
  - `key_links`: For each connection, grep to verify the link exists. Report broken links as `[WARNING]`: "acceptance criterion key_link '{link}' not found in product files."
  If no acceptance_criteria defined in .meta.yaml, skip silently (not all products have them — they're set during /fill).
Score: `valid_refs / total_refs`

**Stage 3 — DNA TIER 1** (blocking, gates MCS-1)

Load `product-dna/{type}.yaml` → `tier1` patterns where `required: true`.
For each applicable pattern, run the validation check:
- D1 Activation Protocol: grep activation section + references/ ref
- D2 Anti-Pattern Guard: grep anti-pattern section, count >= 5 items
- D3 Progressive Disclosure: primary file < 500 lines + references/ exists
- D4 Quality Gate: grep quality gate section, >= 3 verifiable criteria
- D13 Self-Documentation: README.md with what/install/usage/requirements sections
- D14 Graceful Degradation: grep "when not to use" or degradation section
- D19 Attention-Aware Authoring: (claude-md only, required; others optional) — use the attention-position check above. Critical sections (rules/never/must/constraints) must be in last 30% of primary file. For non-claude-md types: check if applicable per product-dna, score as bonus.
Score: `passed / applicable_count`

**Pitfall memory check** (institutional learning):
Load `meta/pitfalls/pitfalls.json` if it exists. For each pitfall entry with `confidence > 0.5`:
  - Check if the current product exhibits the pitfall pattern (grep for the pitfall's `detection_pattern`)
  - If match found, report as `[WARNING]`: "Known pitfall {id}: {description}. Confidence: {confidence}. Previous fix: {resolution}."
  - Pitfall warnings are non-blocking but MUST appear in the validation report
  - This ensures institutional memory is active, not decorative

**Stage 4 — DNA TIER 2** (non-blocking, gates MCS-2, LITE+PRO)

Load `product-dna/{type}.yaml` → `tier2` patterns where `required: true`.
- D5 Question System: grep question/input table or "if missing, ask"
- D6 Confidence Signaling: grep confidence levels or certainty markers
- D7 Pre-Execution Gate: grep precondition checks
- D8 State Persistence: state file or persistence section
- D15 Testability: test scenarios or expected outputs
- D16 Composability: no hardcoded paths, no common command names
- D17 Hook Integration: hooks section in frontmatter or docs
- D20 Cache-Friendly Design: (claude-md required, system optional) — use the semantic scoping check + token economics check above. Three sub-checks: (1) paths: frontmatter exists with specific globs, (2) primary file <2K chars for claude-md / <4K for system, (3) no dynamic content (date/time/counter patterns). All three pass = PASS. Partial = PARTIAL.
Score: `passed / applicable_count`

**Stage 5 — DNA TIER 3** (non-blocking, gates MCS-3, PRO only)

Invoke Quality Sentinel agent for deep review:
- D9 Orchestrate Don't Execute: routing table, no domain instructions
- D10 Handoff Spec: handoff template between agents
- D11 Socratic Pressure: self-challenge pattern
- D12 Compound Memory: memory config with project scope
- D18 Subagent Isolation: context:fork or isolation
Score: `passed / applicable_count`

**Stage 6 — CLI PREFLIGHT** (blocking)

Run `myclaude validate --json` on the `.publish/` directory (if it exists from a previous /package run).
[SOURCE: myclaude CLI v0.9.0 — checks vault.yaml, files, secrets, license, frontmatter, agent-skills-spec]

**Execution logic:**
1. Check if `.publish/` directory exists in workspace/{slug}/
2. If YES: `cd workspace/{slug}/.publish && myclaude validate --json`
   - Parse JSON output → map each CLI check to our report
   - If CLI reports failures → BLOCKING (must fix before publishing)
   - CLI checks complement Engine checks: secrets re-scan, vault.yaml integrity, license validation
3. If NO .publish/: SKIP with note — "CLI preflight deferred. Run /package first to generate .publish/, then re-run /validate for full CLI checks."
4. If `myclaude` not in PATH: SKIP with warning — "myclaude CLI not installed. Install via `npm i -g @myclaude-cli/cli` for marketplace validation."

**CLI checks mapped to Engine report:**
| CLI Check | Maps To | Severity |
|-----------|---------|----------|
| vault.yaml valid | Integrity | BLOCKING |
| secret scan | Integrity | BLOCKING |
| license valid | Integrity | WARNING |
| frontmatter valid | DNA/Structural | WARNING |
| agent-skills-spec | DNA/Composability | COACHING |
| files count+size | Structural | INFO |

**Stage 6b — SYSTEM HEALTH** (advisory, non-blocking)

If `myclaude` is in PATH, run `myclaude doctor --json 2>/dev/null` and check score:
- score >= 8.0: PASS — "Marketplace health: {score}/10"
- score < 8.0: WARNING — "Marketplace health: {score}/10. Run `myclaude doctor --fix` to resolve issues."
- CLI unavailable: SKIP silently

This surfaces systemic issues (auth, API reachability, lockfile integrity) that would block /publish later.

**Stage 7 — ANTI-COMMODITY** (score-impacting for MCS-2+, coaching for MCS-1)

**Purpose:** Prevent polished-but-generic products from reaching MCS-2. Structure without substance is latão polido.

**The Substance Test (4 checks, scored 0-100):**

1. **Uniqueness Test (0-25):** Read the product's primary file. Could Claude produce equivalent output from a direct prompt like "act as [description]"? Score: 25 if content includes creator-specific knowledge (real cases, contrarian insights, domain heuristics). 15 if content is framework-application (applies known frameworks to a niche). 0 if content is pure framework summary (Wardley Maps primer, JTBD overview).
   **Recursion guard:** This test asks Claude to judge if Claude could produce the same output — a self-referential evaluation prone to generosity bias. Apply a -5 point skepticism discount to the raw score to counteract self-evaluation inflation. If score after discount is still >15, PASS. Record both raw and adjusted scores in the report: "Uniqueness: {raw}/25 (adjusted: {raw-5}/25 after self-eval discount)".

2. **Real Example Test (0-25):** Grep examples/ for specificity markers: named companies, specific numbers, concrete scenarios with outcomes. Score: 25 if examples reference real situations (even anonymized). 15 if examples are realistic but hypothetical. 0 if examples are generic templates.

3. **Sparring Evidence Test (0-25):** Read `.meta.yaml → sparring`. Score: 25 if `real_examples_provided >= 3` and `unproven_sections` is empty. 15 if sparring ran but some sections unproven. 0 if `sparring.skipped: true` or sparring section absent (product created before sparring existed).

4. **Contrarian Test (0-25):** Grep primary file for contrarian markers: "however", "the exception", "this fails when", "counterintuitively", "common mistake", "what most people get wrong". Score: 25 if >= 3 contrarian insights found. 15 if 1-2 found. 0 if none.

**Substance Score = sum of 4 checks (0-100)**

**Impact on overall score (MCS-2+ ONLY):**
- Substance >= 70: No impact — product has genuine depth.
- Substance 50-69: WARNING — "Product has structure but may lack unique expertise. Score capped at 90%."
  Apply: `OVERALL = min(OVERALL, 90)`
- Substance 30-49: WARNING — "Product appears generic. Score capped at 85% (MCS-1 ceiling)."
  Apply: `OVERALL = min(OVERALL, 85)`
- Substance < 30: WARNING — "Product could be reproduced by a direct Claude prompt. Score capped at 80%."
  Apply: `OVERALL = min(OVERALL, 80)`
  Show: "Consider running /fill with sparring to inject real expertise."

**For MCS-1:** Substance score is reported as coaching only, no cap applied. MCS-1 is the "just works" tier — generic is acceptable.

**Creator override:** If the creator explicitly says "I accept the substance score", the cap is noted but the state still advances. Record `substance_override: true` in .meta.yaml. This respects creator agency (Value #1) while making the quality tradeoff visible.

For MCS-2+, also load `references/quality/expert-panel.md` and compute Expert Panel Score (0-100) using Domain Specialist (0-40), Buyer Advocate (0-30), and Platform Architect (0-30) dimensions. Scores < 50 produce strong warnings with remediation.

**Stage 7b — COGNITIVE MIND FIDELITY** (advisory, non-blocking — minds depth:cognitive only)

**Purpose:** When validating a cognitive mind (`.meta.yaml` has `minds_depth: cognitive`), run the 5-layer fidelity scoring defined in `product-dna/minds.yaml → fidelity_scoring`. Advisory minds skip this entirely.

**Prerequisite:** Product type is `minds` AND `.meta.yaml` has `minds_depth: cognitive`. If `minds_depth` is absent or `advisory`, skip silently.

**Execution:**

1. **Layer Completeness (weight: 0.30):**
   - Verify all 5 layer files exist: AGENT.md, references/cognitive-core.md, references/personality.md, references/knowledge-base.md, references/reasoning-engine.md
   - Count lines per layer. Compare against target ranges from `product-dna/minds.yaml → layers.{L}.target_lines`
   - Sum total lines. Target: 800-1200 (reference benchmark = 1,032)
   - Score: `existing_layers / 5` × range compliance

2. **Identity Integrity (weight: 0.25):**
   - C1: Grep AGENT.md for "You ARE" (not "Act as", not "You are an assistant")
   - C2: Grep cognitive-core.md for 3+ dates or named events (biographical anchors)
   - C4: Grep cognitive-core.md for singularity section with 3+ markers
   - C5: Grep personality.md for 5+ characteristic expressions/phrases
   - Score: `passed_checks / 4`

3. **Cognitive Depth (weight: 0.25):**
   - C3: Grep for cognitive flow with named steps (not "think carefully")
   - C6: Grep knowledge-base.md for 3+ domain sections with depth AND boundary declarations
   - C7: Grep reasoning-engine.md for 3+ named reasoning patterns with triggers
   - Score: `passed_checks / 3`

4. **Substance (weight: 0.20):**
   - Examples have real scenarios (not hypothetical — grep for specificity markers)
   - Reasoning engine has concrete models (grep for "When", "trigger", application examples)
   - Boundaries are specific ("I do not X because Y" not "I have limitations")
   - Score: `passed_checks / 3`

5. **Compute Fidelity Score:**
   ```
   FIDELITY = (layer_completeness × 0.30) + (identity_integrity × 0.25) + (cognitive_depth × 0.25) + (substance × 0.20)
   FIDELITY = FIDELITY × 100 (percentage)
   ```

6. **Display:**
   ```
   Cognitive Mind Fidelity: {FIDELITY}%
     Layers: {found}/5 ({total_lines} lines, target 800-1200)
     Identity: C1 {✓/✗} C2 {✓/✗} C4 {✓/✗} C5 {✓/✗}
     Depth:    C3 {✓/✗} C6 {✓/✗} C7 {✓/✗}
     Substance: {score}/3 checks passed
   ```
   If FIDELITY >= 80%: "Benchmark-grade cognitive mind."
   If FIDELITY 60-79%: "Good foundation. Strengthen: {weakest strand names}."
   If FIDELITY < 60%: "Needs deeper content. Missing strands: {list}."

7. **Update .meta.yaml:**
   ```yaml
   state:
     fidelity:
       score: {FIDELITY}
       layers_found: {N}
       total_lines: {N}
       strands_passed: [C1, C3, ...]
       strands_failed: [C2, ...]
       scored_at: "{ISO-8601}"
   ```

**Stage 7c — BASELINE DELTA** (advisory, non-blocking — requires scout report)

**Purpose:** Quantify what the product adds beyond Claude's vanilla knowledge. (Formerly 7b — renumbered after cognitive fidelity insertion.) If a scout report exists for this product, compare the baseline (what Claude already knows) against the product's content (what the product teaches). This is the Engine's value proof: "+N points vs Claude vanilla."

**Prerequisite:** `.meta.yaml` has `scout_source` field (set by /create step 10b when scout-aware routing was used). If `scout_source` is absent, skip silently — not all products have scout reports.

**Execution:**

1. **Load scout report:** Read `workspace/{scout_source}` (e.g., `workspace/scout-kubernetes-security.md`). If file doesn't exist, SKIP with note: "Scout report '{scout_source}' referenced in .meta.yaml but not found in workspace/. Run `/scout` to regenerate, or remove scout_source from .meta.yaml."
   **Model version check:** Parse Section 6 for "Baseline model:" field. If present and different from the current model being used, WARN: "Scout baseline was measured with {scout_model}. Current model is {current_model}. Baseline knowledge may have changed — delta accuracy is approximate. Consider re-running /scout to refresh." Non-blocking — proceed with delta calculation but note the discrepancy.

2. **Parse baseline and gaps:**
   - Extract Section 1 (Baseline) — this is what Claude knows without the product.
   - Extract Section 2 (Gap Analysis) — parse the gap table. Each row has: `#`, `Gap`, `Lens`, `Severity`, `Detail`.
   - Build gap inventory: `{id, name, severity, lens}` for each gap.

3. **Weight gaps by severity:**
   ```
   critical    = 3 points
   significant = 2 points
   minor       = 1 point
   ```
   `TOTAL_WEIGHTED_GAPS = sum(weight per gap)`

4. **Score product coverage:** For each gap in the inventory:
   - Extract 3-5 signature keywords from the gap name + detail (e.g., Gap "Supply chain attacks (SLSA, SBOM)" → keywords: "supply chain", "SLSA", "SBOM", "provenance").
   - Grep the product's primary file + references/ for each keyword.
   - **Addressed** (full weight): >= 2 distinct keyword matches AND >= 50 words within 500 chars of at least one match (density check — mention alone is not coverage).
   - **Partially addressed** (half weight): 1 keyword match OR 2+ matches but < 50 words nearby (thin mention without depth).
   - **Not addressed** (zero): 0 keyword matches.
   - `ADDRESSED_WEIGHT = sum(weight of addressed gaps) + sum(half-weight of partially addressed gaps)`

5. **Compute delta score:**
   ```
   BASELINE_DELTA = (ADDRESSED_WEIGHT / TOTAL_WEIGHTED_GAPS) x 100
   ```
   Round to integer.

6. **Compute point gain:**
   ```
   DELTA_POINTS = ADDRESSED_WEIGHT (raw weighted points gained over baseline)
   ```

7. **Display in validation report:**
   ```
   Baseline Delta: +{DELTA_POINTS} points vs Claude vanilla ({BASELINE_DELTA}% of identified gaps addressed)
     Gaps addressed: {N}/{total} ({critical_addressed}C / {significant_addressed}S / {minor_addressed}M)
     Scout report: {scout_source} ({scout_date})
   ```
   If BASELINE_DELTA >= 70%: "Strong differentiation — product substantially extends Claude's baseline."
   If BASELINE_DELTA 40-69%: "Moderate differentiation — product addresses key gaps but leaves some uncovered. Uncovered critical gaps: {list of critical gap names not addressed}."
   If BASELINE_DELTA < 40%: "Low differentiation — product covers few identified gaps. Uncovered critical gaps: {list of critical gap names not addressed}. Consider running /fill with research injection to increase coverage."
   Always append: "(baseline is simulated — see scout report Section 6 for confidence caveats)"

8. **Research provenance:** For each addressed gap, check if the product content near the keyword matches references URLs or citations from the scout report's Section 4 (Research Findings). If yes: mark as "research-backed" (content was sourced during /fill research injection). If no citations nearby: mark as "creator knowledge" (content comes from the creator's domain expertise). Report: "Research-backed: {N} gaps | Creator knowledge: {M} gaps". This distinguishes products built on verified external research from those built on unverified creator claims — a critical quality signal for buyers.

9. **Interaction with Anti-Commodity (Stage 7):** Baseline delta is INDEPENDENT of substance score. A product can have high substance (real expertise, contrarian insights) but low delta (covers gaps Claude already knows). Conversely, high delta with low substance means the product covers new ground but with thin content. Both signals matter — report them side by side, never merge.

10. **Update .meta.yaml after scoring:**
   ```yaml
   state:
     baseline_delta:
       score: {BASELINE_DELTA}
       points: {DELTA_POINTS}
       gaps_total: {total}
       gaps_addressed: {addressed_count}
       gaps_partial: {partial_count}
       gaps_research_backed: {research_backed_count}
       gaps_creator_knowledge: {creator_knowledge_count}
       scout_source: "{scout_source}"
       scored_at: "{ISO-8601}"
   ```

**Stage 7d — COMPOSITION CHECK** (advisory, non-blocking — bundle type only)

**Purpose:** For bundle products, verify that all included products exist, are valid, and compose without redundancy. A bundle is a curated collection — curation quality matters.

**Prerequisite:** Product type is `bundle`. For all other types, skip silently.

**Execution:**

1. **Load bundle manifest:** Read the product's `vault.yaml` → `bundle.includes[]`. Each entry should be a product slug.

2. **Verify product existence:** For each slug in `bundle.includes[]`:
   - Check `workspace/{slug}/.meta.yaml` exists. If missing: WARNING — "Bundle references '{slug}' but no product found in workspace/. Build or import it before publishing the bundle."
   - If exists: read `.meta.yaml` for `product.type`, `state.phase`, `state.overall_score`.

3. **Composition quality checks:**

   a. **Type diversity:** Count unique product types in the bundle. If all products are the same type: COACHING — "All {N} products in this bundle are type '{type}'. Bundles with diverse types (e.g., minds + skill + workflow) offer more complete capability coverage."

   b. **Validation status:** For each included product, check `state.phase`:
      - If any product is in `scaffold` phase: WARNING — "Bundle includes '{slug}' which is still in scaffold phase. Fill and validate it before publishing the bundle."
      - If any product hasn't been validated: COACHING — "Bundle includes '{slug}' (not yet validated). Consider running /validate on all included products."

   c. **Scout coherence (if scout report exists):** If the bundle's `.meta.yaml` has `scout_source`, load the scout report's Section 5 (Setup Recommendation → Composition Map). Verify:
      - All products recommended in the scout report are present in `bundle.includes[]`. Missing = COACHING: "Scout report recommended '{slug}' but it's not in the bundle."
      - No products in the bundle are absent from the scout recommendation. Extra = INFO (acceptable — creator may have added products beyond scout scope).

   d. **Gap coverage breadth:** If scout report exists, for each included product, run the baseline delta gap-matching logic (from Stage 7b step 4). Aggregate: which gaps are covered by at least one product in the bundle?
      - Report: "Bundle covers {N}/{total} gaps from scout report ({percentage}%)."
      - If coverage < 60%: COACHING — "Bundle leaves significant gaps uncovered. Consider adding products that address: {list of uncovered critical gaps}."

4. **Display in validation report:**
   ```
   Composition Check (bundle):
     Products: {N} included ({types_summary})
     Existence: {found}/{total} found in workspace
     Validation: {validated_count}/{total} validated
     {If scout exists:}
     Scout alignment: {recommended_found}/{recommended_total} recommended products included
     Gap coverage: {covered}/{total_gaps} gaps addressed ({percentage}%)
   ```

**Stage 8 — VALUE INTELLIGENCE** (advisory, non-blocking — MCS-2+ only)

**Purpose:** Compute a composite value score for the product based on 4 objective signals. This is the Intelligence Layer's core computation — it transforms structural quality metrics into actionable pricing and positioning intelligence. Reference: `references/intelligence-layer.md` + `config.yaml → intelligence`.

**Prerequisite:** Product must have completed Stage 7 (anti-commodity). For MCS-1, skip entirely — MCS-1 is "just works" tier where value intelligence adds noise, not signal.

**Execution:**

1. **Load intelligence config:** Read `config.yaml → intelligence.pricing` for weights and price_map.

2. **Compute DEPTH factor (0-4):**
   ```
   MCS-1 (75-84%)  → depth = 1
   MCS-2 (85-91%)  → depth = 2
   MCS-3 (92-100%) → depth = 3
   If product type is minds AND minds_depth is cognitive → depth += 1
   ```
   Use the OVERALL score computed in the scoring section below.

3. **Compute UNIQUENESS factor (0-3):**
   Read Stage 7 substance score (anti-commodity).
   ```
   substance < 50  → uniqueness = 0  ("Claude already knows this")
   substance 50-70 → uniqueness = 1  ("adds some depth")
   substance 70-90 → uniqueness = 2  ("genuine expertise")
   substance > 90  → uniqueness = 3  ("irreplaceable knowledge")
   ```

4. **Compute COVERAGE factor (0-3):**
   Read Stage 7c baseline delta (if available).
   ```
   No baseline delta available → coverage = 1 (default — cannot assess without scout)
   gaps_addressed < 3          → coverage = 0
   gaps_addressed 3-6          → coverage = 1
   gaps_addressed 7-10         → coverage = 2
   gaps_addressed > 10         → coverage = 3
   ```

5. **Compute MARKET factor (0-2):**
   Check `.meta.yaml → intelligence.market_position` (set by /scout or /create marketplace scan).
   ```
   market_position not set     → market = 1 (default — cannot assess)
   saturated (4+ competitors)  → market = 0
   moderate (1-3 competitors)  → market = 1
   blue_ocean (0 competitors)  → market = 2
   ```

6. **Compute VALUE_SCORE (0-12):**
   ```
   VALUE_SCORE = round((depth/4 × 0.35 + uniqueness/3 × 0.30 + coverage/3 × 0.20 + market/2 × 0.15) × 12)
   # Guard: if uniqueness=0 AND coverage=0, cap VALUE_SCORE at 2 (free tier)
   ```
   Note: Each factor normalized to 0-1, weighted by importance, scaled to 0-12. G014: original omitted normalization+scaling (max ~3.2). Original raw sum distorted weights. This normalized formula preserves intended ratios. Guard prevents structural quality alone from commanding a price.

7. **Map to pricing:** Read `config.yaml → intelligence.pricing.price_map`. Find the bracket where `VALUE_SCORE >= min AND VALUE_SCORE <= max`. Extract `range`, `strategy`, `guidance`.

8. **Determine portfolio role:**
   Read `STATE.yaml → workspace.products[]`. Count products in the same domain as the current product.
   ```
   Only product in its domain         → role = "anchor"
   Domain has 1 other product          → role = "complement"
   Domain has 2+ other products        → role = "extension"
   Product has no domain assigned      → role = "standalone"
   ```

9. **Determine free-vs-paid recommendation:**
   Read `config.yaml → intelligence.free_vs_paid` decision tree. Apply in order:
   - Count products in the same domain across `STATE.yaml → workspace.products[]`
   - If this is the first product in the domain → "free" (build authority)
   - If creator has <3 published products total → "free" (build audience)
   - If MCS-2+ AND substance >70 → "paid" (value justified)
   - Else → "free_or_signal" ($0-3)

10. **Display in validation report:**
    ```
    VALUE INTELLIGENCE (Stage 8):
      Value score: {VALUE_SCORE}/12
        Depth:      {depth_raw}/{depth_max} (MCS-{level}{if cognitive: " + cognitive"})
        Uniqueness: {uniqueness_raw}/3 (substance: {substance_score}%)
        Coverage:   {coverage_raw}/3 ({gaps_addressed} gaps{if no delta: " — no scout data"})
        Market:     {market_raw}/2 ({market_position}{if unknown: " — run /scout for data"})
      
      Suggested price: ${range[0]}-${range[1]} ({strategy})
      {guidance}
      
      Free vs paid: {recommendation} — {reason}
      Portfolio role: {role} in {domain}
      
      ⓘ Value signal is estimated from structural quality + market position.
        Real value is confirmed by daily use. If YOU use this every day, others will too.
    ```

11. **Update .meta.yaml intelligence fields:**
    ```yaml
    intelligence:
      domain: "{inferred_domain}"
      market_position: "{market_position}"
      value_score: {VALUE_SCORE}
      value_score_breakdown:
        depth: {depth_raw}
        uniqueness: {uniqueness_raw}
        coverage: {coverage_raw}
        market: {market_raw}
      suggested_price_range: [{range[0]}, {range[1]}]
      pricing_strategy: "{strategy}"
      distribution_channels: ["{channels from config.yaml by type}"]
      portfolio_role: "{role}"
      scored_at: "{ISO-8601}"
    ```

**Design decisions:**
- Value intelligence runs AFTER scoring so it can consume the overall MCS score and substance score — it's a synthesizer, not a primary check.
- Factors with missing data default to middle values (1), not zero — prevents penalizing products that simply haven't been scouted yet. The report explicitly notes which factors are estimated vs measured.
- The epistemic caveat is ALWAYS shown. No exceptions. This is what makes the intelligence trustworthy.
- Value score is advisory-only — it never blocks publishing. The user always decides pricing.
