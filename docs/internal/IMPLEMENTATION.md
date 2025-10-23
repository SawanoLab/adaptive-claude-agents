# 実装計画

## プロジェクト構成

### 1. プロジェクト自動分析Skill

**ファイル**: `skills/project-analyzer/SKILL.md`

```markdown
---
name: project-analyzer
description: MUST BE USED when starting work in a new project. Analyzes project structure and creates appropriate subagents automatically.
---

## 目的
プロジェクトの技術スタックを自動検出し、適切なサブエージェントセットを生成

## 実行フロー
1. プロジェクトルートのファイルを確認
2. 技術スタック判定スクリプトを実行
3. テンプレートから適切なサブエージェントを生成
4. .claude/agents/に配置

## プロジェクトタイプ判定
- package.json存在 → Node.js系
- requirements.txt存在 → Python系
- go.mod存在 → Go
- 詳細分析でフレームワーク特定
```

**必要なスクリプト**:
- `analyze_project.py`: プロジェクト構造を解析
- `detect_stack.py`: 技術スタック判定
- `generate_agents.py`: サブエージェント生成

### 2. 適応的レビューSkill

**ファイル**: `skills/adaptive-review/SKILL.md`

```markdown
---
name: adaptive-review
description: Provides phase-aware code review guidance. Adjusts review rigor based on development phase.
---

## 目的
開発フェーズに応じてレビュー濃度を自動調整

## フェーズ判定
CLAUDE.mdから現在のフェーズを読み取り

## レビュー基準
### プロトタイプ期
- 動作確認のみ
- パフォーマンス無視
- スタイル無視

### MVP開発期
- 基本セキュリティ
- 明らかなバグ
- 主要機能のテスト

### 本番前期
- フルセキュリティ監査
- パフォーマンス最適化
- 完全なドキュメント
- 高テストカバレッジ
```

## サブエージェントテンプレート

### Next.js用テンプレート

`templates/nextjs/tester.md`:
```markdown
---
name: nextjs-tester
description: Next.js application testing specialist
tools: Bash, Read, Write
---

あなたはNext.js + TypeScript + Jestの専門家です。

## テスト戦略
- Jestでユニットテスト
- Testing Libraryでコンポーネントテスト
- Playwrightで E2Eテスト

## 実行手順
1. package.jsonでテストコマンド確認
2. 既存テストパターンを学習
3. テスト作成・実行
```

### FastAPI用テンプレート

`templates/fastapi/tester.md`:
```markdown
---
name: fastapi-tester
description: FastAPI testing expert with pytest
tools: Bash, Read, Write
---

あなたはFastAPI + pytest + pytest-asyncioの専門家です。

## テスト戦略
- pytestでユニットテスト
- TestClientでAPIテスト
- 非同期テスト対応

## 実行手順
1. pyproject.toml or setup.pyでテスト設定確認
2. 既存テストパターンを学習
3. テスト作成・実行
```

## 実装フェーズ

### Phase 1: 基本構造（1-2週間）

**目標**: プロジェクト分析の基本機能

- [ ] プロジェクト構造の確定
- [ ] 基本的なプロジェクト分析スクリプト
- [ ] 1つの技術スタック（Next.js）のテンプレート
- [ ] 動作確認

**成果物**:
- `skills/project-analyzer/SKILL.md`
- `skills/project-analyzer/analyze_project.py`
- `templates/nextjs/tester.md`

### Phase 2: テンプレート拡充（1-2週間）

**目標**: 複数の技術スタック対応

- [ ] FastAPIテンプレート
- [ ] React Nativeテンプレート
- [ ] Goテンプレート
- [ ] 技術スタック自動判定の精度向上

**成果物**:
- `templates/`配下に複数のテンプレート

### Phase 3: 適応的レビュー（2-3週間）

**目標**: 開発フェーズ適応機能

- [ ] フェーズ判定ロジック
- [ ] フェーズ別サブエージェント
- [ ] CLAUDE.mdとの連携
- [ ] 動作確認

**成果物**:
- `skills/adaptive-review/SKILL.md`
- `templates/`配下にフェーズ別エージェント

### Phase 4: 統合とドキュメント（1週間）

**目標**: 公開準備

- [ ] インストールスクリプト
- [ ] 使用例の作成
- [ ] ドキュメント整備
- [ ] README.md完成

## 技術スタック

### 開発環境
- Python 3.9+（スクリプト用）
- Claude Code
- Git

### 依存ライブラリ
```python
# requirements.txt
pyyaml>=6.0
tomli>=2.0  # pyproject.toml解析
```

## テスト戦略

### 手動テスト
1. 新規Next.jsプロジェクトで動作確認
2. 既存FastAPIプロジェクトで動作確認
3. フェーズ変更時の振る舞い確認

### 自動テスト（後で追加）
- プロジェクト分析ロジックの単体テスト
- テンプレート生成の統合テスト

## リスクと対策

### リスク1: 技術スタック判定の誤り
**対策**: 
- 複数の判定基準を使用
- ユーザーに確認プロンプト表示
- 手動上書き機能

### リスク2: テンプレートの陳腐化
**対策**:
- コミュニティからのフィードバック収集
- 定期的な更新
- バージョン管理

### リスク3: 過度な自動化
**対策**:
- 生成前にプレビュー表示
- ユーザーの承認を必須に
- 簡単に無効化できる仕組み

## 成功基準

### MVP成功基準
- [ ] 3つ以上の技術スタックに対応
- [ ] プロジェクト分析の精度80%以上
- [ ] 実際のプロジェクトで動作確認
- [ ] ドキュメント完成

### 公開準備完了基準
- [ ] 5人以上のベータテスター
- [ ] フィードバック反映
- [ ] 包括的なドキュメント
- [ ] インストールが5分以内
