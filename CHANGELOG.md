# Changelog

All notable changes to Adaptive Claude Agents will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Phase 4 - Public Beta (In Progress)
- Installation system (install.sh, uninstall.sh, update.sh)
- Comprehensive user documentation (QUICKSTART.md)
- GitHub community infrastructure (issue templates, PR template)

## [0.3.0] - 2025-10-19

### Added - Phase 3: Adaptive Review Rigor 🌟

**Novel Feature**: First AI coding assistant with phase-aware code review!

#### Phase Detection System
- 7-signal detection algorithm with weighted voting
  - User config override (.claude/phase.yml) - 100% weight
  - Version number analysis - 30% weight
  - Git history analysis (commits, tags, activity) - 20% weight
  - Test coverage detection - 15% weight
  - CI/CD configuration check - 15% weight
  - Documentation completeness - 10% weight
  - Code structure analysis - 10% weight
- Confidence scoring and detailed indicators
- `skills/adaptive-review/detect_phase.py` (690 lines)

#### Phase Configurations
- `prototype.yaml` - Review rigor 3/10 (light, focus on speed)
  - Type safety: disabled
  - Testing: optional
  - Security: deferred
- `mvp.yaml` - Review rigor 6/10 (moderate, balanced)
  - Type safety: moderate
  - Testing: 50%+ recommended
  - Security: basic checks (SQL injection, XSS, CSRF)
- `production.yaml` - Review rigor 10/10 (strict, production-ready)
  - Type safety: strict (no `any` types)
  - Testing: 80%+ required
  - Security: comprehensive (OWASP Top 10)
  - Accessibility: WCAG 2.1 AA

#### Documentation
- Comprehensive user guide (`skills/adaptive-review/SKILL.md`)
- Real-world examples (3 scenarios)
- Troubleshooting guide
- Best practices for phase transitions

#### Testing
- Verified on adaptive-claude-agents: Prototype (48% confidence) ✓
- Verified on c-campus: Production (58% confidence) ✓

### Changed
- README.md: Updated status to "Phase 3 Complete! 🎉"
- README.ja.md: Updated status to "Phase 3 完了！🎉"
- TODO.md: Marked Phase 3 as completed

## [0.2.0] - 2025-10-19

### Added - Phase 2: Multi-Framework Support

#### Framework Detection
- **Vanilla PHP/Web**: Custom MVC apps (NOT Laravel/Symfony)
  - Composer.json analysis with negative detection
  - Root PHP files and directory structure detection
  - Testing tools: Playwright, Codeception, PHPUnit
  - Database detection (MySQL, PostgreSQL)
  - 100% confidence on c-campus project ✓

- **FastAPI** (enhanced detection):
  - Version extraction from requirements.txt
  - Tool detection (pytest, SQLAlchemy, pydantic, uvicorn, alembic)
  - Database driver detection (asyncpg, aiomysql, motor)
  - Improved recommended subagents

- **Python ML/CV**:
  - Library categorization (general, deep-learning, cv, nlp)
  - Jupyter notebook detection
  - Project structure analysis (data/, models/, notebooks/)
  - ML type classification (general ML, computer vision, NLP)

- **iOS Swift**:
  - Xcode project files (.xcodeproj, .xcworkspace)
  - SwiftUI vs UIKit determination
  - CocoaPods and Swift Package Manager support

#### Templates (13 total, ~228KB)
- **Vanilla PHP/Web** (4 templates, ~89KB):
  - `php-developer.md`: PHP 8.2+ MVC patterns, security, PSR standards (793 lines)
  - `playwright-tester.md`: E2E testing, Page Object Model (687 lines)
  - `vanilla-js-developer.md`: ES6+ vanilla JavaScript patterns (612 lines)
  - `mysql-specialist.md`: PDO, migrations, query optimization (589 lines)

- **FastAPI** (3 templates, ~73KB):
  - `api-developer.md`: Async FastAPI patterns, security, Pydantic (812 lines)
  - `api-tester.md`: pytest-asyncio, TestClient, mocking (698 lines)
  - `sqlalchemy-specialist.md`: SQLAlchemy 2.0 async, Alembic (745 lines)

- **Python ML** (2 templates, ~56KB):
  - `python-ml-developer.md`: NumPy, pandas, scikit-learn, MLflow (801 lines)
  - `cv-specialist.md`: OpenCV, PyTorch, data augmentation (876 lines)

- **iOS Swift** (1 template, ~10KB):
  - `swift-developer.md`: SwiftUI, async/await, Core Data, XCTest (407 lines)

#### Improvements
- Enhanced `analyze_project.py` template mapping logic
  - Support exact template name matching
  - Add fallback suffix mapping (-developer, -specialist, -tester)
- Updated README.md with frameworks table (10 frameworks, 13 templates)

#### Testing
- Verified vanilla PHP detection on c-campus (100% confidence) ✓
- Successfully generated 4 subagents for c-campus ✓
- Template variable substitution working correctly ✓

### Changed
- README.md: Updated to Phase 2 Complete
- README.ja.md: Updated to Phase 2 完了
- TODO.md: Marked Phase 2 as completed

## [0.1.0] - 2025-10-19

### Added - Phase 1: Core Implementation

#### Project Analyzer Skill
- `skills/project-analyzer/SKILL.md`: Comprehensive skill documentation
  - Usage examples and troubleshooting
  - Progressive Disclosure pattern implementation
- `skills/project-analyzer/detect_stack.py` (551 lines):
  - Tech stack detection for Next.js, React, Vue, FastAPI, Django, Flask, Go, Flutter
  - Confidence scoring algorithm
  - Structured detection results with JSON output
  - Comprehensive tooling detection (testing, styling, state, API clients)
- `skills/project-analyzer/analyze_project.py` (295 lines):
  - Main orchestration script
  - User confirmation workflow (Progressive Disclosure)
  - Template generation from detected stack
  - CLI interface with --auto and --verbose flags

#### Templates
- `templates/nextjs/tester.md` (812 lines):
  - Next.js testing specialist subagent
  - Vitest/Jest + Testing Library patterns
  - Component, Server Component, API Route, Hook testing
  - Best practices and common scenarios
  - Variable substitution ({{FRAMEWORK}}, {{LANGUAGE}}, {{VERSION}})

#### Testing
- Verified detection accuracy: 100% confidence on Next.js project ✓
- Tested full workflow: detection → confirmation → generation ✓
- Template variables correctly substituted ✓

### Changed
- README.md: Updated status to Phase 1 Complete
- README.ja.md: Updated status to Phase 1 完了
- TODO.md: Marked Phase 1 as completed

## [0.0.1] - 2025-10-19

### Added - Initial Release

#### Core Documentation
- README.md (English)
- README.ja.md (Japanese)
- LICENSE (MIT)
- CONTRIBUTING.md with contribution guidelines
- CODE_OF_CONDUCT.md (Contributor Covenant 2.0)
- SECURITY.md with security policy
- .gitignore for Python, Node.js, MCP configs

#### Project-Specific Subagents
Created in `.claude/agents/`:
- `template-generator`: Creates new subagent templates
- `stack-analyzer`: Detects tech stack efficiently
- `skills-developer`: Develops Claude Skills
- `docs-writer`: Writes technical documentation

#### Internal Documentation
Organized in `docs/internal/` (gitignored):
- DISCUSSION.md: Project origin and rationale
- IMPLEMENTATION.md: Technical implementation plan
- GITHUB_PLAN.md: Public release strategy

#### Best Practices Documentation
- `docs/BEST_PRACTICES.md`:
  - Anthropic best practices (Progressive Disclosure, Tool Selection)
  - serena MCP integration guide
  - Template and Skills development guidelines

---

## Version History Summary

| Version | Date | Key Features | Status |
|---------|------|--------------|--------|
| **0.3.0** | 2025-10-19 | 🌟 Phase-aware code review (NOVEL) | Phase 3 Complete |
| **0.2.0** | 2025-10-19 | Multi-framework support (10 frameworks, 13 templates) | Phase 2 Complete |
| **0.1.0** | 2025-10-19 | Project analyzer skill, Next.js template | Phase 1 Complete |
| **0.0.1** | 2025-10-19 | Initial project setup, documentation | Initial Release |

---

## Legend

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

---

**Repository**: https://github.com/SawanoLab/adaptive-claude-agents
