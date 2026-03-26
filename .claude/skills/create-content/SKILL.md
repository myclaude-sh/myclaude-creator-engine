---
name: create-content
description: >-
  Guide a creator through filling their scaffolded product with real content, section
  by section. Extracts domain expertise through targeted questions, drafts content
  using the creator's knowledge, and adapts approach based on creator type (developer,
  domain-expert, marketer, prompt-engineer). Use after /create when the scaffold exists
  but content is empty, when the creator says "help me fill this", "write content",
  "I don't know what to put here", or "build the content".
argument-hint: "[product-path]"
---

# Content Creator

Transform a scaffolded product into a complete, content-rich artifact by extracting
the creator's domain expertise through guided conversation.

## Why This Skill Exists

The biggest drop-off in the creation pipeline is between "scaffold generated" and
"product ready to validate." Creators — especially non-developers — face a blank
canvas problem: the structure is there but the content sections are empty. This skill
bridges that gap by acting as a co-writer, not just a scaffolder.

---

## Activation Protocol

1. Read `creator.yaml` — load expertise domains, technical level, creator type
2. Identify the product to work on:
   - If argument provided → use that path
   - If not → scan `workspace/` for products, ask which one
3. Read the product's primary definition file (SKILL.md, AGENT.md, etc.)
4. Identify all sections with `<!-- GUIDANCE: ... -->` comments — these are unfilled
5. Load the relevant exemplar from `references/exemplars/{category}-exemplar.md`
6. Load the product spec from `references/product-specs/{category}-spec.md`

---

## Core Instructions

### Approach by Creator Type

Adapt the conversation based on `creator.yaml → profile.type`:

| Creator Type | Content Extraction Strategy |
|---|---|
| **developer** | Ask for technical specs, code patterns, tool integrations. Draft from architecture perspective. |
| **domain-expert** | Extract domain knowledge through "teach me" questions. "Walk me through how you'd solve this for a client." Draft from their explanation. |
| **prompt-engineer** | Ask about input/output contracts, edge cases, context engineering. Draft from cognitive flow perspective. |
| **marketer** | Ask about audience, pain points, outcomes. Draft from value proposition perspective. |
| **agency** | Ask about client patterns, repeatable workflows, team processes. Draft from scalability perspective. |

### Section-by-Section Flow

For each unfilled section in the product, execute this loop:

**Step 1 — Context from exemplar**
Show the creator what this section looks like in the exemplar:
"In the reference example, the Activation Protocol looks like this: [condensed excerpt]. Yours needs to do something similar for your domain."

**Step 2 — Extract expertise**
Ask 1-2 targeted questions based on the section purpose. Never ask more than 2 at a time.

For **Activation Protocol:**
- "What files or knowledge should be loaded before your skill responds? What does it need to know?"
- "In what order should the context load — what comes first?"

For **Core Instructions:**
- "Walk me through the step-by-step process you'd follow when doing this task manually."
- "What's the first thing you check? What comes after?"

For **Quality Gate:**
- "Before you'd hand this output to a client, what would you check? What would make it fail?"

For **When to Use / When NOT to Use:**
- "What's the specific situation where someone needs this? And when should they NOT use it?"

For **Anti-Patterns:**
- "What are the most common mistakes people make in your domain? What do beginners get wrong?"

For **Examples:**
- "Give me a real scenario where you used this expertise. What was the input? What did you produce?"

**Step 3 — Draft content**
Based on the creator's answers, draft the section content in the style of the exemplar.
Show the draft to the creator: "Here's my draft based on what you told me. Edit freely."

**Step 4 — Refine**
If the creator edits or gives feedback, incorporate it. If they approve, write to the file and move to the next section.

### Writing Principles

- Draft in the creator's voice, not generic AI voice
- Use their terminology, not textbook language
- Be specific — "Analyze Solidity contracts for reentrancy" not "Analyze code for security"
- If the creator's answer is vague, push for specificity: "Can you give me a concrete example?"
- Reference the exemplar as calibration, not as template to copy

### Handling Ambiguity

If the creator doesn't know what to put in a section:
1. Show the exemplar's version of that section
2. Ask: "Does your skill need something similar? What would be different?"
3. If still stuck: "Let me draft something based on your expertise domains. You can rewrite."
4. Never leave a section empty — draft SOMETHING based on available context

---

## Output Structure

After each section is filled:
```
Section completed: {section name}
  Status: drafted / creator-edited / approved
  Words: {count}

Progress: {filled}/{total} sections complete
Next: {next unfilled section}
```

After all sections filled:
```
Content creation complete for {product-name}!
  Sections filled: {N}
  Estimated MCS readiness: MCS-{level}

Next steps:
  - Review the full product: workspace/{slug}/{PRIMARY_FILE}
  - Run /validate to check quality
  - Run /validate --level=2 if targeting MCS-2
```

---

## Quality Gate

Before marking a section as complete:
- [ ] Content is specific to the creator's domain, not generic
- [ ] Content follows the structure shown in the exemplar
- [ ] No placeholder text remains (TODO, lorem ipsum, coming soon)
- [ ] Section meets the minimum requirements from the product spec
- [ ] Creator has reviewed and approved (or explicitly said "good enough for now")

---

## Anti-Patterns

- **Template copying**: Don't copy the exemplar's content — use it as structural reference only
- **Over-questioning**: Don't ask 10 questions before writing anything. Ask 1-2, draft, refine.
- **Generic language**: "This skill helps with security" → push for "This skill detects reentrancy vulnerabilities in Solidity smart contracts"
- **Perfectionism trap**: A "good enough" draft the creator can edit beats a perfect draft they waited 30 minutes for
- **Ignoring creator type**: A developer and a domain expert need completely different extraction approaches
