# Best Practices & Resources

This document outlines the best practices followed in the Adaptive Claude Agents project and provides references to official resources.

## Table of Contents

- [Anthropic Best Practices](#anthropic-best-practices)
- [serena MCP Integration](#serena-mcp-integration)
- [Template Development](#template-development)
- [Skills Development](#skills-development)
- [Project-Specific Patterns](#project-specific-patterns)
- [Official Resources](#official-resources)
- [Community Resources](#community-resources)

---

## Anthropic Best Practices

### Progressive Disclosure

**Principle**: Don't overwhelm users with information. Reveal details incrementally.

**Bad Example**:

```
Analyzing project...
Found: package.json, tsconfig.json, next.config.js, tailwind.config.js,
vitest.config.ts, .eslintrc, .prettierrc, postcss.config.js

Dependencies: next@14.0.0, react@18.2.0, typescript@5.3.0,
tailwindcss@3.4.0, vitest@1.0.0, @testing-library/react@14.0.0,
zustand@4.4.0, axios@1.6.0, ...

Generate these subagents?
- nextjs-tester (uses Vitest + Testing Library)
- component-reviewer (checks React best practices)
- type-checker (TypeScript strict mode)
- api-handler (axios integration)
- state-manager (zustand patterns)
...
```

**Good Example**:

```
Detected: Next.js 14 + TypeScript

Generate core subagents? [Y/n]
  ✓ nextjs-tester
  ✓ component-reviewer

→ Y

Also add optional agents? [Y/n]
  • type-checker (strict TypeScript)
  • api-handler (axios patterns)

→ n

Created 2 subagents in .claude/agents/
```

**Implementation**:

```python
# In detection logic
def present_findings(detection: dict, verbose: bool = False):
    # Always show framework
    print(f"Detected: {detection['framework']}")

    # Progressive confirmation
    if confirm("Generate core subagents?"):
        generate_core_agents(detection)

        if verbose and has_optional_tools(detection):
            if confirm("Also add optional agents?"):
                generate_optional_agents(detection)
```

### Tool Selection

**Principle**: Choose the right tool for each task.

#### File Operations

```yaml
Read:
  use_for: "Reading existing files"
  example: "Read package.json to detect dependencies"

Write:
  use_for: "Creating new files"
  example: "Generate new subagent template"

Edit:
  use_for: "Modifying specific parts of files"
  example: "Update dependency version in package.json"
```

#### Code Operations (via serena MCP)

```yaml
mcp__serena__find_symbol:
  use_for: "Locating classes, functions, methods"
  example: "Find the ApiClient class definition"

mcp__serena__replace_symbol_body:
  use_for: "Editing specific functions or classes"
  example: "Update the analyze_project function"

mcp__serena__get_symbols_overview:
  use_for: "Understanding file structure without reading all code"
  example: "See all exported functions in a module"

mcp__serena__search_for_pattern:
  use_for: "Finding code patterns across files"
  example: "Find all API endpoint definitions"

mcp__serena__find_referencing_symbols:
  use_for: "Understanding dependencies"
  example: "Find all usages of a utility function"
```

#### System Operations

```yaml
Bash:
  use_for: "Running commands (use sparingly)"
  examples:
    - "npm install"
    - "pytest tests/"
  avoid:
    - "cat file.txt"  # Use Read instead
    - "echo 'text' > file"  # Use Write instead
```

### Context Management

**Principle**: Be efficient with context window. Only read what you need.

**Bad Example**:

```python
# Reading entire large file
def analyze_api_routes(project_path):
    # This reads all 5000 lines
    content = read_file(f"{project_path}/app/api.py")

    # Only using a small part
    if "FastAPI" in content:
        return "fastapi"
```

**Good Example**:

```python
# Using serena MCP for targeted analysis
def analyze_api_routes(project_path):
    # Only searches for the pattern, doesn't load full file
    matches = mcp__serena__search_for_pattern(
        "from fastapi import",
        path=project_path,
        output_mode="files_with_matches"
    )

    if matches:
        return "fastapi"
```

**Implementation Tips**:

1. **Use file overviews first**:

   ```python
   # Get structure without reading full content
   overview = mcp__serena__get_symbols_overview("large_file.py")
   # Only read specific symbols you need
   symbol = mcp__serena__find_symbol("ClassName", "large_file.py", include_body=True)
   ```

2. **Search before reading**:

   ```python
   # Find relevant files first
   files = mcp__serena__find_file("*config*.json", project_path)
   # Then read only those
   for file in files[:5]:  # Limit results
       content = read_file(file)
   ```

3. **Cache results**:

   ```python
   from functools import lru_cache

   @lru_cache(maxsize=128)
   def expensive_analysis(project_path: str) -> dict:
       # Results cached by project_path
       pass
   ```

### Error Handling

**Principle**: Provide actionable, user-friendly error messages.

**Bad Example**:

```python
if not package_json_exists:
    raise Exception("Error: package.json not found")
```

**Good Example**:

```python
if not package_json_exists:
    raise FileNotFoundError(
        "package.json not found.\n\n"
        "This doesn't appear to be a Node.js project.\n\n"
        "Solutions:\n"
        "  1. Create package.json: `npm init`\n"
        "  2. Navigate to project root: `cd /path/to/project`\n"
        "  3. Use a different template for your tech stack\n"
    )
```

**Pattern**:

```python
class UserFriendlyError(Exception):
    """Base class for user-facing errors"""
    def __init__(self, message: str, solutions: list[str]):
        self.message = message
        self.solutions = solutions
        super().__init__(self.format_message())

    def format_message(self) -> str:
        msg = f"{self.message}\n\nSolutions:\n"
        for i, solution in enumerate(self.solutions, 1):
            msg += f"  {i}. {solution}\n"
        return msg
```

---

## serena MCP Integration

### Why serena MCP?

serena MCP provides **symbolic code operations** that are more efficient than text-based file operations:

- **Precision**: Edit specific functions without affecting the rest
- **Efficiency**: Find symbols without reading entire files
- **Safety**: Type-aware operations reduce errors

### When to Use serena MCP

**Use serena MCP for**:

- Finding classes, functions, or methods by name
- Editing specific code symbols
- Understanding code structure
- Searching for code patterns
- Tracking symbol references

**Don't use serena MCP for**:

- Reading/writing configuration files (JSON, YAML, etc.)
- Creating new files from scratch
- Binary file operations
- Operations on non-code files

### Common Patterns

#### Pattern 1: Analyzing Code Structure

```python
# Get high-level overview
overview = mcp__serena__get_symbols_overview("api.py")
# Returns: classes, functions, imports without full code

# Then drill down to specific symbols
if "ApiClient" in [s.name for s in overview.symbols]:
    client = mcp__serena__find_symbol(
        "ApiClient",
        "api.py",
        depth=1,  # Include methods
        include_body=True
    )
```

#### Pattern 2: Finding and Editing Code

```python
# Find all test files
test_files = mcp__serena__find_file("*test*.py", "tests/")

# Find specific test function
test_fn = mcp__serena__find_symbol(
    "test_api_endpoint",
    test_files[0],
    include_body=True
)

# Edit it
mcp__serena__replace_symbol_body(
    "test_api_endpoint",
    test_files[0],
    new_body=updated_test_code
)
```

#### Pattern 3: Understanding Dependencies

```python
# Find a function
symbol = mcp__serena__find_symbol("process_data", "utils.py")

# Find everywhere it's used
references = mcp__serena__find_referencing_symbols(
    "process_data",
    "utils.py"
)

# Update all usages if needed
for ref in references:
    # ... update logic
```

### Configuration

serena MCP configuration is **gitignored** (project-specific):

```bash
# .gitignore includes:
.serena/
.mcp/
mcp_config.json
```

**Setup** (not committed to repo):

```json
// mcp_config.json (local only)
{
  "mcpServers": {
    "serena": {
      "command": "npx",
      "args": ["-y", "@serenaai/serena-mcp"],
      "env": {
        "SERENA_PROJECT_PATH": "/path/to/adaptive-claude-agents"
      }
    }
  }
}
```

---

## Template Development

### Template Structure

Every subagent template follows this structure:

```yaml
---
name: [stack]-[role]
description: One-line purpose description
tools: [List of tools needed]
---

# Role Definition
Clear statement of what this agent does

## Responsibilities
Specific tasks this agent handles

## Best Practices
Framework-specific guidelines

## Workflow
Step-by-step process

## Examples
Concrete usage examples

## References
Official docs and resources
```

### Tool Selection for Templates

**Testing Agents**:

```yaml
tools: [Read, Write, Bash]
# Read: Analyze test patterns
# Write: Create new tests
# Bash: Run test commands
```

**Review Agents**:

```yaml
tools: [Read, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols]
# Read: Check configuration files
# find_symbol: Locate code to review
# find_referencing_symbols: Check usage patterns
```

**Generation Agents**:

```yaml
tools: [Read, Write, Edit, mcp__serena__insert_after_symbol]
# Read: Understand project patterns
# Write: Create new files
# Edit: Modify existing files
# insert_after_symbol: Add code to specific locations
```

### Template Examples

See existing templates:

- `templates/nextjs/` - Next.js examples
- `templates/fastapi/` - FastAPI examples (when implemented)

---

## Skills Development

### Skill Structure

```markdown
---
name: skill-name
description: What this skill does
---

Instructions for Claude on how to use this skill.

Can reference Python scripts in the same directory:
- analyze.py
- generate.py
- utils.py
```

### Testing Skills

1. **Create test project**:

   ```bash
   mkdir test-nextjs-app
   cd test-nextjs-app
   npx create-next-app@latest . --typescript --tailwind
   ```

2. **Invoke skill manually**:

   ```bash
   # Via Claude Code interface
   # Or via direct script execution
   python skills/project-analyzer/analyze_project.py .
   ```

3. **Verify output**:
   - Check generated subagents
   - Validate detection accuracy
   - Test error handling

### Skills Best Practices

See the `skills-developer` subagent for comprehensive guidelines.

---

## Project-Specific Patterns

### Detection Logic Pattern

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DetectionResult:
    framework: str
    confidence: float  # 0.0 to 1.0
    indicators: List[str]
    tools: dict
    recommended_subagents: List[str]

def detect_stack(project_path: str) -> Optional[DetectionResult]:
    # 1. Quick file checks
    if not has_config_file(project_path):
        return None

    # 2. Analyze config
    config = parse_config(project_path)

    # 3. Calculate confidence
    confidence = calculate_confidence(config)

    # 4. Return structured result
    return DetectionResult(
        framework="nextjs",
        confidence=confidence,
        indicators=[...],
        tools={...},
        recommended_subagents=[...]
    )
```

### Confirmation Pattern

```python
def confirm(message: str, default: bool = False) -> bool:
    """
    Ask user for confirmation with clear default.

    Args:
        message: Question to ask
        default: Default choice if user presses enter

    Returns:
        True if user confirms, False otherwise
    """
    suffix = " [Y/n]" if default else " [y/N]"
    response = input(message + suffix).strip().lower()

    if not response:
        return default

    return response in ('y', 'yes')
```

### Logging Pattern

```python
import logging
from pathlib import Path

def setup_logging(project_path: Path) -> None:
    """Setup logging for detection process"""
    log_file = project_path / ".claude" / "detection.log"
    log_file.parent.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also print to console
        ]
    )

# Usage
logger = logging.getLogger(__name__)
logger.info(f"Detected framework: {framework}")
logger.debug(f"Confidence calculation: {indicators}")
```

---

## Official Resources

### Anthropic Documentation

**Core Resources**:

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
  - Overview of Claude Code features
  - Subagent system explanation
  - Best practices for IDE integration

- [Agent Skills Guide](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
  - Official Skills announcement
  - Design philosophy
  - Real-world examples

- [Tool Use Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
  - How to design tools
  - Tool selection guidelines
  - Common patterns

- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
  - Writing effective prompts
  - Progressive disclosure pattern
  - Context optimization

**Advanced Topics**:

- [Subagent Best Practices](https://docs.claude.com/en/docs/claude-code/subagents)
  - Creating effective subagents
  - Task decomposition
  - Error handling

- [Extended Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
  - When to use extended thinking
  - Performance implications

### Sample Skills & Templates

**Official Examples**:

- [Anthropic Quickstarts - Skills](https://github.com/anthropics/anthropic-quickstarts/tree/main/skills)
  - Official skill examples
  - Reference implementations
  - Testing patterns

**Where to find inspiration**:

- Browse official quickstarts repository
- Analyze structure and patterns
- Adapt for this project's needs

---

## Community Resources

### Related Projects

**claude-init** by @dimitritholen:

- [Repository](https://github.com/dimitritholen/claude-init)
- **Use case**: Initial project setup
- **Learn from**: Template generation approach
- **Difference**: One-time vs continuous (our approach)

**awesome-claude-code-subagents** by @VoltAgent:

- [Repository](https://github.com/VoltAgent/awesome-claude-code-subagents)
- **Use case**: Community template collection
- **Learn from**: Diverse template examples
- **Opportunity**: Contribute our templates back

### Learning Resources

**Blogs & Articles**:

- [Anthropic Blog](https://www.anthropic.com/blog)
- Search for "Skills" or "Claude Code" articles
- Read user experiences and case studies

**Community Discussions**:

- [r/ClaudeAI Reddit](https://www.reddit.com/r/ClaudeAI/)
- Claude Code Discord (if available)
- GitHub Discussions on related projects

---

## Continuous Improvement

### Stay Updated

1. **Follow Anthropic announcements**:
   - Subscribe to Anthropic blog
   - Watch for Claude Code updates
   - Check docs regularly

2. **Monitor community**:
   - Track related GitHub repos
   - Participate in discussions
   - Share learnings

3. **Iterate on patterns**:
   - Collect user feedback
   - Analyze what works
   - Update this document

### Contributing to Best Practices

Found a better pattern? Update this document:

1. Test your approach
2. Document it clearly
3. Submit PR with rationale
4. Discuss with maintainers

---

## Questions?

- **Unclear practice?**: Open a [GitHub Discussion](https://github.com/SawanoLab/adaptive-claude-agents/discussions)
- **Found a better way?**: Submit a PR to update this doc
- **Need clarification?**: Create an [Issue](https://github.com/SawanoLab/adaptive-claude-agents/issues)

---

## Tool Access Policy (2025)

### Principle: Least Privilege

Grant only the minimum set of tools required for each subagent's role. This improves security, performance, and clarity of responsibility.

### Tool Access by Agent Role

#### Browser Testing Agents

**chrome-devtools-tester**:
```yaml
tools: [mcp__chrome-devtools__*]
rationale: Chrome DevTools Protocol for performance & debugging
scope: Read-only browser inspection, performance traces
```

**playwright-tester**:
```yaml
tools: [mcp__playwright__*, Read, Write, Edit, Bash]
rationale: Cross-browser E2E automation & test generation
scope: Browser automation, test file creation, test execution
```

#### Developer Agents

**[framework]-developer** (e.g., nextjs-developer, fastapi-developer):
```yaml
tools: [Read, Write, Edit, mcp__serena__replace_symbol_body, mcp__serena__insert_after_symbol]
rationale: Code generation and modification
scope: Create/modify code files, use symbol-level edits
```

#### Tester Agents

**[framework]-tester** (e.g., nextjs-tester, api-tester):
```yaml
tools: [Read, Write, Bash]
rationale: Test creation and execution
scope: Read code, write tests, run test commands
```

#### Specialist Agents

**[domain]-specialist** (e.g., sqlalchemy-specialist, cv-specialist):
```yaml
tools: [Read, mcp__serena__find_symbol, mcp__serena__get_symbols_overview]
rationale: Deep analysis and recommendations
scope: Read code structure, provide guidance (no modifications)
```

#### Reviewer/Analyst Agents

**[framework]-reviewer**:
```yaml
tools: [Read, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols]
rationale: Code review and quality analysis
scope: Read-only, understand dependencies
```

### Tool Selection Decision Tree

```
Need to modify code?
├─ Yes → Write/Edit + serena edit tools
└─ No → Read-only tools

Need browser interaction?
├─ Chrome only → mcp__chrome-devtools__*
└─ Cross-browser → mcp__playwright__*

Need code analysis?
├─ Symbol-level → serena find/overview
└─ Text-level → Read + grep patterns

Need execution?
├─ Tests → Bash (test commands only)
├─ Build → Bash (build commands only)
└─ General → Avoid if possible
```

### Security Considerations

**Never grant**:
- Write access to read-only agents
- Bash access without clear justification
- All tools by default (be explicit)

**Always document**:
- Why each tool is needed
- What scope it will be used for
- Security implications if any

### Example: Secure Template

```yaml
---
name: code-reviewer
description: Security-focused code review specialist
tools: [Read, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols]
# Explicitly NO Write/Edit - review only
---

You are a **read-only code reviewer**. You MUST NOT modify code.

## Tool Restrictions

✅ Allowed:
- Read files
- Find symbols
- Analyze dependencies

❌ Forbidden:
- Write/Edit files
- Execute commands
- Modify codebase

If code changes are needed, report findings and recommend to user.
```

---

## Web Service Testing Patterns (2025)

### Auto-Workflow for UI + API Testing

When users request both UI and API testing (e.g., "クリックしてAPIアクセスを検証"), automatically decompose into specialized workflows.

**Pattern Recognition**:
```
User: "ログインボタンをクリックしてAPIアクセスを検証して"

Analysis:
- UI keywords: "ボタン", "クリック"
- API keywords: "API", "アクセス"
→ Sequential workflow: Browser → API
```

**Execution**:
```
1. chrome-devtools-tester (or playwright-tester):
   - Verify button CSS/position
   - Execute click event
   - Monitor network requests
   - Capture: POST /api/auth/login

2. api-tester (auto-chained):
   - Test endpoint independently
   - Validate request/response
   - Check error handling

3. main-agent:
   - Synthesize results
   - Report comprehensive validation
```

**Delegation Announcement**:
```
User: "登録フォームの見た目とAPIを検証"

Agent: "I'll validate the UI with Chrome DevTools, then test the API endpoint. Starting browser testing..."
[Automatically delegates without asking permission]

chrome-devtools-tester:
✓ Form elements validated
✓ CSS styles confirmed
✓ Network request captured: POST /api/users/register

api-tester (auto-chained):
✓ Endpoint tested independently
✓ Response validated
✓ Error scenarios checked

Agent: "Validation complete: UI and API both working correctly ✓"
```

### Browser Automation Selection Logic

**Default: Chrome DevTools** (90% of cases)
```
User mentions: "性能", "パフォーマンス", "デバッグ", "Chrome"
→ chrome-devtools-tester

User mentions: "見た目", "CSS", "クリック", "ボタン" (no cross-browser)
→ chrome-devtools-tester
```

**Escalate to Playwright** (only when needed)
```
User mentions: "Firefox", "Safari", "クロスブラウザ", "CI"
→ playwright-tester

User mentions: "E2E", "end-to-end", "統合テスト", "パイプライン"
→ playwright-tester
```

**Proactive Suggestion**:
```
User: "ボタンのテストをして"

Agent: "For Chrome-only testing, I'll use chrome-devtools-tester for optimal performance. If you need cross-browser testing (Firefox/Safari), I can use playwright-tester instead. Proceeding with Chrome DevTools..."
```

---

## 2025 Framework Best Practices

See [2025_BEST_PRACTICES.md](2025_BEST_PRACTICES.md) for comprehensive framework-specific guidance including:

- Browser automation (Chrome DevTools vs Playwright)
- Next.js 15 (Turbopack, App Router, ISR)
- FastAPI (Async-first patterns)
- Go frameworks (Gin vs Fiber vs Echo)
- Flutter state management (Riverpod recommended)
- Python ML/CV (PyTorch vs TensorFlow)
- iOS Swift (SwiftUI vs UIKit hybrid)
- React state management (Zustand recommended)

---

**Last Updated**: 2025-10-20
**Next Review**: When major Claude Code update is released or significant pattern changes emerge
