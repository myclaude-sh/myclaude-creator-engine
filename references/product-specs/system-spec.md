# Product Spec: Systems

## Definition

Systems are meta-products that combine multiple product types into cohesive, integrated
solutions. A system is the highest-complexity product type — it is not a collection of
parts but a unified whole with routing, shared state, and emergent capability greater
than any single component.

CE-D6: Systems are the premium tier. The Creator Engine itself is a system-type product.

A system is NOT:
- A squad (squads coordinate agents; systems coordinate any product types)
- A bundle (bundles are collections; systems have routing and integration logic)
- Just a folder with multiple products

A system IS:
- An integrated solution with explicit component interaction
- A product with its own routing layer and shared knowledge base
- Greater-than-the-sum-of-parts through deliberate composition

---

## Canonical File Structure

```
system-name/
├── SYSTEM.md              # System overview and composition (REQUIRED)
├── README.md              # Setup and usage (REQUIRED)
├── skills/                # Included skills
│   └── skill-name/
├── agents/                # Included agents
│   └── agent-name.md
├── workflows/             # Included workflows
│   └── workflow-name/
├── references/            # Shared knowledge base
│   └── shared-knowledge.md
├── config/
│   ├── routing.yaml       # How components interact (REQUIRED)
│   └── manifest.yaml      # Component inventory (REQUIRED)
└── CHANGELOG.md           # Version history
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `SYSTEM.md` | System overview, composition, routing | MCS-1 |
| `README.md` | Setup, entry points, usage | MCS-1 |
| `config/manifest.yaml` | Component inventory | MCS-1 |
| At least 2 component types | Real product diversity | MCS-1 |

---

## Required Sections in SYSTEM.md

### 1. System Name, Purpose, and Composition

```markdown
# System Name

**Purpose:** One sentence — what this system achieves as a whole
**Version:** 1.0.0
**Components:** [list: 2 skills + 1 agent + 1 workflow, etc.]
**Entry Point:** How a user starts using this system
**Complexity:** [OPERATIONAL | COGNITIVE | HYBRID]
```

### 2. Architecture Overview

How the components fit together:
- Which components exist and what they each do
- How components interact with each other
- What data flows between components
- The routing layer that coordinates everything

Visual representation strongly recommended:

```markdown
## Architecture

[User Input]
     │
     ▼
[Routing Layer] ─── intent: "analyze" ──► [analysis-skill]
     │                                         │
     └── intent: "generate" ──► [generator-agent]
                                               │
                                               ▼
                               [shared knowledge base]
                                               │
                                               ▼
                               [output-workflow] ──► [Final Output]
```

### 3. Component Inventory

Every component with its role, type, and location:

```markdown
## Components

| Name | Type | Location | Purpose |
|------|------|----------|---------|
| analysis-skill | Skill | skills/analysis/ | Decomposes input |
| generator-agent | Agent | agents/generator.md | Creates outputs |
| output-workflow | Workflow | workflows/output/ | Formats and delivers |
```

### 4. Routing Logic

How the system decides which component handles which input:

```markdown
## Routing

The system entry point routes requests based on intent:
- Intent: analyze → analysis-skill
- Intent: generate → generator-agent (uses analysis output)
- Intent: both → analysis-skill → generator-agent (sequential)
```

### 5. Shared Knowledge Base

What all components share:
- Files in `references/` that multiple components consume
- Common terminology and definitions
- Shared state and how it's managed

### 6. User Journey

The primary paths a user takes through the system:
- Entry point (how they invoke the system)
- Common paths (the 3-5 most frequent usage patterns)
- Edge case paths (what happens in exceptional scenarios)

### 7. Configuration

How to configure the system for specific contexts:
- What can be customized
- How to enable/disable components
- Integration with other MyClaude products

---

## manifest.yaml Format

```yaml
# manifest.yaml — auto-read by system routing
system:
  name: "system-name"
  version: "1.0.0"
  entry_point: "SYSTEM.md"

components:
  skills:
    - name: "skill-name"
      path: "skills/skill-name/"
      mcs_level: 2
      handles: ["intent-1", "intent-2"]

  agents:
    - name: "agent-name"
      path: "agents/agent-name.md"
      mcs_level: 2
      handles: ["intent-3"]

  workflows:
    - name: "workflow-name"
      path: "workflows/workflow-name/"
      mcs_level: 1
      triggers: ["completion-of-agent-name"]

  shared_references:
    - "references/shared-knowledge.md"

integration:
  routing: "config/routing.yaml"
  knowledge_base: "references/"
```

---

## MCS Requirements

### MCS-1: Publishable

**Universal:**
- [ ] Valid SYSTEM.md with all required sections
- [ ] README.md with: what the system does, all entry points, setup instructions
- [ ] `config/manifest.yaml` listing all components
- [ ] At least 2 different product types as components
- [ ] All component references resolve (files exist)
- [ ] Metadata complete
- [ ] No syntax errors
- [ ] License from approved list

**System-Specific:**
- [ ] Each component at MCS-1 minimum
- [ ] Routing logic documented (even if basic)
- [ ] At least 1 shared knowledge file in `references/`

### MCS-2: Quality

**Universal (beyond MCS-1):**
- [ ] `config/routing.yaml` with explicit routing rules
- [ ] All components at MCS-1+ individually
- [ ] Integration tests (at least 2 end-to-end scenarios)
- [ ] Anti-patterns section
- [ ] No placeholder content
- [ ] Semver versioning

**System-Specific:**
- [ ] Routing tested with ambiguous inputs (which component should handle this?)
- [ ] Shared knowledge base is actually shared (referenced by multiple components)
- [ ] At least 3 component types (not just 2 skills)
- [ ] User journey documented with entry points

### MCS-3: State-of-the-Art

**Universal (beyond MCS-2):**
- [ ] All components at MCS-2+ individually
- [ ] Stress-tested system routing
- [ ] Adaptive system modes
- [ ] Full documentation of system architecture decisions
- [ ] CHANGELOG with versioning history
- [ ] Performance metrics (how many tokens, what response time)
- [ ] Differentiation statement

**System-Specific:**
- [ ] System works as standalone AND individual components usable independently
- [ ] Advanced routing with fallbacks
- [ ] Shared state management strategy documented
- [ ] System tested by at least 5 real users with different intent patterns

---

## Anti-Patterns for Systems

### Structural
- **Bundle masquerading as system:** Folder containing multiple products but no routing, no shared knowledge, no integration logic. A system has emergent capability; a bundle is just packaging.
- **Broken component references:** `manifest.yaml` lists `skills/my-skill/` but the directory doesn't exist. All component references must resolve.
- **Missing manifest:** System without `config/manifest.yaml`. The system's components are implicit instead of explicit.

### Content
- **Components that don't interact:** Each component is self-contained and none share context, state, or outputs. If they don't interact, it's a bundle, not a system.
- **Routing logic in prose only:** "Use the analysis skill when you want analysis" — routing must be declarative (routing.yaml) not just described in English.
- **No entry point definition:** SYSTEM.md doesn't specify how a user invokes the system. Buyers can't figure out where to start.

### Quality
- **Components not individually usable:** All components are so tightly coupled they only work inside the system. MCS-3 requires composable components.
- **No integration tests:** System validated by checking each component independently. Integration tests must verify components work together.

---

## Discovery Questions (from §7)

When creating a system, answer these before scaffolding:

1. What is the system's overarching purpose? (what does the whole achieve that parts cannot)
2. What product types does it combine? (skills + agents + workflows? what's the right mix)
3. How do the components interact? (routing, handoffs, shared state, sequential vs. parallel)
4. What is the user entry point? (what does a user say/do to activate the system)
5. Can components be used independently or only as a system? (composability decision)
6. What is the shared knowledge base? (what context all components need)
7. What are the 3-5 most common user paths through the system?

---

## DNA Requirements

For the complete DNA pattern applicability matrix for this product type,
see `product-dna/system.yaml`. That file defines:
- Which of the 18 DNA patterns (D-01 to D-18) are required vs optional
- Validation checks per pattern (grep/glob commands)
- Template file mapping with DNA injection points
- Frontmatter fields (Anthropic Agent Skills spec)
- Discovery questions for /create

**MCS scoring:** `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
See `references/quality/mcs-spec.md` for full scoring formula.
