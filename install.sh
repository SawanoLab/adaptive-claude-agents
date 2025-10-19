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
VERSION="1.0.0-beta"

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

    # Test detection script
    if python3 "$INSTALL_DIR/skills/project-analyzer/detect_stack.py" --help >/dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} Detection script works"
    else
        echo -e "  ${YELLOW}⚠${NC} Detection script test failed (may need dependencies)"
    fi

    if [ $has_error -eq 1 ]; then
        echo ""
        echo -e "${RED}✗ Installation validation failed${NC}"
        exit 1
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
    echo -e "${BLUE}Next Steps:${NC}"
    echo ""
    echo "  1. Open any project in Claude Code"
    echo "  2. Skills will auto-detect your tech stack"
    echo "  3. Try: \"Analyze my project and generate subagents\""
    echo ""
    echo -e "${BLUE}Usage Examples:${NC}"
    echo ""
    echo "  • \"What development phase am I in?\""
    echo "  • \"Generate appropriate subagents for this project\""
    echo "  • \"Run project analysis\""
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

    print_success
}

# Run main function
main
