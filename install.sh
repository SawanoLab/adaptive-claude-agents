#!/bin/bash
#
# Adaptive Claude Agents - Installation Script
#
# This script installs Adaptive Claude Agents as a global Claude Code Skill
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
#
# Or locally:
#   ./install.sh
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/SawanoLab/adaptive-claude-agents.git"
SKILL_NAME="adaptive-claude-agents"
VERSION="0.4.2-beta"

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Darwin*)    OS="macos";;
        Linux*)     OS="linux";;
        MINGW*|MSYS*|CYGWIN*) OS="windows";;
        *)          OS="unknown";;
    esac
}

# Detect Claude Code Skills directory
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
        echo -e "${YELLOW}  Please set CLAUDE_SKILLS_DIR environment variable${NC}"
        exit 1
    fi
}

# Print header
print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Adaptive Claude Agents Installation"
    echo "  Version: $VERSION"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check system requirements
check_requirements() {
    echo -e "${BLUE}Checking system requirements...${NC}"

    local has_error=0

    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
        PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

        if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
            echo -e "  ${GREEN}✓${NC} Python: $PYTHON_VERSION"
        else
            echo -e "  ${RED}✗${NC} Python: $PYTHON_VERSION (requires 3.9+)"
            has_error=1
        fi
    else
        echo -e "  ${RED}✗${NC} Python 3 not found"
        echo -e "    ${YELLOW}Install from: https://www.python.org/downloads/${NC}"
        has_error=1
    fi

    # Check Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        echo -e "  ${GREEN}✓${NC} Git: $GIT_VERSION"
    else
        echo -e "  ${RED}✗${NC} Git not found"
        echo -e "    ${YELLOW}Install from: https://git-scm.com/${NC}"
        has_error=1
    fi

    # Check OS
    echo -e "  ${GREEN}✓${NC} OS: $OS"

    if [ $has_error -eq 1 ]; then
        echo ""
        echo -e "${RED}✗ System requirements not met${NC}"
        echo -e "${YELLOW}  Please install missing dependencies and try again${NC}"
        exit 1
    fi

    echo ""
}

# Check Python dependencies
check_python_deps() {
    echo -e "${BLUE}Checking Python dependencies...${NC}"

    if python3 -c "import yaml" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} pyyaml installed"
    else
        echo -e "  ${YELLOW}⚠${NC} pyyaml not found, installing..."

        if python3 -m pip install --user pyyaml >/dev/null 2>&1; then
            echo -e "  ${GREEN}✓${NC} pyyaml installed successfully"
        else
            echo -e "  ${RED}✗${NC} Failed to install pyyaml"
            echo -e "    ${YELLOW}Please run: python3 -m pip install pyyaml${NC}"
            exit 1
        fi
    fi

    echo ""
}

# Detect or create skills directory
setup_skills_dir() {
    echo -e "${BLUE}Setting up Claude Code skills directory...${NC}"

    if [ -d "$SKILLS_DIR" ]; then
        echo -e "  ${GREEN}✓${NC} Skills directory found: $SKILLS_DIR"
    else
        echo -e "  ${YELLOW}⚠${NC} Skills directory not found, creating..."
        mkdir -p "$SKILLS_DIR"
        echo -e "  ${GREEN}✓${NC} Created: $SKILLS_DIR"
    fi

    echo ""
}

# Clone or update repository
install_skill() {
    echo -e "${BLUE}Installing Adaptive Claude Agents...${NC}"

    INSTALL_DIR="$SKILLS_DIR/$SKILL_NAME"

    # Remove old installation if exists
    if [ -d "$INSTALL_DIR" ]; then
        echo -e "  ${YELLOW}⚠${NC} Existing installation found, removing..."
        rm -rf "$INSTALL_DIR"
    fi

    # Clone repository
    echo -e "  ${BLUE}→${NC} Cloning repository..."
    if git clone --quiet "$REPO_URL" "$INSTALL_DIR" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Repository cloned"
    else
        echo -e "  ${RED}✗${NC} Failed to clone repository"
        echo -e "    ${YELLOW}Please check your internet connection${NC}"
        exit 1
    fi

    # Remove .git directory to save space
    rm -rf "$INSTALL_DIR/.git"

    echo -e "  ${GREEN}✓${NC} Installed to: $INSTALL_DIR"
    echo ""
}

# Validate installation
validate_installation() {
    echo -e "${BLUE}Validating installation...${NC}"

    INSTALL_DIR="$SKILLS_DIR/$SKILL_NAME"

    # Check key files
    local has_error=0

    if [ -f "$INSTALL_DIR/skills/project-analyzer/detect_stack.py" ]; then
        echo -e "  ${GREEN}✓${NC} Project analyzer found"
    else
        echo -e "  ${RED}✗${NC} Project analyzer missing"
        has_error=1
    fi

    if [ -f "$INSTALL_DIR/skills/adaptive-review/detect_phase.py" ]; then
        echo -e "  ${GREEN}✓${NC} Adaptive review found"
    else
        echo -e "  ${RED}✗${NC} Adaptive review missing"
        has_error=1
    fi

    if [ -d "$INSTALL_DIR/templates" ]; then
        TEMPLATE_COUNT=$(find "$INSTALL_DIR/templates" -name "*.md" | wc -l | tr -d ' ')
        echo -e "  ${GREEN}✓${NC} Templates found: $TEMPLATE_COUNT"
    else
        echo -e "  ${RED}✗${NC} Templates directory missing"
        has_error=1
    fi

    # Test detection script (basic validation only)
    if python3 "$INSTALL_DIR/skills/project-analyzer/detect_stack.py" --help >/dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} Detection script validated"
    else
        echo -e "  ${YELLOW}⚠${NC} Detection script validation skipped"
        echo -e "      ${YELLOW}(Run on actual project to test detection)${NC}"
    fi

    if [ $has_error -eq 1 ]; then
        echo ""
        echo -e "${RED}✗ Installation validation failed${NC}"
        exit 1
    fi

    echo ""
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
        echo -e "      ${YELLOW}To enable AGGRESSIVE policy, create CLAUDE.md in your project${NC}"
        echo -e "      ${YELLOW}Or run: python3 \"\$SKILLS_DIR/$SKILL_NAME/skills/project-analyzer/analyze_project.py\" .${NC}"
    fi

    echo ""
}

# Print success message
print_success() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "  ${GREEN}✓ Installation Complete!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${BLUE}🎯 AGGRESSIVE Mode Enabled${NC}"
    echo ""
    echo "  Adaptive Claude Agents will proactively use subagents for:"
    echo "  • 3+ file modifications (auto-delegate to general-purpose)"
    echo "  • Codebase searches (auto-delegate to Explore agent)"
    echo "  • E2E testing workflows (auto-chain multiple agents)"
    echo "  • Parallel independent tasks (concurrent execution)"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo ""
    echo "  1. Navigate to your project directory"
    echo "  2. Run: python3 \"\$SKILLS_DIR/$SKILL_NAME/skills/project-analyzer/analyze_project.py\" ."
    echo "  3. Review generated .claude/agents/SUBAGENT_GUIDE.md"
    echo "  4. Start coding - subagents will auto-trigger!"
    echo ""
    echo -e "${BLUE}Quick Commands:${NC}"
    echo ""
    echo "  • \"Analyze my project and generate subagents\""
    echo "  • \"What development phase am I in?\""
    echo "  • \"Show me subagent usage examples\""
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  https://github.com/SawanoLab/adaptive-claude-agents"
    echo ""
    echo -e "${BLUE}Issues & Support:${NC}"
    echo "  https://github.com/SawanoLab/adaptive-claude-agents/issues"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Main installation flow
main() {
    print_header

    detect_os
    detect_skills_dir

    check_requirements
    check_python_deps
    setup_skills_dir
    install_skill
    validate_installation
    configure_subagent_policy

    print_success
}

# Run main function
main
