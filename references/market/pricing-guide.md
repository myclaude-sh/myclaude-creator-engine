# Pricing Guide

Pricing benchmarks per category and MCS level. H7: "Price based on value to the
buyer, not effort to create." H8: "MCS-3 products charge 5-10x more than MCS-1."

---

## Pricing Philosophy

Three principles govern marketplace pricing:

1. **Value-to-buyer, not effort-to-create (H7):** A 2-hour MCS-3 skill that saves a
   security professional 4 hours of auditing per week justifies $49+. A 40-hour
   generic agent that doesn't save anyone time should be free.

2. **MCS scales with price (H8):** MCS-3 products charge 5-10x more than MCS-1.
   Quality investment should be rewarded. If you've built to MCS-3, price accordingly.

3. **Free products build reputation (M3):** Free products are a strategic investment
   in visibility and reviews. They lead buyers to paid products.

---

## Pricing Benchmarks by Category and MCS Level

### Skills

| MCS Level | Suggested Range | Sweet Spot |
|-----------|---------------|-----------|
| MCS-1 | Free — $9 | Free (builds reviews) |
| MCS-2 | $9 — $29 | $15 |
| MCS-3 | $29 — $79 | $49 |

**Example:** A systematic reasoning skill at MCS-3 → $49. Justification: saves 1+ hour
of analysis time per use for professionals charging $200+/hr.

---

### Agents

| MCS Level | Suggested Range | Sweet Spot |
|-----------|---------------|-----------|
| MCS-1 | Free — $15 | $9 |
| MCS-2 | $15 — $49 | $29 |
| MCS-3 | $49 — $99 | $69 |

**Example:** Security Audit Agent at MCS-3 → $69. Justification: provides specialist
security review that typically costs $250+/hr from a consultant.

---

### Squads

| MCS Level | Suggested Range | Sweet Spot |
|-----------|---------------|-----------|
| MCS-1 | $15 — $39 | $25 |
| MCS-2 | $39 — $99 | $59 |
| MCS-3 | $99 — $249 | $149 |

**Example:** Content Production Squad at MCS-3 → $149. Justification: replaces
strategist + writer + editor for a content cycle.

---

### Workflows

| MCS Level | Suggested Range | Sweet Spot |
|-----------|---------------|-----------|
| MCS-1 | Free — $9 | Free |
| MCS-2 | $9 — $29 | $15 |
| MCS-3 | $29 — $59 | $39 |

---

### Design Systems

| MCS Level | Suggested Range | Sweet Spot |
|-----------|---------------|-----------|
| MCS-1 | Free — $19 | Free (for community) or $9 |
| MCS-2 | $19 — $59 | $29 |
| MCS-3 | $59 — $149 | $79 |

**Note:** Design systems with unique aesthetic value can command premium pricing.
A distinctive, battle-tested DS is worth more than a generic one.

---

### Prompts

| MCS Level | Suggested Range | Sweet Spot |
|-----------|---------------|-----------|
| MCS-1 | Free | Free |
| MCS-2 | Free — $9 | Free or $5 |
| MCS-3 | $9 — $29 | $15 |

**Note:** Prompts have the lowest price ceiling because alternatives are everywhere.
The value must be extraordinarily clear to charge above $15.

---

### CLAUDE.md Configurations

| MCS Level | Suggested Range | Sweet Spot |
|-----------|---------------|-----------|
| MCS-1 | Free | Free |
| MCS-2 | Free — $15 | Free or $9 |
| MCS-3 | $15 — $49 | $25 |

**Example:** Next.js Enterprise CLAUDE.md at MCS-3 → $25. Justification: replaces
2-3 hours of setup time for a common project type.

---

### Applications

| MCS Level | Suggested Range | Sweet Spot |
|-----------|---------------|-----------|
| MCS-1 | Free — $19 | Free or $9 |
| MCS-2 | $19 — $59 | $29 |
| MCS-3 | $59 — $199 | $99 |

**Note:** Applications have the highest potential ceiling because buyers experience
immediate, concrete value. A working CLI tool that solves a real problem can
command $99+.

---

### Systems

| MCS Level | Suggested Range | Sweet Spot |
|-----------|---------------|-----------|
| MCS-1 | $29 — $69 | $39 |
| MCS-2 | $69 — $199 | $99 |
| MCS-3 | $199 — $499 | $249 |

**Example:** Research Intelligence System at MCS-3 → $249. Justification: provides
a complete research pipeline that replaces a research assistant for specific use cases.

---

## Factors That Increase Justified Price

| Factor | Impact | Why |
|--------|--------|-----|
| **Domain specificity** | +20-40% | Narrow problems have fewer alternatives |
| **Encoded proprietary methodology** | +30-50% | Unique IP that can't be replicated by competitors |
| **Time saved > 1 hour per use** | +$10-30 | Clear ROI calculation supports the price |
| **Replaces professional service** | +50-100% | Priced against consultant rates, not software |
| **Creator reputation / Domain Authority badge** | +15-25% | Trust reduces purchase friction |
| **Regular updates and maintenance** | +10-20% | Signals long-term support |

## Factors That Decrease Justified Price

| Factor | Impact | Why |
|--------|--------|-----|
| **Generic use case** | -30-50% | Alternatives exist; buyer has negotiating power |
| **MCS-1 only** | -60% from MCS-3 ceiling | Minimum quality; some buyers won't pay |
| **No changelog or maintenance signals** | -10-20% | Buyers don't trust long-term viability |
| **Similar products exist at lower price** | Price match required | Competition anchors expectation |

---

## Pricing Strategy Patterns

### Freemium Pattern

Publish MCS-1 or MCS-2 version free. Build reviews. Publish MCS-3 upgrade paid.

Example:
- `security-audit-skill` v1.0.0 → Free (MCS-1, builds reviews)
- `security-audit-skill` v2.0.0 → $39 (MCS-3, full methodology)

---

### Domain Series Pattern

Build 3-5 skills in the same domain at different price points.

Example:
- `code-review-quick` → Free (MCS-2, basic review)
- `code-review-typescript` → $19 (MCS-2, TypeScript-specific)
- `code-review-security-focused` → $49 (MCS-3, security overlay)

Buyers who love one are likely to buy others in the series.

---

### System = Sum of Parts + Premium

Price a system at roughly 60% of the sum of its components' individual prices.
Buyers pay for integration value, not just component count.

Example:
- `analysis-skill` at $19 + `synthesis-skill` at $19 + `report-workflow` at $15 = $53
- `research-intelligence-system` at MCS-3 → $99 (86% premium over buying separately,
  but 46% discount vs. sum — integration value justification)

---

## Free vs. Paid Decision Framework

```
Is this a reference implementation or community contribution?
  → Free (CC0 license)

Do you want to build reviews and reputation in a category?
  → Free at MCS-1 or MCS-2

Does this solve a narrow, specific, high-value problem?
  → Paid — price at value to buyer

Does this replace professional services (consultant, agency)?
  → Paid — premium tier ($99+)

Is this a first product with no reviews yet?
  → Free to build trust, then paid upgraded version
```
