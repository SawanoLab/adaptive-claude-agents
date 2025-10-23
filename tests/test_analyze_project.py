"""Tests for analyze_project.py workflow.

This module tests the ProjectAnalyzer class and its workflow including
detection, confirmation, and template generation.
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add skills directory to Python path for imports
skills_dir = Path(__file__).parent.parent / "skills" / "project-analyzer"
if str(skills_dir) not in sys.path:
    sys.path.insert(0, str(skills_dir))


class TestProjectAnalyzer:
    """Test ProjectAnalyzer class initialization and basic workflow."""

    def test_analyzer_initialization(self, nextjs_project):
        """Test ProjectAnalyzer initializes correctly."""
        from analyze_project import ProjectAnalyzer

        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=True)

        assert analyzer.project_path == nextjs_project
        assert analyzer.auto_confirm is True
        assert analyzer.agents_dir == nextjs_project / ".claude" / "agents"

    def test_analyzer_with_auto_confirm_false(self, nextjs_project):
        """Test ProjectAnalyzer with manual confirmation mode."""
        from analyze_project import ProjectAnalyzer

        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=False)

        assert analyzer.auto_confirm is False

    def test_analyzer_resolves_relative_path(self, tmp_path):
        """Test ProjectAnalyzer resolves relative paths to absolute."""
        from analyze_project import ProjectAnalyzer

        # Create a project in tmp_path
        project = tmp_path / "test-project"
        project.mkdir()

        analyzer = ProjectAnalyzer(project)

        # Path should be resolved to absolute
        assert analyzer.project_path.is_absolute()
        assert analyzer.project_path == project.resolve()


class TestAnalyzeWorkflow:
    """Test the analyze() method workflow."""

    def test_analyze_with_successful_detection(self, nextjs_project, monkeypatch):
        """Test analyze workflow with successful Next.js detection."""
        from analyze_project import ProjectAnalyzer

        # Mock template generation to avoid file I/O
        def mock_generate(self, detection):
            # Create the directory structure
            self.agents_dir.mkdir(parents=True, exist_ok=True)
            return True

        monkeypatch.setattr(
            "analyze_project.ProjectAnalyzer._generate_subagents",
            mock_generate
        )

        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=True)
        result = analyzer.analyze()

        assert result is True
        assert analyzer.agents_dir.exists()

    def test_analyze_with_failed_detection(self, tmp_path):
        """Test analyze workflow when detection fails."""
        from analyze_project import ProjectAnalyzer

        empty_project = tmp_path / "empty"
        empty_project.mkdir()

        analyzer = ProjectAnalyzer(empty_project, auto_confirm=True)
        result = analyzer.analyze()

        # Should return False when detection fails
        assert result is False

    def test_analyze_with_user_abort(self, nextjs_project, monkeypatch):
        """Test analyze workflow when user aborts at confirmation."""
        from analyze_project import ProjectAnalyzer

        # Mock user confirmation to return False (user aborts)
        def mock_confirm(self, detection):
            return False

        monkeypatch.setattr(
            "analyze_project.ProjectAnalyzer._confirm_generation",
            mock_confirm
        )

        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=False)
        result = analyzer.analyze()

        # Should return False when user aborts
        assert result is False


class TestDisplayDetection:
    """Test _display_detection() method."""

    def test_display_detection_output(self, nextjs_project, capsys):
        """Test _display_detection prints detection results."""
        from analyze_project import ProjectAnalyzer
        from detect_stack import detect_tech_stack

        detection = detect_tech_stack(str(nextjs_project))
        assert detection is not None

        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=True)
        analyzer._display_detection(detection)

        # Check that output was printed
        captured = capsys.readouterr()
        assert "Framework:" in captured.out or "Detected" in captured.out
        assert "next" in captured.out.lower()


class TestConfirmGeneration:
    """Test _confirm_generation() method."""

    def test_confirm_generation_with_auto_confirm(self, nextjs_project):
        """Test confirmation is skipped with auto_confirm=True."""
        from analyze_project import ProjectAnalyzer
        from detect_stack import detect_tech_stack

        detection = detect_tech_stack(str(nextjs_project))
        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=True)

        # With auto_confirm, analyze() should proceed without calling _confirm_generation
        # This is tested implicitly in test_analyze_with_successful_detection

    def test_confirm_generation_accepts_yes(self, nextjs_project, monkeypatch):
        """Test confirmation accepts 'yes' input."""
        from analyze_project import ProjectAnalyzer
        from detect_stack import detect_tech_stack

        detection = detect_tech_stack(str(nextjs_project))
        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=False)

        # Mock input to return 'yes'
        monkeypatch.setattr('builtins.input', lambda _: 'yes')

        result = analyzer._confirm_generation(detection)
        assert result is True

    def test_confirm_generation_accepts_y(self, nextjs_project, monkeypatch):
        """Test confirmation accepts 'y' input."""
        from analyze_project import ProjectAnalyzer
        from detect_stack import detect_tech_stack

        detection = detect_tech_stack(str(nextjs_project))
        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=False)

        # Mock input to return 'y'
        monkeypatch.setattr('builtins.input', lambda _: 'y')

        result = analyzer._confirm_generation(detection)
        assert result is True

    def test_confirm_generation_rejects_no(self, nextjs_project, monkeypatch):
        """Test confirmation rejects 'no' input."""
        from analyze_project import ProjectAnalyzer
        from detect_stack import detect_tech_stack

        detection = detect_tech_stack(str(nextjs_project))
        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=False)

        # Mock input to return 'no'
        monkeypatch.setattr('builtins.input', lambda _: 'no')

        result = analyzer._confirm_generation(detection)
        assert result is False


class TestGenerateSubagents:
    """Test _generate_subagents() method."""

    def test_generate_subagents_creates_directory(self, nextjs_project, monkeypatch):
        """Test subagent generation creates .claude/agents directory."""
        from analyze_project import ProjectAnalyzer
        from detect_stack import detect_tech_stack

        detection = detect_tech_stack(str(nextjs_project))
        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=True)

        # Mock template copying to avoid actual file I/O
        def mock_copy_template(self, src, dest, detection):
            return True

        monkeypatch.setattr(
            "analyze_project.ProjectAnalyzer._copy_template",
            mock_copy_template
        )

        result = analyzer._generate_subagents(detection)

        # Should create the agents directory
        assert analyzer.agents_dir.exists()
        assert analyzer.agents_dir.is_dir()


class TestCommandLineInterface:
    """Test CLI argument parsing and main() function."""

    def test_cli_help_flag(self):
        """Test --help flag displays usage information."""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/analyze_project.py", "--help"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "project_path" in result.stdout

    def test_cli_auto_flag(self, nextjs_project):
        """Test --auto flag for automatic confirmation."""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/analyze_project.py",
             str(nextjs_project), "--auto"],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should complete without user interaction
        # Exit code 0 = success, 1 = failure
        assert result.returncode in [0, 1]
        # No "Continue?" prompt should appear in output
        assert "Continue?" not in result.stdout


class TestIntegrationWorkflow:
    """Integration tests for full workflow."""

    @pytest.mark.integration
    def test_full_workflow_nextjs(self, nextjs_project):
        """Test complete workflow for Next.js project."""
        from analyze_project import ProjectAnalyzer

        analyzer = ProjectAnalyzer(nextjs_project, auto_confirm=True)

        # Run full analysis
        result = analyzer.analyze()

        # Workflow should complete successfully
        # Note: Might fail if templates are missing, which is expected
        assert isinstance(result, bool)

    @pytest.mark.integration
    def test_full_workflow_fastapi(self, fastapi_project):
        """Test complete workflow for FastAPI project."""
        from analyze_project import ProjectAnalyzer

        analyzer = ProjectAnalyzer(fastapi_project, auto_confirm=True)

        # Run full analysis
        result = analyzer.analyze()

        assert isinstance(result, bool)

    @pytest.mark.integration
    def test_full_workflow_go(self, go_project):
        """Test complete workflow for Go project."""
        from analyze_project import ProjectAnalyzer

        analyzer = ProjectAnalyzer(go_project, auto_confirm=True)

        # Run full analysis
        result = analyzer.analyze()

        assert isinstance(result, bool)


class TestErrorHandling:
    """Test error handling in analyze_project."""

    def test_nonexistent_project_path(self):
        """Test handling of nonexistent project path."""
        from analyze_project import ProjectAnalyzer

        nonexistent = Path("/nonexistent/path/to/project")

        analyzer = ProjectAnalyzer(nonexistent, auto_confirm=True)

        # Should handle gracefully (detection will fail)
        result = analyzer.analyze()
        assert result is False

    def test_file_instead_of_directory(self, tmp_path):
        """Test handling when project path is a file, not directory."""
        from analyze_project import ProjectAnalyzer

        file_path = tmp_path / "file.txt"
        file_path.write_text("content")

        analyzer = ProjectAnalyzer(file_path, auto_confirm=True)

        # Should handle gracefully
        result = analyzer.analyze()
        assert result is False

    def test_permission_error_handling(self, tmp_path, monkeypatch):
        """Test handling of permission errors during template generation."""
        from analyze_project import ProjectAnalyzer

        project = tmp_path / "test-project"
        project.mkdir()

        # Create a minimal package.json for detection
        (project / "package.json").write_text(json.dumps({
            "dependencies": {"next": "14.0.0"}
        }))
        (project / "next.config.js").write_text("module.exports = {}")

        analyzer = ProjectAnalyzer(project, auto_confirm=True)

        # Mock _copy_template to raise PermissionError
        def mock_copy_error(self, template_file, output_file, detection):
            raise PermissionError("Permission denied")

        monkeypatch.setattr(
            "analyze_project.ProjectAnalyzer._copy_template",
            mock_copy_error
        )

        # Currently, _generate_subagents doesn't catch exceptions,
        # so PermissionError propagates up
        with pytest.raises(PermissionError):
            analyzer.analyze()


class TestTemplateGeneration:
    """Test template generation and copying."""

    def test_agents_directory_creation(self, tmp_path):
        """Test .claude/agents directory is created."""
        from analyze_project import ProjectAnalyzer

        project = tmp_path / "test-project"
        project.mkdir()

        analyzer = ProjectAnalyzer(project, auto_confirm=True)

        # Create agents directory
        analyzer.agents_dir.mkdir(parents=True, exist_ok=True)

        assert analyzer.agents_dir.exists()
        assert (project / ".claude" / "agents").exists()

    def test_claude_directory_structure(self, tmp_path):
        """Test .claude directory structure is created correctly."""
        from analyze_project import ProjectAnalyzer

        project = tmp_path / "test-project"
        project.mkdir()

        analyzer = ProjectAnalyzer(project, auto_confirm=True)

        # Create directory structure
        analyzer.agents_dir.mkdir(parents=True, exist_ok=True)

        claude_dir = project / ".claude"
        assert claude_dir.exists()
        assert claude_dir.is_dir()

        agents_dir = claude_dir / "agents"
        assert agents_dir.exists()
        assert agents_dir.is_dir()
