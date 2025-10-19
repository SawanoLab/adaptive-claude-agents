# Adaptive Claude Agents

> **ステータス**: Week 3 - アルファテスト中 🧪 | パブリックベータ: 10月27-28日 🚀
>
> プロジェクト固有のClaude Codeサブエージェントを自動生成し、開発フェーズに応じて動作を適応させます。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

[English README](./README.md) | [ドキュメント](./docs/) | [使用例](./docs/EXAMPLES.md) | [トラブルシューティング](./docs/TROUBLESHOOTING.md)

---

## これは何？

**Adaptive Claude Agents** は、プロジェクトに最適化されたClaude Codeサブエージェントを自動生成し、開発フェーズに応じてコードレビューの厳格度を調整するツールです。

### 2つの革新的機能

#### 1. 🔍 自動検出＆サブエージェント生成

プロジェクトを分析して適切なサブエージェントを生成：

```bash
検出: Next.js 14 + TypeScript + Vitest
→ 生成: nextjs-tester

検出: FastAPI + SQLAlchemy + pytest
→ 生成: api-developer, api-tester, sqlalchemy-specialist
```

**対応フレームワーク** (10種類): Next.js, React, Vue, FastAPI, Django, Flask, バニラPHP/Web, Python ML/CV, iOS Swift, Go, Flutter

#### 2. 📊 フェーズ適応レビュー ⭐ **業界初**

開発フェーズに応じてレビュー基準を自動調整：

| フェーズ | レビュー厳格度 | 重点 |
|---------|--------------|------|
| **プロトタイプ** | 軽い (3/10) | 「動くか？」 |
| **MVP** | 中程度 (6/10) | 「安全か？」 |
| **本番** | 厳格 (10/10) | 「完璧か？」 |

GitHub Copilot、Cursor等の他のAIコーディングツールにはない機能です。

---

## 🚀 クイックスタート

### インストール

```bash
# ワンコマンドインストール
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
```

または手動インストール：

```bash
git clone https://github.com/SawanoLab/adaptive-claude-agents.git
cd adaptive-claude-agents
./install.sh
```

### 使い方

Claude Codeで以下のように尋ねるだけ：

```text
> "このプロジェクトを分析して適切なサブエージェントを生成して"
```

または直接実行：

```bash
python3 ~/.config/claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py .
```

**詳細ガイド**: [クイックスタート](./docs/QUICKSTART.md) (5分)

---

## 📚 ドキュメント

| ドキュメント | 説明 |
|----------|------|
| [クイックスタート](./docs/QUICKSTART.md) | 5分で始めるガイド |
| [使用例](./docs/EXAMPLES.md) | 5つの実例と完全な出力 |
| [トラブルシューティング](./docs/TROUBLESHOOTING.md) | よくある問題と解決策 |
| [コントリビューション](./CONTRIBUTING.md) | テンプレートの追加方法 |
| [変更履歴](./CHANGELOG.md) | バージョン履歴 |

---

## 🎯 動作の仕組み

### 1. プロジェクト分析

```bash
$ python3 skills/project-analyzer/detect_stack.py .

検出: Next.js 14 + TypeScript
信頼度: 98%
ツール: Vitest, Testing Library, Tailwind CSS
```

### 2. フェーズ検出

```bash
$ python3 skills/adaptive-review/detect_phase.py .

フェーズ: MVP
信頼度: 72%

指標:
  • バージョン 0.5.0 → MVP
  • 127コミット → MVPステージ
  • 45テストファイル → 基本的なテスト (56%)
  • CI/CD: GitHub Actions ✓
```

### 3. サブエージェント生成

```bash
生成されたサブエージェント:
  ✓ .claude/agents/nextjs-tester.md

変数置換:
  {{FRAMEWORK}} → Next.js
  {{LANGUAGE}} → TypeScript
  {{VERSION}} → 14.2.0
```

### 4. 適応的レビュー

レビュー基準が自動的に調整されます：

- **プロトタイプ**: 高速な反復を促進、品質チェックは保留
- **MVP**: 機能と品質のバランス
- **本番**: 厳格な基準を適用（テストカバレッジ80%+、セキュリティ監査等）

---

## 🌟 独自性

### 他ツールとの比較

| 機能 | Adaptive Claude Agents | GitHub Copilot | Cursor |
|------|------------------------|----------------|--------|
| 技術スタック自動検出 | ✅ 10フレームワーク | ❌ | ❌ |
| 専門エージェント生成 | ✅ 13テンプレート | ❌ | ❌ |
| **フェーズ適応レビュー** | ✅ **業界初** | ❌ | ❌ |
| 全プロジェクトで動作 | ✅ グローバルSkills | ❌ | ❌ |
| オープンソース | ✅ MIT | ❌ | ❌ |

---

## 📦 対応フレームワーク

| カテゴリー | フレームワーク | テンプレート数 |
|-----------|--------------|--------------|
| **フロントエンド** | Next.js, React, Vue | 1テンプレート |
| **バックエンド** | FastAPI, Django, Flask | 3テンプレート (FastAPI) |
| **Web** | バニラPHP/JavaScript | 4テンプレート |
| **ML/CV** | Python ML, Computer Vision | 2テンプレート |
| **モバイル** | iOS Swift, Flutter | 1テンプレート (Swift) |
| **その他** | Go | 1テンプレート |

**合計**: 10フレームワーク、13専門テンプレート (~228KB)

新しいフレームワークを追加したい場合: [テンプレートリクエスト](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=template_request.md)

---

## 🛠️ 開発

### プロジェクト構造

```text
adaptive-claude-agents/
├── skills/
│   ├── project-analyzer/     # 技術スタック検出
│   └── adaptive-review/      # フェーズ検出
├── templates/                 # サブエージェントテンプレート (13)
│   ├── nextjs/
│   ├── fastapi/
│   ├── vanilla-php-web/
│   ├── python-ml/
│   └── ios-swift/
├── docs/                      # ユーザードキュメント
└── install.sh                 # インストールスクリプト
```

### 技術スタック

- **言語**: Python 3.9+
- **検出**: ファイルベース + コンテンツ分析
- **テンプレート**: 変数置換付きMarkdown
- **統合**: Claude Code Skills

---

## 🤝 コントリビューション

コントリビューションを歓迎します！詳細は [CONTRIBUTING.md](./CONTRIBUTING.md) を参照：

- 新しいフレームワークテンプレートの追加
- 検出精度の改善
- ドキュメントの拡充
- バグ報告

**クイックリンク**:

- [バグ報告](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=bug_report.md)
- [機能リクエスト](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=feature_request.md)
- [テンプレートリクエスト](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=template_request.md)

---

## 📄 ライセンス

MIT License - 詳細は [LICENSE](./LICENSE) を参照してください。

**帰属表示**: このプロジェクトを使用する場合、このリポジトリへのリンクをいただけると嬉しいです。

---

## 🙏 謝辞

**澤野研究室**（愛知工業大学）で開発されました。

**インスピレーション元**:

- [Anthropic's Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Progressive Disclosure Pattern](https://www.nngroup.com/articles/progressive-disclosure/)

**Special Thanks**:

- AnthropicのClaude CodeとSkillsフレームワーク
- 澤野研究室のアルファテスター
- すべてのコントリビューター

---

## 📬 お問い合わせ

- **Issues**: [GitHub Issues](https://github.com/SawanoLab/adaptive-claude-agents/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SawanoLab/adaptive-claude-agents/discussions)
- **セキュリティ**: <security@sawanolab.org>

---

### 澤野研究室より ❤️

⭐ 役に立った場合はGitHubでスターをお願いします！
