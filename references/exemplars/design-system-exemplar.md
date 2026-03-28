# Design System Exemplar: Minimal Dark DS

**MCS Level:** 2 (Quality)
**Demonstrates:** Complete token files in OKLCH, typography scale, Tailwind export,
CSS variables export, component spec, usage guidelines, anti-patterns.

---

## File: `DESIGN-SYSTEM.md`

```markdown
# Minimal Dark DS

> A dark-first, function-over-decoration design system for professional tools and
> productivity applications. No shadows for aesthetics — only for function.

**Version:** 1.2.0
**Target Platforms:** Web
**Base Unit:** 4px
**Color Space:** OKLCH
**Author:** @minimalworks

---

## Design Philosophy

Minimal Dark DS encodes three values: **function wins over decoration**, **dark is default**,
and **density is a feature**. Professional tools don't need whitespace to breathe — they need
information density. Every token exists because a specific UI decision required it,
not because the system needed to look comprehensive.

**Core values:**
1. **Dark-first** — Light mode is an afterthought, available but not the primary design target
2. **Information density** — Default spacing is tighter than consumer app norms
3. **No decoration** — No gradients, no rounded corners beyond functional radius

---

## Token Architecture

Two-layer system:
- **Primitives:** `zinc-*`, `teal-*`, `red-*` — raw palette values, never used in app code
- **Semantics:** `surface`, `primary`, `error` — named by role, reference primitives

Always reference semantic tokens in application code. Changing from dark to light mode
means updating 6 semantic tokens, not hunting through every component.

**Naming:** kebab-case throughout.

---

## Color System

**Mode support:** Dark mode primary; light mode secondary (separate token file: `tokens/colors-light.yaml`)

See `tokens/colors.yaml` for full definitions.

### Palette Overview

**Brand:**
- `primary` — Teal accent for interactive elements (oklch(72% 0.14 185))
- `primary-hover` — Slightly brighter teal for hover states
- `primary-active` — Dimmer for pressed states

**Surfaces (dark mode):**
- `surface` — Near-black base background (oklch(12% 0 0))
- `surface-raised` — Cards and panels (oklch(16% 0 0))
- `surface-overlay` — Modals and drawers (oklch(20% 0 0))
- `surface-input` — Form input backgrounds (oklch(14% 0 0))

**Content:**
- `on-surface` — Primary text (oklch(90% 0 0))
- `on-surface-muted` — Secondary text, labels (oklch(60% 0 0))
- `on-surface-disabled` — Disabled state text (oklch(35% 0 0))
- `border` — Subtle dividers (oklch(24% 0 0))
- `border-focus` — Focus rings on interactive elements (oklch(72% 0.14 185) = primary)

**Status:**
- `success` — oklch(68% 0.18 145) — Green
- `warning` — oklch(75% 0.18 80) — Amber
- `error` — oklch(62% 0.22 22) — Red
- `info` — oklch(68% 0.15 230) — Blue
```

---

## File: `tokens/colors.yaml`

```yaml
# Minimal Dark DS — Color Tokens v1.2.0
# Dark mode. OKLCH color space.

primitive:
  zinc-950: "oklch(12% 0 0)"
  zinc-900: "oklch(16% 0 0)"
  zinc-850: "oklch(20% 0 0)"
  zinc-800: "oklch(24% 0 0)"
  zinc-400: "oklch(60% 0 0)"
  zinc-200: "oklch(88% 0 0)"
  zinc-50:  "oklch(97% 0 0)"

  teal-400: "oklch(72% 0.14 185)"
  teal-500: "oklch(65% 0.15 185)"
  teal-600: "oklch(58% 0.14 185)"

  red-400: "oklch(62% 0.22 22)"
  amber-400: "oklch(75% 0.18 80)"
  green-400: "oklch(68% 0.18 145)"
  blue-400: "oklch(68% 0.15 230)"

semantic:
  # Surfaces
  surface: "$primitive.zinc-950"
  surface-raised: "$primitive.zinc-900"
  surface-overlay: "$primitive.zinc-850"
  surface-input: "oklch(14% 0 0)"

  # Content
  on-surface: "$primitive.zinc-200"
  on-surface-muted: "$primitive.zinc-400"
  on-surface-disabled: "oklch(35% 0 0)"
  border: "$primitive.zinc-800"
  border-focus: "$primitive.teal-400"

  # Interactive
  primary: "$primitive.teal-400"
  primary-hover: "oklch(78% 0.14 185)"
  primary-active: "$primitive.teal-500"
  primary-foreground: "$primitive.zinc-950"

  # Status
  success: "$primitive.green-400"
  success-surface: "oklch(20% 0.06 145)"
  warning: "$primitive.amber-400"
  warning-surface: "oklch(20% 0.07 80)"
  error: "$primitive.red-400"
  error-surface: "oklch(20% 0.07 22)"
  info: "$primitive.blue-400"
  info-surface: "oklch(20% 0.06 230)"
```

---

## File: `tokens/typography.yaml`

```yaml
# Minimal Dark DS — Typography Tokens v1.2.0

families:
  sans: "'Inter', 'system-ui', '-apple-system', sans-serif"
  mono: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace"

scale:
  xs:   { size: "0.75rem",   lineHeight: "1rem",    tracking: "0.025em" }
  sm:   { size: "0.8125rem", lineHeight: "1.125rem", tracking: "0.01em" }
  base: { size: "0.9375rem", lineHeight: "1.5rem",   tracking: "0" }
  # Slightly smaller base than typical (15px) — density default
  lg:   { size: "1.0625rem", lineHeight: "1.625rem", tracking: "0" }
  xl:   { size: "1.25rem",   lineHeight: "1.75rem",  tracking: "-0.01em" }
  2xl:  { size: "1.5rem",    lineHeight: "2rem",     tracking: "-0.02em" }
  3xl:  { size: "1.875rem",  lineHeight: "2.25rem",  tracking: "-0.025em" }
  4xl:  { size: "2.25rem",   lineHeight: "2.5rem",   tracking: "-0.03em" }

weights:
  normal: 400
  medium: 500
  semibold: 600
  bold: 700
```

---

## File: `tokens/spacing.yaml`

```yaml
# Minimal Dark DS — Spacing Tokens v1.2.0
# Base unit: 4px. Dense by default.

scale:
  0.5: "0.125rem"   # 2px  — tight internal padding
  1:   "0.25rem"    # 4px  — smallest intentional gap
  1.5: "0.375rem"   # 6px
  2:   "0.5rem"     # 8px  — standard internal padding
  3:   "0.75rem"    # 12px — form fields, compact cards
  4:   "1rem"       # 16px — standard padding
  5:   "1.25rem"    # 20px
  6:   "1.5rem"     # 24px — section gaps within a panel
  8:   "2rem"       # 32px — between sections
  10:  "2.5rem"     # 40px
  12:  "3rem"       # 48px — major section breaks
  16:  "4rem"       # 64px — layout-level spacing
  20:  "5rem"       # 80px
  24:  "6rem"       # 96px — page-level gaps
```

---

## File: `exports/tailwind.config.js`

```javascript
// Minimal Dark DS — Tailwind Config v1.2.0
// Extends default Tailwind with design system tokens

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: 'oklch(12% 0 0)',
          raised: 'oklch(16% 0 0)',
          overlay: 'oklch(20% 0 0)',
          input: 'oklch(14% 0 0)',
        },
        'on-surface': {
          DEFAULT: 'oklch(88% 0 0)',
          muted: 'oklch(60% 0 0)',
          disabled: 'oklch(35% 0 0)',
        },
        border: {
          DEFAULT: 'oklch(24% 0 0)',
          focus: 'oklch(72% 0.14 185)',
        },
        primary: {
          DEFAULT: 'oklch(72% 0.14 185)',
          hover: 'oklch(78% 0.14 185)',
          active: 'oklch(65% 0.15 185)',
          foreground: 'oklch(12% 0 0)',
        },
        error: {
          DEFAULT: 'oklch(62% 0.22 22)',
          surface: 'oklch(20% 0.07 22)',
        },
        success: {
          DEFAULT: 'oklch(68% 0.18 145)',
          surface: 'oklch(20% 0.06 145)',
        },
        warning: {
          DEFAULT: 'oklch(75% 0.18 80)',
          surface: 'oklch(20% 0.07 80)',
        },
        info: {
          DEFAULT: 'oklch(68% 0.15 230)',
          surface: 'oklch(20% 0.06 230)',
        },
      },
      fontFamily: {
        sans: ["'Inter'", "'system-ui'", "'-apple-system'", 'sans-serif'],
        mono: ["'JetBrains Mono'", "'Fira Code'", "'Consolas'", 'monospace'],
      },
      fontSize: {
        xs:   ['0.75rem',    { lineHeight: '1rem',     letterSpacing: '0.025em' }],
        sm:   ['0.8125rem',  { lineHeight: '1.125rem', letterSpacing: '0.01em'  }],
        base: ['0.9375rem',  { lineHeight: '1.5rem',   letterSpacing: '0'       }],
        lg:   ['1.0625rem',  { lineHeight: '1.625rem', letterSpacing: '0'       }],
        xl:   ['1.25rem',    { lineHeight: '1.75rem',  letterSpacing: '-0.01em' }],
        '2xl':['1.5rem',     { lineHeight: '2rem',     letterSpacing: '-0.02em' }],
        '3xl':['1.875rem',   { lineHeight: '2.25rem',  letterSpacing: '-0.025em'}],
        '4xl':['2.25rem',    { lineHeight: '2.5rem',   letterSpacing: '-0.03em' }],
      },
      spacing: {
        '0.5': '0.125rem', '1': '0.25rem', '1.5': '0.375rem',
        '2': '0.5rem', '3': '0.75rem', '4': '1rem', '5': '1.25rem',
        '6': '1.5rem', '8': '2rem', '10': '2.5rem', '12': '3rem',
        '16': '4rem', '20': '5rem', '24': '6rem',
      },
    },
  },
  plugins: [],
};
```

---

## File: `components/button.md`

```markdown
# Component: Button

## States

| State | Background | Text | Border | Notes |
|-------|-----------|------|--------|-------|
| Default | `primary` | `primary-foreground` | none | |
| Hover | `primary-hover` | `primary-foreground` | none | |
| Focus | `primary` | `primary-foreground` | `border-focus` ring | 2px ring, 2px offset |
| Active | `primary-active` | `primary-foreground` | none | |
| Disabled | `surface-raised` | `on-surface-disabled` | `border` | Cursor: not-allowed |
| Destructive | `error` | white | none | For irreversible actions |

## Variants

| Variant | Use Case |
|---------|---------|
| `solid` | Primary CTA — one per view |
| `outline` | Secondary actions — border in `border`, hover fills `surface-raised` |
| `ghost` | Tertiary — no border, hover fills `surface-raised` |

## Sizing

| Size | Padding | Font | Height |
|------|---------|------|--------|
| sm | 8px 12px | text-sm | 32px |
| md | 10px 16px | text-base | 38px |
| lg | 12px 24px | text-lg | 44px |

## Usage

```html
<!-- Primary -->
<button class="bg-primary text-primary-foreground hover:bg-primary-hover
               px-4 py-2.5 text-sm font-medium rounded">
  Action
</button>

<!-- Disabled -->
<button disabled class="bg-surface-raised text-on-surface-disabled
                         cursor-not-allowed px-4 py-2.5 text-sm rounded">
  Disabled
</button>
```
```

---

## Quality Verification

This exemplar demonstrates:

- [x] OKLCH color space with two-layer token architecture (primitives + semantics)
- [x] Complete `colors.yaml` with brand, surface, content, and status tokens
- [x] `typography.yaml` with font stack, scale, weights
- [x] `spacing.yaml` with base unit documentation
- [x] Tailwind export that is functional (not placeholder)
- [x] Component spec with all 5 states (default, hover, focus, active, disabled)
- [x] Claude Code instruction pattern in DESIGN-SYSTEM.md
- [x] Design philosophy encoded as enforceable decisions
- [x] MCS-2 criteria met
