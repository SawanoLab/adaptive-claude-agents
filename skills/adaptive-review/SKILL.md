# Adaptive Review - Phase-Aware Code Review Skill

**Status**: Phase 3 Implementation
**Type**: Global Claude Skill
**Purpose**: Automatically adjust code review rigor based on development phase

---

## Overview

This Skill analyzes your project's development maturity and applies appropriate review standards:

- **Prototype**: Light review - "Does it work?"
- **MVP**: Moderate review - "Is it secure and maintainable?"
- **Production**: Strict review - "Is it production-ready?"

## How It Works

### 1. Phase Detection

The skill analyzes 7 signals to determine your project's phase:

| Signal | Weight | What It Checks |
|--------|--------|----------------|
| **User Config** | 100% | `.claude/phase.yml` (manual override) |
| **Version Number** | 30% | package.json/pyproject.toml version |
| **Git History** | 20% | Commit count, tags, activity |
| **Test Coverage** | 15% | Test files, coverage config |
| **CI/CD** | 15% | GitHub Actions, GitLab CI, etc. |
| **Documentation** | 10% | README, CONTRIBUTING, etc. |
| **Code Structure** | 10% | Project organization |

**Example Detection**:

```bash
# Your project:
# - Version 0.1.0
# - 15 commits
# - 3 test files
# - No CI/CD

→ Detected: MVP phase (confidence: 68%)
```

### 2. Phase-Aware Review

Each phase has different review rules:

#### Prototype Phase (Rigor: 3/10)

**Focus**: Speed and iteration

✅ **Checks**:
- Basic functionality
- Critical bugs only

❌ **Skips**:
- Type safety
- Test coverage
- Performance optimization
- Code style

**Review Tone**: Encouraging, minimal friction

#### MVP Phase (Rigor: 6/10)

**Focus**: Core features working reliably

✅ **Checks**:
- Type safety (moderate)
- Basic security (SQL injection, XSS)
- Main feature documentation
- 50%+ test coverage (recommended)

❌ **Skips**:
- Advanced optimization
- Perfect code style
- Edge case handling

**Review Tone**: Constructive, balanced

#### Production Phase (Rigor: 10/10)

**Focus**: Production-ready quality

✅ **Checks**:
- Strict type safety (no `any` types)
- Comprehensive security audit
- 80%+ test coverage (required)
- Full API documentation
- Performance optimization
- Accessibility (WCAG 2.1 AA)

**Review Tone**: Thorough, uncompromising

---

## Usage

### Automatic Detection

The skill runs automatically when you ask for code review:

```
You: Review this code for production readiness

Claude: [Detects phase: Production (confidence: 85%)]
        Applying production-level review standards...

        Found 3 critical issues:
        1. Missing error handling in API endpoint
        2. No input validation
        3. Test coverage: 45% (requires 80%+)
```

### Manual Override

Create `.claude/phase.yml` to override auto-detection:

```yaml
phase: prototype  # or 'mvp', 'production'
reason: "Rapid prototyping for client demo"
expires: 2025-11-01  # Optional: auto-revert to detection
```

### Check Current Phase

```
You: What development phase am I in?

Claude: [Runs phase detection]

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Development Phase: MVP
        Confidence: 68%
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        Indicators:
        • Version 0.5.0 (0.x.x) → MVP
        • 87 commits → MVP stage
        • 12 test files → basic testing
        • README + 2 doc files

        Review Standards:
        - Type safety: Moderate
        - Test coverage: 50%+ recommended
        - Security: Basic checks
```

---

## Configuration Files

Located in: `skills/adaptive-review/phase_configs/`

### prototype.yaml

```yaml
phase_name: prototype
review_rigor: 3  # 1-10 scale
rules:
  type_safety:
    enabled: false
  testing:
    min_coverage: 0
  security:
    level: defer
```

### mvp.yaml

```yaml
phase_name: mvp
review_rigor: 6
rules:
  type_safety:
    enabled: true
    strictness: moderate
  testing:
    min_coverage: 50
  security:
    level: basic
```

### production.yaml

```yaml
phase_name: production
review_rigor: 10
rules:
  type_safety:
    enabled: true
    strictness: strict
    no_any_types: true
  testing:
    min_coverage: 80
    required: true
  security:
    level: comprehensive
```

---

## Troubleshooting

### Wrong Phase Detected?

**Problem**: "Detected as prototype but I'm in MVP"

**Solutions**:
1. Check version number: Use `0.x.x` for MVP, `1.x.x` for production
2. Add tests: More test files → higher phase
3. Manual override: Create `.claude/phase.yml`

### Phase Detection Too Conservative?

**Problem**: "I have tests but still detected as prototype"

**Solution**: Increase maturity signals:
- Add CI/CD (GitHub Actions)
- Bump version to 0.1.0+
- Add CONTRIBUTING.md and CHANGELOG.md

### Want Stricter Review in Prototype?

**Solution**: Use manual override to force higher phase:

```yaml
# .claude/phase.yml
phase: production
reason: "Learning best practices from day 1"
```

---

## Best Practices

### Phase Transitions

**Prototype → MVP**:
- ✅ Bump version to 0.1.0
- ✅ Add 10+ test files
- ✅ Create README and basic docs

**MVP → Production**:
- ✅ Bump version to 1.0.0
- ✅ Add CI/CD pipeline
- ✅ Achieve 80%+ test coverage
- ✅ Add CONTRIBUTING.md, CHANGELOG.md

### When to Use Manual Override

✅ **Good reasons**:
- Time-boxed prototyping
- Learning/educational projects
- Client demos
- Hackathons

❌ **Bad reasons**:
- Avoiding legitimate technical debt
- Skipping security in production
- Ignoring test coverage requirements

---

## Examples

### Example 1: New Project (Prototype)

```
Project state:
- package.json: "version": "0.0.1"
- 5 commits
- 0 test files

Detection: Prototype (confidence: 85%)

Review behavior:
✓ Focuses on functionality
✓ Ignores TODO comments
✓ Skips style nitpicks
✗ No test coverage requirements
```

### Example 2: Growing MVP

```
Project state:
- package.json: "version": "0.3.0"
- 95 commits
- 15 test files
- README + CONTRIBUTING

Detection: MVP (confidence: 72%)

Review behavior:
✓ Checks basic security (XSS, SQL injection)
✓ Recommends tests for new features
✓ Flags type safety issues
✗ Allows some TODO comments
✗ Lenient on code style
```

### Example 3: Production Release

```
Project state:
- package.json: "version": "1.2.0"
- 450 commits, 12 tags
- 120 test files
- CI/CD: GitHub Actions
- Full documentation

Detection: Production (confidence: 92%)

Review behavior:
✓ Strict type checking
✓ Requires 80%+ coverage
✓ Full security audit
✓ Performance analysis
✓ Accessibility checks
✗ No TODO comments allowed
```

---

## Implementation Details

### Python Module: detect_phase.py

```python
from skills.adaptive_review.detect_phase import detect_development_phase

result = detect_development_phase("/path/to/project")
print(f"Phase: {result.phase}")
print(f"Confidence: {result.confidence:.1%}")
```

### Integration with Subagents

When generating subagents, phase information is included:

```markdown
---
name: python-reviewer
phase: mvp
phase_confidence: 0.72
---

You are a Python code reviewer operating in **MVP phase**.

Apply moderate review standards:
- Check basic security
- Recommend 50%+ test coverage
- Allow TODO comments
```

---

## Roadmap

### Current (v1.0)
- ✅ 7-signal phase detection
- ✅ 3 phase configurations
- ✅ Manual override support

### Future (v1.1)
- [ ] Per-file phase detection (monorepos)
- [ ] Custom phase configurations
- [ ] Phase transition recommendations

### Future (v1.2)
- [ ] ML-based phase prediction
- [ ] Integration with project management tools
- [ ] Team collaboration features

---

## References

- [Phase Detection Design](../../docs/internal/PHASE3_DESIGN.md)
- [Configuration Files](./phase_configs/)
- [Detection Script](./detect_phase.py)
- [Project Analyzer Integration](../project-analyzer/)

---

**Note**: This is the **first AI coding assistant** to implement phase-aware code review. This feature differentiates Adaptive Claude Agents from all other tools (GitHub Copilot, Cursor, etc.).
