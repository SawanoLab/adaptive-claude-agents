"""Tests for CLI argument parsing and output modes."""

import pytest
import subprocess
import sys
import json
from pathlib import Path


class TestCLIArguments:
    """Test CLI argument parsing."""

    def test_help_flag(self):
        """Test --help flag displays usage information."""
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", "--help"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "usage: detect_stack" in result.stdout
        assert "Detect tech stack and framework" in result.stdout
        assert "--verbose" in result.stdout
        assert "--json" in result.stdout
        assert "Examples:" in result.stdout
        assert "Supported Frameworks:" in result.stdout

    def test_version_flag(self):
        """Test --version flag displays version information."""
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", "--version"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "0.6.0-beta" in result.stdout
        assert "Adaptive Claude Agents" in result.stdout

    def test_short_version_flag(self):
        """Test -v short flag for verbose (not version)."""
        # Note: -v is for verbose, not version
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", ".", "-v"],
            capture_output=True,
            text=True
        )

        # Should have verbose output (not version)
        assert "Starting tech stack detection" in result.stderr or "Starting tech stack detection" in result.stdout


class TestCLIOutputModes:
    """Test different CLI output modes."""

    def test_json_output_mode(self, nextjs_project):
        """Test --json flag outputs valid JSON."""
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", str(nextjs_project), "--json"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0

        # Should be valid JSON
        try:
            data = json.loads(result.stdout)
            assert "framework" in data
            assert "confidence" in data
            assert "language" in data
            assert data["framework"] in ["nextjs", "next.js", "Next.js"]
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON output: {e}\nOutput: {result.stdout}")

    def test_quiet_mode(self, nextjs_project):
        """Test --quiet flag suppresses normal output."""
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", str(nextjs_project), "--quiet"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        # Quiet mode should have no output on success
        assert result.stdout == ""

    def test_verbose_mode(self, nextjs_project):
        """Test --verbose flag shows detailed information."""
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", str(nextjs_project), "--verbose"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        # Verbose should show INFO level logs
        assert "INFO" in result.stderr or "Starting tech stack detection" in result.stderr

    def test_default_output_mode(self, nextjs_project):
        """Test default output mode (human-readable)."""
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", str(nextjs_project)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "Tech Stack Detection Result" in result.stdout
        assert "=" * 60 in result.stdout


class TestCLIErrorHandling:
    """Test CLI error handling and edge cases."""

    def test_no_arguments_uses_current_directory(self, nextjs_project):
        """Test that no arguments defaults to current directory."""
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent.parent / "skills/project-analyzer/detect_stack.py")],
            capture_output=True,
            text=True,
            cwd=str(nextjs_project)
        )

        # Should attempt detection and succeed with nextjs_project
        assert result.returncode == 0

    def test_invalid_path(self):
        """Test handling of invalid/non-existent path."""
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", "/nonexistent/path/12345"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 1

    def test_quiet_mode_on_failure(self):
        """Test --quiet mode suppresses warnings on detection failure."""
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", "/nonexistent", "--quiet"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 1
        # Quiet mode should suppress non-error messages
        # Errors might still show, but warnings should not

    def test_json_mode_with_verbose(self, nextjs_project):
        """Test combining --json with --verbose (JSON should take precedence)."""
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", str(nextjs_project), "--json", "--verbose"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0

        # stdout should be JSON, verbose logs should be in stderr
        try:
            data = json.loads(result.stdout)
            assert "framework" in data
        except json.JSONDecodeError:
            pytest.fail("JSON output should be valid even with --verbose")


class TestCLIBackwardCompatibility:
    """Test backward compatibility with old CLI usage."""

    def test_positional_argument_still_works(self, nextjs_project):
        """Test that old-style positional argument still works."""
        result = subprocess.run(
            [sys.executable, "skills/project-analyzer/detect_stack.py", str(nextjs_project)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "nextjs" in result.stdout.lower() or "next.js" in result.stdout.lower()


# Integration with existing fixtures
@pytest.fixture
def cli_runner():
    """Fixture to run CLI commands."""
    def run(*args, **kwargs):
        cmd = [sys.executable, "skills/project-analyzer/detect_stack.py"] + list(args)
        return subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    return run
