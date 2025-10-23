# Update Subagents Command

Update existing project subagents from the latest templates.

## Task

You are tasked with updating the subagent files in `.claude/agents/` using the latest templates from Adaptive Claude Agents.

## Instructions

1. **Determine update strategy** by asking the user which mode they prefer:
   - `--update-only`: Update only existing files (safest, preserves all customizations)
   - `--merge`: Add new templates, preserve existing ones with backup
   - `--force`: Complete regeneration (overwrites everything with backup)

2. **Run the update command**:
   ```bash
   python3 "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --[mode]
   ```

3. **Report the results**:
   - Show number of files updated
   - Show number of files preserved
   - Show number of new files added (if merge mode)
   - Location of backup (if created)

## Default Recommendation

If the user doesn't specify, recommend `--update-only` as the safest option that preserves customizations.

## Example Usage

```
User: /update-subagents