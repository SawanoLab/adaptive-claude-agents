# Adaptive Claude Agents - Development Context

## プロジェクト概要

Claude Codeのサブエージェントを、プロジェクトの種類と開発フェーズに応じて自動的に生成・適応させるフレームワークを開発しています。

## 主要な革新点

### 1. プロジェクト自動分析とサブエージェント自動生成
- プロジェクトの技術スタックを自動検出
- 適切なサブエージェントセットを自動生成
- グローバルSkillsとして統合

### 2. 開発フェーズに適応するレビュー濃度調整（完全に新規のアイデア）
- プロトタイプ期：軽いレビュー
- MVP開発期：中程度のレビュー  
- 本番前：厳格なレビュー

## 開発フェーズ

**現在**: Phase 1 - 基本構造の実装

## コーディング規約

### Python
- PEP 8準拠
- 型ヒント必須（Python 3.9+）
- Docstring形式：Google Style

### Markdown
- リンクは相対パス使用
- コードブロックには言語指定必須

### ファイル構成
```
skills/          # Claude Skills実装
templates/       # サブエージェントテンプレート
examples/        # 使用例
docs/            # ドキュメント
tests/           # テスト（将来追加）
```

## 重要な設計原則

1. **Progressive Disclosure**: Anthropicの推奨パターンに従う
2. **ユーザー確認**: 自動生成前に必ず確認プロンプト
3. **モジュール性**: 各テンプレートが独立して動作
4. **透明性**: 判定ロジックをログに記録

## 参考ドキュメント

- `docs/DISCUSSION.md` - このアイデアが生まれた経緯
- `docs/IMPLEMENTATION.md` - 実装計画と技術仕様
- `docs/GITHUB_PLAN.md` - 公開計画と懸念点

## タスク管理

Phase 1の主要タスク:
- [ ] プロジェクト構造の確定
- [ ] 基本的なプロジェクト分析スクリプト
- [ ] Next.jsテンプレート作成
- [ ] 動作確認

## バージョン管理

**重要**: バージョン番号は一元管理されています。

### バージョン更新手順

```bash
# 1. 自動更新スクリプトを実行
./scripts/update-version.sh 0.5.0-beta

# 2. CHANGELOG.mdを手動更新
# 3. git diff で確認
# 4. git add -A && git commit
# 5. git tag v0.5.0-beta && git push origin main --tags
```

**自動更新されるファイル**:
- `VERSION` (真実の唯一の情報源)
- `install.sh`
- `README.md`
- `README.ja.md`

**詳細**: `docs/VERSION_MANAGEMENT.md` を参照

## コミット規約

```
feat: 新機能
fix: バグ修正
docs: ドキュメント変更
refactor: リファクタリング
test: テスト追加
chore: バージョン更新、ビルド設定など
```

## 開発時の注意点

1. **既存ツールとの差別化を明確に**
   - claude-initは初期セットアップのみ
   - 本プロジェクトはグローバルSkillsとして常時動作

2. **フェーズ適応機能の重要性**
   - これが最大の差別化ポイント
   - ドキュメントで強調

3. **コミュニティフレンドリー**
   - テンプレート追加が容易
   - 貢献しやすい設計

## サブエージェント活用ガイド（2025年版）

### 🎯 AGGRESSIVE ポリシー（デフォルト）

**このプロジェクトをインストール = サブエージェントを積極的に使いたい**

以下の条件に該当する場合、**必ずTaskツールでサブエージェントを使用してください:**

#### 必須ルール（MANDATORY）

1. **3+ ファイルの類似修正**
   - 例: "assessment.js, soap.js, nursing_plan.js に同じパターン適用"
   - サブエージェント: `general-purpose`
   - 節約時間: 30-60分

2. **コードベース全体の探索**
   - 例: "version_number はどこで使われているか"
   - サブエージェント: `Explore` (thoroughness: "very thorough")
   - 節約時間: 60-90分

3. **E2Eテスト実行**
   - 例: "ログイン → API呼び出し → DB検証をテスト"
   - サブエージェント: `general-purpose` + `chrome-devtools-tester`
   - 節約時間: 45分以上

4. **並行可能な独立タスク（2つ以上）**
   - 例: ".gitignore更新 + UIコンポーネントのリファクタリング"
   - サブエージェント: 複数の `general-purpose` を単一メッセージで
   - 節約時間: 30分以上

#### コスト vs 時間のトレードオフ

| タスクタイプ | 直接実行コスト | サブエージェントコスト | 節約時間 | **推奨** |
|------------|--------------|---------------------|---------|---------|
| 単一ファイル編集 | 5k トークン | 25k トークン | 0分 | ❌ 直接 |
| 類似パターン（3-4ファイル） | 15k トークン | 35k トークン | 30分 | ✅ サブエージェント |
| 大規模リファクタリング（5+ファイル） | 30k トークン | 50k トークン | 60分 | ✅✅ サブエージェント |
| コードベース検索 | 40k トークン | 60k トークン | 90分 | ✅✅✅ Explore |

**原則**: 20kトークンのオーバーヘッドは30分以上の節約で正当化される

#### 禁止事項

- ❌ 単一ファイルの小規模修正にサブエージェント使用（コスト過多）
- ❌ 5+ファイルの修正でサブエージェント不使用（時間浪費）
- ❌ トークン節約のための過度な直接実行（非効率）

#### 目標メトリクス

- **サブエージェント使用率**: 複雑なタスクの20-30%
- **週あたり節約時間**: 2-4時間
- **トークン効率**: 30分以上の節約で20kオーバーヘッドを許容

---

### Web Service Testing Auto-Workflow

**ユーザーがUI + APIテストを依頼した場合の自動ワークフロー**

```
ユーザー: "ログインボタンをクリックしてAPIアクセスを検証して"

主エージェント（分析）:
  - UIキーワード検出: "ボタン", "クリック"
  - APIキーワード検出: "API", "アクセス"
  → Sequential workflow: Browser testing → API testing

主エージェント（実行）:
  1. "I'll validate the UI with Chrome DevTools, then test the API endpoint..."
  2. chrome-devtools-tester に委譲（自動）
  3. api-tester に自動チェーン
  4. 統合レポート生成
```

**重要**: ユーザーに確認を求めず、自動的に適切なサブエージェントに委譲する

### ブラウザ自動化の選択ロジック

**デフォルト: chrome-devtools-tester（90%のケース）**

```
トリガーキーワード:
  - パフォーマンス: "性能", "パフォーマンス", "Core Web Vitals"
  - デバッグ: "デバッグ", "debug", "エラー"
  - UI: "見た目", "CSS", "クリック", "ボタン"（クロスブラウザ不要時）
```

**Playwrightへエスカレート（必要時のみ）**

```
トリガーキーワード:
  - クロスブラウザ: "Firefox", "Safari", "クロスブラウザ"
  - CI/CD: "CI", "GitHub Actions", "パイプライン"
  - E2E: "E2E", "end-to-end", "統合テスト"
```

**積極的提案パターン**

```
ユーザー: "ボタンのテストをして"

主エージェント:
"Chrome専用テストのため、chrome-devtools-testerを使用します。
クロスブラウザテスト（Firefox/Safari）が必要な場合はplaywrightに切り替えられます。
Chrome DevToolsで進めます..."
```

### 2025年ベストプラクティス参照

各フレームワークの最新推奨事項は以下を参照:

- **総合ガイド**: `docs/2025_BEST_PRACTICES.md`
- **ツールアクセスポリシー**: `docs/BEST_PRACTICES.md` (Tool Access Policy セクション)

**主要な推奨事項**:

- **Browser**: Chrome DevTools（デフォルト）、Playwright（クロスブラウザ時のみ）
- **Next.js 15**: Turbopack + App Router + ISR
- **FastAPI**: Async-first、asyncpg/databases使用
- **Go**: Gin推奨（エコシステム）、Fiber（最速）
- **Flutter**: Riverpod推奨（2025標準）
- **Python ML/CV**: PyTorch（研究）、TensorFlow（本番）
- **iOS Swift**: SwiftUI + UIKitハイブリッド
- **React State**: Zustand推奨

## 質問がある場合

各ドキュメントを参照してください：
- 技術的な詳細 → `docs/IMPLEMENTATION.md`
- 背景や経緯 → `docs/DISCUSSION.md`
- 公開戦略 → `docs/GITHUB_PLAN.md`
- **2025年ベストプラクティス** → `docs/2025_BEST_PRACTICES.md`
- **ツール活用ガイド** → `docs/BEST_PRACTICES.md`
