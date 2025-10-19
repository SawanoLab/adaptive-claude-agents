# Adaptive Claude Agents

> **Status**: Public Beta 🚀
>
> Auto-generate project-specific Claude Code subagents that adapt to your development phase.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0--beta-blue.svg)](https://github.com/SawanoLab/adaptive-claude-agents/releases)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20WSL-lightgrey.svg)](#installation)
[![Status](https://img.shields.io/badge/status-public%20beta-green.svg)](https://github.com/SawanoLab/adaptive-claude-agents/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

[日本語版 README](./README.ja.md) | [Documentation](./docs/) | [Examples](./docs/EXAMPLES.md) | [Troubleshooting](./docs/TROUBLESHOOTING.md)

---

## What is this?

**Adaptive Claude Agents** automatically generates specialized Claude Code subagents for your project and adjusts code review rigor based on your development phase.

### Two Novel Features

#### 1. 🔍 Auto-Detection & Subagent Generation

Analyzes your project and generates appropriate subagents:

```bash
Detected: Next.js 14 + TypeScript + Vitest
→ Generated: nextjs-tester

Detected: FastAPI + SQLAlchemy + pytest
→ Generated: api-developer, api-tester, sqlalchemy-specialist
```

**Supported Frameworks** (10): Next.js, React, Vue, FastAPI, Django, Flask, Vanilla PHP/Web, Python ML/CV, iOS Swift, Go, Flutter

#### 2. 📊 Phase-Adaptive Review ⭐ **Industry First**

Automatically adjusts review standards based on development phase:

| Phase | Review Rigor | Focus |
|-------|--------------|-------|
| **Prototype** | Light (3/10) | "Does it work?" |
| **MVP** | Moderate (6/10) | "Is it secure?" |
| **Production** | Strict (10/10) | "Is it perfect?" |

No other AI coding tool (GitHub Copilot, Cursor, etc.) has this.

---

## 🚀 Quick Start

### Installation

```bash
# One-command install
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
```

Or manual install:

```bash
git clone https://github.com/SawanoLab/adaptive-claude-agents.git
cd adaptive-claude-agents
./install.sh
```

### Usage

In Claude Code, simply ask:

```text
> "Analyze my project and generate appropriate subagents"
```

Or use directly:

```bash
# macOS
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" .

# Linux/WSL
python3 ~/.config/claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py .
```

**Full guide**: [Quick Start](./docs/QUICKSTART.md) (5 minutes)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Quick Start](./docs/QUICKSTART.md) | 5-minute getting started guide |
| [Examples](./docs/EXAMPLES.md) | 5 real-world examples with full output |
| [Troubleshooting](./docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [Contributing](./CONTRIBUTING.md) | How to contribute templates |
| [Changelog](./CHANGELOG.md) | Version history |

---

## 🎯 How It Works

### 1. Project Analysis

```bash
$ python3 skills/project-analyzer/detect_stack.py .

Detected: Next.js 14 + TypeScript
Confidence: 98%
Tools: Vitest, Testing Library, Tailwind CSS
```

### 2. Phase Detection

```bash
$ python3 skills/adaptive-review/detect_phase.py .

Phase: MVP
Confidence: 72%

Indicators:
  • Version 0.5.0 → MVP
  • 127 commits → MVP stage
  • 45 test files → basic testing (56%)
  • CI/CD: GitHub Actions ✓
```

### 3. Subagent Generation

```bash
Generated subagents:
  ✓ .claude/agents/nextjs-tester.md

Variables substituted:
  {{FRAMEWORK}} → Next.js
  {{LANGUAGE}} → TypeScript
  {{VERSION}} → 14.2.0
```

### 4. Adaptive Review

Review standards automatically adjust:

- **Prototype**: Encourages rapid iteration, defers quality checks
- **MVP**: Balances functionality and quality
- **Production**: Enforces strict standards (80%+ test coverage, security audit, etc.)

---

## 🌟 What Makes It Unique

### Compared to Other Tools

| Feature | Adaptive Claude Agents | GitHub Copilot | Cursor |
|---------|------------------------|----------------|--------|
| Auto-detect tech stack | ✅ 10 frameworks | ❌ | ❌ |
| Generate specialized agents | ✅ 13 templates | ❌ | ❌ |
| **Phase-adaptive review** | ✅ **Industry first** | ❌ | ❌ |
| Works across all projects | ✅ Global Skills | ❌ | ❌ |
| Open source | ✅ MIT | ❌ | ❌ |

---

## 📦 Supported Frameworks

| Framework | Detection Confidence | Templates | Tested |
|-----------|---------------------|-----------|--------|
| **Next.js** | 100% | nextjs-tester | ✅ |
| **Vanilla PHP/Web** | 100% | php-developer, playwright-tester, vanilla-js-developer, mysql-specialist | ✅ |
| **Python ML/CV** | 100% | python-ml-developer, cv-specialist | ✅ |
| **Vue** | 90% | (Next.js templates) | ✅ |
| **FastAPI** | 80% | api-developer, api-tester, sqlalchemy-specialist | ✅ |
| **React** | 80% | (Next.js templates) | ✅ |
| **Django** | 80% | (FastAPI templates) | ✅ |
| **iOS Swift** | 80% | swift-developer | ✅ |
| **Flask** | 70% | (FastAPI templates) | ✅ |
| **Go/Flutter** | Planned | TBD | Post-beta |

**Total**: 9/10 frameworks tested (90%), 13 specialized templates (~228KB)

**Legend**: ✅ = Validated in Week 2 testing

Want to add your framework? See [Template Request](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=template_request.md)

---

## 🛠️ Development

### Project Structure

```text
adaptive-claude-agents/
├── skills/
│   ├── project-analyzer/     # Tech stack detection
│   └── adaptive-review/      # Phase detection
├── templates/                 # Subagent templates (13)
│   ├── nextjs/
│   ├── fastapi/
│   ├── vanilla-php-web/
│   ├── python-ml/
│   └── ios-swift/
├── docs/                      # User documentation
└── install.sh                 # Installation script
```

### Tech Stack

- **Language**: Python 3.9+
- **Detection**: File-based + content analysis
- **Templates**: Markdown with variable substitution
- **Integration**: Claude Code Skills

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for:

- Adding new framework templates
- Improving detection accuracy
- Enhancing documentation
- Reporting bugs

**Quick Links**:

- [Bug Report](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=bug_report.md)
- [Feature Request](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=feature_request.md)
- [Template Request](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=template_request.md)

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.

**Attribution**: If you use this project, a link back to this repository is appreciated.

---

## 🙏 Acknowledgments

Developed at **SawanoLab**, Aichi Institute of Technology.

**Inspired by**:

- [Anthropic's Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Progressive Disclosure Pattern](https://www.nngroup.com/articles/progressive-disclosure/)

**Special Thanks**:

- Anthropic for Claude Code and the Skills framework
- Alpha testers from SawanoLab
- All contributors to this project

---

## 📬 Contact

- **Issues**: [GitHub Issues](https://github.com/SawanoLab/adaptive-claude-agents/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SawanoLab/adaptive-claude-agents/discussions)
- **Security**: <security@sawanolab.org>

---

### Made with ❤️ by SawanoLab

⭐ Star us on GitHub if you find this useful!
