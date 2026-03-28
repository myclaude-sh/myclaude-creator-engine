# README Guide

A strong README earns the install decision in 30 seconds (H: Q1). This guide
covers required sections, good vs. bad examples, and marketplace optimization.

---

## Required Sections

Every README must include these sections in this order:

1. **Product name and one-liner** (above the fold)
2. **What it does** (expanded, 2-4 sentences)
3. **Quick Start** (fastest path to working)
4. **Installation** (full requirements and steps)
5. **Usage** (concrete examples with real commands/outputs)
6. **Requirements** (everything needed to use it)

Optional but recommended:
- Configuration
- Architecture (for applications)
- Known limitations
- CHANGELOG link

---

## The First Paragraph Rule

The first paragraph is the most important text in any README. It determines whether
a buyer continues reading or closes the tab.

**The first paragraph must answer:**
- What does this specifically do?
- Who is it for?
- Why is it better than "just using Claude" for this task?

### Good First Paragraph

```markdown
# Security Audit Skill

Analyzes Node.js and TypeScript code for OWASP Top 10 vulnerabilities, authentication
issues, and secret exposure. Produces remediation-ready findings with specific file:line
references and code fix examples.

For teams who want Claude Code to be a security audit partner — not just a code
generator. Implements the OWASP methodology systematically instead of ad-hoc review.
```

**Why it works:**
- First sentence delivers the specific capability immediately
- Second paragraph explains the value proposition and differentiator
- Reader understands exactly what they're getting after 3 sentences

### Weak First Paragraph

```markdown
# Security Helper

This is a useful skill for anyone who works with code. It can help you with many
security-related tasks. Claude Code is a powerful AI assistant and this skill
makes it even better at security.
```

**Why it fails:**
- "Useful skill for anyone who works with code" — who specifically?
- "Many security-related tasks" — which ones?
- "Makes it even better" — better than what baseline?

---

## Quick Start Section

The Quick Start is for the buyer who wants to try it immediately, not read the full
docs. 3-5 steps maximum. Must actually work.

**Good Quick Start:**
```markdown
## Quick Start

```bash
# Install
cp SKILL.md ~/.claude/skills/security-audit/SKILL.md

# Use
/security-audit src/auth/middleware.ts
```

Expected output: A structured security findings report for the specified file.
```

**Weak Quick Start:**
```markdown
## Quick Start

See the Installation section for setup instructions, then the Usage section
for how to use this product.
```

The weak version gives the buyer nothing — it just redirects them to sections they
haven't read yet.

---

## Installation Section

Must include:
1. Specific version requirements (not "Node.js", but "Node.js 20+")
2. Exact installation commands
3. A verification step (how to confirm it worked)

**Good installation block:**
```markdown
## Installation

**Requirements:**
- Claude Code (any version)
- Node.js 20+ (for the CLI tool component)

**Install:**
```bash
cp -r . ~/.claude/skills/security-audit/
```

**Verify:**
Type `/security-audit --help` in Claude Code.
Expected: Shows the skill's help text.
```

**What to avoid:**
- "Requirements: Claude Code, some technical knowledge" — not actionable
- No verification step — buyer can't confirm it worked

---

## Usage Section

Usage examples must:
1. Show real commands (not `[command]` placeholders)
2. Show real expected output (not just "produces a report")
3. Cover the 2-3 most common use cases

**Good usage example:**
```markdown
## Usage

**Basic — analyze a file:**
```
/security-audit src/auth/login.ts
```

Output example:
```
## Security Audit: src/auth/login.ts
Findings: 1 critical, 0 high, 2 medium

CRITICAL: Hardcoded JWT secret at line 12
  Evidence: `const secret = "my-secret-key"`
  Fix: Use `process.env.JWT_SECRET` instead
```

**Advanced — analyze a directory:**
```
/security-audit --depth=radical src/auth/
```
```

**Weak usage example:**
```markdown
## Usage

Use this skill to analyze your code. Simply type the command in Claude Code
and it will produce helpful security information.
```

---

## Requirements Section

List every external dependency:
- Runtime versions (specific)
- External services (APIs, databases, auth providers)
- Claude Code version if applicable
- Operating system restrictions if any

**Good requirements:**
```markdown
## Requirements

- Claude Code (any version — tested on CC 1.0.x)
- Node.js 20.11.0+ (for the link-checking component)
- Git (for the diff analysis workflow)
- No external API keys required
```

**Weak requirements:**
```markdown
## Requirements

- Claude Code
- Some technical knowledge
```

---

## Marketplace Optimization Tips

### First 160 characters are the description field

The marketplace search result shows the product name and description (max 160 chars).
Write your first sentence with this constraint in mind.

```
"Analyzes Node.js code for OWASP vulnerabilities. Produces findings with file:line
references and code fix examples."
```
That's 114 characters — complete, specific, fits the constraint.

### Use the category wisely

Don't cross-list. If your product is a skill, list it as a skill — not as a system
just to appear in more searches. Buyers filter by category and expect the right
product type.

### Version history signals trust

A product at v2.1.0 signals active maintenance. A product at v1.0.0 signals "just
published." Update your version as you improve the product — even minor improvements
justify a PATCH bump.

### The README is the product in the listing view

For skills, agents, and prompts, buyers see the README before they buy. The README IS
the sales page. Treat it as such:
- No jargon without definition
- Benefits, not just features
- Real examples, not toy examples
- No TODOs or placeholders visible

---

## README Checklist

Before publishing:

- [ ] First paragraph answers: what, for whom, why different
- [ ] Quick Start: 3-5 steps, actually works on clean install
- [ ] Installation: specific version numbers, verification step
- [ ] Usage: 2+ real examples with real commands and expected output
- [ ] Requirements: complete list, nothing implicit
- [ ] No placeholder text anywhere
- [ ] No broken links (test all links before publishing)
- [ ] CHANGELOG link if version > 1.0.0
