# Changelog

All notable changes to the MyClaude Studio Engine.

## [2.0.0] — 2026-03-28

### Added
- **Structural DNA system** — 18 patterns in 3 tiers with validation checks (`structural-dna.md`)
- **Product DNA files** — 9 type-specific DNA requirement files (`product-dna/*.yaml`)
- **Quality gates** — state machine: scaffold→content→validated→packaged→published (`quality-gates.yaml`)
- **MCS v2 scoring** — DNA-based formula: `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
- `/map` skill — domain knowledge extraction with structured output
- `/fill` skill — guided content filling (replaces `/create-content`)
- `/status` skill — engine dashboard with workspace overview
- `/help` skill — command reference with edition detection
- `/test` skill — worktree-isolated sandbox testing (3 scenarios)
- **LITE/PRO edition detection** — glob `.claude/skills/forge-master/` in boot
- **Dual manifest generation** — `/package` creates both vault.yaml + plugin.json
- **WHY comments** — templates use `<!-- WHY: D{N} -->` format (stripped by `/package`)

### Changed
- `CLAUDE.md` rewritten to <200 lines with lean boot, edition detection, skill routing
- `config.yaml` rebuilt with MCS scoring weights, 9 product routes, feature flags, validation pipeline
- `STATE.yaml` redesigned with workspace product tracking and MCS results
- `README.md` updated for v2.0 — new architecture, DNA system, editions
- `/validate` evolved — 7-stage DNA pipeline, product-dna/ loading, DNA scoring formula
- `/create` evolved — DNA injection, product-dna/ refs, `/fill` reference
- `/package` rewritten — dual manifests (vault.yaml + plugin.json), SHA-256 checksum
- `/publish` rewritten — lean CLI delegation (~100 lines)
- `/onboard` updated — `.meta.yaml` refs
- Template comments migrated from `GUIDANCE:` to `WHY:` format (9 templates)
- `.engine-meta.yaml` bumped to v2.0.0
- All `.engine-meta.yaml` references → `.meta.yaml` (PRD v2.0 naming)

### Removed
- `/create-content` (replaced by `/fill`)
- `/quick-skill` (streamline: use individual commands)
- `/quick-publish` (streamline: use `/package` then `/publish`)
- `/engine-status` (replaced by `/status`)
- `/engine-help` (replaced by `/help`)
- `/differentiate` (moved to PRO Quality Sentinel agent)
- `/quality-review` (moved to PRO Quality Sentinel agent)
- `/domain-consult` (moved to PRO Domain Cartographer agent)
- `/market-scan` (moved to PRO Market Scout agent)
- `/packaging-review` (absorbed into `/package`)
- `/my-products` (moved to PRO Market Scout agent)
- `references/caching-strategy.md` (obsolete)
- **Net: 11 skills killed, 22 files removed, ~4,257 lines deleted**

## [1.1.0] — 2026-03-26

### Added
- `/create-content` skill — guided content filling after scaffold
- `/package` skill — standalone packaging without publishing
- `/test` skill — sandbox testing against sample inputs
- `/engine-status` skill — dashboard with profile, workspace, stale builds
- `/engine-help` skill — complete command listing
- `/quick-skill` skill — idea-to-marketplace pipeline shortcut
- `/quick-publish` skill — validate-to-publish pipeline shortcut
- `/differentiate` skill — anti-commodity coaching
- `/quality-review` skill — deep MCS-3 quality audit
- Exemplar-first experience in `/create`
- Guided iteration in `/validate`

### Changed
- All skills migrated to Anthropic Agent Skills spec
- Skills renamed for natural invocation
- MCS-spec aligned with validator checks

### Removed
- Legacy `skills/` and `agents/` directories at project root
- Redundant `.claude/commands/` wrappers

## [1.0.0] — 2026-03-25

### Added
- Initial release — 4 core skills, 5 cognitive agents, 9 product specs, 9 templates, 9 exemplars
- MCS 3-tier quality system
- CONDUIT v2 vault.yaml manifest integration
- MyClaude CLI publishing support
