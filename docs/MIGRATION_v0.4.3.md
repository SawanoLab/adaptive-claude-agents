# Migration Guide: v0.4.2-beta → v0.4.3-beta

## Overview

Version 0.4.3-beta introduces **AGGRESSIVE subagent delegation policy** with auto-generated project-specific guides. This guide helps you migrate existing projects to take full advantage of the new features.

---

## What's New in v0.4.3-beta

### 1. AGGRESSIVE Mode (Default)
- **Installation = Consent** to proactive subagent usage
- No user choice needed (AGGRESSIVE by default)
- 3+ files = automatic Task tool delegation

### 2. Auto-Generated SUBAGENT_GUIDE.md
- Framework-specific workflows (~250 lines)
- Auto-trigger keywords for each subagent type
- Cost vs Time analysis table
- Success metrics tracking (20-30% usage rate target)

### 3. CLAUDE.md Auto-Configuration
- AGGRESSIVE policy automatically added during install/update
- Applies to both global tool and individual projects

### 4. Enhanced Templates
- Latest best practices for all 11 frameworks
- Improved detection accuracy (70-100% confidence)

---

## Migration Steps

### Step 1: Update Global Tool (Required)

```bash
# macOS
cd "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents"
./update.sh

# Linux/WSL
cd ~/.config/claude/skills/adaptive-claude-agents
./update.sh
```

**Expected output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ Update Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 AGGRESSIVE Mode Enabled

  New features:
  • Auto-generated SUBAGENT_GUIDE.md (framework-specific)
  • Proactive subagent usage for 3+ file tasks
  • Cost-benefit analysis for efficient delegation
  • Target: 20-30% subagent usage, 2-4 hours saved/week
```

---

### Step 2: Update Each Project (Critical!)

**For every project where you previously ran `analyze_project.py`**, you need to re-run it to get:

1. ✅ Latest SUBAGENT_GUIDE.md with framework-specific workflows
2. ✅ AGGRESSIVE policy in your project's CLAUDE.md
3. ✅ Updated subagent templates with 2025 best practices

#### Quick Update Command

```bash
# Navigate to each project and run:
cd /path/to/project-1
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --auto

cd /path/to/project-2
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --auto

# ... repeat for all projects
```

#### Batch Update Script (Optional)

Create a script to update all your projects at once:

```bash
#!/bin/bash
# update-all-projects.sh

PROJECTS=(
    "$HOME/projects/my-nextjs-app"
    "$HOME/projects/api-backend"
    "$HOME/projects/mobile-app"
)

ANALYZER="$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py"

for project in "${PROJECTS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Updating: $project"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    cd "$project" || continue
    python3 "$ANALYZER" . --auto

    echo ""
done

echo "✅ All projects updated!"
```

Make it executable and run:

```bash
chmod +x update-all-projects.sh
./update-all-projects.sh
```

---

## What Gets Updated in Each Project

### Before Update

```
your-project/
├── .claude/
│   └── agents/
│       ├── nextjs-tester.md          (old template)
│       └── component-reviewer.md     (old template)
└── CLAUDE.md                         (no AGGRESSIVE policy)
```

### After Update

```
your-project/
├── .claude/
│   └── agents/
│       ├── nextjs-tester.md          (✨ updated template)
│       ├── component-reviewer.md     (✨ updated template)
│       └── SUBAGENT_GUIDE.md         (✨ NEW - ~250 lines)
└── CLAUDE.md                         (✨ + AGGRESSIVE policy)
```

---

## Verification Checklist

After updating, verify each project has:

### 1. Check SUBAGENT_GUIDE.md

```bash
cd /path/to/your/project
cat .claude/agents/SUBAGENT_GUIDE.md | head -20
```

**Expected output**:
```markdown
# Subagent Usage Guide for NEXTJS Projects

## 🎯 AGGRESSIVE Mode (Default)

**You installed Adaptive Claude Agents = You want proactive subagent usage.**

This guide was auto-generated based on your project:
- Framework: **nextjs**
- Confidence: **100%**
- Language: **typescript**
...
```

### 2. Check CLAUDE.md Policy

```bash
grep -A 5 "AGGRESSIVE ポリシー" CLAUDE.md
```

**Expected output**:
```markdown
## 🤖 Adaptive Claude Agents - AGGRESSIVE ポリシー

**このプロジェクトにAdaptive Claude Agentsをインストール = サブエージェントを積極的に使いたい**

### 必須ルール（MANDATORY）
...
```

### 3. Test Proactive Delegation

Try these commands in Claude Code:

```text
User: "この3つのファイルに同じ修正を適用して"
→ Expected: Auto-delegates to general-purpose subagent

User: "version_number の使用箇所を検索して"
→ Expected: Auto-delegates to Explore agent (very thorough)

User: "ログインボタンをクリックしてテストして"
→ Expected: Auto-delegates to chrome-devtools-tester
```

---

## Troubleshooting

### Issue 1: "Could not detect tech stack"

**Cause**: Project doesn't match supported frameworks (Next.js, FastAPI, Go, Flutter, etc.)

**Solution**:
1. Check supported frameworks: https://github.com/SawanoLab/adaptive-claude-agents#supported-frameworks
2. Manually create `.claude/project.yml` with framework specification
3. Open an issue: https://github.com/SawanoLab/adaptive-claude-agents/issues

### Issue 2: CLAUDE.md not updated

**Cause**: Running `analyze_project.py` doesn't modify CLAUDE.md (only install.sh/update.sh do)

**Solution**:
Run update.sh in the **project directory** (not skills directory):

```bash
cd /path/to/your/project
bash "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/update.sh"
```

### Issue 3: Old templates still present

**Cause**: `analyze_project.py` doesn't overwrite existing templates by default

**Solution**:
Delete old templates and re-run:

```bash
rm -rf .claude/agents/*.md
python3 "$ANALYZER" . --auto
```

---

## Rollback Instructions

If you need to revert to v0.4.2-beta:

```bash
# 1. Restore backup
cd "$HOME/Library/Application Support/Claude/skills"
rm -rf adaptive-claude-agents
mv adaptive-claude-agents.backup adaptive-claude-agents

# 2. In each project, remove new files
cd /path/to/your/project
rm .claude/agents/SUBAGENT_GUIDE.md

# 3. Remove AGGRESSIVE policy from CLAUDE.md (manual edit)
```

---

## Benefits After Migration

### Expected Improvements

| Metric | Before v0.4.3 | After v0.4.3 |
|--------|---------------|--------------|
| **Subagent Usage** | 5-10% (manual) | 20-30% (auto) |
| **Decision Fatigue** | High | Zero |
| **Time Saved/Week** | 0-1 hour | 2-4 hours |
| **Framework Guidance** | Generic | Specific |

### New Capabilities

1. **Automatic Triggers**
   - "3つのファイルに..." → auto-delegate
   - "検索して..." → Explore agent
   - "テストして..." → framework tester

2. **Framework-Specific Workflows**
   - Next.js: Component Development (3+ components)
   - FastAPI: CRUD Endpoint Development (2+ endpoints)
   - Go: Concurrency Review (MANDATORY)
   - Flutter: Widget Development (3+ widgets)

3. **Cost-Benefit Clarity**
   - Clear tables showing token costs vs time saved
   - No more guessing "should I use a subagent?"

---

## Support

If you encounter any issues during migration:

1. Check [Troubleshooting Guide](./TROUBLESHOOTING.md)
2. Read [Examples](./EXAMPLES.md) for usage patterns
3. Open an issue: https://github.com/SawanoLab/adaptive-claude-agents/issues

---

**Migration completed?** Start using aggressive subagent delegation in your daily workflow! 🚀
