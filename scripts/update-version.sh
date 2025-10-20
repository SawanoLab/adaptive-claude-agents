#!/bin/bash
#
# Version Update Script
#
# This script updates the version number across all files in the project
# Usage: ./scripts/update-version.sh <new-version>
# Example: ./scripts/update-version.sh 0.5.0-beta
#

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get new version from argument
NEW_VERSION="$1"

if [ -z "$NEW_VERSION" ]; then
    echo -e "${RED}Error: Version number required${NC}"
    echo "Usage: $0 <new-version>"
    echo "Example: $0 0.5.0-beta"
    exit 1
fi

# Validate version format (semver with optional -beta/-alpha suffix)
if ! echo "$NEW_VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+(-beta|-alpha)?$'; then
    echo -e "${RED}Error: Invalid version format${NC}"
    echo "Expected: X.Y.Z or X.Y.Z-beta or X.Y.Z-alpha"
    echo "Got: $NEW_VERSION"
    exit 1
fi

# Get current version from VERSION file
CURRENT_VERSION=$(cat VERSION 2>/dev/null || echo "unknown")

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Version Update"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}Current version:${NC} $CURRENT_VERSION"
echo -e "${BLUE}New version:${NC}     $NEW_VERSION"
echo ""

# Confirm with user
read -p "Continue with version update? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Version update cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}Updating files...${NC}"

# Update VERSION file
echo "$NEW_VERSION" > VERSION
echo -e "  ${GREEN}✓${NC} VERSION"

# Update install.sh
sed -i.bak "s/VERSION=\".*\"/VERSION=\"$NEW_VERSION\"/" install.sh
rm -f install.sh.bak
echo -e "  ${GREEN}✓${NC} install.sh"

# Update README.md badge
sed -i.bak "s/version-[0-9.]*-*[a-z]*/version-${NEW_VERSION}/" README.md
rm -f README.md.bak
echo -e "  ${GREEN}✓${NC} README.md"

# Update README.ja.md badge
sed -i.bak "s/version-[0-9.]*-*[a-z]*/version-${NEW_VERSION}/" README.ja.md
rm -f README.ja.md.bak
echo -e "  ${GREEN}✓${NC} README.ja.md"

echo ""
echo -e "${GREEN}✓ Version updated successfully${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Review changes: git diff"
echo "  2. Update CHANGELOG.md manually"
echo "  3. Commit changes: git add -A && git commit -m \"chore: bump version to $NEW_VERSION\""
echo "  4. Create release: git tag v$NEW_VERSION && git push origin main --tags"
echo ""
