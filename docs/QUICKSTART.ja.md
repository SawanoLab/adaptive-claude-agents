# クイックスタートガイド（5分）

Adaptive Claude Agentsをたった5分で使い始めましょう！

---

## このガイドで学べること

- ✅ Adaptive Claude Agentsのインストール方法
- ✅ 最初のプロジェクトを分析する方法
- ✅ 自動生成されたサブエージェントの使い方
- ✅ 開発フェーズの確認方法

---

## ステップ1: インストール（1分）

### ワンコマンドインストール

```bash
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
```

**実行内容**:

- ✓ システム要件の確認（Python 3.9+、git）
- ✓ Claude Code skillsディレクトリの検出
- ✓ すべてのskillsとテンプレートのインストール
- ✓ インストールの検証

**期待される出力**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Adaptive Claude Agents Installation
  Version: 0.4.0-beta
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ System check passed
✓ Claude Code skills directory found
✓ Installation complete!
```

### 手動インストール（必要な場合）

ワンライナーが動作しない場合：

```bash
# 1. リポジトリをクローン
git clone https://github.com/SawanoLab/adaptive-claude-agents.git

# 2. インストールスクリプトを実行
cd adaptive-claude-agents
./install.sh
```

---

## ステップ2: プロジェクトを分析（2分）

### プロジェクトに移動

```bash
cd /path/to/your/project  # Next.js、FastAPI、PHP等
```

### プロジェクト分析を実行

**方法1: Skillsディレクトリ経由**

```bash
# macOS
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" .

# Linux/WSL
python3 ~/.config/claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py .
```

**方法2: Claude Codeに依頼**（project-analyzer skillが設定されている場合）

> 「プロジェクトを分析して適切なサブエージェントを生成して」

**実行結果**:

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

### 生成されたファイルを確認

```bash
# 生成されたサブエージェントを表示
ls .claude/agents/

# 出力例:
# nextjs-tester.md  (またはフレームワーク固有のエージェント)
```

---

## ステップ3: サブエージェントを使用（1分）

### サブエージェントの呼び出し

Claude Codeで専門サブエージェントを使用できます：

> 「nextjs-testerエージェントを使ってButton.tsxのテストを書いて」

**または手動で呼び出し**:

```
@nextjs-tester Loginコンポーネントのテストを書いて
```

### 何が特別なのか？

生成されたサブエージェントは以下を理解しています：

- ✓ あなたのフレームワーク（Next.js、FastAPI等）
- ✓ あなたの言語（TypeScript、Python等）
- ✓ あなたのツール（Vitest、pytest等）
- ✓ あなたのスタックのベストプラクティス

---

## ステップ4: 開発フェーズを確認（1分）

### 🌟 革新的機能：フェーズ適応レビュー

Claudeに尋ねる：

> 「今どの開発フェーズにいる？」

**出力例**:

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

### フェーズがコードレビューに与える影響

**プロトタイプ**（v0.0.x）:

- 軽いレビュー、機能重視
- テスト不要
- 迅速な反復を促進

**MVP**（v0.x.x）:

- 中程度のレビュー
- テストカバレッジ50%+推奨
- 基本的なセキュリティチェック

**本番**（v1.x.x+）:

- 厳格なレビュー
- テストカバレッジ80%+必須
- 包括的なセキュリティ監査

---

## よくあるタスク

### 異なるプロジェクト用のサブエージェント生成

**Next.jsプロジェクト**:

```
→ 生成: nextjs-tester.md
```

**FastAPIプロジェクト**:

```
→ 生成: api-developer.md, api-tester.md, sqlalchemy-specialist.md
```

**バニラPHPプロジェクト**:

```
→ 生成: php-developer.md, playwright-tester.md, vanilla-js-developer.md, mysql-specialist.md
```

### フェーズ検出のオーバーライド

`.claude/phase.yml`を作成：

```yaml
phase: prototype  # または 'mvp'、'production'
reason: "クライアントデモ用の迅速なプロトタイピング"
expires: 2025-11-01  # オプション：自動復帰
```

### 最新バージョンへの更新

```bash
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/update.sh | bash
```

### アンインストール

```bash
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/uninstall.sh | bash
```

---

## 対応フレームワーク

| フレームワーク | 検出精度 | 利用可能なテンプレート | テスト済 |
|-----------|---------|---------------------|--------|
| **Next.js** | ✅ 100% | tester | ✅ Week 2 |
| **バニラPHP/Web** | ✅ 100% | php-developer, playwright-tester, vanilla-js-developer, mysql-specialist | ✅ Week 2 |
| **FastAPI** | ✅ 80% | api-developer, api-tester, sqlalchemy-specialist | ✅ Week 2 |
| **React** | ✅ 80% | (現在はNext.js testerを使用) | ✅ Week 2 |
| **Vue** | ✅ 90% | (現在はNext.js testerを使用) | ✅ Week 2 |
| **Django** | ✅ 80% | (現在はFastAPIテンプレートを使用) | ✅ Week 2 |
| **Flask** | ✅ 70% | (現在はFastAPIテンプレートを使用) | ✅ Week 2 |
| **Python ML/CV** | ✅ 100% | python-ml-developer, cv-specialist | ✅ Week 2 |
| **iOS Swift** | ✅ 80% | swift-developer | ✅ Week 2 |
| **Go/Flutter** | ⏳ 予定 | TBD | ベータ後 |

**合計**: 9/10フレームワークテスト済（90%）、13専門テンプレート

---

## トラブルシューティング

### "Claude Code skills directory not found"

**解決策**: 環境変数を設定：

```bash
export CLAUDE_SKILLS_DIR="/path/to/your/claude/skills"
./install.sh
```

### "Could not detect tech stack"

**解決策**: `.claude/project.yml`を作成：

```yaml
framework: nextjs  # または fastapi、vanilla-php-web等
version: "14.0.0"
language: typescript
```

### "Python 3.9+ required"

**解決策**: [python.org](https://www.python.org/downloads/)からPython 3.9以降をインストール

### "Wrong phase detected"

**解決策**: `.claude/phase.yml`でオーバーライド（上記参照）

---

## 次のステップ

### さらに学ぶ

- 📖 [完全ドキュメント](../README.ja.md) - 包括的ガイド
- 🎯 [使用例ギャラリー](./EXAMPLES.ja.md) - 実例集
- 🔧 [トラブルシューティングガイド](./TROUBLESHOOTING.ja.md) - 詳細な解決策
- 💡 [コントリビューションガイド](../CONTRIBUTING.md) - 独自テンプレートの追加

### ヘルプ

- 🐛 [Issue報告](https://github.com/SawanoLab/adaptive-claude-agents/issues)
- 💬 [ディスカッション](https://github.com/SawanoLab/adaptive-claude-agents/discussions)
- ⭐ [GitHubでスター](https://github.com/SawanoLab/adaptive-claude-agents)

### 体験を共有

Adaptive Claude Agentsが役立った場合：

- ⭐ リポジトリにスター
- 🐦 ツイート
- 📝 ブログ記事を書く
- 🤝 テンプレートを貢献

---

## 何が違うのか？

### vs GitHub Copilot

- ✅ プロジェクト固有のサブエージェント（汎用ではない）
- ✅ フェーズ適応レビュー（プロジェクト成熟度に適応）
- ✅ 10フレームワークに専門テンプレート

### vs Cursor

- ✅ 自動技術スタック検出
- ✅ 開発フェーズ検出 ⭐ **ユニーク**
- ✅ テンプレートベースのサブエージェント生成

### vs claude-init

- ✅ 継続的（Skillsベース） vs 一回限りのセットアップ
- ✅ フェーズ適応 ⭐ **ユニーク**
- ✅ 自動更新

---

## まとめ

5分で、あなたは：

1. ✅ Adaptive Claude Agentsをインストール
2. ✅ プロジェクトを分析
3. ✅ フレームワーク固有のサブエージェントを生成
4. ✅ フェーズ適応レビューについて学習

**より賢くコーディングする準備が整いました！** 🚀

---

**Happy Coding!**

詳細は[完全ドキュメント](../README.ja.md)を参照するか、[Issueを開いて](https://github.com/SawanoLab/adaptive-claude-agents/issues)ください。
