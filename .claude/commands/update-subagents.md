# Update Subagents Command

Update existing project subagents from the latest templates.

## Task

You are tasked with helping the user update the subagent files in `.claude/agents/` using the latest templates from Adaptive Claude Agents.

## Instructions

### Step 1: Check for Existing Agents

First, check if the project has existing subagents:

```bash
ls .claude/agents/*.md 2>/dev/null | grep -v SUBAGENT_GUIDE.md | wc -l
```

If no agents found:
```
⚠️  No existing subagents found. Would you like to generate them for the first time?

Run: python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --auto
```

### Step 2: Present Update Options

If agents exist, present the three update modes to the user:

```
I found existing subagents in .claude/agents/. Which update mode would you like?

**1. --update-only (Recommended for most users)**
   ✅ Updates existing files to latest template versions
   ⚠️  Overwrites your customizations
   ❌ Won't add new templates from latest release
   ❌ No backup created

   Best for: Projects where you haven't customized the generated agents

**2. --merge (Safest if you've customized agents)**
   ✅ Adds any new templates from latest release
   ✅ Preserves your existing files (no changes)
   ✅ Creates backup: .claude/agents.backup.YYYYMMDD-HHMMSS/
   ⚠️  Existing files won't get template improvements

   Best for: Projects where you've customized agents and want new templates

**3. --force (Complete refresh)**
   ✅ Complete regeneration with latest templates
   ✅ Creates backup before overwriting
   ❌ All customizations lost (but backed up)

   Best for: Major version upgrades or when you want a fresh start

Which mode would you like? (Type 1, 2, or 3, or specify the mode name)
```

### Step 3: Execute Update

Based on user's choice:

```bash
# For macOS/Linux
python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --[MODE] --auto

# MODE is one of: update-only, merge, force
```

### Step 4: Report Results

After execution, summarize what happened:

```
✅ Subagents updated successfully!

📊 Summary:
• Updated: X existing agent(s)
• Generated: Y new agent(s)
• Preserved: Z customized agent(s)

📦 Backup created: .claude/agents.backup.20251024-123456/

📁 Location: .claude/agents/
📖 Guide: .claude/agents/SUBAGENT_GUIDE.md

You can now use the updated subagents. They'll auto-trigger based on keywords in your requests.
```

## Default Recommendation

If the user doesn't specify a preference, recommend:
- **`--merge`** if you detect any customizations (file sizes differ from templates)
- **`--update-only`** if files appear to be unmodified

## Example Conversations

### Example 1: User asks directly

```
User: /update-subagents