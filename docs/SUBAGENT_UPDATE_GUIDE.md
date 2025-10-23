# Subagent Update Guide

This guide explains how to update your project's subagents when new template versions are released.

## Overview

Adaptive Claude Agents provides three update modes to handle different scenarios:

| Mode | Use Case | Customizations | New Templates | Backup |
|------|----------|----------------|---------------|--------|
| `--update-only` | **Safest** - Update existing files only | ⚠️ Overwritten | ❌ Not added | ❌ No |
| `--merge` | Add new templates, preserve existing | ✅ Preserved | ✅ Added | ✅ Yes |
| `--force` | Complete regeneration | ❌ Lost | ✅ Added | ✅ Yes |

## Quick Start

### Recommended: Update Only

```bash
cd /path/to/your/project
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --update-only --auto
```

**What happens**:
- ✅ Existing `.claude/agents/*.md` files updated to latest templates
- ⚠️ Your customizations are overwritten
- ❌ New templates from latest version are NOT added
- ❌ No backup created

**When to use**: You haven't customized any subagents and want the latest versions.

### Merge Mode (Preserve Customizations)

```bash
cd /path/to/your/project
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --merge --auto
```

**What happens**:
- ✅ Existing files are preserved (no changes)
- ✅ New templates added from latest version
- ✅ Backup created at `.claude/agents.backup.YYYYMMDD-HHMMSS/`

**When to use**: You have customized subagents and want to add new templates without losing your changes.

### Force Mode (Complete Regeneration)

```bash
cd /path/to/your/project
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --force --auto
```

**What happens**:
- ⚠️ All files completely regenerated
- ❌ Customizations lost
- ✅ New templates added
- ✅ Backup created at `.claude/agents.backup.YYYYMMDD-HHMMSS/`

**When to use**: You want a fresh start with latest templates (e.g., major version upgrade).

## Using Claude Code Slash Command

For easier access within Claude Code:

```
/update-subagents
```

Claude will ask which mode you prefer and run the update for you.

## Update Summary Output

After running an update, you'll see a summary like:

```
📊 Summary:
  • Generated: 2 new agent(s)
  • Updated: 3 existing agent(s)
  • Preserved: 1 customized agent(s)
```

## Backup Management

### Backup Location

Backups are created in `.claude/agents.backup.YYYYMMDD-HHMMSS/` with timestamp:

```
.claude/
├── agents/                        # Current subagents
├── agents.backup.20251024-073851/ # Backup from Oct 24, 7:38 AM
└── agents.backup.20251024-073904/ # Backup from Oct 24, 7:39 AM
```

### Restoring from Backup

If you need to restore:

```bash
cd /path/to/your/project

# List available backups
ls .claude/agents.backup.*

# Restore from specific backup
rm -rf .claude/agents
cp -r .claude/agents.backup.20251024-073851 .claude/agents
```

### Cleaning Old Backups

```bash
# Remove backups older than 30 days
find .claude -name "agents.backup.*" -mtime +30 -exec rm -rf {} \;
```

## Migration Scenarios

### Scenario 1: v1.0.0 → v1.1.0 (Minor Update)

**No customizations**:
```bash
python3 analyze_project.py . --update-only --auto
```

**With customizations**:
```bash
python3 analyze_project.py . --merge --auto
# Review new templates
# Manually merge improvements if desired
```

### Scenario 2: v1.x → v2.0.0 (Major Update)

**Breaking changes expected**:
```bash
# Create manual backup first
cp -r .claude/agents .claude/agents.manual-backup

# Force regeneration
python3 analyze_project.py . --force --auto

# Compare and manually restore customizations
diff -r .claude/agents.manual-backup .claude/agents
```

### Scenario 3: New Framework Support Added

**Example: Next.js project now has `app-router-specialist`**:

```bash
# Merge mode will add the new template
python3 analyze_project.py . --merge --auto

# Result:
# ✓ nextjs-tester.md (preserved)
# ✓ component-reviewer.md (preserved)
# ✓ app-router-specialist.md (NEW!)
```

## Best Practices

### 1. Check Release Notes First

Before updating, read `CHANGELOG.md`:

```bash
cd "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents"
cat CHANGELOG.md | head -50
```

### 2. Update Framework First

Always update the global framework before project subagents:

```bash
# Step 1: Update framework
cd "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents"
bash update.sh

# Step 2: Update project subagents
cd /path/to/your/project
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --merge --auto
```

### 3. Version Control

Commit before and after updates:

```bash
# Before
git add .claude/agents
git commit -m "chore: pre-update snapshot of subagents"

# Update
python3 analyze_project.py . --merge --auto

# After
git add .claude/agents
git commit -m "chore: update subagents to v1.1.0"
```

### 4. Review Changes

Compare before/after:

```bash
# Show what changed
git diff HEAD~1 .claude/agents

# Review new templates
ls .claude/agents/*.md | xargs -I {} basename {}
```

## Troubleshooting

### Update Failed

```
⚠️  No existing agents found. Use without --update-only to generate new agents.
```

**Solution**: Run without `--update-only` for initial generation:
```bash
python3 analyze_project.py . --auto
```

### Customizations Lost

If you accidentally used `--force` instead of `--merge`:

```bash
# Restore from automatic backup
ls .claude/agents.backup.*  # Find latest backup
cp -r .claude/agents.backup.20251024-073851/* .claude/agents/
```

### Merge Not Adding New Templates

Check if detection changed:

```bash
python3 analyze_project.py . --verbose
# Review "recommended_subagents" list
```

## Advanced: Manual Template Merging

For complex customizations, manually merge:

```bash
# 1. Update with merge mode
python3 analyze_project.py . --merge --auto

# 2. Get latest template version
TEMPLATE_DIR="$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/templates/nextjs"
diff "$TEMPLATE_DIR/tester.md" .claude/agents/nextjs-tester.md

# 3. Use your favorite diff/merge tool
code --diff "$TEMPLATE_DIR/tester.md" .claude/agents/nextjs-tester.md
```

## FAQ

### Q: Which mode should I use by default?

**A**: For most users, `--merge` is the safest choice:
- Preserves customizations
- Adds new templates
- Creates backup

### Q: Can I undo an update?

**A**: Yes, if a backup was created:
```bash
cp -r .claude/agents.backup.LATEST/* .claude/agents/
```

### Q: How often should I update?

**A**:
- After major releases (v1.x → v2.0): Use `--force`
- After minor releases (v1.0 → v1.1): Use `--merge`
- Monthly maintenance: Use `--update-only`

### Q: Will updates change my project code?

**A**: No! Updates only affect `.claude/agents/` files (subagent templates). Your project code is never modified.

---

## See Also

- [Quick Start Guide](./QUICKSTART.md)
- [Troubleshooting](./TROUBLESHOOTING.md)
- [Version Management](./VERSION_MANAGEMENT.md)
