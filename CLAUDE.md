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

## Claude Code モデル選択ガイド (2025)

**重要**: Haiku 4.5を活用してコスト削減（60-80%）

### モデル選択ルール

| タスク | モデル | 理由 |
|-------|--------|------|
| 単純な修正(1-2ファイル) | Haiku 4.5 | コスト3-5倍安い |
| テスト実行・検証 | Haiku 4.5 | 定型作業 |
| バージョン番号更新 | Haiku 4.5 | 機械的作業 |
| 複雑なリファクタリング | Sonnet 4.5 | 高精度な推論が必要 |
| コードベース探索 | Sonnet 4.5 | コンテキスト理解が重要 |

**詳細**: `docs/2025_BEST_PRACTICES.md` の「Model Selection」セクション

---

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
2. **ユーザ確認**: 自動生成前に必ず確認プロンプト
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

## サブエージェント トークン最適化戦略（2025年版）

### 🔑 Core Principle: Researchers, Not Implementers

**重要**: サブエージェントは「調査・分析」のみ行い、実装は親エージェントが担当

この原則により、トークン使用量を**50-60%削減**できます。

#### ❌ 悪い例（トークン浪費）

```text
User: "全APIエンドポイントをレビューして"

親エージェント → api-reviewer サブエージェント
  サブエージェントが全ファイルを読み込み
  詳細なレポート（10,000トークン）を返す
  親エージェントがコンテキストに追加
  → トークン消費: 25,000
```

#### ✅ 良い例（トークン効率的）

```text
User: "全APIエンドポイントをレビューして"

親エージェント → api-reviewer サブエージェント
  サブエージェントが調査し、Markdownサマリーを返す:
  「## 発見事項
   - endpoint1.py: 認証なし（要修正）
   - endpoint2.py: エラーハンドリング不足
   → 詳細は .claude/review-summary.md に保存済み」
  → トークン消費: 8,000（68%削減）
```

### 📝 Markdown Shared Memory Pattern

**最も効果的なトークン削減手法（3-4倍の効率化）**

```text
サブエージェント:
1. 詳細な調査を実行
2. 結果を .claude/reports/[task-name]-YYYYMMDD.md に保存
3. 親エージェントには3-5行のサマリーのみ返す

親エージェント:
1. サマリーで判断
2. 必要な場合のみ .claude/reports/*.md を読む
```

**実装例:**

```markdown
## サブエージェントの出力フォーマット

### Summary (3-5 lines)
- Key finding 1
- Key finding 2
- Key finding 3

### Details
Saved to: `.claude/reports/api-review-20251031.md`

### Recommendations
1. [Action item 1]
2. [Action item 2]
```

### ⚡ Context Compression（60-80%削減）

**原則**: サブエージェントに渡すコンテキストを最小化

```python
# ❌ 悪い例
def delegate_to_subagent(full_codebase_context):
    # 全コンテキストを渡す（50,000トークン）
    result = subagent.execute(full_codebase_context)

# ✅ 良い例
def delegate_to_subagent(task):
    # 必要なファイルパスのみ渡す（500トークン）
    relevant_files = ["api/users.py", "api/auth.py"]
    result = subagent.execute({
        "task": task,
        "files": relevant_files  # サブエージェント内で読み込む
    })
```

### 📍 Just-in-Time Context Loading

**原則**: ファイルパスや識別子を保持し、必要な時のみロード

```text
❌ 悪い例: 事前に全ファイルを読み込む（20,000トークン）
✅ 良い例: ファイルパスのリストを保持し、必要な時に Read ツールで取得（2,000トークン）
```

**実装パターン:**

```markdown
## サブエージェントのContext Loading戦略

1. **Initial（概要取得）**:
   - mcp__serena__get_symbols_overview でファイル構造のみ取得
   - トークン: ~500

2. **Targeted（必要な部分のみ）**:
   - mcp__serena__find_symbol で特定のシンボルを取得
   - トークン: ~2,000

3. **Full Read（最終手段）**:
   - 小さいファイル(<200行)のみ
   - トークン: ~3,000
```

### 🚨 並列処理コスト管理（重要）

**危険**: Claude Codeは自動で5つ以上の並列サブエージェントを起動可能

**問題**: トークンを急速に消費し、クォータを使い果たす

**ガイドライン**:

```yaml
✅ 許可される並列処理:
  - 独立した2-3タスク
    例: "テスト実行" + "ドキュメント生成"
  - 最大トークン予測: 各20k × 3 = 60k
  - 時間節約: 30分以上

❌ 禁止される並列処理:
  - 5+サブエージェント同時起動
  - トークン予測なしの無制限並列化
  - 単純タスクの過剰な分割
```

**モニタリング**:

```bash
# トークン使用量の確認（推奨）
# 各サブエージェント起動前に推定値をログ出力
echo "Estimated tokens: 15,000 (within budget)"
```

### 🔧 Token-Efficient Tools (Anthropic公式機能)

**2025年2月リリース**: `token-efficient-tools-2025-02-19` ベータヘッダー

**使用方法**（API統合時）:

```python
# Claude API使用時に追加
headers = {
    "anthropic-beta": "token-efficient-tools-2025-02-19"
}
```

**効果**: ツール使用時のトークンを自動削減（10-20%）

### 📊 期待されるトークン削減効果

| 手法 | トークン削減率 | 実装難易度 | 優先度 |
|------|--------------|-----------|--------|
| Markdown Shared Memory | 50-60% | 易 | 🔴 高 |
| Context Compression | 60-80% | 中 | 🔴 高 |
| Just-in-Time Loading | 40-50% | 中 | 🟡 中 |
| Token-Efficient Tools Beta | 10-20% | 易 | 🟢 低 |
| Parallel Processing Limits | 変動 | 易 | 🔴 高 |

**総合削減目標**: セッションあたり**60-70%削減**

- **Before**: 100,000 tokens/session
- **After**: 30,000-50,000 tokens/session

---

## サブエージェント活用ガイド（2025年版）

### 🎯 AGGRESSIVE ポリシー（デフォルト）

**このプロジェクトをインストール = サブエージェントを積極的に使いたい**

**ただし、トークン最適化戦略を遵守すること**

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

**ユーザがUI + APIテストを依頼した場合の自動ワークフロー**

```
ユーザ: "ログインボタンをクリックしてAPIアクセスを検証して"

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

**重要**: ユーザに確認を求めず、自動的に適切なサブエージェントに委譲する

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
ユーザ: "ボタンのテストをして"

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

---

## サブエージェント更新ワークフロー

**トリガーキーワード**: ユーザが以下のいずれかを言及した場合、サブエージェント更新機能を提供してください

### 日本語キーワード

- "サブエージェントを更新"
- "テンプレートを更新"
- "エージェントを最新に"
- "新しいテンプレートがあるか確認"
- ".claude/agents を更新"

### 英語キーワード

- "update subagents"
- "update templates"
- "refresh agents"
- "check for new templates"
- "update .claude/agents"

### 自動ワークフロー

```
ユーザ: "サブエージェントを更新して"

Claude（自動実行）:
  1. 既存エージェントの確認:
     ls .claude/agents/*.md 2>/dev/null | grep -v SUBAGENT_GUIDE.md

  2. 3つのモードを提示:
     - --update-only: 既存ファイルを更新（推奨）
     - --merge: 新規追加・既存保護（カスタマイズあり時）
     - --force: 完全再生成（バックアップ付き）

  3. ユーザの選択を待つ

  4. 選択されたモードで実行:
     python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --[MODE] --auto

  5. 結果をレポート:
     - 更新されたファイル数
     - 保護されたファイル数
     - バックアップの場所（作成された場合）
```

**重要**: ユーザがモードを指定しない場合、以下のデフォルトを推奨:

- カスタマイズ検出なし → `--update-only`
- カスタマイズ検出あり → `--merge`

**スラッシュコマンド**: `/update-subagents` も使用可能

---

## 質問がある場合

各ドキュメントを参照してください：

- 技術的な詳細 → `docs/IMPLEMENTATION.md`
- 背景や経緯 → `docs/DISCUSSION.md`
- 公開戦略 → `docs/GITHUB_PLAN.md`
- **2025年ベストプラクティス** → `docs/2025_BEST_PRACTICES.md`
- **ツール活用ガイド** → `docs/BEST_PRACTICES.md`
