# トラブルシューティングガイド

このガイドでは、Adaptive Claude Agentsの一般的な問題と解決方法を説明します。

## 目次

- [インストールに関する問題](#インストールに関する問題)
- [検出に関する問題](#検出に関する問題)
- [フェーズ検出に関する問題](#フェーズ検出に関する問題)
- [テンプレート生成に関する問題](#テンプレート生成に関する問題)
- [プラットフォーム固有の問題](#プラットフォーム固有の問題)
- [パフォーマンスに関する問題](#パフォーマンスに関する問題)
- [サポートを受ける](#サポートを受ける)

## インストールに関する問題

### 問題: "command not found: claude-code-skill"

**症状**: インストール後に `claude-code-skill` コマンドが見つからない

**原因**: スクリプトのインストールパスがPATHに含まれていない可能性があります

**解決方法**:

1. インストールスクリプトが正しくコピーされたか確認:
   ```bash
   ls -la ~/.local/bin/claude-code-skill
   ```

2. `~/.local/bin` がPATHに含まれているか確認:
   ```bash
   echo $PATH | grep ".local/bin"
   ```

3. PATHに含まれていない場合、シェル設定ファイルに追加:
   ```bash
   # For bash (~/.bashrc)
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc

   # For zsh (~/.zshrc)
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

4. インストールスクリプトを再実行:
   ```bash
   ./install.sh
   ```

### 問題: 権限が拒否されました

**症状**: インストール中に "Permission denied" エラー

**原因**: インストールスクリプトまたは対象ディレクトリに実行権限がありません

**解決方法**:

```bash
# インストールスクリプトに実行権限を付与
chmod +x install.sh

# ~/.local/bin ディレクトリが存在することを確認
mkdir -p ~/.local/bin

# 再度インストールを実行
./install.sh
```

### 問題: Python依存関係エラー

**症状**: "No module named 'yaml'" または類似のエラー

**原因**: 必要なPythonパッケージがインストールされていません

**解決方法**:

```bash
# PyYAMLをインストール
pip install PyYAML

# または、requirements.txtを使用
pip install -r requirements.txt
```

## 検出に関する問題

### 問題: プロジェクトの種類が検出されない

**症状**: アナライザーが "Unknown" プロジェクトタイプを報告する

**診断**:

```bash
# プロジェクトルートにいることを確認
pwd

# 主要なプロジェクトファイルを確認
ls -la package.json pyproject.toml Cargo.toml pom.xml
```

**一般的な原因と解決方法**:

#### Next.js プロジェクト

```bash
# package.jsonが存在するか確認
cat package.json | grep -E '"next":|"@types/react"'

# なければ、プロジェクトルートに移動
cd /path/to/your/nextjs/project
```

#### FastAPI プロジェクト

```bash
# pyproject.tomlまたはrequirements.txtを確認
cat pyproject.toml | grep fastapi
# または
cat requirements.txt | grep fastapi

# Pythonファイルでfasttapi importを確認
grep -r "from fastapi import" .
```

#### React プロジェクト

```bash
# package.jsonにreactがあるか確認
cat package.json | grep '"react":'

# Next.jsと誤検出されないよう確認
cat package.json | grep '"next":' && echo "This is Next.js, not plain React"
```

### 問題: 間違ったスタックが検出される

**症状**: アナライザーが誤ったフレームワークを識別する

**手動オーバーライド**:

`.claude-project.yaml` でスタック検出をオーバーライドできます:

```yaml
stack_override:
  - nextjs
  - typescript

# または
stack_override:
  - fastapi
  - python
```

**検出ロジックの確認**:

```bash
# プロジェクトアナライザーを詳細モードで実行
python3 skills/project_analyzer.py --verbose
```

### 問題: TypeScript/型チェックが検出されない

**症状**: TypeScriptプロジェクトなのに型チェック関連のサブエージェントが生成されない

**解決方法**:

```bash
# tsconfig.jsonが存在するか確認
ls tsconfig.json

# package.jsonでTypeScript依存関係を確認
cat package.json | grep -E '"typescript"|"@types/'

# ない場合はTypeScriptを追加
npm install --save-dev typescript @types/node
npx tsc --init
```

## フェーズ検出に関する問題

### 問題: 間違った開発フェーズが検出される

**症状**: フェーズ検出がプロジェクトの実際の状態と一致しない

**フェーズ指標を理解する**:

```yaml
# .claude-project.yaml
phase:
  current: mvp  # prototype, mvp, pre-production

  # フェーズ検出は以下を分析します:
  # - Gitコミット数
  # - テストカバレッジ
  # - CI/CD設定
  # - 依存関係の成熟度
```

**手動オーバーライド**:

```yaml
# .claude-project.yaml
phase:
  current: pre-production
  override: true  # 自動検出を無効化
```

**検出ロジックの確認**:

```bash
# フェーズ検出の詳細を表示
python3 -c "
from skills.phase_detector import detect_phase
import json
print(json.dumps(detect_phase('.'), indent=2))
"
```

### 問題: フェーズが自動的に更新されない

**症状**: プロジェクトが進化してもフェーズが変わらない

**解決方法**:

```bash
# .claude-project.yamlを削除して再検出
rm .claude-project.yaml
claude-code-skill analyze

# またはフェーズキャッシュを手動でクリア
python3 -c "
import yaml
with open('.claude-project.yaml', 'r') as f:
    config = yaml.safe_load(f)
config['phase']['last_checked'] = None
with open('.claude-project.yaml', 'w') as f:
    yaml.dump(config, f)
"
```

## テンプレート生成に関する問題

### 問題: サブエージェントが生成されない

**症状**: アナライザーは正常に動作するが、サブエージェントファイルが作成されない

**診断**:

```bash
# 書き込み権限を確認
ls -ld .claude/
ls -la .claude/

# .claude/ ディレクトリを手動で作成
mkdir -p .claude

# 再度生成を実行
claude-code-skill generate
```

### 問題: テンプレート変数が展開されない

**症状**: 生成されたサブエージェントに `{{PROJECT_NAME}}` のような未処理の変数が含まれる

**テンプレート変数を確認**:

```bash
# 利用可能な変数を表示
python3 -c "
from skills.template_engine import get_template_vars
import json
print(json.dumps(get_template_vars('.'), indent=2))
"
```

**一般的な変数**:

- `{{PROJECT_NAME}}` - package.jsonまたはpyproject.tomlから
- `{{TECH_STACK}}` - 検出されたフレームワーク
- `{{PHASE}}` - 現在の開発フェーズ
- `{{LANGUAGE}}` - 主要なプログラミング言語

**手動で変数を設定**:

```yaml
# .claude-project.yaml
template_vars:
  PROJECT_NAME: "my-awesome-app"
  CUSTOM_VAR: "custom-value"
```

### 問題: カスタムテンプレートが認識されない

**症状**: ローカルテンプレートが使用されない

**解決方法**:

```bash
# テンプレート構造を確認
ls -R templates/

# 正しい構造:
# templates/
#   nextjs/
#     code-reviewer.md
#     tester.md
#     architecture-guide.md
#   fastapi/
#     api-reviewer.md
#     ...

# カスタムテンプレートディレクトリを指定
claude-code-skill generate --template-dir ./my-templates
```

## プラットフォーム固有の問題

### macOS

#### 問題: "xcrun: error" または Xcode関連エラー

**解決方法**:

```bash
# Command Line Toolsをインストール
xcode-select --install

# またはフルXcodeをインストール
# App StoreからXcodeをインストール
```

#### 問題: Python3が見つからない

**解決方法**:

```bash
# Homebrewを使用してPythonをインストール
brew install python3

# またはpython.orgから公式インストーラーを使用
```

### Linux

#### 問題: Python.hが見つからない

**症状**: Python開発ヘッダーがない

**解決方法**:

```bash
# Debian/Ubuntu
sudo apt-get install python3-dev

# Fedora/RHEL
sudo dnf install python3-devel

# Arch
sudo pacman -S python
```

### Windows (WSL)

#### 問題: 行末の問題

**症状**: スクリプトが "bad interpreter" エラーで失敗する

**解決方法**:

```bash
# dos2unixをインストール
sudo apt-get install dos2unix

# スクリプトを変換
dos2unix install.sh
dos2unix skills/*.py
```

#### 問題: パス区切り文字の問題

**解決方法**:

WSL内でLinuxスタイルのパス (`/home/user/...`) を使用し、Windowsパス (`C:\Users\...`) は使用しないでください。

## パフォーマンスに関する問題

### 問題: 大規模プロジェクトで分析が遅い

**症状**: 数千のファイルがあるプロジェクトで検出に長時間かかる

**最適化**:

```yaml
# .claude-project.yaml
analysis:
  exclude_patterns:
    - "node_modules/**"
    - "venv/**"
    - ".git/**"
    - "build/**"
    - "dist/**"
    - "*.min.js"

  max_files: 1000  # スキャンする最大ファイル数
```

### 問題: メモリ使用量が多い

**解決方法**:

```yaml
# .claude-project.yaml
analysis:
  cache_enabled: true
  incremental: true  # 変更されたファイルのみを分析
```

## サポートを受ける

### 問題を報告する前に

1. **最新バージョンか確認**:
   ```bash
   cd /path/to/adaptive-claude-agents
   git pull origin main
   ./install.sh
   ```

2. **詳細ログを収集**:
   ```bash
   claude-code-skill analyze --verbose > debug.log 2>&1
   ```

3. **環境情報を収集**:
   ```bash
   # システム情報
   uname -a
   python3 --version

   # プロジェクト構造
   tree -L 2 -a .

   # 設定
   cat .claude-project.yaml
   ```

### Issueを作成

問題が解決しない場合は、GitHubでissueを作成してください:

https://github.com/yourusername/adaptive-claude-agents/issues

**以下を含めてください**:

1. **問題の明確な説明**
   - 何を実行しようとしましたか？
   - 何が期待されましたか？
   - 実際に何が起こりましたか？

2. **再現手順**
   ```
   1. コマンドXを実行
   2. 'Y'を選択
   3. エラーが表示される
   ```

3. **環境**
   - OS: macOS 13.1 / Ubuntu 22.04 / Windows 11 (WSL)
   - Python version: 3.11.2
   - Project type: Next.js / FastAPI / etc.

4. **ログとエラーメッセージ**
   ```
   完全なエラーメッセージをここに貼り付け
   ```

5. **設定ファイル**
   ```yaml
   .claude-project.yamlの内容
   ```

### コミュニティサポート

- **Discussions**: 質問や使用例の共有に使用
- **Discord**: (利用可能な場合) リアルタイムサポート
- **ドキュメント**: 常に最初にドキュメントを確認

### よくある質問（FAQ）

#### Q: このツールは既存の.claude設定を上書きしますか？

A: いいえ。既存のサブエージェントの上書き前に常に確認を求めます。

#### Q: 複数のプロジェクトタイプ（例：Next.js + FastAPI）で使用できますか？

A: はい！`.claude-project.yaml`で `stack_override` に複数のスタックを指定できます。

#### Q: 開発中に検出ロジックをテストするには？

A: テストモードを使用:
```bash
claude-code-skill analyze --dry-run
```

#### Q: テンプレートをチーム全体で共有できますか？

A: はい。テンプレートをバージョン管理し、チームメンバーは同じテンプレートディレクトリを使用できます。

---

**フィードバック**: このドキュメントに問題がありますか？[Issueを開く](https://github.com/yourusername/adaptive-claude-agents/issues)
