# Adaptive Claude Agents - Skill Instructions

## Overview

**Skill Name**: Adaptive Claude Agents
**Version**: 1.1.0
**Purpose**: Auto-generate project-specific Claude Code subagents that adapt to your development phase and framework.

This skill enables Claude to:
1. Automatically detect project technology stack (11 frameworks supported)
2. Detect development phase (Prototype, MVP, Production)
3. Generate appropriate subagents with AGGRESSIVE delegation policy
4. Provide framework-specific workflow guides

---

## When to Use This Skill

Use this skill when:
- User asks: "Analyze my project and generate subagents"
- User asks: "What development phase am I in?"
- User mentions: "Set up adaptive agents for this project"
- Starting work on a new project that needs subagent configuration

**DO NOT use** for:
- Simple file operations
- General code review
- Tasks unrelated to project setup

---

## Available Commands

### 1. Project Analysis & Subagent Generation

**Command**:
```bash
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" [PROJECT_PATH] [--auto]
```

**When to use**:
- First time setting up a project
- After updating Adaptive Claude Agents to latest version
- User explicitly requests project analysis

**What it does**:
1. Detects tech stack (Next.js, FastAPI, Go, Flutter, etc.)
2. Generates `.claude/agents/SUBAGENT_GUIDE.md` with framework-specific workflows
3. Creates specialized subagent templates
4. Adds AGGRESSIVE policy to project's `CLAUDE.md`

**Output**:
```
✅ Successfully generated subagents!
📁 Location: .claude/agents/
📖 Usage Guide: .claude/agents/SUBAGENT_GUIDE.md
```

### 2. Development Phase Detection

**Command**:
```bash
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/adaptive-review/detect_phase.py" [PROJECT_PATH]
```

**When to use**:
- User asks about current development phase
- Determining appropriate code review rigor
- Project planning discussions

**What it does**:
1. Analyzes version number, commits, tests
2. Classifies as Prototype (3/10), MVP (6/10), or Production (10/10)
3. Provides phase-appropriate review recommendations

**Output**:
```
Phase: MVP
Confidence: 72%
Review Rigor: 6/10 (moderate)
```

### 3. Framework Detection Only

**Command**:
```bash
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/detect_stack.py" [PROJECT_PATH]
```

**When to use**:
- Quick framework check without generating subagents
- Debugging detection logic
- User asks: "What framework does this project use?"

**What it does**:
1. Detects framework with confidence score
2. Lists detected tools (testing, database, etc.)
3. Shows detection reasoning

**Output**:
```
Detected: Next.js 14
Confidence: 98%
Tools: Vitest, Testing Library, Tailwind CSS
```

### 4. Update Existing Subagents

**Command**:
```bash
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --[MODE] --auto
```

**When to use**:
- User asks: "サブエージェントを更新して" / "Update my subagents"
- User mentions: "最新のテンプレートに更新" / "Update to latest templates"
- After framework update (e.g., `bash update.sh`)
- User asks: "新しいテンプレートがあるか確認して" / "Check for new templates"

**Available Modes**:

1. **`--update-only`** (RECOMMENDED - Safest)
   - Updates only existing `.claude/agents/*.md` files
   - Preserves file list (no new files added)
   - ⚠️ Overwrites customizations
   - No backup created
   - **Use when**: User hasn't customized agents

2. **`--merge`** (SAFE - Preserves customizations)
   - Adds new templates from latest version
   - Preserves existing files (no changes)
   - ✅ Customizations protected
   - Creates backup: `.claude/agents.backup.YYYYMMDD-HHMMSS/`
   - **Use when**: User has customized agents and wants new templates

3. **`--force`** (DESTRUCTIVE - Complete regeneration)
   - Regenerates all files from templates
   - ❌ Customizations lost
   - Creates backup
   - **Use when**: User explicitly requests complete refresh

**Interactive Workflow**:

When user asks to update subagents:

1. **Check for existing agents**:
   ```bash
   ls .claude/agents/*.md 2>/dev/null
   ```

2. **Ask user which mode**:
   ```
   I found existing subagents in .claude/agents/. Which update mode would you like?

   1. --update-only (Recommended): Update existing files to latest versions
      ⚠️  Your customizations will be overwritten
      ✅ Safest for non-customized projects

   2. --merge: Add new templates, preserve your existing customizations
      ✅ Your changes are safe
      ✅ Gets new templates
      ⚠️  Existing files won't get template improvements

   3. --force: Complete regeneration (creates backup first)
      ❌ Customizations lost
      ✅ Fresh start with latest templates
   ```

3. **Execute with chosen mode**:
   ```bash
   python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --[MODE] --auto
   ```

4. **Report results**:
   ```
   📊 Update Summary:
   • Updated: 3 existing agent(s)
   • Preserved: 1 customized agent(s)
   • Backup: .claude/agents.backup.20251024-073851/
   ```

**Default recommendation**: If user doesn't specify, suggest `--merge` as the safest option.

**Slash command shortcut**: User can also use `/update-subagents`

---

## Supported Frameworks

| Framework | Detection Confidence | Template Quality |
|-----------|---------------------|------------------|
| Next.js | 100% | ✅ Excellent |
| FastAPI | 80% | ✅ Excellent |
| React (Vite) | 80% | ✅ Good |
| Vue | 90% | ✅ Good |
| Django | 80% | ✅ Good |
| Flask | 70% | ✅ Good |
| Vanilla PHP/Web | 80% | ✅ Good |
| Python ML/CV | 100% | ✅ Excellent |
| iOS Swift | 80% | ✅ Good |
| Go | 85% | ✅ Excellent |
| Flutter | 80% | ✅ Excellent |

**Total**: 11 frameworks, 15 specialized templates

---

## AGGRESSIVE Mode Philosophy

**Core Principle**: Installation = Consent to Proactive Subagent Usage

### Mandatory Delegation Rules

Claude MUST use Task tool when:

1. **3+ files need similar modifications**
   - Example: "Apply blur fix to assessment.js, soap.js, nursing_plan.js"
   - Subagent: `general-purpose`
   - Time saved: 30-60 minutes

2. **Searching entire codebase for patterns**
   - Example: "Find all uses of version_number"
   - Subagent: `Explore` (thoroughness: "very thorough")
   - Time saved: 60-90 minutes

3. **E2E testing or automated verification**
   - Example: "Test login flow → API call → DB validation"
   - Subagent: `general-purpose` + `chrome-devtools-tester`
   - Time saved: 45+ minutes

4. **2+ independent tasks can run in parallel**
   - Example: "Update .gitignore + Refactor UI components"
   - Subagent: Multiple `general-purpose` in single message
   - Time saved: 30+ minutes

### Cost vs Time Guidance

| Task Type | Direct Cost | Subagent Cost | Time Saved | Recommendation |
|-----------|-------------|---------------|------------|----------------|
| 1 file edit | 5k tokens | 25k tokens | 0 min | ❌ Direct |
| 3-4 files | 15k tokens | 35k tokens | 30 min | ✅ Subagent |
| 5+ files | 30k tokens | 50k tokens | 60 min | ✅✅ Subagent |
| Codebase search | 40k tokens | 60k tokens | 90 min | ✅✅✅ Explore |

**Rule of Thumb**: 20k token overhead is acceptable for 30+ minutes saved.

---

## Input/Output Specifications

### analyze_project.py

**Inputs**:
- `PROJECT_PATH` (optional, default: current directory)
- `--auto` flag (skip user confirmation)
- `--verbose` flag (enable debug logging)

**Outputs**:
- `.claude/agents/SUBAGENT_GUIDE.md` (~250 lines, framework-specific)
- `.claude/agents/*.md` (specialized subagent templates)
- Updated `CLAUDE.md` (AGGRESSIVE policy added)

**Exit codes**:
- `0`: Success
- `1`: Detection failed or user aborted

### detect_phase.py

**Inputs**:
- `PROJECT_PATH` (optional, default: current directory)

**Outputs**:
- JSON or human-readable phase analysis
- Confidence score (0-100%)
- Review rigor recommendation (1-10)

### detect_stack.py

**Inputs**:
- `PROJECT_PATH` (required)
- `--help` (show usage)

**Outputs**:
- Framework name
- Version (if detected)
- Confidence score
- Detected tools by category

---

## Example Workflows

### Workflow 1: New Project Setup

```text
User: "I started a new Next.js project. Set up adaptive agents for it."

Claude:
1. Confirms project path
2. Runs: analyze_project.py /path/to/project --auto
3. Reports success with generated files
4. Guides user to read SUBAGENT_GUIDE.md
```

### Workflow 2: Framework Identification

```text
User: "What framework is this project using?"

Claude:
1. Runs: detect_stack.py .
2. Shows: "Detected: FastAPI (80% confidence)"
3. Lists tools: pytest, SQLAlchemy, uvicorn
```

### Workflow 3: Phase-Appropriate Review

```text
User: "Review this new feature"

Claude:
1. Runs: detect_phase.py .
2. Detects: Prototype (3/10 rigor)
3. Applies light review: "Does it work?" focus only
```

### Workflow 4: Multi-File Modification (AGGRESSIVE)

```text
User: "この3つのファイルに同じ修正を適用して"

Claude (Internal):
1. Detects: 3 files = MANDATORY Task tool usage
2. Delegates to: general-purpose subagent
3. Returns: Unified result after parallel execution

(No user confirmation needed - AGGRESSIVE mode)
```

---

## Limitations

### Framework Coverage
- **Supported**: 11 frameworks (Next.js, FastAPI, Go, Flutter, etc.)
- **Not Supported**: Ruby on Rails, ASP.NET, Rust (Actix)
- **Workaround**: Manual `.claude/project.yml` creation

### Detection Accuracy
- **Average**: 85% confidence
- **Range**: 70% (Flask) to 100% (Next.js, Python ML)
- **False Negatives**: Possible for unconventional project structures

### Platform Support
- **macOS**: ✅ Fully tested
- **Linux/WSL**: ✅ Supported
- **Windows (native)**: ⚠️ Untested (may require path adjustments)

---

## Error Handling

### Common Errors

**Error**: "Could not detect tech stack"
**Cause**: Project doesn't match supported frameworks
**Solution**:
1. Check supported frameworks list
2. Create manual `.claude/project.yml`
3. Open issue: https://github.com/SawanoLab/adaptive-claude-agents/issues

**Error**: "Python dependency 'yaml' not found"
**Cause**: pyyaml not installed
**Solution**: `python3 -m pip install --user pyyaml`

**Error**: "Permission denied: .claude/agents/"
**Cause**: Insufficient write permissions
**Solution**: `chmod +w .claude/agents/` or run with appropriate permissions

---

## Security Considerations

### Safe Practices
- ✅ All processing is local (no network requests)
- ✅ No telemetry or analytics
- ✅ Input validation in detection scripts
- ✅ No code execution from detected files

### User Responsibilities
- Review generated SUBAGENT_GUIDE.md before using
- Verify CLAUDE.md policy matches team preferences
- Do not commit sensitive data to templates

---

## Dependencies

### Required (Bundled)
- Python 3.9+
- `pyyaml` library (auto-installed by install.sh)

### Optional
- Git (for commit/version detection in phase analysis)
- Claude Code (for subagent execution)

---

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| 0.4.3-beta | 2025-10-23 | AGGRESSIVE mode, SUBAGENT_GUIDE.md auto-generation |
| 0.4.2-beta | 2025-10-20 | Go & Flutter support, 2025 best practices |
| 0.4.1-beta | 2025-10-19 | Proactive subagent delegation |
| 0.4.0-beta | 2025-10-18 | Public beta release |

**Current Version**: 0.4.3-beta
**Stability**: Beta (production-ready with minor edge cases)

---

## Support & Resources

- **Documentation**: https://github.com/SawanoLab/adaptive-claude-agents
- **Migration Guide**: docs/MIGRATION_v0.4.3.md
- **Examples**: docs/EXAMPLES.md
- **Troubleshooting**: docs/TROUBLESHOOTING.md
- **Issues**: https://github.com/SawanoLab/adaptive-claude-agents/issues

---

## Notes for Claude

- **Be proactive**: Suggest running analyze_project.py for new projects
- **AGGRESSIVE mode**: Use Task tool for 3+ files automatically
- **Framework-aware**: Read SUBAGENT_GUIDE.md for project-specific workflows
- **Progressive disclosure**: Only load this skill when project setup is discussed
- **User confirmation**: Skip with --auto flag, ask otherwise

**Remember**: Installation = User consent to aggressive subagent usage. Trust the automation!
