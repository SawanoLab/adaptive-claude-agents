# Subagent Update Workflow Test Guide

このガイドは、サブエージェント更新機能が正しく動作することを確認するためのテストシナリオです。

## 前提条件

1. Adaptive Claude Agents v1.0.0+ がインストール済み
2. テスト用プロジェクトが存在する
3. Claude Code環境で実行

## テストシナリオ

### シナリオ 1: 自然言語でのトリガー（日本語）

**ユーザー入力**:
```
サブエージェントを更新して
```

**期待される動作**:

1. ✅ Claude が `.claude/agents/` の存在を確認
2. ✅ 3つの更新モードを提示:
   - `--update-only`: 既存ファイルのみ更新
   - `--merge`: 新規追加・既存保護
   - `--force`: 完全再生成
3. ✅ ユーザーに選択を促す
4. ✅ 選択後、適切なコマンドを実行
5. ✅ 結果サマリーを表示

**検証ポイント**:
- [ ] 既存エージェント数が正しく検出される
- [ ] 各モードの説明が明確
- [ ] 選択したモードが正しく実行される
- [ ] バックアップが作成される（merge/forceモード時）

---

### シナリオ 2: 自然言語でのトリガー（英語）

**ユーザー入力**:
```
update my subagents
```

**期待される動作**:

シナリオ1と同じ

**検証ポイント**:
- [ ] 英語キーワードでも正しくトリガーされる
- [ ] UI表示は日本語/英語のいずれか適切な方

---

### シナリオ 3: スラッシュコマンド

**ユーザー入力**:
```
/update-subagents
```

**期待される動作**:

1. ✅ コマンドがロードされる
2. ✅ インタラクティブなワークフローが開始
3. ✅ シナリオ1と同じフロー

**検証ポイント**:
- [ ] スラッシュコマンドが認識される
- [ ] 同じワークフローが実行される

---

### シナリオ 4: 初回生成（エージェントが存在しない場合）

**前提条件**: `.claude/agents/` ディレクトリが存在しないプロジェクト

**ユーザー入力**:
```
サブエージェントを更新して
```

**期待される動作**:

1. ✅ エージェントが存在しないことを検出
2. ✅ 初回生成を提案:
   ```
   ⚠️  No existing subagents found. Would you like to generate them for the first time?
   ```
3. ✅ 初回生成コマンドを提示または実行

**検証ポイント**:
- [ ] 存在しない場合の適切なメッセージ
- [ ] 初回生成へのスムーズな誘導

---

### シナリオ 5: update-only モード

**ユーザー入力**:
```
サブエージェントを更新して
```
**モード選択**: 1 (--update-only)

**期待される動作**:

1. ✅ 既存ファイルのみ更新
2. ✅ 新規ファイルは追加されない
3. ✅ バックアップは作成されない
4. ✅ サマリー表示:
   ```
   📊 Summary:
   • Updated: 3 existing agent(s)
   • Preserved: 2 customized agent(s)
   ```

**検証ポイント**:
- [ ] ファイル数が変わらない
- [ ] 既存ファイルのタイムスタンプが更新される
- [ ] バックアップディレクトリが作成されない

---

### シナリオ 6: merge モード

**前提条件**:
1. 既存エージェントにカスタマイズを追加
   ```bash
   echo "# MY CUSTOM SECTION" >> .claude/agents/nextjs-tester.md
   ```

**ユーザー入力**:
```
サブエージェントを更新して
```
**モード選択**: 2 (--merge)

**期待される動作**:

1. ✅ バックアップ作成: `.claude/agents.backup.YYYYMMDD-HHMMSS/`
2. ✅ 既存ファイルは変更されない（カスタマイズ保護）
3. ✅ 新規テンプレートのみ追加
4. ✅ サマリー表示:
   ```
   📊 Summary:
   • Preserved: 3 customized agent(s)
   • Generated: 2 new agent(s)
   📦 Backup: .claude/agents.backup.20251024-123456/
   ```

**検証ポイント**:
- [ ] カスタマイズが保持されている
- [ ] 新規ファイルが追加される
- [ ] バックアップが作成される
- [ ] バックアップの内容が元のファイルと一致

---

### シナリオ 7: force モード

**ユーザー入力**:
```
サブエージェントを更新して
```
**モード選択**: 3 (--force)

**期待される動作**:

1. ✅ バックアップ作成: `.claude/agents.backup.YYYYMMDD-HHMMSS/`
2. ✅ 全ファイル再生成
3. ✅ カスタマイズは失われる（バックアップに残る）
4. ✅ サマリー表示:
   ```
   📊 Summary:
   • Updated: 3 existing agent(s)
   📦 Backup: .claude/agents.backup.20251024-123456/
   ```

**検証ポイント**:
- [ ] すべてのファイルが最新テンプレートに置き換わる
- [ ] カスタマイズは削除される
- [ ] バックアップにカスタマイズが残っている

---

## クイックテストコマンド

### 準備

```bash
# テストプロジェクト作成
mkdir -p /tmp/test-update-workflow
cd /tmp/test-update-workflow
echo '{"name": "test", "dependencies": {"next": "15.0.0"}}' > package.json

# 初回生成
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --auto
```

### テスト 1: update-only

```bash
# Claude Codeで実行
"サブエージェントを更新して"
# モード選択: 1

# 検証
ls -la .claude/agents/
# 期待: ファイル数変わらず、タイムスタンプ更新
```

### テスト 2: merge（カスタマイズあり）

```bash
# カスタマイズ追加
echo "# CUSTOM" >> .claude/agents/nextjs-tester.md

# Claude Codeで実行
"サブエージェントを更新して"
# モード選択: 2

# 検証
grep "CUSTOM" .claude/agents/nextjs-tester.md
# 期待: "CUSTOM"が見つかる
ls .claude/agents.backup.*/
# 期待: バックアップディレクトリ存在
```

### テスト 3: force

```bash
# Claude Codeで実行
"サブエージェントを更新して"
# モード選択: 3

# 検証
grep "CUSTOM" .claude/agents/nextjs-tester.md || echo "Customization removed (expected)"
# 期待: カスタマイズ削除
grep "CUSTOM" .claude/agents.backup.*/nextjs-tester.md
# 期待: バックアップにカスタマイズが残っている
```

---

## トラブルシューティング

### 問題: Claudeが更新ワークフローをトリガーしない

**原因**: キーワードが認識されていない

**解決策**:
1. CLAUDE.mdの「サブエージェント更新ワークフロー」セクションを確認
2. より明示的に: "update subagents using --merge mode"

### 問題: モード選択が反映されない

**原因**: コマンド構築エラー

**解決策**:
1. 手動実行で確認:
   ```bash
   python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --merge --auto
   ```
2. エラーログを確認

### 問題: バックアップが作成されない

**原因**: mergeモードで新規ファイルがない、またはupdate-onlyモード

**解決策**:
- update-onlyモードはバックアップを作成しない（仕様通り）
- mergeモードでバックアップされない場合はログ確認

---

## 成功基準

すべてのシナリオで以下を満たすこと:

- [ ] トリガーキーワードで正しく認識される
- [ ] 3つのモードが明確に説明される
- [ ] 選択したモードが正しく実行される
- [ ] 適切なバックアップが作成される（merge/force時）
- [ ] サマリーが正確に表示される
- [ ] ユーザー体験がスムーズ

---

## 参考

- [SUBAGENT_UPDATE_GUIDE.md](./SUBAGENT_UPDATE_GUIDE.md) - 詳細ガイド
- [SKILL.md](../skills/SKILL.md) - スキル実装詳細
- [CLAUDE.md](../CLAUDE.md) - プロジェクトコンテキスト
