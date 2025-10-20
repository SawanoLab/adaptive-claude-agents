# Version Management Guide

This document describes how to manage version numbers consistently across the Adaptive Claude Agents project.

## Overview

**Single Source of Truth**: The `VERSION` file at the project root contains the authoritative version number.

**Current Version**: `0.4.1-beta`

## Version Format

We follow [Semantic Versioning](https://semver.org/) with pre-release tags:

```
MAJOR.MINOR.PATCH[-prerelease]
```

**Examples**:
- `0.4.1-beta` - Beta pre-release
- `0.5.0-alpha` - Alpha pre-release
- `1.0.0` - Stable release

**Incrementing Rules**:
- **MAJOR**: Breaking changes (e.g., 0.x.x → 1.0.0)
- **MINOR**: New features, backward compatible (e.g., 0.4.x → 0.5.0)
- **PATCH**: Bug fixes, backward compatible (e.g., 0.4.1 → 0.4.2)

**Pre-release Tags**:
- `-alpha`: Early development, unstable
- `-beta`: Feature complete, testing phase
- No suffix: Stable production release

## Files Containing Version Numbers

The version number appears in these files:

1. **`VERSION`** - Single source of truth (1 line)
2. **`install.sh`** - Installation script `VERSION="x.x.x-beta"`
3. **`README.md`** - Badge `![Version](https://img.shields.io/badge/version-x.x.x--beta-blue.svg)`
4. **`README.ja.md`** - Badge (same as README.md)
5. **`CHANGELOG.md`** - Version history (manual update required)

## Updating the Version

### Automated Method (Recommended)

Use the version update script:

```bash
# Update to new version
./scripts/update-version.sh 0.5.0-beta

# The script will:
# 1. Validate version format
# 2. Show current vs new version
# 3. Ask for confirmation
# 4. Update VERSION, install.sh, README.md, README.ja.md
# 5. Show next steps
```

**What the script updates**:
- ✅ `VERSION` file
- ✅ `install.sh` - `VERSION="..."`
- ✅ `README.md` - Version badge
- ✅ `README.ja.md` - Version badge

**What you need to update manually**:
- ⚠️ `CHANGELOG.md` - Add new version entry

### Manual Method (Not Recommended)

If you must update manually:

1. Update `VERSION` file:
   ```bash
   echo "0.5.0-beta" > VERSION
   ```

2. Update `install.sh` line 26:
   ```bash
   VERSION="0.5.0-beta"
   ```

3. Update `README.md` line 8 badge:
   ```markdown
   ![Version](https://img.shields.io/badge/version-0.5.0--beta-blue.svg)
   ```

4. Update `README.ja.md` line 8 badge (same as README.md)

5. Update `CHANGELOG.md` - Add new `[0.5.0-beta]` section

## Complete Version Update Workflow

### 1. Decide New Version Number

Based on changes:
- New features → Increment MINOR (e.g., 0.4.1 → 0.5.0)
- Bug fixes only → Increment PATCH (e.g., 0.4.1 → 0.4.2)
- Breaking changes → Increment MAJOR (e.g., 0.4.1 → 1.0.0)

### 2. Run Update Script

```bash
./scripts/update-version.sh 0.5.0-beta
```

Review and confirm the changes.

### 3. Update CHANGELOG.md

Add a new section at the top:

```markdown
## [0.5.0-beta] - 2025-10-27

### Added
- New feature X
- New feature Y

### Changed
- Improved Z

### Fixed
- Bug fix A
```

### 4. Review Changes

```bash
git status
git diff VERSION install.sh README.md README.ja.md CHANGELOG.md
```

### 5. Commit Changes

```bash
git add VERSION install.sh README.md README.ja.md CHANGELOG.md scripts/
git commit -m "chore: bump version to 0.5.0-beta"
```

### 6. Create Git Tag

```bash
git tag v0.5.0-beta
```

### 7. Push to GitHub

```bash
git push origin main --tags
```

### 8. Create GitHub Release

1. Go to https://github.com/SawanoLab/adaptive-claude-agents/releases
2. Click "Draft a new release"
3. Select tag: `v0.5.0-beta`
4. Title: `v0.5.0-beta - [Brief Description]`
5. Copy content from `CHANGELOG.md` for this version
6. Check "This is a pre-release" (for beta/alpha)
7. Click "Publish release"

### 9. Test Installation

```bash
# Test from GitHub URL
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash

# Verify version
cat ~/Library/Application\ Support/Claude/skills/adaptive-claude-agents/VERSION
```

## Version History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 0.4.1-beta | 2025-10-20 | Current | Go & Flutter support |
| 0.4.0-beta | 2025-10-26 | Released | Public beta launch |
| 0.3.0-alpha | 2025-10-19 | Released | Week 2 testing |
| 0.2.0-alpha | 2025-10-12 | Released | Phase detection |
| 0.1.0-alpha | 2025-10-05 | Released | Initial framework detection |

## Troubleshooting

### Script shows "command not found"

```bash
chmod +x scripts/update-version.sh
```

### Version badge not updating

The badge URL uses `--` (double dash) for hyphens in version:
- Correct: `version-0.5.0--beta-blue.svg`
- Wrong: `version-0.5.0-beta-blue.svg`

The script handles this automatically.

### Git push fails

```bash
# Check remote
git remote -v

# Force push if needed (use with caution)
git push origin main --force
```

## Best Practices

1. **Always use the script** - Reduces human error
2. **Update CHANGELOG.md first** - Document changes before versioning
3. **Test locally** - Run `./install.sh` before pushing
4. **Create meaningful tags** - Use `v` prefix (e.g., `v0.5.0-beta`)
5. **Write good release notes** - Help users understand what changed
6. **Follow semver** - Makes version changes predictable
7. **Pre-release for testing** - Use `-beta` or `-alpha` until stable

## References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Keep a Changelog](https://keepachangelog.com/)
