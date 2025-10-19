# Contributing to Adaptive Claude Agents

First off, thank you for considering contributing to Adaptive Claude Agents! 🎉

This project aims to make Claude Code more powerful through automatic subagent generation and phase-adaptive review. Your contributions help make AI-assisted development better for everyone.

## 🚧 Project Status

**Current Phase**: Phase 1 - Core Implementation

We're building the foundation. This is a great time to get involved!

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- **Clear title**: Describe the bug in one sentence
- **Steps to reproduce**: How can we see the bug?
- **Expected behavior**: What should happen?
- **Actual behavior**: What actually happens?
- **Environment**: OS, Claude Code version, Python version

### Suggesting Features

We love new ideas! Please create an issue with:

- **Problem statement**: What problem does this solve?
- **Proposed solution**: How would it work?
- **Alternatives considered**: What other approaches did you think about?

### Contributing Code

#### For First-Time Contributors

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/adaptive-claude-agents.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Make your changes**
5. **Test** your changes
6. **Commit**: `git commit -m "feat: add feature description"`
7. **Push**: `git push origin feature/your-feature-name`
8. **Open a Pull Request**

#### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add Next.js template
fix: correct Python detection logic
docs: update installation guide
refactor: simplify stack detection
test: add tests for FastAPI template
```

### Contributing Templates

Templates are the heart of this project! To add a new tech stack template:

1. **Check existing templates** in `templates/` directory
2. **Create a new directory**: `templates/your-stack/`
3. **Add template files**:
   - `tester.md` - Testing subagent
   - `reviewer.md` - Code review subagent (if applicable)
   - `README.md` - Template documentation
4. **Update detection logic** in `skills/project-analyzer/detect_stack.py`
5. **Add examples** in `examples/your-stack/`
6. **Test thoroughly**

#### Template Requirements

- Must include clear description and purpose
- Must specify required tools
- Must include usage examples
- Must follow existing template format
- Must be tested with a real project

By submitting a template, you agree to:
- License it under MIT
- Allow modifications
- Receive credit in the template file header

## 📋 Development Setup

### Prerequisites

- Python 3.9+
- Claude Code
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/adaptive-claude-agents.git
cd adaptive-claude-agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (when available)
pip install -r requirements.txt

# Run tests (when available)
pytest
```

### Testing

Before submitting a PR:

1. Test your changes manually
2. Ensure code follows PEP 8 (for Python)
3. Update documentation if needed
4. Add tests if applicable

## 🎯 Priority Areas

We especially welcome contributions in:

1. **New Tech Stack Templates**
   - Python: Django, Flask
   - JavaScript/TypeScript: Vue, Angular, Svelte
   - Mobile: Flutter, Swift, Kotlin
   - Backend: Spring Boot, Laravel, Ruby on Rails

2. **Phase Detection Logic**
   - Improving accuracy
   - Supporting more project structures

3. **Documentation**
   - Tutorials and guides
   - Translation to other languages
   - Video demonstrations

4. **Testing**
   - Unit tests
   - Integration tests
   - End-to-end tests

## 📝 Code Style

### Python

- Follow PEP 8
- Use type hints (Python 3.9+)
- Write Google-style docstrings
- Maximum line length: 88 characters (Black formatter)

### Markdown

- Use relative paths for links
- Specify language for code blocks
- Use headers hierarchically (no skipping levels)

## 🔍 Review Process

1. **Automated checks**: CI/CD runs automatically
2. **Maintainer review**: We'll review your PR within 1 week
3. **Feedback**: We may request changes
4. **Merge**: Once approved, we'll merge your contribution

## ❓ Questions?

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Create an issue
- **Security issues**: Email directly (see SECURITY.md)

## 🌟 Recognition

Contributors will be:
- Listed in README.md
- Credited in template files (for template contributions)
- Thanked in release notes

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making Adaptive Claude Agents better!** 🚀

Every contribution, big or small, makes a difference.
