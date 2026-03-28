---
name: full-suite
description: >-
  Complete documentation pipeline: scan, extract, generate, validate.
  Produces README + Architecture doc + API reference.
disable-model-invocation: true
---

# Full Documentation Suite

## Steps

1. **Scan** — Glob project, identify languages, entry points, structure
2. **Extract** — Route to doc-analyst for deep analysis
3. **Generate README** — Route to quick-doc with analysis context
4. **Generate Architecture** — Write architecture doc from analyst output
5. **Validate** — Check all generated docs for accuracy and completeness

## Output

- README.md (generated or enhanced)
- ARCHITECTURE.md (generated)
- api-reference.md (if API endpoints detected)
