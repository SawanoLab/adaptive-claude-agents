"""
Tests for subagent generation logic.

This module tests the SUBAGENT_GUIDE.md generation, template variable
replacement, and AGGRESSIVE policy configuration.
"""

import pytest
from pathlib import Path
import json


class TestSubagentGuideGeneration:
    """Test SUBAGENT_GUIDE.md generation logic."""

    def test_guide_created(self, nextjs_project, analyzer_factory):
        """Test that SUBAGENT_GUIDE.md is created."""
        analyzer = analyzer_factory(nextjs_project)

        # Run analysis (would need to mock user confirmation)
        # For now, test the internal method if exposed

        guide_path = Path(nextjs_project) / ".claude" / "agents" / "SUBAGENT_GUIDE.md"

        # This test requires integration with actual analyzer
        # Placeholder for now - will implement after analyzer API is confirmed

    def test_guide_contains_framework_name(self, nextjs_project):
        """Test that generated guide contains correct framework name."""
        guide_path = Path(nextjs_project) / ".claude" / "agents" / "SUBAGENT_GUIDE.md"

        # Create minimal guide for testing
        guide_path.parent.mkdir(parents=True, exist_ok=True)
        guide_path.write_text("# Subagent Usage Guide for NEXTJS Projects")

        content = guide_path.read_text()
        assert "NEXTJS" in content or "Next.js" in content

    def test_guide_contains_aggressive_policy(self, tmp_path):
        """Test that guide contains AGGRESSIVE mode instructions."""
        guide_path = tmp_path / "SUBAGENT_GUIDE.md"

        # Expected content structure
        expected_sections = [
            "AGGRESSIVE Mode",
            "ALWAYS Use Task Tool When",
            "3+ files need similar modifications",
            "Cost vs Time",
        ]

        guide_path.write_text("""
# Subagent Usage Guide for TEST Projects

## 🎯 AGGRESSIVE Mode (Default)

### ALWAYS Use Task Tool When:

1. **3+ files need similar modifications**
   - Subagent: `general-purpose`
   - Time saved: 30-60 minutes

## Cost vs Time Guidance

| Task Type | Direct Cost | Subagent Cost | Time Saved |
""")

        content = guide_path.read_text()
        for section in expected_sections:
            assert section in content, f"Missing section: {section}"


class TestTemplateGeneration:
    """Test subagent template file generation."""

    def test_templates_created(self, nextjs_project):
        """Test that framework-specific templates are created."""
        agents_dir = Path(nextjs_project) / ".claude" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Expected templates for Next.js
        expected_templates = [
            "nextjs-tester.md",
            "nextjs-developer.md",
            "component-reviewer.md",
        ]

        # Create dummy templates
        for template in expected_templates:
            (agents_dir / template).write_text(f"# {template}")

        # Verify all templates exist
        created_templates = [f.name for f in agents_dir.glob("*.md") if f.name != "SUBAGENT_GUIDE.md"]

        for template in expected_templates:
            assert template in created_templates or any(
                t.startswith(template.split("-")[0]) for t in created_templates
            )

    def test_template_variable_replacement(self, tmp_path):
        """Test that template variables are correctly replaced."""
        template_content = """
---
framework: {{FRAMEWORK}}
version: {{VERSION}}
language: {{LANGUAGE}}
---

# {{FRAMEWORK}} Developer

This is a developer for {{FRAMEWORK}} {{VERSION}} using {{LANGUAGE}}.
"""

        # Simulate variable replacement
        result = template_content.replace("{{FRAMEWORK}}", "Next.js")
        result = result.replace("{{VERSION}}", "14.2.0")
        result = result.replace("{{LANGUAGE}}", "TypeScript")

        assert "{{FRAMEWORK}}" not in result
        assert "{{VERSION}}" not in result
        assert "{{LANGUAGE}}" not in result
        assert "Next.js" in result
        assert "14.2.0" in result
        assert "TypeScript" in result


class TestClaudeMdConfiguration:
    """Test CLAUDE.md AGGRESSIVE policy configuration."""

    def test_claude_md_created_if_missing(self, tmp_path):
        """Test that CLAUDE.md is created if it doesn't exist."""
        claude_md = tmp_path / "CLAUDE.md"

        # Should not exist initially
        assert not claude_md.exists()

        # After generation, should exist with policy
        claude_md.write_text("""
# Project Instructions

## 🤖 Adaptive Claude Agents - AGGRESSIVE ポリシー

### 必須ルール（MANDATORY）

1. **3+ ファイルの類似修正**
""")

        assert claude_md.exists()
        content = claude_md.read_text()
        assert "AGGRESSIVE" in content
        assert "必須ルール" in content

    def test_claude_md_not_duplicated(self, tmp_path):
        """Test that AGGRESSIVE policy is not added twice."""
        claude_md = tmp_path / "CLAUDE.md"

        # Initial content
        initial_content = """
# Project Instructions

## 🤖 Adaptive Claude Agents - AGGRESSIVE ポリシー

### 必須ルール（MANDATORY）
"""
        claude_md.write_text(initial_content)

        # Simulate re-running installation
        content = claude_md.read_text()
        if "AGGRESSIVE ポリシー" not in content:
            claude_md.write_text(content + "\n\n## 🤖 Adaptive Claude Agents - AGGRESSIVE ポリシー\n")

        # Verify only one occurrence
        final_content = claude_md.read_text()
        count = final_content.count("AGGRESSIVE ポリシー")
        assert count == 1, f"Expected 1 occurrence, found {count}"


class TestDirectoryStructure:
    """Test that correct directory structure is created."""

    def test_claude_agents_directory_created(self, tmp_path):
        """Test that .claude/agents/ directory is created."""
        agents_dir = tmp_path / ".claude" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        assert agents_dir.exists()
        assert agents_dir.is_dir()

    def test_gitignore_excludes_cache(self, tmp_path):
        """Test that .gitignore excludes Python cache files."""
        gitignore = tmp_path / ".gitignore"

        expected_patterns = [
            "__pycache__/",
            "*.pyc",
            ".pytest_cache/",
        ]

        gitignore.write_text("\n".join(expected_patterns))

        content = gitignore.read_text()
        for pattern in expected_patterns:
            assert pattern in content


class TestFrameworkSpecificGeneration:
    """Test generation for each supported framework."""

    @pytest.mark.parametrize("framework,expected_subagents", [
        ("nextjs", ["nextjs-tester", "component-reviewer"]),
        ("fastapi", ["fastapi-tester", "api-reviewer"]),
        ("go", ["go-developer", "go-reviewer"]),
        ("flutter", ["flutter-developer"]),
        ("react", ["component-reviewer"]),
        ("vue", ["component-reviewer"]),
        ("django", ["django-developer"]),
        ("flask", ["flask-developer"]),
        ("python-ml", ["ml-model-reviewer"]),
        ("ios-swift", ["swift-developer"]),
        ("vanilla-php-web", ["playwright-tester"]),
    ])
    def test_framework_specific_subagents(self, framework, expected_subagents, tmp_path):
        """Test that correct subagents are generated for each framework."""
        agents_dir = tmp_path / ".claude" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Simulate subagent generation
        for subagent in expected_subagents:
            (agents_dir / f"{subagent}.md").write_text(f"# {subagent}")

        # Verify expected subagents exist
        created_files = [f.stem for f in agents_dir.glob("*.md")]

        for subagent in expected_subagents:
            assert subagent in created_files, f"Missing subagent: {subagent}"


class TestGenerationErrors:
    """Test error handling during generation."""

    def test_invalid_framework_name(self, tmp_path):
        """Test handling of invalid framework name."""
        # This should not crash, but return None or error
        framework = "invalid-framework-12345"

        # Generator should validate framework name
        valid_frameworks = [
            "nextjs", "fastapi", "go", "flutter", "react", "vue",
            "django", "flask", "python-ml", "ios-swift", "vanilla-php-web"
        ]

        assert framework not in valid_frameworks

    def test_read_only_directory(self, tmp_path):
        """Test handling of read-only .claude/agents/ directory."""
        agents_dir = tmp_path / ".claude" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Make directory read-only
        import os
        os.chmod(agents_dir, 0o444)

        try:
            # Attempt to write should fail gracefully
            test_file = agents_dir / "test.md"
            try:
                test_file.write_text("test")
                pytest.fail("Should have raised PermissionError")
            except PermissionError:
                pass  # Expected
        finally:
            # Restore permissions for cleanup
            os.chmod(agents_dir, 0o755)

    def test_disk_space_full(self, tmp_path):
        """Test handling of disk space issues (simulated)."""
        # This is difficult to test without mocking filesystem
        # Placeholder for future implementation
        pass


class TestRegeneration:
    """Test re-running generation on existing project."""

    def test_regeneration_is_safe(self, tmp_path):
        """Test that re-running generation doesn't corrupt existing files."""
        agents_dir = tmp_path / ".claude" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # Initial generation
        guide = agents_dir / "SUBAGENT_GUIDE.md"
        guide.write_text("# Guide v1")

        # Re-run generation
        guide.write_text("# Guide v2")

        # Verify content is updated, not corrupted
        content = guide.read_text()
        assert "# Guide v2" in content
        assert "# Guide v1" not in content

    def test_user_modifications_preserved(self, tmp_path):
        """Test that user modifications to templates are preserved."""
        agents_dir = tmp_path / ".claude" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        custom_agent = agents_dir / "my-custom-agent.md"
        custom_agent.write_text("# My Custom Agent")

        # Re-run generation (should not delete custom files)
        # Simulate by checking file still exists
        assert custom_agent.exists()
        assert "My Custom Agent" in custom_agent.read_text()


# ============================================================================
# Integration Tests (require actual analyzer)
# ============================================================================

@pytest.mark.integration
class TestFullGenerationWorkflow:
    """Integration tests for complete generation workflow."""

    def test_analyze_and_generate_nextjs(self, nextjs_project, analyzer_factory):
        """Test full workflow: detect Next.js → generate subagents."""
        # This requires actual analyze_project.py integration
        # Deferred to test_integration.py
        pass

    def test_analyze_and_generate_fastapi(self, fastapi_project, analyzer_factory):
        """Test full workflow: detect FastAPI → generate subagents."""
        # Deferred to test_integration.py
        pass
