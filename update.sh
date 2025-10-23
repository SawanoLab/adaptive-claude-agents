#!/bin/bash
#
# Adaptive Claude Agents - Update Script
#
# This script updates Adaptive Claude Agents to the latest version
#
# Usage:
#   ./update.sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

REPO_URL="https://github.com/SawanoLab/adaptive-claude-agents.git"
SKILL_NAME="adaptive-claude-agents"

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Darwin*)    OS="macos";;
        Linux*)     OS="linux";;
        MINGW*|MSYS*|CYGWIN*) OS="windows";;
        *)          OS="unknown";;
    esac
}

# Detect Skills directory
detect_skills_dir() {
    if [ -n "$CLAUDE_SKILLS_DIR" ]; then
        SKILLS_DIR="$CLAUDE_SKILLS_DIR"
    elif [ "$OS" = "macos" ]; then
        SKILLS_DIR="$HOME/Library/Application Support/Claude/skills"
    elif [ "$OS" = "linux" ]; then
        SKILLS_DIR="$HOME/.config/claude/skills"
    elif [ "$OS" = "windows" ]; then
        SKILLS_DIR="$APPDATA/Claude/skills"
    else
        echo -e "${RED}✗ Could not detect Claude Code skills directory${NC}"
        exit 1
    fi
}

# Print header
print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Adaptive Claude Agents Update"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check if installed
check_installation() {
    INSTALL_DIR="$SKILLS_DIR/$SKILL_NAME"

    if [ ! -d "$INSTALL_DIR" ]; then
        echo -e "${RED}✗ Adaptive Claude Agents is not installed${NC}"
        echo -e "${BLUE}Install it first with:${NC}"
        echo -e "  curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash"
        exit 1
    fi
}

# Backup current installation
backup_installation() {
    echo -e "${BLUE}Creating backup...${NC}"

    INSTALL_DIR="$SKILLS_DIR/$SKILL_NAME"
    BACKUP_DIR="$SKILLS_DIR/${SKILL_NAME}.backup"

    if [ -d "$BACKUP_DIR" ]; then
        rm -rf "$BACKUP_DIR"
    fi

    cp -r "$INSTALL_DIR" "$BACKUP_DIR"
    echo -e "  ${GREEN}✓${NC} Backup created: $BACKUP_DIR"
    echo ""
}

# Update installation
update() {
    echo -e "${BLUE}Updating Adaptive Claude Agents...${NC}"

    INSTALL_DIR="$SKILLS_DIR/$SKILL_NAME"
    TEMP_DIR="/tmp/$SKILL_NAME-$(date +%s)"

    # Clone latest version to temp directory
    echo -e "  ${BLUE}→${NC} Downloading latest version..."
    if git clone --quiet "$REPO_URL" "$TEMP_DIR" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Latest version downloaded"
    else
        echo -e "  ${RED}✗${NC} Failed to download update"
        echo -e "    ${YELLOW}Restoring from backup...${NC}"
        rm -rf "$INSTALL_DIR"
        mv "$SKILLS_DIR/${SKILL_NAME}.backup" "$INSTALL_DIR"
        exit 1
    fi

    # Remove .git to save space
    rm -rf "$TEMP_DIR/.git"

    # Replace old installation
    echo -e "  ${BLUE}→${NC} Installing update..."
    rm -rf "$INSTALL_DIR"
    mv "$TEMP_DIR" "$INSTALL_DIR"

    echo -e "  ${GREEN}✓${NC} Update installed"
    echo ""

    # Clean up backup
    rm -rf "$SKILLS_DIR/${SKILL_NAME}.backup"
}

# Configure AGGRESSIVE subagent policy
configure_subagent_policy() {
    echo -e "${BLUE}Configuring AGGRESSIVE subagent policy...${NC}"

    # Check if user's project has CLAUDE.md
    if [ -f "CLAUDE.md" ]; then
        # Check if policy already exists
        if grep -q "AGGRESSIVE ポリシー" CLAUDE.md 2>/dev/null; then
            echo -e "  ${YELLOW}⚠${NC} Subagent policy already configured"
        else
            # Append AGGRESSIVE policy to user's CLAUDE.md
            cat >> CLAUDE.md <<'EOF'

## 🤖 Adaptive Claude Agents - AGGRESSIVE ポリシー

**このプロジェクトにAdaptive Claude Agentsをインストール = サブエージェントを積極的に使いたい**

### 必須ルール（MANDATORY）

以下の条件に該当する場合、**必ずTaskツールでサブエージェントを使用してください:**

1. **3+ ファイルの類似修正**
   - 例: "file1.js, file2.js, file3.js に同じパターン適用"
   - サブエージェント: `general-purpose`
   - 節約時間: 30-60分

2. **コードベース全体の探索**
   - 例: "関数Xはどこで使われているか"
   - サブエージェント: `Explore` (thoroughness: "very thorough")
   - 節約時間: 60-90分

3. **E2Eテスト実行**
   - 例: "ログイン → API呼び出し → DB検証をテスト"
   - サブエージェント: `general-purpose` + framework tester
   - 節約時間: 45分以上

4. **並行可能な独立タスク（2つ以上）**
   - 例: ".gitignore更新 + UIコンポーネントのリファクタリング"
   - サブエージェント: 複数の `general-purpose` を単一メッセージで
   - 節約時間: 30分以上

### コスト vs 時間のトレードオフ

| タスクタイプ | 直接実行 | サブエージェント | 時間節約 | **推奨** |
|------------|---------|----------------|---------|---------|
| 単一ファイル | 5k | 25k | 0分 | ❌ 直接 |
| 3-4ファイル | 15k | 35k | 30分 | ✅ サブエージェント |
| 5+ファイル | 30k | 50k | 60分 | ✅✅ サブエージェント |
| コードベース検索 | 40k | 60k | 90分 | ✅✅✅ Explore |

**原則**: 20kトークンのオーバーヘッドは30分以上の節約で正当化される

### 目標メトリクス

- **サブエージェント使用率**: 複雑なタスクの20-30%
- **週あたり節約時間**: 2-4時間
- **トークン効率**: 30分以上の節約で20kオーバーヘッドを許容

詳細: https://github.com/SawanoLab/adaptive-claude-agents
EOF
            echo -e "  ${GREEN}✓${NC} Subagent policy added to CLAUDE.md"
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} No CLAUDE.md found in current directory"
        echo -e "      ${YELLOW}Run in your project directory to enable AGGRESSIVE policy${NC}"
    fi

    echo ""
}

# Validate update
validate_update() {
    echo -e "${BLUE}Validating update...${NC}"

    INSTALL_DIR="$SKILLS_DIR/$SKILL_NAME"

    if [ -f "$INSTALL_DIR/skills/project-analyzer/detect_stack.py" ] && \
       [ -f "$INSTALL_DIR/skills/adaptive-review/detect_phase.py" ]; then
        echo -e "  ${GREEN}✓${NC} Update successful"
    else
        echo -e "  ${RED}✗${NC} Update validation failed"
        exit 1
    fi

    echo ""
}

# Print success
print_success() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "  ${GREEN}✓ Update Complete!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${BLUE}🎯 AGGRESSIVE Mode Enabled${NC}"
    echo ""
    echo "  New features:"
    echo "  • Auto-generated SUBAGENT_GUIDE.md (framework-specific)"
    echo "  • Proactive subagent usage for 3+ file tasks"
    echo "  • Cost-benefit analysis for efficient delegation"
    echo "  • Target: 20-30% subagent usage, 2-4 hours saved/week"
    echo ""
    echo -e "${BLUE}What's New:${NC}"
    echo "  https://github.com/SawanoLab/adaptive-claude-agents/releases"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "  1. Navigate to your project directory"
    echo "  2. Run: python3 \"\$SKILLS_DIR/$SKILL_NAME/skills/project-analyzer/analyze_project.py\" ."
    echo "  3. Review: .claude/agents/SUBAGENT_GUIDE.md"
    echo "  4. Code naturally - subagents auto-trigger on keywords!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Main
main() {
    print_header
    detect_os
    detect_skills_dir
    check_installation
    backup_installation
    update
    validate_update
    configure_subagent_policy
    print_success
}

main
