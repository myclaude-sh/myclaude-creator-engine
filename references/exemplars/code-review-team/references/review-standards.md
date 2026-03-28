# Review Standards

## Severity Definitions

| Severity | Meaning | Action Required |
|----------|---------|----------------|
| Critical | Security vulnerability or data loss risk | Block merge |
| High | Bug or significant architectural issue | Request changes |
| Medium | Code quality issue with real impact | Suggest fix |
| Low | Style or minor improvement | Optional |

## Review Principles

1. Every finding has a file, line number, and specific suggestion
2. Focus on behavior, not style (linters handle style)
3. Assess against the codebase's OWN conventions, not ideal conventions
4. Flag patterns, not instances (if the same issue appears 10 times, say so once)
5. Acknowledge good code (not just problems)
