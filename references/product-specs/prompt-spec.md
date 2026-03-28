# Product Spec: Prompts

## Definition

Prompts are system prompts, context payloads, and structured instructions for specific
use cases. They are the most focused product type — a well-crafted prompt solves a
specific problem by encoding the right context, constraints, and output structure into
an instruction set.

A prompt is NOT:
- A skill (prompts don't have activation protocols or knowledge bases; they are the instruction themselves)
- A CLAUDE.md config (configs are project-level persistent rules; prompts are task-specific)
- A chat message (prompts are reusable templates, not one-time messages)

A prompt IS:
- A complete, reusable instruction set for a defined task
- Parameterizable via customizable variables
- Variantable for different contexts (concise, detailed, expert)

---

## Canonical File Structure

```
prompt-name/
├── PROMPT.md              # The prompt itself (REQUIRED)
├── README.md              # Usage documentation (REQUIRED)
├── variants/              # Contextual variants
│   ├── concise.md
│   ├── detailed.md
│   └── expert.md
├── examples/              # Example outputs
│   ├── example-1.md
│   └── example-2.md
├── config/
│   └── variables.yaml     # Customizable variables
└── CHANGELOG.md           # Version history
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `PROMPT.md` | The actual prompt | MCS-1 |
| `README.md` | What it does, how to use it, when to use which variant | MCS-1 |
| `examples/example-1.md` | At least 1 example output | MCS-1 |

---

## Required Sections in PROMPT.md

### 1. Header Metadata

```markdown
# Prompt Name

**Version:** 1.0.0
**Target Use Case:** [One sentence — who uses this and for what]
**Tone:** [formal | conversational | technical | creative]
**Output Format:** [markdown | JSON | prose | structured text]
```

### 2. System Prompt (The Core)

The actual prompt text. This is the product. It should:
- Establish context before giving instructions
- Use explicit constraints ("always", "never", "when X then Y")
- Define output structure clearly
- Handle the most common edge cases inline

### 3. Variables Section

All customizable values with defaults:

```markdown
## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `{{AUDIENCE}}` | "software developers" | Target audience |
| `{{TONE}}` | "professional" | Writing tone |
| `{{FORMAT}}` | "markdown" | Output format |
```

### 4. Usage Instructions

How to use this prompt:
- Where to place it (system prompt slot, context injection, etc.)
- How to customize variables
- Which variant to use in which context

### 5. Limitations

What the prompt will NOT do well:
- Input types that degrade quality
- Context conditions that break the prompt
- Edge cases the prompt doesn't handle

---

## MCS Requirements

### MCS-1: Publishable

**Universal:**
- [ ] Valid PROMPT.md with core prompt and metadata
- [ ] README.md with: what it does, how to use, requirements
- [ ] At least 1 example output in `examples/`
- [ ] Metadata complete
- [ ] No syntax errors
- [ ] License from approved list
- [ ] No hardcoded secrets

**Prompt-Specific:**
- [ ] Variables identified and documented
- [ ] Use case clearly specified (not "general writing")
- [ ] Output format specified

### MCS-2: Quality

**Universal (beyond MCS-1):**
- [ ] 3+ example outputs covering different scenarios
- [ ] Variants directory with at least 2 contextual variants
- [ ] Customizable variables in `config/variables.yaml`
- [ ] Anti-patterns section
- [ ] Tested with 5 different input types
- [ ] No placeholder content
- [ ] Semver versioning

**Prompt-Specific:**
- [ ] Variants cover meaningfully different use contexts (not just length variations)
- [ ] Examples show realistic inputs producing realistic outputs
- [ ] Variables cover the most common customization needs
- [ ] Limitations section documents where the prompt breaks down

### MCS-3: State-of-the-Art

**Universal (beyond MCS-2):**
- [ ] Context engineering structure documented (how context is loaded/injected)
- [ ] Composable (can be combined with other prompts or used as system prompt layer)
- [ ] Stress-tested with adversarial inputs
- [ ] Cognitive architecture documented (why this structure works)
- [ ] CHANGELOG with versioning
- [ ] 5+ examples including difficult cases
- [ ] Token efficiency documented (what's in vs. what's out)
- [ ] Differentiation statement

**Prompt-Specific:**
- [ ] Context injection strategy (how variables are injected without breaking structure)
- [ ] Prompt chaining pattern documented (how outputs from this prompt feed into others)
- [ ] Anti-injection safeguards if the prompt is user-facing

---

## Anti-Patterns for Prompts

### Structural
- **Entire prompt in README:** The prompt text is in the README, not in PROMPT.md. Structure signal matters — buyers expect the product file to contain the product.
- **No variants:** One prompt for all contexts. A technical writing prompt used by a marketer and a principal engineer needs different variants.
- **Variables not documented:** Prompt contains `[COMPANY NAME]` and `[TARGET AUDIENCE]` with no documentation of what goes there.

### Content
- **Vague instructions:** "Write professionally" — what does professional mean for this prompt? Specific constraints produce specific results.
- **Missing edge case handling:** Prompt handles the 80% case but has no instructions for what to do when input is ambiguous or malformed.
- **Example outputs that are too short:** 3-sentence examples that don't show the real output quality. Examples should be full-length, real outputs.

### Quality
- **No stress test:** Prompt was only tested with cooperative inputs. Adversarial or confusing inputs reveal whether the prompt is robust.
- **Variants that differ only in length:** "Concise" is 2 paragraphs, "detailed" is 5 paragraphs. Real variants have different structural approaches, not just length.

---

## Discovery Questions (from §7)

When creating a prompt, answer these before scaffolding:

1. What specific task does this prompt address? (one task, not "writing assistance")
2. Who is the target user? (what role, what context, what expertise level)
3. What output format is expected? (markdown doc, JSON, structured list, prose, etc.)
4. What variables should be customizable? (audience, tone, format, domain, etc.)
5. What tone or voice should the prompt enforce?
6. What are the edge cases the prompt must handle? (ambiguous input, missing context, etc.)
7. What are the 2-3 most common ways this prompt will be misused?

---

## DNA Requirements

For the complete DNA pattern applicability matrix for this product type,
see `product-dna/prompt.yaml`. That file defines:
- Which of the 18 DNA patterns (D-01 to D-18) are required vs optional
- Validation checks per pattern (grep/glob commands)
- Template file mapping with DNA injection points
- Frontmatter fields (Anthropic Agent Skills spec)
- Discovery questions for /create

**MCS scoring:** `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
See `references/quality/mcs-spec.md` for full scoring formula.
