# Adaptive Claude Agents

> **ステータス**: パブリックベータ 🚀
>
> プロジェクト固有のClaude Codeサブエージェントを自動生成し、開発フェーズに応じて動作を適応させます。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.2-beta-blue.svg)](https://github.com/SawanoLab/adaptive-claude-agents/releases)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20WSL-lightgrey.svg)](#インストール)
[![Status](https://img.shields.io/badge/status-public%20beta-green.svg)](https://github.com/SawanoLab/adaptive-claude-agents/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

[English README](./README.md) | [ドキュメント](./docs/) | [使用例](./docs/EXAMPLES.ja.md) | [トラブルシューティング](./docs/TROUBLESHOOTING.ja.md)

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

**対応フレームワーク** (11種類): Next.js, React, Vue, FastAPI, Django, Flask, バニラPHP/Web, Python ML/CV, iOS Swift, Go, Flutter

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

### アップデート

すでにインストール済みの場合、以下の2ステップで最新のAGGRESSIVEモード機能を取得：

#### ステップ1: グローバルツールの更新

```bash
# macOS
cd "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents"
./update.sh

# Linux/WSL
cd ~/.config/claude/skills/adaptive-claude-agents
./update.sh
```

**更新内容**:

- 最新の検出ロジックとテンプレート
- 強化された AGGRESSIVE ポリシー設定
- バグ修正と改善

#### ステップ2: 各プロジェクトの更新（重要！）

**以前に `analyze_project.py` を実行したすべてのプロジェクト**で、再実行して新機能を取得：

```bash
# プロジェクトディレクトリに移動
cd /path/to/your/project

# macOS
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --auto

# Linux/WSL
python3 ~/.config/claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py . --auto
```

**これにより**:

1. ✅ 最新のフレームワーク別ワークフローで `.claude/agents/SUBAGENT_GUIDE.md` を再生成
2. ✅ プロジェクトの `CLAUDE.md` に AGGRESSIVE ポリシーを追加（未設定の場合）
3. ✅ すべてのサブエージェントテンプレートを最新のベストプラクティスで更新

**すべてのアクティブなプロジェクトでステップ2を繰り返して**、どこでもプロアクティブなサブエージェント活用を有効化！

### 使い方

Claude Codeで以下のように尋ねるだけ：

```text
> "このプロジェクトを分析して適切なサブエージェントを生成して"
```

または直接実行：

```bash
# macOS
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" .

# Linux/WSL
python3 ~/.config/claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py .
```

**詳細ガイド**: [クイックスタート](./docs/QUICKSTART.ja.md) (5分)

---

## 🎯 サブエージェントの使い分け（効率化ガイド）

**基本方針**: このツールをインストールした = サブエージェントを積極的に使いたい。自動化を信頼しましょう！

### ✅ サブエージェントを必ず使う

| シナリオ | 例 | サブエージェント | 節約時間 |
|---------|---|----------------|---------|
| **3+ファイルの類似パターン** | "assessment.js, soap.js, nursing_plan.js にblur修正を適用" | `general-purpose` | 30-60分 |
| **コードベース全体の検索** | "version_number の使用箇所をすべて検索" | `Explore` ("very thorough") | 60-90分 |
| **E2Eテストワークフロー** | "ログイン → API呼び出し → DB検証をテスト" | `general-purpose` + フレームワークtester | 45分以上 |
| **並行可能な独立タスク** | ".gitignore更新 + UIコンポーネントのリファクタリング" | 複数の `general-purpose` | 30分以上 |

### ❌ サブエージェントをスキップ

- 単一ファイルの小規模編集（10行未満）
- 場所が既知の1-2ファイルのシンプルな検索
- トークン制約環境（稀）

### 💡 プロのコツ

1. **3+ファイルでは標準でサブエージェント** - 20kトークンのオーバーヘッドは価値がある
2. **Exploreエージェントを積極活用** - 手動grep/globより優秀
3. **独立タスクは並列化** - 単一メッセージで複数のTaskツール呼び出し
4. **自動トリガーを信頼** - "テスト", "test", "review"などのキーワードで自動起動

### 📊 コスト対効果分析

| タスクタイプ | 直接実行コスト | サブエージェントコスト | 節約時間 | **推奨** |
|------------|--------------|---------------------|---------|---------|
| 1ファイル編集 | 5kトークン | 25kトークン | 0分 | ❌ 直接 |
| 3-4ファイル | 15kトークン | 35kトークン | 30分 | ✅ サブエージェント |
| 5+ファイル | 30kトークン | 50kトークン | 60分 | ✅✅ サブエージェント |
| コードベース検索 | 40kトークン | 60kトークン | 90分 | ✅✅✅ Explore |

**目標**: 複雑なマルチファイルプロジェクトでは20-30%のサブエージェント使用率を目指す。

詳細は[使用例](./docs/EXAMPLES.ja.md#subagent-workflows)を参照してください。

---

## 📚 ドキュメント

| ドキュメント | 説明 |
|----------|------|
| [クイックスタート](./docs/QUICKSTART.ja.md) | 5分で始めるガイド |
| [使用例](./docs/EXAMPLES.ja.md) | 5つの実例と完全な出力 |
| [トラブルシューティング](./docs/TROUBLESHOOTING.ja.md) | よくある問題と解決策 |
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
| 技術スタック自動検出 | ✅ 11フレームワーク | ❌ | ❌ |
| 専門エージェント生成 | ✅ 15テンプレート | ❌ | ❌ |
| **フェーズ適応レビュー** | ✅ **業界初** | ❌ | ❌ |
| 全プロジェクトで動作 | ✅ グローバルSkills | ❌ | ❌ |
| オープンソース | ✅ MIT | ❌ | ❌ |

---

## 📦 対応フレームワーク

| フレームワーク | 検出精度 | テンプレート | テスト済 |
|-----------|---------|------------|---------|
| **Next.js** | 100% | nextjs-tester | ✅ |
| **バニラPHP/Web** | 100% | php-developer, playwright-tester, vanilla-js-developer, mysql-specialist | ✅ |
| **Python ML/CV** | 100% | python-ml-developer, cv-specialist | ✅ |
| **Vue** | 90% | (Next.jsテンプレート) | ✅ |
| **Go** | 85% | go-developer, go-reviewer, concurrency-checker | ✅ |
| **Flutter** | 80% | flutter-developer, widget-reviewer | ✅ |
| **FastAPI** | 80% | api-developer, api-tester, sqlalchemy-specialist | ✅ |
| **React** | 80% | (Next.jsテンプレート) | ✅ |
| **Django** | 80% | (FastAPIテンプレート) | ✅ |
| **iOS Swift** | 80% | swift-developer | ✅ |
| **Flask** | 70% | (FastAPIテンプレート) | ✅ |

**合計**: 11/11フレームワークテスト済 (100%)、15専門テンプレート (~260KB)

**凡例**: ✅ = Week 2テストで検証済み

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
