# Token Optimization Implementation Guide

**Last Updated**: 2025-10-31
**For**: Template Developers, Subagent Authors, Main Agent Implementers

This guide provides practical implementation patterns for reducing token usage when working with Claude Code subagents.

---

## Table of Contents

- [Quick Reference](#quick-reference)
- [1. Markdown Shared Memory Pattern](#1-markdown-shared-memory-pattern)
- [2. Context Compression](#2-context-compression)
- [3. Just-in-Time Context Loading](#3-just-in-time-context-loading)
- [4. Token-Efficient Tools API](#4-token-efficient-tools-api)
- [5. Parallel Processing Management](#5-parallel-processing-management)
- [6. Monitoring & Debugging](#6-monitoring--debugging)
- [Testing Token Optimization](#testing-token-optimization)
- [Common Pitfalls](#common-pitfalls)

---

## Quick Reference

### Token Savings by Strategy

| Strategy | Savings | Effort | Priority |
|----------|---------|--------|----------|
| Markdown Shared Memory | 50-60% | Low | 🔴 Critical |
| Context Compression | 60-80% | Medium | 🔴 Critical |
| Just-in-Time Loading | 40-50% | Medium | 🟡 High |
| Token-Efficient Tools | 10-20% | Low | 🟢 Medium |
| Parallel Processing Limits | Variable | Low | 🔴 Critical |

### Decision Tree

```text
Before delegating to subagent, ask:

1. Can this be done in main agent with <5k tokens?
   YES → Do it in main agent
   NO → Continue to #2

2. Does task require full file contents?
   NO → Pass only file paths (Context Compression)
   YES → Continue to #3

3. Can I load progressively?
   YES → Use Just-in-Time Loading
   NO → Continue to #4

4. Will result be >1000 tokens?
   YES → Use Markdown Shared Memory
   NO → Return result directly

5. Can this be parallelized?
   YES → Check if <3 parallel tasks, then proceed
   NO → Execute sequentially
```

---

## 1. Markdown Shared Memory Pattern

### Concept

Subagents save detailed reports to `.claude/reports/` and return only summaries (3-5 lines) to the main agent.

### Implementation

#### Step 1: Subagent Output Format

All subagents should follow this output format:

```typescript
// In subagent template
async function completeTask(task: string): Promise<string> {
  // 1. Perform analysis (can be thousands of tokens)
  const analysis = await performDeepAnalysis(task)

  // 2. Generate detailed report
  const reportPath = `.claude/reports/${task.name}-${timestamp()}.md`
  await saveReport(reportPath, analysis)

  // 3. Create concise summary (50-200 tokens)
  const summary = `
## Task: ${task.name}

### Summary
- ${analysis.findings[0]}
- ${analysis.findings[1]}
- ${analysis.findings[2]}

### Details
Saved to: \`${reportPath}\`

### Recommendations
1. ${analysis.recommendations[0]}
2. ${analysis.recommendations[1]}
`

  // 4. Return only summary (not full analysis!)
  return summary
}
```

#### Step 2: Main Agent Reading Reports

Main agent reads reports only when needed:

```typescript
// Main agent logic
const summary = await subagent.execute(task)

// Parse report path from summary
const reportPath = extractReportPath(summary)

// Only read report if user asks for details
if (userAsksForDetails) {
  const fullReport = await readFile(reportPath)
  return fullReport
} else {
  // Just show summary
  return summary
}
```

### Example: Before & After

**Before** (Wasteful):
```typescript
// Subagent returns 8,000 token analysis
const analysis = await subagent.analyzeAPI()
// Main agent context grows by 8,000 tokens
// Every subsequent message costs more
```

**After** (Efficient):
```typescript
// Subagent returns 200 token summary
const summary = await subagent.analyzeAPI()
// Main agent context grows by only 200 tokens
// 97.5% reduction!
```

### Report File Naming Convention

```
.claude/reports/[task-type]-[YYYYMMDD]-[HHMMSS].md

Examples:
- .claude/reports/api-review-20251031-143022.md
- .claude/reports/test-coverage-20251031-150345.md
- .claude/reports/security-audit-20251031-163012.md
```

### Directory Structure

```
project-root/
├── .claude/
│   ├── agents/           # Subagent definitions
│   └── reports/          # Generated reports (gitignored)
│       ├── api-review-20251031-143022.md
│       ├── test-coverage-20251031-150345.md
│       └── ...
├── .gitignore            # Contains .claude/reports/
└── ...
```

---

## 2. Context Compression

### Concept

Pass only essential information to subagents. Use file paths, line numbers, and identifiers instead of full file contents.

### Implementation Patterns

#### Pattern A: File Paths Only

**Bad**:
```typescript
// Reading 10 files (50,000 tokens)
const files = [
  { path: "api/users.ts", content: await readFile("api/users.ts") },
  { path: "api/auth.ts", content: await readFile("api/auth.ts") },
  // ... 8 more files
]

await subagent.execute({ files })  // 50,000 tokens!
```

**Good**:
```typescript
// Passing only paths (500 tokens)
const filePaths = [
  "api/users.ts",
  "api/auth.ts",
  // ... 8 more paths
]

await subagent.execute({ filePaths })  // 500 tokens
// Subagent reads files internally as needed
```

#### Pattern B: Targeted Context

**Bad**:
```typescript
// Passing entire codebase context
const context = {
  allFiles: await glob("**/*.ts"),
  dependencies: await readPackageJson(),
  config: await readAllConfigs(),
  // ... everything
}

await subagent.execute(context)  // 100,000+ tokens
```

**Good**:
```typescript
// Passing only relevant context
const context = {
  task: "Review authentication logic",
  relevantFiles: ["api/auth.ts", "lib/jwt.ts"],
  focusAreas: ["login", "token_refresh"],
}

await subagent.execute(context)  // 1,000 tokens
```

#### Pattern C: Line Range References

Instead of full files, pass line ranges:

```typescript
const context = {
  file: "api/users.ts",
  lineRange: [45, 78],  // Only lines 45-78
  issue: "Potential security vulnerability"
}
```

### Context Compression Checklist

Before calling subagent:

- [ ] Remove redundant information
- [ ] Replace file contents with paths
- [ ] Use line ranges instead of full files
- [ ] Include only task-relevant data
- [ ] Estimate token count (<5k ideal)

---

## 3. Just-in-Time Context Loading

### Concept

Load context progressively in three tiers, starting with the least expensive.

### Three-Tier Loading Strategy

```typescript
// Tier 1: Overview (500 tokens)
async function getOverview(filePath: string) {
  // Get structure without content
  const symbols = await mcp__serena__get_symbols_overview(filePath)
  return symbols  // Just names, no bodies
}

// Tier 2: Targeted (2,000 tokens)
async function getSpecificSymbol(filePath: string, symbolName: string) {
  // Load only what's needed
  const symbol = await mcp__serena__find_symbol(
    symbolName,
    filePath,
    { include_body: true }
  )
  return symbol
}

// Tier 3: Full Read (5,000+ tokens - last resort)
async function getFullFile(filePath: string) {
  // Only for small files or when necessary
  if (await getFileSize(filePath) > 200) {
    throw new Error("File too large, use targeted approach")
  }
  return await readFile(filePath)
}
```

### Implementation Example

```typescript
async function analyzeFunction(
  filePath: string,
  functionName: string
): Promise<Analysis> {
  // Step 1: Get overview
  const overview = await getOverview(filePath)

  // Step 2: Check if function exists
  if (!overview.symbols.includes(functionName)) {
    return { error: "Function not found" }
  }

  // Step 3: Load only that function
  const functionDef = await getSpecificSymbol(filePath, functionName)

  // Step 4: Analyze (without loading entire file)
  return analyze(functionDef)
}

// Tokens used: ~2,500 instead of 10,000 (75% savings)
```

### Progressive Loading Flow Chart

```text
START
  ↓
Get Overview (Tier 1)
  ↓
Is target symbol identified?
  ├─ NO → Return error (no need to proceed)
  ├─ YES → Continue
  ↓
Load Specific Symbol (Tier 2)
  ↓
Is this sufficient for task?
  ├─ YES → Complete task (stop here)
  ├─ NO → Need more context
  ↓
Fallback to Full Read (Tier 3)
  ↓
Complete task
```

---

## 4. Token-Efficient Tools API

### Anthropic Official Feature

Released: February 2025
Beta Header: `token-efficient-tools-2025-02-19`

### Implementation

#### If Using Anthropic API Directly

```python
import anthropic

client = anthropic.Anthropic(api_key="...")

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": "..."}],
    # Add this header for token efficiency
    extra_headers={
        "anthropic-beta": "token-efficient-tools-2025-02-19"
    }
)
```

#### If Using Claude Code

Token-efficient tools are automatically enabled in Claude Code v2.1+. No configuration needed.

#### Verification

Check if feature is enabled:

```python
# In your agent code
import os

def check_token_efficient_tools():
    # Check environment or headers
    beta_features = os.environ.get("ANTHROPIC_BETA_FEATURES", "")
    if "token-efficient-tools" in beta_features:
        print("✅ Token-efficient tools enabled")
    else:
        print("⚠️  Token-efficient tools not enabled")
```

### Expected Savings

- Tool use requests: 10-20% reduction
- Tool responses: 5-10% reduction
- Overall: ~15% savings on tool-heavy workflows

---

## 5. Parallel Processing Management

### Problem

Claude Code can spawn 5+ parallel subagents automatically, causing:
- Rapid token consumption (5x overhead)
- Quota exhaustion
- Increased costs

### Solution

**Guideline**: Limit to 2-3 parallel subagents maximum

### Implementation

#### Pattern A: Sequential Processing (Default)

```typescript
// Execute subagents sequentially
const result1 = await subagent1.execute(task1)
const result2 = await subagent2.execute(task2)
const result3 = await subagent3.execute(task3)

// Total tokens: 3 × 15k = 45k
// Time: 6 minutes
```

#### Pattern B: Limited Parallelism (Approved)

```typescript
// Execute 2-3 subagents in parallel
const [result1, result2, result3] = await Promise.all([
  subagent1.execute(task1),
  subagent2.execute(task2),
  subagent3.execute(task3),
])

// Total tokens: 3 × 15k = 45k
// Time: 2 minutes (3x faster)
// ✅ Acceptable if tasks are independent
```

#### Pattern C: Excessive Parallelism (Prohibited)

```typescript
// ❌ DO NOT DO THIS
const tasks = Array.from({ length: 10 }, (_, i) => `task${i}`)
const results = await Promise.all(
  tasks.map(task => subagent.execute(task))
)

// Total tokens: 10 × 15k = 150k
// ❌ Token quota exceeded!
```

### Pre-Flight Checklist

Before spawning parallel subagents:

```typescript
function canSpawnParallel(tasks: Task[]): boolean {
  // 1. Check task count
  if (tasks.length > 3) {
    console.warn("Too many parallel tasks, execute sequentially")
    return false
  }

  // 2. Estimate tokens
  const estimatedTokens = tasks.length * 15000
  if (estimatedTokens > 60000) {
    console.warn("Estimated tokens too high:", estimatedTokens)
    return false
  }

  // 3. Check if tasks are truly independent
  const hasDependencies = tasks.some((t, i) =>
    tasks.slice(0, i).some(prev => t.dependsOn(prev))
  )
  if (hasDependencies) {
    console.warn("Tasks have dependencies, execute sequentially")
    return false
  }

  return true
}
```

---

## 6. Monitoring & Debugging

### Token Usage Logging

Add logging to track token consumption:

```typescript
class TokenTracker {
  private usage: Map<string, number> = new Map()

  log(subagent: string, tokens: number) {
    const current = this.usage.get(subagent) || 0
    this.usage.set(subagent, current + tokens)

    console.log(`[Token Usage] ${subagent}: +${tokens} (total: ${current + tokens})`)
  }

  report() {
    console.log("\n=== Token Usage Report ===")
    const sorted = Array.from(this.usage.entries())
      .sort((a, b) => b[1] - a[1])

    sorted.forEach(([name, tokens]) => {
      console.log(`${name}: ${tokens.toLocaleString()} tokens`)
    })

    const total = Array.from(this.usage.values()).reduce((a, b) => a + b, 0)
    console.log(`\nTotal: ${total.toLocaleString()} tokens`)
  }
}

// Usage
const tracker = new TokenTracker()

const result = await subagent.execute(task)
tracker.log("api-reviewer", 8500)

// At end of session
tracker.report()
```

### Output Example

```text
[Token Usage] api-reviewer: +8500 (total: 8500)
[Token Usage] test-generator: +12000 (total: 12000)
[Token Usage] api-reviewer: +3200 (total: 11700)

=== Token Usage Report ===
test-generator: 12,000 tokens
api-reviewer: 11,700 tokens

Total: 23,700 tokens
```

### Debug Mode

Add verbose logging for optimization debugging:

```typescript
const DEBUG_TOKENS = process.env.DEBUG_TOKENS === "true"

function debugLog(message: string, tokenCount?: number) {
  if (DEBUG_TOKENS) {
    const timestamp = new Date().toISOString()
    const tokens = tokenCount ? ` [${tokenCount} tokens]` : ""
    console.log(`[${timestamp}]${tokens} ${message}`)
  }
}

// Usage
debugLog("Starting API review", 0)
const analysis = await performAnalysis()
debugLog("Analysis complete", 8500)
```

---

## Testing Token Optimization

### Unit Test Example

```typescript
import { describe, it, expect } from "vitest"

describe("Token Optimization", () => {
  it("should use Markdown Shared Memory for large results", async () => {
    const result = await subagent.execute(largeTask)

    // Check that result is a summary, not full content
    expect(result.length).toBeLessThan(500)  // Summary should be <500 chars

    // Check that report was saved
    expect(result).toContain(".claude/reports/")

    // Verify report exists
    const reportPath = extractReportPath(result)
    const reportExists = await fileExists(reportPath)
    expect(reportExists).toBe(true)
  })

  it("should pass file paths, not contents", async () => {
    const spy = vi.spyOn(subagent, "execute")

    await mainAgent.delegateTask(task)

    // Check that context contains paths, not contents
    const context = spy.mock.calls[0][0]
    expect(context).toHaveProperty("filePaths")
    expect(context).not.toHaveProperty("fileContents")
  })

  it("should use Just-in-Time loading", async () => {
    const overviewSpy = vi.spyOn(mcp, "get_symbols_overview")
    const findSymbolSpy = vi.spyOn(mcp, "find_symbol")
    const readFileSpy = vi.spyOn(fs, "readFile")

    await subagent.analyze("MyClass", "src/file.ts")

    // Should call overview first
    expect(overviewSpy).toHaveBeenCalledOnce()

    // Should call find_symbol for specific symbol
    expect(findSymbolSpy).toHaveBeenCalledWith("MyClass", "src/file.ts")

    // Should NOT read full file
    expect(readFileSpy).not.toHaveBeenCalled()
  })
})
```

---

## Common Pitfalls

### Pitfall 1: Forgetting to Save Reports

**Problem**:
```typescript
// Subagent returns full 10,000 token analysis
return fullAnalysis
```

**Solution**:
```typescript
// Save to file, return summary
await saveReport(reportPath, fullAnalysis)
return createSummary(fullAnalysis, reportPath)
```

### Pitfall 2: Reading Reports Unnecessarily

**Problem**:
```typescript
// Main agent always reads reports
const summary = await subagent.execute(task)
const report = await readFile(extractReportPath(summary))  // Wasteful!
return summary + report
```

**Solution**:
```typescript
// Only read if user asks
const summary = await subagent.execute(task)
if (userWantsDetails) {
  const report = await readFile(extractReportPath(summary))
  return report
}
return summary
```

### Pitfall 3: Over-Parallelization

**Problem**:
```typescript
// Spawning too many subagents
const tasks = files.map(file => subagent.analyze(file))
await Promise.all(tasks)  // 100 parallel subagents!
```

**Solution**:
```typescript
// Batch processing with limit
const PARALLEL_LIMIT = 3
for (let i = 0; i < files.length; i += PARALLEL_LIMIT) {
  const batch = files.slice(i, i + PARALLEL_LIMIT)
  await Promise.all(batch.map(file => subagent.analyze(file)))
}
```

### Pitfall 4: Not Using serena MCP Tools

**Problem**:
```typescript
// Reading entire file when only need one function
const fileContent = await readFile("large_file.ts")  // 10,000 tokens
const func = extractFunction(fileContent, "myFunction")
```

**Solution**:
```typescript
// Use serena to load only the function
const func = await mcp__serena__find_symbol(
  "myFunction",
  "large_file.ts",
  { include_body: true }
)  // 500 tokens
```

### Pitfall 5: Ignoring Token Budgets

**Problem**:
```typescript
// No token estimation
await subagent.execute(veryLargeTask)  // How many tokens?
```

**Solution**:
```typescript
// Estimate and validate
const estimatedTokens = estimateTokens(task)
if (estimatedTokens > 30000) {
  throw new Error(`Task too large: ${estimatedTokens} tokens (max: 30,000)`)
}
await subagent.execute(task)
```

---

## Appendix: Token Estimation

### Rough Token Estimates

```typescript
function estimateTokens(text: string): number {
  // Rough estimate: 1 token ≈ 4 characters
  return Math.ceil(text.length / 4)
}

function estimateFileTokens(filePath: string): number {
  const stats = fs.statSync(filePath)
  const bytes = stats.size
  // 1 token ≈ 4 bytes (for code)
  return Math.ceil(bytes / 4)
}

function estimateContextTokens(context: any): number {
  const json = JSON.stringify(context)
  return estimateTokens(json)
}
```

### Usage

```typescript
const context = { filePaths: [...], task: "..." }
const tokens = estimateContextTokens(context)

if (tokens > 5000) {
  console.warn(`Large context: ${tokens} tokens`)
}
```

---

## Summary Checklist

Before releasing a subagent template:

- [ ] Returns summaries <500 tokens
- [ ] Saves detailed reports to `.claude/reports/`
- [ ] Uses file paths instead of contents
- [ ] Implements Just-in-Time loading
- [ ] Limits parallel execution to 3
- [ ] Includes token usage logging
- [ ] Has token budget validation
- [ ] Tested with large inputs
- [ ] Documentation includes token estimates
- [ ] Reviewed for common pitfalls

---

## Resources

- [Anthropic Token-Efficient Tools](https://docs.claude.com/en/docs/agents-and-tools/tool-use/token-efficient-tool-use)
- [Claude Code Best Practices](https://docs.claude.com/en/docs/claude-code)
- [Community Token Optimization Patterns](https://medium.com/@sampan090611/experiences-on-claude-codes-subagent-and-little-tips-for-using-claude-code-c4759cd375a7)
- [Example Report Template](../examples/reports/EXAMPLE_api-review-20251031-143022.md)

---

**Questions or Issues?**

Open an issue on GitHub: https://github.com/SawanoLab/adaptive-claude-agents/issues
