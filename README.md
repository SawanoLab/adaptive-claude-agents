# Adaptive Claude Agents

> **🚧 Status**: Phase 2 Complete!
> Core detection + 10 frameworks supported. Phase 3 (Adaptive Review) coming soon!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Development Status](https://img.shields.io/badge/status-pre--alpha-red)](https://github.com/SawanoLab/adaptive-claude-agents)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

[日本語版 README](./README.ja.md)

Automatically generates **project-specific Claude Code subagents** and adjusts their behavior based on your **development phase**.

---

## 🎯 What is this?

### The Problem

Setting up Claude Code for a new project is tedious:

- Manually creating subagents for each tech stack
- Same strict code review for quick prototypes and production code
- Reconfiguring agents as project matures

### The Solution

**Adaptive Claude Agents** solves this with two innovative features:

#### 1. 🔍 Auto-Detection & Generation

Analyzes your project structure and automatically generates appropriate subagents:

```bash
# Detects: Next.js + TypeScript + Tailwind CSS
→ Generates: nextjs-tester, component-reviewer, type-checker

# Detects: FastAPI + PostgreSQL + pytest
→ Generates: fastapi-tester, api-reviewer, db-schema-checker
```

Integrated as **global Claude Skills** - works across all your projects!

#### 2. 📊 Phase-Adaptive Review Rigor ⭐ **Novel Approach**

**First tool to bring traditional QA principles to AI agents:**

| Phase | Review Focus | What It Checks | Example |
|-------|-------------|----------------|---------|
| **Prototype** | "Does it work?" | Basic functionality only | Skip performance, style |
| **MVP** | "Is it secure?" | Common vulnerabilities | Basic security audit |
| **Production** | "Is it perfect?" | Everything | Full audit + optimization |

Automatically adjusts based on development phase markers in your codebase.

---

## ✨ Key Features

- ✅ **Zero Configuration**: Works out of the box
- ✅ **Tech Stack Agnostic**: Supports 10 frameworks (Next.js, FastAPI, vanilla PHP, Python ML, iOS Swift, and more)
- ✅ **Phase-Aware**: Adapts review rigor automatically
- ✅ **Global Skills**: One setup, works everywhere
- ✅ **Community Templates**: Easy to add new tech stacks
- ✅ **Progressive Disclosure**: Follows Anthropic's best practices

---

## 🚀 Quick Start

> **Note**: Coming soon in Phase 1 release

### Installation (Planned)

```bash
# Install as global Claude Skill
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
```

### Usage (Planned)

1. Open any project in Claude Code
2. Skill auto-detects your tech stack
3. Confirms before generating subagents
4. Ready to code with optimized agents!

```
Detected: Next.js + TypeScript + Tailwind CSS
Generate these subagents?
  - nextjs-tester (Vitest + Testing Library)
  - component-reviewer (React best practices)
  - type-checker (TypeScript strict mode)
[Y/n]
```

---

## 📁 Project Structure

```
adaptive-claude-agents/
├── skills/                 # Claude Skills implementation
│   ├── project-analyzer/   # Auto-detection logic
│   └── adaptive-review/    # Phase-aware review
├── templates/              # Subagent templates
│   ├── nextjs/
│   ├── fastapi/
│   ├── react-native/
│   └── go/
├── examples/               # Usage examples
└── docs/                   # Documentation
```

---

## 🛣️ Roadmap

- [x] Project conception & planning
- [x] **Phase 1**: Basic project analyzer ✅
  - [x] Tech stack detection
  - [x] Next.js template
  - [x] Basic subagent generation
- [x] **Phase 2**: Multiple tech stacks (2 weeks) ✅
  - [x] FastAPI, vanilla PHP, Python ML, iOS Swift templates
  - [x] Improved detection accuracy
  - [x] 10 frameworks, 13 templates implemented
- [ ] **Phase 3**: Adaptive review rigor (3 weeks)
  - [ ] Phase detection logic
  - [ ] Phase-specific subagents
- [ ] **Phase 4**: Public beta release

See our [internal project board](https://github.com/SawanoLab/adaptive-claude-agents/projects) for detailed progress.

---

## 📦 Supported Frameworks (Phase 2)

| Framework | Templates | Status |
|-----------|-----------|--------|
| **Next.js** | tester | ✅ Phase 1 |
| **Vanilla PHP/Web** | php-developer, playwright-tester, vanilla-js-developer, mysql-specialist | ✅ Phase 2 |
| **FastAPI** | api-developer, api-tester, sqlalchemy-specialist | ✅ Phase 2 |
| **Python ML/CV** | python-ml-developer, cv-specialist | ✅ Phase 2 |
| **iOS Swift** | swift-developer | ✅ Phase 2 |
| **React** | Basic detection | 🚧 Phase 1 |
| **Vue** | Basic detection | 🚧 Phase 1 |
| **Django** | Basic detection | 🚧 Phase 1 |
| **Flask** | Basic detection | 🚧 Phase 1 |
| **Flutter** | Basic detection | 🚧 Phase 1 |

**Total**: 10 frameworks detected, 13 specialized templates

---

## 🆚 How is this different?

| Feature | [claude-init](https://github.com/dimitritholen/claude-init) | **Adaptive Claude Agents** |
|---------|-------------|---------------------------|
| **Timing** | One-time setup | Continuous (Skills-based) |
| **Phase Adaptation** | ❌ No | ✅ **Unique feature** |
| **Updates** | Project start only | Ongoing |
| **Integration** | CLI tool | Claude Skills |
| **Tech Stack Detection** | Manual | Automatic |

**Complementary Tools**: We recommend using `claude-init` for initial setup, then Adaptive Claude Agents for ongoing development!

---

## 🤝 Contributing

We welcome contributions! This project is in early development - a great time to get involved.

### Ways to Contribute

- 💡 **Ideas & Feedback**: Open a [GitHub Issue](https://github.com/SawanoLab/adaptive-claude-agents/issues)
- 🐛 **Bug Reports**: Report issues (when we have code!)
- 📝 **Templates**: Add support for new tech stacks
- 📖 **Documentation**: Improve guides and examples
- 🌍 **Translations**: Help translate documentation

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

### Priority Contributions Needed

- **Templates**: Django, Flask, Vue, Angular, Flutter
- **Detection Logic**: Improve accuracy
- **Documentation**: Tutorials, videos
- **Testing**: Unit & integration tests

---

## 📚 Documentation

- [Contributing Guide](./CONTRIBUTING.md) - How to contribute
- [License](./LICENSE) - MIT License

**Internal Development Docs** (not in public repo):

- Design discussions
- Implementation details
- Release strategy

---

## 🌟 Inspiration & Credits

This project is inspired by:

- [claude-init](https://github.com/dimitritholen/claude-init) by @dimitritholen
- [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) by @VoltAgent
- Traditional software QA best practices

Special thanks to the Claude Code community for feedback and ideas!

---

## 📄 License

[MIT License](./LICENSE) - Copyright (c) 2025 Sawano Hiroaki

---

## 🙋 Author

Sawano Hiroaki

- GitHub: [@SawanoLab](https://github.com/SawanoLab)
- Organization: Aichi Institute of Technology

---

## ⭐ Star History

If you find this project interesting, please consider starring it to follow development!

[![Star History Chart](https://api.star-history.com/svg?repos=SawanoLab/adaptive-claude-agents&type=Date)](https://star-history.com/#SawanoLab/adaptive-claude-agents&Date)

---

**Status**: Pre-alpha | **Next Milestone**: Phase 1 completion (ETA: 2 weeks)

Made with ❤️ for the Claude Code community
