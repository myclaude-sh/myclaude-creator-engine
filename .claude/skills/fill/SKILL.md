---
name: fill
description: >-
  Guide content filling for scaffolded products. Walks each section of a product,
  asks domain questions, and writes the creator's expertise into the product files.
  Replaces the old /create-content. Use after /create when the product is in
  "scaffold" state, or when the creator says "fill", "add content", "write the
  sections", or "help me complete this".
argument-hint: "[product-slug]"
---

# Content Filler

Extract domain expertise from creator conversation and inject into product files.

**When to use:** After /create has generated a scaffold. Product state should be "scaffold" or "content".

**When NOT to use:** If the product doesn't exist yet (use /create first). If the product is already validated (edits will regress state).

---

## Activation Protocol

1. Identify target product:
   - If `$ARGUMENTS` provided, use as product slug → look in `workspace/{slug}/`
   - If not, glob `workspace/*/` and list products in scaffold/content state
   - If multiple products found, ask which one to fill
2. Read `.meta.yaml` from product directory → get type, state, mcs_target
3. Load product spec from `references/product-specs/{type}-spec.md`
4. Load product DNA from `product-dna/{type}.yaml`
5. Load `domain-map.md` if it exists (from /map) → use as knowledge source
6. Scan product files for template placeholders and WHY comments
7. Begin section-by-section guided extraction

---

## Core Instructions

### SECTION WALKER

For each section in the primary file (SKILL.md, AGENT.md, etc.):

1. **Read the WHY comment** — understand what this section needs
2. **Check if content exists** — skip sections already filled
3. **Ask the creator** a targeted question based on:
   - The WHY comment's guidance
   - The product spec requirements
   - The domain-map.md context (if available)
4. **Write the answer** into the section, formatted per the template structure
5. **Show what was written** — let creator approve or edit

### QUESTION STRATEGY

Adapt questions to creator's technical level (from creator.yaml):

- **Beginner:** "In simple terms, what should happen when someone uses this?"
- **Intermediate:** "What specific logic or steps should this section implement?"
- **Expert:** "What's your decision architecture for this? Any edge cases I should encode?"

### SECTION PRIORITY ORDER

Fill sections in this order (most important first):
1. Identity / Purpose (what it is)
2. Activation Protocol (how it starts)
3. Core Instructions (what it does)
4. Quality Gate (how to verify output)
5. Anti-Patterns (what to avoid)
6. References / Knowledge (domain expertise)
7. Examples (demonstrations)
8. Edge cases / Degradation (failure modes)

### AFTER ALL SECTIONS FILLED

1. Update `.meta.yaml`:
   ```yaml
   state:
     phase: "content"  # promote from scaffold
   ```
2. Run quick structural check (Stage 1 of /validate — just file existence)
3. Report:
   ```
   Content filled! {slug} promoted to "content" state.
   Sections filled: {N}/{total}
   Placeholder content remaining: {count}

   Next: /validate to check quality, or edit files directly for fine-tuning.
   ```

---

## Quality Gate

Before promoting to "content" state:
- [ ] Primary file has at least 3 sections with substantive content
- [ ] No sections contain ONLY placeholder/template text
- [ ] README.md has real description (not template boilerplate)
- [ ] At least one domain-specific insight encoded (not generic)

---

## Anti-Patterns

1. **Robotic Q&A** — Don't be a questionnaire. Be conversational. Reference previous answers.
2. **Overwriting creator edits** — If creator has already manually edited a section, don't overwrite. Ask: "This section has content. Want to enhance or replace it?"
3. **Generic fill** — If a section reads like any AI could write it, push: "What's YOUR specific approach here?"
4. **Section overload** — Don't try to fill everything in one session. Offer: "We covered the core sections. Want to continue or save progress?"
5. **Ignoring domain-map** — If domain-map.md exists, USE it. Don't re-ask questions already answered.
