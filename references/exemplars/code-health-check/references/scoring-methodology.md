# Scoring Methodology

## Overall Score

```
OVERALL = (Dead Code × 0.15)
        + (Dependencies × 0.20)
        + (Test Coverage × 0.25)
        + (Security × 0.20)
        + (Complexity × 0.20)
```

## Grade Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Excellent health — maintain |
| 75-89 | B | Good health — minor improvements |
| 60-74 | C | Fair — needs attention |
| 40-59 | D | Poor — significant tech debt |
| 0-39 | F | Critical — immediate action needed |

## Priority Ordering

Findings are ordered by:
1. Security issues first (highest blast radius)
2. Dependency vulnerabilities (external risk)
3. Complexity hotspots (maintenance burden)
4. Test gaps (regression risk)
5. Dead code (cognitive burden)

Within each category, order by: file importance (entry points > utilities > tests).
