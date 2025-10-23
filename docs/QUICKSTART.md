# Quick Start Guide (5 Minutes)

Get started with Adaptive Claude Agents v1.0.0 in just 5 minutes!

**Perfect for beginners** - Start vibe coding immediately with Quick Start sections in all templates.

---

## What You'll Learn

- ✅ How to install Adaptive Claude Agents (30 seconds)
- ✅ How to analyze your first project (1 minute)
- ✅ How to understand your development phase (automatic)
- ✅ How to use Quick Start sections in templates (5 minutes)

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
  Version: 1.0.0 (Production Ready)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ System check passed
✓ Claude Code skills directory found
✓ Installation complete!
✓ Quick Start sections available in all 15 templates
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

### Navigate to Your Project

```bash
cd /path/to/your/project  # Next.js, FastAPI, PHP, etc.
```

### Run Project Analysis

**Method 1: Via Skills Directory**

```bash
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" .
```

**Method 2: Ask Claude Code** (if project-analyzer skill is configured)

> "Run the project analyzer skill to detect my tech stack and generate subagents"

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

🎯 Detecting development phase...

📊 Development Phase
  Phase:         PROTOTYPE
  Review Rigor:  3/10
  Description:   Prototype phase - Focus on "Does it work?" with light review
  Confidence:    65%

📝 Generating subagents...
  ✓ Generated: nextjs-tester.md (with Quick Start section)

✅ Successfully generated subagents!

📁 Location: .claude/agents/
📖 Usage Guide: .claude/agents/SUBAGENT_GUIDE.md

💡 Next steps:
  1. Open .claude/agents/nextjs-tester.md
  2. Read the Quick Start section (50-100 lines)
  3. Start vibe coding with copy-pasteable examples!
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

| Framework | Detection | Templates Available | Tested |
|-----------|-----------|---------------------|--------|
| **Next.js** | ✅ 100% | tester | ✅ Week 2 |
| **Vanilla PHP/Web** | ✅ 100% | php-developer, playwright-tester, vanilla-js-developer, mysql-specialist | ✅ Week 2 |
| **FastAPI** | ✅ 80% | api-developer, api-tester, sqlalchemy-specialist | ✅ Week 2 |
| **React** | ✅ 80% | (uses Next.js tester for now) | ✅ Week 2 |
| **Vue** | ✅ 90% | (uses Next.js tester for now) | ✅ Week 2 |
| **Django** | ✅ 80% | (uses FastAPI templates for now) | ✅ Week 2 |
| **Flask** | ✅ 70% | (uses FastAPI templates for now) | ✅ Week 2 |
| **Python ML/CV** | ✅ 100% | python-ml-developer, cv-specialist | ✅ Week 2 |
| **iOS Swift** | ✅ 80% | swift-developer | ✅ Week 2 |
| **Go/Flutter** | ⏳ Planned | TBD | Post-beta |

**Total**: 9/10 frameworks tested (90%), 13 specialized templates

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
