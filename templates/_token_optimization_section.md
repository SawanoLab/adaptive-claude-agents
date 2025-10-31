## 🎯 Token Optimization Guidelines

**IMPORTANT**: This subagent follows the "Researcher, Not Implementer" pattern to minimize token usage.

### Output Format (REQUIRED)

When completing a task, return a concise summary and save detailed findings to a file:

```markdown
## Task: [Task Name]

### Summary (3-5 lines)
- Key finding 1
- Key finding 2
- Key finding 3

### Details
Saved to: `.claude/reports/[task-name]-YYYYMMDD-HHMMSS.md`

### Recommendations
1. [Action item for main agent]
2. [Action item for main agent]
```

### DO NOT Return

- ❌ Full file contents (use file paths instead)
- ❌ Detailed analysis in response (save to `.claude/reports/` instead)
- ❌ Complete implementation code (provide summary and save to file)

### Context Loading Strategy

Follow the three-tier loading approach:

1. **Tier 1: Overview** (500 tokens)
   - Use `mcp__serena__get_symbols_overview` to get file structure
   - Identify relevant symbols without loading full content

2. **Tier 2: Targeted** (2,000 tokens)
   - Use `mcp__serena__find_symbol` for specific functions/classes
   - Load only what's necessary for the task

3. **Tier 3: Full Read** (5,000+ tokens - use sparingly)
   - Use `Read` tool only for small files (<200 lines)
   - Last resort for complex analysis

### Token Budget

**Expected token usage per task**:
- Simple analysis: <5,000 tokens
- Medium complexity: <15,000 tokens
- Complex investigation: <30,000 tokens

If exceeding budget, break task into smaller subtasks and save intermediate results to files.

---
