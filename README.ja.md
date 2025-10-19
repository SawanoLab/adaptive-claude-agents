# Adaptive Claude Agents

> **🚧 ステータス**: Phase 2 完了！
> コア検出 + 10フレームワーク対応完了。Phase 3（適応的レビュー）近日公開！

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Development Status](https://img.shields.io/badge/status-pre--alpha-red)](https://github.com/SawanoLab/adaptive-claude-agents)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

[English README](./README.md)

プロジェクト固有の**Claude Codeサブエージェントを自動生成**し、**開発フェーズ**に応じて振る舞いを調整します。

---

## 🎯 これは何？

### 解決する課題

Claude Codeで新規プロジェクトを始めるのは面倒です：

- 技術スタックごとに手動でサブエージェントを作成
- プロトタイプと本番コードで同じ厳格なレビュー
- プロジェクトの成熟に伴うエージェントの再設定

### 解決策

**Adaptive Claude Agents**は2つの革新的な機能でこれを解決：

#### 1. 🔍 自動検出と生成

プロジェクト構造を分析し、適切なサブエージェントを自動生成：

```bash
# 検出: Next.js + TypeScript + Tailwind CSS
→ 生成: nextjs-tester, component-reviewer, type-checker

# 検出: FastAPI + PostgreSQL + pytest
→ 生成: fastapi-tester, api-reviewer, db-schema-checker
```

**グローバルClaude Skills**として統合 - すべてのプロジェクトで動作！

#### 2. 📊 フェーズ適応型レビュー濃度 ⭐ **新規アプローチ**

**伝統的なQA原則をAIエージェントに適用した初のツール：**

| フェーズ | レビュー焦点 | チェック内容 | 例 |
|---------|------------|------------|-----|
| **プロトタイプ** | "動く？" | 基本機能のみ | パフォーマンス、スタイルは無視 |
| **MVP** | "安全？" | 一般的な脆弱性 | 基本的なセキュリティ監査 |
| **本番** | "完璧？" | すべて | 完全な監査 + 最適化 |

コードベースの開発フェーズマーカーに基づいて自動調整します。

---

## ✨ 主な機能

- ✅ **ゼロコンフィグ**: すぐに動作
- ✅ **技術スタック非依存**: 10フレームワーク対応（Next.js、FastAPI、バニラPHP、Python ML、iOS Swiftなど）
- ✅ **フェーズ対応**: レビュー濃度を自動調整
- ✅ **グローバルSkills**: 一度の設定で全プロジェクトで利用可能
- ✅ **コミュニティテンプレート**: 新しい技術スタックの追加が容易
- ✅ **Progressive Disclosure**: Anthropicのベストプラクティスに準拠

---

## 🚀 クイックスタート

> **注意**: Phase 1リリースで提供予定

### インストール（予定）

```bash
# グローバルClaude Skillとしてインストール
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
```

### 使い方（予定）

1. Claude Codeでプロジェクトを開く
2. Skillが技術スタックを自動検出
3. サブエージェント生成前に確認
4. 最適化されたエージェントでコーディング開始！

```
検出: Next.js + TypeScript + Tailwind CSS
以下のサブエージェントを生成しますか？
  - nextjs-tester (Vitest + Testing Library)
  - component-reviewer (React ベストプラクティス)
  - type-checker (TypeScript strict mode)
[Y/n]
```

---

## 📁 プロジェクト構造

```
adaptive-claude-agents/
├── skills/                 # Claude Skills実装
│   ├── project-analyzer/   # 自動検出ロジック
│   └── adaptive-review/    # フェーズ対応レビュー
├── templates/              # サブエージェントテンプレート
│   ├── nextjs/
│   ├── fastapi/
│   ├── react-native/
│   └── go/
├── examples/               # 使用例
└── docs/                   # ドキュメント
```

---

## 🛣️ ロードマップ

- [x] プロジェクト構想と計画
- [x] **Phase 1**: 基本プロジェクト分析器 ✅
  - [x] 技術スタック検出
  - [x] Next.jsテンプレート
  - [x] 基本的なサブエージェント生成
- [x] **Phase 2**: 複数の技術スタック（2週間）✅
  - [x] FastAPI、バニラPHP、Python ML、iOS Swiftテンプレート
  - [x] 検出精度の向上
  - [x] 10フレームワーク、13テンプレート実装完了
- [ ] **Phase 3**: 適応的レビュー濃度（3週間）
  - [ ] フェーズ検出ロジック
  - [ ] フェーズ別サブエージェント
- [ ] **Phase 4**: パブリックベータリリース

詳細な進捗は[内部プロジェクトボード](https://github.com/SawanoLab/adaptive-claude-agents/projects)をご覧ください。

---

## 📦 対応フレームワーク（Phase 2）

| フレームワーク | テンプレート | ステータス |
|--------------|------------|----------|
| **Next.js** | tester | ✅ Phase 1 |
| **バニラPHP/Web** | php-developer, playwright-tester, vanilla-js-developer, mysql-specialist | ✅ Phase 2 |
| **FastAPI** | api-developer, api-tester, sqlalchemy-specialist | ✅ Phase 2 |
| **Python ML/CV** | python-ml-developer, cv-specialist | ✅ Phase 2 |
| **iOS Swift** | swift-developer | ✅ Phase 2 |
| **React** | 基本検出のみ | 🚧 Phase 1 |
| **Vue** | 基本検出のみ | 🚧 Phase 1 |
| **Django** | 基本検出のみ | 🚧 Phase 1 |
| **Flask** | 基本検出のみ | 🚧 Phase 1 |
| **Flutter** | 基本検出のみ | 🚧 Phase 1 |

**合計**: 10フレームワーク検出、13専門テンプレート

---

## 🆚 既存ツールとの違い

| 機能 | [claude-init](https://github.com/dimitritholen/claude-init) | **Adaptive Claude Agents** |
|------|-------------|---------------------------|
| **実行タイミング** | 初期セットアップのみ | 継続的（Skillsベース） |
| **フェーズ適応** | ❌ なし | ✅ **独自機能** |
| **更新** | プロジェクト開始時のみ | 継続的 |
| **統合方法** | CLIツール | Claude Skills |
| **技術スタック検出** | 手動 | 自動 |

**補完的ツール**: 初期セットアップには`claude-init`を使い、その後の開発にAdaptive Claude Agentsを使うことをお勧めします！

---

## 🤝 コントリビューション

貢献を歓迎します！このプロジェクトは初期開発中 - 参加する絶好のタイミングです。

### 貢献方法

- 💡 **アイデア・フィードバック**: [GitHub Issue](https://github.com/SawanoLab/adaptive-claude-agents/issues)を開く
- 🐛 **バグ報告**: 問題を報告（コードができたら！）
- 📝 **テンプレート**: 新しい技術スタックのサポートを追加
- 📖 **ドキュメント**: ガイドや例を改善
- 🌍 **翻訳**: ドキュメントの翻訳を手伝う

詳細なガイドラインは[CONTRIBUTING.md](./CONTRIBUTING.md)をご覧ください。

### 優先的に必要な貢献

- **テンプレート**: Django、Flask、Vue、Angular、Flutter
- **検出ロジック**: 精度向上
- **ドキュメント**: チュートリアル、ビデオ
- **テスト**: ユニット・統合テスト

---

## 📚 ドキュメント

- [コントリビューションガイド](./CONTRIBUTING.md) - 貢献方法
- [ライセンス](./LICENSE) - MITライセンス

**内部開発ドキュメント**（公開リポジトリには含まれません）：

- 設計議論
- 実装詳細
- リリース戦略

---

## 🌟 インスピレーションとクレジット

このプロジェクトは以下から着想を得ています：

- [claude-init](https://github.com/dimitritholen/claude-init) by @dimitritholen
- [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) by @VoltAgent
- 伝統的なソフトウェアQAベストプラクティス

フィードバックとアイデアをくれたClaude Codeコミュニティに感謝！

---

## 📄 ライセンス

[MITライセンス](./LICENSE) - Copyright (c) 2025 Sawano Hiroaki

---

## 🙋 作者

Sawano Hiroaki

- GitHub: [@SawanoLab](https://github.com/SawanoLab)

---

## ⭐ Star履歴

このプロジェクトが興味深いと思ったら、Starして開発をフォローしてください！

[![Star History Chart](https://api.star-history.com/svg?repos=SawanoLab/adaptive-claude-agents&type=Date)](https://star-history.com/#SawanoLab/adaptive-claude-agents&Date)

---

**ステータス**: プレアルファ | **次のマイルストーン**: Phase 1完了（予定：2週間後）

Claude Codeコミュニティのために ❤️ を込めて
