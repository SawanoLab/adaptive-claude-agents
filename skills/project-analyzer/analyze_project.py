#!/usr/bin/env python3
"""
Main entry point for project analysis and subagent generation.

This script:
1. Detects tech stack using detect_stack.py
2. Confirms with user (Progressive Disclosure)
3. Generates appropriate subagents from templates

Usage:
    python analyze_project.py /path/to/project
    python analyze_project.py /path/to/project --auto  # Skip confirmation

Dependencies:
    - Python 3.9+
    - detect_stack.py (in same directory)
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

# Import detection logic
from detect_stack import detect_tech_stack, DetectionResult

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

    def __init__(self, project_path: Path, auto_confirm: bool = False):
        """
        Initialize analyzer.

        Args:
            project_path: Path to project root
            auto_confirm: If True, skip user confirmation
        """
        self.project_path = Path(project_path).resolve()
        self.auto_confirm = auto_confirm
        self.agents_dir = self.project_path / ".claude" / "agents"

        logger.info(f"Analyzing project: {self.project_path}")

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

        # Step 2: Display results
        self._display_detection(detection)

        # Step 3: Confirm with user (Progressive Disclosure)
        if not self.auto_confirm:
            if not self._confirm_generation(detection):
                print("\n❌ Aborted by user")
                return False

        # Step 4: Generate subagents
        print("\n📝 Generating subagents...")
        success = self._generate_subagents(detection)

        if success:
            print("\n✅ Successfully generated subagents!")
            print(f"\n📁 Location: {self.agents_dir}")
            print("\n💡 Next steps:")
            print("  1. Review generated agents: ls .claude/agents/")
            print("  2. Customize as needed")
            print("  3. Commit to version control")
            return True
        else:
            print("\n❌ Failed to generate subagents")
            return False

    def _display_detection(self, detection: DetectionResult):
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

    def _generate_subagents(self, detection: DetectionResult) -> bool:
        """
        Generate subagent files from templates.

        Args:
            detection: Detection results

        Returns:
            True if successful, False otherwise
        """
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
        for agent_name in detection.recommended_subagents:
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
                output_file = self.agents_dir / f"{agent_name}.md"
                self._copy_template(template_file, output_file, detection)
                print(f"  ✓ Generated: {agent_name}.md")
                generated_count += 1
            else:
                logger.debug(f"Template not found: {template_file}")

        if generated_count == 0:
            logger.error("No templates could be generated")
            return False

        logger.info(f"Generated {generated_count} subagents")
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
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Run analysis
    analyzer = ProjectAnalyzer(
        project_path=args.project_path,
        auto_confirm=args.auto
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
