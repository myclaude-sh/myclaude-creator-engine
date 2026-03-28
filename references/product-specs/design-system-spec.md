# Product Spec: Design Systems

## Definition

Design Systems are token sets, component specifications, brand kits, and design rules
for Claude Code projects. They enable consistent visual implementation by encoding
design decisions as structured, machine-readable tokens that Claude Code can reference
when building UI.

A design system is NOT:
- A Figma file export (this is a code-first, text-based format)
- A CSS framework (though it can export to Tailwind or CSS variables)
- A collection of UI screenshots

A design system IS:
- A structured set of design tokens (color, type, spacing, shadows, motion)
- A specification that Claude Code can read and apply consistently
- An exportable design contract between design and implementation

---

## Canonical File Structure

```
design-system-name/
├── DESIGN-SYSTEM.md       # Overview and philosophy (REQUIRED)
├── README.md              # Setup and usage (REQUIRED)
├── tokens/
│   ├── colors.yaml        # Color tokens with semantic names (REQUIRED)
│   ├── typography.yaml    # Type scale, font stacks (REQUIRED)
│   ├── spacing.yaml       # Spacing scale (REQUIRED)
│   ├── shadows.yaml       # Shadow/elevation system
│   └── motion.yaml        # Animation tokens
├── components/            # Component specifications
│   ├── button.md
│   ├── card.md
│   └── ...
├── exports/               # Platform-specific exports
│   ├── tailwind.config.js
│   ├── css-variables.css
│   └── dtcg.json
├── guidelines/
│   ├── usage.md
│   └── anti-patterns.md
└── examples/              # Real implementation examples
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `DESIGN-SYSTEM.md` | Philosophy, overview, usage instructions | MCS-1 |
| `README.md` | Installation and quick start | MCS-1 |
| `tokens/colors.yaml` | Color token definitions | MCS-1 |
| `tokens/typography.yaml` | Typography scale | MCS-1 |
| `tokens/spacing.yaml` | Spacing scale | MCS-1 |
| At least 1 file in `exports/` | Platform export | MCS-1 |

---

## Required Sections in DESIGN-SYSTEM.md

### 1. Design System Name and Philosophy

```markdown
# Design System Name

**Version:** 1.0.0
**Philosophy:** One to two sentences describing the design values (e.g., "minimal, functional,
dark-first; no decoration that doesn't serve function")
**Target Platforms:** [web | mobile | both]
**Base Unit:** [4px | 8px | other] (the fundamental spacing unit)
```

### 2. Token Architecture

How the tokens are organized and named:
- Naming convention (semantic vs. scale-based)
- Token hierarchy (primitive → semantic → component)
- Color space used (OKLCH recommended for perceptual uniformity, HSL, or hex)

### 3. Color System

The color token structure with at minimum:
- Brand colors (primary, secondary, accent)
- Semantic colors (surface, on-surface, border, overlay)
- Status colors (success, warning, error, info)
- Full light/dark mode support OR explicit single-mode declaration

### 4. Typography Scale

- Font family stack (with fallbacks)
- Type scale steps (xs through 4xl or equivalent)
- Line height recommendations per scale step
- Font weight options

### 5. Spacing Scale

- Base unit
- Scale multipliers (1×, 1.5×, 2×, 3×, 4×, 6×, 8×, etc.)
- Named steps (xs, sm, md, lg, xl, 2xl, etc.)

### 6. Export Instructions

How to apply the tokens in a project:
- Which export file to use for which platform
- Installation steps
- How to reference tokens in code

---

## Token Format Standards

### colors.yaml

```yaml
# Colors use OKLCH for perceptual uniformity
# Format: oklch(lightness chroma hue)
colors:
  primitive:
    brand-500: "oklch(55% 0.22 250)"
    brand-600: "oklch(48% 0.22 250)"
  semantic:
    primary: "$colors.primitive.brand-500"
    primary-hover: "$colors.primitive.brand-600"
    surface: "oklch(98% 0 0)"
    on-surface: "oklch(15% 0 0)"
    border: "oklch(88% 0 0)"
  status:
    success: "oklch(60% 0.18 145)"
    warning: "oklch(72% 0.18 85)"
    error: "oklch(55% 0.22 20)"
    info: "oklch(62% 0.18 230)"
```

### typography.yaml

```yaml
typography:
  families:
    sans: "'Inter', 'system-ui', sans-serif"
    mono: "'JetBrains Mono', 'Consolas', monospace"
  scale:
    xs:   { size: "0.75rem",  lineHeight: "1rem" }
    sm:   { size: "0.875rem", lineHeight: "1.25rem" }
    base: { size: "1rem",     lineHeight: "1.5rem" }
    lg:   { size: "1.125rem", lineHeight: "1.75rem" }
    xl:   { size: "1.25rem",  lineHeight: "1.75rem" }
    2xl:  { size: "1.5rem",   lineHeight: "2rem" }
    3xl:  { size: "1.875rem", lineHeight: "2.25rem" }
    4xl:  { size: "2.25rem",  lineHeight: "2.5rem" }
  weights:
    normal: 400
    medium: 500
    semibold: 600
    bold: 700
```

---

## MCS Requirements

### MCS-1: Publishable

**Universal:**
- [ ] Valid DESIGN-SYSTEM.md with all required sections
- [ ] README.md with: what it is, how to install, how to use tokens
- [ ] `tokens/colors.yaml` with semantic color tokens
- [ ] `tokens/typography.yaml` with scale
- [ ] `tokens/spacing.yaml` with scale
- [ ] At least 1 export file in `exports/`
- [ ] Metadata complete
- [ ] No syntax errors in YAML files
- [ ] License from approved list

**Design-System-Specific:**
- [ ] Token naming follows consistent convention (semantic names, not raw values)
- [ ] Color tokens have semantic layer (not just "blue-500", but "primary")
- [ ] Export file is valid and usable (not placeholder)

### MCS-2: Quality

**Universal (beyond MCS-1):**
- [ ] Component specifications in `components/`
- [ ] `guidelines/usage.md` with do/don't patterns
- [ ] `guidelines/anti-patterns.md`
- [ ] 2+ export formats
- [ ] Tested in a real project
- [ ] No placeholder tokens (every token has a real value)
- [ ] Semver versioning

**Design-System-Specific:**
- [ ] At least 3 component specifications (button, input, card, etc.)
- [ ] Dark mode token variants OR explicit single-mode statement
- [ ] Both web export formats (Tailwind + CSS variables minimum)
- [ ] Usage examples showing tokens in real code

### MCS-3: State-of-the-Art

**Universal (beyond MCS-2):**
- [ ] Full component library (10+ components)
- [ ] 3+ export formats
- [ ] Theming system (multiple themes from same tokens, OR customization protocol)
- [ ] Motion tokens in `tokens/motion.yaml`
- [ ] Composable with other design systems
- [ ] Documentation of design decisions
- [ ] Differentiation statement

**Design-System-Specific:**
- [ ] DTCG (Design Token Community Group) format export
- [ ] Component specification covers states (default, hover, focus, disabled, error)
- [ ] Accessibility contrast ratios verified (WCAG 2.1 AA minimum)
- [ ] Claude Code integration examples (how to instruct Claude to use these tokens)

---

## Anti-Patterns for Design Systems

### Structural
- **Raw values without semantic layer:** Only providing `brand-blue-500: "#3B82F6"` without `primary: "$brand-blue-500"`. Semantic tokens are what make a design system adaptable.
- **Export files as placeholder:** `tailwind.config.js` that only has `// TODO: add tokens`. Broken exports make the product non-functional.
- **Missing typography scale:** Only providing colors. Typography scale is mandatory — half the visual language is type.

### Content
- **Inconsistent naming:** Some tokens use `camelCase`, others use `kebab-case`, others use underscores. Pick one convention and apply it everywhere.
- **No light/dark specification:** Color tokens that work only in one mode without declaring which mode. Buyers need to know what they're getting.
- **Hardcoded hex without color space strategy:** Large token sets in hex without any perceptual consistency. OKLCH or HSL prevents color math problems.

### Quality
- **No usage examples:** Token library exists but no examples show how to use it in practice. Buyers can't evaluate fit.
- **Component specs without states:** Button component defined only for default state. All interactive components have at minimum 4 states (default, hover, focus, disabled).

---

## Discovery Questions (from §7)

When creating a design system, answer these before scaffolding:

1. What brand identity? (colors, typography personality, visual weight)
2. What platforms? (web only, mobile, both)
3. What export formats are needed? (Tailwind, CSS variables, DTCG, other)
4. How deep is the component library? (tokens only, tokens + basic components, full library)
5. Light mode only, dark mode only, or both?
6. What is the base unit for spacing? (4px, 8px, or other)
7. Does this need theming support? (multiple color themes from same token set)

---

## DNA Requirements

For the complete DNA pattern applicability matrix for this product type,
see `product-dna/design-system.yaml`. That file defines:
- Which of the 18 DNA patterns (D-01 to D-18) are required vs optional
- Validation checks per pattern (grep/glob commands)
- Template file mapping with DNA injection points
- Frontmatter fields (Anthropic Agent Skills spec)
- Discovery questions for /create

**MCS scoring:** `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
See `references/quality/mcs-spec.md` for full scoring formula.
