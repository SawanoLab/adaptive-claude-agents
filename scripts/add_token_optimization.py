#!/usr/bin/env python3
"""
Add Token Optimization Guidelines section to all subagent templates.

This script inserts a standard Token Optimization section before the final
section of each template file.
"""

import re
from pathlib import Path
from typing import List

# Token optimization section to add
TOKEN_OPTIMIZATION_SECTION = """
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
"""


def find_template_files(base_dir: Path) -> List[Path]:
    """Find all template markdown files."""
    template_files = []
    for md_file in base_dir.rglob("*.md"):
        # Skip the common section file itself
        if md_file.name == "_token_optimization_section.md":
            continue
        # Skip files in docs, examples, etc.
        if any(part in md_file.parts for part in ["docs", "examples", ".git", "scripts"]):
            continue
        template_files.append(md_file)
    return sorted(template_files)


def has_token_optimization_section(content: str) -> bool:
    """Check if file already has Token Optimization section."""
    return "## 🎯 Token Optimization Guidelines" in content or \
           "Token Optimization Guidelines" in content


def add_token_optimization(file_path: Path, dry_run: bool = False) -> bool:
    """Add token optimization section to a template file."""
    try:
        rel_path = file_path.relative_to(Path.cwd())
    except ValueError:
        rel_path = file_path
    print(f"Processing: {rel_path}")

    content = file_path.read_text(encoding="utf-8")

    # Check if already has the section
    if has_token_optimization_section(content):
        print(f"  ⏭️  Already has Token Optimization section, skipping")
        return False

    # Find the best insertion point (before the last ## section or at the end)
    lines = content.split("\n")

    # Find last ## heading (not ###)
    last_heading_idx = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("## ") and not lines[i].startswith("###"):
            last_heading_idx = i
            break

    if last_heading_idx is not None:
        # Insert before the last section
        lines.insert(last_heading_idx, TOKEN_OPTIMIZATION_SECTION.rstrip())
        updated_content = "\n".join(lines)
    else:
        # Append at the end
        if not content.endswith("\n\n"):
            content = content.rstrip() + "\n\n"
        updated_content = content + TOKEN_OPTIMIZATION_SECTION

    if not dry_run:
        file_path.write_text(updated_content, encoding="utf-8")
        print(f"  ✅ Added Token Optimization section")
    else:
        print(f"  🔍 Would add Token Optimization section")

    return True


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Add Token Optimization Guidelines to all template files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=Path("templates"),
        help="Templates directory (default: templates/)"
    )

    args = parser.parse_args()

    templates_dir = Path(args.templates_dir)
    if not templates_dir.exists():
        print(f"❌ Error: Templates directory not found: {templates_dir}")
        return 1

    print(f"🔍 Finding template files in {templates_dir}...")
    template_files = find_template_files(templates_dir)

    if not template_files:
        print("❌ No template files found")
        return 1

    print(f"📝 Found {len(template_files)} template files\n")

    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified\n")

    modified_count = 0
    skipped_count = 0

    for template_file in template_files:
        if add_token_optimization(template_file, dry_run=args.dry_run):
            modified_count += 1
        else:
            skipped_count += 1
        print()  # Blank line between files

    print("=" * 60)
    print(f"✅ Modified: {modified_count} files")
    print(f"⏭️  Skipped: {skipped_count} files")
    print(f"📊 Total: {len(template_files)} files")

    if args.dry_run:
        print("\n💡 Run without --dry-run to apply changes")

    return 0


if __name__ == "__main__":
    exit(main())
