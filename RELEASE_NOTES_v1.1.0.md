# 🎯 v1.1.0 - Smart Subagent Update System

> **TL;DR**: You can now safely update your project's subagents when we improve templates, with full protection for your customizations!

---

## ✨ What's New

### 🔄 Three Update Modes

Simply say **"update my subagents"** in Claude Code, and choose:

1. **`--update-only`** (Recommended)
   - Updates existing files to latest templates
   - Best for: Unmodified projects

2. **`--merge`** (Safest)
   - Adds new templates
   - Preserves your customizations
   - Creates automatic backup
   - Best for: Customized projects

3. **`--force`** (Complete refresh)
   - Regenerates everything with latest templates
   - Creates backup first
   - Best for: Major version upgrades

### 🗣️ Natural Language Support

**English**: `"update subagents"`, `"refresh agents"`, `"check for new templates"`

**Japanese**: `"サブエージェントを更新"`, `"テンプレートを更新"`, `"エージェントを最新に"`

### 🛡️ Safety Features

- ✅ Automatic timestamped backups
- ✅ Clear explanations before each action
- ✅ Update summaries showing what changed
- ✅ Easy backup restoration

---

## 🚀 How to Use

### Quick Update (Recommended)

In Claude Code:
```
> update my subagents
```

Claude will:
1. Show 3 update options
2. Execute your choice
3. Report what changed

### Command Line

```bash
cd /path/to/your/project

# Update existing files only
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --update-only --auto

# Add new templates, preserve customizations (safest)
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --merge --auto

# Complete regeneration with backup
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --force --auto
```

### Slash Command

```
/update-subagents
```

---

## 📚 Documentation

- **[Update Guide](https://github.com/SawanoLab/adaptive-claude-agents/blob/main/docs/SUBAGENT_UPDATE_GUIDE.md)**: Complete reference with examples
- **[Test Guide](https://github.com/SawanoLab/adaptive-claude-agents/blob/main/docs/UPDATE_WORKFLOW_TEST.md)**: 7 test scenarios
- **[CHANGELOG](https://github.com/SawanoLab/adaptive-claude-agents/blob/main/CHANGELOG.md#110---2025-10-24)**: Full technical details

---

## 🔧 Installation

### New Users

```bash
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
```

### Existing Users (Upgrade from v1.0.0)

**Step 1**: Update the framework
```bash
cd "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents"
bash update.sh
```

**Step 2**: Update your project subagents
```bash
cd /path/to/your/project
"update my subagents"  # In Claude Code
# or
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --merge --auto
```

---

## 📊 Example Workflow

```
You: サブエージェントを更新して

Claude: I found 3 existing subagents. Which mode?

        1. --update-only: Update existing files
        2. --merge: Add new templates, preserve existing ✅
        3. --force: Complete regeneration

You: 2

Claude: ✅ Done!
        • Preserved: 3 customized agents
        • Added: 1 new agent
        📦 Backup: .claude/agents.backup.20251024-123456/
```

---

## 🆕 What's Changed

- **New**: Smart update mechanism with 3 modes
- **New**: Natural language triggers (JP/EN)
- **New**: Interactive Claude Code workflow
- **New**: Automatic backup system
- **New**: `/update-subagents` slash command
- **Docs**: Comprehensive update guides added
- **Version**: 1.0.0 → 1.1.0

**Full Changelog**: https://github.com/SawanoLab/adaptive-claude-agents/blob/main/CHANGELOG.md#110---2025-10-24

---

## 💡 Use Cases

### Monthly Template Updates
```bash
python3 analyze_project.py . --update-only --auto
```
→ Get latest improvements, no new files

### New Templates Available + You Have Customizations
```bash
python3 analyze_project.py . --merge --auto
```
→ Add new templates, keep your changes

### Major Version Upgrade
```bash
python3 analyze_project.py . --force --auto
```
→ Fresh start with backup

---

## 🙏 Feedback

Issues or suggestions? → [Open an issue](https://github.com/SawanoLab/adaptive-claude-agents/issues/new)

---

**Enjoy safer and easier subagent updates!** 🎉
