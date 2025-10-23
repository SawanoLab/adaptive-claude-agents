#!/usr/bin/env python3
"""
Main entry point for project analysis and subagent generation.

This script:
1. Detects tech stack using detect_stack.py
2. Confirms with user (Progressive Disclosure)
3. Generates appropriate subagents from templates

Usage:
    # Initial generation
    python analyze_project.py /path/to/project
    python analyze_project.py /path/to/project --auto  # Skip confirmation

    # Update existing subagents (preserves customizations)
    python analyze_project.py /path/to/project --update-only

    # Add new templates while preserving existing
    python analyze_project.py /path/to/project --merge

    # Complete regeneration (overwrites all)
    python analyze_project.py /path/to/project --force

Dependencies:
    - Python 3.9+
    - detect_stack.py (in same directory)
"""

import argparse
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# Import detection logic
from detect_stack import detect_tech_stack, DetectionResult
from detect_phase import detect_phase, PhaseResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProjectAnalyzer:
    """
    Main project analyzer class.

    Orchestrates detection, confirmation, and generation.
    """

    def __init__(self, project_path: Path, auto_confirm: bool = False,
                 update_mode: str = "generate"):
        """
        Initialize analyzer.

        Args:
            project_path: Path to project root
            auto_confirm: If True, skip user confirmation
            update_mode: One of "generate", "update-only", "merge", "force"
        """
        self.project_path = Path(project_path).resolve()
        self.auto_confirm = auto_confirm
        self.update_mode = update_mode
        self.agents_dir = self.project_path / ".claude" / "agents"

        logger.info(f"Analyzing project: {self.project_path}")
        logger.info(f"Update mode: {self.update_mode}")

    def analyze(self) -> bool:
        """
        Run full analysis workflow.

        Returns:
            True if successful, False otherwise
        """
        # Step 1: Detect tech stack
        print("\n🔍 Analyzing project structure...")
        detection = detect_tech_stack(str(self.project_path))

        if not detection:
            print("\n❌ Could not detect tech stack")
            print("\nOptions:")
            print("  1. Manually specify stack in .claude/project.yml")
            print("  2. Use generic templates")
            print("  3. Open an issue at https://github.com/SawanoLab/adaptive-claude-agents/issues")
            return False

        # Step 1.5: Detect development phase
        print("\n🎯 Detecting development phase...")
        phase_result = detect_phase(str(self.project_path))

        # Step 2: Display results
        self._display_detection(detection, phase_result)

        # Step 3: Confirm with user (Progressive Disclosure)
        if not self.auto_confirm:
            if not self._confirm_generation(detection):
                print("\n❌ Aborted by user")
                return False

        # Step 4: Generate subagents
        print("\n📝 Generating subagents...")
        success = self._generate_subagents(detection, phase_result)

        if success:
            print("\n✅ Successfully generated subagents!")
            print(f"\n📁 Location: {self.agents_dir}")
            print("\n📖 Usage Guide: .claude/agents/SUBAGENT_GUIDE.md")
            print("\n💡 Next steps:")
            print("  1. Read SUBAGENT_GUIDE.md for auto-trigger keywords")
            print("  2. Review generated agents: ls .claude/agents/")
            print("  3. Start using: Just ask Claude naturally - subagents auto-trigger!")
            print("  4. Commit to version control")
            return True
        else:
            print("\n❌ Failed to generate subagents")
            return False

    def _display_detection(self, detection: DetectionResult, phase_result: PhaseResult):
        """Display detection results to user."""
        print("\n" + "━" * 60)
        print("Detected Tech Stack")
        print("━" * 60)
        print(f"Framework:     {detection.framework.upper()}")
        if detection.version:
            print(f"Version:       {detection.version}")
        print(f"Language:      {detection.language.capitalize()}")

        if detection.tools:
            print("\nTools:")
            for category, tools in detection.tools.items():
                print(f"  {category.capitalize():12} {', '.join(tools)}")

        print(f"\nConfidence:    {detection.confidence * 100:.0f}%")

        # Show detection reasoning
        if detection.indicators:
            print("\nDetection Reasoning:")
            for indicator in detection.indicators:
                print(f"  • {indicator}")

        # Show development phase
        print(f"\n📊 Development Phase")
        print(f"  Phase:         {phase_result.phase.upper()}")
        print(f"  Review Rigor:  {phase_result.rigor}/10")
        print(f"  Description:   {phase_result.description}")
        print(f"  Confidence:    {phase_result.confidence:.0%}")

        print("━" * 60)

    def _confirm_generation(self, detection: DetectionResult) -> bool:
        """
        Confirm subagent generation with user.

        Args:
            detection: Detection results

        Returns:
            True if user confirms, False otherwise
        """
        print("\nGenerate these subagents? [Y/n]")
        for agent in detection.recommended_subagents:
            description = self._get_agent_description(agent)
            print(f"  ✓ {agent:30} {description}")

        response = input("\n> ").strip().lower()
        return response in ('', 'y', 'yes')

    def _get_agent_description(self, agent_name: str) -> str:
        """Get short description for subagent."""
        descriptions = {
            "nextjs-tester": "(Testing specialist)",
            "component-reviewer": "(Component best practices)",
            "type-checker": "(TypeScript strict mode)",
            "app-router-specialist": "(App Router patterns)",
            "fastapi-tester": "(pytest + TestClient)",
            "api-reviewer": "(REST API best practices)",
            "async-checker": "(async/await patterns)",
            "go-tester": "(go test specialist)",
            "go-reviewer": "(Go idioms)",
            "concurrency-checker": "(Goroutines & channels)",
        }
        return descriptions.get(agent_name, "")

    def _backup_existing_agents(self) -> Optional[Path]:
        """
        Create timestamped backup of existing .claude/agents directory.

        Returns:
            Path to backup directory, or None if no backup needed
        """
        if not self.agents_dir.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = self.project_path / ".claude" / f"agents.backup.{timestamp}"

        try:
            shutil.copytree(self.agents_dir, backup_dir)
            print(f"\n📦 Backup created: {backup_dir.relative_to(self.project_path)}")
            return backup_dir
        except Exception as e:
            logger.warning(f"Failed to create backup: {e}")
            return None

    def _get_existing_agents(self) -> List[str]:
        """
        Get list of existing subagent files.

        Returns:
            List of agent filenames (without .md extension)
        """
        if not self.agents_dir.exists():
            return []

        return [
            f.stem for f in self.agents_dir.glob("*.md")
            if f.name != "SUBAGENT_GUIDE.md"
        ]

    def _generate_subagents(self, detection: DetectionResult, phase_result: PhaseResult) -> bool:
        """
        Generate subagent files from templates.

        Args:
            detection: Detection results
            phase_result: Phase detection results

        Returns:
            True if successful, False otherwise
        """
        # Handle update modes
        existing_agents = self._get_existing_agents()

        if self.update_mode == "update-only" and not existing_agents:
            print("\n⚠️  No existing agents found. Use without --update-only to generate new agents.")
            return False

        # Create backup for merge and force modes
        if self.update_mode in ["merge", "force"] and existing_agents:
            self._backup_existing_agents()

        # Ensure .claude/agents/ directory exists
        self.agents_dir.mkdir(parents=True, exist_ok=True)

        # Get templates directory
        templates_dir = Path(__file__).parent.parent.parent / "templates" / detection.framework

        if not templates_dir.exists():
            logger.warning(f"Templates not found for {detection.framework}")
            print(f"\n⚠️  Templates not yet available for {detection.framework}")
            print(f"   Template directory: {templates_dir}")
            print("\n💡 You can:")
            print("  1. Create templates manually in templates/{detection.framework}/")
            print("  2. Use template-generator subagent")
            print("  3. Contribute templates to the project!")
            return False

        # Copy/generate templates
        generated_count = 0
        updated_count = 0
        skipped_count = 0

        for agent_name in detection.recommended_subagents:
            output_file = self.agents_dir / f"{agent_name}.md"

            # Check if file exists for update-only mode
            if self.update_mode == "update-only" and agent_name not in existing_agents:
                logger.debug(f"Skipping new agent in update-only mode: {agent_name}")
                skipped_count += 1
                continue

            # Skip existing files in merge mode (preserve customizations)
            if self.update_mode == "merge" and output_file.exists():
                logger.debug(f"Preserving existing agent: {agent_name}")
                skipped_count += 1
                continue

            # Direct template file mapping (exact match first)
            template_file = templates_dir / f"{agent_name}.md"

            # If exact match doesn't exist, try suffix-based mapping
            if not template_file.exists():
                if agent_name.endswith("-tester"):
                    # Try tester.md as fallback
                    template_file = templates_dir / "tester.md"
                elif agent_name.endswith("-reviewer"):
                    # Try reviewer.md as fallback
                    template_file = templates_dir / "reviewer.md"
                elif agent_name.endswith("-developer"):
                    # Try developer.md as fallback
                    template_file = templates_dir / "developer.md"
                elif agent_name.endswith("-specialist"):
                    # Try specialist.md as fallback
                    template_file = templates_dir / "specialist.md"
                else:
                    # Template not available
                    logger.debug(f"Template not found: {agent_name}.md")
                    continue

            if template_file.exists():
                self._copy_template(template_file, output_file, detection)

                if agent_name in existing_agents:
                    print(f"  ✓ Updated: {agent_name}.md")
                    updated_count += 1
                else:
                    print(f"  ✓ Generated: {agent_name}.md")
                    generated_count += 1
            else:
                logger.debug(f"Template not found: {template_file}")

        # Summary message based on mode
        total_processed = generated_count + updated_count
        if total_processed == 0 and self.update_mode != "merge":
            logger.error("No templates could be generated")
            return False

        # Generate SUBAGENT_GUIDE.md
        self._generate_usage_guide(detection, phase_result)

        # Print summary
        print(f"\n📊 Summary:")
        if generated_count > 0:
            print(f"  • Generated: {generated_count} new agent(s)")
        if updated_count > 0:
            print(f"  • Updated: {updated_count} existing agent(s)")
        if skipped_count > 0:
            print(f"  • Preserved: {skipped_count} customized agent(s)")

        logger.info(f"Generated {generated_count}, updated {updated_count}, skipped {skipped_count}")
        return True

    def _copy_template(
        self,
        template_file: Path,
        output_file: Path,
        detection: DetectionResult
    ):
        """
        Copy and customize template.

        Args:
            template_file: Source template
            output_file: Destination file
            detection: Detection results for customization
        """
        # Read template
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple variable substitution
        # (More sophisticated templating can be added later)
        content = content.replace("{{FRAMEWORK}}", detection.framework)
        content = content.replace("{{LANGUAGE}}", detection.language)
        content = content.replace("{{VERSION}}", detection.version or "latest")

        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Created: {output_file}")

    def _generate_usage_guide(self, detection: DetectionResult, phase_result: PhaseResult):
        """
        Generate framework-specific subagent usage guide.

        Args:
            detection: Detection results
            phase_result: Phase detection results
        """
        guide = f"""# Subagent Usage Guide for {detection.framework.upper()} Projects

## 🎯 AGGRESSIVE Mode (Default)

**You installed Adaptive Claude Agents = You want proactive subagent usage.**

This guide was auto-generated based on your project:
- Framework: **{detection.framework}**
- Confidence: **{detection.confidence * 100:.0f}%**
- Language: **{detection.language}**

### 📊 Development Phase: **{phase_result.phase.upper()}**

- Review Rigor: **{phase_result.rigor}/10**
- Description: {phase_result.description}
- Confidence: {phase_result.confidence:.0%}

**What this means for you:**
- Prototype (3/10): Light review - "Does it work?" - Encourages rapid iteration
- MVP (6/10): Moderate review - "Is it secure?" - Balances functionality and quality
- Production (10/10): Strict review - "Is it perfect?" - Enforces comprehensive standards

---

## 🚀 Mandatory Subagent Usage Rules

### ALWAYS Use Task Tool When:

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

---

## 📊 Framework-Specific Workflows

"""

        # Add framework-specific recommendations
        if detection.framework == "nextjs":
            guide += """### Next.js Development

#### Component Development (3+ components)
**Auto-trigger**: Creating/modifying 3+ React components
**Subagent**: `component-reviewer` (proactive)
**Keywords**: "コンポーネント", "component", "Button", "Card", "Modal"

```text
User: "Add new Button, Card, and Modal components"
→ AUTO: Use component-reviewer subagent
```

#### API Routes Testing
**Auto-trigger**: Creating/testing API routes
**Subagent**: `nextjs-tester` + `api-reviewer` (sequential chain)
**Keywords**: "API", "endpoint", "route", "テスト"

```text
User: "Create /api/users endpoint and test it"
→ AUTO: nextjs-tester (create) → api-reviewer (validate)
```

#### Type Safety (5+ files)
**Auto-trigger**: TypeScript errors across multiple files
**Subagent**: `type-checker` (parallel with code changes)
**Keywords**: "型エラー", "type error", "TypeScript", "fix types"

```text
User: "Fix type errors in 5 component files"
→ AUTO: type-checker subagent (parallel execution)
```
"""
        elif detection.framework == "fastapi":
            guide += """### FastAPI Development

#### CRUD Endpoint Development (2+ endpoints)
**Auto-trigger**: Creating 2+ API endpoints
**Subagent**: `api-developer` + `api-reviewer` (sequential)
**Keywords**: "CRUD", "endpoint", "API", "作成"

```text
User: "Add CRUD endpoints for User model"
→ AUTO: api-developer (create) → api-reviewer (validate)
```

#### Async Testing
**Auto-trigger**: Testing async functions
**Subagent**: `fastapi-tester` + `async-checker` (sequential)
**Keywords**: "async", "テスト", "test", "非同期"

```text
User: "Test database queries with async patterns"
→ AUTO: fastapi-tester → async-checker (validate patterns)
```
"""
        elif detection.framework == "go":
            guide += """### Go Development

#### Concurrency Review (MANDATORY)
**Auto-trigger**: Using goroutines/channels in any file
**Subagent**: `concurrency-checker` (mandatory)
**Keywords**: "goroutine", "channel", "並行", "sync"

```text
User: "Review worker pool implementation"
→ AUTO: concurrency-checker (race condition detection)
```

#### Large Refactoring (5+ files)
**Auto-trigger**: Refactoring 5+ files
**Subagent**: `go-reviewer` (proactive)
**Keywords**: "refactor", "リファクタリング", "改善", "error handling"

```text
User: "Refactor error handling across services"
→ AUTO: go-reviewer (idiomatic Go patterns)
```
"""
        elif detection.framework == "flutter":
            guide += """### Flutter Development

#### Widget Development (3+ widgets)
**Auto-trigger**: Creating/modifying 3+ widgets
**Subagent**: `flutter-developer` (proactive)
**Keywords**: "widget", "StatelessWidget", "StatefulWidget", "画面"

```text
User: "Create HomeScreen, ProfileScreen, SettingsScreen"
→ AUTO: flutter-developer subagent
```

#### State Management Review
**Auto-trigger**: Implementing state management
**Subagent**: `flutter-developer` (pattern validation)
**Keywords**: "Provider", "Riverpod", "BLoC", "状態管理"

```text
User: "Implement user authentication with Riverpod"
→ AUTO: flutter-developer (Riverpod best practices)
```
"""
        else:
            # Generic workflow for other frameworks
            guide += f"""### {detection.framework.capitalize()} Development

#### Multi-File Modifications (3+ files)
**Auto-trigger**: Modifying 3+ files with similar patterns
**Subagent**: `general-purpose`

```text
User: "Apply the same fix to file1, file2, file3"
→ AUTO: general-purpose subagent
```

#### Codebase Exploration
**Auto-trigger**: Searching for usage patterns
**Subagent**: `Explore` (thoroughness: "very thorough")

```text
User: "Where is X function used?"
→ AUTO: Explore subagent
```
"""

        guide += """
---

## 💰 Cost vs Time Analysis

| Task Type | Files | Direct Cost | Subagent Cost | Time Saved | **Decision** |
|-----------|-------|-------------|---------------|------------|--------------|
| Single file edit | 1 | 5k tokens | 25k tokens | 0 min | ❌ **Direct** |
| Similar pattern | 3-4 | 15k tokens | 35k tokens | 30 min | ✅ **Subagent** |
| Large refactor | 5+ | 30k tokens | 50k tokens | 60 min | ✅✅ **Subagent** |
| Codebase search | N/A | 40k tokens | 60k tokens | 90 min | ✅✅✅ **Explore** |

**Rule of Thumb**: 20k token overhead is acceptable for 30+ minutes saved.

---

## 🎯 Auto-Trigger Keywords

The following keywords will **automatically trigger** subagent delegation:

"""

        # Add auto-trigger keywords for each recommended subagent
        for agent in detection.recommended_subagents:
            if agent.endswith("-tester"):
                guide += f"- **{agent}**: `テスト`, `test`, `verify`, `検証`, `validation`\n"
            elif agent.endswith("-reviewer"):
                guide += f"- **{agent}**: `レビュー`, `review`, `改善`, `improve`, `validate`\n"
            elif agent.endswith("-checker"):
                guide += f"- **{agent}**: `チェック`, `check`, `lint`, `validate`, `型エラー`\n"
            elif agent.endswith("-developer"):
                guide += f"- **{agent}**: `作成`, `create`, `開発`, `develop`, `implement`\n"

        guide += """
---

## 📈 Success Metrics

Track your efficiency with these targets:

- **Subagent Usage Rate**: 20-30% of complex tasks
- **Time Saved**: 2-4 hours per week
- **Token Efficiency**: Accept 20k overhead for 30+ min saved

### Monitoring

Ask Claude at end of session:
```text
"How many times did you use Task tool today? Show me efficiency stats."
```

---

## 🚫 Common Mistakes to Avoid

1. ❌ **Using subagents for 1-2 file edits** (too expensive)
   - Fix: Use Read/Edit tools directly

2. ❌ **NOT using subagents for 5+ file patterns** (wastes time)
   - Fix: Always delegate to general-purpose

3. ❌ **Serial execution of parallel tasks** (missed opportunity)
   - Fix: Single message with multiple Task tool calls

4. ❌ **Manual grep/glob for codebase searches** (inefficient)
   - Fix: Use Explore subagent with "very thorough"

---

## 🔥 Quick Reference

```text
3+ files → Task tool (general-purpose)
Codebase search → Task tool (Explore, "very thorough")
E2E testing → Task tool (general-purpose + chrome-devtools-tester)
Parallel tasks → Single message, multiple Task tools
```

---

**Generated by**: Adaptive Claude Agents v0.4.2-beta
**Project**: {detection.framework} ({detection.confidence * 100:.0f}% confidence)
**Policy**: AGGRESSIVE (default for all installations)

💡 **Remember**: You installed this tool to maximize efficiency. Trust the subagents!
"""

        # Write to file
        guide_path = self.agents_dir / "SUBAGENT_GUIDE.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)

        logger.info(f"Generated usage guide: {guide_path}")
        print(f"  ✓ Generated: SUBAGENT_GUIDE.md")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze project and generate Claude Code subagents"
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to project root (default: current directory)"
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Skip confirmation prompts"
    )
    parser.add_argument(
        "--update-only",
        action="store_true",
        help="Update only existing subagent files (preserve customizations)"
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Add new templates while backing up existing ones"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force complete regeneration (overwrite all)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine update mode
    update_mode = "generate"  # default
    if args.update_only:
        update_mode = "update-only"
    elif args.merge:
        update_mode = "merge"
    elif args.force:
        update_mode = "force"

    # Run analysis
    analyzer = ProjectAnalyzer(
        project_path=args.project_path,
        auto_confirm=args.auto,
        update_mode=update_mode
    )

    try:
        success = analyzer.analyze()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
