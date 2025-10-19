# 🚀 Public Beta Launch Steps

実行手順のステップバイステップガイド

---

## ステップ1: GitHub Releaseを作成

### 1-1. Releasesページへ移動

1. https://github.com/SawanoLab/adaptive-claude-agents を開く
2. 右サイドバーの **「Releases」** をクリック
3. **「Create a new release」** または **「Draft a new release」** ボタンをクリック

### 1-2. Releaseフォームに入力

**Choose a tag**:
```
v0.4.0-beta
```
（新規作成。「Create new tag: v0.4.0-beta on publish」を選択）

**Target**:
```
main
```

**Release title**:
```
v0.4.0-beta - Public Beta Release 🚀
```

**Description**:
`docs/internal/RELEASE_NOTES_v0.4.0-beta.md` の内容をコピー&ペースト（行9〜270の全文）

**チェックボックス**:
- ✅ **Set as a pre-release** をチェック（ベータ版なので）
- ❌ **Set as the latest release** はチェック不要（自動で設定される）

### 1-3. Publish

**「Publish release」** ボタンをクリック

✅ 完了！Release v0.4.0-betaが作成されます

---

## ステップ2: リポジトリ設定を更新

### 2-1. Repository Settingsを開く

1. https://github.com/SawanoLab/adaptive-claude-agents/settings を開く
2. **「General」** タブ（デフォルトで開いている）

### 2-2. Descriptionを設定

**Description** (画面上部):
```
Auto-generate specialized Claude Code subagents for your stack. Phase-adaptive code review. 10 frameworks, 13 templates. MIT licensed.
```

**Website** (オプション):
```
（空欄のまま、またはREADMEのURL）
```

### 2-3. Topicsを追加

**Topics** (Descriptionの下):

以下のトピックを追加（1つずつ入力してEnter）:

**必須10個**:
1. `claude-code`
2. `claude-ai`
3. `ai-agents`
4. `developer-tools`
5. `code-generation`
6. `tech-stack-detection`
7. `code-review`
8. `adaptive-systems`
9. `nextjs`
10. `fastapi`

**追加推奨10個**（余裕があれば）:
11. `react`
12. `vue`
13. `python`
14. `typescript`
15. `skills-framework`
16. `automation`
17. `best-practices`
18. `subagents`
19. `phase-detection`
20. `mit-license`

### 2-4. 変更を保存

ページ下部の **「Save changes」** をクリック

✅ 完了！リポジトリの説明とトピックが設定されます

---

## ステップ3: GitHub Discussionsにウェルカム投稿

### 3-1. Discussionsページへ移動

1. https://github.com/SawanoLab/adaptive-claude-agents/discussions を開く
2. **「New discussion」** ボタンをクリック

### 3-2. カテゴリを選択

**Category**: **Announcements** を選択

### 3-3. 投稿内容を入力

**Title**:
```
👋 Welcome to Adaptive Claude Agents!
```

**Body**:
`docs/internal/DISCUSSIONS_WELCOME.md` の内容をコピー&ペースト

または、以下の簡潔版:

```markdown
# 👋 Welcome to the Adaptive Claude Agents community!

We're excited to have you here! This is the place to discuss all things related to Adaptive Claude Agents.

## 🚀 What is Adaptive Claude Agents?

Auto-generate specialized Claude Code subagents for your project and adapt code review rigor based on your development phase.

### Key Features

🔍 **Auto-Detection**: Detects 10 frameworks with 85% average confidence
🤖 **Auto-Generation**: Creates 13 specialized subagent templates (~228KB)
🎯 **Phase-Adaptive Review**: ⭐ **Industry First** - No other AI tool has this!

## 📚 Getting Started

- 📖 [Quick Start Guide](https://github.com/SawanoLab/adaptive-claude-agents/blob/main/docs/QUICKSTART.md) (5 minutes)
- 🎯 [Examples Gallery](https://github.com/SawanoLab/adaptive-claude-agents/blob/main/docs/EXAMPLES.md) (5 real-world examples)
- 🔧 [Troubleshooting](https://github.com/SawanoLab/adaptive-claude-agents/blob/main/docs/TROUBLESHOOTING.md)

## 💬 How to Participate

- **General**: Share your experience, ask questions
- **Q&A**: Get help with installation, detection, templates
- **Ideas**: Suggest new features or frameworks
- **Show and Tell**: Share your custom templates or use cases

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](https://github.com/SawanoLab/adaptive-claude-agents/blob/main/CONTRIBUTING.md) for:

- Adding new framework templates
- Improving detection accuracy
- Enhancing documentation
- Reporting bugs

## 📬 Resources

- 🐛 [Report Issues](https://github.com/SawanoLab/adaptive-claude-agents/issues)
- 💡 [Feature Requests](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=feature_request.md)
- 📝 [Template Requests](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=template_request.md)

## 🙏 Thank You!

Thank you for being part of this community. We're excited to see what you build with Adaptive Claude Agents!

⭐ **Star the repo** if you find it useful!

---

**Happy Coding!** 🚀

*Developed with ❤️ by SawanoLab, Aichi Institute of Technology*
```

### 3-4. 投稿

**「Start discussion」** ボタンをクリック

✅ 完了！ウェルカム投稿が公開されます

---

## ステップ4: 公開URLからインストールテスト

### 4-1. 新しいターミナルウィンドウを開く

別のディレクトリ（例: `/tmp`）で実行

### 4-2. インストールコマンドを実行

```bash
cd /tmp
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
```

### 4-3. 期待される出力

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Adaptive Claude Agents Installation
  Version: 0.4.0-beta
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ System check passed
✓ Claude Code skills directory found
✓ Installation complete!
```

### 4-4. 検証

```bash
ls -la "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/"
```

✅ 完了！公開URLからのインストールが動作確認できました

---

## ステップ5: アナウンス（オプション）

### 5-1. 研究室メール

`docs/internal/LAUNCH_ANNOUNCEMENT.md` の日本語版テンプレートを使用

### 5-2. Twitter/X（オプション）

日本語版:
```
🎉 Adaptive Claude Agents v0.4.0-beta をリリースしました！

✨ Claude Codeのサブエージェントを自動生成
🔍 10フレームワーク対応（Next.js、FastAPI等）
🎯 開発フェーズに応じてレビュー濃度を自動調整（業界初！）

5分でセットアップ完了🚀
https://github.com/SawanoLab/adaptive-claude-agents

#ClaudeCode #ClaudeAI #開発ツール
```

英語版:
```
🎉 Just released Adaptive Claude Agents v0.4.0-beta!

✨ Auto-generate specialized Claude Code subagents
🔍 Supports 10 frameworks (Next.js, FastAPI, etc.)
🎯 Phase-adaptive code review (industry first!)

Get started in 5 minutes 🚀
https://github.com/SawanoLab/adaptive-claude-agents

#ClaudeCode #ClaudeAI #DevTools
```

### 5-3. Reddit（オプション）

r/ClaudeAI に投稿（`LAUNCH_ANNOUNCEMENT.md`のRedditテンプレート使用）

---

## ✅ ローンチ完了チェックリスト

完了したらチェック：

- [ ] ステップ1: GitHub Release v0.4.0-beta作成
- [ ] ステップ2: リポジトリ設定更新（Description、Topics）
- [ ] ステップ3: Discussionsにウェルカム投稿
- [ ] ステップ4: 公開URLからインストールテスト成功
- [ ] ステップ5: アナウンス投稿（オプション）

---

## 🎊 おめでとうございます！

Public Beta Launch完了です！🚀

### 次のステップ

1. **Week 1の目標**:
   - 10-20人のベータユーザー
   - 3-5個のGitHubスター
   - 1-2件のコミュニティ貢献

2. **モニタリング**:
   - GitHub Issues（毎日チェック、最初の3日間）
   - Discussions（24-48時間以内に返信）
   - インストール状況の追跡

3. **フィードバック収集**:
   - v0.5.0に向けた改善点の収集
   - ユーザーからの要望の優先順位付け

---

**Happy Launching!** 🎉

*Generated: 2025-10-19*
