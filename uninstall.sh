#!/bin/bash
#
# Adaptive Claude Agents - Uninstall Script
#
# This script removes Adaptive Claude Agents from Claude Code Skills
#
# Usage:
#   ./uninstall.sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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
    echo "  Adaptive Claude Agents Uninstallation"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Confirm uninstallation
confirm_uninstall() {
    echo -e "${YELLOW}Are you sure you want to uninstall Adaptive Claude Agents?${NC}"
    echo -e "${YELLOW}This will remove all skills and templates.${NC}"
    echo ""
    read -p "Continue? (y/N): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Uninstallation cancelled${NC}"
        exit 0
    fi
    echo ""
}

# Remove installation
uninstall() {
    INSTALL_DIR="$SKILLS_DIR/$SKILL_NAME"

    if [ ! -d "$INSTALL_DIR" ]; then
        echo -e "${YELLOW}⚠ Adaptive Claude Agents is not installed${NC}"
        echo -e "${BLUE}Install directory not found: $INSTALL_DIR${NC}"
        exit 0
    fi

    echo -e "${BLUE}Removing Adaptive Claude Agents...${NC}"

    rm -rf "$INSTALL_DIR"

    echo -e "  ${GREEN}✓${NC} Removed: $INSTALL_DIR"
    echo ""
}

# Print success
print_success() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "  ${GREEN}✓ Uninstallation Complete${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Adaptive Claude Agents has been removed."
    echo ""
    echo "Thank you for trying it out!"
    echo ""
    echo "Feedback: https://github.com/SawanoLab/adaptive-claude-agents/issues"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Main
main() {
    print_header
    detect_os
    detect_skills_dir
    confirm_uninstall
    uninstall
    print_success
}

main
