# Subagent Usage Guide - Adaptive Claude Agents

**Project Type**: Python Tool Development (Claude Code Skills)
**Last Updated**: 2025-10-28

---

## 🎯 Available Subagents

This project has 4 specialized subagents for tool development:

### 1. skills-developer
**Purpose**: Develops and tests Claude Skills implementations
**When to use**:
- Creating new Skills
- Modifying detection logic
- Implementing phase detection
- Testing Skills behavior

**Tools**: Read, Write, Edit, Bash, MCP (serena)

**Trigger keywords**:
- "Skillを開発"
- "検出ロジックを修正"
- "新しいSkillを作成"
- "develop a new skill"

---

### 2. template-generator
**Purpose**: Creates new subagent templates following project conventions
**When to use**:
- Adding support for new frameworks
- Creating specialized subagent templates
- Updating template structure

**Tools**: Read, Write, Edit, MCP (serena)

**Trigger keywords**:
- "テンプレートを作成"
- "新しいフレームワークを追加"
- "create a new template"
- "add framework support"

---

### 3. docs-writer
**Purpose**: Writes and maintains documentation
**When to use**:
- Creating user documentation
- Updating README files
- Writing guides and best practices
- Maintaining changelog

**Tools**: Read, Write, Edit

**Trigger keywords**:
- "ドキュメントを作成"
- "READMEを更新"
- "write documentation"
- "update docs"

---

### 4. stack-analyzer
**Purpose**: Analyzes project structure to detect tech stack
**When to use**:
- Improving framework detection accuracy
- Adding new framework detection
- Testing detection logic

**Tools**: Read, Glob, Grep, Bash, MCP (serena)

**Trigger keywords**:
- "スタック検出を改善"
- "フレームワーク検出"
- "improve detection"
- "analyze tech stack"

---

## 🚀 AGGRESSIVE Mode Workflows

### Mandatory Subagent Usage (自動委譲)

#### 1. Multi-Template Updates (3+ templates)
```
User: "Next.js, FastAPI, Go のテンプレートにQuick Startセクションを追加"

主エージェント（自動）:
  → Detects: 3 templates
  → Delegates to: template-generator
  → Time saved: 45-60 minutes
```

#### 2. Codebase-wide Detection Logic Search
```
User: "version_number はどこで使われているか"

主エージェント（自動）:
  → Detects: Codebase search
  → Delegates to: Explore (thoroughness: "very thorough")
  → Time saved: 60-90 minutes
```

#### 3. Documentation Updates (Multiple files)
```
User: "README.md, README.ja.md, QUICKSTART.md を更新"

主エージェント（自動）:
  → Detects: 3 docs files
  → Delegates to: docs-writer
  → Time saved: 30-45 minutes
```

#### 4. E2E Testing Workflow
```
User: "11フレームワークの検出をテスト"

主エージェント（自動）:
  → Detects: E2E testing
  → Delegates to: skills-developer
  → Runs: pytest with coverage
  → Time saved: 60+ minutes
```

---

## 💰 Model Selection (Haiku 4.5 vs Sonnet 4.5)

### Haiku 4.5を使用（60-80%コスト削減）

| タスク | モデル | 理由 |
|-------|--------|------|
| バージョン番号更新 | Haiku 4.5 | 機械的置換 |
| Typo修正(1-2ファイル) | Haiku 4.5 | 単純修正 |
| テスト実行・レポート | Haiku 4.5 | 定型作業 |
| 表記統一（ユーザー→ユーザ） | Haiku 4.5 | パターン置換 |

### Sonnet 4.5を使用（高精度）

| タスク | モデル | 理由 |
|-------|--------|------|
| 新フレームワーク検出ロジック | Sonnet 4.5 | 複雑な推論 |
| テンプレート設計 | Sonnet 4.5 | アーキテクチャ判断 |
| コードレビュー | Sonnet 4.5 | 品質評価 |
| 複雑なリファクタリング | Sonnet 4.5 | 依存関係理解 |

**詳細**: `docs/2025_BEST_PRACTICES.md` の「Model Selection」セクション

---

## 📊 Success Metrics

### Target KPIs
- **Subagent usage rate**: 20-30% of complex tasks
- **Time saved per week**: 2-4 hours
- **Token efficiency**: 20k overhead acceptable for 30+ min savings

### Common Workflows

#### Workflow 1: New Framework Support
```
1. User: "Railsサポートを追加して"
2. Delegates to: template-generator (creates Rails template)
3. Delegates to: skills-developer (adds detection logic)
4. Delegates to: docs-writer (updates README)
5. Result: Complete framework support in 60-90 minutes
```

#### Workflow 2: Version Release
```
1. User: "v1.2.0としてリリース準備"
2. Haiku 4.5: Update version numbers (install.sh, VERSION, SKILL.md)
3. Sonnet 4.5: Generate CHANGELOG entry
4. Haiku 4.5: Execute git tag and push
5. Result: Release ready in 15 minutes
```

#### Workflow 3: Documentation Overhaul
```
1. User: "READMEをビギナーフレンドリーに更新"
2. Delegates to: docs-writer
3. Sonnet 4.5: Analyzes existing docs, proposes structure
4. Haiku 4.5: Applies formatting and typo fixes
5. Result: Improved docs in 30-45 minutes
```

---

## 🎯 Best Practices

### When NOT to Use Subagents
- ❌ Single file simple edits (use Haiku 4.5 directly)
- ❌ Quick questions about code (use Sonnet 4.5 directly)
- ❌ Exploratory discussions (main agent is better)

### When to ALWAYS Use Subagents
- ✅ 3+ files with similar modifications
- ✅ Codebase-wide searches
- ✅ E2E testing workflows
- ✅ Parallel independent tasks

### Delegation Efficiency
```
Direct execution: 5-10 minutes per task
Subagent delegation: 2-3 minutes per task (with 20k token overhead)

ROI Calculation:
  If task saves 30+ minutes → 20k overhead justified
  If task saves <10 minutes → Direct execution preferred
```

---

## 🔗 Related Resources

- **Project Structure**: `README.md` - Overview of directories and components
- **Development Context**: `CLAUDE.md` - Coding standards and design principles
- **Best Practices**: `docs/BEST_PRACTICES.md` - Anthropic recommendations
- **2025 Updates**: `docs/2025_BEST_PRACTICES.md` - Latest framework patterns
- **Examples**: `docs/EXAMPLES.md` - Real-world usage examples

---

## 🤖 Meta Note

This guide was generated manually for the Adaptive Claude Agents project itself.

**Why manual?**: This is a tool development project without a detectable runtime framework (Next.js, FastAPI, etc.). The `analyze_project.py` script is designed for application projects, not meta-projects like this one.

**Update frequency**: Update this guide when:
- New subagents are added
- AGGRESSIVE mode workflows change
- Model selection guidance evolves
- Success metrics are updated

---

**Last reviewed**: 2025-10-28 by Claude (Sonnet 4.5)
