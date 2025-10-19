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
    echo "Adaptive Claude Agents has been updated to the latest version."
    echo ""
    echo "Changes: https://github.com/SawanoLab/adaptive-claude-agents/releases"
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
    print_success
}

main
