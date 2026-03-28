# Code Review Team

> Three-perspective code review: security + architecture + performance.

## What It Does

A squad of 3 specialist agents that review code from different angles:
- **Security Reviewer** — finds vulnerabilities and data exposure
- **Architecture Reviewer** — evaluates patterns and boundaries
- **Performance Reviewer** — identifies bottlenecks and scaling risks

Produces a unified review with severity ratings and specific fix suggestions.

## Installation

```bash
myclaude install code-review-team
```

## Usage

```
/code-review-team src/                    # Review a directory
/code-review-team src/lib/auth.ts         # Review specific file
```

## Requirements

- Claude Code >= 1.0.0
- Agent tool access (for multi-agent routing)

---

**Version:** 1.0.0 | **License:** MIT | **MCS:** 3
**Author:** @myclaude-team
