---
name: quick-doc
description: >-
  Fast README generation from codebase analysis. Reads entry points,
  extracts purpose, generates structured README.
allowed-tools: [Read, Glob, Grep]
---

# Quick Doc

> Generate a README by reading the code, not imagining it.

## Protocol

1. Glob for entry points (index.*, main.*, app.*, package.json)
2. Read entry point to extract: purpose, exports, dependencies
3. Read package manifest for: name, description, scripts
4. Generate README with: What, Install, Usage, Requirements
5. If existing README found: compare and suggest enhancements

## Output

Standard README.md following the 4-section MCS-1 requirement.
