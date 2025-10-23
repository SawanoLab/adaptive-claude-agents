"""Tests for monorepo detection.

Tests workspace detection for:
- npm workspaces
- pnpm workspaces
- Yarn workspaces
- Lerna
- Nx
- Nested monorepo structures
"""

import pytest
from pathlib import Path


class TestNpmWorkspaces:
    """Test npm workspaces detection."""

    def test_npm_workspaces_detected(self, npm_monorepo, monorepo_detector):
        """Test npm workspaces are correctly detected."""
        detector = monorepo_detector(npm_monorepo)
        result = detector.detect()

        assert result.is_monorepo is True
        assert result.workspace_manager == "npm"
        assert result.root_path == npm_monorepo
        assert len(result.workspaces) == 3  # web, admin, ui

    def test_npm_workspace_names(self, npm_monorepo, monorepo_detector):
        """Test npm workspace names are extracted correctly."""
        detector = monorepo_detector(npm_monorepo)
        result = detector.detect()

        workspace_names = [w.name for w in result.workspaces]
        assert "test-nextjs" in workspace_names  # web app
        assert "test-react" in workspace_names   # admin app
        assert "@test/ui" in workspace_names     # shared package

    def test_npm_workspace_paths(self, npm_monorepo, monorepo_detector):
        """Test npm workspace paths are correct."""
        detector = monorepo_detector(npm_monorepo)
        result = detector.detect()

        for workspace in result.workspaces:
            assert workspace.path.exists()
            assert workspace.path.is_dir()
            assert (workspace.path / "package.json").exists()

    def test_npm_workspace_package_manager(self, npm_monorepo, monorepo_detector):
        """Test npm workspaces have correct package_manager field."""
        detector = monorepo_detector(npm_monorepo)
        result = detector.detect()

        for workspace in result.workspaces:
            assert workspace.package_manager == "npm"


class TestPnpmWorkspaces:
    """Test pnpm workspaces detection."""

    def test_pnpm_workspaces_detected(self, pnpm_monorepo, monorepo_detector):
        """Test pnpm workspaces are correctly detected."""
        detector = monorepo_detector(pnpm_monorepo)
        result = detector.detect()

        assert result.is_monorepo is True
        assert result.workspace_manager == "pnpm"
        assert result.root_path == pnpm_monorepo
        assert len(result.workspaces) == 3  # api, admin, shared

    def test_pnpm_workspace_yaml_parsed(self, pnpm_monorepo, monorepo_detector):
        """Test pnpm-workspace.yaml is correctly parsed."""
        detector = monorepo_detector(pnpm_monorepo)
        result = detector.detect()

        workspace_names = [w.name for w in result.workspaces]
        assert "@test/api" in workspace_names
        assert "@test/admin" in workspace_names
        assert "@test/shared" in workspace_names

    def test_pnpm_workspace_paths(self, pnpm_monorepo, monorepo_detector):
        """Test pnpm workspace paths are correct."""
        detector = monorepo_detector(pnpm_monorepo)
        result = detector.detect()

        # Check services/api exists
        api_found = any(
            "api" in str(w.path) and w.name == "@test/api"
            for w in result.workspaces
        )
        assert api_found

        # Check services/admin exists
        admin_found = any(
            "admin" in str(w.path) and w.name == "@test/admin"
            for w in result.workspaces
        )
        assert admin_found

    def test_pnpm_without_yaml_available(self, pnpm_monorepo, monorepo_detector, monkeypatch):
        """Test pnpm detection handles missing PyYAML gracefully."""
        # Simulate PyYAML not available
        import sys
        from pathlib import Path

        # Add skills directory to Python path
        skills_dir = Path(__file__).parent.parent / "skills" / "project-analyzer"
        if str(skills_dir) not in sys.path:
            sys.path.insert(0, str(skills_dir))

        import detect_monorepo as dm
        monkeypatch.setattr(dm, "YAML_AVAILABLE", False)

        detector = monorepo_detector(pnpm_monorepo)
        result = detector.detect()

        # Should fail gracefully and return non-monorepo result
        assert result.is_monorepo is False


class TestYarnWorkspaces:
    """Test Yarn workspaces detection."""

    def test_yarn_workspaces_detected(self, yarn_monorepo, monorepo_detector):
        """Test Yarn workspaces are correctly detected."""
        detector = monorepo_detector(yarn_monorepo)
        result = detector.detect()

        assert result.is_monorepo is True
        assert result.workspace_manager == "npm"  # Yarn uses npm detection (package.json)
        assert result.root_path == yarn_monorepo
        assert len(result.workspaces) == 2  # api, app

    def test_yarn_workspace_object_format(self, yarn_monorepo, monorepo_detector):
        """Test Yarn workspaces object format {packages: [...]} is parsed."""
        detector = monorepo_detector(yarn_monorepo)
        result = detector.detect()

        workspace_names = [w.name for w in result.workspaces]
        assert "@test/backend-api" in workspace_names
        assert "@test/mobile-app" in workspace_names

    def test_yarn_lock_exists(self, yarn_monorepo):
        """Test yarn.lock file exists in Yarn monorepo."""
        yarn_lock = yarn_monorepo / "yarn.lock"
        assert yarn_lock.exists()


class TestLernaMonorepo:
    """Test Lerna monorepo detection."""

    def test_lerna_monorepo_detected(self, lerna_monorepo, monorepo_detector):
        """Test Lerna monorepo is correctly detected."""
        detector = monorepo_detector(lerna_monorepo)
        result = detector.detect()

        assert result.is_monorepo is True
        assert result.workspace_manager == "lerna"
        assert result.root_path == lerna_monorepo
        assert len(result.workspaces) == 2  # vue-app, react-app

    def test_lerna_json_parsed(self, lerna_monorepo, monorepo_detector):
        """Test lerna.json is correctly parsed."""
        lerna_json = lerna_monorepo / "lerna.json"
        assert lerna_json.exists()

        detector = monorepo_detector(lerna_monorepo)
        result = detector.detect()

        workspace_names = [w.name for w in result.workspaces]
        assert "test-vue" in workspace_names
        assert "test-react" in workspace_names

    def test_lerna_package_manager(self, lerna_monorepo, monorepo_detector):
        """Test Lerna workspaces have correct package_manager field."""
        detector = monorepo_detector(lerna_monorepo)
        result = detector.detect()

        for workspace in result.workspaces:
            assert workspace.package_manager == "lerna"


class TestNxMonorepo:
    """Test Nx monorepo detection."""

    def test_nx_monorepo_detected(self, nx_monorepo, monorepo_detector):
        """Test Nx monorepo is correctly detected."""
        detector = monorepo_detector(nx_monorepo)
        result = detector.detect()

        assert result.is_monorepo is True
        assert result.workspace_manager == "nx"
        assert result.root_path == nx_monorepo
        assert len(result.workspaces) >= 2  # web, api (from workspace.json and project.json)

    def test_nx_workspace_json_parsed(self, nx_monorepo, monorepo_detector):
        """Test Nx workspace.json is correctly parsed."""
        workspace_json = nx_monorepo / "workspace.json"
        assert workspace_json.exists()

        detector = monorepo_detector(nx_monorepo)
        result = detector.detect()

        workspace_names = [w.name for w in result.workspaces]
        assert "web" in workspace_names
        assert "api" in workspace_names

    def test_nx_project_json_detected(self, nx_monorepo, monorepo_detector):
        """Test Nx project.json files are detected (Nx >= 13)."""
        # Check that project.json files exist
        web_project_json = nx_monorepo / "apps" / "web" / "project.json"
        api_project_json = nx_monorepo / "apps" / "api" / "project.json"

        assert web_project_json.exists()
        assert api_project_json.exists()

        detector = monorepo_detector(nx_monorepo)
        result = detector.detect()

        # project.json files should be detected (may duplicate workspace.json entries)
        assert len(result.workspaces) >= 2


class TestNestedMonorepo:
    """Test nested monorepo structures."""

    def test_nested_monorepo_outer_detected(self, nested_monorepo, monorepo_detector):
        """Test outer monorepo is detected in nested structure."""
        detector = monorepo_detector(nested_monorepo)
        result = detector.detect()

        assert result.is_monorepo is True
        assert result.workspace_manager == "npm"
        assert result.root_path == nested_monorepo

    def test_nested_monorepo_inner_workspace(self, nested_monorepo, monorepo_detector):
        """Test inner monorepo can also be detected separately."""
        inner_monorepo = nested_monorepo / "workspaces" / "inner"

        detector = monorepo_detector(inner_monorepo)
        result = detector.detect()

        assert result.is_monorepo is True
        assert result.workspace_manager == "npm"
        # Inner monorepo should have its own workspaces
        assert len(result.workspaces) >= 2


class TestNonMonorepo:
    """Test non-monorepo projects."""

    def test_single_project_not_monorepo(self, nextjs_project, monorepo_detector):
        """Test single Next.js project is not detected as monorepo."""
        detector = monorepo_detector(nextjs_project)
        result = detector.detect()

        assert result.is_monorepo is False
        assert result.workspace_manager is None
        assert result.workspaces == []
        assert result.root_path == nextjs_project

    def test_empty_directory_not_monorepo(self, tmp_path, monorepo_detector):
        """Test empty directory is not detected as monorepo."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        detector = monorepo_detector(empty_dir)
        result = detector.detect()

        assert result.is_monorepo is False
        assert result.workspace_manager is None


class TestMonorepoErrorHandling:
    """Test error handling in monorepo detection."""

    def test_invalid_package_json(self, tmp_path, monorepo_detector):
        """Test handling of invalid package.json."""
        project = tmp_path / "invalid-json"
        project.mkdir()

        # Write invalid JSON
        (project / "package.json").write_text("{invalid json")

        detector = monorepo_detector(project)
        result = detector.detect()

        # Should not crash, should return non-monorepo
        assert result.is_monorepo is False

    def test_invalid_yaml(self, tmp_path, monorepo_detector):
        """Test handling of invalid pnpm-workspace.yaml."""
        project = tmp_path / "invalid-yaml"
        project.mkdir()

        # Write invalid YAML
        (project / "pnpm-workspace.yaml").write_text("packages:\n  - invalid: : :")

        detector = monorepo_detector(project)
        result = detector.detect()

        # Should not crash
        assert result.is_monorepo is False

    def test_missing_workspace_package_json(self, tmp_path, monorepo_detector):
        """Test handling of workspace directories without package.json."""
        import json

        monorepo = tmp_path / "broken-monorepo"
        monorepo.mkdir()

        # Create root package.json with workspaces
        root_pkg = {
            "name": "test",
            "workspaces": ["packages/*"]
        }
        (monorepo / "package.json").write_text(json.dumps(root_pkg))

        # Create workspace directory but no package.json
        packages_dir = monorepo / "packages"
        packages_dir.mkdir()
        broken_pkg = packages_dir / "broken"
        broken_pkg.mkdir()
        # No package.json here

        detector = monorepo_detector(monorepo)
        result = detector.detect()

        # Should detect as monorepo but with no workspaces
        assert result.is_monorepo is True
        assert len(result.workspaces) == 0

    def test_nonexistent_path(self, tmp_path, monorepo_detector):
        """Test handling of nonexistent project path."""
        nonexistent = tmp_path / "does-not-exist"

        detector = monorepo_detector(nonexistent)
        result = detector.detect()

        # Should not crash
        assert result.is_monorepo is False


class TestMonorepoDetectionPriority:
    """Test detection priority when multiple config files exist."""

    def test_pnpm_takes_priority_over_npm(self, tmp_path, monorepo_detector):
        """Test pnpm-workspace.yaml takes priority over package.json workspaces."""
        import json

        monorepo = tmp_path / "mixed-config"
        monorepo.mkdir()

        # Create both npm and pnpm config
        (monorepo / "package.json").write_text(json.dumps({
            "name": "test",
            "workspaces": ["npm/*"]
        }))

        (monorepo / "pnpm-workspace.yaml").write_text("packages:\n  - 'pnpm/*'\n")

        # Create both workspace directories
        (monorepo / "npm").mkdir()
        (monorepo / "pnpm").mkdir()

        detector = monorepo_detector(monorepo)
        result = detector.detect()

        # Should detect as pnpm (higher priority)
        assert result.is_monorepo is True
        assert result.workspace_manager == "pnpm"


class TestMonorepoIntegration:
    """Integration tests for monorepo detection with framework detection."""

    @pytest.mark.integration
    def test_detect_frameworks_in_monorepo_workspaces(
        self, npm_monorepo, monorepo_detector, detector
    ):
        """Test framework detection works for each workspace."""
        monorepo_result = monorepo_detector(npm_monorepo).detect()

        assert monorepo_result.is_monorepo is True

        # Detect framework for each workspace
        for workspace in monorepo_result.workspaces:
            framework_result = detector(str(workspace.path))

            # Workspaces should have detectable frameworks
            if "nextjs" in workspace.name.lower() or workspace.path.name == "web":
                assert framework_result is not None
                assert "next" in framework_result.framework.lower()

            elif "react" in workspace.name.lower() or workspace.path.name == "admin":
                assert framework_result is not None
                # React app (may be detected as React or generic Node.js)

    @pytest.mark.integration
    def test_monorepo_with_mixed_frameworks(
        self, pnpm_monorepo, monorepo_detector, detector
    ):
        """Test monorepo with Python (FastAPI, Flask) and JS workspaces."""
        monorepo_result = monorepo_detector(pnpm_monorepo).detect()

        assert monorepo_result.is_monorepo is True
        assert len(monorepo_result.workspaces) >= 2

        # Check we can detect different frameworks
        frameworks_found = []
        for workspace in monorepo_result.workspaces:
            framework_result = detector(str(workspace.path))
            if framework_result:
                frameworks_found.append(framework_result.framework)

        # Should have detected Python frameworks (FastAPI/Flask)
        python_frameworks = [f for f in frameworks_found if f.lower() in ["fastapi", "flask", "python"]]
        assert len(python_frameworks) >= 1


@pytest.mark.benchmark
class TestMonorepoPerformance:
    """Performance benchmarks for monorepo detection."""

    def test_npm_monorepo_detection_speed(self, npm_monorepo, monorepo_detector, benchmark):
        """Benchmark npm monorepo detection speed."""
        def detect():
            detector = monorepo_detector(npm_monorepo)
            return detector.detect()

        result = benchmark(detect)
        assert result.is_monorepo is True

    def test_large_monorepo_detection(self, tmp_path, monorepo_detector):
        """Test detection performance with large monorepo (20+ workspaces)."""
        import json
        import time

        monorepo = tmp_path / "large-monorepo"
        monorepo.mkdir()

        # Create root package.json
        (monorepo / "package.json").write_text(json.dumps({
            "name": "large-test",
            "workspaces": ["packages/*"]
        }))

        # Create 25 workspace packages
        packages_dir = monorepo / "packages"
        packages_dir.mkdir()

        for i in range(25):
            pkg_dir = packages_dir / f"package-{i}"
            pkg_dir.mkdir()
            (pkg_dir / "package.json").write_text(json.dumps({
                "name": f"@test/package-{i}",
                "version": "1.0.0"
            }))

        # Measure detection time
        start_time = time.perf_counter()
        detector = monorepo_detector(monorepo)
        result = detector.detect()
        elapsed = time.perf_counter() - start_time

        assert result.is_monorepo is True
        assert len(result.workspaces) == 25
        # Should complete in < 5 seconds even with 25 workspaces
        assert elapsed < 5.0
