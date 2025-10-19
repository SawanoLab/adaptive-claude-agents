# Troubleshooting Guide

Solutions to common issues with Adaptive Claude Agents.

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Detection Issues](#detection-issues)
3. [Phase Detection Issues](#phase-detection-issues)
4. [Template Generation Issues](#template-generation-issues)
5. [Platform-Specific Issues](#platform-specific-issues)
6. [Performance Issues](#performance-issues)
7. [Getting Help](#getting-help)

---

## Installation Issues

### Issue: "Claude Code skills directory not found"

**Symptoms**:
```
✗ Could not detect Claude Code skills directory
Please set CLAUDE_SKILLS_DIR environment variable
```

**Cause**: Installation script couldn't auto-detect your Claude Code installation

**Solution 1** (Recommended): Set environment variable

```bash
# macOS
export CLAUDE_SKILLS_DIR="$HOME/Library/Application Support/Claude/skills"

# Linux
export CLAUDE_SKILLS_DIR="$HOME/.config/claude/skills"

# Windows WSL
export CLAUDE_SKILLS_DIR="/mnt/c/Users/YourName/AppData/Roaming/Claude/skills"

# Run install again
./install.sh
```

**Solution 2**: Manual installation

```bash
# 1. Find your skills directory
# macOS: ~/Library/Application Support/Claude/skills
# Linux: ~/.config/claude/skills
# Windows: %APPDATA%\Claude\skills

# 2. Clone manually
cd "/path/to/skills/directory"
git clone https://github.com/SawanoLab/adaptive-claude-agents.git
rm -rf adaptive-claude-agents/.git  # Save space
```

**Verification**:
```bash
ls "$CLAUDE_SKILLS_DIR/adaptive-claude-agents/skills"
# Should show: adaptive-review, project-analyzer
```

---

### Issue: "Python 3.9+ required"

**Symptoms**:
```
✗ Python 3.9 or higher is required
Current version: Python 3.7.10
```

**Cause**: Your Python version is too old

**Solution 1**: Install Python 3.9+ from [python.org](https://www.python.org/downloads/)

**Solution 2**: Use pyenv (macOS/Linux)

```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python 3.11
pyenv install 3.11.7
pyenv global 3.11.7

# Verify
python3 --version  # Should show 3.11.7
```

**Solution 3**: Use Homebrew (macOS)

```bash
brew install python@3.11
```

---

### Issue: "git command not found"

**Symptoms**:
```
✗ git is not installed
```

**Cause**: Git is not installed on your system

**Solution**:

**macOS**:
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Or use Homebrew
brew install git
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install git
```

**Linux (Fedora/RHEL)**:
```bash
sudo dnf install git
```

**Windows**:
Download from [git-scm.com](https://git-scm.com/download/win)

---

### Issue: "pyyaml installation failed"

**Symptoms**:
```
✗ Failed to install pyyaml dependency
```

**Cause**: pip installation issues or permissions

**Solution 1**: Install with user flag

```bash
pip3 install --user pyyaml
```

**Solution 2**: Use virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows
pip install pyyaml
```

**Solution 3**: Check pip

```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Try again
pip3 install pyyaml
```

---

## Detection Issues

### Issue: "Could not detect tech stack"

**Symptoms**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Could not detect tech stack with confidence >50%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please ensure:
- Project has package.json, requirements.txt, or similar
- Project is in a supported framework
```

**Cause**: Project structure doesn't match supported frameworks, or confidence is too low

**Solution 1**: Manual override with `.claude/project.yml`

```bash
# Create .claude directory
mkdir -p .claude

# Create project.yml
cat > .claude/project.yml << 'EOF'
framework: nextjs  # or fastapi, vanilla-php-web, etc.
version: "14.0.0"
language: typescript
EOF
```

**Supported framework values**:
- `nextjs`, `react`, `vue`
- `fastapi`, `django`, `flask`
- `vanilla-php-web`
- `python-ml`, `python-cv`
- `ios-swift`
- `go`, `flutter`

**Solution 2**: Check project structure

```bash
# For Next.js
ls package.json  # Should exist
grep "next" package.json  # Should contain "next" dependency

# For FastAPI
ls requirements.txt  # Should exist
grep -i "fastapi" requirements.txt  # Should contain fastapi

# For vanilla PHP
ls composer.json  # Should exist
ls *.php  # Should have root PHP files
```

**Solution 3**: Increase verbosity to see detection details

```bash
python3 skills/project-analyzer/detect_stack.py . --verbose
```

---

### Issue: "Wrong framework detected"

**Symptoms**:
```
Detected: React
Expected: Next.js
```

**Cause**: Project has both React and Next.js dependencies, detector chose wrong one

**Solution**: Use manual override (`.claude/project.yml` above)

**Verification**:
```bash
# Run detection again
python3 skills/project-analyzer/detect_stack.py .

# Should now show your specified framework
```

---

### Issue: "Confidence too low (< 50%)"

**Symptoms**:
```
Framework:     Next.js
Confidence:    48%  ← Below threshold
```

**Cause**: Project missing key indicators (package.json incomplete, no tests, etc.)

**Solution 1**: Add missing files

```bash
# For Next.js, ensure package.json has:
{
  "dependencies": {
    "next": "14.0.0",  # Framework version
    "react": "^18"
  },
  "devDependencies": {
    "vitest": "^1.0.0"  # Testing framework
  }
}
```

**Solution 2**: Use `--auto` flag to skip confirmation

```bash
python3 skills/project-analyzer/analyze_project.py . --auto
# Generates subagents even if confidence < 50%
```

**Solution 3**: Override with `.claude/project.yml` (100% confidence)

---

## Phase Detection Issues

### Issue: "Wrong phase detected"

**Symptoms**:
```
Detected: Prototype
Expected: MVP or Production
```

**Cause**: Insufficient maturity signals (version, tests, docs, etc.)

**Solution 1**: Improve project maturity signals

**For MVP phase**:
```bash
# 1. Bump version to 0.x.x
# In package.json or pyproject.toml
"version": "0.5.0"  # Not 0.0.x

# 2. Add tests
mkdir tests  # Or __tests__
# Add at least 10 test files

# 3. Add documentation
touch README.md CONTRIBUTING.md

# 4. Re-run detection
python3 skills/adaptive-review/detect_phase.py .
```

**For Production phase**:
```bash
# 1. Bump version to 1.x.x
"version": "1.0.0"

# 2. Add comprehensive tests (80%+ coverage)
# 3. Add CI/CD
mkdir -p .github/workflows
# Add ci.yml

# 4. Add full documentation
touch CHANGELOG.md SECURITY.md

# 5. Re-run detection
python3 skills/adaptive-review/detect_phase.py .
```

**Solution 2**: Manual override

```bash
mkdir -p .claude

cat > .claude/phase.yml << 'EOF'
phase: production  # or 'prototype', 'mvp'
reason: "Manual override for strict review standards"
expires: 2025-12-31  # Optional: auto-revert date
EOF
```

**Verification**:
```bash
python3 skills/adaptive-review/detect_phase.py .
# Should show 100% confidence with your phase
```

---

### Issue: "Phase detection is too conservative"

**Symptoms**:
```
Indicators:
  • Version 0.3.0 → MVP
  • 95 commits → MVP
  • 25 test files → Basic testing
  • README + 2 docs

Detected: Prototype (confidence: 52%)
Expected: MVP
```

**Cause**: Weighted voting favors lower phases when signals are mixed

**Solution 1**: Strengthen key signals

```bash
# Phase detection weights:
# - User override: 100%
# - Version: 30%
# - Git history: 20%
# - Tests: 15%
# - CI/CD: 15%
# - Docs: 10%
# - Structure: 10%

# To reach MVP:
# 1. Bump version to 0.5.0+ (strong signal)
# 2. Add CI/CD (15% weight)
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm test
EOF

# Re-run detection
python3 skills/adaptive-review/detect_phase.py .
```

**Solution 2**: Use manual override (fastest)

---

### Issue: "Phase override not working"

**Symptoms**:
```
# .claude/phase.yml exists
phase: production

# But detection still shows:
Detected: MVP
```

**Cause**: YAML syntax error or file not found

**Solution**:

```bash
# 1. Verify file exists
ls -la .claude/phase.yml

# 2. Validate YAML syntax
python3 -c "import yaml; print(yaml.safe_load(open('.claude/phase.yml')))"
# Should print: {'phase': 'production', ...}

# 3. Check for typos
cat .claude/phase.yml
# phase: production  ← Must be lowercase
# reason: "..."      ← Optional but recommended

# 4. Ensure detection looks in current directory
python3 skills/adaptive-review/detect_phase.py .
#                                               ^ Don't forget the dot
```

---

## Template Generation Issues

### Issue: "No templates generated"

**Symptoms**:
```
📝 Generating subagents...

✗ No templates found for framework: my-framework
```

**Cause**: Framework not yet supported, or template path incorrect

**Solution 1**: Check supported frameworks

```bash
# List available templates
ls skills/adaptive-claude-agents/templates/

# Current supported:
# - nextjs/
# - fastapi/
# - vanilla-php-web/
# - python-ml/
# - ios-swift/
```

**Solution 2**: Request template support

[Create a template request](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=template_request.md)

**Solution 3**: Create custom template

```bash
# See CONTRIBUTING.md for template creation guide
mkdir -p .claude/agents
cat > .claude/agents/my-tester.md << 'EOF'
---
name: my-tester
description: Custom testing specialist
tools: [Read, Write, Edit, Bash]
---

You are a testing specialist for [your framework]...
EOF
```

---

### Issue: "Template variables not substituted"

**Symptoms**:
```markdown
# Generated template shows:
Framework: {{FRAMEWORK}}  ← Not substituted
Language: {{LANGUAGE}}
```

**Cause**: Template generation script error, or reading template directly

**Solution**:

```bash
# Don't read template source files directly
# ✗ Wrong:
cat skills/adaptive-claude-agents/templates/nextjs/tester.md

# ✓ Correct: Use analyze_project.py
python3 skills/project-analyzer/analyze_project.py .

# Generated files in .claude/agents/ will have substituted values
cat .claude/agents/nextjs-tester.md
# Framework: Next.js ✓
# Language: TypeScript ✓
```

---

### Issue: "Permission denied when generating"

**Symptoms**:
```
✗ Permission denied: .claude/agents/
```

**Cause**: No write permissions for .claude directory

**Solution**:

```bash
# Check permissions
ls -la .claude/

# Fix permissions
chmod 755 .claude
chmod 755 .claude/agents

# Or recreate directory
rm -rf .claude/agents
mkdir -p .claude/agents

# Try again
python3 skills/project-analyzer/analyze_project.py .
```

---

## Platform-Specific Issues

### macOS Issues

#### Issue: "Operation not permitted"

**Cause**: macOS Gatekeeper or Full Disk Access restrictions

**Solution**:

```bash
# 1. Allow Terminal full disk access
# System Settings → Privacy & Security → Full Disk Access
# Enable for Terminal

# 2. For install.sh permission issues
chmod +x install.sh
xattr -dr com.apple.quarantine install.sh  # Remove quarantine

# 3. Run again
./install.sh
```

---

#### Issue: "Skills directory contains spaces"

**Cause**: Default macOS path has spaces: `~/Library/Application Support/Claude/skills`

**Solution**: This is normal and handled by the scripts

```bash
# Scripts properly quote paths
# No action needed - this should work out of the box

# If you see issues, try:
CLAUDE_SKILLS_DIR="$HOME/Library/Application Support/Claude/skills"
export CLAUDE_SKILLS_DIR
```

---

### Linux Issues

#### Issue: "~/.config/claude/skills doesn't exist"

**Cause**: Claude Code uses different path on your system

**Solution**:

```bash
# Find Claude Code installation
find ~ -type d -name "claude" 2>/dev/null

# Or set custom path
export CLAUDE_SKILLS_DIR="/path/to/your/claude/skills"
./install.sh
```

---

#### Issue: "pip3 command not found"

**Solution**:

```bash
# Ubuntu/Debian
sudo apt install python3-pip

# Fedora/RHEL
sudo dnf install python3-pip

# Arch
sudo pacman -S python-pip
```

---

### Windows WSL Issues

#### Issue: "Path conversion errors"

**Symptoms**:
```
Error: /mnt/c/Users/.../AppData/Roaming/Claude/skills: No such file
```

**Solution**:

```bash
# Convert Windows path to WSL path
# Windows: C:\Users\YourName\AppData\Roaming\Claude\skills
# WSL: /mnt/c/Users/YourName/AppData/Roaming/Claude/skills

# Set correct path
export CLAUDE_SKILLS_DIR="/mnt/c/Users/$(cmd.exe /c "echo %USERNAME%" | tr -d '\r')/AppData/Roaming/Claude/skills"

./install.sh
```

---

#### Issue: "Line ending issues (^M)"

**Cause**: Git converted LF to CRLF on Windows

**Solution**:

```bash
# Configure git to use LF
git config --global core.autocrlf input

# Convert existing files
dos2unix install.sh update.sh uninstall.sh

# Or manually
sed -i 's/\r$//' install.sh
chmod +x install.sh
```

---

## Performance Issues

### Issue: "Detection is slow (> 30 seconds)"

**Cause**: Large project with many files

**Solution 1**: Use `.gitignore` patterns

```bash
# Detection automatically respects .gitignore
# Add to .gitignore:
echo "node_modules/" >> .gitignore
echo "venv/" >> .gitignore
echo ".venv/" >> .gitignore
echo "dist/" >> .gitignore
```

**Solution 2**: Specify project type manually (skips detection)

```bash
# Use .claude/project.yml (instant)
cat > .claude/project.yml << 'EOF'
framework: nextjs
version: "14.0.0"
language: typescript
EOF

# Detection will skip file scanning
```

---

### Issue: "Phase detection times out"

**Cause**: Very large git history or many test files

**Solution**:

```bash
# 1. Use manual override (instant)
cat > .claude/phase.yml << 'EOF'
phase: mvp
reason: "Manual override for performance"
EOF

# 2. Or limit git log depth in detect_phase.py
# Edit skills/adaptive-review/detect_phase.py:
# git log --oneline --max-count=1000  # Instead of all commits
```

---

## Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide** (you are here!)
2. **Search existing issues**: [GitHub Issues](https://github.com/SawanoLab/adaptive-claude-agents/issues)
3. **Check documentation**:
   - [Quick Start](./QUICKSTART.md)
   - [Full README](../README.md)
   - [Examples](./EXAMPLES.md)

### How to Report an Issue

**Good bug report**:

```markdown
**Bug Description**: Detection fails for Next.js project

**Environment**:
- OS: macOS 14.1
- Python: 3.11.7
- Claude Code: 0.4.2
- Project type: Next.js 14 with TypeScript

**Steps to Reproduce**:
1. Run `python3 skills/project-analyzer/detect_stack.py .`
2. See error: "ModuleNotFoundError: No module named 'yaml'"

**Expected**: Detection completes successfully
**Actual**: Python error

**Logs**:
```
[paste error output]
```

**Additional Context**:
- Fresh installation
- Virtual environment: No
- package.json exists and has "next": "14.2.0"
```

### Where to Get Help

- **Bug reports**: [GitHub Issues](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=bug_report.md)
- **Feature requests**: [GitHub Issues](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=feature_request.md)
- **Questions**: [GitHub Discussions](https://github.com/SawanoLab/adaptive-claude-agents/discussions)
- **Security issues**: Email security@sawanolab.org

### Provide Debug Information

When reporting issues, include:

```bash
# 1. System info
uname -a
python3 --version
git --version

# 2. Installation check
ls -la "$CLAUDE_SKILLS_DIR/adaptive-claude-agents"

# 3. Detection output (if applicable)
python3 skills/project-analyzer/detect_stack.py . --verbose 2>&1 | tee detection.log

# 4. Phase detection (if applicable)
python3 skills/adaptive-review/detect_phase.py . 2>&1 | tee phase.log
```

### Community Support

- **Star the repo** ⭐ to show support
- **Share your experience** in [Discussions](https://github.com/SawanoLab/adaptive-claude-agents/discussions)
- **Contribute fixes** via [Pull Requests](https://github.com/SawanoLab/adaptive-claude-agents/pulls)

---

## Still Having Issues?

If your issue isn't covered here:

1. 📝 [Open a new issue](https://github.com/SawanoLab/adaptive-claude-agents/issues/new)
2. 💬 [Start a discussion](https://github.com/SawanoLab/adaptive-claude-agents/discussions)
3. 📧 Email security@sawanolab.org (for security issues only)

We're here to help! 🙏

---

**Last Updated**: 2025-10-19

For more documentation:
- [Quick Start Guide](./QUICKSTART.md)
- [Examples Gallery](./EXAMPLES.md)
- [Full Documentation](../README.md)
