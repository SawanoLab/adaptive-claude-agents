# Quick Start Guide (5 Minutes)

Get started with Adaptive Claude Agents in just 5 minutes!

---

## What You'll Learn

- ✅ How to install Adaptive Claude Agents
- ✅ How to analyze your first project
- ✅ How to use auto-generated subagents
- ✅ How to check your development phase

---

## Step 1: Install (1 minute)

### One-Command Installation

```bash
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
```

**What this does**:

- ✓ Checks system requirements (Python 3.9+, git)
- ✓ Detects your Claude Code skills directory
- ✓ Installs all skills and templates
- ✓ Validates the installation

**Expected output**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Adaptive Claude Agents Installation
  Version: 1.0.0-beta
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ System check passed
✓ Claude Code skills directory found
✓ Installation complete!
```

### Manual Installation (if needed)

If the one-liner doesn't work:

```bash
# 1. Clone the repository
git clone https://github.com/SawanoLab/adaptive-claude-agents.git

# 2. Run install script
cd adaptive-claude-agents
./install.sh
```

---

## Step 2: Analyze Your Project (2 minutes)

### Open Your Project in Claude Code

1. Open Claude Code
2. Navigate to any project (Next.js, FastAPI, PHP, etc.)

### Run Project Analysis

In Claude Code, type:

> "Analyze my project and generate appropriate subagents"

**What happens**:

```
🔍 Analyzing project structure...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detected Tech Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework:     Next.js 14
Language:      TypeScript
Styling:       Tailwind CSS
Testing:       Vitest + Testing Library
Confidence:    95%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Generating subagents...
  ✓ Generated: nextjs-tester.md

✅ Successfully generated subagents!
```

### Check Generated Files

```bash
# View generated subagents
ls .claude/agents/

# Output:
# nextjs-tester.md  (or other framework-specific agents)
```

---

## Step 3: Use Subagents (1 minute)

### Invoke a Subagent

In Claude Code, you can now use specialized subagents:

> "Use the nextjs-tester agent to write tests for Button.tsx"

**Or manually invoke**:

```
@nextjs-tester Write tests for the Login component
```

### What Makes It Special?

The generated subagent knows:

- ✓ Your framework (Next.js, FastAPI, etc.)
- ✓ Your language (TypeScript, Python, etc.)
- ✓ Your tools (Vitest, pytest, etc.)
- ✓ Best practices for your stack

---

## Step 4: Check Development Phase (1 minute)

### 🌟 Novel Feature: Phase-Aware Review

Ask Claude:

> "What development phase am I in?"

**Example output**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Development Phase: MVP
Confidence: 68%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Indicators:
  • Version 0.5.0 (0.x.x) → MVP
  • 87 commits → MVP stage
  • 12 test files → basic testing
  • README + 2 doc files

Review Standards (Moderate):
  - Type safety: Enabled
  - Test coverage: 50%+ recommended
  - Security: Basic checks
  - Code style: Lenient
```

### How Phase Affects Code Review

**Prototype** (v0.0.x):

- Light review, focus on functionality
- No test requirements
- Encourages rapid iteration

**MVP** (v0.x.x):

- Moderate review
- 50%+ test coverage recommended
- Basic security checks

**Production** (v1.x.x+):

- Strict review
- 80%+ test coverage required
- Comprehensive security audit

---

## Common Tasks

### Generate Subagents for Different Projects

**Next.js project**:

```
→ Generates: nextjs-tester.md
```

**FastAPI project**:

```
→ Generates: api-developer.md, api-tester.md, sqlalchemy-specialist.md
```

**Vanilla PHP project**:

```
→ Generates: php-developer.md, playwright-tester.md, vanilla-js-developer.md, mysql-specialist.md
```

### Override Phase Detection

Create `.claude/phase.yml`:

```yaml
phase: prototype  # or 'mvp', 'production'
reason: "Rapid prototyping for client demo"
expires: 2025-11-01  # Optional: auto-revert
```

### Update to Latest Version

```bash
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/update.sh | bash
```

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/uninstall.sh | bash
```

---

## Supported Frameworks

| Framework | Templates | Status |
|-----------|-----------|--------|
| **Next.js** | tester | ✅ |
| **Vanilla PHP/Web** | php-developer, playwright-tester, vanilla-js-developer, mysql-specialist | ✅ |
| **FastAPI** | api-developer, api-tester, sqlalchemy-specialist | ✅ |
| **Python ML/CV** | python-ml-developer, cv-specialist | ✅ |
| **iOS Swift** | swift-developer | ✅ |
| **React** | Basic detection | 🚧 |
| **Vue** | Basic detection | 🚧 |
| **Django** | Basic detection | 🚧 |
| **Flask** | Basic detection | 🚧 |
| **Flutter** | Basic detection | 🚧 |

**Total**: 10 frameworks detected, 13 specialized templates

---

## Troubleshooting

### "Claude Code skills directory not found"

**Solution**: Set environment variable:

```bash
export CLAUDE_SKILLS_DIR="/path/to/your/claude/skills"
./install.sh
```

### "Could not detect tech stack"

**Solution**: Create `.claude/project.yml`:

```yaml
framework: nextjs  # or fastapi, vanilla-php-web, etc.
version: "14.0.0"
language: typescript
```

### "Python 3.9+ required"

**Solution**: Install Python 3.9 or later from [python.org](https://www.python.org/downloads/)

### "Wrong phase detected"

**Solution**: Override with `.claude/phase.yml` (see above)

---

## Next Steps

### Learn More

- 📖 [Full Documentation](../README.md) - Complete guide
- 🎯 [Examples Gallery](./EXAMPLES.md) - Real-world examples
- 🔧 [Troubleshooting Guide](./TROUBLESHOOTING.md) - Detailed solutions
- 💡 [Contributing Guide](../CONTRIBUTING.md) - Add your own templates

### Get Help

- 🐛 [Report Issues](https://github.com/SawanoLab/adaptive-claude-agents/issues)
- 💬 [Discussions](https://github.com/SawanoLab/adaptive-claude-agents/discussions)
- ⭐ [Star on GitHub](https://github.com/SawanoLab/adaptive-claude-agents)

### Share Your Experience

If you find Adaptive Claude Agents useful:

- ⭐ Star the repo
- 🐦 Tweet about it
- 📝 Write a blog post
- 🤝 Contribute templates

---

## What Makes This Different?

### vs GitHub Copilot

- ✅ Project-specific subagents (not generic)
- ✅ Phase-aware review (adapts to your project maturity)
- ✅ 10 frameworks with specialized templates

### vs Cursor

- ✅ Automatic tech stack detection
- ✅ Development phase detection ⭐ **UNIQUE**
- ✅ Template-based subagent generation

### vs claude-init

- ✅ Continuous (Skills-based) vs one-time setup
- ✅ Phase adaptation ⭐ **UNIQUE**
- ✅ Automatic updates

---

## Summary

In 5 minutes, you:

1. ✅ Installed Adaptive Claude Agents
2. ✅ Analyzed your project
3. ✅ Generated framework-specific subagents
4. ✅ Learned about phase-aware review

**You're ready to code smarter!** 🚀

---

**Happy Coding!**

For more help, see the [Full Documentation](../README.md) or [open an issue](https://github.com/SawanoLab/adaptive-claude-agents/issues).
