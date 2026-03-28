# Sample Report

```
CODE HEALTH REPORT — my-web-app
Generated: 2026-03-28 | Scope: src/ | Files: 142

OVERALL HEALTH: 73/100 (C — Fair)

  Dead Code        85/100  █████████░  3 unused exports
  Dependencies     62/100  ██████░░░░  5 stale, 1 vulnerable
  Test Coverage    58/100  ██████░░░░  32% file coverage
  Security Surface 90/100  █████████░  1 finding
  Complexity       78/100  ████████░░  4 hotspots

TOP PRIORITIES (fix these first):
  1. src/lib/auth.ts:45 — hardcoded API key pattern detected — security
  2. package.json — lodash@4.17.15 has CVE-2021-23337 — dependency
  3. src/components/Dashboard.tsx — 612 lines, 8 functions — complexity

DETAILED FINDINGS: 14 total across 5 dimensions
```
