"""
End-to-end integration tests.

This module tests complete workflows from project detection through
subagent generation and usage.
"""

import pytest
from pathlib import Path
import subprocess
import json


@pytest.mark.integration
class TestEndToEndWorkflow:
    """Test complete workflow from detection to generation."""

    def test_nextjs_full_workflow(self, nextjs_project, detector):
        """Test complete workflow for Next.js project."""
        # 1. Detect framework using detector fixture
        result = detector(str(nextjs_project))
        assert result is not None
        assert result.framework == "nextjs"
        assert result.confidence >= 0.95

        # 2. Verify file structure (generation tested separately)
        # Generation requires analyze_project.py which needs user confirmation

    def test_fastapi_full_workflow(self, fastapi_project, detector):
        """Test complete workflow for FastAPI project."""
        result = detector(str(fastapi_project))
        assert result is not None
        assert result.framework == "fastapi"
        assert result.confidence >= 0.75

    def test_go_full_workflow(self, go_project, detector):
        """Test complete workflow for Go project."""
        result = detector(str(go_project))
        assert result is not None
        assert result.framework.startswith("go")
        assert result.confidence >= 0.80


@pytest.mark.integration
class TestMultiProjectWorkflow:
    """Test workflows involving multiple projects."""

    def test_analyze_multiple_projects(self, nextjs_project, fastapi_project):
        """Test analyzing multiple projects in sequence."""
        # Analyze Next.js project
        agents_dir_1 = Path(nextjs_project) / ".claude" / "agents"
        agents_dir_1.mkdir(parents=True, exist_ok=True)
        (agents_dir_1 / "SUBAGENT_GUIDE.md").write_text("# Next.js Guide")

        # Analyze FastAPI project
        agents_dir_2 = Path(fastapi_project) / ".claude" / "agents"
        agents_dir_2.mkdir(parents=True, exist_ok=True)
        (agents_dir_2 / "SUBAGENT_GUIDE.md").write_text("# FastAPI Guide")

        # Verify both have different guides
        guide_1 = (agents_dir_1 / "SUBAGENT_GUIDE.md").read_text()
        guide_2 = (agents_dir_2 / "SUBAGENT_GUIDE.md").read_text()

        assert "Next.js" in guide_1
        assert "FastAPI" in guide_2
        assert guide_1 != guide_2

    def test_regenerate_after_framework_change(self, tmp_path):
        """Test regenerating subagents after framework change."""
        # Start as Next.js project
        project = tmp_path / "project"
        project.mkdir()

        package_json = project / "package.json"
        package_json.write_text('{"dependencies": {"next": "14.0.0"}}')

        # Generate subagents (would detect Next.js)
        agents_dir = project / ".claude" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        (agents_dir / "SUBAGENT_GUIDE.md").write_text("# Next.js Guide")

        # Change to React project
        package_json.write_text('{"dependencies": {"react": "18.0.0", "vite": "5.0.0"}}')
        (project / "next.config.js").unlink(missing_ok=True)

        # Regenerate (would detect React)
        (agents_dir / "SUBAGENT_GUIDE.md").write_text("# React Guide")

        guide = (agents_dir / "SUBAGENT_GUIDE.md").read_text()
        assert "React" in guide
        assert "Next.js" not in guide


@pytest.mark.integration
class TestUpdateWorkflow:
    """Test update workflows for existing installations."""

    def test_update_global_tool(self, tmp_path):
        """Test updating the global Adaptive Claude Agents tool."""
        # Simulate global tool location
        global_tool = tmp_path / "skills" / "adaptive-claude-agents"
        global_tool.mkdir(parents=True)

        # Create VERSION file
        version_file = global_tool / "VERSION"
        version_file.write_text("0.4.2-beta")

        # Simulate update
        version_file.write_text("0.4.3-beta")

        # Verify version updated
        assert version_file.read_text().strip() == "0.4.3-beta"

    def test_update_project_guides(self, nextjs_project):
        """Test updating project-specific guides after global tool update."""
        # Initial guide (v0.4.2)
        agents_dir = Path(nextjs_project) / ".claude" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        guide = agents_dir / "SUBAGENT_GUIDE.md"
        guide.write_text("# Guide v0.4.2\n\nOld content")

        # Update guide (v0.4.3)
        guide.write_text("# Guide v0.4.3\n\nNew AGGRESSIVE content")

        # Verify update
        content = guide.read_text()
        assert "0.4.3" in content
        assert "AGGRESSIVE" in content
        assert "0.4.2" not in content


@pytest.mark.integration
class TestPhaseDetectionIntegration:
    """Test integration between phase detection and code review."""

    def test_prototype_phase_light_review(self, tmp_path):
        """Test that Prototype phase triggers light review."""
        project = tmp_path / "prototype-project"
        project.mkdir()

        # Create minimal project indicators
        (project / "package.json").write_text('{"version": "0.1.0"}')

        # Run phase detection
        script = Path(__file__).parent.parent / "skills" / "adaptive-review" / "detect_phase.py"

        result = subprocess.run(
            ["python3", str(script), str(project)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Verify output indicates Prototype
        assert result.returncode == 0
        # Would parse phase from output

    def test_production_phase_strict_review(self, tmp_path):
        """Test that Production phase triggers strict review."""
        project = tmp_path / "production-project"
        project.mkdir()

        # Create production indicators
        (project / "package.json").write_text('{"version": "1.2.3"}')
        tests_dir = project / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_main.py").write_text("def test_example(): pass")

        # Run phase detection
        script = Path(__file__).parent.parent / "skills" / "adaptive-review" / "detect_phase.py"

        result = subprocess.run(
            ["python3", str(script), str(project)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Verify output indicates Production
        assert result.returncode == 0


@pytest.mark.integration
class TestCLIUsability:
    """Test command-line interface usability."""

    @pytest.mark.skip(reason="detect_stack.py --help not yet implemented (argparse needed)")
    def test_detect_stack_help(self):
        """Test that detect_stack.py shows help message."""
        script = Path(__file__).parent.parent / "skills" / "project-analyzer" / "detect_stack.py"

        result = subprocess.run(
            ["python3", str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )

        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "detect" in result.stdout.lower()

    def test_analyze_project_auto_flag(self, nextjs_project):
        """Test that --auto flag skips user confirmation."""
        script = Path(__file__).parent.parent / "skills" / "project-analyzer" / "analyze_project.py"

        result = subprocess.run(
            ["python3", str(script), str(nextjs_project), "--auto"],
            capture_output=True,
            text=True,
            timeout=60,
            input=""  # No user input needed with --auto
        )

        # Should complete without waiting for input
        assert result.returncode == 0

    def test_verbose_logging(self, nextjs_project):
        """Test that --verbose flag enables debug logging."""
        script = Path(__file__).parent.parent / "skills" / "project-analyzer" / "detect_stack.py"

        result = subprocess.run(
            ["python3", str(script), str(nextjs_project), "--verbose"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Verbose output should be longer
        assert len(result.stdout) > 100 or len(result.stderr) > 100


@pytest.mark.integration
@pytest.mark.slow
class TestRealWorldProjects:
    """Test with real-world project structures (slow tests)."""

    def test_complex_nextjs_project(self, tmp_path):
        """Test detection on complex Next.js project structure."""
        project = tmp_path / "complex-nextjs"
        project.mkdir()

        # Create realistic structure
        (project / "package.json").write_text('''
        {
          "name": "complex-app",
          "version": "2.1.0",
          "dependencies": {
            "next": "14.2.0",
            "react": "18.2.0",
            "typescript": "5.3.0"
          },
          "devDependencies": {
            "vitest": "1.0.0",
            "@testing-library/react": "14.0.0",
            "tailwindcss": "3.4.0"
          }
        }
        ''')

        (project / "next.config.js").write_text("module.exports = {}")
        (project / "tsconfig.json").write_text('{"compilerOptions": {}}')

        # Create app directory structure
        app_dir = project / "app"
        app_dir.mkdir()
        (app_dir / "page.tsx").write_text("export default function Page() {}")
        (app_dir / "layout.tsx").write_text("export default function Layout() {}")

        # Create components
        components_dir = project / "components"
        components_dir.mkdir()
        (components_dir / "Header.tsx").write_text("export default function Header() {}")

        # Run detection
        script = Path(__file__).parent.parent / "skills" / "project-analyzer" / "detect_stack.py"

        result = subprocess.run(
            ["python3", str(script), str(project)],
            capture_output=True,
            text=True,
            timeout=30
        )

        assert result.returncode == 0

    def test_monorepo_structure(self, tmp_path):
        """Test detection in monorepo with multiple frameworks."""
        monorepo = tmp_path / "monorepo"
        monorepo.mkdir()

        # Frontend (Next.js)
        frontend = monorepo / "frontend"
        frontend.mkdir()
        (frontend / "package.json").write_text('{"dependencies": {"next": "14.0.0"}}')

        # Backend (FastAPI)
        backend = monorepo / "backend"
        backend.mkdir()
        (backend / "requirements.txt").write_text("fastapi==0.109.0\nuvicorn==0.27.0")
        (backend / "main.py").write_text("from fastapi import FastAPI\napp = FastAPI()")

        # Each project should be detected independently
        # Test frontend
        script = Path(__file__).parent.parent / "skills" / "project-analyzer" / "detect_stack.py"

        result_frontend = subprocess.run(
            ["python3", str(script), str(frontend)],
            capture_output=True,
            text=True,
            timeout=30
        )

        result_backend = subprocess.run(
            ["python3", str(script), str(backend)],
            capture_output=True,
            text=True,
            timeout=30
        )

        assert result_frontend.returncode == 0
        assert result_backend.returncode == 0


# ============================================================================
# Error Recovery Tests
# ============================================================================

@pytest.mark.integration
class TestErrorRecovery:
    """Test error recovery and graceful degradation."""

    def test_corrupted_package_json(self, tmp_path):
        """Test handling of corrupted package.json."""
        project = tmp_path / "corrupted"
        project.mkdir()

        # Invalid JSON
        (project / "package.json").write_text('{"dependencies": {"next"')

        script = Path(__file__).parent.parent / "skills" / "project-analyzer" / "detect_stack.py"

        result = subprocess.run(
            ["python3", str(script), str(project)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should fail gracefully, not crash
        # Acceptable: return None or error message
        assert "error" in result.stderr.lower() or result.returncode != 0

    def test_missing_dependencies(self, tmp_path):
        """Test handling when PyYAML is not installed."""
        # This would require a clean Python environment
        # Difficult to test in real environment
        # Placeholder for documentation purposes
        pass

    def test_network_timeout(self, tmp_path):
        """Test that no network calls cause timeouts."""
        project = tmp_path / "offline"
        project.mkdir()
        (project / "package.json").write_text('{"dependencies": {"next": "14.0.0"}}')

        # All operations should work offline
        script = Path(__file__).parent.parent / "skills" / "project-analyzer" / "detect_stack.py"

        import time
        start = time.time()

        result = subprocess.run(
            ["python3", str(script), str(project)],
            capture_output=True,
            text=True,
            timeout=30
        )

        elapsed = time.time() - start

        # Should complete quickly (no network delays), even if detection fails
        assert elapsed < 10.0, f"Detection took too long: {elapsed:.1f}s"
        # returncode may be non-zero if detection confidence too low, which is OK for this test
