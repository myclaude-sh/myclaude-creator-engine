# Health Check Definitions

## Dimension 1: Dead Code

### What to check
- Exported symbols not imported anywhere in the codebase
- Files not referenced by any import/require statement
- CSS classes not used in any template/component
- Configuration keys defined but never read

### How to check
```
1. Glob all source files by language (*.ts, *.py, *.go, etc.)
2. Extract exports: grep for "export ", "module.exports", "def ", "func "
3. For each export, grep entire codebase for usage
4. Report: symbol, file, line number, confidence (high if zero refs found)
```

### Scoring
- 0 dead exports: 100
- 1-5%: 80
- 5-15%: 60
- 15-30%: 40
- 30%+: 20

## Dimension 2: Dependency Health

### What to check
- Dependencies with last publish > 1 year ago
- Dependencies with known CVEs
- Dependencies marked as deprecated
- Pinned vs floating version ranges

### Scoring
- 0 issues: 100
- Each stale dep: -5
- Each CVE (high): -15
- Each CVE (medium): -8
- Each deprecated: -10

## Dimension 3: Test Coverage

### What to check
- Ratio of test files to source files
- Test configuration present (jest.config, pytest.ini, etc.)
- CI configuration present (.github/workflows, .gitlab-ci.yml)
- Test scripts in package manifest

### Scoring
- test_ratio × 50 (0.5+ ratio = full marks)
- has_config × 25
- has_ci × 25

## Dimension 4: Security Surface

### Patterns to flag
- API keys: `sk-`, `AIza`, `ghp_`, `xox`
- Secrets: `password=`, `secret=`, `token=` with values
- Dangerous functions: `eval(`, `exec(`, `dangerouslySetInnerHTML`
- Missing .env.example when .env is gitignored

### Scoring
- Each secret pattern: -20
- Each dangerous function: -10
- Missing .env.example: -10

## Dimension 5: Complexity

### Thresholds
- File > 500 lines: hotspot
- Function > 50 lines: hotspot
- Nesting > 4 levels: hotspot
- Cyclomatic complexity > 10: hotspot (if measurable)

### Scoring
- 0 hotspots: 100
- Each hotspot: -5, min 0
